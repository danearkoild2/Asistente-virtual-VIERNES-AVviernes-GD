package com.viernes.mobile.ui.screens;

import androidx.compose.runtime.DisposableEffectResult;
import com.viernes.mobile.assistant.VoiceManager;
import kotlin.Metadata;
import kotlin.jvm.internal.SourceDebugExtension;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000\u0011\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000*\u0001\u0000\b\n\u0018\u00002\u00020\u0001J\b\u0010\u0002\u001a\u00020\u0003H\u0016¨\u0006\u0004¸\u0006\u0000"},
   d2 = {"androidx/compose/runtime/DisposableEffectScope$onDispose$1", "Landroidx/compose/runtime/DisposableEffectResult;", "dispose", "", "runtime_release"}
)
@SourceDebugExtension({"SMAP\nEffects.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Effects.kt\nandroidx/compose/runtime/DisposableEffectScope$onDispose$1\n+ 2 ChatScreen.kt\ncom/viernes/mobile/ui/screens/ChatScreenKt$ChatScreen$3\n*L\n1#1,497:1\n103#2,3:498\n*E\n"})
public final class ChatScreenKt$ChatScreen$3$invoke$$inlined$onDispose$1 implements DisposableEffectResult {
   // $FF: synthetic field
   final VoiceManager $voiceManager$inlined;

   public ChatScreenKt$ChatScreen$3$invoke$$inlined$onDispose$1(VoiceManager var1) {
      this.$voiceManager$inlined = var1;
   }

   public void dispose() {
      int var1 = 0;
      this.$voiceManager$inlined.stopListening();
      this.$voiceManager$inlined.stopSpeaking();
   }
}
