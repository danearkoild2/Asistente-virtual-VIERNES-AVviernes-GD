"""
Viernes — Edith Contextual Visual Intelligence Engine
=====================================================
Analyzes queries and conversations to detect visual topics (monuments, science,
nature, astronomy, art, technology, etc.), tracks conversational follow-ups,
and fetches high-quality images via SerpAPI with caching and local buffering.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx

from memory.config_manager import get_base_dir
from core.research.serpapi_client import SerpApiClient

logger = logging.getLogger("Viernes.VisualEngine")

CACHE_DIR = get_base_dir() / "config" / "visual_cache"
IMG_CACHE_DIR = CACHE_DIR / "images"


@dataclass
class VisualCardData:
    topic: str
    category: str
    summary: str
    interesting_fact: str
    images: List[Dict[str, str]] = field(default_factory=list)  # [{'url', 'thumb', 'local_path', 'local_thumb', 'title', 'source'}]
    source: str = "Google Images / SerpAPI"
    query: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "category": self.category,
            "summary": self.summary,
            "interesting_fact": self.interesting_fact,
            "images": self.images,
            "source": self.source,
            "query": self.query,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> VisualCardData:
        return cls(
            topic=data.get("topic", ""),
            category=data.get("category", "EXPLORACIÓN VISUAL"),
            summary=data.get("summary", ""),
            interesting_fact=data.get("interesting_fact", ""),
            images=data.get("images", []),
            source=data.get("source", "Google Images"),
            query=data.get("query", ""),
            timestamp=data.get("timestamp", time.time()),
        )


class VisualQueryDetector:
    """
    Intelligent detector for visual context, entity identification,
    and conversational continuation tracking.
    """

    # Explicit visual requests (Highest confidence)
    EXPLICIT_VISUAL_PATTERNS = [
        # Match anything asking for photos/images even if preceded by "busca en internet", "en la red", etc.
        r"(?:mu[eé]strame|ens[eé][nñ]ame|pon|muestra|ver|quiero ver|busca|b[uú]scame|dame)\s+.*?(?:fotos?|im[aá]genes?|una foto|una imagen|ilustraci[oó]n|c[oó]mo es|c[oó]mo se ve|c[oó]mo luce)\s+(?:de\s+|del\s+|sobre\s+)?(.+)",
        r"(?:fotos?|im[aá]genes?)\s+(?:de\s+|del\s+|sobre\s+)?(.+)",
        r"c[oó]mo (?:es|se ve|luce|es el aspecto de)\s+(?:un|una|el|la|los|las)?\s*(.+)",
        r"(?:busca|b[uú]scame|investiga)\s+(?:en internet|en la red|en google|en la web)\s+(?:sobre|acerca de|de|del|fotos de|im[aá]genes de)?\s*(.+)",
        r"(?:busca|b[uú]scame|consultar|investiga)\s+(?:informaci[oó]n\s+(?:de|sobre)|datos\s+(?:de|sobre))\s+(.+)",
    ]

    # Topics that strongly benefit from visual display
    VISUAL_DOMAIN_KEYWORDS = {
        "ASTRONOMÍA Y ESPACIO": [
            "agujero negro", "planeta", "galaxia", "nebulosa", "supernova", "saturno", "jupiter", "júpiter",
            "marte", "venus", "mercurio", "urano", "neptuno", "telescopio james webb", "hubble",
            "estaci[oó]n espacial", "pulsar", "qu[aá]sar", "asteroide", "cometa", "eclipse", "aurora boreal",
            "sol", "luna", "sistema solar", "v[ií]a l[aá]ctea", "andromeda", "andr[oó]meda"
        ],
        "MONUMENTOS Y ARQUITECTURA": [
            "machu picchu", "torre eiffel", "coliseo", "pir[aá]mides?", "taj mahal", "muralla china",
            "cristo redentor", "gran ca[nñ][oó]n", "cataratas", "everest", "parten[oó]n", "sagrada familia",
            "acropolis", "acr[oó]polis", "chichen itza", "chich[eé]n itz[aá]", "petra", "stonehenge",
            "big ben", "estatua de la libertad", "burj khalifa", "catedral de notre dame", "alhambra",
            "angkor wat", "monte fuji", "opera de sydney", "[oó]pera de s[ií]dney", "torre de pisa"
        ],
        "GASTRONOMÍA Y CULTURA": [
            "gallo pinto", "arroz con pollo", "ceviche", "tamal", "tamales", "tacos?", "paella", "sushi",
            "arepas?", "empanadas?", "asado", "mole", "pizza", "ramen", "croissant", "pasta", "caf[eé]",
            "chocolate", "vino", "plato t[ií]pico", "comida tradicional", "platillo", "gastronom[ií]a",
            "receta", "ingredientes?", "bebida tradicional", "postre", "dulce t[ií]pico"
        ],
        "ANIMALES Y NATURALEZA": [
            "le[oó]n", "tigre", "ballena", "delf[ií]n", "tibur[oó]n", "panda", "lobo", "[aá]guila",
            "leopardo", "guepardo", "oso polar", "colibr[ií]", "pulpo", "calamar gigante", "orca",
            "elefante", "jirafa", "camale[oó]n", "ajolote", "axolotl", "dinosaurio", "t-rex",
            "tiranosaurio", "pterod[aá]ctilo", "arrecife de coral", "selva amaz[oó]nica", "bosque de secuoyas",
            "capibara", "carpincho", "perro", "gato", "caballo", "oso", "zorro", "nutria", "koala", "canguro"
        ],
        "FLORA Y BOTÁNICA": [
            "orqu[ií]dea", "rosa", "girasol", "planta carn[ií]vora", "bons[aá]i", "secuoya", "baobab",
            "cactus", "[aá]rbol", "flor", "hongo", "coral", "loto", "bamb[uú]", "cerezo"
        ],
        "CIENCIA Y TECNOLOGÍA": [
            "computadora cu[aá]ntica", "procesador", "microscopio", "adn", "estructura del adn",
            "c[eé]lula", "acelerador de part[ií]culas", "cern", "reactor de fusi[oó]n", "tokamak",
            "robot", "boston dynamics", "motor de avi[oó]n", "turbina", "cohete", "falcon 9",
            "starship", "rover de marte", "curiosity", "perseverance", "nanotubo de carbono",
            "ferrari", "lamborghini", "porsche", "tesla", "bugatti", "mclaren", "auto", "carro", "veh[ií]culo",
            "iphone", "smartphone", "tarjeta gr[aá]fica", "rtx", "playstation", "xbox", "nintendo"
        ],
        "ARTE E HISTORIA": [
            "mona lisa", "la gioconda", "noche estrellada", "david de miguel [aá]ngel", "el grito",
            "guernica", "la [uú]ltima cena", "el nacimiento de venus", "sarc[oó]fago", "tutankam[oó]n",
            "armadura medieval", "casco espartano", "samur[aá]i", "pergamino", "fara[oó]n"
        ],
        "GEOGRAFÍA Y LUGARES": [
            "volc[aá]n", "glaciar", "fiordo", "desierto del sahara", "salinas de uyuni", "cueva",
            "islas gal[aá]pagos", "maldivas", "santorini", "venecia", "kioto", "parque yellowstone",
            "fosa de las marianas", "atol[oó]n", "isla de pascua"
        ]
    }

    # Informative inquiry patterns covering questions about entities, places, food, concepts
    INQUIRY_PATTERNS = [
        # "Quiero información de/sobre/del X", "Dame información de X", "Información de X"
        r"^(?:edith|viernes|oye)?\s*[\,\;]?\s*(?:quiero|dame|necesito|busca|tienes)?\s*(?:m[aá]s\s+)?informaci[oó]n\s+(?:del?|de la|de los|de las|sobre)\s+(.+)",
        # "Quiero saber de/sobre X", "Qué sabes de/sobre X", "Cuéntame de/sobre X", "Háblame de/sobre X", "Dime de/sobre X"
        r"^(?:edith|viernes|oye)?\s*[\,\;]?\s*(?:quiero\s+saber|qu[eé]\s+sabes|cu[eé]ntame|h[aá]blame|expl[ií]came|dime)\s+(?:m[aá]s\s+)?(?:del?|de la|de los|de las|sobre)\s+(.+)",
        # "¿Qué es X?", "¿Quién fue X?", "¿Dónde queda X?", "¿Cómo funciona X?", "¿Cómo se prepara X?"
        r"^(?:edith|viernes|oye)?\s*[\,\;]?\s*(?:busca\s+)?(?:en\s+internet\s+)?(?:qu[eé]\s+es|qu[eé]\s+son|qu[ií][eé]n\s+(?:es|fue|era)|d[oó]nde\s+(?:est[aá]|queda)|c[oó]mo\s+funciona|c[oó]mo\s+se\s+(?:hace|prepara|construye))\s+(?:un|una|el|la|los|las)?\s*(.+)",
        # "Busca X en internet", "Busca X"
        r"^(?:edith|viernes|oye)?\s*[\,\;]?\s*(?:busca|b[uú]scame|investiga)\s+(?:a\s+|al\s+|el\s+|la\s+|los\s+|las\s+|un\s+|una\s+)?(.+?)(?:\s+en\s+internet|\s+en\s+la\s+red|\s+en\s+google|$)",
        # "¿Conoces X?", "¿Has escuchado sobre X?", "¿Has probado X?"
        r"^(?:edith|viernes|oye)?\s*[\,\;]?\s*(?:conoces|has\s+escuchado|has\s+visto|has\s+probado)\s+(?:del?|de la|de los|de las|el|la|los|las|un|una|sobre)?\s*(.+)",
    ]

    # Non-visual / rejection patterns
    NON_VISUAL_PATTERNS = [
        r"^(?:hola|buenos d[ií]as|buenas tardes|buenas noches|hey|qu[eé] tal|c[oó]mo est[aá]s|qu[ií][eé]n eres|c[oó]mo te llamas)\b",
        r"^(?:gracias|de nada|perfecto|ok|genial|entendido|adi[oó]s|chao|hasta luego)\b",
        r"^(?:cu[aá]nto es|calcula|suma|resta|multiplica|divide|\d+\s*[\+\-\*\/]\s*\d+)",
        r"(?:escribe|crea|corrige|programa|c[oó]digo|script|funci[oó]n|python|javascript|bash|powershell|sql|html)\b",
        r"^(?:silencio|c[aá]llate|du[eé]rmete|descansa|despierta|modo reposo|apaga|reinicia|sube el volumen|baja el volumen)\b",
        r"(?:qu[eé] hora es|qu[eé] fecha es|qu[eé] d[ií]a es|dime la hora)\b",
        r"(?:qu[eé] opinas|cu[aá]l es tu opini[oó]n|cu[aá]l es el sentido de la vida|qu[eé] piensas)\b",
    ]

    # Follow-up conversational queries referring to active context
    FOLLOW_UP_PATTERNS = [
        r"^(?:y\s+)?c[oó]mo\s+(?:lo|la|los|las)\s+(?:construyeron|hicieron|crearon|descubrieron)",
        r"^(?:y\s+)?qui[eé]n\s+(?:lo|la|los|las)\s+(?:construy[oó]|hizo|cre[oó]|descubri[oó]|gobernaba)",
        r"^(?:y\s+)?d[oó]nde\s+(?:est[aá]|queda|se encuentra)(?:\s+exactamente)?",
        r"^(?:y\s+)?cu[aá]ntos\s+a[nñ]os\s+tiene",
        r"^(?:y\s+)?en\s+qu[eé]\s+a[nñ]o",
        r"^(?:y\s+)?de\s+qu[eé]\s+est[aá]\s+hech[oa]",
        r"^(?:y\s+)?por\s+qu[eé]\s+(?:es|fue|se llama)",
        r"^(?:cu[eé]ntame|dime|h[aá]blame)\s+m[aá]s\s+(?:de\s+(?:eso|ello)|sobre\s+(?:eso|ello))",
    ]

    def __init__(self):
        self._last_entity: Optional[str] = None
        self._last_category: str = "EXPLORACIÓN VISUAL"

    def analyze(self, user_query: str, assistant_response: str = "") -> Optional[Tuple[str, str, float]]:
        """
        Analyzes the query and response.
        Returns Tuple of (entity_topic, category, confidence) if visual, or None.
        """
        q = (user_query or "").strip().lower()
        if not q or len(q) < 3:
            return None

        # Clean punctuation from query for matching
        q_clean = re.sub(r"[¿?¡!]", "", q).strip()

        # Check negative/non-visual patterns
        for n_pat in self.NON_VISUAL_PATTERNS:
            if re.search(n_pat, q_clean, re.IGNORECASE):
                return None

        # 1. Check Follow-Up context query
        if self._last_entity:
            for f_pat in self.FOLLOW_UP_PATTERNS:
                if re.search(f_pat, q_clean, re.IGNORECASE):
                    logger.info(f"Follow-up context detected for entity: '{self._last_entity}'")
                    return (self._last_entity, self._last_category, 0.95)

        # 2. Check Explicit Visual Request ("Muéstrame fotos de Machu Picchu")
        for exp_pat in self.EXPLICIT_VISUAL_PATTERNS:
            m = re.search(exp_pat, q_clean, re.IGNORECASE)
            if m:
                topic = m.group(1).strip()
                topic = self._clean_topic(topic)
                if topic:
                    cat = self._detect_category(topic, assistant_response)
                    self._last_entity = topic
                    self._last_category = cat
                    return (topic, cat, 1.0)

        # 3. Check Domain Keywords in query
        for cat, kw_list in self.VISUAL_DOMAIN_KEYWORDS.items():
            for kw in kw_list:
                pattern = r"\b" + re.escape(kw) + r"\b"
                if re.search(pattern, q_clean, re.IGNORECASE):
                    # Matched domain keyword
                    topic = kw.title()
                    # If an inquiry pattern contains the keyword, extract full specific topic
                    for inq_pat in self.INQUIRY_PATTERNS:
                        m_inq = re.search(inq_pat, q_clean, re.IGNORECASE)
                        if m_inq:
                            extracted = self._clean_topic(m_inq.group(1).strip())
                            if extracted and len(extracted) >= len(topic):
                                topic = extracted.title()
                    self._last_entity = topic
                    self._last_category = cat
                    return (topic, cat, 0.92)

        # 4. Check Informative Inquiry Patterns ("Quiero información del gallo pinto de Costa Rica", "¿Qué es X?")
        for inq_pat in self.INQUIRY_PATTERNS:
            m = re.search(inq_pat, q_clean, re.IGNORECASE)
            if m:
                topic = m.group(1).strip()
                topic = self._clean_topic(topic)
                if topic and len(topic) >= 3:
                    cat = self._detect_category(topic, assistant_response)
                    # Check if the topic or response contains visual markers, or category is specific
                    if self._is_visual_entity(topic, assistant_response) or cat != "EXPLORACIÓN VISUAL":
                        self._last_entity = topic
                        self._last_category = cat
                        return (topic, cat, 0.88)
                    # If response is substantial and discusses the topic
                    if len(assistant_response) > 30 and not self._is_abstract_text(assistant_response):
                        self._last_entity = topic
                        self._last_category = cat
                        return (topic, cat, 0.82)

        # 5. Extract entity from Assistant definition response ("El gallo pinto es un plato tradicional...")
        if assistant_response and len(assistant_response) > 25:
            def_match = re.search(
                r"^([A-ZÁÉÍÓÚ][\w\s\-\'\’]{2,40}?)\s+es\s+(?:un|una|el|la|uno de los|una de las)\s+([\w\s]+?)(?:[\.,;]|$|\s+que\b)",
                assistant_response.strip()
            )
            if def_match:
                cand_topic = self._clean_topic(def_match.group(1))
                predicate = def_match.group(2)
                if self._is_visual_entity(cand_topic, predicate):
                    cat = self._detect_category(cand_topic, predicate)
                    self._last_entity = cand_topic
                    self._last_category = cat
                    return (cand_topic, cat, 0.85)

        # 6. Fallback: Check Assistant Response for high visual density if query asked something informative
        if len(assistant_response) > 40:
            for cat, kw_list in self.VISUAL_DOMAIN_KEYWORDS.items():
                for kw in kw_list:
                    if re.search(r"\b" + re.escape(kw) + r"\b", assistant_response, re.IGNORECASE):
                        topic = kw.title()
                        self._last_entity = topic
                        self._last_category = cat
                        return (topic, cat, 0.8)

        return None

    def _clean_topic(self, topic: str) -> str:
        # Strip trailing punctuation, polite phrases, extra words
        topic = re.sub(r"[¿?¡!.,;]", "", topic).strip()
        noise = [
            r"^(?:del|de la|de los|de las|de un|de una|de|al)\s+",
            r"^(?:un|una|el|la|los|las)\s+",
            r"^(?:sobre|acerca de)\s+",
            r"^(?:en internet|de internet|en la red|en google|en la web|fotos de|im[aá]genes de)\s+",
            r"\s+(?:en internet|de internet|en la red|en google|en la web)$",
            r"\s+(?:por favor|edith|viernes)$",
        ]
        changed = True
        while changed:
            changed = False
            for n in noise:
                new_t = re.sub(n, "", topic, flags=re.IGNORECASE).strip()
                if new_t != topic:
                    topic = new_t
                    changed = True
        return topic.strip()

    def _detect_category(self, topic: str, response: str) -> str:
        text = f"{topic} {response}".lower()
        for cat, kw_list in self.VISUAL_DOMAIN_KEYWORDS.items():
            for kw in kw_list:
                if kw in text:
                    return cat
        return "EXPLORACIÓN VISUAL"

    def _is_abstract_text(self, text: str) -> bool:
        """True if the response is purely abstract, philosophical, or mathematical."""
        abstract_markers = [
            "opinión", "sentimiento", "filosofía", "conciencia", "concepto abstracto",
            "en mi opinión", "no tengo cuerpo", "como inteligencia artificial"
        ]
        t = text.lower()
        return any(am in t for am in abstract_markers)

    def _is_visual_entity(self, topic: str, response: str) -> bool:
        combined = f"{topic} {response}".lower()
        visual_markers = [
            # Lugares, Monumentos y Geografía
            "ciudad", "ruinas", "monumento", "santuario", "templo", "monta[nñ]a", "r[ií]o", "lago",
            "volc[aá]n", "planeta", "estrella", "galaxia", "pa[ií]s", "regi[oó]n", "zona", "parque",
            "reserva", "paisaje", "playa", "isla", "bosque", "desierto", "valle", "costa",
            # Gastronomía y Alimentos
            "plato", "platillo", "comida", "receta", "gastronom[ií]a", "alimento", "bebida", "fruta",
            "ingrediente", "postre", "arroz", "frijol", "preparaci[oó]n", "sabor", "cocina",
            # Seres vivos (Flora y Fauna)
            "especie", "animal", "mam[ií]fero", "ave", "pez", "reptil", "planta", "flor", "[aá]rbol",
            "hongo", "fauna", "flora", "capibara", "felino", "canino",
            # Arte, Construcciones y Objetos
            "escultura", "pintura", "museo", "edificio", "torre", "puente", "veh[ií]culo", "nave",
            "robot", "dispositivo", "m[aá]quina", "invento", "herramienta", "objeto", "artefacto",
            "traje", "vestimenta", "s[ií]mbolo", "bandera", "auto", "carro", "coche", "ferrari", "superdeportivo",
            # Historia y Cultura
            "ubicado en", "construido en", "declarado patrimonio", "descubierto en", "restos arqueol[oó]gicos",
            "tradicional", "t[ií]pico", "originario de", "popular en", "elaborado con", "civilizaci[oó]n"
        ]
        for vm in visual_markers:
            if re.search(r"\b" + vm, combined, re.IGNORECASE):
                return True
        return len(topic.strip()) >= 3 and not self._is_abstract_text(combined)


class VisualEngine:
    """
    Central Coordinator: detects visual requests, queries SerpAPI Images,
    downloads and caches image files locally, and structures elegant visual cards.
    """

    _instance: Optional[VisualEngine] = None
    _lock = threading.Lock()

    def __init__(self):
        self.detector = VisualQueryDetector()
        self.serp_client = SerpApiClient.get_instance()
        self._cards_cache_file = CACHE_DIR / "cards_index.json"
        self._cards_cache: Dict[str, Dict[str, Any]] = {}
        self._init_cache()

    @classmethod
    def get_instance(cls) -> VisualEngine:
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def _init_cache(self):
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            IMG_CACHE_DIR.mkdir(parents=True, exist_ok=True)
            if self._cards_cache_file.exists():
                data = json.loads(self._cards_cache_file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    self._cards_cache = data
        except Exception as e:
            logger.warning(f"Error initializing visual cache: {e}")

    def _save_cache_index(self):
        try:
            self._cards_cache_file.write_text(
                json.dumps(self._cards_cache, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception:
            pass

    def _fetch_ddg_images(self, query: str, max_results: int = 6) -> list:
        """Fallback to DuckDuckGo Images when SerpAPI is unconfigured, rate-limited, or returns empty."""
        try:
            from actions.web_search import _get_ddgs
            from core.research.serpapi_client import SearchResultItem
            DDGS = _get_ddgs()
            items = []
            with DDGS() as ddgs:
                for r in ddgs.images(query, max_results=max_results):
                    img_url = r.get("image") or r.get("thumbnail")
                    if img_url:
                        items.append(SearchResultItem(
                            title=r.get("title", query),
                            link=img_url,
                            snippet=r.get("source", ""),
                            source=r.get("source", "DuckDuckGo Images"),
                            thumbnail=r.get("thumbnail") or img_url
                        ))
            return items
        except Exception as e:
            logger.warning(f"DDG image search fallback failed: {e}")
            return []

    def evaluate_and_fetch(
        self,
        user_query: str,
        assistant_response: str = "",
        force: bool = False
    ) -> Optional[VisualCardData]:
        """
        Main entry point. Evaluates if the interaction merits a visual panel.
        If yes, fetches SerpAPI images, synthesizes summary & fact, and caches images.
        Safe to call from background worker thread.
        """
        user_query = (user_query or "").strip()
        analysis = self.detector.analyze(user_query, assistant_response)

        if not analysis and not force:
            return None

        if analysis:
            topic, category, confidence = analysis
        else:
            topic = user_query
            category = "EXPLORACIÓN VISUAL"

        norm_key = re.sub(r"\s+", " ", topic.lower().strip())

        # Check memory cache
        if norm_key in self._cards_cache:
            cached_entry = self._cards_cache[norm_key]
            # Ensure local image files still exist
            images = cached_entry.get("images", [])
            valid_images = [img for img in images if Path(img.get("local_path", "")).exists()]
            if valid_images:
                card = VisualCardData.from_dict(cached_entry)
                card.images = valid_images
                logger.info(f"Visual card served from disk cache for topic: '{topic}'")
                return card

        # Generate summary and interesting fact
        summary, fact = self._synthesize_summary_and_fact(topic, assistant_response)

        # 1. Fetch Images via SerpAPI if configured
        results = None
        try:
            results = self.serp_client.search(
                query=topic,
                engine="google_images",
                num=6,
                hl="es",
                gl="es",
                use_cache=True
            )
        except Exception as e:
            logger.debug(f"SerpAPI search error: {e}")

        if not results:
            # Fallback query with photography keywords
            try:
                results = self.serp_client.search(
                    query=f"{topic} foto",
                    engine="google_images",
                    num=6,
                    hl="es",
                    gl="es",
                    use_cache=True
                )
            except Exception as e:
                logger.debug(f"SerpAPI fallback search error: {e}")

        # 2. Resilient Fallback: DuckDuckGo Images
        if not results:
            logger.info(f"SerpAPI returned no images for '{topic}', attempting DuckDuckGo Images fallback...")
            results = self._fetch_ddg_images(topic, max_results=6)

        if not results:
            results = self._fetch_ddg_images(f"{topic} fotos", max_results=6)

        if not results:
            logger.warning(f"No image results found for topic: '{topic}'")
            return None

        # Download and store top images locally in parallel
        from concurrent.futures import ThreadPoolExecutor

        processed_images = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(
                    self._download_and_cache_image,
                    topic,
                    idx,
                    item.link,
                    item.thumbnail or item.link,
                    item.title,
                    item.source
                )
                for idx, item in enumerate(results[:4])
            ]
            for f in futures:
                try:
                    info = f.result()
                    if info:
                        processed_images.append(info)
                except Exception as e:
                    logger.debug(f"Image fetch error: {e}")

        if not processed_images:
            logger.warning(f"Failed to cache any images for topic: '{topic}'")
            return None

        card = VisualCardData(
            topic=topic.title(),
            category=category,
            summary=summary,
            interesting_fact=fact,
            images=processed_images,
            source=processed_images[0].get("source", "SerpAPI / Google Images"),
            query=user_query,
        )

        # Store in cache
        self._cards_cache[norm_key] = card.to_dict()
        self._save_cache_index()

        return card

    def _download_and_cache_image(
        self,
        topic: str,
        index: int,
        main_url: str,
        thumb_url: str,
        title: str,
        source: str
    ) -> Optional[Dict[str, str]]:
        """Downloads main and thumbnail images into local cache directory."""
        slug = re.sub(r"[^a-zA-Z0-9_-]", "_", topic.lower())[:30]
        url_hash = hashlib.md5((main_url or thumb_url).encode("utf-8")).hexdigest()[:8]
        main_file = IMG_CACHE_DIR / f"{slug}_{index}_{url_hash}_main.jpg"
        thumb_file = IMG_CACHE_DIR / f"{slug}_{index}_{url_hash}_thumb.jpg"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # 1. Download thumb (fast, reliable)
        if not thumb_file.exists():
            target_thumb_url = thumb_url or main_url
            try:
                with httpx.Client(timeout=8.0, follow_redirects=True) as client:
                    resp = client.get(target_thumb_url, headers=headers)
                    if resp.status_code == 200 and len(resp.content) > 500:
                        thumb_file.write_bytes(resp.content)
            except Exception as e:
                logger.debug(f"Thumb download failed for {target_thumb_url}: {e}")

        # 2. Download main high-res image (with fallback to thumb if main fails or times out)
        if not main_file.exists():
            downloaded = False
            if main_url and not main_url.startswith("data:"):
                try:
                    with httpx.Client(timeout=3.5, follow_redirects=True) as client:
                        resp = client.get(main_url, headers=headers)
                        if resp.status_code == 200 and len(resp.content) > 2000:
                            main_file.write_bytes(resp.content)
                            downloaded = True
                except Exception as e:
                    logger.debug(f"Main image download failed for {main_url}: {e}")

            if not downloaded:
                # If main failed or timed out, use thumbnail as main image fallback
                if thumb_file.exists():
                    try:
                        main_file.write_bytes(thumb_file.read_bytes())
                        downloaded = True
                    except Exception:
                        pass

        if not main_file.exists() and not thumb_file.exists():
            return None

        chosen_main = str(main_file if main_file.exists() else thumb_file)
        chosen_thumb = str(thumb_file if thumb_file.exists() else main_file)

        return {
            "url": main_url,
            "thumb": thumb_url,
            "local_path": chosen_main,
            "local_thumb": chosen_thumb,
            "title": title or topic,
            "source": source or "Web",
        }

    def _synthesize_summary_and_fact(self, topic: str, assistant_response: str) -> Tuple[str, str]:
        """
        Extracts an elegant 35-55 word summary and an engaging key fact
        from the assistant's own response or generated context.
        """
        resp = (assistant_response or "").strip()
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", resp) if len(s.strip()) > 10]

        fact = ""
        summary_sentences = []

        # Look for a sentence with high curiosity value (numbers, records, dates, key facts)
        fact_indicators = [
            r"\bconstruid[oa]\b", r"\bdescubiert[oa]\b", r"\ba m[aá]s de\b", r"\bpatrimonio\b",
            r"\b[uú]nic[oa]\b", r"\bm[aá]s de\b", r"\bdeclarad[oa]\b", r"\ben el a[nñ]o\b",
            r"\bsiglo\b", r"\bmetros\b", r"\bkil[oó]metros\b", r"\bcuenta con\b", r"\bse destaca por\b",
            r"\bcuriosidad\b", r"\bdato interesante\b", r"\bconocid[oa] por\b"
        ]

        for s in sentences:
            if not fact:
                for ind in fact_indicators:
                    if re.search(ind, s, re.IGNORECASE):
                        fact = s
                        break
            if s != fact:
                summary_sentences.append(s)

        # Assemble summary (around 35-50 words)
        words_accum = []
        for s in summary_sentences:
            words = s.split()
            if len(words_accum) + len(words) <= 55 or len(words_accum) < 25:
                words_accum.extend(words)
            else:
                break

        summary = " ".join(words_accum).strip()

        # If assistant response was short or empty, provide high quality default text
        if len(summary) < 20:
            summary = f"{topic.title()} es uno de los temas más fascinantes y destacados en su categoría, reconocido internacionalmente por su relevancia histórica, científica y cultural."

        if not fact:
            if len(sentences) > 1:
                fact = sentences[-1]
            else:
                fact = f"{topic.title()} continúa siendo objeto de estudio y admiración por expertos alrededor del mundo."

        # Clean fact string
        fact = re.sub(r"^(?:adem[aá]s|tambi[eé]n|por otro lado|cabe destacar que)\,?\s*", "", fact, flags=re.IGNORECASE).strip()

        return summary, fact
