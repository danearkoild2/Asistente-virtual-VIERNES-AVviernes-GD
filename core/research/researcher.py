"""
Viernes — Autonomous Web Research Engine
========================================
Performs deep, multi-step investigation:
1. Deconstructs complex queries into targeted sub-searches.
2. Executes multi-engine searches (SerpApi / Fallback).
3. Reads, extracts, and sanitizes public web sources.
4. Compares perspectives, detects contradictions, separates facts from claims.
5. Synthesizes a structured report with direct numbered citations.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urlparse

from core.research.serpapi_client import SearchResultItem, SerpApiClient
from core.research.web_reader import ExtractedPage, WebReader

logger = logging.getLogger("Viernes.Researcher")


@dataclass
class ResearchReport:
    topic: str
    category: str
    sub_queries: List[str]
    sources: List[Dict[str, Any]]
    summary: str
    full_report: str
    key_facts: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)
    duration_sec: float = 0.0
    provider: str = "SerpApi"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "category": self.category,
            "sub_queries": self.sub_queries,
            "sources": self.sources,
            "summary": self.summary,
            "full_report": self.full_report,
            "key_facts": self.key_facts,
            "contradictions": self.contradictions,
            "duration_sec": self.duration_sec,
            "provider": self.provider,
        }


class ResearchEngine:
    """Autonomous deep research and cross-source analysis engine."""

    def __init__(
        self,
        serp_client: Optional[SerpApiClient] = None,
        web_reader: Optional[WebReader] = None,
        max_subqueries: int = 3,
        max_sources_to_read: int = 5,
        timeout_seconds: float = 40.0,
    ):
        self.serp_client = serp_client or SerpApiClient.get_instance()
        self.web_reader = web_reader or WebReader()
        self.max_subqueries = max_subqueries
        self.max_sources_to_read = max_sources_to_read
        self.timeout_seconds = timeout_seconds

    def research(
        self,
        topic: str,
        category: str = "general",
        on_progress: Optional[Callable[[str, str, Dict[str, Any]], None]] = None,
    ) -> ResearchReport:
        """
        Execute full autonomous research workflow.
        category: 'general' | 'news' | 'scholar' | 'tech' | 'products' | 'media'
        """
        t0 = time.time()
        topic = (topic or "").strip()
        if not topic:
            return ResearchReport(
                topic="",
                category=category,
                sub_queries=[],
                sources=[],
                summary="No se proporcionó un tema de investigación.",
                full_report="Error: Consulta vacía.",
            )

        def _notify(stage: str, msg: str, data: Optional[Dict[str, Any]] = None):
            if on_progress:
                try:
                    on_progress(stage, msg, data or {})
                except Exception:
                    pass

        # ── 1. Plan Sub-queries ──────────────────────────────────────────────
        _notify("PLANNING", f"Planificando investigación para: '{topic}'...", {"topic": topic})
        sub_queries = self._generate_subqueries(topic, category)
        _notify("PLANNED", f"Generadas {len(sub_queries)} sub-consultas de exploración.", {"sub_queries": sub_queries})

        # ── 2. Universal Multi-Search via SerpApi ────────────────────────────
        all_results: List[SearchResultItem] = []
        engine_map = {
            "general": "google",
            "news": "google_news",
            "scholar": "google_scholar",
            "tech": "google",
            "products": "google_shopping",
            "media": "youtube",
        }
        primary_engine = engine_map.get(category, "google")

        seen_links = set()
        for idx, sq in enumerate(sub_queries):
            _notify("SEARCHING", f"Consultando fuentes: '{sq}' ({idx+1}/{len(sub_queries)})...", {"query": sq})
            results = self.serp_client.search(
                query=sq,
                engine=primary_engine,
                num=6,
                use_cache=True,
            )
            for item in results:
                # Deduplicate by link or domain
                parsed = urlparse(item.link)
                clean_link = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")
                if clean_link and clean_link not in seen_links:
                    seen_links.add(clean_link)
                    all_results.append(item)

        _notify("SEARCH_DONE", f"Recopilados {len(all_results)} resultados iniciales.", {"count": len(all_results)})

        if not all_results:
            return ResearchReport(
                topic=topic,
                category=category,
                sub_queries=sub_queries,
                sources=[],
                summary="No se encontraron fuentes disponibles para esta consulta.",
                full_report="No se pudo obtener información verificable en las fuentes consultadas.",
                duration_sec=time.time() - t0,
            )

        # ── 3. Select & Read Top Web Pages ───────────────────────────────────
        # Filter and rank candidates (skip common unparseable or login portals)
        candidates = []
        for r in all_results:
            low_link = r.link.lower()
            if not r.link.startswith("http"):
                continue
            if any(block in low_link for block in ("login", "signin", "accounts.google", "facebook.com", "instagram.com")):
                continue
            candidates.append(r)

        selected_candidates = candidates[:self.max_sources_to_read]
        read_pages: List[Tuple[SearchResultItem, ExtractedPage]] = []

        for idx, cand in enumerate(selected_candidates):
            _notify(
                "READING",
                f"Leyendo fuente [{idx+1}/{len(selected_candidates)}]: {cand.title[:45]}...",
                {"url": cand.link, "title": cand.title, "index": idx + 1, "total": len(selected_candidates)},
            )
            try:
                page = self.web_reader.fetch_page(cand.link, try_playwright_if_empty=False)
                if page.word_count >= 40:
                    read_pages.append((cand, page))
            except Exception as e:
                logger.warning(f"Error reading {cand.link}: {e}")

        # ── 4. Cross-Source Analysis & Synthesis ─────────────────────────────
        _notify("ANALYZING", "Sintetizando información y contrastando fuentes...", {"sources_read": len(read_pages)})

        sources_payload = []
        source_texts_context = []

        for idx, (res_item, page) in enumerate(read_pages, 1):
            domain = urlparse(res_item.link).netloc
            sources_payload.append({
                "id": idx,
                "title": res_item.title or page.title,
                "link": res_item.link,
                "domain": domain,
                "snippet": res_item.snippet,
                "words": page.word_count,
            })
            source_texts_context.append(
                f"--- FUENTE [{idx}]: {res_item.title} ({domain}) ---\n"
                f"URL: {res_item.link}\n"
                f"CONTENIDO:\n{page.text[:3500]}\n"
            )

        # If no page content could be read, use the search snippets
        if not source_texts_context:
            for idx, res_item in enumerate(all_results[:6], 1):
                domain = urlparse(res_item.link).netloc
                sources_payload.append({
                    "id": idx,
                    "title": res_item.title,
                    "link": res_item.link,
                    "domain": domain,
                    "snippet": res_item.snippet,
                    "words": 0,
                })
                source_texts_context.append(
                    f"--- FUENTE [{idx}]: {res_item.title} ({domain}) ---\n"
                    f"URL: {res_item.link}\n"
                    f"FRAGMENTO: {res_item.snippet}\n"
                )

        full_report, summary, key_facts, contradictions = self._synthesize_report(
            topic=topic,
            category=category,
            sources_context="\n\n".join(source_texts_context),
            sources_list=sources_payload,
        )

        duration = time.time() - t0
        _notify("COMPLETE", f"Investigación finalizada en {duration:.1f}s.", {"duration": duration})

        provider = "SerpApi" if self.serp_client.is_configured() else "Web Search"

        return ResearchReport(
            topic=topic,
            category=category,
            sub_queries=sub_queries,
            sources=sources_payload,
            summary=summary,
            full_report=full_report,
            key_facts=key_facts,
            contradictions=contradictions,
            duration_sec=duration,
            provider=provider,
        )

    def _generate_subqueries(self, topic: str, category: str) -> List[str]:
        """Generate targeted sub-queries for deep investigation."""
        # 1. Try Gemini FAST model for semantic subquery breakdown
        try:
            from core import gemini
            prompt = (
                f"Descompón el siguiente tema en 2 o 3 consultas de búsqueda web precisas y complementarias para investigar a fondo.\n"
                f"Categoría: {category}\n"
                f"Tema: {topic}\n"
                f"Responde ÚNICAMENTE con las consultas, una por línea, sin numeración ni viñetas ni explicaciones adicionales."
            )
            resp = gemini.call(prompt, tier=gemini.FAST, timeout_ms=8000)
            if resp and resp.text:
                lines = [line.strip() for line in resp.text.split("\n") if line.strip() and not line.strip().startswith("#")]
                clean = [re.sub(r"^[\d\.\-\*\•\>\s]+", "", l).strip() for l in lines]
                valid = [c for c in clean if len(c) > 3][:self.max_subqueries]
                if valid:
                    return valid
        except Exception:
            pass

        # 2. Heuristic fallback based on category
        if category == "news":
            return [
                f"{topic} últimas noticias hoy",
                f"{topic} desarrollo reciente declaraciones",
            ]
        elif category == "scholar":
            return [
                f"{topic} scientific paper research study",
                f"{topic} methodology results conclusions",
            ]
        elif category == "tech":
            return [
                f"{topic} documentation guide architecture",
                f"{topic} github repository benchmarks",
            ]
        elif category == "products":
            return [
                f"{topic} precio especificaciones características",
                f"{topic} review opiniones comparativa",
            ]
        else:
            return [
                topic,
                f"{topic} qué es detalles clave actualidad",
                f"{topic} análisis perspectivas puntos de vista",
            ]

    def _synthesize_report(
        self,
        topic: str,
        category: str,
        sources_context: str,
        sources_list: List[Dict[str, Any]],
    ) -> Tuple[str, str, List[str], List[str]]:
        """Synthesize facts, detect disagreements, and format full report with citations."""
        # Build prompt for Gemini SMART
        prompt = f"""Eres VIERNES, una asistente de investigación avanzada con rigor analítico.
