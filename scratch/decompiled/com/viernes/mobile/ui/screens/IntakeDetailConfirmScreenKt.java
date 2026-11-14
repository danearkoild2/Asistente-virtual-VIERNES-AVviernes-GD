package com.viernes.mobile.ui.screens;

import android.content.Context;
import android.widget.Toast;
import androidx.compose.foundation.BackgroundKt;
import androidx.compose.foundation.BorderStroke;
import androidx.compose.foundation.ScrollKt;
import androidx.compose.foundation.gestures.FlingBehavior;
import androidx.compose.foundation.interaction.MutableInteractionSource;
import androidx.compose.foundation.layout.Arrangement;
import androidx.compose.foundation.layout.BoxKt;
import androidx.compose.foundation.layout.BoxScope;
import androidx.compose.foundation.layout.BoxScopeInstance;
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
import androidx.compose.foundation.shape.RoundedCornerShape;
import androidx.compose.foundation.shape.RoundedCornerShapeKt;
import androidx.compose.foundation.text.KeyboardActions;
import androidx.compose.foundation.text.KeyboardOptions;
import androidx.compose.foundation.text.selection.TextSelectionColors;
import androidx.compose.material.icons.Icons;
import androidx.compose.material.icons.filled.VerifiedUserKt;
import androidx.compose.material3.AndroidAlertDialog_androidKt;
import androidx.compose.material3.AppBarKt;
import androidx.compose.material3.ButtonColors;
import androidx.compose.material3.ButtonDefaults;
import androidx.compose.material3.ButtonElevation;
import androidx.compose.material3.ButtonKt;
import androidx.compose.material3.CardColors;
import androidx.compose.material3.CardDefaults;
import androidx.compose.material3.CardElevation;
import androidx.compose.material3.CardKt;
import androidx.compose.material3.IconButtonColors;
import androidx.compose.material3.IconButtonKt;
import androidx.compose.material3.IconKt;
import androidx.compose.material3.MaterialTheme;
import androidx.compose.material3.OutlinedTextFieldDefaults;
import androidx.compose.material3.OutlinedTextFieldKt;
import androidx.compose.material3.ProgressIndicatorKt;
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
import androidx.compose.ui.graphics.Color;
import androidx.compose.ui.graphics.Shape;
import androidx.compose.ui.graphics.vector.ImageVector;
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
import androidx.compose.ui.unit.TextUnitKt;
import androidx.compose.ui.window.DialogProperties;
import com.viernes.mobile.data.repository.IntakeRepository;
import com.viernes.mobile.data.repository.MedicationRepository;
import com.viernes.mobile.domain.model.Intake;
import com.viernes.mobile.domain.model.IntakeStatus;
import com.viernes.mobile.domain.model.Medication;
import com.viernes.mobile.domain.model.VerificationStatus;
import com.viernes.mobile.notifications.AlarmScheduler;
import com.viernes.mobile.ui.theme.ColorKt;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.coroutines.EmptyCoroutineContext;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.functions.Function3;
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
   d1 = {"\u0000<\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000b\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0002\u001a3\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0006\u001a\u00020\u00072\f\u0010\b\u001a\b\u0012\u0004\u0012\u00020\u00010\tH\u0007¢\u0006\u0002\u0010\n¨\u0006\u000b²\u0006\f\u0010\f\u001a\u0004\u0018\u00010\rX\u008a\u008e\u0002²\u0006\f\u0010\u000e\u001a\u0004\u0018\u00010\u000fX\u008a\u008e\u0002²\u0006\n\u0010\u0010\u001a\u00020\u0011X\u008a\u008e\u0002²\u0006\n\u0010\u0012\u001a\u00020\u0013X\u008a\u008e\u0002²\u0006\n\u0010\u0014\u001a\u00020\u0013X\u008a\u008e\u0002²\u0006\n\u0010\u0015\u001a\u00020\u0011X\u008a\u008e\u0002"},
   d2 = {"IntakeDetailConfirmScreen", "", "intakeId", "", "intakeRepo", "Lcom/viernes/mobile/data/repository/IntakeRepository;", "medRepo", "Lcom/viernes/mobile/data/repository/MedicationRepository;", "onNavigateBack", "Lkotlin/Function0;", "(JLcom/viernes/mobile/data/repository/IntakeRepository;Lcom/viernes/mobile/data/repository/MedicationRepository;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "app_debug", "intake", "Lcom/viernes/mobile/domain/model/Intake;", "medication", "Lcom/viernes/mobile/domain/model/Medication;", "isLoading", "", "notesText", "", "skipReasonText", "showSkipDialog"}
)
@SourceDebugExtension({"SMAP\nIntakeDetailConfirmScreen.kt\nKotlin\n*S Kotlin\n*F\n+ 1 IntakeDetailConfirmScreen.kt\ncom/viernes/mobile/ui/screens/IntakeDetailConfirmScreenKt\n+ 2 CompositionLocal.kt\nandroidx/compose/runtime/CompositionLocal\n+ 3 Effects.kt\nandroidx/compose/runtime/EffectsKt\n+ 4 Composables.kt\nandroidx/compose/runtime/ComposablesKt\n+ 5 Composer.kt\nandroidx/compose/runtime/ComposerKt\n+ 6 Effects.kt\nandroidx/compose/runtime/EffectsKt$rememberCoroutineScope$1\n+ 7 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,353:1\n74#2:354\n487#3,4:355\n491#3,2:363\n495#3:369\n25#4:359\n1116#5,3:360\n1119#5,3:366\n1116#5,6:370\n1116#5,6:376\n1116#5,6:382\n1116#5,6:388\n1116#5,6:394\n1116#5,6:400\n1116#5,6:406\n487#6:365\n81#7:412\n107#7,2:413\n81#7:415\n107#7,2:416\n81#7:418\n107#7,2:419\n81#7:421\n107#7,2:422\n81#7:424\n107#7,2:425\n81#7:427\n107#7,2:428\n*S KotlinDebug\n*F\n+ 1 IntakeDetailConfirmScreen.kt\ncom/viernes/mobile/ui/screens/IntakeDetailConfirmScreenKt\n*L\n37#1:354\n38#1:355,4\n38#1:363,2\n38#1:369\n38#1:359\n38#1:360,3\n38#1:366,3\n40#1:370,6\n41#1:376,6\n42#1:382,6\n43#1:388,6\n44#1:394,6\n45#1:400,6\n305#1:406,6\n38#1:365\n40#1:412\n40#1:413,2\n41#1:415\n41#1:416,2\n42#1:418\n42#1:419,2\n43#1:421\n43#1:422,2\n44#1:424\n44#1:425,2\n45#1:427\n45#1:428,2\n*E\n"})
public final class IntakeDetailConfirmScreenKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void IntakeDetailConfirmScreen(final long intakeId, @NotNull final IntakeRepository intakeRepo, @NotNull final MedicationRepository medRepo, @NotNull final Function0<Unit> onNavigateBack, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(intakeRepo, "intakeRepo");
      Intrinsics.checkNotNullParameter(medRepo, "medRepo");
      Intrinsics.checkNotNullParameter(onNavigateBack, "onNavigateBack");
      $composer = $composer.startRestartGroup(822407759);
      ComposerKt.sourceInformation($composer, "C(IntakeDetailConfirmScreen)36@1396L7,37@1429L24,39@1473L42,40@1538L46,41@1606L33,42@1661L31,43@1719L31,44@1777L34,46@1817L278,56@2101L11647,304@13877L26,303@13833L2085:IntakeDetailConfirmScreen.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(intakeId) ? 4 : 2);
      }

      if (($changed & 112) == 0) {
         $dirty |= $composer.changed(intakeRepo) ? 32 : 16;
      }

      if (($changed & 896) == 0) {
         $dirty |= $composer.changed(medRepo) ? 256 : 128;
      }

      if (($changed & 7168) == 0) {
         $dirty |= $composer.changedInstance(onNavigateBack) ? 2048 : 1024;
      }

      if (($dirty & 5851) == 1170 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(822407759, $dirty, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen (IntakeDetailConfirmScreen.kt:35)");
         }

         CompositionLocal this_$iv = (CompositionLocal)AndroidCompositionLocals_androidKt.getLocalContext();
         int $changed$iv = 0;
         int $i$f$getCurrent = 0;
         ComposerKt.sourceInformationMarkerStart($composer, 2023513938, "CC:CompositionLocal.kt#9igjgp");
         Object var12 = $composer.consume(this_$iv);
         ComposerKt.sourceInformationMarkerEnd($composer);
         final Context context = (Context)var12;
         $i$f$getCurrent = 0;
         int $i$f$rememberCoroutineScope = 0;
         $composer.startReplaceableGroup(773894976);
         ComposerKt.sourceInformation($composer, "CC(rememberCoroutineScope)489@20472L144:Effects.kt#9igjgp");
         boolean var14 = false;
         int $i$f$remember = 0;
         $composer.startReplaceableGroup(-492369756);
         ComposerKt.sourceInformation($composer, "CC(remember):Composables.kt#9igjgp");
         boolean invalid$iv$iv$iv = (boolean)0;
         int $i$f$cache = 0;
         Object it$iv$iv$iv = $composer.rememberedValue();
         int var20 = 0;
         Object var10000;
         if (it$iv$iv$iv == Composer.Companion.getEmpty()) {
            int var21 = 0;
            int var22 = 0;
            CoroutineScope var25 = EffectsKt.createCompositionCoroutineScope((CoroutineContext)EmptyCoroutineContext.INSTANCE, $composer);
            Object value$iv$iv$iv = new CompositionScopedCoroutineScopeCanceller(var25);
            $composer.updateRememberedValue(value$iv$iv$iv);
            var10000 = value$iv$iv$iv;
         } else {
            var10000 = it$iv$iv$iv;
         }

         Object value$iv = var10000;
         $composer.endReplaceableGroup();
         CompositionScopedCoroutineScopeCanceller wrapper$iv = (CompositionScopedCoroutineScopeCanceller)value$iv;
         CoroutineScope $i$f$cache = wrapper$iv.getCoroutineScope();
         $composer.endReplaceableGroup();
         final CoroutineScope coroutineScope = $i$f$cache;
         $composer.startReplaceableGroup(-1074770811);
         ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
         boolean composer$iv = false;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int $this$cache$iv$iv$iv = 0;
         if (it$iv == Composer.Companion.getEmpty()) {
            invalid$iv$iv$iv = (boolean)0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default((Object)null, (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState medication$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         final MutableState intake$delegate = medication$delegate;
         $composer.startReplaceableGroup(-1074768727);
         ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
         $i$f$cache = 0;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         invalid$iv$iv$iv = (boolean)0;
         if (it$iv == Composer.Companion.getEmpty()) {
            $i$f$cache = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default((Object)null, (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState isLoading$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         medication$delegate = isLoading$delegate;
         $composer.startReplaceableGroup(-1074766564);
         ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
         $i$f$cache = 0;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         $i$f$cache = 0;
         if (it$iv == Composer.Companion.getEmpty()) {
            int var65 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default(true, (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState notesText$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         isLoading$delegate = notesText$delegate;
         $composer.startReplaceableGroup(-1074764806);
         ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
         $i$f$cache = 0;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var67 = 0;
         if (it$iv == Composer.Companion.getEmpty()) {
            var20 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default("", (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState skipReasonText$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         notesText$delegate = skipReasonText$delegate;
         $composer.startReplaceableGroup(-1074762950);
         ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
         $i$f$cache = 0;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         var20 = 0;
         if (it$iv == Composer.Companion.getEmpty()) {
            int var76 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default("", (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState showSkipDialog$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         skipReasonText$delegate = showSkipDialog$delegate;
         $composer.startReplaceableGroup(-1074761091);
         ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
         $i$f$cache = 0;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var78 = 0;
         if (it$iv == Composer.Companion.getEmpty()) {
            int var81 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default(false, (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState invalid$iv = (MutableState)var10000;
         $composer.endReplaceableGroup();
         showSkipDialog$delegate = invalid$iv;
         EffectsKt.LaunchedEffect(intakeId, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
            Object L$0;
            Object L$1;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               label33: {
                  Intake itk;
                  MutableState var3;
                  Object var10000;
                  label34: {
                     Object var4 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                     switch (this.label) {
                        case 0:
                           ResultKt.throwOnFailure($result);
                           IntakeRepository var6 = intakeRepo;
                           long var10001 = intakeId;
                           Continuation var10002 = (Continuation)this;
                           this.label = 1;
                           var10000 = var6.getIntakeById(var10001, var10002);
                           if (var10000 == var4) {
                              return var4;
                           }
                           break;
                        case 1:
                           ResultKt.throwOnFailure($result);
                           var10000 = $result;
                           break;
                        case 2:
                           var3 = (MutableState)this.L$1;
                           itk = (Intake)this.L$0;
                           ResultKt.throwOnFailure($result);
                           var10000 = $result;
                           break label34;
                        default:
                           throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                     }

                     itk = (Intake)var10000;
                     IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$2(intake$delegate, itk);
                     if (itk == null) {
                        break label33;
                     }

                     var3 = medication$delegate;
                     MedicationRepository var7 = medRepo;
                     long var9 = itk.getMedicationId();
                     Continuation var11 = (Continuation)this;
                     this.L$0 = itk;
                     this.L$1 = var3;
                     this.label = 2;
                     var10000 = var7.getMedicationById(var9, var11);
                     if (var10000 == var4) {
                        return var4;
                     }
                  }

                  IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$5(var3, (Medication)var10000);
                  MutableState var8 = notesText$delegate;
                  String var10 = itk.getNotes();
                  if (var10 == null) {
                     var10 = "";
                  }

                  IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$11(var8, var10);
               }

               IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$8(isLoading$delegate, false);
               return Unit.INSTANCE;
            }

            @NotNull
            public final Continuation<Unit> create(@Nullable Object value, @NotNull Continuation<?> $completion) {
               return (Continuation)(new <anonymous constructor>($completion));
            }

            @Nullable
            public final Object invoke(@NotNull CoroutineScope p1, @Nullable Continuation<? super Unit> p2) {
               return ((<undefinedtype>)this.create(p1, p2)).invokeSuspend(Unit.INSTANCE);
            }
         }, $composer, 64 | 14 & $dirty);
         ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -1421927917, true, new Function2<Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@Nullable Composer $composer, int $changed) {
               ComposerKt.sourceInformation($composer, "C65@2543L48,58@2142L463:IntakeDetailConfirmScreen.kt#k2q6ai");
               if (($changed & 11) == 2 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-1421927917, $changed, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen.<anonymous> (IntakeDetailConfirmScreen.kt:58)");
                  }

                  AppBarKt.TopAppBar(ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-1$app_debug(), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 202865165, true, new Function2<Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@Nullable Composer $composer, int $changed) {
                        ComposerKt.sourceInformation($composer, "C61@2313L167:IntakeDetailConfirmScreen.kt#k2q6ai");
                        if (($changed & 11) == 2 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(202865165, $changed, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen.<anonymous>.<anonymous> (IntakeDetailConfirmScreen.kt:61)");
                           }

                           IconButtonKt.IconButton(onNavigateBack, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-2$app_debug(), $composer, 196608, 30);
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
         }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1998111006, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter(padding, "padding");
               ComposerKt.sourceInformation($composer, "C92@3448L21,87@3279L10463:IntakeDetailConfirmScreen.kt#k2q6ai");
               int $dirty = $changed;
               if (($changed & 14) == 0) {
                  $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
               }

               if (($dirty & 91) == 18 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(1998111006, $dirty, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen.<anonymous> (IntakeDetailConfirmScreen.kt:70)");
                  }

                  $composer.startReplaceableGroup(1867425323);
                  ComposerKt.sourceInformation($composer, "71@2713L174");
                  if (IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$7(isLoading$delegate)) {
                     Modifier currentIntake = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
                     Alignment med = Alignment.Companion.getCenter();
                     int $changed$iv = 48;
                     int $i$f$Box = 0;
                     $composer.startReplaceableGroup(733328855);
                     ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
                     boolean propagateMinConstraints$iv = false;
                     MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(med, propagateMinConstraints$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                     int var79 = 112 & $changed$iv << 3;
                     int $i$f$Layout = 0;
                     $composer.startReplaceableGroup(-1323940314);
                     ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                     int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                     CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                     Function0 var87 = ComposeUiNode.Companion.getConstructor();
                     Function3 $changed$iv = LayoutKt.modifierMaterializerOf(currentIntake);
                     int $i$f$Column = 6 | 7168 & var79 << 9;
                     int $i$f$ReusableComposeNode = 0;
                     if (!($composer.getApplier() instanceof Applier)) {
                        ComposablesKt.invalidApplier();
                     }

                     $composer.startReusableNode();
                     if ($composer.getInserting()) {
                        $composer.createNode(var87);
                     } else {
                        $composer.useNode();
                     }

                     Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                     int $i$f$Layout = 0;
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                     Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                     int localMap$iv$ivxx = 0;
                     int $this$set_impl_u24lambda_u240$iv$iv$iv = 0;
                     if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                        $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                        $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                     }

                     $changed$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $i$f$Column >> 3);
                     $composer.startReplaceableGroup(2058660585);
                     int var105 = 14 & $i$f$Column >> 9;
                     int $composer$iv = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                     int var109 = 6 | 112 & $changed$iv >> 6;
                     BoxScope var165 = (BoxScope)BoxScopeInstance.INSTANCE;
                     int var31 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, -1403843751, "C72@2824L49:IntakeDetailConfirmScreen.kt#k2q6ai");
                     ProgressIndicatorKt.CircularProgressIndicator-LxG7B9w((Modifier)null, ColorKt.getViernesPrimary(), 0.0F, 0L, 0, $composer, 48, 29);
                     ComposerKt.sourceInformationMarkerEnd($composer);
                     ComposerKt.sourceInformationMarkerEnd($composer);
                     $composer.endReplaceableGroup();
                     $composer.endNode();
                     $composer.endReplaceableGroup();
                     $composer.endReplaceableGroup();
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventEnd();
                     }

                     $composer.endReplaceableGroup();
                     return;
                  }

                  $composer.endReplaceableGroup();
                  final Intake currentIntake = IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$1(intake$delegate);
                  $composer.startReplaceableGroup(1867434503);
                  ComposerKt.sourceInformation($composer, "79@3011L190");
                  if (currentIntake == null) {
                     Modifier modifier$ivx = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
                     Alignment $this$dp$ivxxxxxxxx = Alignment.Companion.getCenter();
                     int $changed$iv = 48;
                     int $i$f$Box = 0;
                     $composer.startReplaceableGroup(733328855);
                     ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
                     boolean propagateMinConstraints$iv = false;
                     MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy($this$dp$ivxxxxxxxx, propagateMinConstraints$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                     int $changed$iv$ivxx = 112 & $changed$iv << 3;
                     int $i$f$Layout = 0;
                     $composer.startReplaceableGroup(-1323940314);
                     ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                     int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                     CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                     Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                     Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$ivx);
                     int $changed$iv$iv$iv = 6 | 7168 & $changed$iv$ivxx << 9;
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
                     int var98 = 0;
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                     Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                     int var102 = 0;
                     int var104 = 0;
                     if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                        $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                        $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                     }

                     skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                     $composer.startReplaceableGroup(2058660585);
                     int $changed$ivxx = 14 & $changed$iv$iv$iv >> 9;
                     int var108 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                     int $changedx = 6 | 112 & $changed$iv >> 6;
                     BoxScope var164 = (BoxScope)BoxScopeInstance.INSTANCE;
                     int var111 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, -1403547639, "C80@3122L65:IntakeDetailConfirmScreen.kt#k2q6ai");
                     TextKt.Text--4IGK_g("Toma no encontrada o ya eliminada.", (Modifier)null, ColorKt.getTextSecondary(), 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 390, 0, 131066);
                     ComposerKt.sourceInformationMarkerEnd($composer);
                     ComposerKt.sourceInformationMarkerEnd($composer);
                     $composer.endReplaceableGroup();
                     $composer.endNode();
                     $composer.endReplaceableGroup();
                     $composer.endReplaceableGroup();
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventEnd();
                     }

                     $composer.endReplaceableGroup();
                     return;
                  }

                  $composer.endReplaceableGroup();
                  final Medication med = IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$4(medication$delegate);
                  Modifier var10000 = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
                  int $this$dp$iv = 16;
                  int $i$f$getDp = 0;
                  Modifier contentAlignment$ivx = ScrollKt.verticalScroll$default(PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), ScrollKt.rememberScrollState(0, $composer, 0, 1), false, (FlingBehavior)null, false, 14, (Object)null);
                  $i$f$getDp = 16;
                  int $i$f$getDp = 0;
                  Arrangement.Vertical $i$f$getDpxxxxxxxx = (Arrangement.Vertical)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                  final MutableState measurePolicy$ivx = notesText$delegate;
                  final CoroutineScope $changed$iv$ivx = coroutineScope;
                  final IntakeRepository $i$f$Layoutx = intakeRepo;
                  final Context compositeKeyHash$iv$iv = context;
                  final Function0 localMap$iv$ivx = onNavigateBack;
                  final MutableState factory$iv$iv$ivx = invalid$iv;
                  int $changed$iv = 48;
                  int $i$f$Column = 0;
                  $composer.startReplaceableGroup(-483455358);
                  ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                  Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
                  MeasurePolicy measurePolicy$iv = ColumnKt.columnMeasurePolicy($i$f$getDpxxxxxxxx, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                  int $this$Layout_u24lambda_u240$iv$ivx = 112 & $changed$iv << 3;
                  int $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  Function0 $this$set_impl_u24lambda_u240$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
                  Function3 var24 = LayoutKt.modifierMaterializerOf(contentAlignment$ivx);
                  int $changed$ivxxx = 6 | 7168 & $this$Layout_u24lambda_u240$iv$ivx << 9;
                  int $i$f$ReusableComposeNode = 0;
                  if (!($composer.getApplier() instanceof Applier)) {
                     ComposablesKt.invalidApplier();
                  }

                  $composer.startReusableNode();
                  if ($composer.getInserting()) {
                     $composer.createNode($this$set_impl_u24lambda_u240$iv$iv$ivx);
                  } else {
                     $composer.useNode();
                  }

                  Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                  int $changedxx = 0;
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                  Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                  int $this$invoke_u24lambda_u240 = 0;
                  int var32 = 0;
                  if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                     $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                     $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                  }

                  var24.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$ivxxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int var33 = 14 & $changed$ivxxx >> 9;
                  int var35 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                  int var36 = 6 | 112 & $changed$iv >> 6;
                  ColumnScope var157 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  int var39 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -1402760425, "C106@4030L40,104@3934L3534,176@7631L44,174@7535L1373,207@9245L247,204@9045L18,202@8959L598,219@9751L40,217@9655L935,236@10604L40:IntakeDetailConfirmScreen.kt#k2q6ai");
                  long var158;
                  switch (null.WhenMappings.$EnumSwitchMapping$0[currentIntake.getStatus().ordinal()]) {
                     case 1 -> var158 = ColorKt.getStatusConfirmed();
                     case 2 -> var158 = ColorKt.getStatusPending();
                     case 3 -> var158 = ColorKt.getStatusDelayed();
                     case 4 -> var158 = ColorKt.getStatusSkipped();
                     default -> var158 = ColorKt.getTextSecondary();
                  }

                  final long statusColor = var158;
                  Modifier var42 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  CardColors var43 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  int $this$dp$iv = 16;
                  int $i$f$getDp = 0;
                  RoundedCornerShape var46 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var42, (Shape)var46, var43, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 98397750, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                        Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                        ComposerKt.sourceInformation($composer, "C109@4154L3300:IntakeDetailConfirmScreen.kt#k2q6ai");
                        if (($changed & 81) == 16 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(98397750, $changed, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen.<anonymous>.<anonymous>.<anonymous> (IntakeDetailConfirmScreen.kt:109)");
                           }

                           Modifier var10000 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 16;
                           int $i$f$getDp = 0;
                           Modifier modifier$ivxx = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                           Medication var7 = med;
                           Intake var8 = currentIntake;
                           long var9 = statusColor;
                           int $changed$iv = 6;
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
                           Function0 factory$iv$iv$ivxxx = ComposeUiNode.Companion.getConstructor();
                           Function3 skippableUpdate$iv$iv$ivxxx = LayoutKt.modifierMaterializerOf(modifier$ivxx);
                           int $changed$iv$iv$ivxxx = 6 | 7168 & $changed$iv$iv << 9;
                           int $i$f$ReusableComposeNode = 0;
                           if (!($composer.getApplier() instanceof Applier)) {
                              ComposablesKt.invalidApplier();
                           }

                           $composer.startReusableNode();
                           if ($composer.getInserting()) {
                              $composer.createNode(factory$iv$iv$ivxxx);
                           } else {
                              $composer.useNode();
                           }

                           Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                           int var23 = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           int var25 = 0;
                           int var27 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           skippableUpdate$iv$iv$ivxxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxxx >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           int var28 = 14 & $changed$iv$iv$ivxxx >> 9;
                           int var30 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                           int var31 = 6 | 112 & $changed$iv >> 6;
                           ColumnScope var230 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int var34 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -117844517, "C110@4219L1211,136@5452L41,139@5651L10,137@5514L291,152@6176L40,153@6237L1199:IntakeDetailConfirmScreen.kt#k2q6ai");
                           Modifier modifier$ivx = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                           Arrangement.Horizontal horizontalArrangement$iv = (Arrangement.Horizontal)Arrangement.INSTANCE.getSpaceBetween();
                           Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                           short $changed$ivxxx = 438;
                           int $i$f$Row = 0;
                           $composer.startReplaceableGroup(693286680);
                           ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                           MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, verticalAlignment$iv, $composer, 14 & $changed$ivxxx >> 3 | 112 & $changed$ivxxx >> 3);
                           int $changed$iv$ivx = 112 & $changed$ivxxx << 3;
                           int $i$f$Layout = 0;
                           $composer.startReplaceableGroup(-1323940314);
                           ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                           int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                           CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                           Function0 factory$iv$iv$ivxxxx = ComposeUiNode.Companion.getConstructor();
                           Function3 skippableUpdate$iv$iv$ivxxxx = LayoutKt.modifierMaterializerOf(modifier$ivx);
                           int $changed$iv$iv$ivxxxx = 6 | 7168 & $changed$iv$ivx << 9;
                           int $i$f$ReusableComposeNode = 0;
                           if (!($composer.getApplier() instanceof Applier)) {
                              ComposablesKt.invalidApplier();
                           }

                           $composer.startReusableNode();
                           if ($composer.getInserting()) {
                              $composer.createNode(factory$iv$iv$ivxxxx);
                           } else {
                              $composer.useNode();
                           }

                           Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                           int var50 = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           int var52 = 0;
                           int var54 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           skippableUpdate$iv$iv$ivxxxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxxxx >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           int $changed$ivxxxx = 14 & $changed$iv$iv$ivxxxx >> 9;
                           int var57 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                           int $changedxxx = 6 | 112 & $changed$ivxxx >> 6;
                           RowScope var231 = (RowScope)RowScopeInstance.INSTANCE;
                           int var61 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 1285976362, "C117@4610L10,115@4477L288,121@4790L618:IntakeDetailConfirmScreen.kt#k2q6ai");
                           String var62 = "Paciente: " + var8.getPatientName();
                           TextStyle var63 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                           FontWeight var64 = FontWeight.Companion.getBold();
                           long var65 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g(var62, (Modifier)null, var65, 0L, (FontStyle)null, var64, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var63, $composer, 196992, 0, 65498);
                           Modifier var232 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 6;
                           int $i$f$getDp = 0;
                           var232 = BackgroundKt.background-bw27NRU$default(ClipKt.clip(var232, (Shape)RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv))), Color.copy-wmQWz5c$default(var9, 0.2F, 0.0F, 0.0F, 0.0F, 14, (Object)null), (Shape)null, 2, (Object)null);
                           $this$dp$iv = 8;
                           $i$f$getDp = 0;
                           float var10001 = Dp.constructor-impl((float)$this$dp$iv);
                           $this$dp$iv = 4;
                           $i$f$getDp = 0;
                           Modifier $changed$ivxxxxxxxx = PaddingKt.padding-VpY3zN4(var232, var10001, Dp.constructor-impl((float)$this$dp$iv));
                           byte $changed$ivxxxxx = 0;
                           int $i$f$Box = 0;
                           $composer.startReplaceableGroup(733328855);
                           ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
                           Alignment contentAlignment$iv = Alignment.Companion.getTopStart();
                           boolean propagateMinConstraints$iv = false;
                           MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(contentAlignment$iv, propagateMinConstraints$iv, $composer, 14 & $changed$ivxxxxx >> 3 | 112 & $changed$ivxxxxx >> 3);
                           int compositeKeyHash$iv$iv = 112 & $changed$ivxxxxx << 3;
                           int $i$f$Layout = 0;
                           $composer.startReplaceableGroup(-1323940314);
                           ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                           int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                           CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                           Function0 factory$iv$iv$ivxxxxx = ComposeUiNode.Companion.getConstructor();
                           Function3 skippableUpdate$iv$iv$ivxxxxx = LayoutKt.modifierMaterializerOf($changed$ivxxxxxxxx);
                           int $changed$iv$iv$ivxxxxx = 6 | 7168 & compositeKeyHash$iv$iv << 9;
                           int $i$f$ReusableComposeNode = 0;
                           if (!($composer.getApplier() instanceof Applier)) {
                              ComposablesKt.invalidApplier();
                           }

                           $composer.startReusableNode();
                           if ($composer.getInserting()) {
                              $composer.createNode(factory$iv$iv$ivxxxxx);
                           } else {
                              $composer.useNode();
                           }

                           Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                           int var79 = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           int var81 = 0;
                           int var83 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           label142: {
                              skippableUpdate$iv$iv$ivxxxxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxxxxx >> 3);
                              $composer.startReplaceableGroup(2058660585);
                              int var84 = 14 & $changed$iv$iv$ivxxxxx >> 9;
                              int var86 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                              int var87 = 6 | 112 & $changed$ivxxxxx >> 6;
                              BoxScope var234 = (BoxScope)BoxScopeInstance.INSTANCE;
                              int var90 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, 663948196, "C127@5116L266:IntakeDetailConfirmScreen.kt#k2q6ai");
                              String var91 = var8.getStatus().getValue();
                              FontWeight var92 = FontWeight.Companion.getBold();
                              long var93 = TextUnitKt.getSp(12);
                              TextKt.Text--4IGK_g(var91, (Modifier)null, var9, var93, (FontStyle)null, var92, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 199680, 0, 131026);
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
                              Modifier var235 = (Modifier)Modifier.Companion;
                              int $this$dp$iv = 12;
                              int $i$f$getDp = 0;
                              SpacerKt.Spacer(SizeKt.height-3ABfNKs(var235, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                              if (var7 != null) {
                                 var236 = var7.getTranscribedName();
                                 if (var236 != null) {
                                    break label142;
                                 }
                              }

                              var236 = var8.getMedicationName();
                           }

                           String $this$dp$ivxx = var236;
                           TextStyle $i$f$getDpxx = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getHeadlineMedium();
                           FontWeight $i$f$getDpxxx = FontWeight.Companion.getBold();
                           long var95 = ColorKt.getViernesPrimaryLight();
                           TextKt.Text--4IGK_g($this$dp$ivxx, (Modifier)null, var95, 0L, (FontStyle)null, $i$f$getDpxxx, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, $i$f$getDpxx, $composer, 196992, 0, 65498);
                           $composer.startReplaceableGroup(134794462);
                           ComposerKt.sourceInformation($composer, "147@6034L10,145@5897L235");
                           CharSequence modifier$ivxxx = (CharSequence)(var7 != null ? var7.getActiveIngredient() : null);
                           if (modifier$ivxxx != null && !StringsKt.isBlank(modifier$ivxxx)) {
                              String var111 = "Principio Activo: " + (var7 != null ? var7.getActiveIngredient() : null);
                              $i$f$getDpxx = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodyMedium();
                              long var97 = ColorKt.getTextSecondary();
                              TextKt.Text--4IGK_g(var111, (Modifier)null, var97, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, $i$f$getDpxx, $composer, 384, 0, 65530);
                           }

                           $composer.endReplaceableGroup();
                           var232 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 8;
                           int $i$f$getDp = 0;
                           SpacerKt.Spacer(SizeKt.height-3ABfNKs(var232, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                           Modifier var113 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                           $i$f$getDp = 16;
                           int $i$f$getDp = 0;
                           Arrangement.Horizontal var119 = (Arrangement.Horizontal)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                           $changed$ivxxx = 54;
                           $i$f$Row = 0;
                           $composer.startReplaceableGroup(693286680);
                           ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                           Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getTop();
                           measurePolicy$iv = RowKt.rowMeasurePolicy(var119, verticalAlignment$iv, $composer, 14 & $changed$ivxxx >> 3 | 112 & $changed$ivxxx >> 3);
                           $changed$iv$ivx = 112 & $changed$ivxxx << 3;
                           $i$f$Layout = 0;
                           $composer.startReplaceableGroup(-1323940314);
                           ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                           compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                           localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                           factory$iv$iv$ivxxxx = ComposeUiNode.Companion.getConstructor();
                           skippableUpdate$iv$iv$ivxxxx = LayoutKt.modifierMaterializerOf(var113);
                           $changed$iv$iv$ivxxxx = 6 | 7168 & $changed$iv$ivx << 9;
                           $i$f$ReusableComposeNode = 0;
                           if (!($composer.getApplier() instanceof Applier)) {
                              ComposablesKt.invalidApplier();
                           }

                           $composer.startReusableNode();
                           if ($composer.getInserting()) {
                              $composer.createNode(factory$iv$iv$ivxxxx);
                           } else {
                              $composer.useNode();
                           }

                           $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                           var50 = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           var52 = 0;
                           var54 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           skippableUpdate$iv$iv$ivxxxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxxxx >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           $changed$ivxxxx = 14 & $changed$iv$iv$ivxxxx >> 9;
                           var57 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                           $changedxxx = 6 | 112 & $changed$ivxxx >> 6;
                           RowScope var238 = (RowScope)RowScopeInstance.INSTANCE;
                           var61 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 1287911537, "C157@6426L308,161@6759L328,165@7112L302:IntakeDetailConfirmScreen.kt#k2q6ai");
                           int $changed$iv = 0;
                           int $i$f$Column = 0;
                           $composer.startReplaceableGroup(-483455358);
                           ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                           Modifier modifier$iv = (Modifier)Modifier.Companion;
                           Arrangement.Vertical verticalArrangement$iv = Arrangement.INSTANCE.getTop();
                           Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
                           MeasurePolicy measurePolicy$iv = ColumnKt.columnMeasurePolicy(verticalArrangement$iv, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                           $i$f$Box = 112 & $changed$iv << 3;
                           int $i$f$Layout = 0;
                           $composer.startReplaceableGroup(-1323940314);
                           ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                           compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                           CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                           Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                           Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$iv);
                           int $changed$iv$iv$iv = 6 | 7168 & $i$f$Box << 9;
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
                           $i$f$ReusableComposeNode = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           var79 = 0;
                           var81 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           int $this$set_impl_u24lambda_u240$iv$iv$iv = 14 & $changed$iv$iv$iv >> 9;
                           int var205 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                           int $composer$iv = 6 | 112 & $changed$iv >> 6;
                           ColumnScope var239 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int $composer = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 665283769, "C158@6510L10,158@6463L88,159@6631L10,159@6580L128:IntakeDetailConfirmScreen.kt#k2q6ai");
                           TextStyle $this$invoke_u24lambda_u246_u24lambda_u241_u24lambda_u240 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getLabelSmall();
                           long var101 = ColorKt.getTextMuted();
                           TextKt.Text--4IGK_g("Dosis Programada", (Modifier)null, var101, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, $this$invoke_u24lambda_u246_u24lambda_u241_u24lambda_u240, $composer, 390, 0, 65530);
                           String var212 = var8.getDoseText();
                           TextStyle var217 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleSmall();
                           FontWeight var103 = FontWeight.Companion.getSemiBold();
                           long var104 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g(var212, (Modifier)null, var104, 0L, (FontStyle)null, var103, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var217, $composer, 196992, 0, 65498);
                           ComposerKt.sourceInformationMarkerEnd($composer);
                           ComposerKt.sourceInformationMarkerEnd($composer);
                           $composer.endReplaceableGroup();
                           $composer.endNode();
                           $composer.endReplaceableGroup();
                           $composer.endReplaceableGroup();
                           $changed$iv = 0;
                           $i$f$Column = 0;
                           $composer.startReplaceableGroup(-483455358);
                           ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                           modifier$iv = (Modifier)Modifier.Companion;
                           verticalArrangement$iv = Arrangement.INSTANCE.getTop();
                           horizontalAlignment$iv = Alignment.Companion.getStart();
                           measurePolicy$iv = ColumnKt.columnMeasurePolicy(verticalArrangement$iv, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                           $i$f$Box = 112 & $changed$iv << 3;
                           $i$f$Layout = 0;
                           $composer.startReplaceableGroup(-1323940314);
                           ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                           compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                           localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                           factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                           skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$iv);
                           $changed$iv$iv$iv = 6 | 7168 & $i$f$Box << 9;
                           $i$f$ReusableComposeNode = 0;
                           if (!($composer.getApplier() instanceof Applier)) {
                              ComposablesKt.invalidApplier();
                           }

                           $composer.startReusableNode();
                           if ($composer.getInserting()) {
                              $composer.createNode(factory$iv$iv$iv);
                           } else {
                              $composer.useNode();
                           }

                           $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                           $i$f$ReusableComposeNode = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           var79 = 0;
                           var81 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           $this$set_impl_u24lambda_u240$iv$iv$iv = 14 & $changed$iv$iv$iv >> 9;
                           var205 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                           $composer$iv = 6 | 112 & $changed$iv >> 6;
                           var239 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           $composer = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 665614725, "C162@6839L10,162@6796L84,163@6984L10,163@6909L152:IntakeDetailConfirmScreen.kt#k2q6ai");
                           TextStyle var213 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getLabelSmall();
                           var101 = ColorKt.getTextMuted();
                           TextKt.Text--4IGK_g("Hora de Toma", (Modifier)null, var101, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var213, $composer, 390, 0, 65530);
                           String var241 = var8.getScheduledTime();
                           if (var241 == null) {
                              var241 = "Sin hora fija";
                           }

                           String var214 = var241;
                           var217 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleSmall();
                           var103 = FontWeight.Companion.getSemiBold();
                           var104 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g(var214, (Modifier)null, var104, 0L, (FontStyle)null, var103, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var217, $composer, 196992, 0, 65498);
                           ComposerKt.sourceInformationMarkerEnd($composer);
                           ComposerKt.sourceInformationMarkerEnd($composer);
                           $composer.endReplaceableGroup();
                           $composer.endNode();
                           $composer.endReplaceableGroup();
                           $composer.endReplaceableGroup();
                           $changed$iv = 0;
                           $i$f$Column = 0;
                           $composer.startReplaceableGroup(-483455358);
                           ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                           modifier$iv = (Modifier)Modifier.Companion;
                           verticalArrangement$iv = Arrangement.INSTANCE.getTop();
                           horizontalAlignment$iv = Alignment.Companion.getStart();
                           measurePolicy$iv = ColumnKt.columnMeasurePolicy(verticalArrangement$iv, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                           $i$f$Box = 112 & $changed$iv << 3;
                           $i$f$Layout = 0;
                           $composer.startReplaceableGroup(-1323940314);
                           ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                           compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                           localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                           factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                           skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$iv);
                           $changed$iv$iv$iv = 6 | 7168 & $i$f$Box << 9;
                           $i$f$ReusableComposeNode = 0;
                           if (!($composer.getApplier() instanceof Applier)) {
                              ComposablesKt.invalidApplier();
                           }

                           $composer.startReusableNode();
                           if ($composer.getInserting()) {
                              $composer.createNode(factory$iv$iv$iv);
                           } else {
                              $composer.useNode();
                           }

                           $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                           $i$f$ReusableComposeNode = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           var79 = 0;
                           var81 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           $this$set_impl_u24lambda_u240$iv$iv$iv = 14 & $changed$iv$iv$iv >> 9;
                           var205 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                           $composer$iv = 6 | 112 & $changed$iv >> 6;
                           ColumnScope var242 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           $composer = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 665964095, "C166@7185L10,166@7149L77,167@7311L10,167@7255L133:IntakeDetailConfirmScreen.kt#k2q6ai");
                           TextStyle var215 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getLabelSmall();
                           var101 = ColorKt.getTextMuted();
                           TextKt.Text--4IGK_g("Fecha", (Modifier)null, var101, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var215, $composer, 390, 0, 65530);
                           String var216 = var8.getScheduledDate();
                           var217 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleSmall();
                           var103 = FontWeight.Companion.getSemiBold();
                           var104 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g(var216, (Modifier)null, var104, 0L, (FontStyle)null, var103, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var217, $composer, 196992, 0, 65498);
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
                  }), $composer, 196614, 24);
                  var42 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  var43 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceElevated(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  $this$dp$iv = 12;
                  $i$f$getDp = 0;
                  var46 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var42, (Shape)var46, var43, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, -1718792353, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                        Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                        ComposerKt.sourceInformation($composer, "C179@7759L1135:IntakeDetailConfirmScreen.kt#k2q6ai");
                        if (($changed & 81) == 16 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(-1718792353, $changed, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen.<anonymous>.<anonymous>.<anonymous> (IntakeDetailConfirmScreen.kt:179)");
                           }

                           Modifier var10000 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 14;
                           int $i$f$getDp = 0;
                           Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                           Medication var7 = med;
                           int $changed$iv = 6;
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
                           Function3 skippableUpdate$iv$iv$ivx = LayoutKt.modifierMaterializerOf(modifier$iv);
                           int $changed$iv$iv$ivx = 6 | 7168 & $changed$iv$iv << 9;
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

                           skippableUpdate$iv$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivx >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           int var25 = 14 & $changed$iv$iv$ivx >> 9;
                           int var27 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                           int var28 = 6 | 112 & $changed$iv >> 6;
                           ColumnScope var81 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int var31 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -114335472, "C180@7824L637:IntakeDetailConfirmScreen.kt#k2q6ai");
                           Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                           int $changed$iv = 384;
                           int $i$f$Row = 0;
                           $composer.startReplaceableGroup(693286680);
                           ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                           Modifier modifier$iv = (Modifier)Modifier.Companion;
                           Arrangement.Horizontal horizontalArrangement$iv = Arrangement.INSTANCE.getStart();
                           MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, verticalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                           int $changed$iv$ivx = 112 & $changed$iv << 3;
                           int $i$f$Layout = 0;
                           $composer.startReplaceableGroup(-1323940314);
                           ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                           int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                           CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                           Function0 factory$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
                           Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$iv);
                           int $changed$iv$iv$iv = 6 | 7168 & $changed$iv$ivx << 9;
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
                           int var47 = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           int var49 = 0;
                           int var51 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           label63: {
                              skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                              $composer.startReplaceableGroup(2058660585);
                              int var52 = 14 & $changed$iv$iv$iv >> 9;
                              int var54 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                              int var55 = 6 | 112 & $changed$iv >> 6;
                              RowScope var82 = (RowScope)RowScopeInstance.INSTANCE;
                              int var58 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, 1289361748, "C181@7902L116,182@8043L39,185@8284L10,183@8107L332:IntakeDetailConfirmScreen.kt#k2q6ai");
                              ImageVector var59 = VerifiedUserKt.getVerifiedUser(Icons.INSTANCE.getDefault());
                              long var60 = ColorKt.getStatusConfirmed();
                              Modifier var83 = (Modifier)Modifier.Companion;
                              int $this$dp$iv = 18;
                              int $i$f$getDp = 0;
                              Modifier var64 = SizeKt.size-3ABfNKs(var83, Dp.constructor-impl((float)$this$dp$iv));
                              IconKt.Icon-ww6aTOc(var59, (String)null, var64, var60, $composer, 3504, 0);
                              var83 = (Modifier)Modifier.Companion;
                              int $this$dp$iv = 6;
                              int $i$f$getDp = 0;
                              SpacerKt.Spacer(SizeKt.width-3ABfNKs(var83, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                              if (var7 != null) {
                                 VerificationStatus var85 = var7.getVerificationStatus();
                                 if (var85 != null) {
                                    var86 = var85.getValue();
                                    if (var86 != null) {
                                       break label63;
                                    }
                                 }
                              }

                              var86 = "DESCONOCIDO";
                           }

                           String var79 = "Estado Clínico del Tratamiento: " + var86;
                           TextStyle var80 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getLabelMedium();
                           FontWeight var66 = FontWeight.Companion.getBold();
                           long var67 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g(var79, (Modifier)null, var67, 0L, (FontStyle)null, var66, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var80, $composer, 196992, 0, 65498);
                           ComposerKt.sourceInformationMarkerEnd($composer);
                           ComposerKt.sourceInformationMarkerEnd($composer);
                           $composer.endReplaceableGroup();
                           $composer.endNode();
                           $composer.endReplaceableGroup();
                           $composer.endReplaceableGroup();
                           $composer.startReplaceableGroup(134879489);
                           ComposerKt.sourceInformation($composer, "191@8555L40,194@8757L10,192@8620L234");
                           CharSequence $this$dp$ivxx = (CharSequence)(var7 != null ? var7.getSpecialInstructions() : null);
                           if ($this$dp$ivxx != null && !StringsKt.isBlank($this$dp$ivxx)) {
                              Modifier var87 = (Modifier)Modifier.Companion;
                              int $this$dp$iv = 6;
                              int $i$f$getDp = 0;
                              SpacerKt.Spacer(SizeKt.height-3ABfNKs(var87, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                              String var75 = "Instrucciones: " + (var7 != null ? var7.getSpecialInstructions() : null);
                              TextStyle var77 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                              long var69 = ColorKt.getTextSecondary();
                              TextKt.Text--4IGK_g(var75, (Modifier)null, var69, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var77, $composer, 384, 0, 65530);
                           }

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
                  }), $composer, 196614, 24);
                  String var113 = IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$10(measurePolicy$ivx);
                  Modifier var120 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  OutlinedTextFieldDefaults $this$dp$ivxx = OutlinedTextFieldDefaults.INSTANCE;
                  long var47 = ColorKt.getViernesPrimary();
                  long var49 = ColorKt.getSurfaceElevated();
                  long var51 = ColorKt.getTextPrimary();
                  long var53 = ColorKt.getTextPrimary();
                  TextFieldColors var144 = $this$dp$ivxx.colors-0hiis_0(var51, var53, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, (TextSelectionColors)null, var47, var49, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, $composer, 54, 432, 0, 0, 3072, 2147477500, 4095);
                  $i$f$getDp = 12;
                  int $i$f$getDp = 0;
                  RoundedCornerShape $this$dp$ivxxxx = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                  String var159 = var113;
                  $composer.startReplaceableGroup(370555755);
                  ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
                  int $i$f$cache = 0;
                  int $i$f$cache = 0;
                  Object it$iv = $composer.rememberedValue();
                  int var59 = 0;
                  Object var166;
                  if (it$iv == Composer.Companion.getEmpty()) {
                     int var61 = 0;
                     Function1 var10001 = new Function1<String, Unit>() {
                        public final void invoke(@NotNull String it) {
                           Intrinsics.checkNotNullParameter(it, "it");
                           IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$11(measurePolicy$ivx, it);
                        }
                     };
                     var159 = var113;
                     Object value$iv = var10001;
                     $composer.updateRememberedValue(value$iv);
                     var166 = value$iv;
                  } else {
                     var166 = it$iv;
                  }

                  Function1 $i$f$getDpxx = (Function1)var166;
                  $composer.endReplaceableGroup();
                  OutlinedTextFieldKt.OutlinedTextField(var159, $i$f$getDpxx, var120, false, false, (TextStyle)null, ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-3$app_debug(), (Function2)null, (Function2)null, (Function2)null, (Function2)null, (Function2)null, (Function2)null, false, (VisualTransformation)null, (KeyboardOptions)null, (KeyboardActions)null, false, 0, 0, (MutableInteractionSource)null, (Shape)$this$dp$ivxxxx, var144, $composer, 1573296, 0, 0, 2097080);
                  Modifier var114 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  CardColors var121 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  int $this$dp$iv = 12;
                  int $i$f$getDp = 0;
                  RoundedCornerShape var145 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var114, (Shape)var145, var121, (CardElevation)null, (BorderStroke)null, ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-4$app_debug(), $composer, 196614, 24);
                  Modifier var160 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 8;
                  int $i$f$getDp = 0;
                  SpacerKt.Spacer(SizeKt.height-3ABfNKs(var160, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                  if (currentIntake.getStatus() != IntakeStatus.CONFIRMED) {
                     $composer.startReplaceableGroup(-1395915843);
                     ComposerKt.sourceInformation($composer, "258@11730L46,241@10808L1301,270@12371L50,268@12230L25,267@12184L522");
                     var160 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                     $i$f$getDp = 52;
                     int $i$f$getDp = 0;
                     Modifier var116 = SizeKt.height-3ABfNKs(var160, Dp.constructor-impl((float)$i$f$getDp));
                     ButtonColors var124 = ButtonDefaults.INSTANCE.buttonColors-ro_MJ88(ColorKt.getStatusConfirmed(), 0L, 0L, 0L, $composer, 6 | ButtonDefaults.$stable << 12, 14);
                     $this$dp$iv = 12;
                     $i$f$getDp = 0;
                     RoundedCornerShape var147 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                     ButtonKt.Button(new Function0<Unit>() {
                        public final void invoke() {
                           BuildersKt.launch$default($changed$iv$ivx, (CoroutineContext)null, (CoroutineStart)null, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
                              int label;

                              @Nullable
                              public final Object invokeSuspend(@NotNull Object $result) {
                                 Object var11 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                                 Object var10000;
                                 switch (this.label) {
                                    case 0:
                                       ResultKt.throwOnFailure($result);
                                       IntakeRepository var12 = $i$f$Layoutx;
                                       long var10001 = currentIntake.getId();
                                       IntakeStatus var10002 = IntakeStatus.CONFIRMED;
                                       String var10003 = "cuidador_movil";
                                       CharSequence var3 = (CharSequence)IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$10(measurePolicy$ivx);
                                       CharSequence var10004;
                                       if (StringsKt.isBlank(var3)) {
                                          String var9 = "cuidador_movil";
                                          IntakeStatus var8 = var10002;
                                          long var6 = var10001;
                                          IntakeRepository var5 = var12;
                                          int var4 = 0;
                                          Object var10 = null;
                                          var12 = var5;
                                          var10001 = var6;
                                          var10002 = var8;
                                          var10003 = var9;
                                          var10004 = (CharSequence)var10;
                                       } else {
                                          var10004 = var3;
                                       }

                                       String var13 = (String)var10004;
                                       Continuation var10005 = (Continuation)this;
                                       this.label = 1;
                                       var10000 = var12.confirmIntake(var10001, var10002, var10003, var13, var10005);
                                       if (var10000 == var11) {
                                          return var11;
                                       }
                                       break;
                                    case 1:
                                       ResultKt.throwOnFailure($result);
                                       var10000 = $result;
                                       break;
                                    default:
                                       throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                                 }

                                 boolean ok = (Boolean)var10000;
                                 if (ok) {
                                    AlarmScheduler.INSTANCE.cancelIntakeAlarm(compositeKeyHash$iv$iv, currentIntake.getId());
                                    Toast.makeText(compositeKeyHash$iv$iv, (CharSequence)"Toma confirmada exitosamente.", 0).show();
                                    localMap$iv$ivx.invoke();
                                 }

                                 return Unit.INSTANCE;
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
                     }, var116, false, (Shape)var147, var124, (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-5$app_debug(), $composer, 805306416, 484);
                     var160 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                     int $this$dp$iv = 48;
                     int $i$f$getDp = 0;
                     var116 = SizeKt.height-3ABfNKs(var160, Dp.constructor-impl((float)$this$dp$iv));
                     ButtonColors var126 = ButtonDefaults.INSTANCE.outlinedButtonColors-ro_MJ88(0L, ColorKt.getStatusDelayed(), 0L, 0L, $composer, 48 | ButtonDefaults.$stable << 12, 13);
                     $this$dp$iv = 12;
                     $i$f$getDp = 0;
                     RoundedCornerShape var149 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                     $composer.startReplaceableGroup(370657682);
                     ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
                     $i$f$getDp = 0;
                     $i$f$cache = 0;
                     Object it$iv = $composer.rememberedValue();
                     int var154 = 0;
                     Object var163;
                     if (it$iv == Composer.Companion.getEmpty()) {
                        var59 = 0;
                        Object value$iv = new Function0<Unit>() {
                           public final void invoke() {
                              IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$17(factory$iv$iv$ivx, true);
                           }
                        };
                        $composer.updateRememberedValue(value$iv);
                        var163 = value$iv;
                     } else {
                        var163 = it$iv;
                     }

                     Function0 var134 = (Function0)var163;
                     $composer.endReplaceableGroup();
                     ButtonKt.OutlinedButton(var134, var116, false, (Shape)var149, var126, (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-6$app_debug(), $composer, 805306422, 484);
                     $composer.endReplaceableGroup();
                  } else {
                     $composer.startReplaceableGroup(-1393991301);
                     ComposerKt.sourceInformation($composer, "280@12848L64,278@12744L974");
                     Modifier var118 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                     CardColors var127 = CardDefaults.INSTANCE.cardColors-ro_MJ88(Color.copy-wmQWz5c$default(ColorKt.getStatusConfirmed(), 0.15F, 0.0F, 0.0F, 0.0F, 14, (Object)null), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                     $this$dp$iv = 12;
                     $i$f$getDp = 0;
                     var145 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                     CardKt.Card(var118, (Shape)var145, var127, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1585932306, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                        @Composable
                        @ComposableTarget(
                           applier = "androidx.compose.ui.UiComposable"
                        )
                        public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                           Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                           ComposerKt.sourceInformation($composer, "C283@13008L692:IntakeDetailConfirmScreen.kt#k2q6ai");
                           if (($changed & 81) == 16 && $composer.getSkipping()) {
                              $composer.skipToGroupEnd();
                           } else {
                              if (ComposerKt.isTraceInProgress()) {
                                 ComposerKt.traceEventStart(1585932306, $changed, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen.<anonymous>.<anonymous>.<anonymous> (IntakeDetailConfirmScreen.kt:283)");
                              }

                              Modifier var10000 = (Modifier)Modifier.Companion;
                              int $this$dp$iv = 16;
                              int $i$f$getDp = 0;
                              Modifier modifier$ivx = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                              Intake var7 = currentIntake;
                              int $changed$iv = 6;
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
                              Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$ivx);
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
                              ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                              int var28 = 6 | 112 & $changed$iv >> 6;
                              ColumnScope var41 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                              int var31 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, -109138477, "C286@13205L10,284@13077L287,292@13583L10,290@13389L289:IntakeDetailConfirmScreen.kt#k2q6ai");
                              TextStyle var32 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                              FontWeight var33 = FontWeight.Companion.getBold();
                              long var34 = ColorKt.getStatusConfirmed();
                              TextKt.Text--4IGK_g("✅ Dosis Administrada y Registrada", (Modifier)null, var34, 0L, (FontStyle)null, var33, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var32, $composer, 196998, 0, 65498);
                              String var42 = var7.getConfirmedBy();
                              if (var42 == null) {
                                 var42 = "Cuidador";
                              }

                              String var10001 = var7.getConfirmedAt();
                              if (var10001 == null) {
                                 var10001 = "";
                              }

                              String var38 = "Confirmado por: " + var42 + " a las " + var10001;
                              TextStyle var39 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                              var34 = ColorKt.getTextPrimary();
                              TextKt.Text--4IGK_g(var38, (Modifier)null, var34, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var39, $composer, 384, 0, 65530);
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
                     }), $composer, 196614, 24);
                     $composer.endReplaceableGroup();
                  }

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
                  int[] var0 = new int[IntakeStatus.values().length];

                  try {
                     var0[IntakeStatus.CONFIRMED.ordinal()] = 1;
                  } catch (NoSuchFieldError var5) {
                  }

                  try {
                     var0[IntakeStatus.PENDING.ordinal()] = 2;
                  } catch (NoSuchFieldError var4) {
                  }

                  try {
                     var0[IntakeStatus.DELAYED.ordinal()] = 3;
                  } catch (NoSuchFieldError var3) {
                  }

                  try {
                     var0[IntakeStatus.SKIPPED.ordinal()] = 4;
                  } catch (NoSuchFieldError var2) {
                  }

                  $EnumSwitchMapping$0 = var0;
               }
            }
         }), $composer, 806879280, 445);
         if (IntakeDetailConfirmScreen$lambda$16(invalid$iv)) {
            $composer.startReplaceableGroup(-1074373899);
            ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
            $i$f$cache = 0;
            $i$f$cache = 0;
            it$iv = $composer.rememberedValue();
            var78 = 0;
            if (it$iv == Composer.Companion.getEmpty()) {
               int var83 = 0;
               value$iv = new Function0<Unit>() {
                  public final void invoke() {
                     IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$17(invalid$iv, false);
                  }
               };
               $composer.updateRememberedValue(value$iv);
               var10000 = value$iv;
            } else {
               var10000 = it$iv;
            }

            Function0 $this$cache$iv = (Function0)var10000;
            $composer.endReplaceableGroup();
            AndroidAlertDialog_androidKt.AlertDialog-Oix01E0($this$cache$iv, (Function2)ComposableLambdaKt.composableLambda($composer, -1382263006, true, new Function2<Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@Nullable Composer $composer, int $changed) {
                  ComposerKt.sourceInformation($composer, "C339@15599L44,323@14745L982:IntakeDetailConfirmScreen.kt#k2q6ai");
                  if (($changed & 11) == 2 && $composer.getSkipping()) {
                     $composer.skipToGroupEnd();
                  } else {
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventStart(-1382263006, $changed, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen.<anonymous> (IntakeDetailConfirmScreen.kt:323)");
                     }

                     ButtonKt.Button(new Function0<Unit>() {
                        public final void invoke() {
                           if (!StringsKt.isBlank((CharSequence)IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$13(skipReasonText$delegate))) {
                              BuildersKt.launch$default(coroutineScope, (CoroutineContext)null, (CoroutineStart)null, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
                                 int label;

                                 @Nullable
                                 public final Object invokeSuspend(@NotNull Object $result) {
                                    Object var2 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                                    switch (this.label) {
                                       case 0:
                                          ResultKt.throwOnFailure($result);
                                          IntakeRepository var10000 = intakeRepo;
                                          long var10001 = intakeId;
                                          String var10002 = IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$13(skipReasonText$delegate);
                                          Continuation var10004 = (Continuation)this;
                                          this.label = 1;
                                          if (var10000.skipIntake(var10001, var10002, "cuidador_movil", var10004) == var2) {
                                             return var2;
                                          }
                                          break;
                                       case 1:
                                          ResultKt.throwOnFailure($result);
                                          break;
                                       default:
                                          throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                                    }

                                    AlarmScheduler.INSTANCE.cancelIntakeAlarm(context, intakeId);
                                    IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$17(showSkipDialog$delegate, false);
                                    Toast.makeText(context, (CharSequence)"Omisión registrada correctamente.", 0).show();
                                    onNavigateBack.invoke();
                                    return Unit.INSTANCE;
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
                     }, (Modifier)null, false, (Shape)null, ButtonDefaults.INSTANCE.buttonColors-ro_MJ88(ColorKt.getStatusDelayed(), 0L, 0L, 0L, $composer, 6 | ButtonDefaults.$stable << 12, 14), (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-7$app_debug(), $composer, 805306368, 494);
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventEnd();
                     }
                  }

               }
            }), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 141499616, true, new Function2<Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@Nullable Composer $composer, int $changed) {
                  ComposerKt.sourceInformation($composer, "C345@15810L26,345@15789L105:IntakeDetailConfirmScreen.kt#k2q6ai");
                  if (($changed & 11) == 2 && $composer.getSkipping()) {
                     $composer.skipToGroupEnd();
                  } else {
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventStart(141499616, $changed, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen.<anonymous> (IntakeDetailConfirmScreen.kt:345)");
                     }

                     $composer.startReplaceableGroup(1867845140);
                     ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
                     boolean var5 = false;
                     final MutableState var6 = showSkipDialog$delegate;
                     int $i$f$cache = 0;
                     Object it$iv = $composer.rememberedValue();
                     int var9 = 0;
                     Object var10000;
                     if (it$iv == Composer.Companion.getEmpty()) {
                        int var10 = 0;
                        Object value$iv = new Function0<Unit>() {
                           public final void invoke() {
                              IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$17(var6, false);
                           }
                        };
                        $composer.updateRememberedValue(value$iv);
                        var10000 = value$iv;
                     } else {
                        var10000 = it$iv;
                     }

                     Function0 var3 = (Function0)var10000;
                     $composer.endReplaceableGroup();
                     ButtonKt.TextButton(var3, (Modifier)null, false, (Shape)null, (ButtonColors)null, (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-8$app_debug(), $composer, 805306374, 510);
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventEnd();
                     }
                  }

               }
            }), (Function2)null, ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-9$app_debug(), (Function2)ComposableLambdaKt.composableLambda($composer, -1867823747, true, new Function2<Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@Nullable Composer $composer, int $changed) {
                  ComposerKt.sourceInformation($composer, "C307@13999L684:IntakeDetailConfirmScreen.kt#k2q6ai");
                  if (($changed & 11) == 2 && $composer.getSkipping()) {
                     $composer.skipToGroupEnd();
                  } else {
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventStart(-1867823747, $changed, -1, "com.viernes.mobile.ui.screens.IntakeDetailConfirmScreen.<anonymous> (IntakeDetailConfirmScreen.kt:307)");
                     }

                     final MutableState var6 = skipReasonText$delegate;
                     int $changed$iv = 0;
                     int $i$f$Column = 0;
                     $composer.startReplaceableGroup(-483455358);
                     ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                     Modifier modifier$iv = (Modifier)Modifier.Companion;
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
                     int var19 = 0;
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                     Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                     int var21 = 0;
                     int var23 = 0;
                     if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                        $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                        $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                     }

                     skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                     $composer.startReplaceableGroup(2058660585);
                     int var24 = 14 & $changed$iv$iv$iv >> 9;
                     int var26 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                     int var27 = 6 | 112 & $changed$iv >> 6;
                     ColumnScope var10000 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                     int var30 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, -1392711155, "C310@14217L10,308@14028L279,313@14328L41,316@14497L23,314@14390L275:IntakeDetailConfirmScreen.kt#k2q6ai");
                     TextStyle var31 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodyMedium();
                     long var32 = ColorKt.getTextSecondary();
                     TextKt.Text--4IGK_g("Por favor indique el motivo de la omisión (ej. paciente en ayunas para exámenes, náuseas, indicación médica):", (Modifier)null, var32, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var31, $composer, 390, 0, 65530);
                     Modifier var47 = (Modifier)Modifier.Companion;
                     int $this$dp$iv = 10;
                     int $i$f$getDp = 0;
                     SpacerKt.Spacer(SizeKt.height-3ABfNKs(var47, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                     String var45 = IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$13(var6);
                     Modifier var46 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                     String var48 = var45;
                     $composer.startReplaceableGroup(370730224);
                     ComposerKt.sourceInformation($composer, "CC(remember):IntakeDetailConfirmScreen.kt#9igjgp");
                     boolean var36 = false;
                     int $i$f$cache = 0;
                     Object it$iv = $composer.rememberedValue();
                     int var39 = 0;
                     Object var49;
                     if (it$iv == Composer.Companion.getEmpty()) {
                        int var41 = 0;
                        Function1 var10001 = new Function1<String, Unit>() {
                           public final void invoke(@NotNull String it) {
                              Intrinsics.checkNotNullParameter(it, "it");
                              IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen$lambda$14(var6, it);
                           }
                        };
                        var48 = var45;
                        Object value$iv = var10001;
                        $composer.updateRememberedValue(value$iv);
                        var49 = value$iv;
                     } else {
                        var49 = it$iv;
                     }

                     Function1 var43 = (Function1)var49;
                     $composer.endReplaceableGroup();
                     OutlinedTextFieldKt.OutlinedTextField(var48, var43, var46, false, false, (TextStyle)null, ComposableSingletons$IntakeDetailConfirmScreenKt.INSTANCE.getLambda-10$app_debug(), (Function2)null, (Function2)null, (Function2)null, (Function2)null, (Function2)null, (Function2)null, false, (VisualTransformation)null, (KeyboardOptions)null, (KeyboardActions)null, false, 0, 0, (MutableInteractionSource)null, (Shape)null, (TextFieldColors)null, $composer, 1573296, 0, 0, 8388536);
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
            }), (Shape)null, 0L, 0L, 0L, 0L, 0.0F, (DialogProperties)null, $composer, 1772598, 0, 16276);
         }

         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventEnd();
         }
      }

      ScopeUpdateScope var92 = $composer.endRestartGroup();
      if (var92 != null) {
         var92.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen(intakeId, intakeRepo, medRepo, onNavigateBack, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   private static final Intake IntakeDetailConfirmScreen$lambda$1(MutableState<Intake> $intake$delegate) {
      State $this$getValue$iv = (State)$intake$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Intake)$this$getValue$iv.getValue();
   }

   private static final void IntakeDetailConfirmScreen$lambda$2(MutableState<Intake> $intake$delegate, Intake value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $intake$delegate.setValue(value);
   }

   private static final Medication IntakeDetailConfirmScreen$lambda$4(MutableState<Medication> $medication$delegate) {
      State $this$getValue$iv = (State)$medication$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Medication)$this$getValue$iv.getValue();
   }

   private static final void IntakeDetailConfirmScreen$lambda$5(MutableState<Medication> $medication$delegate, Medication value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $medication$delegate.setValue(value);
   }

   private static final boolean IntakeDetailConfirmScreen$lambda$7(MutableState<Boolean> $isLoading$delegate) {
      State $this$getValue$iv = (State)$isLoading$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Boolean)$this$getValue$iv.getValue();
   }

   private static final void IntakeDetailConfirmScreen$lambda$8(MutableState<Boolean> $isLoading$delegate, boolean value) {
      Object var3 = null;
      Object var4 = null;
      Object value$iv = value;
      int $i$f$setValue = 0;
      $isLoading$delegate.setValue(value$iv);
   }

   private static final String IntakeDetailConfirmScreen$lambda$10(MutableState<String> $notesText$delegate) {
      State $this$getValue$iv = (State)$notesText$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (String)$this$getValue$iv.getValue();
   }

   private static final void IntakeDetailConfirmScreen$lambda$11(MutableState<String> $notesText$delegate, String value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $notesText$delegate.setValue(value);
   }

   private static final String IntakeDetailConfirmScreen$lambda$13(MutableState<String> $skipReasonText$delegate) {
      State $this$getValue$iv = (State)$skipReasonText$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (String)$this$getValue$iv.getValue();
   }

   private static final void IntakeDetailConfirmScreen$lambda$14(MutableState<String> $skipReasonText$delegate, String value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $skipReasonText$delegate.setValue(value);
   }

   private static final boolean IntakeDetailConfirmScreen$lambda$16(MutableState<Boolean> $showSkipDialog$delegate) {
      State $this$getValue$iv = (State)$showSkipDialog$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Boolean)$this$getValue$iv.getValue();
   }

   private static final void IntakeDetailConfirmScreen$lambda$17(MutableState<Boolean> $showSkipDialog$delegate, boolean value) {
      Object var3 = null;
      Object var4 = null;
      Object value$iv = value;
      int $i$f$setValue = 0;
      $showSkipDialog$delegate.setValue(value$iv);
   }
}
