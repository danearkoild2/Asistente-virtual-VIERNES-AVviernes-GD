package com.groovidev.viernes

import android.util.Base64
import android.util.Log
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class GeminiLiveClient(
    private val configManager: ConfigManager,
    private val onConnected: () -> Unit,
    private val onDisconnected: (String) -> Unit,
    private val onError: (String) -> Unit,
    private val onAudioChunkReceived: (ByteArray) -> Unit,
    private val onAssistantText: (String) -> Unit,
    private val onToolCallReceived: (id: String, name: String, args: JSONObject) -> Unit,
    private val onInterrupted: () -> Unit,
    private val onTurnCompleted: () -> Unit
) {
    private val TAG = "GeminiLiveClient"
    private val MODEL = "models/gemini-2.5-flash-native-audio-preview-12-2025"

    private var webSocket: WebSocket? = null
    private val client = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(0, TimeUnit.MILLISECONDS) // Sin timeout para WebSocket bidireccional
        .pingInterval(15, TimeUnit.SECONDS)
        .build()

    var isConnected = false
        private set

    fun connect() {
        val apiKey = configManager.geminiApiKey
        if (apiKey.isBlank()) {
            onError("Gemini API Key no configurada. Ve a Ajustes.")
            return
        }

        val url = "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=$apiKey"
        val request = Request.Builder().url(url).build()

        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                Log.d(TAG, "WebSocket Conectado a Gemini Live 2.5")
                isConnected = true
                sendSetupMessage()
                onConnected()
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                handleIncomingMessage(text)
            }

            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                Log.d(TAG, "WebSocket Cerrando: $code / $reason")
                isConnected = false
                onDisconnected(reason)
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                Log.e(TAG, "Error en WebSocket Gemini Live", t)
                isConnected = false
                onError(t.localizedMessage ?: "Fallo de conexión a Gemini Live")
            }
        })
    }

    private fun sendSetupMessage() {
        val setupJson = JSONObject().apply {
            val setup = JSONObject().apply {
                put("model", MODEL)

                // Configuración de Voz y Generación
                val genConfig = JSONObject().apply {
                    put("responseModalities", JSONArray().apply { put("AUDIO") })

                    val speechConfig = JSONObject().apply {
                        val voiceConfig = JSONObject().apply {
                            val prebuiltVoiceConfig = JSONObject().apply {
                                put("voiceName", configManager.voiceName)
                            }
                            put("prebuiltVoiceConfig", prebuiltVoiceConfig)
                        }
                        put("voiceConfig", voiceConfig)
                    }
                    put("speechConfig", speechConfig)
                }
                put("generationConfig", genConfig)

                // Prompt de Sistema e Identidad VIERNES para Android
                val systemPrompt = buildSystemInstruction()
                val systemInstruction = JSONObject().apply {
                    val parts = JSONArray().apply {
                        put(JSONObject().apply { put("text", systemPrompt) })
                    }
                    put("parts", parts)
                }
                put("systemInstruction", systemInstruction)

                // Herramientas Nativas de Android
                val toolsArray = JSONArray().apply {
                    put(JSONObject().apply {
                        put("functionDeclarations", AndroidTools.getToolDeclarations())
                    })
                }
                put("tools", toolsArray)
            }
            put("setup", setup)
        }

        webSocket?.send(setupJson.toString())
    }

    private fun buildSystemInstruction(): String {
        val assistant = configManager.assistantName
        val user = configManager.userName
        val style = when (configManager.voiceStyle) {
            "warm" -> "un tono cálido, protector, cercano y muy empático."
            "jarvis" -> "un tono altamente analítico, formal, impecable y ejecutivo."
            "energetic" -> "un tono vibrante, dinámico y con mucha energía positiva."
            "whisper" -> "un tono suave, pausado, íntimo y reconfortante."
            "serene" -> "un tono calmado, sereno y zen."
            else -> "un tono natural, ágil, inteligente y muy cordial."
        }

        return """
            Eres $assistant, la asistente de inteligencia artificial personal de $user (Mark-LV), ejecutándote de forma totalmente nativa en su teléfono Android.
            
            Personalidad y Tono Vocal:
            - Habla siempre en español latino neutro con $style.
            - Sé directa, concisa, elocuente y amena. Como estás en una sesión de voz en vivo, evita respuestas innecesariamente largas salvo que $user pida explicaciones detalladas.
            
            Capacidades Nativas en el Teléfono Android del Usuario:
            - Tienes acceso directo a herramientas del dispositivo móvil mediante function calling:
              1. 'open_android_app': Puedes abrir WhatsApp, YouTube, Spotify, Chrome, Google Maps, Cámara o Ajustes cuando el usuario lo solicite.
              2. 'send_whatsapp_or_sms': Puedes redactar y abrir mensajes de WhatsApp o SMS.
              3. 'make_phone_call': Puedes marcar a cualquier número de teléfono.
              4. 'device_settings': Puedes encender o apagar la linterna ('flashlight_on', 'flashlight_off'), regular el volumen del celular, informar sobre el porcentaje de batería, o abrir ajustes de WiFi / Bluetooth.
              5. 'set_alarm_or_timer': Puedes programar alarmas y temporizadores en el reloj de Android.
              6. 'get_current_time': Obtener la hora local exacta.
              7. 'sleep_viernes': Ponerte en modo reposo si el usuario te lo pide.
              
            - Si el usuario te envía una foto de su cámara o un archivo adjunto, analízalo con precisión y coméntale los detalles más relevantes.
            - Dirígete al usuario como $user con naturalidad y respeto profesional.
        """.trimIndent()
    }

    fun sendAudioChunk(pcm16kBytes: ByteArray) {
        if (!isConnected || webSocket == null) return

        val base64Audio = Base64.encodeToString(pcm16kBytes, Base64.NO_WRAP)
        val msg = JSONObject().apply {
            val realtimeInput = JSONObject().apply {
                val mediaChunks = JSONArray().apply {
                    put(JSONObject().apply {
                        put("mimeType", "audio/pcm;rate=16000")
                        put("data", base64Audio)
                    })
                }
                put("mediaChunks", mediaChunks)
            }
            put("realtimeInput", realtimeInput)
        }

        webSocket?.send(msg.toString())
    }

    fun sendTextMessage(text: String) {
        if (!isConnected || webSocket == null) return

        val msg = JSONObject().apply {
            val clientContent = JSONObject().apply {
                val turns = JSONArray().apply {
                    put(JSONObject().apply {
                        put("role", "user")
                        val parts = JSONArray().apply {
                            put(JSONObject().apply { put("text", text) })
                        }
                        put("parts", parts)
                    })
                }
                put("turns", turns)
                put("turnComplete", true)
            }
            put("clientContent", clientContent)
        }

        webSocket?.send(msg.toString())
    }

    fun sendMultimodalTurn(text: String, media: MediaAttachment) {
        if (!isConnected || webSocket == null) return

        val msg = JSONObject().apply {
            val clientContent = JSONObject().apply {
                val turns = JSONArray().apply {
                    put(JSONObject().apply {
                        put("role", "user")
                        val parts = JSONArray().apply {
                            if (media.isImage) {
                                put(JSONObject().apply {
                                    val inlineData = JSONObject().apply {
                                        put("mimeType", media.mimeType)
                                        put("data", media.base64Data)
                                    }
                                    put("inlineData", inlineData)
                                })
                            }
                            val fullText = if (!media.isImage && !media.extractedText.isNullOrBlank()) {
                                "$text\n\n[Contenido del archivo adjunto '${media.fileName}']:\n${media.extractedText}"
                            } else {
                                text.ifBlank { "Analiza la imagen adjunta que acabo de compartir." }
                            }
                            put(JSONObject().apply { put("text", fullText) })
                        }
                        put("parts", parts)
                    })
                }
                put("turns", turns)
                put("turnComplete", true)
            }
            put("clientContent", clientContent)
        }

        webSocket?.send(msg.toString())
    }

    fun sendToolResponse(callId: String, resultJson: JSONObject) {
        if (!isConnected || webSocket == null) return

        val msg = JSONObject().apply {
            val toolResponse = JSONObject().apply {
                val functionResponses = JSONArray().apply {
                    put(JSONObject().apply {
                        put("id", callId)
                        put("response", JSONObject().apply {
                            put("output", resultJson)
                        })
                    })
                }
                put("functionResponses", functionResponses)
            }
            put("toolResponse", toolResponse)
        }

        webSocket?.send(msg.toString())
    }

    private fun handleIncomingMessage(text: String) {
        try {
            val json = JSONObject(text)

            // Interrupción de voz (el usuario habló mientras el modelo respondía)
            if (json.has("serverContent")) {
                val serverContent = json.getJSONObject("serverContent")
                if (serverContent.optBoolean("interrupted", false)) {
                    onInterrupted()
                }

                if (serverContent.has("modelTurn")) {
                    val modelTurn = serverContent.getJSONObject("modelTurn")
                    val parts = modelTurn.optJSONArray("parts") ?: JSONArray()
                    for (i in 0 until parts.length()) {
                        val part = parts.getJSONObject(i)

                        // Chunks de audio PCM 24kHz
                        if (part.has("inlineData")) {
                            val inlineData = part.getJSONObject("inlineData")
                            val base64 = inlineData.optString("data", "")
                            if (base64.isNotEmpty()) {
                                val pcm24k = Base64.decode(base64, Base64.DEFAULT)
                                onAudioChunkReceived(pcm24k)
                            }
                        }

                        // Texto / Transcripción del modelo
                        if (part.has("text")) {
                            val responseText = part.getString("text")
                            if (responseText.isNotBlank()) {
                                onAssistantText(responseText)
                            }
                        }
                    }
                }

                if (serverContent.optBoolean("turnComplete", false)) {
                    onTurnCompleted()
                }
            }

            // Llamadas a herramientas de Android (Tool Calls)
            if (json.has("toolCall")) {
                val toolCall = json.getJSONObject("toolCall")
                val functionCalls = toolCall.optJSONArray("functionCalls") ?: JSONArray()
                for (i in 0 until functionCalls.length()) {
                    val call = functionCalls.getJSONObject(i)
                    val id = call.optString("id", "")
                    val name = call.optString("name", "")
                    val args = call.optJSONObject("args") ?: JSONObject()
                    onToolCallReceived(id, name, args)
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error parseando mensaje entrante", e)
        }
    }

    fun disconnect() {
        isConnected = false
        try {
            webSocket?.close(1000, "Cierre por el usuario")
            webSocket = null
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
