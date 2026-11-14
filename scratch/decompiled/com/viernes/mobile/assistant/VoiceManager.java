package com.viernes.mobile.assistant;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.util.Log;
import androidx.compose.runtime.internal.StabilityInferred;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Locale;
import java.util.UUID;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.internal.Intrinsics;
import kotlin.ranges.RangesKt;
import kotlinx.coroutines.flow.MutableStateFlow;
import kotlinx.coroutines.flow.StateFlow;
import kotlinx.coroutines.flow.StateFlowKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000R\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\u0007\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\u0010\u000e\n\u0002\u0010\u0002\n\u0002\b\n\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0010\b\n\u0002\b\t\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004J\b\u0010!\u001a\u00020\u0012H\u0002J\u0010\u0010\"\u001a\u00020\u00122\u0006\u0010#\u001a\u00020$H\u0016J\u0006\u0010%\u001a\u00020\u0012J\b\u0010&\u001a\u00020\u0012H\u0002J\u0018\u0010'\u001a\u00020\u00122\u0006\u0010(\u001a\u00020\u00112\b\b\u0002\u0010)\u001a\u00020\u0011J\u0006\u0010*\u001a\u00020\u0012J\u0006\u0010+\u001a\u00020\u0012J\u0006\u0010,\u001a\u00020\u0012R\u0014\u0010\u0005\u001a\b\u0012\u0004\u0012\u00020\u00070\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u0014\u0010\b\u001a\b\u0012\u0004\u0012\u00020\u00070\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u0014\u0010\t\u001a\b\u0012\u0004\u0012\u00020\n0\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u0017\u0010\u000b\u001a\b\u0012\u0004\u0012\u00020\u00070\f¢\u0006\b\n\u0000\u001a\u0004\b\u000b\u0010\rR\u0017\u0010\u000e\u001a\b\u0012\u0004\u0012\u00020\u00070\f¢\u0006\b\n\u0000\u001a\u0004\b\u000e\u0010\rR(\u0010\u000f\u001a\u0010\u0012\u0004\u0012\u00020\u0011\u0012\u0004\u0012\u00020\u0012\u0018\u00010\u0010X\u0086\u000e¢\u0006\u000e\n\u0000\u001a\u0004\b\u0013\u0010\u0014\"\u0004\b\u0015\u0010\u0016R(\u0010\u0017\u001a\u0010\u0012\u0004\u0012\u00020\u0011\u0012\u0004\u0012\u00020\u0012\u0018\u00010\u0010X\u0086\u000e¢\u0006\u000e\n\u0000\u001a\u0004\b\u0018\u0010\u0014\"\u0004\b\u0019\u0010\u0016R\u0017\u0010\u001a\u001a\b\u0012\u0004\u0012\u00020\n0\f¢\u0006\b\n\u0000\u001a\u0004\b\u001b\u0010\rR\u0010\u0010\u001c\u001a\u0004\u0018\u00010\u001dX\u0082\u000e¢\u0006\u0002\n\u0000R\u0010\u0010\u001e\u001a\u0004\u0018\u00010\u001fX\u0082\u000e¢\u0006\u0002\n\u0000R\u000e\u0010 \u001a\u00020\u0007X\u0082\u000e¢\u0006\u0002\n\u0000¨\u0006-"},
   d2 = {"Lcom/viernes/mobile/assistant/VoiceManager;", "Landroid/speech/tts/TextToSpeech$OnInitListener;", "context", "Landroid/content/Context;", "(Landroid/content/Context;)V", "_isListening", "Lkotlinx/coroutines/flow/MutableStateFlow;", "", "_isSpeaking", "_speechAmplitude", "", "isListening", "Lkotlinx/coroutines/flow/StateFlow;", "()Lkotlinx/coroutines/flow/StateFlow;", "isSpeaking", "onSpeechError", "Lkotlin/Function1;", "", "", "getOnSpeechError", "()Lkotlin/jvm/functions/Function1;", "setOnSpeechError", "(Lkotlin/jvm/functions/Function1;)V", "onSpeechRecognized", "getOnSpeechRecognized", "setOnSpeechRecognized", "speechAmplitude", "getSpeechAmplitude", "speechRecognizer", "Landroid/speech/SpeechRecognizer;", "textToSpeech", "Landroid/speech/tts/TextToSpeech;", "ttsReady", "initializeTts", "onInit", "status", "", "release", "setupTtsListener", "speak", "text", "utteranceId", "startListening", "stopListening", "stopSpeaking", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
public final class VoiceManager implements TextToSpeech.OnInitListener {
   @NotNull
   private final Context context;
   @Nullable
   private SpeechRecognizer speechRecognizer;
   @Nullable
   private TextToSpeech textToSpeech;
   private boolean ttsReady;
   @NotNull
   private final MutableStateFlow<Boolean> _isListening;
   @NotNull
   private final StateFlow<Boolean> isListening;
   @NotNull
   private final MutableStateFlow<Boolean> _isSpeaking;
   @NotNull
   private final StateFlow<Boolean> isSpeaking;
   @NotNull
   private final MutableStateFlow<Float> _speechAmplitude;
   @NotNull
   private final StateFlow<Float> speechAmplitude;
   @Nullable
   private Function1<? super String, Unit> onSpeechRecognized;
   @Nullable
   private Function1<? super String, Unit> onSpeechError;
   public static final int $stable = 8;

   public VoiceManager(@NotNull Context context) {
      Intrinsics.checkNotNullParameter(context, "context");
      super();
      this.context = context;
      this._isListening = StateFlowKt.MutableStateFlow(false);
      this.isListening = (StateFlow)this._isListening;
      this._isSpeaking = StateFlowKt.MutableStateFlow(false);
      this.isSpeaking = (StateFlow)this._isSpeaking;
      this._speechAmplitude = StateFlowKt.MutableStateFlow(0.0F);
      this.speechAmplitude = (StateFlow)this._speechAmplitude;
      this.initializeTts();
   }

   @NotNull
   public final StateFlow<Boolean> isListening() {
      return this.isListening;
   }

   @NotNull
   public final StateFlow<Boolean> isSpeaking() {
      return this.isSpeaking;
   }

   @NotNull
   public final StateFlow<Float> getSpeechAmplitude() {
      return this.speechAmplitude;
   }

   @Nullable
   public final Function1<String, Unit> getOnSpeechRecognized() {
      return this.onSpeechRecognized;
   }

   public final void setOnSpeechRecognized(@Nullable Function1<? super String, Unit> var1) {
      this.onSpeechRecognized = var1;
   }

   @Nullable
   public final Function1<String, Unit> getOnSpeechError() {
      return this.onSpeechError;
   }

   public final void setOnSpeechError(@Nullable Function1<? super String, Unit> var1) {
      this.onSpeechError = var1;
   }

   private final void initializeTts() {
      this.textToSpeech = new TextToSpeech(this.context, this);
   }

   public void onInit(int status) {
      if (status == 0) {
         label30: {
            label36: {
               TextToSpeech var10000 = this.textToSpeech;
               Integer result = var10000 != null ? var10000.setLanguage(new Locale("es", "ES")) : null;
               byte var3 = -1;
               if (result != null) {
                  if (result == var3) {
                     break label36;
                  }
               }

               var3 = -2;
               if (result == null) {
                  break label30;
               }

               if (result != var3) {
                  break label30;
               }
            }

            TextToSpeech var5 = this.textToSpeech;
            if (var5 != null) {
               var5.setLanguage(Locale.getDefault());
            }
         }

         this.ttsReady = true;
         this.setupTtsListener();
      } else {
         Log.e("VoiceManager", "Error al inicializar TextToSpeech de Android.");
      }

   }

   private final void setupTtsListener() {
      TextToSpeech var10000 = this.textToSpeech;
      if (var10000 != null) {
         var10000.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            public void onStart(@Nullable String utteranceId) {
               VoiceManager.this._isSpeaking.setValue(true);
               VoiceManager.this._speechAmplitude.setValue(0.7F);
            }

            public void onDone(@Nullable String utteranceId) {
               VoiceManager.this._isSpeaking.setValue(false);
               VoiceManager.this._speechAmplitude.setValue(0.0F);
            }

            public void onError(@Nullable String utteranceId) {
               VoiceManager.this._isSpeaking.setValue(false);
               VoiceManager.this._speechAmplitude.setValue(0.0F);
            }
         });
      }

   }

   public final void startListening() {
      if (!SpeechRecognizer.isRecognitionAvailable(this.context)) {
         Function1 var6 = this.onSpeechError;
         if (var6 != null) {
            var6.invoke("El reconocimiento de voz de Google no está disponible en este dispositivo.");
         }

      } else {
         this.stopSpeaking();
         SpeechRecognizer var1 = SpeechRecognizer.createSpeechRecognizer(this.context);
         int var3 = 0;
         var1.setRecognitionListener(new RecognitionListener() {
            public void onReadyForSpeech(@Nullable Bundle params) {
               VoiceManager.this._isListening.setValue(true);
            }

            public void onBeginningOfSpeech() {
            }

            public void onRmsChanged(float rmsdB) {
               float amp = RangesKt.coerceIn((rmsdB + 2.0F) / 12.0F, 0.0F, 1.0F);
               VoiceManager.this._speechAmplitude.setValue(amp);
            }

            public void onBufferReceived(@Nullable byte[] buffer) {
            }

            public void onEndOfSpeech() {
               VoiceManager.this._isListening.setValue(false);
               VoiceManager.this._speechAmplitude.setValue(0.0F);
            }

            public void onError(int error) {
               VoiceManager.this._isListening.setValue(false);
               VoiceManager.this._speechAmplitude.setValue(0.0F);
               String var10000;
               switch (error) {
                  case 2:
                     var10000 = "Error de conexión en reconocimiento de voz.";
                     break;
                  case 3:
                     var10000 = "Error de grabación de audio.";
                     break;
                  case 4:
                  case 5:
                  case 6:
                  default:
                     var10000 = "Reconocimiento de voz detenido (código " + error + ").";
                     break;
                  case 7:
                     var10000 = "No se reconoció ninguna frase.";
               }

               String msg = var10000;
               Function1 var3 = VoiceManager.this.getOnSpeechError();
               if (var3 != null) {
                  var3.invoke(msg);
               }

            }

            public void onResults(@Nullable Bundle results) {
               VoiceManager.this._isListening.setValue(false);
               VoiceManager.this._speechAmplitude.setValue(0.0F);
               ArrayList matches = results != null ? results.getStringArrayList("results_recognition") : null;
               Collection var3 = (Collection)matches;
               if (var3 != null && !var3.isEmpty()) {
                  String transcript = (String)matches.get(0);
                  Function1 var10000 = VoiceManager.this.getOnSpeechRecognized();
                  if (var10000 != null) {
                     Intrinsics.checkNotNull(transcript);
                     var10000.invoke(transcript);
                  }
               }

            }

            public void onPartialResults(@Nullable Bundle partialResults) {
            }

            public void onEvent(int eventType, @Nullable Bundle params) {
            }
         });
         this.speechRecognizer = var1;
         Intent $this$startListening_u24lambda_u240 = new Intent("android.speech.action.RECOGNIZE_SPEECH");
         int var4 = 0;
         $this$startListening_u24lambda_u240.putExtra("android.speech.extra.LANGUAGE_MODEL", "free_form");
         $this$startListening_u24lambda_u240.putExtra("android.speech.extra.LANGUAGE", "es-ES");
         $this$startListening_u24lambda_u240.putExtra("android.speech.extra.MAX_RESULTS", 1);
         SpeechRecognizer var10000 = this.speechRecognizer;
         if (var10000 != null) {
            var10000.startListening($this$startListening_u24lambda_u240);
         }

      }
   }

   public final void stopListening() {
      try {
         SpeechRecognizer var10000 = this.speechRecognizer;
         if (var10000 != null) {
            var10000.stopListening();
         }

         var10000 = this.speechRecognizer;
         if (var10000 != null) {
            var10000.destroy();
         }

         this.speechRecognizer = null;
         this._isListening.setValue(false);
         this._speechAmplitude.setValue(0.0F);
      } catch (Exception e) {
         Log.e("VoiceManager", "Error deteniendo escucha: " + e.getMessage());
      }

   }

   public final void speak(@NotNull String text, @NotNull String utteranceId) {
      Intrinsics.checkNotNullParameter(text, "text");
      Intrinsics.checkNotNullParameter(utteranceId, "utteranceId");
      if (this.ttsReady && this.textToSpeech != null) {
         this.stopListening();
         TextToSpeech var10000 = this.textToSpeech;
         if (var10000 != null) {
            var10000.speak((CharSequence)text, 0, (Bundle)null, utteranceId);
         }

      }
   }

   // $FF: synthetic method
   public static void speak$default(VoiceManager var0, String var1, String var2, int var3, Object var4) {
      if ((var3 & 2) != 0) {
         String var10000 = UUID.randomUUID().toString();
         Intrinsics.checkNotNullExpressionValue(var10000, "toString(...)");
         var2 = var10000;
      }

      var0.speak(var1, var2);
   }

   public final void stopSpeaking() {
      TextToSpeech var10000 = this.textToSpeech;
      if (var10000 != null ? var10000.isSpeaking() : false) {
         var10000 = this.textToSpeech;
         if (var10000 != null) {
            var10000.stop();
         }
      }

      this._isSpeaking.setValue(false);
      this._speechAmplitude.setValue(0.0F);
   }

   public final void release() {
      this.stopListening();
      TextToSpeech var10000 = this.textToSpeech;
      if (var10000 != null) {
         var10000.shutdown();
      }

      this.textToSpeech = null;
   }
}
