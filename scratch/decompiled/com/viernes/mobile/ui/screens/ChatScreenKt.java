package com.viernes.mobile.ui.screens;

import android.content.Context;
import androidx.activity.compose.ActivityResultRegistryKt;
import androidx.activity.compose.ManagedActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContract;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.compose.foundation.BackgroundKt;
import androidx.compose.foundation.gestures.FlingBehavior;
import androidx.compose.foundation.interaction.MutableInteractionSource;
import androidx.compose.foundation.layout.Arrangement;
import androidx.compose.foundation.layout.BoxKt;
import androidx.compose.foundation.layout.ColumnKt;
import androidx.compose.foundation.layout.ColumnScope;
import androidx.compose.foundation.layout.ColumnScopeInstance;
import androidx.compose.foundation.layout.PaddingKt;
import androidx.compose.foundation.layout.PaddingValues;
import androidx.compose.foundation.layout.RowKt;
import androidx.compose.foundation.layout.RowScope;
import androidx.compose.foundation.layout.RowScopeInstance;
import androidx.compose.foundation.layout.SizeKt;
import androidx.compose.foundation.layout.SpacerKt;
import androidx.compose.foundation.layout.WindowInsets;
import androidx.compose.foundation.lazy.LazyDslKt;
import androidx.compose.foundation.lazy.LazyListScope;
import androidx.compose.foundation.lazy.LazyListState;
import androidx.compose.foundation.lazy.LazyListStateKt;
import androidx.compose.foundation.shape.RoundedCornerShape;
import androidx.compose.foundation.shape.RoundedCornerShapeKt;
import androidx.compose.foundation.text.KeyboardActions;
import androidx.compose.foundation.text.KeyboardOptions;
import androidx.compose.foundation.text.selection.TextSelectionColors;
import androidx.compose.material.icons.Icons;
import androidx.compose.material.icons.filled.MicKt;
import androidx.compose.material.icons.filled.MicOffKt;
import androidx.compose.material.icons.filled.SendKt;
import androidx.compose.material3.AppBarKt;
import androidx.compose.material3.IconButtonColors;
import androidx.compose.material3.IconButtonKt;
import androidx.compose.material3.IconKt;
import androidx.compose.material3.OutlinedTextFieldDefaults;
import androidx.compose.material3.OutlinedTextFieldKt;
import androidx.compose.material3.ScaffoldKt;
import androidx.compose.material3.TextFieldColors;
import androidx.compose.material3.TextKt;
import androidx.compose.material3.TopAppBarDefaults;
import androidx.compose.material3.TopAppBarScrollBehavior;
import androidx.compose.runtime.Applier;
import androidx.compose.runtime.Composable;
import androidx.compose.runtime.ComposableTarget;
import androidx.compose.runtime.ComposablesKt;
import androidx.compose.runtime.Composer;
import androidx.compose.runtime.ComposerKt;
import androidx.compose.runtime.CompositionLocal;
import androidx.compose.runtime.CompositionLocalMap;
import androidx.compose.runtime.CompositionScopedCoroutineScopeCanceller;
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
import androidx.compose.runtime.internal.ComposableLambdaKt;
import androidx.compose.ui.Alignment;
import androidx.compose.ui.Modifier;
import androidx.compose.ui.draw.ClipKt;
import androidx.compose.ui.graphics.Shape;
import androidx.compose.ui.layout.LayoutKt;
import androidx.compose.ui.layout.MeasurePolicy;
import androidx.compose.ui.node.ComposeUiNode;
import androidx.compose.ui.platform.AndroidCompositionLocals_androidKt;
import androidx.compose.ui.text.TextStyle;
import androidx.compose.ui.text.font.FontFamily;
import androidx.compose.ui.text.font.FontStyle;
import androidx.compose.ui.text.font.FontWeight;
import androidx.compose.ui.text.input.VisualTransformation;
import androidx.compose.ui.text.style.TextAlign;
import androidx.compose.ui.text.style.TextDecoration;
import androidx.compose.ui.unit.Dp;
import androidx.core.content.ContextCompat;
import com.viernes.mobile.assistant.AssistantResponse;
import com.viernes.mobile.assistant.ViernesAiAssistant;
import com.viernes.mobile.assistant.VoiceManager;
import com.viernes.mobile.avatar.HuoAvatarController;
import com.viernes.mobile.avatar.HuoState;
import com.viernes.mobile.ui.theme.ColorKt;
import java.util.Collection;
import java.util.List;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.collections.CollectionsKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.coroutines.EmptyCoroutineContext;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.functions.Function3;
import kotlin.jvm.functions.Function4;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.reflect.KProperty;
import kotlin.text.StringsKt;
import kotlinx.coroutines.BuildersKt;
import kotlinx.coroutines.CoroutineScope;
import kotlinx.coroutines.CoroutineStart;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 2,
   xi = 48,
   d1 = {"\u0000>\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\u0007\u001a3\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0006\u001a\u00020\u00072\f\u0010\b\u001a\b\u0012\u0004\u0012\u00020\u00010\tH\u0007¢\u0006\u0002\u0010\n¨\u0006\u000b²\u0006\n\u0010\f\u001a\u00020\rX\u008a\u008e\u0002²\u0006\u0010\u0010\u000e\u001a\b\u0012\u0004\u0012\u00020\u00100\u000fX\u008a\u008e\u0002²\u0006\n\u0010\u0011\u001a\u00020\u0012X\u008a\u0084\u0002²\u0006\n\u0010\u0013\u001a\u00020\u0012X\u008a\u0084\u0002²\u0006\n\u0010\u0014\u001a\u00020\u0015X\u008a\u0084\u0002"},
   d2 = {"ChatScreen", "", "assistant", "Lcom/viernes/mobile/assistant/ViernesAiAssistant;", "voiceManager", "Lcom/viernes/mobile/assistant/VoiceManager;", "huoController", "Lcom/viernes/mobile/avatar/HuoAvatarController;", "onNavigateBack", "Lkotlin/Function0;", "(Lcom/viernes/mobile/assistant/ViernesAiAssistant;Lcom/viernes/mobile/assistant/VoiceManager;Lcom/viernes/mobile/avatar/HuoAvatarController;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "app_debug", "inputText", "", "messages", "", "Lcom/viernes/mobile/ui/screens/ChatMessage;", "isListening", "", "isSpeaking", "speechAmp", ""}
)
@SourceDebugExtension({"SMAP\nChatScreen.kt\nKotlin\n*S Kotlin\n*F\n+ 1 ChatScreen.kt\ncom/viernes/mobile/ui/screens/ChatScreenKt\n+ 2 CompositionLocal.kt\nandroidx/compose/runtime/CompositionLocal\n+ 3 Effects.kt\nandroidx/compose/runtime/EffectsKt\n+ 4 Composables.kt\nandroidx/compose/runtime/ComposablesKt\n+ 5 Composer.kt\nandroidx/compose/runtime/ComposerKt\n+ 6 Effects.kt\nandroidx/compose/runtime/EffectsKt$rememberCoroutineScope$1\n+ 7 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,271:1\n74#2:272\n487#3,4:273\n491#3,2:281\n495#3:287\n25#4:277\n1116#5,3:278\n1119#5,3:284\n1116#5,6:288\n1116#5,6:294\n487#6:283\n81#7:300\n107#7,2:301\n81#7:303\n107#7,2:304\n81#7:306\n81#7:307\n81#7:308\n*S KotlinDebug\n*F\n+ 1 ChatScreen.kt\ncom/viernes/mobile/ui/screens/ChatScreenKt\n*L\n48#1:272\n49#1:273,4\n49#1:281,2\n49#1:287\n49#1:277\n49#1:278,3\n49#1:284,3\n52#1:288,6\n53#1:294,6\n49#1:283\n52#1:300\n52#1:301,2\n53#1:303\n53#1:304,2\n64#1:306\n65#1:307\n66#1:308\n*E\n"})
public final class ChatScreenKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void ChatScreen(@NotNull final ViernesAiAssistant assistant, @NotNull final VoiceManager voiceManager, @NotNull final HuoAvatarController huoController, @NotNull final Function0<Unit> onNavigateBack, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(assistant, "assistant");
      Intrinsics.checkNotNullParameter(voiceManager, "voiceManager");
      Intrinsics.checkNotNullParameter(huoController, "huoController");
      Intrinsics.checkNotNullParameter(onNavigateBack, "onNavigateBack");
      $composer = $composer.startRestartGroup(-1148618776);
      ComposerKt.sourceInformation($composer, "C(ChatScreen)P(!1,3)47@1822L7,48@1855L24,49@1900L23,51@1946L31,52@1998L284,63@2332L16,64@2395L16,65@2462L16,67@2484L85,71@2575L293,81@2910L201,89@3117L721,107@3844L7315:ChatScreen.kt#k2q6ai");
      if (ComposerKt.isTraceInProgress()) {
         ComposerKt.traceEventStart(-1148618776, $changed, -1, "com.viernes.mobile.ui.screens.ChatScreen (ChatScreen.kt:46)");
      }

      CompositionLocal this_$iv = (CompositionLocal)AndroidCompositionLocals_androidKt.getLocalContext();
      int $changed$iv = 0;
      int $i$f$getCurrent = 0;
      ComposerKt.sourceInformationMarkerStart($composer, 2023513938, "CC:CompositionLocal.kt#9igjgp");
      Object var10 = $composer.consume(this_$iv);
      ComposerKt.sourceInformationMarkerEnd($composer);
      final Context context = (Context)var10;
      $i$f$getCurrent = 0;
      int $i$f$rememberCoroutineScope = 0;
      $composer.startReplaceableGroup(773894976);
      ComposerKt.sourceInformation($composer, "CC(rememberCoroutineScope)489@20472L144:Effects.kt#9igjgp");
      boolean var12 = false;
      int $i$f$remember = 0;
      $composer.startReplaceableGroup(-492369756);
      ComposerKt.sourceInformation($composer, "CC(remember):Composables.kt#9igjgp");
      boolean invalid$iv$iv$iv = (boolean)0;
      int $i$f$cache = 0;
      Object it$iv$iv$iv = $composer.rememberedValue();
      int var18 = 0;
      Object var10000;
      if (it$iv$iv$iv == Composer.Companion.getEmpty()) {
         int var19 = 0;
         int var20 = 0;
         CoroutineScope var23 = EffectsKt.createCompositionCoroutineScope((CoroutineContext)EmptyCoroutineContext.INSTANCE, $composer);
         Object value$iv$iv$iv = new CompositionScopedCoroutineScopeCanceller(var23);
         $composer.updateRememberedValue(value$iv$iv$iv);
         var10000 = value$iv$iv$iv;
      } else {
         var10000 = it$iv$iv$iv;
      }

      Object var21 = var10000;
      $composer.endReplaceableGroup();
      CompositionScopedCoroutineScopeCanceller wrapper$iv = (CompositionScopedCoroutineScopeCanceller)var21;
      CoroutineScope invalid$iv = wrapper$iv.getCoroutineScope();
      $composer.endReplaceableGroup();
      final CoroutineScope coroutineScope = invalid$iv;
      final LazyListState listState = LazyListStateKt.rememberLazyListState(0, 0, $composer, 0, 3);
      $composer.startReplaceableGroup(-105015945);
      ComposerKt.sourceInformation($composer, "CC(remember):ChatScreen.kt#9igjgp");
      boolean $this$cache$iv = false;
      $i$f$remember = 0;
      Object it$iv = $composer.rememberedValue();
      invalid$iv$iv$iv = (boolean)0;
      if (it$iv == Composer.Companion.getEmpty()) {
         $i$f$cache = 0;
         Object value$iv = SnapshotStateKt.mutableStateOf$default("", (SnapshotMutationPolicy)null, 2, (Object)null);
         $composer.updateRememberedValue(value$iv);
         var10000 = value$iv;
      } else {
         var10000 = it$iv;
      }

      final MutableState messages$delegate = (MutableState)var10000;
      $composer.endReplaceableGroup();
      final MutableState inputText$delegate = messages$delegate;
      $composer.startReplaceableGroup(-105014028);
      ComposerKt.sourceInformation($composer, "CC(remember):ChatScreen.kt#9igjgp");
      $i$f$remember = 0;
      int $i$f$cache = 0;
      Object it$iv = $composer.rememberedValue();
      $i$f$cache = 0;
      if (it$iv == Composer.Companion.getEmpty()) {
         int var46 = 0;
         Object value$iv = SnapshotStateKt.mutableStateOf$default(CollectionsKt.listOf(new ChatMessage((String)null, "viernes", "Hola, soy VIERNES. ¿En qué puedo asistirte hoy con la gestión médica de tu familia?", (String)null, 9, (DefaultConstructorMarker)null)), (SnapshotMutationPolicy)null, 2, (Object)null);
         $composer.updateRememberedValue(value$iv);
         var10000 = value$iv;
      } else {
         var10000 = it$iv;
      }

      MutableState composer$iv = (MutableState)var10000;
      $composer.endReplaceableGroup();
      messages$delegate = composer$iv;
      final State isListening$delegate = SnapshotStateKt.collectAsState(voiceManager.isListening(), (CoroutineContext)null, $composer, 8, 1);
      final State isSpeaking$delegate = SnapshotStateKt.collectAsState(voiceManager.isSpeaking(), (CoroutineContext)null, $composer, 8, 1);
      final State speechAmp$delegate = SnapshotStateKt.collectAsState(voiceManager.getSpeechAmplitude(), (CoroutineContext)null, $composer, 8, 1);
      EffectsKt.LaunchedEffect(ChatScreen$lambda$8(speechAmp$delegate), new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
         int label;

         @Nullable
         public final Object invokeSuspend(@NotNull Object $result) {
            IntrinsicsKt.getCOROUTINE_SUSPENDED();
            switch (this.label) {
               case 0:
                  ResultKt.throwOnFailure($result);
                  huoController.setSpeechAmplitude(ChatScreenKt.ChatScreen$lambda$8(speechAmp$delegate));
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
      }, $composer, 64);
      EffectsKt.LaunchedEffect(ChatScreen$lambda$6(isListening$delegate), ChatScreen$lambda$7(isSpeaking$delegate), new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
         int label;

         @Nullable
         public final Object invokeSuspend(@NotNull Object $result) {
            IntrinsicsKt.getCOROUTINE_SUSPENDED();
            switch (this.label) {
               case 0:
                  ResultKt.throwOnFailure($result);
                  if (ChatScreenKt.ChatScreen$lambda$7(isSpeaking$delegate)) {
                     huoController.setState(HuoState.SPEAKING);
                  } else if (ChatScreenKt.ChatScreen$lambda$6(isListening$delegate)) {
                     huoController.setState(HuoState.LISTENING);
                  } else {
                     huoController.setState(HuoState.IDLE);
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
      }, $composer, 512);
      final ManagedActivityResultLauncher recordAudioPermissionLauncher = ActivityResultRegistryKt.rememberLauncherForActivityResult((ActivityResultContract)(new ActivityResultContracts.RequestPermission()), new Function1<Boolean, Unit>() {
         public final void invoke(boolean isGranted) {
            if (isGranted) {
               voiceManager.startListening();
            }

         }
      }, $composer, 8);
      EffectsKt.DisposableEffect(Unit.INSTANCE, new Function1<DisposableEffectScope, DisposableEffectResult>() {
         @NotNull
         public final DisposableEffectResult invoke(@NotNull DisposableEffectScope $this$DisposableEffect) {
            Intrinsics.checkNotNullParameter($this$DisposableEffect, "$this$DisposableEffect");
            voiceManager.setOnSpeechRecognized(new Function1<String, Unit>() {
               public final void invoke(@NotNull final String recognizedText) {
                  Intrinsics.checkNotNullParameter(recognizedText, "recognizedText");
                  ChatScreenKt.ChatScreen$lambda$2(inputText$delegate, recognizedText);
                  BuildersKt.launch$default(coroutineScope, (CoroutineContext)null, (CoroutineStart)null, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
                     int label;

                     @Nullable
                     public final Object invokeSuspend(@NotNull Object $result) {
                        Object var3 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                        Object var10000;
                        switch (this.label) {
                           case 0:
                              ResultKt.throwOnFailure($result);
                              ChatScreenKt.ChatScreen$lambda$5(messages$delegate, CollectionsKt.plus((Collection)ChatScreenKt.ChatScreen$lambda$4(messages$delegate), new ChatMessage((String)null, "user", recognizedText, (String)null, 9, (DefaultConstructorMarker)null)));
                              huoController.setState(HuoState.THINKING);
                              ViernesAiAssistant var4 = assistant;
                              String var10001 = recognizedText;
                              Continuation var10003 = (Continuation)this;
                              this.label = 1;
                              var10000 = ViernesAiAssistant.processUserMessage$default(var4, var10001, (Long)null, var10003, 2, (Object)null);
                              if (var10000 == var3) {
                                 return var3;
                              }
                              break;
                           case 1:
                              ResultKt.throwOnFailure($result);
                              var10000 = $result;
                              break;
                           case 2:
                              ResultKt.throwOnFailure($result);
                              return Unit.INSTANCE;
                           default:
                              throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                        }

                        AssistantResponse resp = (AssistantResponse)var10000;
                        ChatScreenKt.ChatScreen$lambda$5(messages$delegate, CollectionsKt.plus((Collection)ChatScreenKt.ChatScreen$lambda$4(messages$delegate), new ChatMessage((String)null, "viernes", resp.getText(), (String)null, 9, (DefaultConstructorMarker)null)));
                        VoiceManager.speak$default(voiceManager, resp.getText(), (String)null, 2, (Object)null);
                        LazyListState var5 = listState;
                        int var6 = ChatScreenKt.ChatScreen$lambda$4(messages$delegate).size() - 1;
                        Continuation var7 = (Continuation)this;
                        this.label = 2;
                        if (LazyListState.animateScrollToItem$default(var5, var6, 0, var7, 2, (Object)null) == var3) {
                           return var3;
                        } else {
                           return Unit.INSTANCE;
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
                  }, 3, (Object)null);
               }
            });
            VoiceManager var3 = voiceManager;
            int $i$f$onDispose = 0;
            return new ChatScreenKt$ChatScreen$3$invoke$$inlined$onDispose$1(var3);
         }
      }, $composer, 6);
      ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 1277787556, true, new Function2<Composer, Integer, Unit>() {
         @Composable
         @ComposableTarget(
            applier = "androidx.compose.ui.UiComposable"
         )
         public final void invoke(@Nullable Composer $composer, int $changed) {
            ComposerKt.sourceInformation($composer, "C127@4825L48,109@3885L1002:ChatScreen.kt#k2q6ai");
            if (($changed & 11) == 2 && $composer.getSkipping()) {
               $composer.skipToGroupEnd();
            } else {
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventStart(1277787556, $changed, -1, "com.viernes.mobile.ui.screens.ChatScreen.<anonymous> (ChatScreen.kt:109)");
               }

               AppBarKt.TopAppBar((Function2)ComposableLambdaKt.composableLambda($composer, 1114572136, true, new Function2<Composer, Integer, Unit>() {
                  @Composable
                  @ComposableTarget(
                     applier = "androidx.compose.ui.UiComposable"
                  )
                  public final void invoke(@Nullable Composer $composer, int $changed) {
                     ComposerKt.sourceInformation($composer, "C111@3942L578:ChatScreen.kt#k2q6ai");
                     if (($changed & 11) == 2 && $composer.getSkipping()) {
                        $composer.skipToGroupEnd();
                     } else {
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventStart(1114572136, $changed, -1, "com.viernes.mobile.ui.screens.ChatScreen.<anonymous>.<anonymous> (ChatScreen.kt:111)");
                        }

                        Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                        State var6 = isListening$delegate;
                        State var7 = isSpeaking$delegate;
                        int $changed$iv = 384;
                        int $i$f$Row = 0;
                        $composer.startReplaceableGroup(693286680);
                        ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                        Modifier modifier$iv = (Modifier)Modifier.Companion;
                        Arrangement.Horizontal horizontalArrangement$iv = Arrangement.INSTANCE.getStart();
                        MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, verticalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                        int $changed$iv$iv = 112 & $changed$iv << 3;
                        int $i$f$Layout = 0;
                        $composer.startReplaceableGroup(-1323940314);
                        ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                        int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                        CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                        Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                        Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$iv);
                        int $changed$iv$iv$iv = 6 | 7168 & $changed$iv$iv << 9;
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
                        int var20 = 0;
                        Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                        Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                        Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                        int var22 = 0;
                        int var24 = 0;
                        if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                           $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                           $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                        }

                        skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                        $composer.startReplaceableGroup(2058660585);
                        int var25 = 14 & $changed$iv$iv$iv >> 9;
                        int var27 = 0;
                        ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                        int var28 = 6 | 112 & $changed$iv >> 6;
                        RowScope var10000 = (RowScope)RowScopeInstance.INSTANCE;
                        int var31 = 0;
                        ComposerKt.sourceInformationMarkerStart($composer, -625263248, "C112@4020L306,118@4351L39,119@4415L83:ChatScreen.kt#k2q6ai");
                        Modifier var39 = (Modifier)Modifier.Companion;
                        int $this$dp$iv = 10;
                        int $i$f$getDp = 0;
                        BoxKt.Box(BackgroundKt.background-bw27NRU$default(ClipKt.clip(SizeKt.size-3ABfNKs(var39, Dp.constructor-impl((float)$this$dp$iv)), (Shape)RoundedCornerShapeKt.getCircleShape()), ChatScreenKt.ChatScreen$lambda$6(var6) ? ColorKt.getStatusDelayed() : (ChatScreenKt.ChatScreen$lambda$7(var7) ? ColorKt.getViernesAccent() : ColorKt.getStatusConfirmed()), (Shape)null, 2, (Object)null), $composer, 0);
                        var39 = (Modifier)Modifier.Companion;
                        $this$dp$iv = 8;
                        $i$f$getDp = 0;
                        SpacerKt.Spacer(SizeKt.width-3ABfNKs(var39, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                        FontWeight var37 = FontWeight.Companion.getBold();
                        long var34 = ColorKt.getTextPrimary();
                        TextKt.Text--4IGK_g("Conversación con VIERNES", (Modifier)null, var34, 0L, (FontStyle)null, var37, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 196998, 0, 131034);
                        ComposerKt.sourceInformationMarkerEnd($composer);
                        ComposerKt.sourceInformationMarkerEnd($composer);
                        $composer.endReplaceableGroup();
                        $composer.endNode();
                        $composer.endReplaceableGroup();
                        $composer.endReplaceableGroup();
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventEnd();
                        }
                     }

                  }
               }), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -966011542, true, new Function2<Composer, Integer, Unit>() {
                  @Composable
                  @ComposableTarget(
                     applier = "androidx.compose.ui.UiComposable"
                  )
                  public final void invoke(@Nullable Composer $composer, int $changed) {
                     ComposerKt.sourceInformation($composer, "C123@4595L167:ChatScreen.kt#k2q6ai");
                     if (($changed & 11) == 2 && $composer.getSkipping()) {
                        $composer.skipToGroupEnd();
                     } else {
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventStart(-966011542, $changed, -1, "com.viernes.mobile.ui.screens.ChatScreen.<anonymous>.<anonymous> (ChatScreen.kt:123)");
                        }

                        IconButtonKt.IconButton(onNavigateBack, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$ChatScreenKt.INSTANCE.getLambda-1$app_debug(), $composer, 196608, 30);
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventEnd();
                        }
                     }

                  }
               }), (Function3)null, (WindowInsets)null, TopAppBarDefaults.INSTANCE.topAppBarColors-zjMxDiM(ColorKt.getBackgroundDark(), 0L, 0L, 0L, 0L, $composer, 6 | TopAppBarDefaults.$stable << 15, 30), (TopAppBarScrollBehavior)null, $composer, 390, 90);
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventEnd();
               }
            }

         }
      }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, -1138678343, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
         @Composable
         @ComposableTarget(
            applier = "androidx.compose.ui.UiComposable"
         )
         public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
            Intrinsics.checkNotNullParameter(padding, "padding");
            ComposerKt.sourceInformation($composer, "C132@4966L6187:ChatScreen.kt#k2q6ai");
            int $dirty = $changed;
            if (($changed & 14) == 0) {
               $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
            }

            if (($dirty & 91) == 18 && $composer.getSkipping()) {
               $composer.skipToGroupEnd();
            } else {
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventStart(-1138678343, $dirty, -1, "com.viernes.mobile.ui.screens.ChatScreen.<anonymous> (ChatScreen.kt:132)");
               }

               Modifier modifier$iv = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
               final LazyListState var8 = listState;
               final MutableState var9 = messages$delegate;
               final VoiceManager var10 = voiceManager;
               final Context var11 = context;
               final ManagedActivityResultLauncher var12 = recordAudioPermissionLauncher;
               final State var13 = isListening$delegate;
               final MutableState var14 = inputText$delegate;
               final CoroutineScope var15 = coroutineScope;
               final HuoAvatarController var16 = huoController;
               final ViernesAiAssistant var17 = assistant;
               int $changed$iv = 0;
               int $i$f$Column = 0;
               $composer.startReplaceableGroup(-483455358);
               ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
               Arrangement.Vertical verticalArrangement$iv = Arrangement.INSTANCE.getTop();
               Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
               MeasurePolicy measurePolicy$iv = ColumnKt.columnMeasurePolicy(verticalArrangement$iv, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
               int $changed$iv$iv = 112 & $changed$iv << 3;
               int $i$f$Layout = 0;
               $composer.startReplaceableGroup(-1323940314);
               ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
               int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
               CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
               Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
               Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$iv);
               int $changed$iv$iv$iv = 6 | 7168 & $changed$iv$iv << 9;
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
               int var30x = 0;
               Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
               Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
               Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
               int var32 = 0;
               int var34 = 0;
               if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                  $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                  $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
               }

               skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
               $composer.startReplaceableGroup(2058660585);
               int var35 = 14 & $changed$iv$iv$iv >> 9;
               int var37 = 0;
               ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
               int var38 = 6 | 112 & $changed$iv >> 6;
               ColumnScope $this$invoke_u24lambda_u243 = (ColumnScope)ColumnScopeInstance.INSTANCE;
               int var41 = 0;
               ComposerKt.sourceInformationMarkerStart($composer, -987688306, "C144@5373L2156,138@5128L2401,187@7606L3537:ChatScreen.kt#k2q6ai");
               Modifier var10000 = ColumnScope.weight$default($this$invoke_u24lambda_u243, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
               int $this$dp$iv = 16;
               int $i$f$getDp = 0;
               Modifier var44 = PaddingKt.padding-VpY3zN4$default(var10000, Dp.constructor-impl((float)$this$dp$iv), 0.0F, 2, (Object)null);
               $i$f$getDp = 10;
               int $i$f$getDp = 0;
               Arrangement.HorizontalOrVertical $i$f$getDp = Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
               var10000 = var44;
               LazyListState var10001 = var8;
               Object var10002 = null;
               boolean var10003 = false;
               Arrangement.Vertical var10004 = (Arrangement.Vertical)$i$f$getDp;
               Object var10005 = null;
               Object var10006 = null;
               boolean var10007 = false;
               $composer.startReplaceableGroup(-1971519582);
               ComposerKt.sourceInformation($composer, "CC(remember):ChatScreen.kt#9igjgp");
               int $i$f$Row = 0;
               int $i$f$cache = 0;
               Object it$iv = $composer.rememberedValue();
               int var49 = 0;
               Object var10008;
               if (it$iv == Composer.Companion.getEmpty()) {
                  boolean var50 = false;
                  Object var51 = null;
                  Object var52 = null;
                  Arrangement.Vertical var53 = var10004;
                  boolean var54 = false;
                  Object var55 = null;
                  int var58 = 0;
                  Function1 value$iv = new Function1<LazyListScope, Unit>() {
                     public final void invoke(@NotNull LazyListScope $this$LazyColumn) {
                        Intrinsics.checkNotNullParameter($this$LazyColumn, "$this$LazyColumn");
                        LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$ChatScreenKt.INSTANCE.getLambda-2$app_debug(), 3, (Object)null);
                        List items$iv = ChatScreenKt.ChatScreen$lambda$4(var9);
                        Function1 key$iv = null;
                        Function1 contentType$iv = ChatScreenKt$ChatScreen$5$1$1$1$invoke$$inlined$items$default$1.INSTANCE;
                        int $i$f$items = 0;
                        $this$LazyColumn.items(items$iv.size(), (Function1)null, new ChatScreenKt$ChatScreen$5$1$1$1$invoke$$inlined$items$default$3(contentType$iv, items$iv), (Function4)ComposableLambdaKt.composableLambdaInstance(-632812321, true, new ChatScreenKt$ChatScreen$5$1$1$1$invoke$$inlined$items$default$4(items$iv)));
                        LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$ChatScreenKt.INSTANCE.getLambda-3$app_debug(), 3, (Object)null);
                     }
                  };
                  var10000 = var44;
                  var10001 = var8;
                  var10002 = var55;
                  var10003 = var54;
                  var10004 = var53;
                  var10005 = var52;
                  var10006 = var51;
                  var10007 = var50;
                  $composer.updateRememberedValue(value$iv);
                  var10008 = value$iv;
               } else {
                  var10008 = it$iv;
               }

               Function1 verticalAlignment$iv = (Function1)var10008;
               $composer.endReplaceableGroup();
               LazyDslKt.LazyColumn(var10000, var10001, (PaddingValues)var10002, var10003, var10004, (Alignment.Horizontal)var10005, (FlingBehavior)var10006, var10007, verticalAlignment$iv, $composer, 100687872, 236);
               var10000 = BackgroundKt.background-bw27NRU$default(SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), ColorKt.getSurfaceDark(), (Shape)null, 2, (Object)null);
               int $this$dp$iv = 12;
               int $i$f$getDp = 0;
               Modifier var106 = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
               Alignment.Vertical var104 = Alignment.Companion.getCenterVertically();
               $i$f$getDp = 390;
               $i$f$Row = 0;
               $composer.startReplaceableGroup(693286680);
               ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
               Arrangement.Horizontal horizontalArrangement$iv = Arrangement.INSTANCE.getStart();
               MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, var104, $composer, 14 & $i$f$getDp >> 3 | 112 & $i$f$getDp >> 3);
               int $changed$iv$ivx = 112 & $i$f$getDp << 3;
               var49 = 0;
               $composer.startReplaceableGroup(-1323940314);
               ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
               int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
               CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
               Function0 factory$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
               Function3 skippableUpdate$iv$iv$ivx = LayoutKt.modifierMaterializerOf(var106);
               int $changed$iv$iv$ivx = 6 | 7168 & $changed$iv$ivx << 9;
               int $i$f$ReusableComposeNode = 0;
               if (!($composer.getApplier() instanceof Applier)) {
                  ComposablesKt.invalidApplier();
               }

               $composer.startReusableNode();
               if ($composer.getInserting()) {
                  $composer.createNode(factory$iv$iv$ivx);
               } else {
                  $composer.useNode();
               }

               Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
               int var66 = 0;
               Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
               Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
               Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
               int var68 = 0;
               int var70 = 0;
               if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                  $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                  $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
               }

               skippableUpdate$iv$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivx >> 3);
               $composer.startReplaceableGroup(2058660585);
               int var71 = 14 & $changed$iv$iv$ivx >> 9;
               int var73 = 0;
               ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
               int var74 = 6 | 112 & $i$f$getDp >> 6;
               RowScope $this$invoke_u24lambda_u243_u24lambda_u242 = (RowScope)RowScopeInstance.INSTANCE;
               int var77 = 0;
               ComposerKt.sourceInformationMarkerStart($composer, -621330929, "C195@7898L1232,224@9148L39,232@9568L267,228@9299L18,226@9205L682,241@9905L39,243@9962L1167:ChatScreen.kt#k2q6ai");
               Function0 var124 = new Function0<Unit>() {
                  public final void invoke() {
                     if (ChatScreenKt.ChatScreen$lambda$6(var13)) {
                        var10.stopListening();
                     } else {
                        boolean hasPerm = ContextCompat.checkSelfPermission(var11, "android.permission.RECORD_AUDIO") == 0;
                        if (hasPerm) {
                           var10.startListening();
                        } else {
                           var12.launch("android.permission.RECORD_AUDIO");
                        }
                     }

                  }
               };
               Modifier var128 = (Modifier)Modifier.Companion;
               int $this$dp$iv = 46;
               int $i$f$getDp = 0;
               IconButtonKt.IconButton(var124, BackgroundKt.background-bw27NRU$default(ClipKt.clip(SizeKt.size-3ABfNKs(var128, Dp.constructor-impl((float)$this$dp$iv)), (Shape)RoundedCornerShapeKt.getCircleShape()), ChatScreenKt.ChatScreen$lambda$6(var13) ? ColorKt.getStatusDelayed() : ColorKt.getViernesPrimary(), (Shape)null, 2, (Object)null), false, (IconButtonColors)null, (MutableInteractionSource)null, (Function2)ComposableLambdaKt.composableLambda($composer, -264425424, true, new Function2<Composer, Integer, Unit>() {
                  @Composable
                  @ComposableTarget(
                     applier = "androidx.compose.ui.UiComposable"
                  )
                  public final void invoke(@Nullable Composer $composer, int $changed) {
                     ComposerKt.sourceInformation($composer, "C217@8898L214:ChatScreen.kt#k2q6ai");
                     if (($changed & 11) == 2 && $composer.getSkipping()) {
                        $composer.skipToGroupEnd();
                     } else {
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventStart(-264425424, $changed, -1, "com.viernes.mobile.ui.screens.ChatScreen.<anonymous>.<anonymous>.<anonymous>.<anonymous> (ChatScreen.kt:217)");
                        }

                        IconKt.Icon-ww6aTOc(ChatScreenKt.ChatScreen$lambda$6(var13) ? MicOffKt.getMicOff(Icons.INSTANCE.getDefault()) : MicKt.getMic(Icons.INSTANCE.getDefault()), "Micrófono", (Modifier)null, ColorKt.getTextPrimary(), $composer, 3120, 4);
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventEnd();
                        }
                     }

                  }
               }), $composer, 196608, 28);
               Modifier var125 = (Modifier)Modifier.Companion;
               $this$dp$iv = 8;
               $i$f$getDp = 0;
               SpacerKt.Spacer(SizeKt.width-3ABfNKs(var125, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
               String $this$dp$ivxx = ChatScreenKt.ChatScreen$lambda$1(var14);
               Modifier $i$f$getDpxx = RowScope.weight$default($this$invoke_u24lambda_u243_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
               int $this$dp$iv = 24;
               int $i$f$getDp = 0;
               RoundedCornerShape var82 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
               OutlinedTextFieldDefaults var120 = OutlinedTextFieldDefaults.INSTANCE;
               long var83 = ColorKt.getViernesPrimary();
               long var85 = ColorKt.getSurfaceElevated();
               long var87 = ColorKt.getTextPrimary();
               long var89 = ColorKt.getTextPrimary();
               TextFieldColors var119 = var120.colors-0hiis_0(var87, var89, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, (TextSelectionColors)null, var83, var85, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, $composer, 54, 432, 0, 0, 3072, 2147477500, 4095);
               String var126 = $this$dp$ivxx;
               $composer.startReplaceableGroup(1365472007);
               ComposerKt.sourceInformation($composer, "CC(remember):ChatScreen.kt#9igjgp");
               boolean var92 = false;
               int $i$f$cache = 0;
               Object it$iv = $composer.rememberedValue();
               int var95 = 0;
               Object var130;
               if (it$iv == Composer.Companion.getEmpty()) {
                  int var97 = 0;
                  Function1 var129 = new Function1<String, Unit>() {
                     public final void invoke(@NotNull String it) {
                        Intrinsics.checkNotNullParameter(it, "it");
                        ChatScreenKt.ChatScreen$lambda$2(var14, it);
                     }
                  };
                  var126 = $this$dp$ivxx;
                  Object value$iv = var129;
                  $composer.updateRememberedValue(value$iv);
                  var130 = value$iv;
               } else {
                  var130 = it$iv;
               }

               Function1 var121 = (Function1)var130;
               $composer.endReplaceableGroup();
               OutlinedTextFieldKt.OutlinedTextField(var126, var121, $i$f$getDpxx, false, false, (TextStyle)null, (Function2)null, ComposableSingletons$ChatScreenKt.INSTANCE.getLambda-4$app_debug(), (Function2)null, (Function2)null, (Function2)null, (Function2)null, (Function2)null, false, (VisualTransformation)null, (KeyboardOptions)null, (KeyboardActions)null, false, 3, 0, (MutableInteractionSource)null, (Shape)var82, var119, $composer, 12582960, 100663296, 0, 1834872);
               Modifier var127 = (Modifier)Modifier.Companion;
               int $this$dp$iv = 8;
               int $i$f$getDp = 0;
               SpacerKt.Spacer(SizeKt.width-3ABfNKs(var127, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
               IconButtonKt.IconButton(new Function0<Unit>() {
                  public final void invoke() {
                     if (!StringsKt.isBlank((CharSequence)ChatScreenKt.ChatScreen$lambda$1(var14))) {
                        final String textToSend = StringsKt.trim((CharSequence)ChatScreenKt.ChatScreen$lambda$1(var14)).toString();
                        ChatScreenKt.ChatScreen$lambda$2(var14, "");
                        BuildersKt.launch$default(var15, (CoroutineContext)null, (CoroutineStart)null, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
                           int label;

                           @Nullable
                           public final Object invokeSuspend(@NotNull Object $result) {
                              Object var3 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                              Object var10000;
                              switch (this.label) {
                                 case 0:
                                    ResultKt.throwOnFailure($result);
                                    ChatScreenKt.ChatScreen$lambda$5(var9, CollectionsKt.plus((Collection)ChatScreenKt.ChatScreen$lambda$4(var9), new ChatMessage((String)null, "user", textToSend, (String)null, 9, (DefaultConstructorMarker)null)));
                                    var16.setState(HuoState.THINKING);
                                    ViernesAiAssistant var4 = var17;
                                    String var10001 = textToSend;
                                    Continuation var10003 = (Continuation)this;
                                    this.label = 1;
                                    var10000 = ViernesAiAssistant.processUserMessage$default(var4, var10001, (Long)null, var10003, 2, (Object)null);
                                    if (var10000 == var3) {
                                       return var3;
                                    }
                                    break;
                                 case 1:
                                    ResultKt.throwOnFailure($result);
                                    var10000 = $result;
                                    break;
                                 case 2:
                                    ResultKt.throwOnFailure($result);
                                    return Unit.INSTANCE;
                                 default:
                                    throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                              }

                              AssistantResponse resp = (AssistantResponse)var10000;
                              ChatScreenKt.ChatScreen$lambda$5(var9, CollectionsKt.plus((Collection)ChatScreenKt.ChatScreen$lambda$4(var9), new ChatMessage((String)null, "viernes", resp.getText(), (String)null, 9, (DefaultConstructorMarker)null)));
                              VoiceManager.speak$default(var10, resp.getText(), (String)null, 2, (Object)null);
                              LazyListState var5 = var8;
                              int var6 = ChatScreenKt.ChatScreen$lambda$4(var9).size() - 1;
                              Continuation var7 = (Continuation)this;
                              this.label = 2;
                              if (LazyListState.animateScrollToItem$default(var5, var6, 0, var7, 2, (Object)null) == var3) {
                                 return var3;
                              } else {
                                 return Unit.INSTANCE;
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
                        }, 3, (Object)null);
                     }

                  }
               }, (Modifier)null, !StringsKt.isBlank((CharSequence)ChatScreenKt.ChatScreen$lambda$1(var14)), (IconButtonColors)null, (MutableInteractionSource)null, (Function2)ComposableLambdaKt.composableLambda($composer, 2049769575, true, new Function2<Composer, Integer, Unit>() {
                  @Composable
                  @ComposableTarget(
                     applier = "androidx.compose.ui.UiComposable"
                  )
                  public final void invoke(@Nullable Composer $composer, int $changed) {
                     ComposerKt.sourceInformation($composer, "C260@10896L215:ChatScreen.kt#k2q6ai");
                     if (($changed & 11) == 2 && $composer.getSkipping()) {
                        $composer.skipToGroupEnd();
                     } else {
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventStart(2049769575, $changed, -1, "com.viernes.mobile.ui.screens.ChatScreen.<anonymous>.<anonymous>.<anonymous>.<anonymous> (ChatScreen.kt:260)");
                        }

                        IconKt.Icon-ww6aTOc(SendKt.getSend(Icons.INSTANCE.getDefault()), "Enviar", (Modifier)null, !StringsKt.isBlank((CharSequence)ChatScreenKt.ChatScreen$lambda$1(var14)) ? ColorKt.getViernesPrimary() : ColorKt.getTextMuted(), $composer, 48, 4);
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventEnd();
                        }
                     }

                  }
               }), $composer, 196608, 26);
               ComposerKt.sourceInformationMarkerEnd($composer);
               ComposerKt.sourceInformationMarkerEnd($composer);
               $composer.endReplaceableGroup();
               $composer.endNode();
               $composer.endReplaceableGroup();
               $composer.endReplaceableGroup();
               ComposerKt.sourceInformationMarkerEnd($composer);
               ComposerKt.sourceInformationMarkerEnd($composer);
               $composer.endReplaceableGroup();
               $composer.endNode();
               $composer.endReplaceableGroup();
               $composer.endReplaceableGroup();
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventEnd();
               }
            }

         }
      }), $composer, 806879280, 445);
      if (ComposerKt.isTraceInProgress()) {
         ComposerKt.traceEventEnd();
      }

      ScopeUpdateScope var51 = $composer.endRestartGroup();
      if (var51 != null) {
         var51.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               ChatScreenKt.ChatScreen(assistant, voiceManager, huoController, onNavigateBack, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   private static final String ChatScreen$lambda$1(MutableState<String> $inputText$delegate) {
      State $this$getValue$iv = (State)$inputText$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (String)$this$getValue$iv.getValue();
   }

   private static final void ChatScreen$lambda$2(MutableState<String> $inputText$delegate, String value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $inputText$delegate.setValue(value);
   }

   private static final List<ChatMessage> ChatScreen$lambda$4(MutableState<List<ChatMessage>> $messages$delegate) {
      State $this$getValue$iv = (State)$messages$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$this$getValue$iv.getValue();
   }

   private static final void ChatScreen$lambda$5(MutableState<List<ChatMessage>> $messages$delegate, List<ChatMessage> value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $messages$delegate.setValue(value);
   }

   private static final boolean ChatScreen$lambda$6(State<Boolean> $isListening$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Boolean)$isListening$delegate.getValue();
   }

   private static final boolean ChatScreen$lambda$7(State<Boolean> $isSpeaking$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Boolean)$isSpeaking$delegate.getValue();
   }

   private static final float ChatScreen$lambda$8(State<Float> $speechAmp$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return ((Number)$speechAmp$delegate.getValue()).floatValue();
   }
}
