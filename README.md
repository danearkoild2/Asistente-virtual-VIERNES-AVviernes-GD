<div align="center">

# ⚡ VIERNES OS
### Asistente Virtual Multimodal de Nueva Generación · por **Groovi Developer**

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/UI-PyQt6%20%2B%20WebEngine-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![Gemini Live](https://img.shields.io/badge/IA-Gemini%20Live%20API-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![Acciones](https://img.shields.io/badge/Acciones%20Nativas-57%20M%C3%B3dulos-FF6B6B?style=for-the-badge)](#cat%C3%A1logo-completo-de-57-acciones-nativas)
[![Plugins](https://img.shields.io/badge/Plugins%20Modulares-41%20Extensiones-00B4D8?style=for-the-badge)](#cat%C3%A1logo-completo-de-41-plugins-modulares)
[![Open Source](https://img.shields.io/badge/Producci%C3%B3n-100%25%20Gratuita%20Open%20Source-10B981?style=for-the-badge)](#-apoya-el-proyecto--groovi-developer)

**Viernes OS** es un ecosistema de asistencia inteligente en tiempo real para escritorio (**Windows 10/11, Linux y macOS**) con voz bidireccional de baja latencia, avatar interactivo **Live2D / VRM 3D**, control total de PC y red LAN, **TV y Deportes con AdBlock nativo**, **Radio con visualizador de espectro**, limpieza segura de Android TV (**Clean Your TV**), **Segundo Cerebro RAG local**, grabador de reuniones, estudio por voz estilo Anki, historial visual de pantalla (**Screen Recall**), visión **OpenCV**, agentes autónomos (**OpenHands, LangGraph, Windmill, Letta, Crawl4AI, Midscene**) y personalización extrema mediante **HUD Studio**.

[📖 Documentación Oficial Interactiva](documentación%20Oficial/index.html) · [🚀 Instalación Rápida](#-instalaci%C3%B3n-oficial-guiada) · [🔑 APIs](#-apis-obligatoria-vs-opcionales) · [🧩 Live2D](#-modelos-live2d-y-c%C3%B3mo-instalar-nuevos) · [💛 Donar vía PayPal](#-apoya-el-proyecto--groovi-developer)

</div>

---

## 📸 Galería Visual del Sistema (Capturas Reales)

| HUD Principal (Interfaz + Avatar + Telemetría) | HUD Studio (Personalización Total en Vivo) |
| :---: | :---: |
| ![HUD Principal](documentación%20Oficial/assets/shot_hud_principal.png) | ![HUD Studio](documentación%20Oficial/assets/shot_hud_studio_v2.png) |

| Instalador Oficial · Paso 1 (Dependencias) | Instalador Oficial · Paso 4 (Voz TTS & Skin Live2D) |
| :---: | :---: |
| ![Instalador Paso 1](documentación%20Oficial/assets/shot_installer_step1_v2.png) | ![Instalador Voz y Skin](documentación%20Oficial/assets/shot_installer_voz_skin_v2.png) |

| Clean Your TV (Debloat Android TV / Google TV) | Avatar Live2D (Cubism + Lip-Sync) | Donación PayPal Integrada en HUD |
| :---: | :---: | :---: |
| ![Clean Your TV](documentación%20Oficial/assets/shot_cleanyourtv_v2.png) | ![Avatar Live2D Huohuo](documentación%20Oficial/assets/shot_live2d_huohuo.png) | ![Donación PayPal](documentación%20Oficial/assets/shot_donation_paypal_v2.png) |

### Escenarios Ambientales Profesionales Incluidos
| Penthouse Nocturno | Puente de Comando | Loft Arquitectónico |
| :---: | :---: | :---: |
| ![Penthouse](documentación%20Oficial/assets/bg_penthouse.jpg) | ![Command](documentación%20Oficial/assets/bg_command.jpg) | ![Loft](documentación%20Oficial/assets/bg_loft.jpg) |

---

## 💻 Requisitos Mínimos y Dependencias

| Componente | Mínimo Requerido | Recomendado (Uso Completo / Local IA) |
| :--- | :--- | :--- |
| **Sistema Operativo** | Windows 10/11 (64-bit), Linux o macOS | Windows 11 64-bit |
| **Python** | 3.11 o 3.12 | **Python 3.12** |
| **Procesador (CPU)** | 4 núcleos (Intel i5 / Ryzen 5) | 8 núcleos+ |
| **Memoria RAM** | 8 GB | 16 GB (recomendado para Coqui XTTS-v2) |
| **GPU** | Integrada | NVIDIA con CUDA (opcional para XTTS-v2 y `gpu_taskman`) |
| **Audio y Video** | Micrófono y altavoces | Webcam (para `opencv_vision` y `webcam_sentinel`) |
| **Red** | Conexión a Internet | Banda ancha estable para Gemini Live, TV y Radio |

### Dependencias Principales (`requirements.txt`)
- **Interfaz y Web:** `PyQt6`, `PyQt6-WebEngine`, `adblock` (Brave AdBlock-Rust)
- **IA y Voz:** `google-genai`, `edge-tts`, `SpeechRecognition`, `sounddevice`, `miniaudio`, `soundfile`, `scipy`
- **Agentes, RAG y Web:** `langgraph`, `letta-client`, `wmill` (Windmill), `crawl4ai`, `playwright`, `httpx`, `beautifulsoup4`, `ddgs`
- **Visión, Media y PC:** `opencv-python`, `mss`, `pillow`, `yt-dlp`, `pyautogui`, `pyperclip`, `psutil`, `nvidia-ml-py`, `send2trash`
- **Documentos y Domótica:** `pypdf`, `pdfplumber`, `python-docx`, `python-pptx`, `openpyxl`, `homeassistant-api`, `tinytuya`, `paho-mqtt`, `zeroconf`
- **Remote Dashboard & Seguridad:** `fastapi`, `uvicorn`, `cryptography`, `qrcode[pil]`

---

## 🚀 Instalación Oficial Guiada

```bash
# 1. Clona el repositorio oficial
git clone https://github.com/danearkoild2/Asistente-virtual-VIERNES-AVviernes-GD.git
cd Asistente-virtual-VIERNES-AVviernes-GD

# 2. Ejecuta el Instalador Oficial de Groovi Developer (Windows)
instalar_viernes.bat
```

*(En Linux/macOS o consola manual: `py -3.12 installer.py` o `python3 installer.py`, y luego `python main.py`.)*

### ¿Qué hace el Instalador Oficial (`installer.py`) en 5 Pasos?
1. **Dependencias:** Verifica Python e instala todos los paquetes desde `requirements.txt`.
2. **Tu Nombre e Identidad:** Pregunta tu nombre y cómo deseas llamar al asistente para personalizar cada interacción.
3. **APIs (Obligatoria vs. Opcionales):** Te guía paso a paso para obtener tu **API Key gratuita de Gemini**, la valida en vivo contra la API y permite añadir claves opcionales.
4. **Selector de Voz (TTS) & Skin Live2D:** Elige entre los 4 motores de voz y selecciona tu modelo Live2D inicial (`discover_live2d_skins()`).
5. **Donación y Créditos:** Información de soporte del proyecto y lanzamiento directo de Viernes OS.

---

## 🔑 APIs: Obligatoria vs. Opcionales

> **Solo una API es obligatoria** para que Viernes funcione al 100% de sus capacidades centrales, y **es gratuita** desde Google AI Studio.

| Servicio | ¿Obligatoria? | Cómo obtenerla | Función en Viernes OS |
| :--- | :---: | :--- | :--- |
| **Google Gemini API** | ✅ **OBLIGATORIA** | Entra a [aistudio.google.com/apikey](https://aistudio.google.com/apikey), inicia sesión y pulsa **Create API Key** | Motor principal de conversación, Gemini Live Audio, visión, minutas, flashcards y síntesis RAG |
| **SerpAPI** | ⚪ Opcional | [serpapi.com](https://serpapi.com/) (Plan gratuito) | Búsquedas web enriquecidas (sin ella usa DuckDuckGo gratis) |
| **OpenWeatherMap** | ⚪ Opcional | [openweathermap.org/api](https://openweathermap.org/api) | Reportes meteorológicos extendidos por ciudad |
| **ElevenLabs** | ⚪ Opcional | [elevenlabs.io](https://elevenlabs.io/) | Voces neuronales ultra-realistas premium |
| **VirusTotal** | ⚪ Opcional | [virustotal.com](https://www.virustotal.com/) | Escáner de archivos y URLs (`virustotal_file_scanner.py`) |
| **Home Assistant / Tuya** | ⚪ Opcional | Token local de tu servidor Home Assistant / TinyTuya | Control domótico de luces, enchufes y escenas LAN |
| **Gmail OAuth / SMTP** | ⚪ Opcional | Google Cloud Console / App Password | Lectura, resumen y envío de correos (`gmail_controller.py`) |

---

## 🎙️ 4 Motores de Voz (TTS) + Biometría Vocal

| Motor TTS | Tipo | Costo | Descripción |
| :--- | :--- | :---: | :--- |
| **Gemini Native Audio** | Nube (Baja Latencia) | Gratis (con Gemini Key) | Conversación fluida en tiempo real con expresividad natural (`Aoede`, `Puck`, `Charon`, `Kore`, `Fenrir`) |
| **Edge-TTS Neural** | Nube Microsoft | 100% Gratis | Voces neuronales en español LATAM/ES (`es-MX-DaliaNeural`, `es-CR-MariaNeural`, etc.) + respaldo automático |
| **ElevenLabs** | Nube Premium | Freemium | Clonación y voces de calidad cinematográfica configurando tu Voice ID |
| **Coqui XTTS-v2** | 100% Local (`idiap/coqui-ai-TTS`) | 100% Gratis / Offline | Síntesis y clonación multilingüe local a partir de una muestra `.wav` |

Además incluye **Wake Word local** (`core/wake_word.py`), **Traducción Simultánea en vivo** (`realtime_translation.py`) y **Autenticación Biométrica por Voz** (`voice_security.py` mediante similitud coseno).

---

## 🧩 Modelos Live2D y Cómo Instalar Nuevos

Viernes soporta avatares **Live2D Cubism 3/4** (WebEngine PixiJS + Cubism Core), avatares **VRM 3D**, protocolo **VMC** y un **Avatar Holográfico** por software.

### Cómo instalar un nuevo modelo Live2D en 3 pasos:
1. Consigue una carpeta de modelo Live2D Cubism 3/4 (debe contener `.model3.json`, `.moc3`, texturas `*.png`, física `.physics3.json` y expresiones `.exp3.json`).
2. Copia la carpeta dentro de `live2d_models/<nombre_del_modelo>/` (o en la raíz junto a `edith/`, `ohto/`, `viernes/`).
3. En Viernes, abre **⚙ → Personalizar asistente y voz** (o ejecuta `installer.py`) y elige tu nuevo skin. Se detecta automáticamente con `discover_live2d_skins()`.

---

## 🌟 Módulos Destacados en Detalle

### 📺 TV Web, Agenda Deportiva, IPTV y Radio
- **TV y Deportes (`iptv_player.py`, `core/sports_tv.py`):** Pide canales (*"Ponme Cartoon Network en pantalla completa"*) o partidos por equipos (*"Ponga el partido de Costa Rica vs Ecuador"*). Viernes consulta **`futbolenvivo.top`**, identifica el canal exacto que transmite el encuentro y abre el reproductor con **Brave AdBlock-Rust** nativo y selector de opciones (Opción 1, 2, 3...).
- **Radio Global y LATAM (`radio_player.py`, `core/radio_engine.py`, `core/radio_visualizer.py`):** Usa el directorio `ondachannels.com` + emisoras latinas. Pide emisoras exactas (*"Ponme Bésame de Costa Rica"*) o *"Pon una radio random"* (siempre en español) con **visualizador de espectro multibanda a 30 FPS** (0% CPU al cerrarse).

### 🧹 Clean Your TV (`cleanyourtv.py`, `core/cleanyourtv.py`)
Integración nativa de `udhaykumarbala/cleanyourtv-app` y 473 perfiles comunitarios para optimizar Android TV / Google TV:
1. **Conectar:** Escanea tu Wi-Fi en busca de TVs con ADB (puerto 5555) y te guía paso a paso con el control remoto.
2. **Analizar:** Clasifica aplicaciones del sistema en anuncios, telemetría y bloatware.
3. **Limpiar y Restaurar (100% Reversible):** Crea respaldo automático en `config/cleanyourtv_backups/` y desactiva con `pm disable-user --user 0`.

### 🧠 Segundo Cerebro, Reuniones, Estudio y Screen Recall
- **Grabador y Resumidor de Reuniones (`meeting_recorder.py`):** Graba reuniones (Meet, Zoom, Teams, Discord) en `outputs/meetings/*.wav`, identifica hablantes y genera minutas Markdown con decisiones y tareas (`- [ ]`).
- **Segundo Cerebro RAG Local (`local_rag.py`):** Indexa carpetas de código, Markdown, TXT, PDF y DOCX en SQLite FTS5 (`memory/local_rag.db`) y responde citando archivo y líneas exactas (`archivo.py:L10-L35`).
- **Modo Estudio / Flashcards por Voz (`study_flashcards.py`):** Crea mazos estilo Anki desde PDFs o temas y realiza sesiones habladas con repaso espaciado en `memory/flashcards.json`.
- **Screen Recall Local (`screen_recall.py`):** Historial visual 100% local (estilo Rewind/Recall) en SQLite FTS5 + capturas comprimidas con retención configurable y purga instantánea.

---

## 📦 Catálogo Completo de 57 Acciones Nativas

<details>
<summary><strong>Haz clic para desplegar los 57 módulos en <code>actions/</code> con sus comandos de voz</strong></summary>

| Categoría | Archivo (`actions/`) | Descripción y Ejemplo de Voz |
| :--- | :--- | :--- |
| **Control PC** | `computer_control.py` | Ratón, teclado, clics, atajos y escritura (*"Haz clic en guardar"*) |
| **Control PC** | `computer_settings.py` | Volumen, brillo, modo oscuro, energía (*"Baja el volumen al 30%"*) |
| **Control PC** | `desktop.py` | Escritorios virtuales y ventanas (*"Minimiza todas las ventanas"*) |
| **Control PC** | `open_app.py` | Abre cualquier programa instalado (*"Abre Visual Studio Code"*) |
| **Control PC** | `file_controller.py` | Copia, mueve, organiza y borra a papelera segura (`send2trash`) |
| **Control PC** | `file_processor.py` | Extrae texto y tablas de PDF, DOCX y PPTX |
| **Control PC** | `system_monitor.py` | Monitorea CPU, RAM, disco y procesos pesados |
| **Control PC** | `system_diagnostics.py` | Diagnóstico completo de salud del sistema y red |
| **Control PC** | `gpu_taskman.py` | Carga, temperatura, VRAM y procesos en GPUs NVIDIA |
| **Control PC** | `game_updater.py` | Verifica actualizaciones de juegos en Steam y launchers |
| **Control PC** | `browser_control.py` | Automatización completa de navegador con Playwright |
| **IA & Código** | `openhands_agent.py` | Delega ingeniería de software autónoma a OpenHands |
| **IA & Código** | `dev_agent.py` | Generación de scripts, módulos y parches |
| **IA & Código** | `code_helper.py` | Explica funciones, depura errores y refactoriza |
| **IA & Código** | `project_intelligence.py` | Indexa y analiza la arquitectura completa de repositorios |
| **IA & Código** | `langgraph_agent.py` | Orquestación de flujos multi-paso con LangGraph |
| **IA & Código** | `windmill_runner.py` | Ejecución de workflows y scripts con Windmill SDK |
| **IA & Código** | `letta_memory.py` | Memoria persistente a largo plazo tipo MemGPT + FTS5 |
| **IA & Código** | `midscene_ui.py` | Automatización visual de interfaces con Midscene.js |
| **IA & Código** | `openamika_companion.py` | Estado emocional y expresiones del compañero virtual |
| **IA & Código** | `change_personality.py` | Cambia personalidad, tono y rol en caliente |
| **Multimedia** | `iptv_player.py` | TV Web, IPTV-org, AdBlock y partidos vía `futbolenvivo.top` |
| **Multimedia** | `radio_player.py` | Emisoras `ondachannels` + visualizador + random en español |
| **Multimedia** | `cleanyourtv.py` | Limpieza y debloat reversible para Android TV vía ADB |
| **Multimedia** | `video_player.py` | Reproductor de video integrado en el HUD |
| **Multimedia** | `youtube_video.py` | Busca, reproduce y resume videos por transcripción |
| **Multimedia** | `now_playing.py` | Detecta y controla música en Spotify / Windows GSMTC |
| **Productividad** | `meeting_recorder.py` | Grabador de reuniones y generador de minutas Markdown |
| **Productividad** | `local_rag.py` | Segundo Cerebro RAG local en SQLite FTS5 con cita de líneas |
| **Productividad** | `study_flashcards.py` | Flashcards estilo Anki con repaso espaciado por voz |
| **Productividad** | `web_search.py` | Búsqueda web instantánea (DuckDuckGo / SerpAPI) |
| **Productividad** | `web_research.py` | Investigación profunda multi-fuente |
| **Productividad** | `web_page_reader.py` | Lee y resume contenido limpio de cualquier URL |
| **Productividad** | `crawl4ai_scraper.py` | Extracción web estructurada en Markdown con Crawl4AI |
| **Productividad** | `learn_book.py` | Memoriza y asimila libros completos en PDF |
| **Productividad** | `recall_book_knowledge.py` | Consulta conocimiento de libros aprendidos |
| **Productividad** | `data_analyzer.py` | Análisis estadístico de CSV y hojas Excel |
| **Productividad** | `financial_analytics.py` | Seguimiento, métricas y análisis financiero |
| **Productividad** | `flight_finder.py` | Buscador de vuelos, rutas y precios |
| **Productividad** | `weather_report.py` | Pronóstico del clima actual y extendido |
| **Productividad** | `current_time.py` | Hora y fecha mundial por zona horaria |
| **Productividad** | `reminder.py` | Recordatorios y avisos programados |
| **Visión & Voz** | `screen_recall.py` | Historial visual de pantalla 100% local estilo Rewind |
| **Visión & Voz** | `opencv_vision.py` | Percepción visual en tiempo real por cámara |
| **Visión & Voz** | `screen_processor.py` | Captura y lectura instantánea de pantalla |
| **Visión & Voz** | `realtime_translation.py` | Traducción simultánea bidireccional en vivo |
| **Visión & Voz** | `voice_security.py` | Verificación biométrica de identidad por voz |
| **Visión & Voz** | `repeat_last_said.py` | Repite con claridad la última respuesta hablada |
| **Domótica** | `smart_home.py` | Control de luces, enchufes y escenas del hogar |
| **Domótica** | `home_assistant.py` | Conexión directa con Home Assistant Core |
| **Domótica** | `device_control.py` | Descubrimiento SSDP/mDNS/WOL, Samsung/LG/Roku/Android TV |
| **Comunicación** | `gmail_controller.py` | Lee, busca, resume y envía correos con Gmail OAuth / SMTP |
| **Comunicación** | `send_message.py` | Envía mensajes por plataformas vinculadas |
| **Comunicación** | `inbound_notifications.py` | Centraliza y anuncia notificaciones entrantes |
| **Comunicación** | `social_media.py` | Gestión y redacción para redes sociales |
| **Proactivo** | `proactive.py` | Sugerencias e iniciativas contextuales |
| **Proactivo** | `background_monitor.py` | Vigilancia silenciosa de métricas y eventos |

</details>

---

## 🔌 Catálogo Completo de 41 Plugins Modulares

<details>
<summary><strong>Haz clic para desplegar los 41 plugins incluidos en <code>plugins/</code> (extensibles con <code>_template.py</code>)</strong></summary>

- **Seguridad y Red:** `virustotal_file_scanner.py` · `privacy_lock.py` · `password_vault_generator.py` · `webcam_sentinel.py` · `local_network_auditor.py` · `network_diagnostic.py` · `speedtest_pro.py` · `whois_domain_dns_lookup.py` · `url_unmasker.py` · `temp_mail_burner.py`
- **Desarrollo y Utilidades:** `git_assistant.py` · `github_trending_radar.py` · `error_explainer.py` · `quick_regex_tester.py` · `clipboard_history_vault.py` · `clipboard_translator.py` · `pdf_summary_extractor.py` · `qr_generator_reader.py` · `unit_converter.py` · `image_optimizer.py` · `rembg_background_remover.py` · `crypto_stock_tracker.py`
- **Sistema y Hardware:** `system_cleaner.py` · `downloads_organizer.py` · `duplicate_file_finder.py` · `hardware_temperature_alert.py` · `battery_advisor.py` · `peripheral_battery_sentinel.py` · `bluetooth_auto_mesh.py` · `window_layout_manager.py` · `screen_color_night_light.py` · `shutdown_timer.py`
- **Bienestar, Ocio y Media:** `spotify_smart_controller.py` · `ambient_sound.py` · `gaming_mode.py` · `game_decider.py` · `steam_deal_hunter.py` · `pomodoro_timer.py` · `breathing_coach.py` · `wellness_reminder.py` · `voice_journal.py`

</details>

---

## 🏗️ Arquitectura, Seguridad y Atajos del HUD

```text
Mark-LV-main/
├── actions/                  # 57 módulos de acción auto-descubiertos (TOOL)
├── plugins/                  # 41 plugins extensibles + _template.py
├── core/                     # 60+ motores (Gemini, TTS/STT, Live2D, TV, Radio, CleanYourTV, HUD Studio)
├── memory/                   # Memoria a largo plazo, book_knowledge, config_manager, RAG/Recall local
├── dashboard/ & app/         # Dashboard Web FastAPI + QR y App Android nativa
├── security/                 # Bóveda cifrada, RBAC, voice_id y auditoría
├── documentación Oficial/    # Documentación HTML/CSS/JS interactiva + capturas reales
├── installer.py              # Instalador gráfico oficial (5 pasos)
├── instalar_viernes.bat      # Lanzador rápido en Windows
└── main.py / ui.py           # Núcleo de ejecución e interfaz HUD PyQt6
```

- **Seguridad:** Cifrado local con `cryptography`, confirmación obligatoria humana (`core/confirm.py`) para acciones irreversibles, `core/undo.py` + `send2trash`, y repositorio 100% libre de API Keys mediante `.gitignore` reforzado.
- **Atajos rápidos:** `F4` (silenciar/activar micrófono) · `🎛️ HUD Studio` (personalización total) · `🎭 Presencia` (Live2D / VRM 3D / Holograma) · `💛 Donar · PayPal` (esquina inferior derecha del HUD).

---

## 🤝 Repositorios Open-Source Integrados Nativamente

`All-Hands-AI/OpenHands` · `langchain-ai/langgraph` · `letta-ai/letta` · `windmill-labs/windmill` · `unclecode/crawl4ai` · `web-infra-dev/midscene` · `OpenAmika` · `idiap/coqui-ai-TTS` · `iptv-org` · `OndaChannels` · `udhaykumarbala/cleanyourtv-app` · `brave/adblock-rust` · `home-assistant/core` · `TinyTuya`

---

## 💛 Apoya el Proyecto · Groovi Developer

**Viernes OS** se distribuye de forma **100% gratuita y Open Source** para toda la comunidad. Si este sistema te resulta útil, te ahorra tiempo o quieres impulsar nuevas integraciones y actualizaciones continuas, puedes apoyar el proyecto con una donación segura vía PayPal (también integrada directamente dentro del HUD):

<div align="center">

[![Donar vía PayPal](https://img.shields.io/badge/💛_Donar_vía_PayPal-Groovi_Developer-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/ncp/payment/NE56HM9KTAQRQ)

**Creado con dedicación por [Groovi Developer](https://github.com/danearkoild2)**

</div>
