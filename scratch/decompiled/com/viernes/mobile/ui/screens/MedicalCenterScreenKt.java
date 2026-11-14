package com.viernes.mobile.ui.screens;

import androidx.compose.foundation.BackgroundKt;
import androidx.compose.foundation.BorderStroke;
import androidx.compose.foundation.ClickableKt;
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
import androidx.compose.material.icons.Icons;
import androidx.compose.material.icons.filled.CalendarMonthKt;
import androidx.compose.material.icons.filled.ChevronRightKt;
import androidx.compose.material.icons.filled.HistoryKt;
import androidx.compose.material.icons.filled.InventoryKt;
import androidx.compose.material.icons.filled.MedicationKt;
import androidx.compose.material.icons.filled.WarningKt;
import androidx.compose.material3.AppBarKt;
import androidx.compose.material3.ButtonColors;
import androidx.compose.material3.ButtonElevation;
import androidx.compose.material3.ButtonKt;
import androidx.compose.material3.CardColors;
import androidx.compose.material3.CardDefaults;
import androidx.compose.material3.CardElevation;
import androidx.compose.material3.CardKt;
import androidx.compose.material3.ChipKt;
import androidx.compose.material3.FilterChipDefaults;
import androidx.compose.material3.IconButtonColors;
import androidx.compose.material3.IconButtonKt;
import androidx.compose.material3.IconKt;
import androidx.compose.material3.MaterialTheme;
import androidx.compose.material3.ScaffoldKt;
import androidx.compose.material3.SelectableChipElevation;
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
import androidx.compose.ui.draw.ClipKt;
import androidx.compose.ui.graphics.Color;
import androidx.compose.ui.graphics.Shape;
import androidx.compose.ui.graphics.vector.ImageVector;
import androidx.compose.ui.layout.LayoutKt;
import androidx.compose.ui.layout.MeasurePolicy;
import androidx.compose.ui.node.ComposeUiNode;
import androidx.compose.ui.semantics.Role;
import androidx.compose.ui.text.TextStyle;
import androidx.compose.ui.text.font.FontFamily;
import androidx.compose.ui.text.font.FontStyle;
import androidx.compose.ui.text.font.FontWeight;
import androidx.compose.ui.text.style.TextAlign;
import androidx.compose.ui.text.style.TextDecoration;
import androidx.compose.ui.unit.Dp;
import androidx.compose.ui.unit.TextUnitKt;
import com.viernes.mobile.data.repository.AppointmentRepository;
import com.viernes.mobile.data.repository.IntakeRepository;
import com.viernes.mobile.data.repository.InventoryRepository;
import com.viernes.mobile.data.repository.MedicationRepository;
import com.viernes.mobile.data.repository.PatientRepository;
import com.viernes.mobile.data.repository.RefillRepository;
import com.viernes.mobile.domain.model.Intake;
import com.viernes.mobile.domain.model.IntakeStatus;
import com.viernes.mobile.domain.model.Inventory;
import com.viernes.mobile.domain.model.MedicalAppointment;
import com.viernes.mobile.domain.model.Medication;
import com.viernes.mobile.domain.model.Patient;
import com.viernes.mobile.domain.model.Refill;
import com.viernes.mobile.ui.theme.ColorKt;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.collections.CollectionsKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.Boxing;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.functions.Function3;
import kotlin.jvm.functions.Function4;
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
   d1 = {"\u0000\u0082\u0001\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010\u000e\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\u001a#\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\f\u0010\u0004\u001a\b\u0012\u0004\u0012\u00020\u00010\u0005H\u0007¢\u0006\u0002\u0010\u0006\u001aQ\u0010\u0007\u001a\u00020\u00012\u0006\u0010\b\u001a\u00020\t2\u0006\u0010\n\u001a\u00020\u000b2\u0006\u0010\f\u001a\u00020\r2\u0006\u0010\u000e\u001a\u00020\u000f2\u0006\u0010\u0010\u001a\u00020\u00112\u0006\u0010\u0012\u001a\u00020\u00132\u0012\u0010\u0014\u001a\u000e\u0012\u0004\u0012\u00020\u0016\u0012\u0004\u0012\u00020\u00010\u0015H\u0007¢\u0006\u0002\u0010\u0017\u001aB\u0010\u0018\u001a\u00020\u00012\u0006\u0010\u0019\u001a\u00020\u00162\u0006\u0010\u001a\u001a\u00020\u001b2\u0006\u0010\u001c\u001a\u00020\u001d2\b\b\u0002\u0010\u001e\u001a\u00020\u001f2\f\u0010\u0004\u001a\b\u0012\u0004\u0012\u00020\u00010\u0005H\u0007ø\u0001\u0000¢\u0006\u0004\b \u0010!\u0082\u0002\u0007\n\u0005\b¡\u001e0\u0001¨\u0006\"²\u0006\u0010\u0010#\u001a\b\u0012\u0004\u0012\u00020%0$X\u008a\u0084\u0002²\u0006\f\u0010&\u001a\u0004\u0018\u00010'X\u008a\u008e\u0002²\u0006\u0010\u0010(\u001a\b\u0012\u0004\u0012\u00020\u00030$X\u008a\u0084\u0002²\u0006\u0010\u0010)\u001a\b\u0012\u0004\u0012\u00020*0$X\u008a\u0084\u0002²\u0006\u0010\u0010+\u001a\b\u0012\u0004\u0012\u00020,0$X\u008a\u0084\u0002²\u0006\u0010\u0010-\u001a\b\u0012\u0004\u0012\u00020.0$X\u008a\u0084\u0002²\u0006\u0010\u0010/\u001a\b\u0012\u0004\u0012\u0002000$X\u008a\u0084\u0002"},
   d2 = {"IntakeMedicalRow", "", "intake", "Lcom/viernes/mobile/domain/model/Intake;", "onClick", "Lkotlin/Function0;", "(Lcom/viernes/mobile/domain/model/Intake;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "MedicalCenterScreen", "patientRepo", "Lcom/viernes/mobile/data/repository/PatientRepository;", "medRepo", "Lcom/viernes/mobile/data/repository/MedicationRepository;", "intakeRepo", "Lcom/viernes/mobile/data/repository/IntakeRepository;", "appointmentRepo", "Lcom/viernes/mobile/data/repository/AppointmentRepository;", "refillRepo", "Lcom/viernes/mobile/data/repository/RefillRepository;", "inventoryRepo", "Lcom/viernes/mobile/data/repository/InventoryRepository;", "onNavigate", "Lkotlin/Function1;", "", "(Lcom/viernes/mobile/data/repository/PatientRepository;Lcom/viernes/mobile/data/repository/MedicationRepository;Lcom/viernes/mobile/data/repository/IntakeRepository;Lcom/viernes/mobile/data/repository/AppointmentRepository;Lcom/viernes/mobile/data/repository/RefillRepository;Lcom/viernes/mobile/data/repository/InventoryRepository;Lkotlin/jvm/functions/Function1;Landroidx/compose/runtime/Composer;I)V", "MedicalQuickPill", "label", "icon", "Landroidx/compose/ui/graphics/vector/ImageVector;", "color", "Landroidx/compose/ui/graphics/Color;", "modifier", "Landroidx/compose/ui/Modifier;", "MedicalQuickPill-T042LqI", "(Ljava/lang/String;Landroidx/compose/ui/graphics/vector/ImageVector;JLandroidx/compose/ui/Modifier;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;II)V", "app_debug", "patients", "", "Lcom/viernes/mobile/domain/model/Patient;", "selectedPatientId", "", "intakes", "medications", "Lcom/viernes/mobile/domain/model/Medication;", "appointments", "Lcom/viernes/mobile/domain/model/MedicalAppointment;", "refills", "Lcom/viernes/mobile/domain/model/Refill;", "inventoryList", "Lcom/viernes/mobile/domain/model/Inventory;"}
)
@SourceDebugExtension({"SMAP\nMedicalCenterScreen.kt\nKotlin\n*S Kotlin\n*F\n+ 1 MedicalCenterScreen.kt\ncom/viernes/mobile/ui/screens/MedicalCenterScreenKt\n+ 2 Composer.kt\nandroidx/compose/runtime/ComposerKt\n+ 3 _Collections.kt\nkotlin/collections/CollectionsKt___CollectionsKt\n+ 4 Dp.kt\nandroidx/compose/ui/unit/DpKt\n+ 5 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,308:1\n1116#2,6:309\n1116#2,6:315\n1116#2,6:321\n1116#2,6:330\n1116#2,6:337\n766#3:327\n857#3,2:328\n154#4:336\n154#4:343\n81#5:344\n81#5:345\n107#5,2:346\n81#5:348\n81#5:349\n81#5:350\n81#5:351\n81#5:352\n*S KotlinDebug\n*F\n+ 1 MedicalCenterScreen.kt\ncom/viernes/mobile/ui/screens/MedicalCenterScreenKt\n*L\n42#1:309,6\n44#1:315,6\n51#1:321,6\n242#1:330,6\n294#1:337,6\n59#1:327\n59#1:328,2\n244#1:336\n296#1:343\n41#1:344\n42#1:345\n42#1:346,2\n53#1:348\n54#1:349\n55#1:350\n56#1:351\n57#1:352\n*E\n"})
public final class MedicalCenterScreenKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void MedicalCenterScreen(@NotNull final PatientRepository patientRepo, @NotNull final MedicationRepository medRepo, @NotNull final IntakeRepository intakeRepo, @NotNull final AppointmentRepository appointmentRepo, @NotNull final RefillRepository refillRepo, @NotNull final InventoryRepository inventoryRepo, @NotNull final Function1<? super String, Unit> onNavigate, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(patientRepo, "patientRepo");
      Intrinsics.checkNotNullParameter(medRepo, "medRepo");
      Intrinsics.checkNotNullParameter(intakeRepo, "intakeRepo");
      Intrinsics.checkNotNullParameter(appointmentRepo, "appointmentRepo");
      Intrinsics.checkNotNullParameter(refillRepo, "refillRepo");
      Intrinsics.checkNotNullParameter(inventoryRepo, "inventoryRepo");
      Intrinsics.checkNotNullParameter(onNavigate, "onNavigate");
      $composer = $composer.startRestartGroup(169635600);
      ComposerKt.sourceInformation($composer, "C(MedicalCenterScreen)P(5,3,1!1,6)40@1568L37,41@1635L40,43@1706L135,43@1681L160,50@1913L39,52@2030L37,53@2142L37,54@2264L37,55@2371L37,56@2489L37,60@2605L7848:MedicalCenterScreen.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(patientRepo) ? 4 : 2);
      }

      if (($changed & 112) == 0) {
         $dirty |= $composer.changed(medRepo) ? 32 : 16;
      }

      if (($changed & 896) == 0) {
         $dirty |= $composer.changed(intakeRepo) ? 256 : 128;
      }

      if (($changed & 7168) == 0) {
         $dirty |= $composer.changed(appointmentRepo) ? 2048 : 1024;
      }

      if (($changed & '\ue000') == 0) {
         $dirty |= $composer.changed(refillRepo) ? 16384 : 8192;
      }

      if (($changed & 458752) == 0) {
         $dirty |= $composer.changed(inventoryRepo) ? 131072 : 65536;
      }

      if (($changed & 3670016) == 0) {
         $dirty |= $composer.changedInstance(onNavigate) ? 1048576 : 524288;
      }

      if (($dirty & 2995931) == 599186 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(169635600, $dirty, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen (MedicalCenterScreen.kt:39)");
         }

         final State patients$delegate = SnapshotStateKt.collectAsState(patientRepo.getActivePatients(), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
         $composer.startReplaceableGroup(1330786214);
         ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
         boolean invalid$iv = false;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var17 = 0;
         Object var10000;
         if (it$iv == Composer.Companion.getEmpty()) {
            int var18 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default((Object)null, (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState var12 = (MutableState)var10000;
         $composer.endReplaceableGroup();
         final MutableState selectedPatientId$delegate = var12;
         List var53 = MedicalCenterScreen$lambda$0(patients$delegate);
         $composer.startReplaceableGroup(1330788581);
         ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
         invalid$iv = $composer.changed(patients$delegate);
         $i$f$cache = 0;
         it$iv = $composer.rememberedValue();
         var17 = 0;
         Object var57;
         if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
            var57 = it$iv;
         } else {
            List var30 = var53;
            int var44 = 0;
            Function2 var10001 = new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
               int label;

               @Nullable
               public final Object invokeSuspend(@NotNull Object $result) {
                  IntrinsicsKt.getCOROUTINE_SUSPENDED();
                  switch (this.label) {
                     case 0:
                        ResultKt.throwOnFailure($result);
                        if (MedicalCenterScreenKt.MedicalCenterScreen$lambda$2(var12) == null && !((Collection)MedicalCenterScreenKt.MedicalCenterScreen$lambda$0(patients$delegate)).isEmpty()) {
                           MedicalCenterScreenKt.MedicalCenterScreen$lambda$3(var12, Boxing.boxLong(((Patient)CollectionsKt.first(MedicalCenterScreenKt.MedicalCenterScreen$lambda$0(patients$delegate))).getId()));
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
            var53 = var30;
            Object value$iv = var10001;
            $composer.updateRememberedValue(value$iv);
            var57 = value$iv;
         }

         Function2 var32 = (Function2)var57;
         $composer.endReplaceableGroup();
         EffectsKt.LaunchedEffect(var53, var32, $composer, 72);
         Long var54 = MedicalCenterScreen$lambda$2(selectedPatientId$delegate);
         final long currentPatientId = var54 != null ? var54 : 1L;
         $composer.startReplaceableGroup(1330795109);
         ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
         boolean invalid$iv = false;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var21 = 0;
         Object var55;
         if (it$iv == Composer.Companion.getEmpty()) {
            int var22 = 0;
            Object value$iv = LocalDate.now().toString();
            $composer.updateRememberedValue(value$iv);
            var55 = value$iv;
         } else {
            var55 = it$iv;
         }

         String medications$delegate = (String)var55;
         $composer.endReplaceableGroup();
         Intrinsics.checkNotNull(medications$delegate);
         final String todayStr = medications$delegate;
         final State intakes$delegate = SnapshotStateKt.collectAsState(intakeRepo.getIntakesForDate(currentPatientId, medications$delegate), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
         final State medications$delegate = SnapshotStateKt.collectAsState(medRepo.getMedicationsForPatient(currentPatientId), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
         final State appointments$delegate = SnapshotStateKt.collectAsState(appointmentRepo.getAppointmentsForPatient(currentPatientId), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
         State refills$delegate = SnapshotStateKt.collectAsState(refillRepo.getRefillsForPatient(currentPatientId), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
         final State inventoryList$delegate = SnapshotStateKt.collectAsState(inventoryRepo.getInventoryForPatient(currentPatientId), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
         Iterable $this$filter$iv = (Iterable)MedicalCenterScreen$lambda$7(medications$delegate);
         int $i$f$filter = 0;
         Collection destination$iv$iv = (Collection)(new ArrayList());
         int $i$f$filterTo = 0;

         for(Object element$iv$iv : $this$filter$iv) {
            Medication it = (Medication)element$iv$iv;
            int var29 = 0;
            if (!it.isVerifiedAndActive()) {
               destination$iv$iv.add(element$iv$iv);
            }
         }

         final List unverifiedMeds = (List)destination$iv$iv;
         ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -1898383148, true, new Function2<Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@Nullable Composer $composer, int $changed) {
               ComposerKt.sourceInformation($composer, "C69@3098L48,62@2646L514:MedicalCenterScreen.kt#k2q6ai");
               if (($changed & 11) == 2 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-1898383148, $changed, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen.<anonymous> (MedicalCenterScreen.kt:62)");
                  }

                  AppBarKt.TopAppBar(ComposableSingletons$MedicalCenterScreenKt.INSTANCE.getLambda-1$app_debug(), (Modifier)null, (Function2)null, (Function3)ComposableLambdaKt.composableLambda($composer, 59646277, true, new Function3<RowScope, Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@NotNull RowScope $this$TopAppBar, @Nullable Composer $composer, int $changed) {
                        Intrinsics.checkNotNullParameter($this$TopAppBar, "$this$TopAppBar");
                        ComposerKt.sourceInformation($composer, "C65@2836L49,65@2815L220:MedicalCenterScreen.kt#k2q6ai");
                        if (($changed & 81) == 16 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(59646277, $changed, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen.<anonymous>.<anonymous> (MedicalCenterScreen.kt:65)");
                           }

                           $composer.startReplaceableGroup(-415282867);
                           ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
                           boolean invalid$iv = $composer.changed(onNavigate) | $composer.changed(currentPatientId);
                           final Function1 var7 = onNavigate;
                           final long var8 = currentPatientId;
                           int $i$f$cache = 0;
                           Object it$iv = $composer.rememberedValue();
                           int var12 = 0;
                           Object var10000;
                           if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
                              var10000 = it$iv;
                           } else {
                              int var13 = 0;
                              Object value$iv = new Function0<Unit>() {
                                 public final void invoke() {
                                    var7.invoke("recipe_import/" + var8);
                                 }
                              };
                              $composer.updateRememberedValue(value$iv);
                              var10000 = value$iv;
                           }

                           Function0 var4 = (Function0)var10000;
                           $composer.endReplaceableGroup();
                           IconButtonKt.IconButton(var4, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$MedicalCenterScreenKt.INSTANCE.getLambda-2$app_debug(), $composer, 196608, 30);
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventEnd();
                           }
                        }

                     }
                  }), (WindowInsets)null, TopAppBarDefaults.INSTANCE.topAppBarColors-zjMxDiM(ColorKt.getBackgroundDark(), 0L, 0L, 0L, 0L, $composer, 6 | TopAppBarDefaults.$stable << 15, 30), (TopAppBarScrollBehavior)null, $composer, 3078, 86);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }
               }

            }
         }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, -1510734497, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter(padding, "padding");
               ComposerKt.sourceInformation($composer, "C74@3239L7208:MedicalCenterScreen.kt#k2q6ai");
               int $dirty = $changed;
               if (($changed & 14) == 0) {
                  $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
               }

               if (($dirty & 91) == 18 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-1510734497, $dirty, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen.<anonymous> (MedicalCenterScreen.kt:74)");
                  }

                  Modifier var10000 = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
                  int $this$dp$iv = 16;
                  int $i$f$getDp = 0;
                  var10000 = PaddingKt.padding-VpY3zN4$default(var10000, Dp.constructor-impl((float)$this$dp$iv), 0.0F, 2, (Object)null);
                  $this$dp$iv = 16;
                  $i$f$getDp = 0;
                  LazyDslKt.LazyColumn(var10000, (LazyListState)null, (PaddingValues)null, false, (Arrangement.Vertical)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$this$dp$iv)), (Alignment.Horizontal)null, (FlingBehavior)null, false, new Function1<LazyListScope, Unit>() {
                     public final void invoke(@NotNull LazyListScope $this$LazyColumn) {
                        Intrinsics.checkNotNullParameter($this$LazyColumn, "$this$LazyColumn");
                        LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, (Function3)ComposableLambdaKt.composableLambdaInstance(-1406013109, true, new Function3<LazyItemScope, Composer, Integer, Unit>() {
                           @Composable
                           @ComposableTarget(
                              applier = "androidx.compose.ui.UiComposable"
                           )
                           public final void invoke(@NotNull LazyItemScope $this$item, @Nullable Composer $composer, int $changed) {
                              Intrinsics.checkNotNullParameter($this$item, "$this$item");
                              ComposerKt.sourceInformation($composer, "C83@3613L10,83@3562L92,84@3671L40,85@3728L976:MedicalCenterScreen.kt#k2q6ai");
                              if (($changed & 81) == 16 && $composer.getSkipping()) {
                                 $composer.skipToGroupEnd();
                              } else {
                                 if (ComposerKt.isTraceInProgress()) {
                                    ComposerKt.traceEventStart(-1406013109, $changed, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen.<anonymous>.<anonymous>.<anonymous> (MedicalCenterScreen.kt:83)");
                                 }

                                 TextStyle var4 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getLabelSmall();
                                 long var5 = ColorKt.getTextMuted();
                                 TextKt.Text--4IGK_g("Seleccionar Paciente", (Modifier)null, var5, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var4, $composer, 390, 0, 65530);
                                 Modifier var10000 = (Modifier)Modifier.Companion;
                                 int $this$dp$iv = 6;
                                 int $i$f$getDp = 0;
                                 SpacerKt.Spacer(SizeKt.height-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                                 Modifier var61 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                                 $i$f$getDp = 8;
                                 int $i$f$getDp = 0;
                                 Arrangement.Horizontal var64 = (Arrangement.Horizontal)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                                 State var7 = patients$delegate;
                                 long var8 = currentPatientId;
                                 final MutableState var10 = selectedPatientId$delegate;
                                 int $changed$iv = 54;
                                 int $i$f$Row = 0;
                                 $composer.startReplaceableGroup(693286680);
                                 ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                                 Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getTop();
                                 MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(var64, verticalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                                 int $changed$iv$iv = 112 & $changed$iv << 3;
                                 int $i$f$Layout = 0;
                                 $composer.startReplaceableGroup(-1323940314);
                                 ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                                 int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                                 CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                                 Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                                 Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(var61);
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
                                 ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                                 int var31 = 6 | 112 & $changed$iv >> 6;
                                 Composer $composer = $composer;
                                 RowScope var67 = (RowScope)RowScopeInstance.INSTANCE;
                                 int var34 = 0;
                                 ComposerKt.sourceInformationMarkerStart($composer, 147725015, "C:MedicalCenterScreen.kt#k2q6ai");
                                 $composer.startReplaceableGroup(1113144259);
                                 ComposerKt.sourceInformation($composer, "*93@4115L28,95@4331L307,91@4014L650");
                                 Iterable $this$forEach$iv = (Iterable)MedicalCenterScreenKt.MedicalCenterScreen$lambda$0(var7);
                                 int $i$f$forEach = 0;

                                 for(Object element$iv : $this$forEach$iv) {
                                    final Patient p = (Patient)element$iv;
                                    int var40x = 0;
                                    final boolean isSelected = p.getId() == var8;
                                    boolean var68 = isSelected;
                                    $composer.startReplaceableGroup(152649109);
                                    ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
                                    boolean invalid$iv = $composer.changed(p);
                                    int $i$f$cache = 0;
                                    Object it$iv = $composer.rememberedValue();
                                    int var46 = 0;
                                    Object var10001;
                                    if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
                                       var10001 = it$iv;
                                    } else {
                                       int var48 = 0;
                                       Function0 value$iv = new Function0<Unit>() {
                                          public final void invoke() {
                                             MedicalCenterScreenKt.MedicalCenterScreen$lambda$3(var10, p.getId());
                                          }
                                       };
                                       var68 = isSelected;
                                       $composer.updateRememberedValue(value$iv);
                                       var10001 = value$iv;
                                    }

                                    Function0 var51 = (Function0)var10001;
                                    $composer.endReplaceableGroup();
                                    Function0 var69 = var51;
                                    Function2 var10002 = (Function2)ComposableLambdaKt.composableLambda($composer, -693452378, true, new Function2<Composer, Integer, Unit>() {
                                       @Composable
                                       @ComposableTarget(
                                          applier = "androidx.compose.ui.UiComposable"
                                       )
                                       public final void invoke(@Nullable Composer $composer, int $changed) {
                                          ComposerKt.sourceInformation($composer, "C94@4183L88:MedicalCenterScreen.kt#k2q6ai");
                                          if (($changed & 11) == 2 && $composer.getSkipping()) {
                                             $composer.skipToGroupEnd();
                                          } else {
                                             if (ComposerKt.isTraceInProgress()) {
                                                ComposerKt.traceEventStart(-693452378, $changed, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen.<anonymous>.<anonymous>.<anonymous>.<anonymous>.<anonymous>.<anonymous> (MedicalCenterScreen.kt:94)");
                                             }

                                             TextKt.Text--4IGK_g(p.getDisplayName(), (Modifier)null, 0L, 0L, (FontStyle)null, isSelected ? FontWeight.Companion.getBold() : FontWeight.Companion.getNormal(), (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 0, 0, 131038);
                                             if (ComposerKt.isTraceInProgress()) {
                                                ComposerKt.traceEventEnd();
                                             }
                                          }

                                       }
                                    });
                                    FilterChipDefaults var66 = FilterChipDefaults.INSTANCE;
                                    long var52 = ColorKt.getViernesPrimary();
                                    long var54 = ColorKt.getTextPrimary();
                                    long var56 = ColorKt.getSurfaceDark();
                                    long var58 = ColorKt.getTextSecondary();
                                    ChipKt.FilterChip(var68, var69, var10002, (Modifier)null, false, (Function2)null, (Function2)null, (Shape)null, var66.filterChipColors-XqyqHi0(var56, var58, 0L, 0L, 0L, 0L, 0L, var52, 0L, var54, 0L, 0L, $composer, 817889334, FilterChipDefaults.$stable << 6, 3452), (SelectableChipElevation)null, (BorderStroke)null, (MutableInteractionSource)null, $composer, 384, 0, 3832);
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
                        }), 3, (Object)null);
                        if (!((Collection)unverifiedMeds).isEmpty()) {
                           LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, (Function3)ComposableLambdaKt.composableLambdaInstance(497793616, true, new Function3<LazyItemScope, Composer, Integer, Unit>() {
                              @Composable
                              @ComposableTarget(
                                 applier = "androidx.compose.ui.UiComposable"
                              )
                              public final void invoke(@NotNull LazyItemScope $this$item, @Nullable Composer $composer, int $changed) {
                                 Intrinsics.checkNotNullParameter($this$item, "$this$item");
                                 ComposerKt.sourceInformation($composer, "C112@5019L46,113@5113L62,109@4886L1683:MedicalCenterScreen.kt#k2q6ai");
                                 if (($changed & 81) == 16 && $composer.getSkipping()) {
                                    $composer.skipToGroupEnd();
                                 } else {
                                    if (ComposerKt.isTraceInProgress()) {
                                       ComposerKt.traceEventStart(497793616, $changed, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen.<anonymous>.<anonymous>.<anonymous> (MedicalCenterScreen.kt:109)");
                                    }

                                    Modifier var10000 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                                    boolean var10001 = false;
                                    Object var10002 = null;
                                    Object var10003 = null;
                                    $composer.startReplaceableGroup(1767412265);
                                    ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
                                    int $this$dp$iv = $composer.changed(onNavigate) | $composer.changed(currentPatientId);
                                    final Function1 var8 = onNavigate;
                                    final long var9 = currentPatientId;
                                    int $i$f$cache = 0;
                                    Object it$iv = $composer.rememberedValue();
                                    int var13 = 0;
                                    Object var10004;
                                    if (!$this$dp$iv && it$iv != Composer.Companion.getEmpty()) {
                                       var10004 = it$iv;
                                    } else {
                                       Object var19 = null;
                                       Object var18 = null;
                                       boolean var17 = false;
                                       Modifier var16 = var10000;
                                       int var14 = 0;
                                       Function0 value$iv = new Function0<Unit>() {
                                          public final void invoke() {
                                             var8.invoke("treatments/" + var9);
                                          }
                                       };
                                       var10000 = var16;
                                       var10001 = var17;
                                       var10002 = var18;
                                       var10003 = var19;
                                       $composer.updateRememberedValue(value$iv);
                                       var10004 = value$iv;
                                    }

                                    Function0 var5 = (Function0)var10004;
                                    $composer.endReplaceableGroup();
                                    Modifier var4 = ClickableKt.clickable-XHw0xAI$default(var10000, var10001, (String)var10002, (Role)var10003, var5, 7, (Object)null);
                                    CardColors var21 = CardDefaults.INSTANCE.cardColors-ro_MJ88(Color.copy-wmQWz5c$default(ColorKt.getStatusDelayed(), 0.15F, 0.0F, 0.0F, 0.0F, 14, (Object)null), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                                    $this$dp$iv = 12;
                                    int $i$f$getDp = 0;
                                    RoundedCornerShape $this$cache$ivx = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                                    CardKt.Card(var4, (Shape)$this$cache$ivx, var21, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1862899742, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                                       @Composable
                                       @ComposableTarget(
                                          applier = "androidx.compose.ui.UiComposable"
                                       )
                                       public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                                          Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                                          ComposerKt.sourceInformation($composer, "C116@5283L1264:MedicalCenterScreen.kt#k2q6ai");
                                          if (($changed & 81) == 16 && $composer.getSkipping()) {
                                             $composer.skipToGroupEnd();
                                          } else {
                                             if (ComposerKt.isTraceInProgress()) {
                                                ComposerKt.traceEventStart(1862899742, $changed, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen.<anonymous>.<anonymous>.<anonymous>.<anonymous> (MedicalCenterScreen.kt:116)");
                                             }

                                             Modifier var10000 = (Modifier)Modifier.Companion;
                                             int $this$dp$iv = 14;
                                             int $i$f$getDp = 0;
                                             Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                                             Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                                             List var7 = unverifiedMeds;
                                             int $changed$iv = 390;
                                             int $i$f$Row = 0;
                                             $composer.startReplaceableGroup(693286680);
                                             ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                                             Arrangement.Horizontal horizontalArrangement$iv = Arrangement.INSTANCE.getStart();
                                             MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, verticalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
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
                                             ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                                             int var28 = 6 | 112 & $changed$iv >> 6;
                                             RowScope $this$invoke_u24lambda_u241 = (RowScope)RowScopeInstance.INSTANCE;
                                             int var31 = 0;
                                             ComposerKt.sourceInformationMarkerStart($composer, 438543452, "C120@5483L76,121@5588L40,122@5657L754,135@6440L81:MedicalCenterScreen.kt#k2q6ai");
                                             IconKt.Icon-ww6aTOc(WarningKt.getWarning(Icons.INSTANCE.getDefault()), (String)null, (Modifier)null, ColorKt.getStatusDelayed(), $composer, 3120, 4);
                                             var10000 = (Modifier)Modifier.Companion;
                                             int $this$dp$iv = 12;
                                             int $i$f$getDp = 0;
                                             SpacerKt.Spacer(SizeKt.width-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                                             Modifier modifier$ivx = RowScope.weight$default($this$invoke_u24lambda_u241, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                                             int $changed$iv = 0;
                                             int $i$f$Column = 0;
                                             $composer.startReplaceableGroup(-483455358);
                                             ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                                             Arrangement.Vertical verticalArrangement$iv = Arrangement.INSTANCE.getTop();
                                             Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
                                             MeasurePolicy measurePolicy$iv = ColumnKt.columnMeasurePolicy(verticalArrangement$iv, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                                             int $changed$iv$ivx = 112 & $changed$iv << 3;
                                             int $i$f$Layout = 0;
                                             $composer.startReplaceableGroup(-1323940314);
                                             ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                                             int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                                             CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                                             Function0 factory$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
                                             Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$ivx);
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

                                             skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                                             $composer.startReplaceableGroup(2058660585);
                                             int var52 = 14 & $changed$iv$iv$iv >> 9;
                                             int var54 = 0;
                                             ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                                             int var55 = 6 | 112 & $changed$iv >> 6;
                                             ColumnScope var73 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                                             int var58 = 0;
                                             ComposerKt.sourceInformationMarkerStart($composer, 939482624, "C123@5730L330,131@6268L10,129@6093L288:MedicalCenterScreen.kt#k2q6ai");
                                             String var59 = var7.size() + " tratamiento(s) pendiente(s) de verificación";
                                             FontWeight var60 = FontWeight.Companion.getBold();
                                             long var61 = ColorKt.getStatusDelayed();
                                             long var63 = TextUnitKt.getSp(14);
                                             TextKt.Text--4IGK_g(var59, (Modifier)null, var61, var63, (FontStyle)null, var60, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 200064, 0, 131026);
                                             TextStyle var71 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                                             long var65 = ColorKt.getTextSecondary();
                                             TextKt.Text--4IGK_g("No generarán alarmas activas hasta ser verificados clínicamente.", (Modifier)null, var65, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var71, $composer, 390, 0, 65530);
                                             ComposerKt.sourceInformationMarkerEnd($composer);
                                             ComposerKt.sourceInformationMarkerEnd($composer);
                                             $composer.endReplaceableGroup();
                                             $composer.endNode();
                                             $composer.endReplaceableGroup();
                                             $composer.endReplaceableGroup();
                                             IconKt.Icon-ww6aTOc(ChevronRightKt.getChevronRight(Icons.INSTANCE.getDefault()), (String)null, (Modifier)null, ColorKt.getStatusDelayed(), $composer, 3120, 4);
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

                              }
                           }), 3, (Object)null);
                        }

                        LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, (Function3)ComposableLambdaKt.composableLambdaInstance(914758644, true, new Function3<LazyItemScope, Composer, Integer, Unit>() {
                           @Composable
                           @ComposableTarget(
                              applier = "androidx.compose.ui.UiComposable"
                           )
                           public final void invoke(@NotNull LazyItemScope $this$item, @Nullable Composer $composer, int $changed) {
                              Intrinsics.checkNotNullParameter($this$item, "$this$item");
                              ComposerKt.sourceInformation($composer, "C143@6706L701:MedicalCenterScreen.kt#k2q6ai");
                              if (($changed & 81) == 16 && $composer.getSkipping()) {
                                 $composer.skipToGroupEnd();
                              } else {
                                 if (ComposerKt.isTraceInProgress()) {
                                    ComposerKt.traceEventStart(914758644, $changed, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen.<anonymous>.<anonymous>.<anonymous> (MedicalCenterScreen.kt:143)");
                                 }

                                 Modifier modifier$iv = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                                 Arrangement.Horizontal horizontalArrangement$iv = (Arrangement.Horizontal)Arrangement.INSTANCE.getSpaceBetween();
                                 Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                                 String var7 = todayStr;
                                 final Function1 var8 = onNavigate;
                                 final long var9 = currentPatientId;
                                 int $changed$iv = 438;
                                 int $i$f$Row = 0;
                                 $composer.startReplaceableGroup(693286680);
                                 ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
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
                                 ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                                 int var31 = 6 | 112 & $changed$iv >> 6;
                                 RowScope var10000 = (RowScope)RowScopeInstance.INSTANCE;
                                 int var34 = 0;
                                 ComposerKt.sourceInformationMarkerStart($composer, 150734092, "C150@7056L10,148@6944L255,154@7241L49,154@7220L169:MedicalCenterScreen.kt#k2q6ai");
                                 String var35 = "Agenda de Hoy (" + var7 + ")";
                                 TextStyle var36 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                                 FontWeight var37 = FontWeight.Companion.getBold();
                                 long var38 = ColorKt.getTextPrimary();
                                 TextKt.Text--4IGK_g(var35, (Modifier)null, var38, 0L, (FontStyle)null, var37, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var36, $composer, 196992, 0, 65498);
                                 $composer.startReplaceableGroup(1113250155);
                                 ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
                                 boolean var46 = $composer.changed(var8) | $composer.changed(var9);
                                 int $i$f$cache = 0;
                                 Object it$iv = $composer.rememberedValue();
                                 int var42 = 0;
                                 Object var47;
                                 if (!var46 && it$iv != Composer.Companion.getEmpty()) {
                                    var47 = it$iv;
                                 } else {
                                    int var43 = 0;
                                    Object value$iv = new Function0<Unit>() {
                                       public final void invoke() {
                                          var8.invoke("intake_agenda/" + var9);
                                       }
                                    };
                                    $composer.updateRememberedValue(value$iv);
                                    var47 = value$iv;
                                 }

                                 Function0 var45 = (Function0)var47;
                                 $composer.endReplaceableGroup();
                                 ButtonKt.TextButton(var45, (Modifier)null, false, (Shape)null, (ButtonColors)null, (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$MedicalCenterScreenKt.INSTANCE.getLambda-3$app_debug(), $composer, 805306368, 510);
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
                        }), 3, (Object)null);
                        if (MedicalCenterScreenKt.MedicalCenterScreen$lambda$6(intakes$delegate).isEmpty()) {
                           LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$MedicalCenterScreenKt.INSTANCE.getLambda-5$app_debug(), 3, (Object)null);
                        } else {
                           List items$iv = MedicalCenterScreenKt.MedicalCenterScreen$lambda$6(intakes$delegate);
                           Function1 var6 = onNavigate;
                           Function1 key$iv = null;
                           Function1 contentType$iv = MedicalCenterScreenKt$MedicalCenterScreen$3$1$invoke$$inlined$items$default$1.INSTANCE;
                           int $i$f$items = 0;
                           $this$LazyColumn.items(items$iv.size(), (Function1)null, new MedicalCenterScreenKt$MedicalCenterScreen$3$1$invoke$$inlined$items$default$3(contentType$iv, items$iv), (Function4)ComposableLambdaKt.composableLambdaInstance(-632812321, true, new MedicalCenterScreenKt$MedicalCenterScreen$3$1$invoke$$inlined$items$default$4(items$iv, var6)));
                        }

                        LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, (Function3)ComposableLambdaKt.composableLambdaInstance(-418040557, true, new Function3<LazyItemScope, Composer, Integer, Unit>() {
                           @Composable
                           @ComposableTarget(
                              applier = "androidx.compose.ui.UiComposable"
                           )
                           public final void invoke(@NotNull LazyItemScope $this$item, @Nullable Composer $composer, int $changed) {
                              Intrinsics.checkNotNullParameter($this$item, "$this$item");
                              ComposerKt.sourceInformation($composer, "C183@8447L10,183@8396L125,184@8538L40,185@8595L856,201@9468L41,202@9526L833:MedicalCenterScreen.kt#k2q6ai");
                              if (($changed & 81) == 16 && $composer.getSkipping()) {
                                 $composer.skipToGroupEnd();
                              } else {
                                 if (ComposerKt.isTraceInProgress()) {
                                    ComposerKt.traceEventStart(-418040557, $changed, -1, "com.viernes.mobile.ui.screens.MedicalCenterScreen.<anonymous>.<anonymous>.<anonymous> (MedicalCenterScreen.kt:183)");
                                 }

                                 TextStyle var4 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                                 FontWeight var5 = FontWeight.Companion.getBold();
                                 long var6 = ColorKt.getTextPrimary();
                                 TextKt.Text--4IGK_g("Módulos del Paciente", (Modifier)null, var6, 0L, (FontStyle)null, var5, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var4, $composer, 196998, 0, 65498);
                                 Modifier var10000 = (Modifier)Modifier.Companion;
                                 int $this$dp$iv = 8;
                                 int $i$f$getDp = 0;
                                 SpacerKt.Spacer(SizeKt.height-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                                 Modifier $this$dp$iv = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                                 $i$f$getDp = 10;
                                 int $i$f$getDp = 0;
                                 Arrangement.Horizontal $i$f$getDp = (Arrangement.Horizontal)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                                 final Function1 var7 = onNavigate;
                                 final long var8 = currentPatientId;
                                 State var10 = medications$delegate;
                                 State var11 = appointments$delegate;
                                 int $changed$iv = 54;
                                 int $i$f$Row = 0;
                                 $composer.startReplaceableGroup(693286680);
                                 ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                                 Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getTop();
                                 MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy($i$f$getDp, verticalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                                 int $i$f$Layout = 112 & $changed$iv << 3;
                                 int $i$f$Layout = 0;
                                 $composer.startReplaceableGroup(-1323940314);
                                 ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                                 int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                                 CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                                 Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                                 Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf($this$dp$iv);
                                 int $i$f$ReusableComposeNode = 6 | 7168 & $i$f$Layout << 9;
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
                                 int var24 = 0;
                                 Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                                 Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                                 Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                                 int var26 = 0;
                                 int var28 = 0;
                                 if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                                    $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                                    $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                                 }

                                 skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $i$f$ReusableComposeNode >> 3);
                                 $composer.startReplaceableGroup(2058660585);
                                 int var29 = 14 & $i$f$ReusableComposeNode >> 9;
                                 int var31 = 0;
                                 ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                                 int var32 = 6 | 112 & $changed$iv >> 6;
                                 RowScope $this$invoke_u24lambda_u242 = (RowScope)RowScopeInstance.INSTANCE;
                                 int var35 = 0;
                                 ComposerKt.sourceInformationMarkerStart($composer, 152494582, "C191@8993L46,186@8710L351,198@9363L48,193@9082L351:MedicalCenterScreen.kt#k2q6ai");
                                 String var115 = "Tratamientos (" + MedicalCenterScreenKt.MedicalCenterScreen$lambda$7(var10).size() + ")";
                                 ImageVector var10001 = MedicationKt.getMedication(Icons.INSTANCE.getDefault());
                                 long var10002 = ColorKt.getViernesPrimary();
                                 Modifier var10003 = RowScope.weight$default($this$invoke_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                                 $composer.startReplaceableGroup(1113306216);
                                 ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
                                 int $i$f$cache = $composer.changed(var7) | $composer.changed(var8);
                                 int $i$f$cache = 0;
                                 Object it$iv = $composer.rememberedValue();
                                 int var40x = 0;
                                 Object var10004;
                                 if (!$i$f$cache && it$iv != Composer.Companion.getEmpty()) {
                                    var10004 = it$iv;
                                 } else {
                                    Modifier var41 = var10003;
                                    long var42 = var10002;
                                    ImageVector var44 = var10001;
                                    String var45 = var115;
                                    int value$iv = 0;
                                    Function0 value$iv = new Function0<Unit>() {
                                       public final void invoke() {
                                          var7.invoke("treatments/" + var8);
                                       }
                                    };
                                    var115 = var45;
                                    var10001 = var44;
                                    var10002 = var42;
                                    var10003 = var41;
                                    $composer.updateRememberedValue(value$iv);
                                    var10004 = value$iv;
                                 }

                                 Function0 var49 = (Function0)var10004;
                                 $composer.endReplaceableGroup();
                                 MedicalCenterScreenKt.MedicalQuickPill-T042LqI(var115, var10001, var10002, var10003, var49, $composer, 384, 0);
                                 var115 = "Citas (" + MedicalCenterScreenKt.MedicalCenterScreen$lambda$8(var11).size() + ")";
                                 var10001 = CalendarMonthKt.getCalendarMonth(Icons.INSTANCE.getDefault());
                                 var10002 = ColorKt.getStatusConfirmed();
                                 var10003 = RowScope.weight$default($this$invoke_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                                 $composer.startReplaceableGroup(1113318058);
                                 ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
                                 $i$f$cache = $composer.changed(var7) | $composer.changed(var8);
                                 $i$f$cache = 0;
                                 it$iv = $composer.rememberedValue();
                                 var40x = 0;
                                 if (!$i$f$cache && it$iv != Composer.Companion.getEmpty()) {
                                    var10004 = it$iv;
                                 } else {
                                    Modifier var98 = var10003;
                                    long var101 = var10002;
                                    ImageVector var103 = var10001;
                                    String var106 = var115;
                                    int var109 = 0;
                                    Function0 value$iv = new Function0<Unit>() {
                                       public final void invoke() {
                                          var7.invoke("appointments/" + var8);
                                       }
                                    };
                                    var115 = var106;
                                    var10001 = var103;
                                    var10002 = var101;
                                    var10003 = var98;
                                    $composer.updateRememberedValue(value$iv);
                                    var10004 = value$iv;
                                 }

                                 var49 = (Function0)var10004;
                                 $composer.endReplaceableGroup();
                                 MedicalCenterScreenKt.MedicalQuickPill-T042LqI(var115, var10001, var10002, var10003, var49, $composer, 384, 0);
                                 ComposerKt.sourceInformationMarkerEnd($composer);
                                 ComposerKt.sourceInformationMarkerEnd($composer);
                                 $composer.endReplaceableGroup();
                                 $composer.endNode();
                                 $composer.endReplaceableGroup();
                                 $composer.endReplaceableGroup();
                                 Modifier var117 = (Modifier)Modifier.Companion;
                                 int $this$dp$iv = 10;
                                 int $i$f$getDp = 0;
                                 SpacerKt.Spacer(SizeKt.height-3ABfNKs(var117, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                                 Modifier var53 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                                 $i$f$getDp = 10;
                                 int $i$f$getDp = 0;
                                 Arrangement.Horizontal var59 = (Arrangement.Horizontal)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                                 var7 = onNavigate;
                                 var8 = currentPatientId;
                                 var10 = inventoryList$delegate;
                                 int $changed$iv = 54;
                                 $changed$iv = 0;
                                 $composer.startReplaceableGroup(693286680);
                                 ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                                 Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getTop();
                                 MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(var59, verticalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                                 int $changed$iv$ivx = 112 & $changed$iv << 3;
                                 $i$f$Layout = 0;
                                 $composer.startReplaceableGroup(-1323940314);
                                 ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                                 $i$f$Layout = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                                 CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                                 Function0 factory$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
                                 Function3 skippableUpdate$iv$iv$ivx = LayoutKt.modifierMaterializerOf(var53);
                                 int $changed$iv$iv$ivx = 6 | 7168 & $changed$iv$ivx << 9;
                                 $i$f$ReusableComposeNode = 0;
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
                                 int var79 = 0;
                                 Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                                 Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                                 Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                                 int var81 = 0;
                                 int $this$set_impl_u24lambda_u240$iv$iv$iv = 0;
                                 if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), $i$f$Layout)) {
                                    $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue($i$f$Layout);
                                    $this$Layout_u24lambda_u240$iv$iv.apply($i$f$Layout, block$iv$iv$iv);
                                 }

                                 skippableUpdate$iv$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivx >> 3);
                                 $composer.startReplaceableGroup(2058660585);
                                 var28 = 14 & $changed$iv$iv$ivx >> 9;
                                 int $composer$iv = 0;
                                 ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                                 var31 = 6 | 112 & $changed$iv >> 6;
                                 RowScope $this$invoke_u24lambda_u245 = (RowScope)RowScopeInstance.INSTANCE;
                                 int var84 = 0;
                                 ComposerKt.sourceInformationMarkerStart($composer, 153417421, "C208@9922L45,203@9641L348,215@10276L43,210@10010L331:MedicalCenterScreen.kt#k2q6ai");
                                 String var118 = "Inventario (" + MedicalCenterScreenKt.MedicalCenterScreen$lambda$10(var10).size() + ")";
                                 var10001 = InventoryKt.getInventory(Icons.INSTANCE.getDefault());
                                 var10002 = ColorKt.getStatusPending();
                                 var10003 = RowScope.weight$default($this$invoke_u24lambda_u245, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                                 $composer.startReplaceableGroup(1113335943);
                                 ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
                                 boolean $this$cache$ivx = $composer.changed(var7) | $composer.changed(var8);
                                 $i$f$cache = 0;
                                 Object it$iv = $composer.rememberedValue();
                                 int var93 = 0;
                                 if (!$this$cache$ivx && it$iv != Composer.Companion.getEmpty()) {
                                    var10004 = it$iv;
                                 } else {
                                    Modifier var96 = var10003;
                                    long var99 = var10002;
                                    ImageVector var43 = var10001;
                                    String var104 = var118;
                                    int var107 = 0;
                                    Function0 value$iv = new Function0<Unit>() {
                                       public final void invoke() {
                                          var7.invoke("inventory/" + var8);
                                       }
                                    };
                                    var118 = var104;
                                    var10001 = var43;
                                    var10002 = var99;
                                    var10003 = var96;
                                    $composer.updateRememberedValue(value$iv);
                                    var10004 = value$iv;
                                 }

                                 Function0 value$ivx = (Function0)var10004;
                                 $composer.endReplaceableGroup();
                                 MedicalCenterScreenKt.MedicalQuickPill-T042LqI(var118, var10001, var10002, var10003, value$ivx, $composer, 384, 0);
                                 var118 = "Historial & Auditoría";
                                 var10001 = HistoryKt.getHistory(Icons.INSTANCE.getDefault());
                                 var10002 = ColorKt.getStatusSkipped();
                                 var10003 = RowScope.weight$default($this$invoke_u24lambda_u245, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                                 $composer.startReplaceableGroup(1113347269);
                                 ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
                                 $this$cache$ivx = $composer.changed(var7) | $composer.changed(var8);
                                 $i$f$cache = 0;
                                 it$iv = $composer.rememberedValue();
                                 var93 = 0;
                                 if (!$this$cache$ivx && it$iv != Composer.Companion.getEmpty()) {
                                    var10004 = it$iv;
                                 } else {
                                    Modifier var97 = var10003;
                                    long var100 = var10002;
                                    ImageVector var102 = var10001;
                                    String var105 = "Historial & Auditoría";
                                    int var108 = 0;
                                    Function0 value$iv = new Function0<Unit>() {
                                       public final void invoke() {
                                          var7.invoke("history/" + var8);
                                       }
                                    };
                                    var118 = var105;
                                    var10001 = var102;
                                    var10002 = var100;
                                    var10003 = var97;
                                    $composer.updateRememberedValue(value$iv);
                                    var10004 = value$iv;
                                 }

                                 value$ivx = (Function0)var10004;
                                 $composer.endReplaceableGroup();
                                 MedicalCenterScreenKt.MedicalQuickPill-T042LqI(var118, var10001, var10002, var10003, value$ivx, $composer, 390, 0);
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
                        }), 3, (Object)null);
                        LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$MedicalCenterScreenKt.INSTANCE.getLambda-6$app_debug(), 3, (Object)null);
                     }
                  }, $composer, 24576, 238);
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

      ScopeUpdateScope var56 = $composer.endRestartGroup();
      if (var56 != null) {
         var56.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               MedicalCenterScreenKt.MedicalCenterScreen(patientRepo, medRepo, intakeRepo, appointmentRepo, refillRepo, inventoryRepo, onNavigate, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void IntakeMedicalRow(@NotNull final Intake intake, @NotNull final Function0<Unit> onClick, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(intake, "intake");
      Intrinsics.checkNotNullParameter(onClick, "onClick");
      $composer = $composer.startRestartGroup(669578209);
      ComposerKt.sourceInformation($composer, "C(IntakeMedicalRow)241@10939L13,242@10984L40,238@10854L1655:MedicalCenterScreen.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(intake) ? 4 : 2);
      }

      if (($changed & 112) == 0) {
         $dirty |= $composer.changedInstance(onClick) ? 32 : 16;
      }

      if (($dirty & 91) == 18 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(669578209, $dirty, -1, "com.viernes.mobile.ui.screens.IntakeMedicalRow (MedicalCenterScreen.kt:229)");
         }

         long var10000;
         switch (MedicalCenterScreenKt.WhenMappings.$EnumSwitchMapping$0[intake.getStatus().ordinal()]) {
            case 1 -> var10000 = ColorKt.getStatusConfirmed();
            case 2 -> var10000 = intake.isDelayed() ? ColorKt.getStatusDelayed() : ColorKt.getStatusPending();
            case 3 -> var10000 = ColorKt.getStatusDelayed();
            case 4 -> var10000 = ColorKt.getStatusSkipped();
            default -> var10000 = ColorKt.getTextSecondary();
         }

         final long statusColor = var10000;
         Modifier var25 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
         boolean var10001 = false;
         Object var10002 = null;
         Object var10003 = null;
         $composer.startReplaceableGroup(-39880138);
         ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
         boolean invalid$iv = ($dirty & 112) == 32;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var13 = 0;
         Object var10004;
         if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
            var10004 = it$iv;
         } else {
            Object var19 = null;
            Object var18 = null;
            boolean var17 = false;
            Modifier var16 = var25;
            int var14 = 0;
            Function0 value$iv = new Function0<Unit>() {
               public final void invoke() {
                  onClick.invoke();
               }
            };
            var25 = var16;
            var10001 = var17;
            var10002 = var18;
            var10003 = var19;
            $composer.updateRememberedValue(value$iv);
            var10004 = value$iv;
         }

         Function0 var8 = (Function0)var10004;
         $composer.endReplaceableGroup();
         Modifier var7 = ClickableKt.clickable-XHw0xAI$default(var25, var10001, (String)var10002, (Role)var10003, var8, 7, (Object)null);
         CardColors var22 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
         invalid$iv = (boolean)12;
         $i$f$cache = 0;
         RoundedCornerShape $this$cache$iv = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)invalid$iv));
         CardKt.Card(var7, (Shape)$this$cache$iv, var22, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1918438959, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
               ComposerKt.sourceInformation($composer, "C245@11084L1419:MedicalCenterScreen.kt#k2q6ai");
               if (($changed & 81) == 16 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(1918438959, $changed, -1, "com.viernes.mobile.ui.screens.IntakeMedicalRow.<anonymous> (MedicalCenterScreen.kt:245)");
                  }

                  Modifier var10000 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  int $this$dp$iv = 14;
                  int $i$f$getDp = 0;
                  Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                  Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                  long var7 = statusColor;
                  Intake var9 = intake;
                  int $changed$iv = 390;
                  int $i$f$Row = 0;
                  $composer.startReplaceableGroup(693286680);
                  ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
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
                  int var22 = 0;
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                  Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                  int var24 = 0;
                  int var26 = 0;
                  if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                     $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                     $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                  }

                  skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int var27 = 14 & $changed$iv$iv$ivx >> 9;
                  int var29 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                  int var30 = 6 | 112 & $changed$iv >> 6;
                  RowScope $this$invoke_u24lambda_u242 = (RowScope)RowScopeInstance.INSTANCE;
                  int var33 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -720323788, "C251@11269L487,265@11769L40,266@11822L577,279@12412L81:MedicalCenterScreen.kt#k2q6ai");
                  var10000 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 44;
                  int $i$f$getDp = 0;
                  Modifier modifier$ivx = BackgroundKt.background-bw27NRU$default(ClipKt.clip(SizeKt.size-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), (Shape)RoundedCornerShapeKt.getCircleShape()), Color.copy-wmQWz5c$default(var7, 0.2F, 0.0F, 0.0F, 0.0F, 14, (Object)null), (Shape)null, 2, (Object)null);
                  Alignment contentAlignment$iv = Alignment.Companion.getCenter();
                  int $changed$iv = 48;
                  int $i$f$Box = 0;
                  $composer.startReplaceableGroup(733328855);
                  ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
                  boolean propagateMinConstraints$iv = false;
                  MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(contentAlignment$iv, propagateMinConstraints$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                  int $changed$iv$ivx = 112 & $changed$iv << 3;
                  int $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  Function0 factory$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
                  Function3 skippableUpdate$iv$iv$ivx = LayoutKt.modifierMaterializerOf(modifier$ivx);
                  int $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$ivx << 9;
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
                  int var49 = 0;
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                  Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                  int var51 = 0;
                  int var53 = 0;
                  if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                     $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                     $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                  }

                  skippableUpdate$iv$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int $changed$ivxxx = 14 & $changed$iv$iv$ivxx >> 9;
                  int var56 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                  int $changedxx = 6 | 112 & $changed$iv >> 6;
                  BoxScope var102 = (BoxScope)BoxScopeInstance.INSTANCE;
                  int var60 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -2049075158, "C258@11531L211:MedicalCenterScreen.kt#k2q6ai");
                  String var103 = var9.getScheduledTime();
                  if (var103 == null) {
                     var103 = "--:--";
                  }

                  String var61 = var103;
                  FontWeight var62 = FontWeight.Companion.getBold();
                  long var63 = TextUnitKt.getSp(12);
                  TextKt.Text--4IGK_g(var61, (Modifier)null, var7, var63, (FontStyle)null, var62, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 199680, 0, 131026);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  $composer.endReplaceableGroup();
                  $composer.endNode();
                  $composer.endReplaceableGroup();
                  $composer.endReplaceableGroup();
                  Modifier var104 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 12;
                  int $i$f$getDp = 0;
                  SpacerKt.Spacer(SizeKt.width-3ABfNKs(var104, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                  Modifier modifier$ivxx = RowScope.weight$default($this$invoke_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                  $changed$iv = 0;
                  $i$f$Box = 0;
                  $composer.startReplaceableGroup(-483455358);
                  ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                  Arrangement.Vertical verticalArrangement$iv = Arrangement.INSTANCE.getTop();
                  Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
                  measurePolicy$iv = ColumnKt.columnMeasurePolicy(verticalArrangement$iv, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                  $changed$iv$ivx = 112 & $changed$iv << 3;
                  $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  factory$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
                  skippableUpdate$iv$iv$ivx = LayoutKt.modifierMaterializerOf(modifier$ivxx);
                  $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$ivx << 9;
                  $i$f$ReusableComposeNode = 0;
                  if (!($composer.getApplier() instanceof Applier)) {
                     ComposablesKt.invalidApplier();
                  }

                  $composer.startReusableNode();
                  if ($composer.getInserting()) {
                     $composer.createNode(factory$iv$iv$ivx);
                  } else {
                     $composer.useNode();
                  }

                  $this$Layout_u24lambda_u240$iv$iv = Updater.constructor-impl($composer);
                  var49 = 0;
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                  block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                  var51 = 0;
                  var53 = 0;
                  if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                     $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                     $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                  }

                  skippableUpdate$iv$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  $changed$ivxxx = 14 & $changed$iv$iv$ivxx >> 9;
                  var56 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                  $changedxx = 6 | 112 & $changed$iv >> 6;
                  ColumnScope var105 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  var60 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -2048720797, "C269@12003L10,267@11879L254,275@12306L10,273@12150L235:MedicalCenterScreen.kt#k2q6ai");
                  String var106 = var9.getMedicationName();
                  var61 = var106 + " (" + var9.getDoseText() + ")";
                  TextStyle var99 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleSmall();
                  FontWeight var65 = FontWeight.Companion.getBold();
                  long var66 = ColorKt.getTextPrimary();
                  TextKt.Text--4IGK_g(var61, (Modifier)null, var66, 0L, (FontStyle)null, var65, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var99, $composer, 196992, 0, 65498);
                  var106 = var9.getStatus().getValue();
                  var61 = "Estado: " + var106 + (var9.isDelayed() ? " (RETRASADA)" : "");
                  var99 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                  TextKt.Text--4IGK_g(var61, (Modifier)null, var7, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var99, $composer, 0, 0, 65530);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  $composer.endReplaceableGroup();
                  $composer.endNode();
                  $composer.endReplaceableGroup();
                  $composer.endReplaceableGroup();
                  IconKt.Icon-ww6aTOc(ChevronRightKt.getChevronRight(Icons.INSTANCE.getDefault()), (String)null, (Modifier)null, ColorKt.getTextSecondary(), $composer, 3120, 4);
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

      ScopeUpdateScope var26 = $composer.endRestartGroup();
      if (var26 != null) {
         var26.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               MedicalCenterScreenKt.IntakeMedicalRow(intake, onClick, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void MedicalQuickPill_T042LqI/* $FF was: MedicalQuickPill-T042LqI*/(@NotNull final String label, @NotNull final ImageVector icon, final long color, @Nullable final Modifier modifier, @NotNull final Function0<Unit> onClick, @Nullable Composer $composer, final int $changed, final int var8) {
      Intrinsics.checkNotNullParameter(label, "label");
      Intrinsics.checkNotNullParameter(icon, "icon");
      Intrinsics.checkNotNullParameter(onClick, "onClick");
      $composer = $composer.startRestartGroup(-337320018);
      ComposerKt.sourceInformation($composer, "C(MedicalQuickPill)P(2,1,0:c#ui.graphics.Color)293@12754L13,294@12799L44,292@12710L611:MedicalCenterScreen.kt#k2q6ai");
      int $dirty = $changed;
      if ((var8 & 1) != 0) {
         $dirty = $changed | 6;
      } else if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(label) ? 4 : 2);
      }

      if ((var8 & 2) != 0) {
         $dirty |= 48;
      } else if (($changed & 112) == 0) {
         $dirty |= $composer.changed(icon) ? 32 : 16;
      }

      if ((var8 & 4) != 0) {
         $dirty |= 384;
      } else if (($changed & 896) == 0) {
         $dirty |= $composer.changed(color) ? 256 : 128;
      }

      if ((var8 & 8) != 0) {
         $dirty |= 3072;
      } else if (($changed & 7168) == 0) {
         $dirty |= $composer.changed(modifier) ? 2048 : 1024;
      }

      if ((var8 & 16) != 0) {
         $dirty |= 24576;
      } else if (($changed & '\ue000') == 0) {
         $dirty |= $composer.changedInstance(onClick) ? 16384 : 8192;
      }

      if (($dirty & '뛛') == 9362 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if ((var8 & 8) != 0) {
            modifier = (Modifier)Modifier.Companion;
         }

         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(-337320018, $dirty, -1, "com.viernes.mobile.ui.screens.MedicalQuickPill (MedicalCenterScreen.kt:291)");
         }

         Modifier var10000 = modifier;
         boolean var10001 = false;
         Object var10002 = null;
         Object var10003 = null;
         $composer.startReplaceableGroup(-1901007754);
         ComposerKt.sourceInformation($composer, "CC(remember):MedicalCenterScreen.kt#9igjgp");
         boolean invalid$iv = ($dirty & '\ue000') == 16384;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var16 = 0;
         Object var10004;
         if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
            var10004 = it$iv;
         } else {
            Object var22 = null;
            Object var21 = null;
            boolean var20 = false;
            int var17 = 0;
            Function0 value$iv = new Function0<Unit>() {
               public final void invoke() {
                  onClick.invoke();
               }
            };
            var10000 = modifier;
            var10001 = var20;
            var10002 = var21;
            var10003 = var22;
            $composer.updateRememberedValue(value$iv);
            var10004 = value$iv;
         }

         Function0 var11 = (Function0)var10004;
         $composer.endReplaceableGroup();
         Modifier var10 = ClickableKt.clickable-XHw0xAI$default(var10000, var10001, (String)var10002, (Role)var10003, var11, 7, (Object)null);
         CardColors var25 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceElevated(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
         invalid$iv = (boolean)10;
         $i$f$cache = 0;
         RoundedCornerShape $this$cache$iv = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)invalid$iv));
         CardKt.Card(var10, (Shape)$this$cache$iv, var25, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 904187040, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
               ComposerKt.sourceInformation($composer, "C297@12903L412:MedicalCenterScreen.kt#k2q6ai");
               if (($changed & 81) == 16 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(904187040, $changed, -1, "com.viernes.mobile.ui.screens.MedicalQuickPill.<anonymous> (MedicalCenterScreen.kt:297)");
                  }

                  Modifier var10000 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 12;
                  int $i$f$getDp = 0;
                  Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                  Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                  ImageVector var7 = icon;
                  long var8 = color;
                  String var10 = label;
                  int $changed$iv = 390;
                  int $i$f$Row = 0;
                  $composer.startReplaceableGroup(693286680);
                  ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
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
                  ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                  int var31 = 6 | 112 & $changed$iv >> 6;
                  RowScope var46 = (RowScope)RowScopeInstance.INSTANCE;
                  int var34 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -1391948142, "C301@13039L84,302@13136L39,303@13229L10,303@13188L117:MedicalCenterScreen.kt#k2q6ai");
                  Modifier var47 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 20;
                  int $i$f$getDp = 0;
                  Modifier var37 = SizeKt.size-3ABfNKs(var47, Dp.constructor-impl((float)$this$dp$iv));
                  IconKt.Icon-ww6aTOc(var7, (String)null, var37, var8, $composer, 432, 0);
                  var47 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 8;
                  $this$dp$iv = 0;
                  SpacerKt.Spacer(SizeKt.width-3ABfNKs(var47, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                  TextStyle var45 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                  FontWeight var43 = FontWeight.Companion.getSemiBold();
                  long var38 = ColorKt.getTextPrimary();
                  TextKt.Text--4IGK_g(var10, (Modifier)null, var38, 0L, (FontStyle)null, var43, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var45, $composer, 196992, 0, 65498);
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

      ScopeUpdateScope var28 = $composer.endRestartGroup();
      if (var28 != null) {
         var28.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               MedicalCenterScreenKt.MedicalQuickPill-T042LqI(label, icon, color, modifier, onClick, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1), var8);
            }
         });
      }

   }

   private static final List<Patient> MedicalCenterScreen$lambda$0(State<? extends List<Patient>> $patients$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$patients$delegate.getValue();
   }

   private static final Long MedicalCenterScreen$lambda$2(MutableState<Long> $selectedPatientId$delegate) {
      State $this$getValue$iv = (State)$selectedPatientId$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Long)$this$getValue$iv.getValue();
   }

   private static final void MedicalCenterScreen$lambda$3(MutableState<Long> $selectedPatientId$delegate, Long value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $selectedPatientId$delegate.setValue(value);
   }

   private static final List<Intake> MedicalCenterScreen$lambda$6(State<? extends List<Intake>> $intakes$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$intakes$delegate.getValue();
   }

   private static final List<Medication> MedicalCenterScreen$lambda$7(State<? extends List<Medication>> $medications$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$medications$delegate.getValue();
   }

   private static final List<MedicalAppointment> MedicalCenterScreen$lambda$8(State<? extends List<MedicalAppointment>> $appointments$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$appointments$delegate.getValue();
   }

   private static final List<Refill> MedicalCenterScreen$lambda$9(State<? extends List<Refill>> $refills$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$refills$delegate.getValue();
   }

   private static final List<Inventory> MedicalCenterScreen$lambda$10(State<? extends List<Inventory>> $inventoryList$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$inventoryList$delegate.getValue();
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
}
