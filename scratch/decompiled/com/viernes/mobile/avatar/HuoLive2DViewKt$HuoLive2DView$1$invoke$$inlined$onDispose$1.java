package com.viernes.mobile.avatar;

import android.webkit.WebView;
import androidx.compose.runtime.DisposableEffectResult;
import androidx.compose.runtime.MutableState;
import androidx.lifecycle.LifecycleEventObserver;
import androidx.lifecycle.LifecycleObserver;
import androidx.lifecycle.LifecycleOwner;
import kotlin.Metadata;
import kotlin.jvm.internal.SourceDebugExtension;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000\u0011\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000*\u0001\u0000\b\n\u0018\u00002\u00020\u0001J\b\u0010\u0002\u001a\u00020\u0003H\u0016¨\u0006\u0004¸\u0006\u0000"},
   d2 = {"androidx/compose/runtime/DisposableEffectScope$onDispose$1", "Landroidx/compose/runtime/DisposableEffectResult;", "dispose", "", "runtime_release"}
)
@SourceDebugExtension({"SMAP\nEffects.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Effects.kt\nandroidx/compose/runtime/DisposableEffectScope$onDispose$1\n+ 2 HuoLive2DView.kt\ncom/viernes/mobile/avatar/HuoLive2DViewKt$HuoLive2DView$1\n*L\n1#1,497:1\n51#2,4:498\n*E\n"})
public final class HuoLive2DViewKt$HuoLive2DView$1$invoke$$inlined$onDispose$1 implements DisposableEffectResult {
   // $FF: synthetic field
   final LifecycleOwner $lifecycleOwner$inlined;
   // $FF: synthetic field
   final LifecycleEventObserver $observer$inlined;
   // $FF: synthetic field
   final MutableState $webViewRef$delegate$inlined;

   public HuoLive2DViewKt$HuoLive2DView$1$invoke$$inlined$onDispose$1(LifecycleOwner var1, LifecycleEventObserver var2, MutableState var3) {
      this.$lifecycleOwner$inlined = var1;
      this.$observer$inlined = var2;
      this.$webViewRef$delegate$inlined = var3;
   }

   public void dispose() {
      int var1 = 0;
      this.$lifecycleOwner$inlined.getLifecycle().removeObserver((LifecycleObserver)this.$observer$inlined);
      WebView var10000 = HuoLive2DViewKt.access$HuoLive2DView$lambda$5(this.$webViewRef$delegate$inlined);
      if (var10000 != null) {
         var10000.destroy();
      }

      HuoLive2DViewKt.access$HuoLive2DView$lambda$6(this.$webViewRef$delegate$inlined, (WebView)null);
   }
}
