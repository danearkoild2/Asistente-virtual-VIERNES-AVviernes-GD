package com.groovidev.viernes

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.ArrayAdapter
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.groovidev.viernes.databinding.ActivityMainBinding
import org.json.JSONObject

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var configManager: ConfigManager
    private lateinit var androidTools: AndroidTools
    private lateinit var fileHelper: FileAndVisionHelper
    private lateinit var audioEngine: AudioEngine
    private lateinit var geminiClient: GeminiLiveClient

    private var currentModeState = "LISTENING" // LISTENING, THINKING, SPEAKING, SLEEPING
    private var isMicMuted = false
    private var pendingMedia: MediaAttachment? = null

    // Permisos de Android
    private val requiredPermissions = arrayOf(
        Manifest.permission.RECORD_AUDIO,
        Manifest.permission.CAMERA
    )

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { perms ->
        val recordGranted = perms[Manifest.permission.RECORD_AUDIO] ?: false
        if (recordGranted) {
            connectLiveSession()
        } else {
            Toast.makeText(this, "Se requiere permiso de micrófono para hablar con VIERNES.", Toast.LENGTH_LONG).show()
        }
    }

    // Selector de Archivos del Celular
    private val filePickerLauncher = registerForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri ->
        if (uri != null) {
            val media = fileHelper.processUri(uri)
            if (media != null) {
                setPendingAttachment(media)
            }
        }
    }

    // Cámara Rápida para Visión en Vivo
    private val cameraLauncher = registerForActivityResult(
        ActivityResultContracts.TakePicturePreview()
    ) { bitmap ->
        if (bitmap != null) {
            val media = fileHelper.processBitmap(bitmap)
            setPendingAttachment(media)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        configManager = ConfigManager(this)
        androidTools = AndroidTools(this)
        fileHelper = FileAndVisionHelper(this)

        initAudioEngine()
        initGeminiClient()
        setupAvatarWebView()
        setupPcRemoteWebView()
        setupNavigationTabs()
        setupSettingsUi()
        setupActionListeners()

        checkPermissionsAndAutoStart()
    }

    private fun checkPermissionsAndAutoStart() {
        val missing = requiredPermissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }
        if (missing.isNotEmpty()) {
            permissionLauncher.launch(missing.toTypedArray())
        } else {
            connectLiveSession()
        }
    }

    // =========================================================================
    // INICIALIZACIÓN DE MOTORES DE AUDIO Y GEMINI LIVE
    // =========================================================================
    private fun initAudioEngine() {
        audioEngine = AudioEngine(
            onAudioRecorded = { pcm16k ->
                if (!isMicMuted && geminiClient.isConnected && currentModeState != "SLEEPING") {
                    geminiClient.sendAudioChunk(pcm16k)
                }
            },
            onMouthLevel = { level ->
                runOnUiThread {
                    binding.avatarWebView.evaluateJavascript("window.setMouth($level);", null)
                }
            },
            onPlaybackStarted = {
                runOnUiThread {
                    setAssistantState("SPEAKING")
                }
            },
            onPlaybackEnded = {
                runOnUiThread {
                    if (currentModeState == "SPEAKING") {
                        setAssistantState("LISTENING")
                    }
                }
            }
        )
    }

    private fun initGeminiClient() {
        geminiClient = GeminiLiveClient(
            configManager = configManager,
            onConnected = {
                runOnUiThread {
                    binding.tvConnectionStatus.text = "● En Línea • Conectada"
                    binding.tvConnectionStatus.setTextColor(ContextCompat.getColor(this, R.color.emerald_glow))
                    binding.btnConnectToggle.text = "DETENER"
                    binding.btnConnectToggle.setBackgroundColor(ContextCompat.getColor(this, R.color.bg_card))
                    binding.btnConnectToggle.setTextColor(ContextCompat.getColor(this, R.color.danger_red))
                    audioEngine.startRecording()
                    setAssistantState("LISTENING")
                    addChatBubble("VIERNES", "Sistemas en línea, señor. ¿En qué puedo asistirle hoy?", isAssistant = true)
                }
            },
            onDisconnected = { reason ->
                runOnUiThread {
                    binding.tvConnectionStatus.text = "● Desconectada"
                    binding.tvConnectionStatus.setTextColor(ContextCompat.getColor(this, R.color.text_secondary))
                    binding.btnConnectToggle.text = "⚡ CONECTAR"
                    binding.btnConnectToggle.setBackgroundColor(ContextCompat.getColor(this, R.color.emerald_primary))
                    binding.btnConnectToggle.setTextColor(Color.parseColor("#04130D"))
                    audioEngine.stopRecording()
                }
            },
            onError = { err ->
                runOnUiThread {
                    binding.tvConnectionStatus.text = "● Error de Conexión"
                    binding.tvConnectionStatus.setTextColor(ContextCompat.getColor(this, R.color.danger_red))
                    Toast.makeText(this, err, Toast.LENGTH_SHORT).show()
                }
            },
            onAudioChunkReceived = { pcm24k ->
                if (configManager.ttsEngine == "gemini") {
                    audioEngine.playAudioChunk(pcm24k)
                }
            },
            onAssistantText = { text ->
                runOnUiThread {
                    addChatBubble("VIERNES", text, isAssistant = true)
                    if (configManager.ttsEngine == "elevenlabs") {
                        audioEngine.streamElevenLabs(
                            text,
                            configManager.elevenlabsApiKey,
                            configManager.elevenlabsVoiceId
                        )
                    }
                }
            },
            onToolCallReceived = { id, name, args ->
                runOnUiThread {
                    setAssistantState("THINKING")
                    addToolBubble("⚡ Ejecutando: $name...", isTool = true)
                    val result = androidTools.execute(name, args) {
                        setAssistantState("SLEEPING")
                    }
                    val msg = result.optString("message", "Completado.")
                    addToolBubble("✓ $msg", isTool = false)
                    geminiClient.sendToolResponse(id, result)
                }
            },
            onInterrupted = {
                runOnUiThread {
                    audioEngine.stopAudioPlayback()
                    setAssistantState("LISTENING")
                }
            },
            onTurnCompleted = {
                runOnUiThread {
                    // Turno completado
                }
            }
        )
    }

    private fun connectLiveSession() {
        if (!geminiClient.isConnected) {
            binding.tvConnectionStatus.text = "● Conectando a Gemini Live 2.5..."
            binding.tvConnectionStatus.setTextColor(ContextCompat.getColor(this, R.color.amber_warn))
            geminiClient.connect()
        }
    }

    private fun disconnectLiveSession() {
        geminiClient.disconnect()
        audioEngine.stopRecording()
        audioEngine.stopAudioPlayback()
        setAssistantState("IDLE")
    }

    // =========================================================================
    // CONFIGURACIÓN DE AVATAR WEBVIEW (60 FPS + INTERACCIÓN)
    // =========================================================================
    @SuppressLint("SetJavaScriptEnabled")
    private fun setupAvatarWebView() {
        binding.avatarWebView.apply {
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.allowFileAccess = true
            settings.allowContentAccess = true
            settings.mediaPlaybackRequiresUserGesture = false
            setBackgroundColor(Color.TRANSPARENT)

            addJavascriptInterface(object {
                @JavascriptInterface
                fun onAvatarTapped(reaction: String) {
                    runOnUiThread {
                        // Reacción táctil
                    }
                }

                @JavascriptInterface
                fun onWakeRequested() {
                    runOnUiThread {
                        wakeViernes()
                    }
                }
            }, "AndroidBridge")

            webViewClient = object : WebViewClient() {
                override fun onPageFinished(view: WebView?, url: String?) {
                    setAssistantState(currentModeState)
                }
            }

            loadUrl("file:///android_asset/avatar/viewer.html")
        }
    }

    // =========================================================================
    // CONFIGURACIÓN DE PESTAÑA ENLACE PC (CONTROL REMOTO WEBVIEW)
    // =========================================================================
    @SuppressLint("SetJavaScriptEnabled")
    private fun setupPcRemoteWebView() {
        binding.pcRemoteWebView.apply {
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.databaseEnabled = true
            settings.allowFileAccess = true
            settings.mediaPlaybackRequiresUserGesture = false
            settings.cacheMode = WebSettings.LOAD_NO_CACHE

            webChromeClient = object : WebChromeClient() {
                override fun onPermissionRequest(request: android.webkit.PermissionRequest?) {
                    request?.grant(request.resources)
                }
            }
            webViewClient = WebViewClient()
        }

        binding.etPcUrl.setText(configManager.pcServerUrl)
        binding.btnLoadPcUrl.setOnClickListener {
            val url = binding.etPcUrl.text.toString().trim()
            if (url.isNotBlank()) {
                configManager.pcServerUrl = url
                binding.pcRemoteWebView.loadUrl(url)
            }
        }
    }

    // =========================================================================
    // LISTENERS Y ACCIONES DEL ASISTENTE MÓVIL
    // =========================================================================
    private fun setupActionListeners() {
        // Botón conectar / desconectar
        binding.btnConnectToggle.setOnClickListener {
            if (geminiClient.isConnected) {
                disconnectLiveSession()
            } else {
                connectLiveSession()
            }
        }

        // Botón reposo / despertar
        binding.btnSleepWake.setOnClickListener {
            if (currentModeState == "SLEEPING") {
                wakeViernes()
            } else {
                sleepViernes()
            }
        }

        // Micrófono Silenciar / Activar
        binding.btnMicToggle.setOnClickListener {
            isMicMuted = !isMicMuted
            if (isMicMuted) {
                binding.btnMicToggle.text = "🔇"
                binding.btnMicToggle.setBackgroundColor(ContextCompat.getColor(this, R.color.bg_card))
                Toast.makeText(this, "Micrófono en silencio", Toast.LENGTH_SHORT).show()
            } else {
                binding.btnMicToggle.text = "🎙️"
                binding.btnMicToggle.setBackgroundColor(ContextCompat.getColor(this, R.color.emerald_primary))
                Toast.makeText(this, "Micrófono activado", Toast.LENGTH_SHORT).show()
            }
        }

        // Adjuntar Archivo o Imagen del Teléfono
        binding.btnAttachFile.setOnClickListener {
            filePickerLauncher.launch("*/*")
        }

        // Tomar Foto con Cámara
        binding.btnCameraSnap.setOnClickListener {
            cameraLauncher.launch(null)
        }

        // Botón rápido superior linterna
        binding.btnQuickTorch.setOnClickListener {
            val res = androidTools.handleDeviceSettings("flashlight_toggle", "")
            Toast.makeText(this, res.second, Toast.LENGTH_SHORT).show()
        }

        // Botón rápido superior cámara
        binding.btnQuickVision.setOnClickListener {
            cameraLauncher.launch(null)
        }

        // Eliminar adjunto pendiente
        binding.btnClearAttachment.setOnClickListener {
            clearPendingAttachment()
        }

        // Enviar mensaje de texto o adjunto multimodal
        binding.btnSendMessage.setOnClickListener {
            sendMessage()
        }
    }

    private fun sendMessage() {
        val text = binding.etMessage.text.toString().trim()
        val media = pendingMedia

        if (text.isBlank() && media == null) return

        if (!geminiClient.isConnected) {
            connectLiveSession()
        }

        if (media != null) {
            addChatBubble("Tú", if (text.isNotBlank()) "$text\n[Adjunto: ${media.fileName}]" else "[Adjunto: ${media.fileName}]", isAssistant = false)
            geminiClient.sendMultimodalTurn(text, media)
            clearPendingAttachment()
        } else {
            addChatBubble("Tú", text, isAssistant = false)
            geminiClient.sendTextMessage(text)
        }

        binding.etMessage.text.clear()
        setAssistantState("THINKING")
    }

    private fun setPendingAttachment(media: MediaAttachment) {
        pendingMedia = media
        binding.attachmentBanner.visibility = View.VISIBLE
        binding.tvAttachmentName.text = "📎 ${media.fileName}"
        Toast.makeText(this, "Adjunto listo. Presiona Enviar.", Toast.LENGTH_SHORT).show()
    }

    private fun clearPendingAttachment() {
        pendingMedia = null
        binding.attachmentBanner.visibility = View.GONE
    }

    private fun sleepViernes() {
        setAssistantState("SLEEPING")
        binding.btnSleepWake.text = "☀️ Despertar"
        audioEngine.stopRecording()
        audioEngine.stopAudioPlayback()
    }

    private fun wakeViernes() {
        setAssistantState("LISTENING")
        binding.btnSleepWake.text = "🌙 Reposo"
        audioEngine.startRecording()
        binding.avatarWebView.evaluateJavascript("window.triggerExpression('greeting_wave', 2000);", null)
    }

    private fun setAssistantState(state: String) {
        currentModeState = state
        binding.avatarWebView.evaluateJavascript("window.setState('$state');", null)
    }

    // =========================================================================
    // CHAT BUBBLES UI
    // =========================================================================
    private fun addChatBubble(sender: String, message: String, isAssistant: Boolean) {
        val bubble = TextView(this).apply {
            text = "$sender: $message"
            textSize = 13f
            setPadding(24, 16, 24, 16)
            setTextColor(Color.WHITE)
            val bgRes = if (isAssistant) R.color.bg_card else R.color.bg_input
            setBackgroundColor(ContextCompat.getColor(context, bgRes))

            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, 8, 0, 8)
            }
            layoutParams = params
        }

        binding.chatContainer.addView(bubble)
        binding.chatScrollView.post {
            binding.chatScrollView.fullScroll(View.FOCUS_DOWN)
        }
    }

    private fun addToolBubble(message: String, isTool: Boolean) {
        val bubble = TextView(this).apply {
            text = message
            textSize = 12f
            setPadding(20, 10, 20, 10)
            setTextColor(if (isTool) ContextCompat.getColor(context, R.color.cyan_accent) else ContextCompat.getColor(context, R.color.emerald_glow))
            setBackgroundColor(ContextCompat.getColor(context, R.color.bg_obsidian))

            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, 4, 0, 4)
            }
            layoutParams = params
        }

        binding.chatContainer.addView(bubble)
        binding.chatScrollView.post {
            binding.chatScrollView.fullScroll(View.FOCUS_DOWN)
        }
    }

    // =========================================================================
    // NAVEGACIÓN ENTRE PESTAÑAS (ASISTENTE, ENLACE PC, AJUSTES)
    // =========================================================================
    private fun setupNavigationTabs() {
        binding.tabBtnAssistant.setOnClickListener { switchTab(0) }
        binding.tabBtnPcLink.setOnClickListener { switchTab(1) }
        binding.tabBtnSettings.setOnClickListener { switchTab(2) }
    }

    private fun switchTab(index: Int) {
        binding.viewAssistant.visibility = if (index == 0) View.VISIBLE else View.GONE
        binding.viewPcLink.visibility = if (index == 1) View.VISIBLE else View.GONE
        binding.viewSettings.visibility = if (index == 2) View.VISIBLE else View.GONE

        val activeColor = ContextCompat.getColor(this, R.color.emerald_glow)
        val inactiveColor = ContextCompat.getColor(this, R.color.text_secondary)

        binding.tabBtnAssistant.setTextColor(if (index == 0) activeColor else inactiveColor)
        binding.tabBtnPcLink.setTextColor(if (index == 1) activeColor else inactiveColor)
        binding.tabBtnSettings.setTextColor(if (index == 2) activeColor else inactiveColor)

        if (index == 1 && binding.pcRemoteWebView.url.isNullOrBlank()) {
            val url = binding.etPcUrl.text.toString().trim()
            if (url.isNotBlank()) binding.pcRemoteWebView.loadUrl(url)
        }
    }

    // =========================================================================
    // PESTAÑA AJUSTES & VOCES
    // =========================================================================
    private fun setupSettingsUi() {
        // Cargar valores guardados
        binding.etGeminiKey.setText(configManager.geminiApiKey)
        binding.etAssistantName.setText(configManager.assistantName)
        binding.etUserName.setText(configManager.userName)
        binding.etElevenKey.setText(configManager.elevenlabsApiKey)
        binding.etElevenVoiceId.setText(configManager.elevenlabsVoiceId)

        if (configManager.ttsEngine == "elevenlabs") {
            binding.rbEngineElevenLabs.isChecked = true
        } else {
            binding.rbEngineGemini.isChecked = true
        }

        // Spinner Voces Gemini
        val geminiVoices = arrayOf("Aoede", "Kore", "Leda", "Zephyr", "Puck", "Charon", "Fenrir", "Orus")
        val voiceAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, geminiVoices)
        binding.spinnerGeminiVoice.adapter = voiceAdapter
        val vIdx = geminiVoices.indexOf(configManager.voiceName)
        if (vIdx >= 0) binding.spinnerGeminiVoice.setSelection(vIdx)

        // Spinner Estilo Vocal
        val styles = arrayOf("Natural", "Cálida y Cercana", "Ejecutiva Jarvis", "Enérgica", "Susurro Suave", "Serena")
        val styleCodes = arrayOf("natural", "warm", "jarvis", "energetic", "whisper", "serene")
        val styleAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, styles)
        binding.spinnerVoiceStyle.adapter = styleAdapter
        val sIdx = styleCodes.indexOf(configManager.voiceStyle)
        if (sIdx >= 0) binding.spinnerVoiceStyle.setSelection(sIdx)

        // Guardar Ajustes
        binding.btnSaveSettings.setOnClickListener {
            configManager.geminiApiKey = binding.etGeminiKey.text.toString().trim()
            configManager.assistantName = binding.etAssistantName.text.toString().trim()
            configManager.userName = binding.etUserName.text.toString().trim()
            configManager.ttsEngine = if (binding.rbEngineElevenLabs.isChecked) "elevenlabs" else "gemini"
            configManager.voiceName = binding.spinnerGeminiVoice.selectedItem?.toString() ?: "Aoede"
            configManager.voiceStyle = styleCodes[binding.spinnerVoiceStyle.selectedItemPosition]
            configManager.elevenlabsApiKey = binding.etElevenKey.text.toString().trim()
            configManager.elevenlabsVoiceId = binding.etElevenVoiceId.text.toString().trim()

            Toast.makeText(this, "Ajustes guardados. Reiniciando sesión...", Toast.LENGTH_SHORT).show()
            disconnectLiveSession()
            connectLiveSession()
            switchTab(0)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        geminiClient.disconnect()
        audioEngine.release()
    }
}
