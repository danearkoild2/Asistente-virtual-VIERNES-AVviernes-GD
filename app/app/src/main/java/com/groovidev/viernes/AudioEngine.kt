package com.groovidev.viernes

import android.annotation.SuppressLint
import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.AudioTrack
import android.media.MediaRecorder
import android.media.audiofx.AcousticEchoCanceler
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.InputStream
import java.util.concurrent.LinkedBlockingQueue
import java.util.concurrent.TimeUnit
import kotlin.math.abs
import kotlin.math.sqrt

class AudioEngine(
    private val onAudioRecorded: (ByteArray) -> Unit,
    private val onMouthLevel: (Float) -> Unit,
    private val onPlaybackStarted: () -> Unit,
    private val onPlaybackEnded: () -> Unit
) {
    private val TAG = "AudioEngine"

    // Grabación: 16 kHz Mono PCM 16-bit
    private val RECORDER_SAMPLE_RATE = 16000
    private val RECORDER_CHANNELS = AudioFormat.CHANNEL_IN_MONO
    private val RECORDER_ENCODING = AudioFormat.ENCODING_PCM_16BIT

    // Reproducción: 24 kHz Mono PCM 16-bit (Gemini Live & ElevenLabs Flash)
    private val PLAYER_SAMPLE_RATE = 24000
    private val PLAYER_CHANNELS = AudioFormat.CHANNEL_OUT_MONO
    private val PLAYER_ENCODING = AudioFormat.ENCODING_PCM_16BIT

    private var audioRecord: AudioRecord? = null
    private var echoCanceler: AcousticEchoCanceler? = null
    private var recordJob: Job? = null
    private var isRecording = false

    private var audioTrack: AudioTrack? = null
    private val audioQueue = LinkedBlockingQueue<ByteArray>()
    private var playbackJob: Job? = null
    private var isPlaying = false

    private val httpClient = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    init {
        initAudioTrack()
    }

    private fun initAudioTrack() {
        val minBufferSize = AudioTrack.getMinBufferSize(
            PLAYER_SAMPLE_RATE,
            PLAYER_CHANNELS,
            PLAYER_ENCODING
        )
        val bufferSize = maxOf(minBufferSize, 24000 * 2) // 1 segundo de búfer

        audioTrack = AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build()
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setSampleRate(PLAYER_SAMPLE_RATE)
                    .setChannelMask(PLAYER_CHANNELS)
                    .setEncoding(PLAYER_ENCODING)
                    .build()
            )
            .setBufferSizeInBytes(bufferSize)
            .setTransferMode(AudioTrack.MODE_STREAM)
            .build()

        audioTrack?.play()
        startPlaybackWorker()
    }

    private fun startPlaybackWorker() {
        playbackJob = CoroutineScope(Dispatchers.IO).launch {
            while (isActive) {
                try {
                    val chunk = audioQueue.poll(100, TimeUnit.MILLISECONDS)
                    if (chunk != null && chunk.isNotEmpty()) {
                        if (!isPlaying) {
                            isPlaying = true
                            onPlaybackStarted()
                        }

                        // Calcular nivel RMS para lip-sync
                        val rms = calculateRms(chunk)
                        val mouthNorm = (rms / 3200f).coerceIn(0f, 1f)
                        onMouthLevel(mouthNorm)

                        // Reproducir
                        audioTrack?.write(chunk, 0, chunk.size)
                    } else {
                        if (isPlaying && audioQueue.isEmpty()) {
                            isPlaying = false
                            onMouthLevel(0f)
                            onPlaybackEnded()
                        }
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "Error en reproducción de audio", e)
                }
            }
        }
    }

    fun playAudioChunk(pcm24kBytes: ByteArray) {
        audioQueue.offer(pcm24kBytes)
    }

    fun stopAudioPlayback() {
        audioQueue.clear()
        audioTrack?.pause()
        audioTrack?.flush()
        audioTrack?.play()
        isPlaying = false
        onMouthLevel(0f)
        onPlaybackEnded()
    }

    @SuppressLint("MissingPermission")
    fun startRecording() {
        if (isRecording) return

        val minBufSize = AudioRecord.getMinBufferSize(
            RECORDER_SAMPLE_RATE,
            RECORDER_CHANNELS,
            RECORDER_ENCODING
        )
        val bufferSize = maxOf(minBufSize, 2048)

        try {
            audioRecord = AudioRecord(
                MediaRecorder.AudioSource.VOICE_COMMUNICATION,
                RECORDER_SAMPLE_RATE,
                RECORDER_CHANNELS,
                RECORDER_ENCODING,
                bufferSize
            )

            if (AcousticEchoCanceler.isAvailable()) {
                echoCanceler = AcousticEchoCanceler.create(audioRecord!!.audioSessionId)?.apply {
                    enabled = true
                }
            }

            audioRecord?.startRecording()
            isRecording = true

            recordJob = CoroutineScope(Dispatchers.IO).launch {
                val buffer = ByteArray(1024)
                while (isActive && isRecording) {
                    val read = audioRecord?.read(buffer, 0, buffer.size) ?: 0
                    if (read > 0) {
                        val chunk = buffer.copyOf(read)
                        onAudioRecorded(chunk)
                    }
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error al iniciar grabación", e)
            stopRecording()
        }
    }

    fun stopRecording() {
        isRecording = false
        recordJob?.cancel()
        recordJob = null
        try {
            echoCanceler?.release()
            echoCanceler = null
            audioRecord?.stop()
            audioRecord?.release()
            audioRecord = null
        } catch (e: Exception) {
            Log.e(TAG, "Error al detener grabación", e)
        }
    }

    fun streamElevenLabs(text: String, apiKey: String, voiceId: String) {
        if (apiKey.isBlank() || text.isBlank()) return

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val url = "https://api.elevenlabs.io/v1/text-to-speech/$voiceId/stream?output_format=pcm_24000"
                val bodyJson = JSONObject().apply {
                    put("text", text)
                    put("model_id", "eleven_flash_v2_5")
                    put("voice_settings", JSONObject().apply {
                        put("stability", 0.45)
                        put("similarity_boost", 0.85)
                    })
                }

                val request = Request.Builder()
                    .url(url)
                    .addHeader("xi-api-key", apiKey)
                    .addHeader("Content-Type", "application/json")
                    .post(bodyJson.toString().toRequestBody("application/json".toMediaType()))
                    .build()

                httpClient.newCall(request).execute().use { response ->
                    if (!response.isSuccessful) {
                        Log.e(TAG, "Error ElevenLabs: ${response.code}")
                        return@launch
                    }
                    val stream: InputStream = response.body?.byteStream() ?: return@launch
                    val buffer = ByteArray(2048)
                    var read: Int
                    while (stream.read(buffer).also { read = it } != -1) {
                        val chunk = buffer.copyOf(read)
                        playAudioChunk(chunk)
                    }
                }
            } catch (e: Exception) {
                Log.e(TAG, "Excepción en stream ElevenLabs", e)
            }
        }
    }

    private fun calculateRms(pcmBytes: ByteArray): Float {
        var sum = 0.0
        val sampleCount = pcmBytes.size / 2
        if (sampleCount == 0) return 0f

        for (i in 0 until sampleCount) {
            val sample = (pcmBytes[i * 2 + 1].toInt() shl 8) or (pcmBytes[i * 2].toInt() and 0xFF)
            sum += abs(sample.toDouble())
        }
        return (sum / sampleCount).toFloat()
    }

    fun release() {
        stopRecording()
        stopAudioPlayback()
        playbackJob?.cancel()
        audioTrack?.release()
        audioTrack = null
    }
}
