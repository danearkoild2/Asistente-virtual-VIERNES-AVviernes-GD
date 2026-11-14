package com.viernes.mobile.avatar;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Paint;
import android.view.ViewGroup;
import android.webkit.ValueCallback;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.compose.foundation.layout.BoxKt;
import androidx.compose.foundation.layout.BoxScope;
import androidx.compose.foundation.layout.BoxScopeInstance;
import androidx.compose.foundation.layout.SizeKt;
import androidx.compose.runtime.Applier;
import androidx.compose.runtime.Composable;
import androidx.compose.runtime.ComposableTarget;
import androidx.compose.runtime.ComposablesKt;
import androidx.compose.runtime.Composer;
import androidx.compose.runtime.ComposerKt;
import androidx.compose.runtime.CompositionLocal;
import androidx.compose.runtime.CompositionLocalMap;
import androidx.compose.runtime.DisposableEffectResult;
import androidx.compose.runtime.DisposableEffectScope;
import androidx.compose.runtime.EffectsKt;
import androidx.compose.runtime.MutableState;
import androidx.compose.runtime.RecomposeScopeImplKt;
import androidx.compose.runtime.ScopeUpdateScope;
import androidx.compose.runtime.SkippableUpdater;
import androidx.compose.runtime.SnapshotMutationPolicy;
import androidx.compose.runtime.SnapshotStateKt;
import androidx.compose.runtime.State;
import androidx.compose.runtime.Updater;
import androidx.compose.ui.Alignment;
import androidx.compose.ui.Modifier;
import androidx.compose.ui.layout.LayoutKt;
import androidx.compose.ui.layout.MeasurePolicy;
import androidx.compose.ui.node.ComposeUiNode;
import androidx.compose.ui.platform.AndroidCompositionLocals_androidKt;
import androidx.compose.ui.viewinterop.AndroidView_androidKt;
import androidx.lifecycle.Lifecycle;
import androidx.lifecycle.LifecycleEventObserver;
import androidx.lifecycle.LifecycleObserver;
import androidx.lifecycle.LifecycleOwner;
import androidx.lifecycle.Lifecycle.Event;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.functions.Function3;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.reflect.KProperty;
import kotlin.text.StringsKt;
import kotlinx.coroutines.CoroutineScope;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 2,
   xi = 48,
   d1 = {"\u0000.\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0010\u0007\n\u0000\n\u0002\u0018\u0002\u001a\u001f\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u0005H\u0007¢\u0006\u0002\u0010\u0006¨\u0006\u0007²\u0006\n\u0010\b\u001a\u00020\tX\u008a\u0084\u0002²\u0006\n\u0010\n\u001a\u00020\u000bX\u008a\u0084\u0002²\u0006\n\u0010\f\u001a\u00020\u000bX\u008a\u0084\u0002²\u0006\n\u0010\r\u001a\u00020\u000eX\u008a\u0084\u0002²\u0006\f\u0010\u000f\u001a\u0004\u0018\u00010\u0010X\u008a\u008e\u0002"},
   d2 = {"HuoLive2DView", "", "controller", "Lcom/viernes/mobile/avatar/HuoAvatarController;", "modifier", "Landroidx/compose/ui/Modifier;", "(Lcom/viernes/mobile/avatar/HuoAvatarController;Landroidx/compose/ui/Modifier;Landroidx/compose/runtime/Composer;II)V", "app_debug", "state", "Lcom/viernes/mobile/avatar/HuoState;", "motion", "", "expression", "mouthOpen", "", "webViewRef", "Landroid/webkit/WebView;"}
)
@SourceDebugExtension({"SMAP\nHuoLive2DView.kt\nKotlin\n*S Kotlin\n*F\n+ 1 HuoLive2DView.kt\ncom/viernes/mobile/avatar/HuoLive2DViewKt\n+ 2 CompositionLocal.kt\nandroidx/compose/runtime/CompositionLocal\n+ 3 Composer.kt\nandroidx/compose/runtime/ComposerKt\n+ 4 Box.kt\nandroidx/compose/foundation/layout/BoxKt\n+ 5 Layout.kt\nandroidx/compose/ui/layout/LayoutKt\n+ 6 Composables.kt\nandroidx/compose/runtime/ComposablesKt\n+ 7 Composer.kt\nandroidx/compose/runtime/Updater\n+ 8 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,111:1\n74#2:112\n74#2:113\n1116#3,6:114\n1116#3,6:120\n1116#3,6:161\n1116#3,6:167\n68#4,6:126\n74#4:160\n78#4:177\n79#5,11:132\n92#5:176\n456#6,8:143\n464#6,3:157\n467#6,3:173\n3737#7,6:151\n81#8:178\n81#8:179\n81#8:180\n81#8:181\n81#8:182\n107#8,2:183\n*S KotlinDebug\n*F\n+ 1 HuoLive2DView.kt\ncom/viernes/mobile/avatar/HuoLive2DViewKt\n*L\n26#1:112\n27#1:113\n34#1:114,6\n58#1:120,6\n70#1:161,6\n105#1:167,6\n67#1:126,6\n67#1:160\n67#1:177\n67#1:132,11\n67#1:176\n67#1:143,8\n67#1:157,3\n67#1:173,3\n67#1:151,6\n29#1:178\n30#1:179\n31#1:180\n32#1:181\n34#1:182\n34#1:183,2\n*E\n"})
public final class HuoLive2DViewKt {
   @SuppressLint({"SetJavaScriptEnabled"})
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void HuoLive2DView(@NotNull final HuoAvatarController controller, @Nullable final Modifier modifier, @Nullable Composer $composer, final int $changed, final int var4) {
      Intrinsics.checkNotNullParameter(controller, "controller");
      $composer = $composer.startRestartGroup(-1491264966);
      ComposerKt.sourceInformation($composer, "C(HuoLive2DView)25@852L7,26@905L7,28@955L16,29@1015L16,30@1083L16,31@1142L16,33@1182L43,36@1317L671,57@2140L253,57@2087L306,66@2399L1838:HuoLive2DView.kt#2urv2e");
      if ((var4 & 2) != 0) {
         modifier = (Modifier)Modifier.Companion;
      }

      if (ComposerKt.isTraceInProgress()) {
         ComposerKt.traceEventStart(-1491264966, $changed, -1, "com.viernes.mobile.avatar.HuoLive2DView (HuoLive2DView.kt:24)");
      }

      CompositionLocal this_$iv = (CompositionLocal)AndroidCompositionLocals_androidKt.getLocalContext();
      int $changed$iv = 0;
      int $i$f$getCurrent = 0;
      ComposerKt.sourceInformationMarkerStart($composer, 2023513938, "CC:CompositionLocal.kt#9igjgp");
      Object var10 = $composer.consume(this_$iv);
      ComposerKt.sourceInformationMarkerEnd($composer);
      Context context = (Context)var10;
      CompositionLocal this_$iv = (CompositionLocal)AndroidCompositionLocals_androidKt.getLocalLifecycleOwner();
      $i$f$getCurrent = 0;
      int $i$f$getCurrent = 0;
      ComposerKt.sourceInformationMarkerStart($composer, 2023513938, "CC:CompositionLocal.kt#9igjgp");
      Object var11 = $composer.consume(this_$iv);
      ComposerKt.sourceInformationMarkerEnd($composer);
      final LifecycleOwner lifecycleOwner = (LifecycleOwner)var11;
      final State state$delegate = SnapshotStateKt.collectAsState(controller.getCurrentState(), (CoroutineContext)null, $composer, 8, 1);
      final State motion$delegate = SnapshotStateKt.collectAsState(controller.getCurrentMotion(), (CoroutineContext)null, $composer, 8, 1);
      final State expression$delegate = SnapshotStateKt.collectAsState(controller.getCurrentExpression(), (CoroutineContext)null, $composer, 8, 1);
      final State mouthOpen$delegate = SnapshotStateKt.collectAsState(controller.getMouthOpen(), (CoroutineContext)null, $composer, 8, 1);
      $composer.startReplaceableGroup(1227188040);
      ComposerKt.sourceInformation($composer, "CC(remember):HuoLive2DView.kt#9igjgp");
      boolean invalid$iv = (boolean)0;
      int $i$f$cache = 0;
      Object it$iv = $composer.rememberedValue();
      int var18 = 0;
      Object var10000;
      if (it$iv == Composer.Companion.getEmpty()) {
         int var19 = 0;
         Object value$iv = SnapshotStateKt.mutableStateOf$default((Object)null, (SnapshotMutationPolicy)null, 2, (Object)null);
         $composer.updateRememberedValue(value$iv);
         var10000 = value$iv;
      } else {
         var10000 = it$iv;
      }

      final MutableState var13 = (MutableState)var10000;
      $composer.endReplaceableGroup();
      final MutableState webViewRef$delegate = var13;
      EffectsKt.DisposableEffect(lifecycleOwner, new Function1<DisposableEffectScope, DisposableEffectResult>() {
         @NotNull
         public final DisposableEffectResult invoke(@NotNull DisposableEffectScope $this$DisposableEffect) {
            Intrinsics.checkNotNullParameter($this$DisposableEffect, "$this$DisposableEffect");
            LifecycleEventObserver observer = <undefinedtype>::invoke$lambda$0;
            lifecycleOwner.getLifecycle().addObserver((LifecycleObserver)observer);
            LifecycleOwner var4 = lifecycleOwner;
            MutableState var5 = var13;
            int $i$f$onDispose = 0;
            return new HuoLive2DViewKt$HuoLive2DView$1$invoke$$inlined$onDispose$1(var4, observer, var5);
         }

         private static final void invoke$lambda$0(MutableState $webViewRef$delegate, LifecycleOwner var1, Lifecycle.Event event) {
            Intrinsics.checkNotNullParameter($webViewRef$delegate, "$webViewRef$delegate");
            Intrinsics.checkNotNullParameter(var1, "<anonymous parameter 0>");
            Intrinsics.checkNotNullParameter(event, "event");
            switch (null.WhenMappings.$EnumSwitchMapping$0[event.ordinal()]) {
               case 1:
                  WebView var4 = HuoLive2DViewKt.HuoLive2DView$lambda$5($webViewRef$delegate);
                  if (var4 != null) {
                     var4.onResume();
                  }
                  break;
               case 2:
                  WebView var3 = HuoLive2DViewKt.HuoLive2DView$lambda$5($webViewRef$delegate);
                  if (var3 != null) {
                     var3.onPause();
                  }
                  break;
               case 3:
                  WebView var10000 = HuoLive2DViewKt.HuoLive2DView$lambda$5($webViewRef$delegate);
                  if (var10000 != null) {
                     var10000.destroy();
                  }

                  HuoLive2DViewKt.HuoLive2DView$lambda$6($webViewRef$delegate, (WebView)null);
            }

         }

         // $FF: synthetic class
         @Metadata(
            mv = {1, 9, 0},
            k = 3,
            xi = 48
         )
         public class WhenMappings {
            // $FF: synthetic field
            public static final int[] $EnumSwitchMapping$0;

            static {
               int[] var0 = new int[Event.values().length];

               try {
                  var0[Event.ON_RESUME.ordinal()] = 1;
               } catch (NoSuchFieldError var4) {
               }

               try {
                  var0[Event.ON_PAUSE.ordinal()] = 2;
               } catch (NoSuchFieldError var3) {
               }

               try {
                  var0[Event.ON_DESTROY.ordinal()] = 3;
               } catch (NoSuchFieldError var2) {
               }

               $EnumSwitchMapping$0 = var0;
            }
         }
      }, $composer, 8);
      Function2 var61 = new Object[]{HuoLive2DView$lambda$0(state$delegate), HuoLive2DView$lambda$1(motion$delegate), HuoLive2DView$lambda$2(expression$delegate), HuoLive2DView$lambda$3(mouthOpen$delegate)};
      BoxScope var82 = var61;
      $composer.startReplaceableGroup(1227218906);
      ComposerKt.sourceInformation($composer, "CC(remember):HuoLive2DView.kt#9igjgp");
      invalid$iv = $composer.changed(state$delegate) | $composer.changed(motion$delegate) | $composer.changed(expression$delegate) | $composer.changed(mouthOpen$delegate);
      $i$f$cache = 0;
      it$iv = $composer.rememberedValue();
      var18 = 0;
      Object var87;
      if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
         var87 = it$iv;
      } else {
         int var73 = 0;
         Function2 var10001 = new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               IntrinsicsKt.getCOROUTINE_SUSPENDED();
               switch (this.label) {
                  case 0:
                     ResultKt.throwOnFailure($result);
                     String var10000 = HuoLive2DViewKt.HuoLive2DView$lambda$0(state$delegate).name();
                     String jsCall = StringsKt.trimIndent("\n            if (window.setHuoState) {\n                window.setHuoState('" + var10000 + "', '" + HuoLive2DViewKt.HuoLive2DView$lambda$1(motion$delegate) + "', '" + HuoLive2DViewKt.HuoLive2DView$lambda$2(expression$delegate) + "', " + HuoLive2DViewKt.HuoLive2DView$lambda$3(mouthOpen$delegate) + ");\n            }\n        ");
                     WebView var3 = HuoLive2DViewKt.HuoLive2DView$lambda$5(webViewRef$delegate);
                     if (var3 != null) {
                        var3.evaluateJavascript(jsCall, (ValueCallback)null);
                     }

                     return Unit.INSTANCE;
                  default:
                     throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
               }
            }