Tu tarea es analizar y sintetizar información extraída de la web sobre el siguiente tema:

TEMA DE INVESTIGACIÓN: {topic}
CATEGORÍA: {category}

FUENTES CONSULTADAS:
{sources_context}

INSTRUCCIONES OBLIGATORIAS:
1. Utiliza ÚNICAMENTE la información provista en las fuentes anteriores. NO inventes hechos, citas ni URLs.
2. Cada afirmación clave debe incluir su cita de fuente numérica entre corchetes, por ejemplo [1], [2].
3. Estructura el informe con el siguiente formato Markdown:
   # ◈ INVESTIGACIÓN: {topic.upper()}
   
   ## RESUMEN EJECUTIVO
   (Síntesis clara y directa en 2 o 3 párrafos con citas [x])
   
   ## HALLAZGOS Y DATOS CLAVE
   - Dato o hecho relevante comprobado [x]
   - Dato técnico, estadística o cronología [y]
   
   ## ANÁLISIS DE PERSPECTIVAS Y CONTRASTES
   (Compara fuentes. Si hay acuerdos o contradicciones/discrepancias entre las fuentes, indícalo explícitamente distinguiendo hechos de opiniones).
   
   ## FUENTES CONSULTADAS
   (Lista numerada con [1] Título - URL, [2] Título - URL)

