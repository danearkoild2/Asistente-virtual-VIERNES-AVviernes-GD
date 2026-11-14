# 📱 VIERNES MARK-LV • ANDROID EDITION

Proyecto nativo completo para **Android Studio** que traslada la experiencia completa de **VIERNES** a tu smartphone Android.

La aplicación está diseñada con una arquitectura de **Doble Modo**:
1. **Modo Autónomo (100% Nativo en el Teléfono)**: Funciona en la calle o donde sea, sin depender de la PC. Se conecta directamente a **Gemini Live 2.5** (`models/gemini-2.5-flash-native-audio-preview-12-2025`) mediante WebSockets bidireccionales de baja latencia con audio nativo PCM (16kHz entrada / 24kHz salida) y control de hardware de Android (abrir WhatsApp, YouTube, Spotify, encender linterna, consultar batería, alarmas, llamadas, etc.).
2. **Modo Enlace PC (Control Remoto)**: Permite controlar tu estación de trabajo en la PC desde el celular a través de la red local (`http://<IP_PC>:8000`).

---

## 🚀 Cómo Abrir y Ejecutar en Android Studio

### Paso 1: Abrir el Proyecto
1. Abre **Android Studio** (Koala, Jellyfish, Iguana, Hedgehog o superior).
2. Haz clic en **File > Open...** (o *Open Project* en la pantalla de bienvenida).
3. Selecciona la carpeta:
   ```
   c:\Users\DanearKoild\Desktop\Mark-LV-main\app
   ```
4. Espera a que Gradle sincronice las dependencias automáticamente (se descargará Gradle 8.7 y las librerías de Material 3 y OkHttp).

### Paso 2: Conectar tu Celular Android
1. Activa la **Depuración por USB** (*USB Debugging*) en las *Opciones de Desarrollador* de tu teléfono Android.
2. Conecta tu celular a la PC con un cable USB.
3. En la barra superior de Android Studio, selecciona tu dispositivo en la lista desplegable.
4. Presiona el botón verde **Run (▶)** (o presiona `Shift + F10`).
5. ¡Listo! La app se instalará y abrirá en tu celular con el nombre **VIERNES OS**.

---

## 🌟 Características Principales de la App

### 1. Avatar Interactivo 60 FPS con Lip-Sync en Tiempo Real
- **Renderizado Fluido**: Ubicado en `assets/avatar/viewer.html`, utiliza los frames de alta resolución de VIERNES (`assets/avatar/frames/`) sobre el fondo cinemático del **Penthouse Ejecutivo**.
- **Cambio de Fondo Dinámico**: Cambia automáticamente entre día, atardecer y noche según la hora del teléfono.
- **Lip-Sync Tridimensional**: La boca de VIERNES modula dinámicamente en 3 etapas (`mouth_1`, `mouth_2`, `mouth_3`) al ritmo del volumen RMS del audio.
- **Parpadeo Natural**: Algoritmo de parpadeo biomimético con doble cuadro (`blink_half` -> `blink`).
- **Modo Reposo & Luciérnaga Dorada**: Al ordenar descansar o pulsar "🌙 Reposo", VIERNES duerme y una luciérnaga flotante ilumina la habitación. Tocar la luciérnaga despierta a VIERNES al instante.

### 2. Voz Bidireccional en Tiempo Real (Gemini Live 2.5)
- **Captura de Micrófono**: 16,000 Hz, 16-bit mono PCM con cancelación de eco por hardware (`AcousticEchoCanceler`).
- **Reproducción Inmediata**: 24,000 Hz, 16-bit mono PCM directamente a `AudioTrack` de Android.
- **Detección de Interrupción**: Si comienzas a hablar mientras VIERNES está respondiendo, el sistema detiene inmediatamente el altavoz para escucharte.

### 3. Selector de Voces y Motores de Síntesis
En la pestaña **⚙️ Ajustes**:
- **Gemini 2.5 Native Audio (Latencia Cero ~250ms)**: Voces HD (`Aoede`, `Kore`, `Leda`, `Zephyr`, `Puck`, `Charon`, `Fenrir`, `Orus`).
- **Estilos Vocales**: *Natural*, *Cálida y Cercana*, *Ejecutiva Jarvis*, *Enérgica*, *Susurro Suave*, *Serena*.
- **ElevenLabs Flash v2.5**: Integración opcional de PCM 24kHz de ultra-baja latencia con tus Voice IDs personalizados.

