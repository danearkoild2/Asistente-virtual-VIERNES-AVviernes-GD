package com.groovidev.viernes

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.hardware.camera2.CameraManager
import android.media.AudioManager
import android.net.Uri
import android.os.BatteryManager
import android.provider.AlarmClock
import android.provider.Settings
import org.json.JSONArray
import org.json.JSONObject
import java.net.URLEncoder
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class AndroidTools(private val activity: Activity) {

    private val cameraManager = activity.getSystemService(Context.CAMERA_SERVICE) as? CameraManager
    private val audioManager = activity.getSystemService(Context.AUDIO_SERVICE) as? AudioManager
    private var isTorchOn = false

    companion object {
        fun getToolDeclarations(): JSONArray {
            val tools = JSONArray()

            // Tool 1: open_android_app
            val openApp = JSONObject().apply {
                put("name", "open_android_app")
                put("description", "Abre cualquier aplicación instalada en el teléfono Android del usuario, como WhatsApp, YouTube, Spotify, Google Maps, Chrome, Cámara, Configuración, etc.")
                val params = JSONObject().apply {
                    put("type", "object")
                    val props = JSONObject().apply {
                        val appName = JSONObject().apply {
                            put("type", "string")
                            put("description", "Nombre o identificador de la aplicación a abrir (ej. 'whatsapp', 'youtube', 'spotify', 'maps', 'chrome', 'camera', 'settings').")
                        }
                        put("app_name", appName)
                    }
                    put("properties", props)
                    put("required", JSONArray().apply { put("app_name") })
                }
                put("parameters", params)
            }

            // Tool 2: send_whatsapp_or_sms
            val sendMsg = JSONObject().apply {
                put("name", "send_whatsapp_or_sms")
                put("description", "Envía o abre un mensaje de WhatsApp o SMS en el teléfono Android con el texto indicado.")
                val params = JSONObject().apply {
                    put("type", "object")
                    val props = JSONObject().apply {
                        val recipient = JSONObject().apply {
                            put("type", "string")
                            put("description", "Número telefónico con código de país (ej. +521...) o vacío para elegir contacto.")
                        }
                        val message = JSONObject().apply {
                            put("type", "string")
                            put("description", "Texto del mensaje a enviar.")
                        }
                        val app = JSONObject().apply {
                            put("type", "string")
                            put("description", "'whatsapp' o 'sms'. Por defecto 'whatsapp'.")
                        }
                        put("recipient", recipient)
                        put("message", message)
                        put("app", app)
                    }
                    put("properties", props)
                    put("required", JSONArray().apply { put("message") })
                }
                put("parameters", params)
            }

            // Tool 3: make_phone_call
            val call = JSONObject().apply {
                put("name", "make_phone_call")
                put("description", "Abre el marcador telefónico o llama a un número de teléfono en Android.")
                val params = JSONObject().apply {
                    put("type", "object")
                    val props = JSONObject().apply {
                        val number = JSONObject().apply {
                            put("type", "string")
                            put("description", "Número telefónico a marcar.")
                        }
                        put("phone_number", number)
                    }
                    put("properties", props)
                    put("required", JSONArray().apply { put("phone_number") })
                }
                put("parameters", params)
            }

            // Tool 4: device_settings
            val devSettings = JSONObject().apply {
                put("name", "device_settings")
                put("description", "Controla funciones nativas del hardware del teléfono: linterna (encender/apagar), volumen del sistema, consultar nivel de batería, o abrir ajustes de WiFi / Bluetooth.")
                val params = JSONObject().apply {
                    put("type", "object")
                    val props = JSONObject().apply {
                        val action = JSONObject().apply {
                            put("type", "string")
                            put("description", "Acción a realizar: 'flashlight_on', 'flashlight_off', 'flashlight_toggle', 'get_battery', 'set_volume', 'open_wifi_settings', 'open_bluetooth_settings'.")
                        }
                        val value = JSONObject().apply {
                            put("type", "string")
                            put("description", "Valor adicional si aplica, ej. porcentaje de volumen (0 a 100).")
                        }
                        put("action", action)
                        put("value", value)
                    }
                    put("properties", props)
                    put("required", JSONArray().apply { put("action") })
                }
                put("parameters", params)
            }

            // Tool 5: set_alarm_or_timer
            val alarm = JSONObject().apply {
                put("name", "set_alarm_or_timer")
                put("description", "Configura una alarma despertadora o un temporizador cuenta regresiva en el reloj nativo de Android.")
                val params = JSONObject().apply {
                    put("type", "object")
                    val props = JSONObject().apply {
                        val kind = JSONObject().apply {
                            put("type", "string")
                            put("description", "'alarm' para alarma o 'timer' para temporizador.")
                        }
                        val hour = JSONObject().apply {
                            put("type", "integer")
                            put("description", "Hora de la alarma (0-23).")
                        }
                        val minute = JSONObject().apply {
                            put("type", "integer")
                            put("description", "Minuto de la alarma (0-59).")
                        }
                        val seconds = JSONObject().apply {
                            put("type", "integer")
                            put("description", "Segundos de duración si es un temporizador.")
                        }
                        val label = JSONObject().apply {
                            put("type", "string")
                            put("description", "Etiqueta o motivo de la alarma/temporizador.")
                        }
                        put("type", kind)
                        put("hour", hour)
                        put("minute", minute)
                        put("seconds", seconds)
                        put("label", label)
                    }
                    put("properties", props)
                    put("required", JSONArray().apply { put("type") })
                }
                put("parameters", params)
            }

            // Tool 6: get_current_time
            val timeTool = JSONObject().apply {
                put("name", "get_current_time")
                put("description", "Obtiene la fecha y hora exacta del sistema local del teléfono.")
                val params = JSONObject().apply {
                    put("type", "object")
                    put("properties", JSONObject())
                }
                put("parameters", params)
            }

            // Tool 7: sleep_viernes
            val sleepTool = JSONObject().apply {
                put("name", "sleep_viernes")
                put("description", "Pone a VIERNES en modo de reposo o descanso en el teléfono móvil.")
                val params = JSONObject().apply {
                    put("type", "object")
                    put("properties", JSONObject())
                }
                put("parameters", params)
            }

            tools.put(openApp)
            tools.put(sendMsg)
            tools.put(call)
            tools.put(devSettings)
            tools.put(alarm)
            tools.put(timeTool)
            tools.put(sleepTool)

            return tools
        }
    }

    fun execute(callName: String, args: JSONObject, onSleepCallback: (() -> Unit)? = null): JSONObject {
        val result = JSONObject()
        try {
            when (callName) {
                "open_android_app" -> {
                    val appName = args.optString("app_name", "").lowercase()
                    val res = openApp(appName)
                    result.put("status", if (res.first) "success" else "error")
                    result.put("message", res.second)
                }
                "send_whatsapp_or_sms" -> {
                    val recipient = args.optString("recipient", "")
                    val message = args.optString("message", "")
                    val app = args.optString("app", "whatsapp").lowercase()
                    val res = sendWhatsAppOrSms(recipient, message, app)
                    result.put("status", if (res.first) "success" else "error")
                    result.put("message", res.second)
                }
                "make_phone_call" -> {
                    val phone = args.optString("phone_number", "")
                    val res = makePhoneCall(phone)
                    result.put("status", if (res.first) "success" else "error")
                    result.put("message", res.second)
                }
                "device_settings" -> {
                    val action = args.optString("action", "")
                    val value = args.optString("value", "")
                    val res = handleDeviceSettings(action, value)
                    result.put("status", if (res.first) "success" else "error")
                    result.put("message", res.second)
                }
                "set_alarm_or_timer" -> {
                    val kind = args.optString("type", "alarm")
                    val hour = args.optInt("hour", 8)
                    val min = args.optInt("minute", 0)
                    val sec = args.optInt("seconds", 300)
                    val label = args.optString("label", "Alarma VIERNES")
                    val res = setAlarmOrTimer(kind, hour, min, sec, label)
                    result.put("status", if (res.first) "success" else "error")
                    result.put("message", res.second)
                }
                "get_current_time" -> {
                    val sdf = SimpleDateFormat("EEEE, d 'de' MMMM 'de' yyyy, HH:mm:ss", Locale("es", "ES"))
                    val now = sdf.format(Date())
                    result.put("status", "success")
                    result.put("current_time", now)
                }
                "sleep_viernes" -> {
                    activity.runOnUiThread { onSleepCallback?.invoke() }
                    result.put("status", "success")
                    result.put("message", "VIERNES ha entrado en modo reposo.")
                }
                else -> {
                    result.put("status", "error")
                    result.put("message", "Herramienta desconocida: $callName")
                }
            }
        } catch (e: Exception) {
            result.put("status", "error")
            result.put("message", e.localizedMessage ?: "Excepción al ejecutar herramienta")
        }
        return result
    }

    private fun openApp(appName: String): Pair<Boolean, String> {
        val pm = activity.packageManager
        val targetPackage = when {
            appName.contains("whatsapp") -> "com.whatsapp"
            appName.contains("youtube") -> "com.google.android.youtube"
            appName.contains("spotify") -> "com.spotify.music"
            appName.contains("chrome") || appName.contains("navegador") -> "com.android.chrome"
            appName.contains("map") || appName.contains("gps") -> "com.google.android.apps.maps"
            appName.contains("camara") || appName.contains("camera") -> {
                val intent = Intent("android.media.action.IMAGE_CAPTURE")
                activity.startActivity(intent)
                return Pair(true, "Cámara abierta correctamente.")
            }
            appName.contains("ajustes") || appName.contains("config") || appName.contains("setting") -> {
                val intent = Intent(Settings.ACTION_SETTINGS)
                activity.startActivity(intent)
                return Pair(true, "Ajustes del teléfono abiertos.")
            }
            else -> findPackageByName(appName)
        }

        if (targetPackage != null) {
            val launchIntent = pm.getLaunchIntentForPackage(targetPackage)
            if (launchIntent != null) {
                activity.startActivity(launchIntent)
                return Pair(true, "Aplicación '$appName' ($targetPackage) abierta con éxito.")
            }
        }

        return Pair(false, "No se encontró la aplicación '$appName' en el teléfono.")
    }

    private fun findPackageByName(query: String): String? {
        val pm = activity.packageManager
        val packages = pm.getInstalledApplications(PackageManager.GET_META_DATA)
        for (app in packages) {
            val label = pm.getApplicationLabel(app).toString().lowercase()
            if (label.contains(query) || app.packageName.lowercase().contains(query)) {
                return app.packageName
            }
        }
        return null
    }

    private fun sendWhatsAppOrSms(recipient: String, message: String, app: String): Pair<Boolean, String> {
        return try {
            val cleanPhone = recipient.replace(Regex("[^0-9+]"), "")
            if (app == "whatsapp") {
                val url = if (cleanPhone.isNotEmpty()) {
                    "https://wa.me/$cleanPhone?text=${URLEncoder.encode(message, "UTF-8")}"
                } else {
                    "https://api.whatsapp.com/send?text=${URLEncoder.encode(message, "UTF-8")}"
                }
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
                activity.startActivity(intent)
                Pair(true, "WhatsApp abierto con el mensaje listo para enviar.")
            } else {
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse("sms:$cleanPhone")).apply {
                    putExtra("sms_body", message)
                }
                activity.startActivity(intent)
                Pair(true, "SMS preparado en la aplicación de mensajería.")
            }
        } catch (e: Exception) {
            Pair(false, "Error al abrir mensajería: ${e.message}")
        }
    }

    private fun makePhoneCall(phoneNumber: String): Pair<Boolean, String> {
        return try {
            val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:${phoneNumber.trim()}"))
            activity.startActivity(intent)
            Pair(true, "Marcador telefónico abierto con el número $phoneNumber.")
        } catch (e: Exception) {
            Pair(false, "No se pudo abrir el marcador telefónico: ${e.message}")
        }
    }

    fun handleDeviceSettings(action: String, value: String): Pair<Boolean, String> {
        return try {
            when (action) {
                "flashlight_on" -> {
                    setTorch(true)
                    Pair(true, "Linterna encendida.")
                }
                "flashlight_off" -> {
                    setTorch(false)
                    Pair(true, "Linterna apagada.")
                }
                "flashlight_toggle" -> {
                    isTorchOn = !isTorchOn
                    setTorch(isTorchOn)
                    Pair(true, if (isTorchOn) "Linterna encendida." else "Linterna apagada.")
                }
                "get_battery" -> {
                    val bm = activity.getSystemService(Context.BATTERY_SERVICE) as? BatteryManager
                    val level = bm?.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY) ?: -1
                    val isCharging = bm?.isCharging ?: false
                    Pair(true, "Batería del teléfono al $level% ${if (isCharging) "(Cargando)" else "(En uso)"}.")
                }
                "set_volume" -> {
                    val targetPercent = value.toIntOrNull() ?: 60
                    val am = audioManager ?: return Pair(false, "Audio no disponible")
                    val maxVol = am.getStreamMaxVolume(AudioManager.STREAM_MUSIC)
                    val targetVol = (maxVol * (targetPercent / 100f)).toInt().coerceIn(0, maxVol)
                    am.setStreamVolume(AudioManager.STREAM_MUSIC, targetVol, AudioManager.FLAG_SHOW_UI)
                    Pair(true, "Volumen ajustado al $targetPercent% (nivel $targetVol de $maxVol).")
                }
                "open_wifi_settings" -> {
                    activity.startActivity(Intent(Settings.ACTION_WIFI_SETTINGS))
                    Pair(true, "Ajustes de Wi-Fi abiertos.")
                }
                "open_bluetooth_settings" -> {
                    activity.startActivity(Intent(Settings.ACTION_BLUETOOTH_SETTINGS))
                    Pair(true, "Ajustes de Bluetooth abiertos.")
                }
                else -> Pair(false, "Acción de configuración no reconocida: $action")
            }
        } catch (e: Exception) {
            Pair(false, "Error ejecutando ajuste: ${e.message}")
        }
    }

    private fun setAlarmOrTimer(kind: String, hour: Int, minute: Int, seconds: Int, label: String): Pair<Boolean, String> {
        return try {
            if (kind == "timer") {
                val intent = Intent(AlarmClock.ACTION_SET_TIMER).apply {
                    putExtra(AlarmClock.EXTRA_LENGTH, seconds)
                    putExtra(AlarmClock.EXTRA_MESSAGE, label)
                    putExtra(AlarmClock.EXTRA_SKIP_UI, false)
                }
                activity.startActivity(intent)
                Pair(true, "Temporizador de $seconds segundos configurado ($label).")
            } else {
                val intent = Intent(AlarmClock.ACTION_SET_ALARM).apply {
                    putExtra(AlarmClock.EXTRA_HOUR, hour)
                    putExtra(AlarmClock.EXTRA_MINUTES, minute)
                    putExtra(AlarmClock.EXTRA_MESSAGE, label)
                    putExtra(AlarmClock.EXTRA_SKIP_UI, false)
                }
                activity.startActivity(intent)
                Pair(true, "Alarma programada para las %02d:%02d (%s).".format(hour, minute, label))
            }
        } catch (e: Exception) {
            Pair(false, "No se pudo programar alarma/temporizador: ${e.message}")
        }
    }

    private fun setTorch(enabled: Boolean) {
        val cm = cameraManager ?: return
        try {
            val cameraId = cm.cameraIdList.firstOrNull() ?: return
            cm.setTorchMode(cameraId, enabled)
            isTorchOn = enabled
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