Genera el informe completo con tono profesional, objetivo y preciso en español."""

        full_text = ""
        try:
            from core import gemini
            resp = gemini.call(prompt, tier=gemini.SMART, timeout_ms=30_000)
            if resp and resp.text:
                full_text = resp.text.strip()
        except Exception as e:
            logger.warning(f"Gemini synthesis call failed: {e}")

        # Fallback local synthesis if Gemini is unavailable
        if not full_text:
            lines = [
                f"# ◈ INVESTIGACIÓN: {topic.upper()}",
                "",
                "## RESUMEN EJECUTIVO",
                f"Se consultaron {len(sources_list)} fuentes principales sobre el tema solicitado.",
                "",
                "## HALLAZGOS CLAVE",
            ]
            for s in sources_list:
                lines.append(f"- **{s['title']}** [{s['id']}]: {s['snippet']}")
            lines.append("")
            lines.append("## FUENTES CONSULTADAS")
            for s in sources_list:
                lines.append(f"[{s['id']}] {s['title']} — {s['link']}")
            full_text = "\n".join(lines)

        # Extract summary paragraph
        summary = ""
        m = re.search(r"##\s*RESUMEN EJECUTIVO\s*\n(.*?)(?=\n##|\Z)", full_text, re.DOTALL)
        if m:
            summary = m.group(1).strip()
        else:
            summary = full_text[:400].strip()

        # Extract Key Facts
        key_facts = []
        for line in full_text.split("\n"):
            line_str = line.strip()
            if line_str.startswith("- ") and "[" in line_str and "]" in line_str:
                key_facts.append(line_str[2:].strip())

        # Extract Contradictions / Contrasts if mentioned
        contradictions = []
        m_contr = re.search(r"##\s*ANÁLISIS DE PERSPECTIVAS.*?\n(.*?)(?=\n##|\Z)", full_text, re.DOTALL)
        if m_contr:
            c_text = m_contr.group(1).strip()
            for sentence in c_text.split(". "):
                low = sentence.lower()
                if any(w in low for w in ("discrep", "contrad", "difer", "sin embargo", "mientras que", "a diferencia")):
                    contradictions.append(sentence.strip())

        return full_text, summary, key_facts[:8], contradictions[:5]
