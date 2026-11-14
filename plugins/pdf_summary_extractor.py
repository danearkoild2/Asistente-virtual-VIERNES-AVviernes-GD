"""
PDF Summary Extractor Plugin for MARK LV / Viernes.
Extracts text and key sections from PDF documents in Downloads or custom paths.
"""
from __future__ import annotations
import os
from pathlib import Path
import re
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "pdf_summary_extractor",
    "description": (
        "Extracts text, outlines, or summaries from a PDF document. "
        "Use when user asks 'resume este PDF', 'lee el PDF de descargas', 'qué dice el documento', "
        "or 'extrae el texto del PDF'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "filename": {
                "type": "STRING",
                "description": "Filename or path of the PDF. If omitted, checks most recent PDF in Downloads.",
            },
            "max_characters": {
                "type": "INTEGER",
                "description": "Maximum characters to extract (default: 2000).",
            }
        },
        "required": [],
    },
}

PLUGIN_SETTINGS = {
    "title": "Extractor de Resúmenes PDF",
    "fields": [
        {
            "key": "default_search_folder",
            "label": "Carpeta de Búsqueda",
            "type": "choice",
            "options": ["Downloads", "Documents", "Desktop"],
            "default": "Downloads",
        },
    ],
}

def _find_pdf(filename: str | None) -> Path | None:
    user_home = Path(os.environ.get("USERPROFILE", "."))
    if filename:
        p = Path(filename)
        if p.exists():
            return p
        p_dl = user_home / "Downloads" / filename
        if p_dl.exists():
            return p_dl
        p_doc = user_home / "Documents" / filename
        if p_doc.exists():
            return p_doc

    # Search newest in Downloads
    dl_dir = user_home / "Downloads"
    if dl_dir.exists():
        pdfs = sorted(dl_dir.glob("*.pdf"), key=lambda f: f.stat().st_mtime, reverse=True)
        if pdfs:
            return pdfs[0]
    return None

def run(parameters: dict, player=None, session_memory=None) -> str:
    target_name = parameters.get("filename")
    pdf_path = _find_pdf(target_name)

    if not pdf_path:
        return "No pude encontrar ningún archivo PDF en tu carpeta de Descargas o la ruta especificada."

    try:
        max_chars = int(parameters.get("max_characters", 2000))
    except (TypeError, ValueError):
        max_chars = 2000

    extracted_text = ""
    # Try pypdf / PyPDF2 / pdfplumber or fallback string extractor
    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        for page in reader.pages[:10]:
            t = page.extract_text() or ""
            extracted_text += t + "\n"
            if len(extracted_text) >= max_chars:
                break
    except Exception:
        # Fallback binary string regex extraction for ascii/utf-8 text
        try:
            raw = pdf_path.read_bytes()
            matches = re.findall(rb"[(]([\w\s.,;:?!-]{3,})[)]", raw)
            extracted_text = " ".join(m.decode("latin1", errors="ignore") for m in matches[:100])
            num_pages = 1
        except Exception as e:
            return f"No se pudo leer el archivo PDF '{pdf_path.name}': {e}"

    clean = " ".join(extracted_text.split())
    if not clean:
        return f"El archivo PDF '{pdf_path.name}' parece estar vacío o contiene únicamente imágenes escaneadas."

    preview = clean[:600] + "..." if len(clean) > 600 else clean
    msg = f"📄 PDF '{pdf_path.name}' leído ({len(clean)} caracteres extraídos). Fragmento inicial:\n{preview}"

    if player:
        try:
            player.write_log(f"📄 PDF LEÍDO ({pdf_path.name}): {preview[:150]}...")
        except Exception:
            pass

    return f"He leído '{pdf_path.name}'. Aquí tienes el extracto principal del documento: {preview}"