            @NotNull
            public final Continuation<Unit> create(@Nullable Object value, @NotNull Continuation<?> $completion) {
               return (Continuation)(new <anonymous constructor>($completion));
            }

            @Nullable
            public final Object invoke(@NotNull CoroutineScope p1, @Nullable Continuation<? super Unit> p2) {
               return ((<undefinedtype>)this.create(p1, p2)).invokeSuspend(Unit.INSTANCE);
            }
         };
         var82 = var61;
         Object value$iv = var10001;
         $composer.updateRememberedValue(value$iv);
         var87 = value$iv;
      }

      var61 = (Function2)var87;
      $composer.endReplaceableGroup();
      EffectsKt.LaunchedEffect(var82, var61, $composer, 72);
      invalid$iv = (boolean)(14 & $changed >> 3);
      $i$f$cache = 0;
      $composer.startReplaceableGroup(733328855);
      ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
      Alignment contentAlignment$iv = Alignment.Companion.getTopStart();
      boolean propagateMinConstraints$iv = false;
      MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(contentAlignment$iv, propagateMinConstraints$iv, $composer, 14 & invalid$iv >> 3 | 112 & invalid$iv >> 3);
      var18 = 112 & invalid$iv << 3;
      int $i$f$Layout = 0;
      $composer.startReplaceableGroup(-1323940314);
      ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
      int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
      CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
      Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
      Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier);
      int $changed$iv$iv$iv = 6 | 7168 & var18 << 9;
      int $i$f$ReusableComposeNode = 0;
      if (!($composer.getApplier() instanceof Applier)) {
         ComposablesKt.invalidApplier();
      }

      $composer.startReusableNode();
      if ($composer.getInserting()) {
         $composer.createNode(factory$iv$iv$iv);
      } else {
         $composer.useNode();
      }

      Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
      int var27 = 0;
      Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
      Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
      Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
      int var29 = 0;
      int var31 = 0;
      if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
         $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
         $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
      }

      skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
      $composer.startReplaceableGroup(2058660585);
      int var32 = 14 & $changed$iv$iv$iv >> 9;
      int var34 = 0;
      ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
      int var35 = 6 | 112 & invalid$iv >> 6;
      var82 = (BoxScope)BoxScopeInstance.INSTANCE;
      int var38 = 0;
      ComposerKt.sourceInformationMarkerStart($composer, -478086398, "C69@2516L1625,104@4164L57,67@2434L1797:HuoLive2DView.kt#2urv2e");
      Modifier var39 = SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
      $composer.startReplaceableGroup(-1123798347);
      ComposerKt.sourceInformation($composer, "CC(remember):HuoLive2DView.kt#9igjgp");
      boolean invalid$iv = $composer.changed(state$delegate) | $composer.changed(motion$delegate) | $composer.changed(expression$delegate) | $composer.changed(mouthOpen$delegate);
      int $i$f$cache = 0;
      Object it$iv = $composer.rememberedValue();
      int var44 = 0;
      Object var84;
      if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
         var84 = it$iv;
      } else {
         int var45 = 0;
         Object value$iv = new Function1<Context, WebView>() {
            @NotNull
            public final WebView invoke(@NotNull Context ctx) {
               Intrinsics.checkNotNullParameter(ctx, "ctx");
               WebView $this$invoke_u24lambda_u241 = new WebView(ctx);
               final State var3 = state$delegate;
               final State var4 = motion$delegate;
               final State var5 = expression$delegate;
               final State var6 = mouthOpen$delegate;
               MutableState var7 = webViewRef$delegate;
               int var9 = 0;
               $this$invoke_u24lambda_u241.setLayoutParams(new ViewGroup.LayoutParams(-1, -1));
               $this$invoke_u24lambda_u241.setBackgroundColor(0);
               $this$invoke_u24lambda_u241.setLayerType(2, (Paint)null);
               WebSettings $this$invoke_u24lambda_u241_u24lambda_u240 = $this$invoke_u24lambda_u241.getSettings();
               int var12 = 0;
               $this$invoke_u24lambda_u241_u24lambda_u240.setJavaScriptEnabled(true);
               $this$invoke_u24lambda_u241_u24lambda_u240.setDomStorageEnabled(true);
               $this$invoke_u24lambda_u241_u24lambda_u240.setAllowFileAccess(true);
               $this$invoke_u24lambda_u241_u24lambda_u240.setAllowContentAccess(true);
               $this$invoke_u24lambda_u241_u24lambda_u240.setLoadWithOverviewMode(true);
               $this$invoke_u24lambda_u241_u24lambda_u240.setUseWideViewPort(true);
               $this$invoke_u24lambda_u241_u24lambda_u240.setCacheMode(2);
               $this$invoke_u24lambda_u241.setWebViewClient(new WebViewClient() {
                  public void onPageFinished(@Nullable WebView view, @Nullable String url) {
                     super.onPageFinished(view, url);
                     if (view != null) {
                        String var10001 = HuoLive2DViewKt.HuoLive2DView$lambda$0(var3).name();
                        view.evaluateJavascript("if (window.setHuoState) window.setHuoState('" + var10001 + "', '" + HuoLive2DViewKt.HuoLive2DView$lambda$1(var4) + "', '" + HuoLive2DViewKt.HuoLive2DView$lambda$2(var5) + "', " + HuoLive2DViewKt.HuoLive2DView$lambda$3(var6) + ");", (ValueCallback)null);
                     }

                  }
               });
               $this$invoke_u24lambda_u241.loadUrl("file:///android_asset/live2d/huohuo_viewer.html");
               HuoLive2DViewKt.HuoLive2DView$lambda$6(var7, $this$invoke_u24lambda_u241);
               return $this$invoke_u24lambda_u241;
            }
         };
         $composer.updateRememberedValue(value$iv);
         var84 = value$iv;
      }

      Function1 var47 = (Function1)var84;
      $composer.endReplaceableGroup();
      Function1 var85 = var47;
      Modifier var88 = var39;
      $composer.startReplaceableGroup(-1123747179);
      ComposerKt.sourceInformation($composer, "CC(remember):HuoLive2DView.kt#9igjgp");
      invalid$iv = false;
      $i$f$cache = 0;
      it$iv = $composer.rememberedValue();
      var44 = 0;
      Object var10002;
      if (it$iv == Composer.Companion.getEmpty()) {
         int var80 = 0;
         Function1 value$iv = new Function1<WebView, Unit>() {
            public final void invoke(@NotNull WebView view) {
               Intrinsics.checkNotNullParameter(view, "view");
               HuoLive2DViewKt.HuoLive2DView$lambda$6(webViewRef$delegate, view);
            }
         };
         var85 = var47;
         var88 = var39;
         $composer.updateRememberedValue(value$iv);
         var10002 = value$iv;
      } else {
         var10002 = it$iv;
      }

      var47 = (Function1)var10002;
      $composer.endReplaceableGroup();
      AndroidView_androidKt.AndroidView(var85, var88, var47, $composer, 432, 0);
      ComposerKt.sourceInformationMarkerEnd($composer);
      ComposerKt.sourceInformationMarkerEnd($composer);
      $composer.endReplaceableGroup();
      $composer.endNode();
      $composer.endReplaceableGroup();
      $composer.endReplaceableGroup();
      if (ComposerKt.isTraceInProgress()) {
         ComposerKt.traceEventEnd();
      }

      ScopeUpdateScope var86 = $composer.endRestartGroup();
      if (var86 != null) {
         var86.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               HuoLive2DViewKt.HuoLive2DView(controller, modifier, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1), var4);
            }
         });
      }

   }

   private static final HuoState HuoLive2DView$lambda$0(State<? extends HuoState> $state$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (HuoState)$state$delegate.getValue();
   }

   private static final String HuoLive2DView$lambda$1(State<String> $motion$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (String)$motion$delegate.getValue();
   }

   private static final String HuoLive2DView$lambda$2(State<String> $expression$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (String)$expression$delegate.getValue();
   }

   private static final float HuoLive2DView$lambda$3(State<Float> $mouthOpen$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return ((Number)$mouthOpen$delegate.getValue()).floatValue();
   }

   private static final WebView HuoLive2DView$lambda$5(MutableState<WebView> $webViewRef$delegate) {
      State $this$getValue$iv = (State)$webViewRef$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (WebView)$this$getValue$iv.getValue();
   }

   private static final void HuoLive2DView$lambda$6(MutableState<WebView> $webViewRef$delegate, WebView value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $webViewRef$delegate.setValue(value);
   }
}
