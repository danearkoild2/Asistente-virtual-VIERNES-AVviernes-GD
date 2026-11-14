# ⚡ VIERNES OS — Asistente Virtual Multimodal de Nueva Generación

### Desarrollado por **Groovi Developer** · 100% Gratuito y Open Source

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/UI-PyQt6%20%2B%20WebEngine-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Gemini Live](https://img.shields.io/badge/IA-Gemini%20Live%20API-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Modulos](https://img.shields.io/badge/Capacidades-57%20Acciones%20%2B%2041%20Plugins-FF6B6B?style=for-the-badge)
![License](https://img.shields.io/badge/Producci%C3%B3n-Gratuita%20Open%20Source-10B981?style=for-the-badge)

**Viernes OS** es un asistente virtual inteligente multimodal para escritorio (**Windows, Linux y macOS**) con conversación por voz bidireccional en tiempo real, avatares interactivos **Live2D / VRM 3D**, control total del PC, TV y Deportes en vivo con AdBlock nativo, Radio con visualizador de espectro, limpieza segura de Android TV (**CleanYourTV**), **Segundo Cerebro RAG local**, grabador de reuniones, estudio con flashcards por voz, visión por computadora **OpenCV**, domótica LAN y personalización completa mediante **HUD Studio**.

---

## 📸 Capturas Reales del Sistema

| HUD Principal | HUD Studio (Personalización Total) |
| :---: | :---: |
| ![HUD Principal](documentación%20Oficial/assets/shot_hud_principal.png) | ![HUD Studio](documentación%20Oficial/assets/shot_hud_studio.png) |

| Instalador Oficial (Groovi Developer) | Clean Your TV (Android TV / Google TV) |
| :---: | :---: |
| ![Instalador Oficial](documentación%20Oficial/assets/shot_installer_step1.png) | ![Clean Your TV](documentación%20Oficial/assets/shot_cleanyourtv.png) |

> 💡 Abre **[`documentación Oficial/index.html`](documentación%20Oficial/index.html)** en tu navegador para explorar la documentación interactiva completa con buscador en vivo, galería ampliable, catálogo de las **98 capacidades** y guías paso a paso.

---

## 🚀 Instalación Rápida (Asistente Oficial)

### Requisitos Mínimos
- **Sistema Operativo:** Windows 10/11 (64-bit), Linux o macOS
- **Python:** 3.11 o 3.12 *(recomendado 3.12)*
- **CPU / RAM:** 4 núcleos · 8 GB RAM *(16 GB recomendado si usas Coqui XTTS-v2 local)*
- **Internet:** Requerido para Gemini Live API, TV/Radio y búsquedas web

### Pasos de Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/danearkoild2/Asistente-virtual-VIERNES-AVviernes-GD.git
cd Asistente-virtual-VIERNES-AVviernes-GD

# 2. Ejecuta el Instalador Oficial (Windows)
instalar_viernes.bat
```

O ejecútalo directamente con Python en Windows/Linux/macOS:
```bash
py -3.12 installer.py
# Una vez configurado:
py -3.12 main.py
```

El instalador oficial de **Groovi Developer** te guiará en 5 pasos:
1. Instalación automática de dependencias (`requirements.txt`).
2. Personalización de tu nombre y el del asistente.
3. Configuración y verificación en vivo de tu **API Key de Gemini** (y APIs opcionales).
4. Selección del **motor de voz (TTS)** y tu **skin Live2D**.
5. Resumen, créditos e información de apoyo.

---

## 🔑 APIs: Obligatoria vs. Opcionales

| API / Servicio | Estado | Uso en Viernes | Costo |
| :--- | :---: | :--- | :--- |
| **Google Gemini API** | **OBLIGATORIA** | Cerebro conversacional, voz Gemini Live, visión, resúmenes y RAG | Gratis en [Google AI Studio](https://aistudio.google.com/apikey) |
| **SerpAPI** | Opcional | Resultados enriquecidos de búsqueda (respaldo gratuito con DuckDuckGo) | Plan gratuito |
| **OpenWeatherMap** | Opcional | Pronóstico meteorológico detallado por ciudad | Plan gratuito |
| **ElevenLabs** | Opcional | Voces hiperrealistas premium (alternativa a Gemini/Edge/Coqui) | Freemium |
| **VirusTotal** | Opcional | Escaneo de archivos y URLs sospechosas (`virustotal_file_scanner`) | Plan gratuito |
| **Home Assistant / Tuya** | Opcional | Control domótico de luces, enchufes y escenas en tu red LAN | Local / Gratis |
| **Gmail OAuth / SMTP** | Opcional | Lectura y envío de correos (`gmail_controller`) | Gratis |

---

## 🧠 Qué Puede Hacer Viernes (57 Acciones + 41 Plugins)

### 🎭 Avatares, Presencia y Personalización
- **Live2D Cubism (WebEngine PixiJS) + VRM 3D + VMC + Avatar Holográfico:** Lip-sync en tiempo real, parpadeo, expresiones y cambio de skin en caliente (`edith`, `ohto`, `viernes`, o cualquier modelo propio en `live2d_models/`).
- **HUD Studio (`core/hud_studio_ui.py`):** 6+ temas visuales, colores de acento, tipografías, opacidad y escenarios arquitectónicos profesionales (`Penthouse Nocturno`, `Puente de Comando`, `Loft Arquitectónico`).

### 🎙️ 4 Motores de Voz (TTS) + Seguridad Vocal
- **Gemini Native Audio** · **Edge-TTS Neural** (gratis, español LATAM/ES) · **ElevenLabs** · **Coqui XTTS-v2** (clonación de voz 100% local).
- **Wake Word** local, traducción simultánea en tiempo real (`realtime_translation.py`) y **biometría vocal** (`voice_security.py`).

### 📺 TV, Deportes, IPTV, Radio y Clean Your TV
- **TV Web & Agenda Deportiva:** Pide canales o partidos (*"Ponme el partido de Costa Rica vs Ecuador"*); consulta `futbolenvivo.top`, detecta el canal y lo abre con **Brave AdBlock-Rust** nativo y selector de opciones.
- **Radio en Vivo (`ondachannels`):** Emisoras globales y latinas (*"Ponme Bésame de Costa Rica"*, *"Pon una radio random en español"*) con visualizador de espectro multibanda a 30 FPS.
- **Clean Your TV (`cleanyourtv.py`):** Escanea tu Wi-Fi (ADB puerto 5555), analiza paquetes contra 473 perfiles comunitarios, crea respaldo automático y desactiva bloatware/anuncios de forma 100% reversible.
- **YouTube, Video Local & Spotify/GSMTC:** Reproduce videos en el HUD, resume transcripciones de YouTube y detecta lo que está sonando.

### 📚 Productividad Extrema, Segundo Cerebro y Reuniones
- **Grabador y Resumidor de Reuniones (`meeting_recorder.py`):** Graba Meet/Zoom/Teams/Discord, identifica hablantes y genera minutas Markdown con tareas pendientes.
- **Segundo Cerebro RAG Local (`local_rag.py`):** Indexa carpetas, código, Markdown, PDFs y DOCX en SQLite FTS5 local citando archivo y líneas exactas.
- **Modo Estudio / Flashcards por Voz (`study_flashcards.py`):** Mazos estilo Anki generados desde PDFs o temas con repaso espaciado y evaluación oral.
- **Historial Visual de Pantalla (`screen_recall.py`):** Capturas ligeras 100% locales en SQLite FTS5 para preguntar *"¿Qué estaba viendo hoy sobre X?"* (con purga instantánea).
- **Lectura de Libros y Documentos:** `learn_book.py`, `recall_book_knowledge.py`, `file_processor.py` (PDF, DOCX, PPTX), `data_analyzer.py`, `financial_analytics.py`, `flight_finder.py`.

### 🤖 Agentes IA, Código y Automatización
- **OpenHands** · **LangGraph** · **Letta (MemGPT)** · **Windmill** · **Crawl4AI** · **Midscene UI** · **Playwright** · **Dev Agent** · **Code Helper** · **Project Intelligence**.

### 🖥️ Control Total del PC, Visión, Domótica y 41 Plugins
- **Control PC & Hardware:** Ratón/teclado, apertura de apps, organización de archivos con papelera segura (`send2trash`), monitor CPU/RAM/GPU NVIDIA (`gpu_taskman.py`), diagnósticos y actualizador de juegos.
- **Visión por Computadora:** Cámara en vivo con **OpenCV** (`opencv_vision.py`) y análisis instantáneo de pantalla (`screen_processor.py`).
- **Domótica & Red:** Descubrimiento LAN (`SSDP`, `mDNS/Zeroconf`, `Wake-on-LAN`), Android TV, Samsung Tizen, LG webOS, Roku, Chromecast, Home Assistant, TinyTuya, MQTT y App Android remota.
- **41 Plugins en `plugins/`:** `virustotal_file_scanner`, `webcam_sentinel`, `local_network_auditor`, `speedtest_pro`, `git_assistant`, `github_trending_radar`, `rembg_background_remover`, `crypto_stock_tracker`, `spotify_smart_controller`, `steam_deal_hunter`, `pomodoro_timer`, `voice_journal`, y muchos más.

---

## 🧩 Cómo Instalar Nuevos Modelos Live2D

1. Descarga o exporta tu modelo **Live2D Cubism 3/4** (debe incluir `.model3.json`, `.moc3` y carpeta de texturas).
2. Crea una carpeta dentro de `live2d_models/mi_modelo/` y coloca allí los archivos.
3. Abre **⚙ → Personalizar asistente y voz** (o el **Instalador Oficial**) y selecciona tu nuevo skin al instante.

---

## 🤝 Repositorios Open-Source Integrados Nativamente

`All-Hands-AI/OpenHands` · `langchain-ai/langgraph` · `letta-ai/letta` · `windmill-labs/windmill` · `unclecode/crawl4ai` · `web-infra-dev/midscene` · `OpenAmika` · `idiap/coqui-ai-TTS` · `iptv-org` · `OndaChannels` · `udhaykumarbala/cleanyourtv-app` · `brave/adblock-rust` · `home-assistant/core` · `TinyTuya`

---

## 💛 Apoya el Proyecto (Donaciones)

**Viernes OS** se distribuye de forma **100% gratuita y abierta** para toda la comunidad. Si este proyecto te ahorra tiempo o te gusta su desarrollo, puedes apoyar su evolución continua con una donación segura vía PayPal (también disponible dentro del HUD en el botón **💛 Donar · PayPal** en la esquina inferior derecha):

- 👉 **[Donar vía PayPal — Groovi Developer](https://www.paypal.com/ncp/payment/NE56HM9KTAQRQ)**

---

<p align="center">
  Desarrollado con dedicación por <strong>Groovi Developer</strong> · Viernes OS
</p>