### 4. Herramientas Nativas de Android (Function Calling)
Gemini Live tiene acceso directo a funciones del sistema Android:
- **Abrir Apps**: *"Viernes, abre WhatsApp"*, *"Abre YouTube"*, *"Abre Spotify"*, *"Abre Google Maps"*, *"Abre la Cámara"*, *"Abre Ajustes"*.
- **Mensajería**: *"Envía un WhatsApp al +52... diciendo que llego en 15 minutos"*.
- **Llamadas**: *"Marca al número ..."*.
- **Hardware**: *"Enciende la linterna"*, *"¿Cuánta batería me queda?"*, *"Sube el volumen al 70%"*.
- **Reloj**: *"Pon una alarma a las 7:00 AM"*, *"Pon un temporizador de 10 minutos"*.

### 5. Visión Artificial Multimodal y Archivos
- **Botón 📷 Cámara**: Toma una fotografía instantánea con la cámara de tu celular y VIERNES la analizará en vivo en la conversación.
- **Botón 📎 Adjuntar**: Sube cualquier imagen, código, PDF o documento almacenado en tu teléfono para que VIERNES lo lea y te responda.

### 6. Pestaña de Control Remoto de la PC
- Permite vincularte al servidor local de tu PC (`http://<IP_PC>:8000`) desde la misma app para alternar entre el uso en el celular y el control remoto de tu computadora.

---

## 📂 Estructura de Archivos del Proyecto

```
app/
├── build.gradle.kts                   <- Configuración raíz de Gradle
├── settings.gradle.kts                 <- Módulos del proyecto (:app)
├── gradle.properties                  <- Configuración de memoria JVM
├── gradlew / gradlew.bat              <- Scripts ejecutables de Gradle
├── gradle/wrapper/
│   └── gradle-wrapper.properties      <- Versión de Gradle (8.7)
└── app/
    ├── build.gradle.kts               <- Dependencias (OkHttp, Coroutines, Material3)
    ├── proguard-rules.pro             <- Reglas de optimización
    └── src/main/
        ├── AndroidManifest.xml        <- Permisos (Audio, Cámara, Linterna, Apps)
        ├── assets/
        │   ├── default_config.json    <- API Keys y configuración inicial precargada
        │   └── avatar/
        │       ├── viewer.html        <- Motor HTML5/Canvas del Avatar 60 FPS
        │       ├── room_bg.jpg        <- Fondo Penthouse (Día)
        │       ├── room_bg_night.jpg  <- Fondo Penthouse (Noche)
        │       ├── room_bg_sunset.jpg <- Fondo Penthouse (Atardecer)
        │       └── frames/*.png       <- Expresiones y cuadros faciales de VIERNES
        ├── java/com/groovidev/viernes/
        │   ├── MainActivity.kt        <- Controlador principal de interfaz y ciclo de vida
        │   ├── GeminiLiveClient.kt    <- Cliente WebSocket Gemini Live 2.5 (BidiGenerateContent)
        │   ├── AudioEngine.kt         <- Motor PCM (Record 16k, Track 24k, ElevenLabs Flash)
        │   ├── AndroidTools.kt        <- Declaración y ejecución de herramientas nativas Android
        │   ├── FileAndVisionHelper.kt <- Procesamiento multimodal de fotos y archivos
        │   └── ConfigManager.kt       <- Almacenamiento seguro SharedPreferences
        └── res/
            ├── layout/
            │   └── activity_main.xml  <- Interfaz HUD Ejecutiva Dark Cyberpunk
            ├── values/
            │   ├── colors.xml         <- Paleta Obsidian, Emerald y Cyan
            │   ├── strings.xml        <- Títulos y cadenas
            │   └── themes.xml         <- Tema Material3 Dark NoActionBar
            └── drawable/
                └── ic_viernes_logo.xml<- Logotipo vectorial de la aplicación
```
