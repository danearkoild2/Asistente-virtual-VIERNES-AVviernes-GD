package com.viernes.mobile.ui.screens;

import android.content.Context;
import android.widget.Toast;
import androidx.compose.foundation.BackgroundKt;
import androidx.compose.foundation.BorderStroke;
import androidx.compose.foundation.ClickableKt;
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
import androidx.compose.foundation.lazy.LazyDslKt;
import androidx.compose.foundation.lazy.LazyItemScope;
import androidx.compose.foundation.lazy.LazyListScope;
import androidx.compose.foundation.lazy.LazyListState;
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
import androidx.compose.runtime.CompositionLocal;
import androidx.compose.runtime.CompositionLocalMap;
import androidx.compose.runtime.CompositionScopedCoroutineScopeCanceller;
import androidx.compose.runtime.EffectsKt;
import androidx.compose.runtime.MutableState;
import androidx.compose.runtime.ProduceStateScope;
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
import androidx.compose.ui.layout.LayoutKt;
import androidx.compose.ui.layout.MeasurePolicy;
import androidx.compose.ui.node.ComposeUiNode;
import androidx.compose.ui.platform.AndroidCompositionLocals_androidKt;
import androidx.compose.ui.semantics.Role;
import androidx.compose.ui.text.TextStyle;
import androidx.compose.ui.text.font.FontFamily;
import androidx.compose.ui.text.font.FontStyle;
import androidx.compose.ui.text.font.FontWeight;
import androidx.compose.ui.text.style.TextAlign;
import androidx.compose.ui.text.style.TextDecoration;
import androidx.compose.ui.unit.Dp;
import androidx.compose.ui.unit.TextUnitKt;
import com.viernes.mobile.data.repository.IntakeRepository;
import com.viernes.mobile.data.repository.MedicationRepository;
import com.viernes.mobile.data.repository.PatientRepository;
import com.viernes.mobile.domain.model.Medication;
import com.viernes.mobile.domain.model.Patient;
import com.viernes.mobile.domain.model.VerificationStatus;
import com.viernes.mobile.notifications.AlarmScheduler;
import com.viernes.mobile.ui.theme.ColorKt;
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
   d1 = {"\u0000H\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\t\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010 \n\u0000\n\u0002\u0010\u000b\u001a#\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\f\u0010\u0004\u001a\b\u0012\u0004\u0012\u00020\u00010\u0005H\u0007¢\u0006\u0002\u0010\u0006\u001a3\u0010\u0007\u001a\u00020\u00012\u0006\u0010\b\u001a\u00020\t2\u0006\u0010\n\u001a\u00020\u000b2\u0006\u0010\f\u001a\u00020\r2\f\u0010\u000e\u001a\b\u0012\u0004\u0012\u00020\u00010\u0005H\u0007¢\u0006\u0002\u0010\u000f\u001aG\u0010\u0010\u001a\u00020\u00012\u0006\u0010\u0011\u001a\u00020\t2\u0006\u0010\u0012\u001a\u00020\u00132\u0006\u0010\n\u001a\u00020\u000b2\u0012\u0010\u0014\u001a\u000e\u0012\u0004\u0012\u00020\t\u0012\u0004\u0012\u00020\u00010\u00152\f\u0010\u000e\u001a\b\u0012\u0004\u0012\u00020\u00010\u0005H\u0007¢\u0006\u0002\u0010\u0016¨\u0006\u0017²\u0006\f\u0010\u0018\u001a\u0004\u0018\u00010\u0019X\u008a\u0084\u0002²\u0006\u0010\u0010\u001a\u001a\b\u0012\u0004\u0012\u00020\u00030\u001bX\u008a\u0084\u0002²\u0006\f\u0010\u0002\u001a\u0004\u0018\u00010\u0003X\u008a\u008e\u0002²\u0006\n\u0010\u001c\u001a\u00020\u001dX\u008a\u008e\u0002"},
   d2 = {"MedicationCard", "", "medication", "Lcom/viernes/mobile/domain/model/Medication;", "onClick", "Lkotlin/Function0;", "(Lcom/viernes/mobile/domain/model/Medication;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "TreatmentDetailScreen", "medicationId", "", "medRepo", "Lcom/viernes/mobile/data/repository/MedicationRepository;", "intakeRepo", "Lcom/viernes/mobile/data/repository/IntakeRepository;", "onNavigateBack", "(JLcom/viernes/mobile/data/repository/MedicationRepository;Lcom/viernes/mobile/data/repository/IntakeRepository;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "TreatmentListScreen", "patientId", "patientRepo", "Lcom/viernes/mobile/data/repository/PatientRepository;", "onNavigateToDetail", "Lkotlin/Function1;", "(JLcom/viernes/mobile/data/repository/PatientRepository;Lcom/viernes/mobile/data/repository/MedicationRepository;Lkotlin/jvm/functions/Function1;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "app_debug", "patient", "Lcom/viernes/mobile/domain/model/Patient;", "medications", "", "isLoading", ""}
)
@SourceDebugExtension({"SMAP\nTreatmentScreens.kt\nKotlin\n*S Kotlin\n*F\n+ 1 TreatmentScreens.kt\ncom/viernes/mobile/ui/screens/TreatmentScreensKt\n+ 2 Composer.kt\nandroidx/compose/runtime/ComposerKt\n+ 3 Dp.kt\nandroidx/compose/ui/unit/DpKt\n+ 4 CompositionLocal.kt\nandroidx/compose/runtime/CompositionLocal\n+ 5 Effects.kt\nandroidx/compose/runtime/EffectsKt\n+ 6 Composables.kt\nandroidx/compose/runtime/ComposablesKt\n+ 7 Effects.kt\nandroidx/compose/runtime/EffectsKt$rememberCoroutineScope$1\n+ 8 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,320:1\n1116#2,6:321\n1116#2,3:334\n1119#2,3:340\n1116#2,6:344\n1116#2,6:350\n154#3:327\n74#4:328\n487#5,4:329\n491#5,2:337\n495#5:343\n25#6:333\n487#7:339\n81#8:356\n81#8:357\n81#8:358\n107#8,2:359\n81#8:361\n107#8,2:362\n*S KotlinDebug\n*F\n+ 1 TreatmentScreens.kt\ncom/viernes/mobile/ui/screens/TreatmentScreensKt\n*L\n114#1:321,6\n178#1:334,3\n178#1:340,3\n179#1:344,6\n180#1:350,6\n116#1:327\n177#1:328\n178#1:329,4\n178#1:337,2\n178#1:343\n178#1:333\n178#1:339\n41#1:356\n44#1:357\n179#1:358\n179#1:359,2\n180#1:361\n180#1:362,2\n*E\n"})
public final class TreatmentScreensKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void TreatmentListScreen(final long patientId, @NotNull final PatientRepository patientRepo, @NotNull final MedicationRepository medRepo, @NotNull final Function1<? super Long, Unit> onNavigateToDetail, @NotNull final Function0<Unit> onNavigateBack, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(patientRepo, "patientRepo");
      Intrinsics.checkNotNullParameter(medRepo, "medRepo");
      Intrinsics.checkNotNullParameter(onNavigateToDetail, "onNavigateToDetail");
      Intrinsics.checkNotNullParameter(onNavigateBack, "onNavigateBack");
      $composer = $composer.startRestartGroup(-1960988230);
      ComposerKt.sourceInformation($composer, "C(TreatmentListScreen)P(3,4!1,2)40@1583L137,43@1788L37,45@1831L2114:TreatmentScreens.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(patientId) ? 4 : 2);
      }

      if (($changed & 112) == 0) {
         $dirty |= $composer.changed(patientRepo) ? 32 : 16;
      }

      if (($changed & 896) == 0) {
         $dirty |= $composer.changed(medRepo) ? 256 : 128;
      }

      if (($changed & 7168) == 0) {
         $dirty |= $composer.changedInstance(onNavigateToDetail) ? 2048 : 1024;
      }

      if (($changed & '\ue000') == 0) {
         $dirty |= $composer.changedInstance(onNavigateBack) ? 16384 : 8192;
      }

      if (($dirty & '뛛') == 9362 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(-1960988230, $dirty, -1, "com.viernes.mobile.ui.screens.TreatmentListScreen (TreatmentScreens.kt:39)");
         }

         final State patient$delegate = SnapshotStateKt.produceState((Object)null, new Function2<ProduceStateScope<Patient>, Continuation<? super Unit>, Object>((Continuation)null) {
            int label;
            // $FF: synthetic field
            private Object L$0;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               Object var4 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
               ProduceStateScope var3;
               Object var10000;
               switch (this.label) {
                  case 0:
                     ResultKt.throwOnFailure($result);
                     ProduceStateScope $this$produceState = (ProduceStateScope)this.L$0;
                     var3 = $this$produceState;
                     PatientRepository var5 = patientRepo;
                     long var10001 = patientId;
                     Continuation var10002 = (Continuation)this;
                     this.L$0 = $this$produceState;
                     this.label = 1;
                     var10000 = var5.getPatientById(var10001, var10002);
                     if (var10000 == var4) {
                        return var4;
                     }
                     break;
                  case 1:
                     var3 = (ProduceStateScope)this.L$0;
                     ResultKt.throwOnFailure($result);
                     var10000 = $result;
                     break;
                  default:
                     throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
               }

               var3.setValue(var10000);
               return Unit.INSTANCE;
            }

            @NotNull
            public final Continuation<Unit> create(@Nullable Object value, @NotNull Continuation<?> $completion) {
               Function2 var3 = new <anonymous constructor>($completion);
               var3.L$0 = value;
               return (Continuation)var3;
            }

            @Nullable
            public final Object invoke(@NotNull ProduceStateScope<Patient> p1, @Nullable Continuation<? super Unit> p2) {
               return ((<undefinedtype>)this.create(p1, p2)).invokeSuspend(Unit.INSTANCE);
            }
         }, $composer, 70);
         final State medications$delegate = SnapshotStateKt.collectAsState(medRepo.getMedicationsForPatient(patientId), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
         ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -2096473218, true, new Function2<Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@Nullable Composer $composer, int $changed) {
               ComposerKt.sourceInformation($composer, "C54@2309L48,47@1872L499:TreatmentScreens.kt#k2q6ai");
               if (($changed & 11) == 2 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-2096473218, $changed, -1, "com.viernes.mobile.ui.screens.TreatmentListScreen.<anonymous> (TreatmentScreens.kt:47)");
                  }

                  AppBarKt.TopAppBar((Function2)ComposableLambdaKt.composableLambda($composer, -1386949574, true, new Function2<Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@Nullable Composer $composer, int $changed) {
                        ComposerKt.sourceInformation($composer, "C48@1909L111:TreatmentScreens.kt#k2q6ai");
                        if (($changed & 11) == 2 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(-1386949574, $changed, -1, "com.viernes.mobile.ui.screens.TreatmentListScreen.<anonymous>.<anonymous> (TreatmentScreens.kt:48)");
                           }

                           String var7;
                           label20: {
                              Patient var10000 = TreatmentScreensKt.TreatmentListScreen$lambda$0(patient$delegate);
                              if (var10000 != null) {
                                 var7 = var10000.getDisplayName();
                                 if (var7 != null) {
                                    break label20;
                                 }
                              }

                              var7 = "Paciente";
                           }

                           String var3 = "Tratamientos — " + var7;
                           FontWeight var4 = FontWeight.Companion.getBold();
                           long var5 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g(var3, (Modifier)null, var5, 0L, (FontStyle)null, var4, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 196992, 0, 131034);
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventEnd();
                           }
                        }

                     }
                  }), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 833996920, true, new Function2<Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@Nullable Composer $composer, int $changed) {
                        ComposerKt.sourceInformation($composer, "C50@2079L167:TreatmentScreens.kt#k2q6ai");
                        if (($changed & 11) == 2 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(833996920, $changed, -1, "com.viernes.mobile.ui.screens.TreatmentListScreen.<anonymous>.<anonymous> (TreatmentScreens.kt:50)");
                           }

                           IconButtonKt.IconButton(onNavigateBack, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$TreatmentScreensKt.INSTANCE.getLambda-1$app_debug(), $composer, 196608, 30);
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
         }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, -61915127, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter(padding, "padding");
               ComposerKt.sourceInformation($composer, "C65@2677L1262,59@2450L1489:TreatmentScreens.kt#k2q6ai");
               int $dirty = $changed;
               if (($changed & 14) == 0) {
                  $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
               }

               if (($dirty & 91) == 18 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-61915127, $dirty, -1, "com.viernes.mobile.ui.screens.TreatmentListScreen.<anonymous> (TreatmentScreens.kt:59)");
                  }

                  Modifier var10000 = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
                  int $this$dp$iv = 16;
                  int $i$f$getDp = 0;
                  var10000 = PaddingKt.padding-VpY3zN4$default(var10000, Dp.constructor-impl((float)$this$dp$iv), 0.0F, 2, (Object)null);
                  Object var10001 = null;
                  Object var10002 = null;
                  boolean var10003 = false;
                  $this$dp$iv = 12;
                  $i$f$getDp = 0;
                  Arrangement.Vertical var10004 = (Arrangement.Vertical)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  Object var10005 = null;
                  Object var10006 = null;
                  boolean var10007 = false;
                  $composer.startReplaceableGroup(-1629805925);
                  ComposerKt.sourceInformation($composer, "CC(remember):TreatmentScreens.kt#9igjgp");
                  boolean invalid$iv = $composer.changed(medications$delegate) | $composer.changed(onNavigateToDetail);
                  final State var8 = medications$delegate;
                  final Function1 var9 = onNavigateToDetail;
                  int $i$f$cache = 0;
                  Object it$iv = $composer.rememberedValue();
                  int var12 = 0;
                  Object var10008;
                  if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
                     var10008 = it$iv;
                  } else {
                     boolean var22 = false;
                     Object var21 = null;
                     Object var20 = null;
                     Arrangement.Vertical var19 = var10004;
                     boolean var18 = false;
                     Object var17 = null;
                     Object var16 = null;
                     Modifier var15 = var10000;
                     int var13 = 0;
                     Function1 value$iv = new Function1<LazyListScope, Unit>() {
                        public final void invoke(@NotNull LazyListScope $this$LazyColumn) {
                           Intrinsics.checkNotNullParameter($this$LazyColumn, "$this$LazyColumn");
                           LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, (Function3)ComposableLambdaKt.composableLambdaInstance(1440910325, true, new Function3<LazyItemScope, Composer, Integer, Unit>() {
                              @Composable
                              @ComposableTarget(
                                 applier = "androidx.compose.ui.UiComposable"
                              )
                              public final void invoke(@NotNull LazyItemScope $this$item, @Nullable Composer $composer, int $changed) {
                                 Intrinsics.checkNotNullParameter($this$item, "$this$item");
                                 ComposerKt.sourceInformation($composer, "C69@2842L10,67@2714L259:TreatmentScreens.kt#k2q6ai");
                                 if (($changed & 81) == 16 && $composer.getSkipping()) {
                                    $composer.skipToGroupEnd();
                                 } else {
                                    if (ComposerKt.isTraceInProgress()) {
                                       ComposerKt.traceEventStart(1440910325, $changed, -1, "com.viernes.mobile.ui.screens.TreatmentListScreen.<anonymous>.<anonymous>.<anonymous>.<anonymous> (TreatmentScreens.kt:67)");
                                    }

                                    String var4 = "Tratamientos y Medicamentos (" + TreatmentScreensKt.TreatmentListScreen$lambda$1(var8).size() + ")";
                                    TextStyle var5 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                                    FontWeight var6 = FontWeight.Companion.getBold();
                                    long var7 = ColorKt.getTextPrimary();
                                    TextKt.Text--4IGK_g(var4, (Modifier)null, var7, 0L, (FontStyle)null, var6, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var5, $composer, 196992, 0, 65498);
                                    if (ComposerKt.isTraceInProgress()) {
                                       ComposerKt.traceEventEnd();
                                    }
                                 }

                              }
                           }), 3, (Object)null);
                           if (TreatmentScreensKt.TreatmentListScreen$lambda$1(var8).isEmpty()) {
                              LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$TreatmentScreensKt.INSTANCE.getLambda-3$app_debug(), 3, (Object)null);
                           } else {
                              List items$iv = TreatmentScreensKt.TreatmentListScreen$lambda$1(var8);
                              Function1 var6 = var9;
                              Function1 key$iv = null;
                              Function1 contentType$iv = TreatmentScreensKt$TreatmentListScreen$2$1$1$invoke$$inlined$items$default$1.INSTANCE;
                              int $i$f$items = 0;
                              $this$LazyColumn.items(items$iv.size(), (Function1)null, new TreatmentScreensKt$TreatmentListScreen$2$1$1$invoke$$inlined$items$default$3(contentType$iv, items$iv), (Function4)ComposableLambdaKt.composableLambdaInstance(-632812321, true, new TreatmentScreensKt$TreatmentListScreen$2$1$1$invoke$$inlined$items$default$4(items$iv, var6)));
                           }

                           LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$TreatmentScreensKt.INSTANCE.getLambda-4$app_debug(), 3, (Object)null);
                        }
                     };
                     var10000 = var15;
                     var10001 = var16;
                     var10002 = var17;
                     var10003 = var18;
                     var10004 = var19;
                     var10005 = var20;
                     var10006 = var21;
                     var10007 = var22;
                     $composer.updateRememberedValue(value$iv);
                     var10008 = value$iv;
                  }

                  Function1 var25 = (Function1)var10008;
                  $composer.endReplaceableGroup();
                  LazyDslKt.LazyColumn(var10000, (LazyListState)var10001, (PaddingValues)var10002, var10003, var10004, (Alignment.Horizontal)var10005, (FlingBehavior)var10006, var10007, var25, $composer, 24576, 238);
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

      ScopeUpdateScope var10000 = $composer.endRestartGroup();
      if (var10000 != null) {
         var10000.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               TreatmentScreensKt.TreatmentListScreen(patientId, patientRepo, medRepo, onNavigateToDetail, onNavigateBack, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void MedicationCard(@NotNull final Medication medication, @NotNull final Function0<Unit> onClick, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(medication, "medication");
      Intrinsics.checkNotNullParameter(onClick, "onClick");
      $composer = $composer.startRestartGroup(-516660891);
      ComposerKt.sourceInformation($composer, "C(MedicationCard)113@4339L13,114@4384L40,110@4254L2290:TreatmentScreens.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(medication) ? 4 : 2);
      }

      if (($changed & 112) == 0) {
         $dirty |= $composer.changedInstance(onClick) ? 32 : 16;
      }

      if (($dirty & 91) == 18 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(-516660891, $dirty, -1, "com.viernes.mobile.ui.screens.MedicationCard (TreatmentScreens.kt:105)");
         }

         boolean isVerified = medication.isVerifiedAndActive();
         final long badgeColor = isVerified ? ColorKt.getStatusConfirmed() : ColorKt.getStatusDelayed();
         final String badgeText = isVerified ? "ACTIVO & VERIFICADO" : "PENDIENTE VERIFICACIÓN";
         Modifier var10000 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
         boolean var10001 = false;
         Object var10002 = null;
         Object var10003 = null;
         $composer.startReplaceableGroup(-508909472);
         ComposerKt.sourceInformation($composer, "CC(remember):TreatmentScreens.kt#9igjgp");
         boolean invalid$iv = ($dirty & 112) == 32;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var15 = 0;
         Object var10004;
         if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
            var10004 = it$iv;
         } else {
            Object var21 = null;
            Object var20 = null;
            boolean var19 = false;
            Modifier var18 = var10000;
            int var16 = 0;
            Function0 value$iv = new Function0<Unit>() {
               public final void invoke() {
                  onClick.invoke();
               }
            };
            var10000 = var18;
            var10001 = var19;
            var10002 = var20;
            var10003 = var21;
            $composer.updateRememberedValue(value$iv);
            var10004 = value$iv;
         }

         Function0 var10 = (Function0)var10004;
         $composer.endReplaceableGroup();
         Modifier var9 = ClickableKt.clickable-XHw0xAI$default(var10000, var10001, (String)var10002, (Role)var10003, var10, 7, (Object)null);
         CardColors var24 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
         invalid$iv = (boolean)12;
         $i$f$cache = 0;
         RoundedCornerShape $this$cache$iv = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)invalid$iv));
         CardKt.Card(var9, (Shape)$this$cache$iv, var24, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, -1169111721, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
               ComposerKt.sourceInformation($composer, "C117@4484L2054:TreatmentScreens.kt#k2q6ai");
               if (($changed & 81) == 16 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-1169111721, $changed, -1, "com.viernes.mobile.ui.screens.MedicationCard.<anonymous> (TreatmentScreens.kt:117)");
                  }

                  Modifier var10000 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 14;
                  int $i$f$getDp = 0;
                  Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                  Medication var7 = medication;
                  long var8 = badgeColor;
                  String var10 = badgeText;
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

                  skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int var28 = 14 & $changed$iv$iv$iv >> 9;
                  int var30 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                  int var31 = 6 | 112 & $changed$iv >> 6;
                  ColumnScope var141 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  int var34 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -1166648145, "C118@4541L876,148@5792L40,149@5845L683:TreatmentScreens.kt#k2q6ai");
                  Modifier modifier$ivxx = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  Arrangement.Horizontal horizontalArrangement$ivx = (Arrangement.Horizontal)Arrangement.INSTANCE.getSpaceBetween();
                  Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                  short $changed$ivxxx = 438;
                  int $i$f$Row = 0;
                  $composer.startReplaceableGroup(693286680);
                  ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                  MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$ivx, verticalAlignment$iv, $composer, 14 & $changed$ivxxx >> 3 | 112 & $changed$ivxxx >> 3);
                  int $changed$iv$ivxx = 112 & $changed$ivxxx << 3;
                  int $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  Function0 factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                  Function3 skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(modifier$ivxx);
                  int $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$ivxx << 9;
                  int $i$f$ReusableComposeNode = 0;
                  if (!($composer.getApplier() instanceof Applier)) {
                     ComposablesKt.invalidApplier();
                  }

                  $composer.startReusableNode();
                  if ($composer.getInserting()) {
                     $composer.createNode(factory$iv$iv$ivxx);
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

                  skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int $changed$ivxxxx = 14 & $changed$iv$iv$ivxx >> 9;
                  int var57 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                  int $changedxx = 6 | 112 & $changed$ivxxx >> 6;
                  RowScope var142 = (RowScope)RowScopeInstance.INSTANCE;
                  int var61 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -423954897, "C125@4862L10,123@4759L242,129@5018L385:TreatmentScreens.kt#k2q6ai");
                  String var62 = var7.getTranscribedName();
                  TextStyle var63 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                  FontWeight var64 = FontWeight.Companion.getBold();
                  long var65 = ColorKt.getViernesPrimaryLight();
                  TextKt.Text--4IGK_g(var62, (Modifier)null, var65, 0L, (FontStyle)null, var64, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var63, $composer, 196992, 0, 65498);
                  Modifier var143 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 4;
                  int $i$f$getDp = 0;
                  var143 = BackgroundKt.background-bw27NRU$default(ClipKt.clip(var143, (Shape)RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv))), Color.copy-wmQWz5c$default(var8, 0.2F, 0.0F, 0.0F, 0.0F, 14, (Object)null), (Shape)null, 2, (Object)null);
                  $this$dp$iv = 6;
                  $i$f$getDp = 0;
                  float var10001 = Dp.constructor-impl((float)$this$dp$iv);
                  $this$dp$iv = 2;
                  $i$f$getDp = 0;
                  Modifier var130 = PaddingKt.padding-VpY3zN4(var143, var10001, Dp.constructor-impl((float)$this$dp$iv));
                  byte $changed$ivxxxxx = 0;
                  int $i$f$Box = 0;
                  $composer.startReplaceableGroup(733328855);
                  ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
                  Alignment contentAlignment$iv = Alignment.Companion.getTopStart();
                  boolean propagateMinConstraints$iv = false;
                  MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(contentAlignment$iv, propagateMinConstraints$iv, $composer, 14 & $changed$ivxxxxx >> 3 | 112 & $changed$ivxxxxx >> 3);
                  int $changed$iv$ivxxx = 112 & $changed$ivxxxxx << 3;
                  int $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  Function0 factory$iv$iv$ivxxx = ComposeUiNode.Companion.getConstructor();
                  Function3 skippableUpdate$iv$iv$ivxxx = LayoutKt.modifierMaterializerOf(var130);
                  int $changed$iv$iv$ivxxx = 6 | 7168 & $changed$iv$ivxxx << 9;
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

                  skippableUpdate$iv$iv$ivxxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int var84 = 14 & $changed$iv$iv$ivxxx >> 9;
                  int var86 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                  int var87 = 6 | 112 & $changed$ivxxxxx >> 6;
                  BoxScope var145 = (BoxScope)BoxScopeInstance.INSTANCE;
                  int var90 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 1815852538, "C135@5295L90:TreatmentScreens.kt#k2q6ai");
                  TextKt.Text--4IGK_g(var10, (Modifier)null, var8, TextUnitKt.getSp(11), (FontStyle)null, FontWeight.Companion.getBold(), (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 199680, 0, 131026);
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
                  $composer.startReplaceableGroup(-868890964);
                  ComposerKt.sourceInformation($composer, "140@5499L40,143@5683L10,141@5556L208");
                  CharSequence $this$dp$ivx = (CharSequence)var7.getActiveIngredient();
                  if ($this$dp$ivx != null && !StringsKt.isBlank($this$dp$ivx)) {
                     Modifier var146 = (Modifier)Modifier.Companion;
                     int $this$dp$iv = 4;
                     int $i$f$getDp = 0;
                     SpacerKt.Spacer(SizeKt.height-3ABfNKs(var146, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                     String modifier$ivx = "Principio Activo: " + var7.getActiveIngredient();
                     TextStyle $i$f$getDpxx = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                     long var91 = ColorKt.getTextSecondary();
                     TextKt.Text--4IGK_g(modifier$ivx, (Modifier)null, var91, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, $i$f$getDpxx, $composer, 384, 0, 65530);
                  }

                  $composer.endReplaceableGroup();
                  Modifier var147 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 6;
                  int $i$f$getDp = 0;
                  SpacerKt.Spacer(SizeKt.height-3ABfNKs(var147, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                  Modifier var101 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  Arrangement.Horizontal var105 = (Arrangement.Horizontal)Arrangement.INSTANCE.getSpaceBetween();
                  $changed$ivxxx = 54;
                  $i$f$Row = 0;
                  $composer.startReplaceableGroup(693286680);
                  ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                  verticalAlignment$iv = Alignment.Companion.getTop();
                  measurePolicy$iv = RowKt.rowMeasurePolicy(var105, verticalAlignment$iv, $composer, 14 & $changed$ivxxx >> 3 | 112 & $changed$ivxxx >> 3);
                  $changed$iv$ivxx = 112 & $changed$ivxxx << 3;
                  $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                  skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(var101);
                  $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$ivxx << 9;
                  $i$f$ReusableComposeNode = 0;
                  if (!($composer.getApplier() instanceof Applier)) {
                     ComposablesKt.invalidApplier();
                  }

                  $composer.startReusableNode();
                  if ($composer.getInserting()) {
                     $composer.createNode(factory$iv$iv$ivxx);
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

                  skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  $changed$ivxxxx = 14 & $changed$iv$iv$ivxx >> 9;
                  var57 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                  $changedxx = 6 | 112 & $changed$ivxxx >> 6;
                  RowScope var148 = (RowScope)RowScopeInstance.INSTANCE;
                  var61 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -422728816, "C155@6166L10,153@5999L246,160@6433L10,158@6262L252:TreatmentScreens.kt#k2q6ai");
                  String var149 = var7.getPrescribedDose();
                  if (var149 == null) {
                     var149 = var7.getIndicatedQuantity();
                     if (var149 == null) {
                        var149 = "No especificada";
                     }
                  }

                  String var131 = "Dosis: " + var149;
                  TextStyle var137 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                  long var93 = ColorKt.getTextPrimary();
                  TextKt.Text--4IGK_g(var131, (Modifier)null, var93, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var137, $composer, 384, 0, 65530);
                  var149 = var7.getExactScheduleHours();
                  if (var149 == null) {
                     var149 = var7.getTranscribedSchedules();
                     if (var149 == null) {
                        var149 = "Sin fijar";
                     }
                  }

                  var131 = "Horarios: " + var149;
                  var137 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                  var93 = ColorKt.getTextSecondary();
                  TextKt.Text--4IGK_g(var131, (Modifier)null, var93, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var137, $composer, 384, 0, 65530);
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
         }), $composer, 196608, 24);
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventEnd();
         }
      }

      ScopeUpdateScope var27 = $composer.endRestartGroup();
      if (var27 != null) {
         var27.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               TreatmentScreensKt.MedicationCard(medication, onClick, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void TreatmentDetailScreen(final long medicationId, @NotNull final MedicationRepository medRepo, @NotNull final IntakeRepository intakeRepo, @NotNull final Function0<Unit> onNavigateBack, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(medRepo, "medRepo");
      Intrinsics.checkNotNullParameter(intakeRepo, "intakeRepo");
      Intrinsics.checkNotNullParameter(onNavigateBack, "onNavigateBack");
      $composer = $composer.startRestartGroup(-38038923);
      ComposerKt.sourceInformation($composer, "C(TreatmentDetailScreen)P(2,1)176@6786L7,177@6819L24,178@6866L46,179@6934L33,181@6973L123,186@7102L6697:TreatmentScreens.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(medicationId) ? 4 : 2);
      }

      if (($changed & 112) == 0) {
         $dirty |= $composer.changed(medRepo) ? 32 : 16;
      }

      if (($changed & 896) == 0) {
         $dirty |= $composer.changed(intakeRepo) ? 256 : 128;
      }

      if (($changed & 7168) == 0) {
         $dirty |= $composer.changedInstance(onNavigateBack) ? 2048 : 1024;
      }

      if (($dirty & 5851) == 1170 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(-38038923, $dirty, -1, "com.viernes.mobile.ui.screens.TreatmentDetailScreen (TreatmentScreens.kt:175)");
         }

         CompositionLocal this_$iv = (CompositionLocal)AndroidCompositionLocals_androidKt.getLocalContext();
         int $changed$iv = 0;
         int $i$f$getCurrent = 0;
         ComposerKt.sourceInformationMarkerStart($composer, 2023513938, "CC:CompositionLocal.kt#9igjgp");
         Object isLoading$delegate = $composer.consume(this_$iv);
         ComposerKt.sourceInformationMarkerEnd($composer);
         final Context context = (Context)isLoading$delegate;
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

         Object var23 = var10000;
         $composer.endReplaceableGroup();
         CompositionScopedCoroutineScopeCanceller wrapper$iv = (CompositionScopedCoroutineScopeCanceller)var23;
         CoroutineScope $i$f$cache = wrapper$iv.getCoroutineScope();
         $composer.endReplaceableGroup();
         final CoroutineScope coroutineScope = $i$f$cache;
         $composer.startReplaceableGroup(314877999);
         ComposerKt.sourceInformation($composer, "CC(remember):TreatmentScreens.kt#9igjgp");
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

         final MutableState isLoading$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         $composer.startReplaceableGroup(314880162);
         ComposerKt.sourceInformation($composer, "CC(remember):TreatmentScreens.kt#9igjgp");
         $i$f$cache = 0;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         invalid$iv$iv$iv = (boolean)0;
         if (it$iv == Composer.Companion.getEmpty()) {
            $i$f$cache = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default(true, (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState isLoading$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         EffectsKt.LaunchedEffect(medicationId, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
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
                     var2 = isLoading$delegate;
                     MedicationRepository var4 = medRepo;
                     long var10001 = medicationId;
                     Continuation var10002 = (Continuation)this;
                     this.L$0 = var2;
                     this.label = 1;
                     var10000 = var4.getMedicationById(var10001, var10002);
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

               TreatmentScreensKt.TreatmentDetailScreen$lambda$5(var2, (Medication)var10000);
               TreatmentScreensKt.TreatmentDetailScreen$lambda$8(isLoading$delegate, false);
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
         ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 650648625, true, new Function2<Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@Nullable Composer $composer, int $changed) {
               ComposerKt.sourceInformation($composer, "C195@7550L48,188@7143L469:TreatmentScreens.kt#k2q6ai");
               if (($changed & 11) == 2 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(650648625, $changed, -1, "com.viernes.mobile.ui.screens.TreatmentDetailScreen.<anonymous> (TreatmentScreens.kt:188)");
                  }

                  AppBarKt.TopAppBar(ComposableSingletons$TreatmentScreensKt.INSTANCE.getLambda-5$app_debug(), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 766594551, true, new Function2<Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@Nullable Composer $composer, int $changed) {
                        ComposerKt.sourceInformation($composer, "C191@7320L167:TreatmentScreens.kt#k2q6ai");
                        if (($changed & 11) == 2 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(766594551, $changed, -1, "com.viernes.mobile.ui.screens.TreatmentDetailScreen.<anonymous>.<anonymous> (TreatmentScreens.kt:191)");
                           }

                           IconButtonKt.IconButton(onNavigateBack, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$TreatmentScreensKt.INSTANCE.getLambda-6$app_debug(), $composer, 196608, 30);
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
         }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, -1036722362, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter(padding, "padding");
               ComposerKt.sourceInformation($composer, "C213@8155L21,208@7986L5807:TreatmentScreens.kt#k2q6ai");
               int $dirty = $changed;
               if (($changed & 14) == 0) {
                  $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
               }

               if (($dirty & 91) == 18 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-1036722362, $dirty, -1, "com.viernes.mobile.ui.screens.TreatmentDetailScreen.<anonymous> (TreatmentScreens.kt:200)");
                  }

                  final Medication med = TreatmentScreensKt.TreatmentDetailScreen$lambda$4(isLoading$delegate);
                  $composer.startReplaceableGroup(-1729446848);
                  ComposerKt.sourceInformation($composer, "202@7764L174");
                  if (TreatmentScreensKt.TreatmentDetailScreen$lambda$7(isLoading$delegate) || med == null) {
                     Modifier modifier$iv = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
                     Alignment verticalArrangement$iv = Alignment.Companion.getCenter();
                     int $changed$iv = 48;
                     int $i$f$Box = 0;
                     $composer.startReplaceableGroup(733328855);
                     ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
                     boolean propagateMinConstraints$iv = false;
                     MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(verticalArrangement$iv, propagateMinConstraints$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                     int var53 = 112 & $changed$iv << 3;
                     int $i$f$Layout = 0;
                     $composer.startReplaceableGroup(-1323940314);
                     ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                     int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                     CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                     Function0 measurePolicy$ivx = ComposeUiNode.Companion.getConstructor();
                     Function3 $changed$iv$ivx = LayoutKt.modifierMaterializerOf(modifier$iv);
                     int $i$f$Layoutx = 6 | 7168 & var53 << 9;
                     int $i$f$ReusableComposeNode = 0;
                     if (!($composer.getApplier() instanceof Applier)) {
                        ComposablesKt.invalidApplier();
                     }

                     $composer.startReusableNode();
                     if ($composer.getInserting()) {
                        $composer.createNode(measurePolicy$ivx);
                     } else {
                        $composer.useNode();
                     }

                     Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                     int factory$iv$iv$ivx = 0;
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                     Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                     Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                     int $changed$iv$iv$ivx = 0;
                     int $this$Layout_u24lambda_u240$iv$ivx = 0;
                     if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                        $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                        $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                     }

                     $changed$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $i$f$Layoutx >> 3);
                     $composer.startReplaceableGroup(2058660585);
                     int var66 = 14 & $i$f$Layoutx >> 9;
                     int var67 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                     int var29 = 6 | 112 & $changed$iv >> 6;
                     BoxScope var82 = (BoxScope)BoxScopeInstance.INSTANCE;
                     int var32 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, 2076272947, "C203@7875L49:TreatmentScreens.kt#k2q6ai");
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
                  Modifier $this$dp$iv = ScrollKt.verticalScroll$default(PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), ScrollKt.rememberScrollState(0, $composer, 0, 1), false, (FlingBehavior)null, false, 14, (Object)null);
                  $i$f$getDp = 14;
                  int $i$f$getDp = 0;
                  Arrangement.Vertical $this$dp$ivx = (Arrangement.Vertical)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                  final CoroutineScope $changed$iv = coroutineScope;
                  final MedicationRepository $i$f$Box = medRepo;
                  final IntakeRepository measurePolicy$iv = intakeRepo;
                  final Context $changed$iv$iv = context;
                  final MutableState $i$f$Layout = isLoading$delegate;
                  int $changed$iv = 48;
                  int $i$f$Column = 0;
                  $composer.startReplaceableGroup(-483455358);
                  ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                  Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
                  MeasurePolicy measurePolicy$iv = ColumnKt.columnMeasurePolicy($this$dp$ivx, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                  int skippableUpdate$iv$iv$iv = 112 & $changed$iv << 3;
                  int $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  Function0 var21 = ComposeUiNode.Companion.getConstructor();
                  Function3 block$iv$iv$iv = LayoutKt.modifierMaterializerOf($this$dp$iv);
                  int var23 = 6 | 7168 & skippableUpdate$iv$iv$iv << 9;
                  int $i$f$ReusableComposeNode = 0;
                  if (!($composer.getApplier() instanceof Applier)) {
                     ComposablesKt.invalidApplier();
                  }

                  $composer.startReusableNode();
                  if ($composer.getInserting()) {
                     $composer.createNode(var21);
                  } else {
                     $composer.useNode();
                  }

                  Composer $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                  int $changed$ivxx = 0;
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                  Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                  int var28 = 0;
                  int $composer = 0;
                  if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                     $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                     $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                  }

                  block$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & var23 >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int $this$invoke_u24lambda_u240 = 14 & var23 >> 9;
                  int var33 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                  int var34 = 6 | 112 & $changed$iv >> 6;
                  ColumnScope var80 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  int var37 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 2076829366, "C218@8361L40,216@8265L2131,262@10542L44,260@10446L1202:TreatmentScreens.kt#k2q6ai");
                  Modifier var38 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  CardColors var39 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  int $this$dp$iv = 16;
                  int $i$f$getDp = 0;
                  RoundedCornerShape var42 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var38, (Shape)var42, var39, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 283429678, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                        Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                        ComposerKt.sourceInformation($composer, "C221@8485L1897:TreatmentScreens.kt#k2q6ai");
                        if (($changed & 81) == 16 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(283429678, $changed, -1, "com.viernes.mobile.ui.screens.TreatmentDetailScreen.<anonymous>.<anonymous>.<anonymous> (TreatmentScreens.kt:221)");
                           }

                           Modifier var10000 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 16;
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
                           ColumnScope var60 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int var31 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -1637673520, "C224@8654L10,222@8550L258,228@8829L40,231@9037L10,229@8890L237,236@9297L10,234@9148L239,241@9551L10,239@9408L233,246@9815L10,244@9662L243,249@9926L40,252@10163L10,250@9987L377:TreatmentScreens.kt#k2q6ai");
                           String var32 = var7.getTranscribedName();
                           TextStyle var33 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getHeadlineMedium();
                           FontWeight var34 = FontWeight.Companion.getBold();
                           long var35 = ColorKt.getViernesPrimaryLight();
                           TextKt.Text--4IGK_g(var32, (Modifier)null, var35, 0L, (FontStyle)null, var34, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var33, $composer, 196992, 0, 65498);
                           Modifier var61 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 4;
                           int $i$f$getDp = 0;
                           SpacerKt.Spacer(SizeKt.height-3ABfNKs(var61, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                           String var62 = var7.getCommercialName();
                           if (var62 == null) {
                              var62 = "No especificado";
                           }

                           String var42 = "Nombre Comercial: " + var62;
                           TextStyle var49 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodyMedium();
                           long var37 = ColorKt.getTextSecondary();
                           TextKt.Text--4IGK_g(var42, (Modifier)null, var37, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var49, $composer, 384, 0, 65530);
                           var62 = var7.getActiveIngredient();
                           if (var62 == null) {
                              var62 = "No especificado";
                           }

                           var42 = "Principio Activo: " + var62;
                           var49 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodyMedium();
                           var37 = ColorKt.getTextSecondary();
                           TextKt.Text--4IGK_g(var42, (Modifier)null, var37, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var49, $composer, 384, 0, 65530);
                           var62 = var7.getConcentration();
                           if (var62 == null) {
                              var62 = "No especificada";
                           }

                           var42 = "Concentración: " + var62;
                           var49 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodyMedium();
                           var37 = ColorKt.getTextSecondary();
                           TextKt.Text--4IGK_g(var42, (Modifier)null, var37, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var49, $composer, 384, 0, 65530);
                           var62 = var7.getPharmaceuticalForm();
                           if (var62 == null) {
                              var62 = "Tabletas / Oral";
                           }

                           var42 = "Forma Farmacéutica: " + var62;
                           var49 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodyMedium();
                           var37 = ColorKt.getTextSecondary();
                           TextKt.Text--4IGK_g(var42, (Modifier)null, var37, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var49, $composer, 384, 0, 65530);
                           Modifier var66 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 8;
                           int $i$f$getDp = 0;
                           SpacerKt.Spacer(SizeKt.height-3ABfNKs(var66, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                           String var67 = var7.getExactScheduleHours();
                           if (var67 == null) {
                              var67 = "Ninguno (solo periodos informativos)";
                           }

                           String var47 = "Horarios Confirmados: " + var67;
                           TextStyle var54 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleSmall();
                           var34 = FontWeight.Companion.getBold();
                           var35 = var7.getExactScheduleHours() != null ? ColorKt.getStatusConfirmed() : ColorKt.getStatusPending();
                           TextKt.Text--4IGK_g(var47, (Modifier)null, var35, 0L, (FontStyle)null, var34, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var54, $composer, 196608, 0, 65498);
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
                  var38 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  var39 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceElevated(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  $this$dp$iv = 12;
                  $i$f$getDp = 0;
                  var42 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var38, (Shape)var42, var39, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, -1013892251, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                        Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                        ComposerKt.sourceInformation($composer, "C265@10670L964:TreatmentScreens.kt#k2q6ai");
                        if (($changed & 81) == 16 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(-1013892251, $changed, -1, "com.viernes.mobile.ui.screens.TreatmentDetailScreen.<anonymous>.<anonymous>.<anonymous> (TreatmentScreens.kt:265)");
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
                           ColumnScope var43 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int var31 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -1635534923, "C266@10735L275,271@11031L40,277@11527L10,272@11092L524:TreatmentScreens.kt#k2q6ai");
                           String var44 = var7.getVerificationStatus().getValue();
                           String var32 = "Estado de Verificación Clínica: " + var44;
                           FontWeight var33 = FontWeight.Companion.getBold();
                           long var34 = var7.isVerifiedAndActive() ? ColorKt.getStatusConfirmed() : ColorKt.getStatusDelayed();
                           TextKt.Text--4IGK_g(var32, (Modifier)null, var34, 0L, (FontStyle)null, var33, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 196608, 0, 131034);
                           Modifier var45 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 4;
                           int $i$f$getDp = 0;
                           SpacerKt.Spacer(SizeKt.height-3ABfNKs(var45, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                           String var39 = var7.isVerifiedAndActive() ? "Este tratamiento ha sido verificado y está autorizado para generar recordatorios y órdenes de toma." : "ADVERTENCIA DE SEGURIDAD: Este tratamiento NO está verificado. Requiere confirmación clínica antes de activar recordatorios exactos.";
                           TextStyle var41 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                           var34 = ColorKt.getTextSecondary();
                           TextKt.Text--4IGK_g(var39, (Modifier)null, var34, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var41, $composer, 384, 0, 65530);
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
                  $composer.startReplaceableGroup(1591122254);
                  ComposerKt.sourceInformation($composer, "308@13404L45,285@11768L2001");
                  if (!med.isVerifiedAndActive()) {
                     Modifier var81 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                     int $this$dp$iv = 50;
                     int $i$f$getDp = 0;
                     var38 = SizeKt.height-3ABfNKs(var81, Dp.constructor-impl((float)$this$dp$iv));
                     ButtonColors var72 = ButtonDefaults.INSTANCE.buttonColors-ro_MJ88(ColorKt.getViernesPrimary(), 0L, 0L, 0L, $composer, 6 | ButtonDefaults.$stable << 12, 14);
                     $this$dp$iv = 12;
                     $i$f$getDp = 0;
                     RoundedCornerShape var79 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                     ButtonKt.Button(new Function0<Unit>() {
                        public final void invoke() {
                           BuildersKt.launch$default($changed$iv, (CoroutineContext)null, (CoroutineStart)null, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
                              Object L$0;
                              int label;

                              @Nullable
                              public final Object invokeSuspend(@NotNull Object $result) {
                                 MutableState var3;
                                 Object var10000;
                                 label92: {
                                    Object var4;
                                    label77: {
                                       label76: {
                                          List generated;
                                          label83: {
                                             label87: {
                                                var4 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                                                switch (this.label) {
                                                   case 0:
                                                      ResultKt.throwOnFailure($result);
                                                      MedicationRepository var14 = $i$f$Box;
                                                      long var20 = med.getId();
                                                      Continuation var10003 = (Continuation)this;
                                                      this.label = 1;
                                                      if (var14.verifyAndActivate(var20, "profesional_cuidador", var10003) == var4) {
                                                         return var4;
                                                      }
                                                      break;
                                                   case 1:
                                                      ResultKt.throwOnFailure($result);
                                                      break;
                                                   case 2:
                                                      try {
                                                         ResultKt.throwOnFailure($result);
                                                         var10000 = $result;
                                                         break label87;
                                                      } catch (Exception var8) {
                                                         var12 = var8;
                                                         boolean var19 = false;
                                                         break label76;
                                                      }
                                                   case 3:
                                                      generated = (List)this.L$0;

                                                      try {
                                                         ResultKt.throwOnFailure($result);
                                                         break label83;
                                                      } catch (Exception var9) {
                                                         var12 = var9;
                                                         boolean var10001 = false;
                                                         break label76;
                                                      }
                                                   case 4:
                                                      var3 = (MutableState)this.L$0;
                                                      ResultKt.throwOnFailure($result);
                                                      var10000 = $result;
                                                      break label92;
                                                   default:
                                                      throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                                                }

                                                CharSequence var10 = (CharSequence)med.getExactScheduleHours();
                                                if (var10 == null || StringsKt.isBlank(var10)) {
                                                   Toast.makeText($changed$iv$iv, (CharSequence)"Tratamiento verificado. Agregue horarios exactos para activar recordatorios.", 1).show();
                                                   break label77;
                                                }

                                                try {
                                                   IntakeRepository var15 = measurePolicy$iv;
                                                   Medication var22 = Medication.copy$default(med, 0L, 0L, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, (String)null, VerificationStatus.ACTIVE, "active", (String)null, (String)null, (String)null, (String)null, false, (String)null, (String)null, 266862591, (Object)null);
                                                   Continuation var28 = (Continuation)this;
                                                   this.label = 2;
                                                   var10000 = var15.generateIntakesForMedication(var22, 7, var28);
                                                } catch (Exception var7) {
                                                   var12 = var7;
                                                   boolean var21 = false;
                                                   break label76;
                                                }

                                                if (var10000 == var4) {
                                                   return var4;
                                                }
                                             }

                                             try {
                                                generated = (List)var10000;
                                                AlarmScheduler var16 = AlarmScheduler.INSTANCE;
                                                Context var24 = $changed$iv$iv;
                                                Continuation var10002 = (Continuation)this;
                                                this.L$0 = generated;
                                                this.label = 3;
                                                var10000 = var16.rescheduleAllPendingAlarms(var24, var10002);
                                             } catch (Exception var6) {
                                                var12 = var6;
                                                boolean var23 = false;
                                                break label76;
                                             }

                                             if (var10000 == var4) {
                                                return var4;
                                             }
                                          }

                                          try {
                                             Toast.makeText($changed$iv$iv, (CharSequence)("Tratamiento verificado. " + generated.size() + " tomas programadas con alarmas exactas."), 1).show();
                                             break label77;
                                          } catch (Exception var5) {
                                             var12 = var5;
                                             boolean var25 = false;
                                          }
                                       }

                                       Exception e = var12;
                                       Toast.makeText($changed$iv$iv, (CharSequence)("Tratamiento verificado: " + e.getMessage()), 0).show();
                                    }

                                    var3 = $i$f$Layout;
                                    MedicationRepository var18 = $i$f$Box;
                                    long var26 = med.getId();
                                    Continuation var27 = (Continuation)this;
                                    this.L$0 = var3;
                                    this.label = 4;
                                    var10000 = var18.getMedicationById(var26, var27);
                                    if (var10000 == var4) {
                                       return var4;
                                    }
                                 }

                                 TreatmentScreensKt.TreatmentDetailScreen$lambda$5(var3, (Medication)var10000);
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
                     }, var38, false, (Shape)var79, var72, (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$TreatmentScreensKt.INSTANCE.getLambda-7$app_debug(), $composer, 805306416, 484);
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
         }), $composer, 806879280, 445);
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventEnd();
         }
      }

      ScopeUpdateScope var46 = $composer.endRestartGroup();
      if (var46 != null) {
         var46.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               TreatmentScreensKt.TreatmentDetailScreen(medicationId, medRepo, intakeRepo, onNavigateBack, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   private static final Patient TreatmentListScreen$lambda$0(State<Patient> $patient$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Patient)$patient$delegate.getValue();
   }

   private static final List<Medication> TreatmentListScreen$lambda$1(State<? extends List<Medication>> $medications$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$medications$delegate.getValue();
   }

   private static final Medication TreatmentDetailScreen$lambda$4(MutableState<Medication> $medication$delegate) {
      State $this$getValue$iv = (State)$medication$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Medication)$this$getValue$iv.getValue();
   }

   private static final void TreatmentDetailScreen$lambda$5(MutableState<Medication> $medication$delegate, Medication value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $medication$delegate.setValue(value);
   }

   private static final boolean TreatmentDetailScreen$lambda$7(MutableState<Boolean> $isLoading$delegate) {
      State $this$getValue$iv = (State)$isLoading$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Boolean)$this$getValue$iv.getValue();
   }

   private static final void TreatmentDetailScreen$lambda$8(MutableState<Boolean> $isLoading$delegate, boolean value) {
      Object var3 = null;
      Object var4 = null;
      Object value$iv = value;
      int $i$f$setValue = 0;
      $isLoading$delegate.setValue(value$iv);
   }
}
