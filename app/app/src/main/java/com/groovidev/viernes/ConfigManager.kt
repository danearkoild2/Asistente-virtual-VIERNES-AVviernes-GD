package com.groovidev.viernes

import android.content.Context
import android.content.SharedPreferences
import org.json.JSONObject
import java.io.InputStreamReader

class ConfigManager(private val context: Context) {

    private val prefs: SharedPreferences =
        context.getSharedPreferences("viernes_prefs", Context.MODE_PRIVATE)

    companion object {
        const val KEY_GEMINI_API_KEY = "gemini_api_key"
        const val KEY_ASSISTANT_NAME = "assistant_name"
        const val KEY_USER_NAME = "user_name"
        const val KEY_TTS_ENGINE = "tts_engine" // "gemini" or "elevenlabs"
        const val KEY_VOICE_NAME = "voice_name" // "Aoede", "Kore", "Leda", "Zephyr", "Puck", "Charon", "Fenrir", "Orus"
        const val KEY_VOICE_STYLE = "voice_style" // "natural", "warm", "jarvis", "energetic", "whisper", "serene"
        const val KEY_ELEVEN_KEY = "elevenlabs_api_key"
        const val KEY_ELEVEN_VOICE_ID = "elevenlabs_voice_id"
        const val KEY_PC_URL = "pc_server_url"
        const val KEY_PC_KEY = "pc_access_key"
    }

    init {
        loadDefaultsFromAssetIfNeeded()
    }

    private fun loadDefaultsFromAssetIfNeeded() {
        if (!prefs.contains(KEY_GEMINI_API_KEY)) {
            try {
                context.assets.open("default_config.json").use { stream ->
                    val text = InputStreamReader(stream).readText()
                    val json = JSONObject(text)
                    val editor = prefs.edit()
                    if (json.has("gemini_api_key")) editor.putString(KEY_GEMINI_API_KEY, json.getString("gemini_api_key"))
                    if (json.has("assistant_name")) editor.putString(KEY_ASSISTANT_NAME, json.getString("assistant_name"))
                    if (json.has("user_name")) editor.putString(KEY_USER_NAME, json.getString("user_name"))
                    if (json.has("tts_engine")) editor.putString(KEY_TTS_ENGINE, json.getString("tts_engine"))
                    if (json.has("voice_name")) editor.putString(KEY_VOICE_NAME, json.getString("voice_name"))
                    if (json.has("voice_style")) editor.putString(KEY_VOICE_STYLE, json.getString("voice_style"))
                    if (json.has("elevenlabs_api_key")) editor.putString(KEY_ELEVEN_KEY, json.getString("elevenlabs_api_key"))
                    if (json.has("elevenlabs_voice_id")) editor.putString(KEY_ELEVEN_VOICE_ID, json.getString("elevenlabs_voice_id"))
                    if (json.has("pc_server_url")) editor.putString(KEY_PC_URL, json.getString("pc_server_url"))
                    if (json.has("pc_access_key")) editor.putString(KEY_PC_KEY, json.getString("pc_access_key"))
                    editor.apply()
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    var geminiApiKey: String
        get() = prefs.getString(KEY_GEMINI_API_KEY, "") ?: ""
        set(value) = prefs.edit().putString(KEY_GEMINI_API_KEY, value.trim()).apply()

    var assistantName: String
        get() = prefs.getString(KEY_ASSISTANT_NAME, "Viernes") ?: "Viernes"
        set(value) = prefs.edit().putString(KEY_ASSISTANT_NAME, value.trim()).apply()

    var userName: String
        get() = prefs.getString(KEY_USER_NAME, "Jesús") ?: "Jesús"
        set(value) = prefs.edit().putString(KEY_USER_NAME, value.trim()).apply()

    var ttsEngine: String
        get() = prefs.getString(KEY_TTS_ENGINE, "gemini") ?: "gemini"
        set(value) = prefs.edit().putString(KEY_TTS_ENGINE, value.trim()).apply()

    var voiceName: String
        get() = prefs.getString(KEY_VOICE_NAME, "Aoede") ?: "Aoede"
        set(value) = prefs.edit().putString(KEY_VOICE_NAME, value.trim()).apply()

    var voiceStyle: String
        get() = prefs.getString(KEY_VOICE_STYLE, "natural") ?: "natural"
        set(value) = prefs.edit().putString(KEY_VOICE_STYLE, value.trim()).apply()

    var elevenlabsApiKey: String
        get() = prefs.getString(KEY_ELEVEN_KEY, "") ?: ""
        set(value) = prefs.edit().putString(KEY_ELEVEN_KEY, value.trim()).apply()

    var elevenlabsVoiceId: String
        get() = prefs.getString(KEY_ELEVEN_VOICE_ID, "XPvfYQ2tvMb3p1coSWGS") ?: "XPvfYQ2tvMb3p1coSWGS"
        set(value) = prefs.edit().putString(KEY_ELEVEN_VOICE_ID, value.trim()).apply()

    var pcServerUrl: String
        get() = prefs.getString(KEY_PC_URL, "http://192.168.100.23:8000") ?: "http://192.168.100.23:8000"
        set(value) = prefs.edit().putString(KEY_PC_URL, value.trim()).apply()

    var pcAccessKey: String
        get() = prefs.getString(KEY_PC_KEY, "") ?: ""
        set(value) = prefs.edit().putString(KEY_PC_KEY, value.trim()).apply()
}
