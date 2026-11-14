package com.groovidev.viernes

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.net.Uri
import android.provider.OpenableColumns
import android.util.Base64
import java.io.ByteArrayOutputStream
import java.io.InputStream
import kotlin.math.max

data class MediaAttachment(
    val fileName: String,
    val mimeType: String,
    val base64Data: String,
    val isImage: Boolean,
    val extractedText: String? = null
)

class FileAndVisionHelper(private val context: Context) {

    fun processUri(uri: Uri): MediaAttachment? {
        val contentResolver = context.contentResolver
        val mimeType = contentResolver.getType(uri) ?: "application/octet-stream"
        val fileName = getFileName(uri)

        return if (mimeType.startsWith("image/")) {
            val bitmap = loadAndScaleBitmap(uri, 1024) ?: return null
            val base64 = bitmapToBase64(bitmap)
            MediaAttachment(
                fileName = fileName,
                mimeType = "image/jpeg",
                base64Data = base64,
                isImage = true
            )
        } else {
            // Documento o archivo de texto / código / pdf
            val text = try {
                contentResolver.openInputStream(uri)?.use { stream ->
                    stream.bufferedReader(Charsets.UTF_8).use { it.readText() }
                } ?: ""
            } catch (e: Exception) {
                "[Archivo no legible en texto plano: $fileName (${e.message})]"
            }

            val base64 = Base64.encodeToString(text.toByteArray(Charsets.UTF_8), Base64.NO_WRAP)
            MediaAttachment(
                fileName = fileName,
                mimeType = "text/plain",
                base64Data = base64,
                isImage = false,
                extractedText = text
            )
        }
    }

    fun processBitmap(bitmap: Bitmap): MediaAttachment {
        val scaled = scaleBitmap(bitmap, 1024)
        val base64 = bitmapToBase64(scaled)
        return MediaAttachment(
            fileName = "camera_snapshot.jpg",
            mimeType = "image/jpeg",
            base64Data = base64,
            isImage = true
        )
    }

    private fun loadAndScaleBitmap(uri: Uri, maxDimension: Int): Bitmap? {
        return try {
            val input: InputStream? = context.contentResolver.openInputStream(uri)
            val fullBitmap = BitmapFactory.decodeStream(input)
            input?.close()
            fullBitmap?.let { scaleBitmap(it, maxDimension) }
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }

    private fun scaleBitmap(bitmap: Bitmap, maxDimension: Int): Bitmap {
        val width = bitmap.width
        val height = bitmap.height
        val maxSide = max(width, height)
        if (maxSide <= maxDimension) return bitmap

        val ratio = maxDimension.toFloat() / maxSide
        val matrix = Matrix().apply { postScale(ratio, ratio) }
        return Bitmap.createBitmap(bitmap, 0, 0, width, height, matrix, true)
    }

    private fun bitmapToBase64(bitmap: Bitmap): String {
        val output = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG, 85, output)
        val bytes = output.toByteArray()
        return Base64.encodeToString(bytes, Base64.NO_WRAP)
    }

    private fun getFileName(uri: Uri): String {
        var name = "archivo"
        val cursor = context.contentResolver.query(uri, null, null, null, null)
        cursor?.use {
            if (it.moveToFirst()) {
                val index = it.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                if (index != -1) {
                    name = it.getString(index)
                }
            }
        }
        return name
    }
}
