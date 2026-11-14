package com.viernes.mobile.ui.screens;

import androidx.compose.foundation.BorderStroke;
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
import androidx.compose.foundation.layout.SizeKt;
import androidx.compose.foundation.layout.SpacerKt;
import androidx.compose.foundation.layout.WindowInsets;
import androidx.compose.foundation.shape.RoundedCornerShape;
import androidx.compose.foundation.shape.RoundedCornerShapeKt;
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
import androidx.compose.material3.MaterialTheme;
import androidx.compose.material3.ProgressIndicatorKt;
import androidx.compose.material3.ScaffoldKt;
import androidx.compose.material3.TextKt;
import androidx.compose.material3.TopAppBarDefaults;
import androidx.compose.material3.TopAppBarScrollBehavior;
import androidx.compose.runtime.Applier;
import androidx.compose.runtime.Composable;
import androidx.compose.runtime.ComposableTarget;
import androidx.compose.runtime.ComposablesKt;
import androidx.compose.runtime.Composer;
import androidx.compose.runtime.ComposerKt;
import androidx.compose.runtime.CompositionLocalMap;
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
import androidx.compose.ui.graphics.Shape;
import androidx.compose.ui.layout.LayoutKt;
import androidx.compose.ui.layout.MeasurePolicy;
import androidx.compose.ui.node.ComposeUiNode;
import androidx.compose.ui.text.TextStyle;
import androidx.compose.ui.text.font.FontFamily;
import androidx.compose.ui.text.font.FontStyle;
import androidx.compose.ui.text.font.FontWeight;
import androidx.compose.ui.text.style.TextAlign;
import androidx.compose.ui.text.style.TextDecoration;
import androidx.compose.ui.unit.Dp;
import com.viernes.mobile.data.repository.PatientRepository;
import com.viernes.mobile.domain.model.Patient;
import com.viernes.mobile.ui.theme.ColorKt;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.functions.Function3;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.reflect.KProperty;
import kotlinx.coroutines.CoroutineScope;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 2,
   xi = 48,
   d1 = {"\u0000&\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\u001a?\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00052\u0012\u0010\u0006\u001a\u000e\u0012\u0004\u0012\u00020\u0003\u0012\u0004\u0012\u00020\u00010\u00072\f\u0010\b\u001a\b\u0012\u0004\u0012\u00020\u00010\tH\u0007¢\u0006\u0002\u0010\n¨\u0006\u000b²\u0006\f\u0010\f\u001a\u0004\u0018\u00010\rX\u008a\u008e\u0002"},
   d2 = {"PatientDetailScreen", "", "patientId", "", "patientRepo", "Lcom/viernes/mobile/data/repository/PatientRepository;", "onNavigateToTreatments", "Lkotlin/Function1;", "onNavigateBack", "Lkotlin/Function0;", "(JLcom/viernes/mobile/data/repository/PatientRepository;Lkotlin/jvm/functions/Function1;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "app_debug", "patient", "Lcom/viernes/mobile/domain/model/Patient;"}
)
@SourceDebugExtension({"SMAP\nPatientScreens.kt\nKotlin\n*S Kotlin\n*F\n+ 1 PatientScreens.kt\ncom/viernes/mobile/ui/screens/PatientScreensKt\n+ 2 Composer.kt\nandroidx/compose/runtime/ComposerKt\n+ 3 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,90:1\n1116#2,6:91\n81#3:97\n107#3,2:98\n*S KotlinDebug\n*F\n+ 1 PatientScreens.kt\ncom/viernes/mobile/ui/screens/PatientScreensKt\n*L\n28#1:91,6\n28#1:97\n28#1:98,2\n*E\n"})
public final class PatientScreensKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void PatientDetailScreen(final long patientId, @NotNull final PatientRepository patientRepo, @NotNull final Function1<? super Long, Unit> onNavigateToTreatments, @NotNull final Function0<Unit> onNavigateBack, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(patientRepo, "patientRepo");
      Intrinsics.checkNotNullParameter(onNavigateToTreatments, "onNavigateToTreatments");
      Intrinsics.checkNotNullParameter(onNavigateBack, "onNavigateBack");
      $composer = $composer.startRestartGroup(-239952440);
      ComposerKt.sourceInformation($composer, "C(PatientDetailScreen)P(2,3,1)27@981L43,29@1030L89,33@1125L2562:PatientScreens.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(patientId) ? 4 : 2);
      }

      if (($changed & 112) == 0) {
         $dirty |= $composer.changed(patientRepo) ? 32 : 16;
      }

      if (($changed & 896) == 0) {
         $dirty |= $composer.changedInstance(onNavigateToTreatments) ? 256 : 128;
      }

      if (($changed & 7168) == 0) {
         $dirty |= $composer.changedInstance(onNavigateBack) ? 2048 : 1024;
      }

      if (($dirty & 5851) == 1170 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(-239952440, $dirty, -1, "com.viernes.mobile.ui.screens.PatientDetailScreen (PatientScreens.kt:26)");
         }

         $composer.startReplaceableGroup(-261332135);
         ComposerKt.sourceInformation($composer, "CC(remember):PatientScreens.kt#9igjgp");
         boolean var11 = false;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var14 = 0;
         Object var10000;
         if (it$iv == Composer.Companion.getEmpty()) {
            int var15 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default((Object)null, (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState patient$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         EffectsKt.LaunchedEffect(patientId, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
            Object L$0;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               Object var3 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
               MutableState var2;
               Object var10000;
               switch (this.label) {
                  case 0:
                     ResultKt.throwOnFailure($result);
                     var2 = patient$delegate;
                     PatientRepository var4 = patientRepo;
                     long var10001 = patientId;
                     Continuation var10002 = (Continuation)this;
                     this.L$0 = var2;
                     this.label = 1;
                     var10000 = var4.getPatientById(var10001, var10002);
                     if (var10000 == var3) {
                        return var3;
                     }
                     break;
                  case 1:
                     var2 = (MutableState)this.L$0;
                     ResultKt.throwOnFailure($result);
                     var10000 = $result;
                     break;
                  default:
                     throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
               }

               PatientScreensKt.PatientDetailScreen$lambda$2(var2, (Patient)var10000);
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
         ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 1699258500, true, new Function2<Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@Nullable Composer $composer, int $changed) {
               ComposerKt.sourceInformation($composer, "C42@1594L48,35@1166L490:PatientScreens.kt#k2q6ai");
               if (($changed & 11) == 2 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(1699258500, $changed, -1, "com.viernes.mobile.ui.screens.PatientDetailScreen.<anonymous> (PatientScreens.kt:35)");
                  }

                  AppBarKt.TopAppBar((Function2)ComposableLambdaKt.composableLambda($composer, -1053799608, true, new Function2<Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@Nullable Composer $composer, int $changed) {
                        ComposerKt.sourceInformation($composer, "C36@1203L102:PatientScreens.kt#k2q6ai");
                        if (($changed & 11) == 2 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(-1053799608, $changed, -1, "com.viernes.mobile.ui.screens.PatientDetailScreen.<anonymous>.<anonymous> (PatientScreens.kt:36)");
                           }

                           String var7;
                           label20: {
                              Patient var10000 = PatientScreensKt.PatientDetailScreen$lambda$1(patient$delegate);
                              if (var10000 != null) {
                                 var7 = var10000.getDisplayName();
                                 if (var7 != null) {
                                    break label20;
                                 }
                              }

                              var7 = "Perfil del Paciente";
                           }

                           String var3 = var7;
                           FontWeight var4 = FontWeight.Companion.getBold();
                           long var5 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g(var3, (Modifier)null, var5, 0L, (FontStyle)null, var4, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 196992, 0, 131034);
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventEnd();
                           }
                        }

                     }
                  }), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -150879030, true, new Function2<Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@Nullable Composer $composer, int $changed) {
                        ComposerKt.sourceInformation($composer, "C38@1364L167:PatientScreens.kt#k2q6ai");
                        if (($changed & 11) == 2 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(-150879030, $changed, -1, "com.viernes.mobile.ui.screens.PatientDetailScreen.<anonymous>.<anonymous> (PatientScreens.kt:38)");
                           }

                           IconButtonKt.IconButton(onNavigateBack, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$PatientScreensKt.INSTANCE.getLambda-1$app_debug(), $composer, 196608, 30);
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
         }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, -237945767, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter(padding, "padding");
               ComposerKt.sourceInformation($composer, "C55@2010L1671:PatientScreens.kt#k2q6ai");
               int $dirty = $changed;
               if (($changed & 14) == 0) {
                  $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
               }

               if (($dirty & 91) == 18 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-237945767, $dirty, -1, "com.viernes.mobile.ui.screens.PatientDetailScreen.<anonymous> (PatientScreens.kt:47)");
                  }

                  final Patient p = PatientScreensKt.PatientDetailScreen$lambda$1(patient$delegate);
                  $composer.startReplaceableGroup(409444958);
                  ComposerKt.sourceInformation($composer, "49@1788L174");
                  if (p == null) {
                     Modifier modifier$iv = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
                     Alignment verticalArrangement$iv = Alignment.Companion.getCenter();
                     int $changed$iv = 48;
                     int $i$f$Box = 0;
                     $composer.startReplaceableGroup(733328855);
                     ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
                     boolean propagateMinConstraints$iv = false;
                     MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(verticalArrangement$iv, propagateMinConstraints$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                     int measurePolicy$ivx = 112 & $changed$iv << 3;
                     int $i$f$Layout = 0;
                     $composer.startReplaceableGroup(-1323940314);
                     ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                     int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                     CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                     Function0 localMap$iv$ivx = ComposeUiNode.Companion.getConstructor();
                     Function3 factory$iv$iv$ivx = LayoutKt.modifierMaterializerOf(modifier$iv);
                     int skippableUpdate$iv$iv$ivx = 6 | 7168 & measurePolicy$ivx << 9;
                     int $i$f$ReusableComposeNode = 0;
                     if (!($composer.getApplier() instanceof Applier)) {
                        ComposablesKt.invalidApplier();
                     }

                     $composer.startReusableNode();
                     if ($composer.getInserting()) {
                        $composer.createNode(localMap$iv$ivx);
                     } else {
                        $composer.useNode();
                     }

                     Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                     int $this$Layout_u24lambda_u240$iv$ivx = 0;
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                     Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                     int block$iv$iv$ivx = 0;
                     int var25 = 0;
                     if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                        $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                        $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                     }

                     factory$iv$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & skippableUpdate$iv$iv$ivx >> 3);
                     $composer.startReplaceableGroup(2058660585);
                     int var67 = 14 & skippableUpdate$iv$iv$ivx >> 9;
                     int var28 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                     int var68 = 6 | 112 & $changed$iv >> 6;
                     BoxScope var80 = (BoxScope)BoxScopeInstance.INSTANCE;
                     int var32 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, -1476056570, "C50@1899L49:PatientScreens.kt#k2q6ai");
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
                  Modifier var10000 = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
                  int $this$dp$iv = 16;
                  int $i$f$getDp = 0;
                  Modifier $this$dp$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                  $i$f$getDp = 14;
                  int $i$f$getDp = 0;
                  Arrangement.Vertical $this$dp$ivx = (Arrangement.Vertical)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                  final Function1 $changed$iv = onNavigateToTreatments;
                  int $changed$iv = 48;
                  int $i$f$Column = 0;
                  $composer.startReplaceableGroup(-483455358);
                  ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                  Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
                  MeasurePolicy measurePolicy$iv = ColumnKt.columnMeasurePolicy($this$dp$ivx, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                  int $i$f$Layout = 112 & $changed$iv << 3;
                  int $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  Function0 skippableUpdate$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                  Function3 $changed$iv$iv$iv = LayoutKt.modifierMaterializerOf($this$dp$iv);
                  int $i$f$ReusableComposeNode = 6 | 7168 & $i$f$Layout << 9;
                  int $i$f$ReusableComposeNode = 0;
                  if (!($composer.getApplier() instanceof Applier)) {
                     ComposablesKt.invalidApplier();
                  }

                  $composer.startReusableNode();
                  if ($composer.getInserting()) {
                     $composer.createNode(skippableUpdate$iv$iv$iv);
                  } else {
                     $composer.useNode();
                  }

                  Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                  int block$iv$iv$iv = 0;
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                  Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                  int $this$set_impl_u24lambda_u240$iv$iv$iv = 0;
                  int $changed$ivxx = 0;
                  if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                     $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                     $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                  }

                  $changed$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $i$f$ReusableComposeNode >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int $composer$iv = 14 & $i$f$ReusableComposeNode >> 9;
                  int $changedx = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                  int $composer = 6 | 112 & $changed$iv >> 6;
                  ColumnScope var77 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  int var33 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -1475681222, "C64@2330L40,62@2234L907,79@3329L45,77@3189L32,76@3155L516:PatientScreens.kt#k2q6ai");
                  Modifier var34 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  CardColors var35 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  int $this$dp$iv = 16;
                  int $i$f$getDp = 0;
                  RoundedCornerShape var38 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var34, (Shape)var38, var35, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 656842305, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                        Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                        ComposerKt.sourceInformation($composer, "C67@2454L673:PatientScreens.kt#k2q6ai");
                        if (($changed & 81) == 16 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(656842305, $changed, -1, "com.viernes.mobile.ui.screens.PatientDetailScreen.<anonymous>.<anonymous>.<anonymous> (PatientScreens.kt:67)");
                           }

                           Modifier var10000 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 16;
                           int $i$f$getDp = 0;
                           Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                           Patient var7 = p;
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
                           ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                           int var28 = 6 | 112 & $changed$iv >> 6;
                           ColumnScope var41 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int var31 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 1147528267, "C68@2568L10,68@2519L126,69@2666L40,70@2727L140,71@2888L102,72@3011L98:PatientScreens.kt#k2q6ai");
                           String var32 = var7.getDisplayName();
                           TextStyle var33 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getHeadlineMedium();
                           FontWeight var34 = FontWeight.Companion.getBold();
                           long var35 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g(var32, (Modifier)null, var35, 0L, (FontStyle)null, var34, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var33, $composer, 196992, 0, 65498);
                           Modifier var42 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 6;
                           int $i$f$getDp = 0;
                           SpacerKt.Spacer(SizeKt.height-3ABfNKs(var42, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                           String var43 = var7.getDeclaredAllergies();
                           if (var43 == null) {
                              var43 = "Ninguna";
                           }

                           TextKt.Text--4IGK_g("Alergias Declaradas: " + var43, (Modifier)null, var7.getAllergiesVerified() ? ColorKt.getStatusConfirmed() : ColorKt.getStatusDelayed(), 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 0, 0, 131066);
                           var43 = var7.getEmergencyContact();
                           if (var43 == null) {
                              var43 = "No registrado";
                           }

                           TextKt.Text--4IGK_g("Contacto de Emergencia: " + var43, (Modifier)null, ColorKt.getTextSecondary(), 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 384, 0, 131066);
                           var43 = var7.getMedicalNotes();
                           if (var43 == null) {
                              var43 = "Sin notas registradas";
                           }

                           TextKt.Text--4IGK_g("Notas Clínicas: " + var43, (Modifier)null, ColorKt.getTextSecondary(), 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 384, 0, 131066);
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
                  Modifier var78 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  int $this$dp$iv = 50;
                  int $i$f$getDp = 0;
                  var34 = SizeKt.height-3ABfNKs(var78, Dp.constructor-impl((float)$this$dp$iv));
                  ButtonColors var71 = ButtonDefaults.INSTANCE.buttonColors-ro_MJ88(ColorKt.getViernesPrimary(), 0L, 0L, 0L, $composer, 6 | ButtonDefaults.$stable << 12, 14);
                  $this$dp$iv = 12;
                  $i$f$getDp = 0;
                  RoundedCornerShape var76 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  $composer.startReplaceableGroup(1199352524);
                  ComposerKt.sourceInformation($composer, "CC(remember):PatientScreens.kt#9igjgp");
                  boolean invalid$iv = $composer.changed($changed$iv) | $composer.changed(p);
                  int $i$f$cache = 0;
                  Object it$iv = $composer.rememberedValue();
                  int var42 = 0;
                  Object var79;
                  if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
                     var79 = it$iv;
                  } else {
                     int var43 = 0;
                     Object value$iv = new Function0<Unit>() {
                        public final void invoke() {
                           $changed$iv.invoke(p.getId());
                        }
                     };
                     $composer.updateRememberedValue(value$iv);
                     var79 = value$iv;
                  }

                  Function0 var73 = (Function0)var79;
                  $composer.endReplaceableGroup();
                  ButtonKt.Button(var73, var34, false, (Shape)var76, var71, (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$PatientScreensKt.INSTANCE.getLambda-2$app_debug(), $composer, 805306416, 484);
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
      }

      ScopeUpdateScope var18 = $composer.endRestartGroup();
      if (var18 != null) {
         var18.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               PatientScreensKt.PatientDetailScreen(patientId, patientRepo, onNavigateToTreatments, onNavigateBack, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   private static final Patient PatientDetailScreen$lambda$1(MutableState<Patient> $patient$delegate) {
      State $this$getValue$iv = (State)$patient$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Patient)$this$getValue$iv.getValue();
   }

   private static final void PatientDetailScreen$lambda$2(MutableState<Patient> $patient$delegate, Patient value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $patient$delegate.setValue(value);
   }
}
