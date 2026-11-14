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
import androidx.compose.material.icons.filled.ChevronRightKt;
import androidx.compose.material.icons.filled.DocumentScannerKt;
import androidx.compose.material.icons.filled.EventKt;
import androidx.compose.material.icons.filled.Inventory2Kt;
import androidx.compose.material.icons.filled.MedicalServicesKt;
import androidx.compose.material.icons.filled.PersonKt;
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
import androidx.compose.runtime.RecomposeScopeImplKt;
import androidx.compose.runtime.ScopeUpdateScope;
import androidx.compose.runtime.SkippableUpdater;
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
import com.viernes.mobile.avatar.HuoAvatarController;
import com.viernes.mobile.avatar.HuoLive2DViewKt;
import com.viernes.mobile.avatar.HuoState;
import com.viernes.mobile.data.repository.IntakeRepository;
import com.viernes.mobile.data.repository.PatientRepository;
import com.viernes.mobile.domain.model.Intake;
import com.viernes.mobile.domain.model.Patient;
import com.viernes.mobile.ui.theme.ColorKt;
import java.time.LocalDate;
import java.util.List;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.collections.CollectionsKt;
import kotlin.coroutines.CoroutineContext;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.functions.Function3;
import kotlin.jvm.functions.Function4;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.reflect.KProperty;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 2,
   xi = 48,
   d1 = {"\u0000`\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010 \n\u0002\b\u0002\n\u0002\u0018\u0002\u001aJ\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00032\u0006\u0010\u0005\u001a\u00020\u00062\u0006\u0010\u0007\u001a\u00020\b2\b\b\u0002\u0010\t\u001a\u00020\n2\f\u0010\u000b\u001a\b\u0012\u0004\u0012\u00020\u00010\fH\u0007ø\u0001\u0000¢\u0006\u0004\b\r\u0010\u000e\u001a9\u0010\u000f\u001a\u00020\u00012\u0006\u0010\u0010\u001a\u00020\u00112\u0006\u0010\u0012\u001a\u00020\u00132\u0006\u0010\u0014\u001a\u00020\u00152\u0012\u0010\u0016\u001a\u000e\u0012\u0004\u0012\u00020\u0003\u0012\u0004\u0012\u00020\u00010\u0017H\u0007¢\u0006\u0002\u0010\u0018\u001a#\u0010\u0019\u001a\u00020\u00012\u0006\u0010\u001a\u001a\u00020\u001b2\f\u0010\u000b\u001a\b\u0012\u0004\u0012\u00020\u00010\fH\u0007¢\u0006\u0002\u0010\u001c\u001a-\u0010\u001d\u001a\u00020\u00012\u0006\u0010\u001e\u001a\u00020\u001f2\b\b\u0002\u0010\t\u001a\u00020\n2\f\u0010\u000b\u001a\b\u0012\u0004\u0012\u00020\u00010\fH\u0007¢\u0006\u0002\u0010 \u0082\u0002\u0007\n\u0005\b¡\u001e0\u0001¨\u0006!²\u0006\u0010\u0010\"\u001a\b\u0012\u0004\u0012\u00020\u001f0#X\u008a\u0084\u0002²\u0006\u0010\u0010$\u001a\b\u0012\u0004\u0012\u00020\u001b0#X\u008a\u0084\u0002²\u0006\n\u0010%\u001a\u00020&X\u008a\u0084\u0002"},
   d2 = {"ActionCard", "", "title", "", "subtitle", "icon", "Landroidx/compose/ui/graphics/vector/ImageVector;", "color", "Landroidx/compose/ui/graphics/Color;", "modifier", "Landroidx/compose/ui/Modifier;", "onClick", "Lkotlin/Function0;", "ActionCard-fWhpE4E", "(Ljava/lang/String;Ljava/lang/String;Landroidx/compose/ui/graphics/vector/ImageVector;JLandroidx/compose/ui/Modifier;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;II)V", "HomeScreen", "patientRepo", "Lcom/viernes/mobile/data/repository/PatientRepository;", "intakeRepo", "Lcom/viernes/mobile/data/repository/IntakeRepository;", "huoController", "Lcom/viernes/mobile/avatar/HuoAvatarController;", "onNavigate", "Lkotlin/Function1;", "(Lcom/viernes/mobile/data/repository/PatientRepository;Lcom/viernes/mobile/data/repository/IntakeRepository;Lcom/viernes/mobile/avatar/HuoAvatarController;Lkotlin/jvm/functions/Function1;Landroidx/compose/runtime/Composer;I)V", "IntakeItemCard", "intake", "Lcom/viernes/mobile/domain/model/Intake;", "(Lcom/viernes/mobile/domain/model/Intake;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "PatientQuickCard", "patient", "Lcom/viernes/mobile/domain/model/Patient;", "(Lcom/viernes/mobile/domain/model/Patient;Landroidx/compose/ui/Modifier;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;II)V", "app_debug", "patients", "", "upcomingIntakes", "huoState", "Lcom/viernes/mobile/avatar/HuoState;"}
)
@SourceDebugExtension({"SMAP\nHomeScreen.kt\nKotlin\n*S Kotlin\n*F\n+ 1 HomeScreen.kt\ncom/viernes/mobile/ui/screens/HomeScreenKt\n+ 2 Composer.kt\nandroidx/compose/runtime/ComposerKt\n+ 3 Dp.kt\nandroidx/compose/ui/unit/DpKt\n+ 4 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,399:1\n1116#2,6:400\n1116#2,6:406\n1116#2,6:413\n1116#2,6:420\n154#3:412\n154#3:419\n154#3:426\n81#4:427\n81#4:428\n81#4:429\n*S KotlinDebug\n*F\n+ 1 HomeScreen.kt\ncom/viernes/mobile/ui/screens/HomeScreenKt\n*L\n40#1:400,6\n277#1:406,6\n321#1:413,6\n357#1:420,6\n279#1:412\n323#1:419\n359#1:426\n41#1:427\n42#1:428\n43#1:429\n*E\n"})
public final class HomeScreenKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void HomeScreen(@NotNull final PatientRepository patientRepo, @NotNull final IntakeRepository intakeRepo, @NotNull final HuoAvatarController huoController, @NotNull final Function1<? super String, Unit> onNavigate, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(patientRepo, "patientRepo");
      Intrinsics.checkNotNullParameter(intakeRepo, "intakeRepo");
      Intrinsics.checkNotNullParameter(huoController, "huoController");
      Intrinsics.checkNotNullParameter(onNavigate, "onNavigate");
      $composer = $composer.startRestartGroup(2105048173);
      ComposerKt.sourceInformation($composer, "C(HomeScreen)P(3,1)39@1525L39,40@1617L37,41@1729L37,42@1814L16,44@1836L9652:HomeScreen.kt#k2q6ai");
      if (ComposerKt.isTraceInProgress()) {
         ComposerKt.traceEventStart(2105048173, $changed, -1, "com.viernes.mobile.ui.screens.HomeScreen (HomeScreen.kt:38)");
      }

      $composer.startReplaceableGroup(-169522330);
      ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
      boolean var10 = false;
      int $i$f$cache = 0;
      Object it$iv = $composer.rememberedValue();
      int var13 = 0;
      Object var10000;
      if (it$iv == Composer.Companion.getEmpty()) {
         int var14 = 0;
         Object value$iv = LocalDate.now().toString();
         $composer.updateRememberedValue(value$iv);
         var10000 = value$iv;
      } else {
         var10000 = it$iv;
      }

      String todayStr = (String)var10000;
      $composer.endReplaceableGroup();
      Intrinsics.checkNotNull(todayStr);
      final State patients$delegate = SnapshotStateKt.collectAsState(patientRepo.getActivePatients(), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
      final State upcomingIntakes$delegate = SnapshotStateKt.collectAsState(intakeRepo.getUpcomingPendingIntakes(todayStr), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
      final State huoState$delegate = SnapshotStateKt.collectAsState(huoController.getCurrentState(), (CoroutineContext)null, $composer, 8, 1);
      ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -1418474191, true, new Function2<Composer, Integer, Unit>() {
         @Composable
         @ComposableTarget(
            applier = "androidx.compose.ui.UiComposable"
         )
         public final void invoke(@Nullable Composer $composer, int $changed) {
            ComposerKt.sourceInformation($composer, "C75@3210L86,46@1877L1433:HomeScreen.kt#k2q6ai");
            if (($changed & 11) == 2 && $composer.getSkipping()) {
               $composer.skipToGroupEnd();
            } else {
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventStart(-1418474191, $changed, -1, "com.viernes.mobile.ui.screens.HomeScreen.<anonymous> (HomeScreen.kt:46)");
               }

               AppBarKt.TopAppBar(ComposableSingletons$HomeScreenKt.INSTANCE.getLambda-1$app_debug(), (Modifier)null, (Function2)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1846224738, true, new Function3<RowScope, Composer, Integer, Unit>() {
                  @Composable
                  @ComposableTarget(
                     applier = "androidx.compose.ui.UiComposable"
                  )
                  public final void invoke(@NotNull RowScope $this$TopAppBar, @Nullable Composer $composer, int $changed) {
                     Intrinsics.checkNotNullParameter($this$TopAppBar, "$this$TopAppBar");
                     ComposerKt.sourceInformation($composer, "C71@2989L26,71@2968L179:HomeScreen.kt#k2q6ai");
                     if (($changed & 81) == 16 && $composer.getSkipping()) {
                        $composer.skipToGroupEnd();
                     } else {
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventStart(1846224738, $changed, -1, "com.viernes.mobile.ui.screens.HomeScreen.<anonymous>.<anonymous> (HomeScreen.kt:71)");
                        }

                        $composer.startReplaceableGroup(494818007);
                        ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
                        boolean invalid$iv = $composer.changed(onNavigate);
                        final Function1 var7 = onNavigate;
                        int $i$f$cache = 0;
                        Object it$iv = $composer.rememberedValue();
                        int var10 = 0;
                        Object var10000;
                        if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
                           var10000 = it$iv;
                        } else {
                           int var11 = 0;
                           Object value$iv = new Function0<Unit>() {
                              public final void invoke() {
                                 var7.invoke("settings");
                              }
                           };
                           $composer.updateRememberedValue(value$iv);
                           var10000 = value$iv;
                        }

                        Function0 var4 = (Function0)var10000;
                        $composer.endReplaceableGroup();
                        IconButtonKt.IconButton(var4, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$HomeScreenKt.INSTANCE.getLambda-2$app_debug(), $composer, 196608, 30);
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
      }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1887744252, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
         @Composable
         @ComposableTarget(
            applier = "androidx.compose.ui.UiComposable"
         )
         public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
            Intrinsics.checkNotNullParameter(padding, "padding");
            ComposerKt.sourceInformation($composer, "C82@3389L8093:HomeScreen.kt#k2q6ai");
            int $dirty = $changed;
            if (($changed & 14) == 0) {
               $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
            }

            if (($dirty & 91) == 18 && $composer.getSkipping()) {
               $composer.skipToGroupEnd();
            } else {
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventStart(1887744252, $dirty, -1, "com.viernes.mobile.ui.screens.HomeScreen.<anonymous> (HomeScreen.kt:82)");
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
                     LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, (Function3)ComposableLambdaKt.composableLambdaInstance(-544470552, true, new Function3<LazyItemScope, Composer, Integer, Unit>() {
                        @Composable
                        @ComposableTarget(
                           applier = "androidx.compose.ui.UiComposable"
                        )
                        public final void invoke(@NotNull LazyItemScope $this$item, @Nullable Composer $composer, int $changed) {
                           Intrinsics.checkNotNullParameter($this$item, "$this$item");
                           ComposerKt.sourceInformation($composer, "C93@3811L40,91@3707L2634:HomeScreen.kt#k2q6ai");
                           if (($changed & 81) == 16 && $composer.getSkipping()) {
                              $composer.skipToGroupEnd();
                           } else {
                              if (ComposerKt.isTraceInProgress()) {
                                 ComposerKt.traceEventStart(-544470552, $changed, -1, "com.viernes.mobile.ui.screens.HomeScreen.<anonymous>.<anonymous>.<anonymous> (HomeScreen.kt:91)");
                              }

                              Modifier var4 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                              CardColors var5 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                              int $this$dp$iv = 16;
                              int $i$f$getDp = 0;
                              RoundedCornerShape var6 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                              CardKt.Card(var4, (Shape)var6, var5, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, -1229561418, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                                 @Composable
                                 @ComposableTarget(
                                    applier = "androidx.compose.ui.UiComposable"
                                 )
                                 public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                                    Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                                    ComposerKt.sourceInformation($composer, "C96@3947L2376:HomeScreen.kt#k2q6ai");
                                    if (($changed & 81) == 16 && $composer.getSkipping()) {
                                       $composer.skipToGroupEnd();
                                    } else {
                                       if (ComposerKt.isTraceInProgress()) {
                                          ComposerKt.traceEventStart(-1229561418, $changed, -1, "com.viernes.mobile.ui.screens.HomeScreen.<anonymous>.<anonymous>.<anonymous>.<anonymous> (HomeScreen.kt:96)");
                                       }

                                       Modifier var10000 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                                       int $this$dp$iv = 16;
                                       int $i$f$getDp = 0;
                                       Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                                       Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                                       final Function1 var7 = onNavigate;
                                       HuoAvatarController var8 = huoController;
                                       State var9 = huoState$delegate;
                                       int $changed$iv = 390;
                                       int $i$f$Row = 0;
                                       $composer.startReplaceableGroup(693286680);
                                       ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                                       Arrangement.Horizontal horizontalArrangement$iv = Arrangement.INSTANCE.getStart();
                                       MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, verticalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                                       int $changed$iv$ivx = 112 & $changed$iv << 3;
                                       int $i$f$Layout = 0;
                                       $composer.startReplaceableGroup(-1323940314);
                                       ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                                       int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                                       CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                                       Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                                       Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$iv);
                                       int $changed$iv$iv$iv = 6 | 7168 & $changed$iv$ivx << 9;
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

                                       skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                                       $composer.startReplaceableGroup(2058660585);
                                       int var27 = 14 & $changed$iv$iv$iv >> 9;
                                       int var29 = 0;
                                       ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                                       int var30 = 6 | 112 & $changed$iv >> 6;
                                       RowScope $this$invoke_u24lambda_u244 = (RowScope)RowScopeInstance.INSTANCE;
                                       int var33 = 0;
                                       ComposerKt.sourceInformationMarkerStart($composer, -4903161, "C108@4518L24,103@4251L544,116@4821L40,118@4887L1414:HomeScreen.kt#k2q6ai");
                                       var10000 = (Modifier)Modifier.Companion;
                                       int $this$dp$iv = 90;
                                       int $i$f$getDp = 0;
                                       var10000 = SizeKt.size-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                                       $this$dp$iv = 12;
                                       $i$f$getDp = 0;
                                       var10000 = BackgroundKt.background-bw27NRU$default(ClipKt.clip(var10000, (Shape)RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv))), ColorKt.getSurfaceElevated(), (Shape)null, 2, (Object)null);
                                       boolean var10001 = false;
                                       Object var10002 = null;
                                       Object var10003 = null;
                                       $composer.startReplaceableGroup(-1524172302);
                                       ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
                                       boolean invalid$iv = $composer.changed(var7);
                                       int $i$f$cache = 0;
                                       Object it$iv = $composer.rememberedValue();
                                       int var39 = 0;
                                       Object var10004;
                                       if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
                                          var10004 = it$iv;
                                       } else {
                                          Object var40 = null;
                                          Object var41 = null;
                                          boolean var42 = false;
                                          Modifier var43 = var10000;
                                          int var44 = 0;
                                          Function0 value$iv = new Function0<Unit>() {
                                             public final void invoke() {
                                                var7.invoke("avatar");
                                             }
                                          };
                                          var10000 = var43;
                                          var10001 = var42;
                                          var10002 = var41;
                                          var10003 = var40;
                                          $composer.updateRememberedValue(value$iv);
                                          var10004 = value$iv;
                                       }

                                       Function0 modifier$ivx = (Function0)var10004;
                                       $composer.endReplaceableGroup();
                                       Modifier $this$dp$ivxxxxxx = ClickableKt.clickable-XHw0xAI$default(var10000, var10001, (String)var10002, (Role)var10003, modifier$ivx, 7, (Object)null);
                                       $i$f$cache = 0;
                                       int $i$f$Box = 0;
                                       $composer.startReplaceableGroup(733328855);
                                       ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
                                       Alignment contentAlignment$iv = Alignment.Companion.getTopStart();
                                       invalid$iv = false;
                                       MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(contentAlignment$iv, invalid$iv, $composer, 14 & $i$f$cache >> 3 | 112 & $i$f$cache >> 3);
                                       int $changed$iv$iv = 112 & $i$f$cache << 3;
                                       int $i$f$Layout = 0;
                                       $composer.startReplaceableGroup(-1323940314);
                                       ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                                       int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                                       CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                                       Function0 factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                                       Function3 skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf($this$dp$ivxxxxxx);
                                       int $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$iv << 9;
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
                                       int var54 = 0;
                                       Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                                       Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                                       Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                                       int var56 = 0;
                                       int var58 = 0;
                                       if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                                          $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                                          $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                                       }

                                       skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                                       $composer.startReplaceableGroup(2058660585);
                                       int $changed$ivxxxx = 14 & $changed$iv$iv$ivxx >> 9;
                                       int var61 = 0;
                                       ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                                       int $changedxx = 6 | 112 & $i$f$cache >> 6;
                                       BoxScope var131 = (BoxScope)BoxScopeInstance.INSTANCE;
                                       int var65 = 0;
                                       ComposerKt.sourceInformationMarkerStart($composer, -913406784, "C110@4599L170:HomeScreen.kt#k2q6ai");
                                       HuoLive2DViewKt.HuoLive2DView(var8, SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), $composer, 56, 0);
                                       ComposerKt.sourceInformationMarkerEnd($composer);
                                       ComposerKt.sourceInformationMarkerEnd($composer);
                                       $composer.endReplaceableGroup();
                                       $composer.endNode();
                                       $composer.endReplaceableGroup();
                                       $composer.endReplaceableGroup();
                                       Modifier var132 = (Modifier)Modifier.Companion;
                                       int $this$dp$iv = 16;
                                       int $i$f$getDp = 0;
                                       SpacerKt.Spacer(SizeKt.width-3ABfNKs(var132, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                                       Modifier var85 = RowScope.weight$default($this$invoke_u24lambda_u244, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                                       $i$f$cache = 0;
                                       $i$f$Box = 0;
                                       $composer.startReplaceableGroup(-483455358);
                                       ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                                       Arrangement.Vertical verticalArrangement$iv = Arrangement.INSTANCE.getTop();
                                       Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
                                       measurePolicy$iv = ColumnKt.columnMeasurePolicy(verticalArrangement$iv, horizontalAlignment$iv, $composer, 14 & $i$f$cache >> 3 | 112 & $i$f$cache >> 3);
                                       $changed$iv$iv = 112 & $i$f$cache << 3;
                                       $i$f$Layout = 0;
                                       $composer.startReplaceableGroup(-1323940314);
                                       ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                                       compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                                       localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                                       factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                                       skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(var85);
                                       $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$iv << 9;
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
                                       var54 = 0;
                                       Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                                       Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                                       block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                                       var56 = 0;
                                       var58 = 0;
                                       if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                                          $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                                          $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                                       }

                                       skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                                       $composer.startReplaceableGroup(2058660585);
                                       $changed$ivxxxx = 14 & $changed$iv$iv$ivxx >> 9;
                                       var61 = 0;
                                       ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                                       $changedxx = 6 | 112 & $i$f$cache >> 6;
                                       ColumnScope var133 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                                       var65 = 0;
                                       ComposerKt.sourceInformationMarkerStart($composer, -913017021, "C121@5078L10,119@4956L291,127@5403L10,125@5276L232,130@5537L40,133@5736L45,132@5656L22,131@5606L669:HomeScreen.kt#k2q6ai");
                                       TextStyle var66 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                                       FontWeight var67 = FontWeight.Companion.getBold();
                                       long var68 = ColorKt.getViernesAccent();
                                       TextKt.Text--4IGK_g("Avatar Oficial: HUO", (Modifier)null, var68, 0L, (FontStyle)null, var67, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var66, $composer, 196998, 0, 65498);
                                       String var116 = "Estado: " + HomeScreenKt.HomeScreen$lambda$3(var9).name();
                                       TextStyle var119 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                                       var68 = ColorKt.getTextSecondary();
                                       TextKt.Text--4IGK_g(var116, (Modifier)null, var68, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var119, $composer, 384, 0, 65530);
                                       Modifier var134 = (Modifier)Modifier.Companion;
                                       int $this$dp$iv = 6;
                                       int $i$f$getDp = 0;
                                       SpacerKt.Spacer(SizeKt.height-3ABfNKs(var134, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                                       ButtonColors var118 = ButtonDefaults.INSTANCE.buttonColors-ro_MJ88(ColorKt.getViernesPrimary(), 0L, 0L, 0L, $composer, 6 | ButtonDefaults.$stable << 12, 14);
                                       int $this$dp$iv = 12;
                                       int $i$f$getDp = 0;
                                       float var135 = Dp.constructor-impl((float)$this$dp$iv);
                                       $this$dp$iv = 6;
                                       $i$f$getDp = 0;
                                       PaddingValues var121 = PaddingKt.PaddingValues-YgX7TsA(var135, Dp.constructor-impl((float)$this$dp$iv));
                                       $i$f$getDp = 8;
                                       int $i$f$getDp = 0;
                                       RoundedCornerShape var124 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                                       $composer.startReplaceableGroup(-2107641041);
                                       ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
                                       boolean invalid$ivx = $composer.changed(var7);
                                       int $i$f$cache = 0;
                                       Object it$iv = $composer.rememberedValue();
                                       int var76 = 0;
                                       Object var136;
                                       if (!invalid$ivx && it$iv != Composer.Companion.getEmpty()) {
                                          var136 = it$iv;
                                       } else {
                                          int var77 = 0;
                                          Object value$iv = new Function0<Unit>() {
                                             public final void invoke() {
                                                var7.invoke("chat");
                                             }
                                          };
                                          $composer.updateRememberedValue(value$iv);
                                          var136 = value$iv;
                                       }

                                       Function0 var127 = (Function0)var136;
                                       $composer.endReplaceableGroup();
                                       ButtonKt.Button(var127, (Modifier)null, false, (Shape)var124, var118, (ButtonElevation)null, (BorderStroke)null, var121, (MutableInteractionSource)null, ComposableSingletons$HomeScreenKt.INSTANCE.getLambda-3$app_debug(), $composer, 817889280, 358);
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
                              if (ComposerKt.isTraceInProgress()) {
                                 ComposerKt.traceEventEnd();
                              }
                           }

                        }
                     }), 3, (Object)null);
                     LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, (Function3)ComposableLambdaKt.composableLambdaInstance(-920131503, true, new Function3<LazyItemScope, Composer, Integer, Unit>() {
                        @Composable
                        @ComposableTarget(
                           applier = "androidx.compose.ui.UiComposable"
                        )
                        public final void invoke(@NotNull LazyItemScope $this$item, @Nullable Composer $composer, int $changed) {
                           Intrinsics.checkNotNullParameter($this$item, "$this$item");
                           ComposerKt.sourceInformation($composer, "C150@6536L10,148@6436L231,154@6684L40,155@6741L495:HomeScreen.kt#k2q6ai");
                           if (($changed & 81) == 16 && $composer.getSkipping()) {
                              $composer.skipToGroupEnd();
                           } else {
                              if (ComposerKt.isTraceInProgress()) {
                                 ComposerKt.traceEventStart(-920131503, $changed, -1, "com.viernes.mobile.ui.screens.HomeScreen.<anonymous>.<anonymous>.<anonymous> (HomeScreen.kt:148)");
                              }

                              TextStyle var4 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                              FontWeight var5 = FontWeight.Companion.getBold();
                              long var6 = ColorKt.getTextPrimary();
                              TextKt.Text--4IGK_g("Pacientes Registrados", (Modifier)null, var6, 0L, (FontStyle)null, var5, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var4, $composer, 196998, 0, 65498);
                              Modifier var10000 = (Modifier)Modifier.Companion;
                              int $this$dp$iv = 8;
                              int $i$f$getDp = 0;
                              SpacerKt.Spacer(SizeKt.height-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                              Modifier var51 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                              $i$f$getDp = 12;
                              int $i$f$getDp = 0;
                              Arrangement.Horizontal var54 = (Arrangement.Horizontal)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                              State var7 = patients$delegate;
                              final Function1 var8 = onNavigate;
                              int $changed$iv = 54;
                              int $i$f$Row = 0;
                              $composer.startReplaceableGroup(693286680);
                              ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                              Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getTop();
                              MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(var54, verticalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                              int $changed$iv$iv = 112 & $changed$iv << 3;
                              int $i$f$Layout = 0;
                              $composer.startReplaceableGroup(-1323940314);
                              ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                              int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                              CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                              Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                              Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(var51);
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
                              int var21 = 0;
                              Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                              Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                              Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                              int var23 = 0;
                              int var25 = 0;
                              if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                                 $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                                 $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                              }

                              skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                              $composer.startReplaceableGroup(2058660585);
                              int var26 = 14 & $changed$iv$iv$iv >> 9;
                              int var28 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                              int var29 = 6 | 112 & $changed$iv >> 6;
                              Composer $composer = $composer;
                              RowScope $this$invoke_u24lambda_u242 = (RowScope)RowScopeInstance.INSTANCE;
                              int var32 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, 2027957336, "C:HomeScreen.kt#k2q6ai");
                              $composer.startReplaceableGroup(619607586);
                              ComposerKt.sourceInformation($composer, "*163@7131L39,160@6968L228");
                              Iterable $this$forEach$iv = (Iterable)HomeScreenKt.HomeScreen$lambda$1(var7);
                              int $i$f$forEach = 0;

                              for(Object element$iv : $this$forEach$iv) {
                                 final Patient patient = (Patient)element$iv;
                                 int var38 = 0;
                                 Patient var57 = patient;
                                 Modifier var10001 = RowScope.weight$default($this$invoke_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                                 $composer.startReplaceableGroup(-1524088671);
                                 ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
                                 boolean invalid$iv = $composer.changed(var8) | $composer.changed(patient);
                                 int $i$f$cache = 0;
                                 Object it$iv = $composer.rememberedValue();
                                 int var43 = 0;
                                 Object var10002;
                                 if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
                                    var10002 = it$iv;
                                 } else {
                                    Modifier var44 = var10001;
                                    int var46 = 0;
                                    Function0 value$iv = new Function0<Unit>() {
                                       public final void invoke() {
                                          var8.invoke("patient/" + patient.getId());
                                       }
                                    };
                                    var57 = patient;
                                    var10001 = var44;
                                    $composer.updateRememberedValue(value$iv);
                                    var10002 = value$iv;
                                 }

                                 Function0 var49 = (Function0)var10002;
                                 $composer.endReplaceableGroup();
                                 HomeScreenKt.PatientQuickCard(var57, var10001, var49, $composer, 0, 0);
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
                     LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, (Function3)ComposableLambdaKt.composableLambdaInstance(-1056158800, true, new Function3<LazyItemScope, Composer, Integer, Unit>() {
                        @Composable
                        @ComposableTarget(
                           applier = "androidx.compose.ui.UiComposable"
                        )
                        public final void invoke(@NotNull LazyItemScope $this$item, @Nullable Composer $composer, int $changed) {
                           Intrinsics.checkNotNullParameter($this$item, "$this$item");
                           ComposerKt.sourceInformation($composer, "C173@7423L10,171@7329L225,177@7571L40,178@7628L2187:HomeScreen.kt#k2q6ai");
                           if (($changed & 81) == 16 && $composer.getSkipping()) {
                              $composer.skipToGroupEnd();
                           } else {
                              if (ComposerKt.isTraceInProgress()) {
                                 ComposerKt.traceEventStart(-1056158800, $changed, -1, "com.viernes.mobile.ui.screens.HomeScreen.<anonymous>.<anonymous>.<anonymous> (HomeScreen.kt:171)");
                              }

                              TextStyle var4 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                              FontWeight var5 = FontWeight.Companion.getBold();
                              long var6 = ColorKt.getTextPrimary();
                              TextKt.Text--4IGK_g("Módulos Médicos", (Modifier)null, var6, 0L, (FontStyle)null, var5, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var4, $composer, 196998, 0, 65498);
                              Modifier var10000 = (Modifier)Modifier.Companion;
                              int $this$dp$iv = 8;
                              int $i$f$getDp = 0;
                              SpacerKt.Spacer(SizeKt.height-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                              $i$f$getDp = 10;
                              int $i$f$getDp = 0;
                              Arrangement.Vertical var78 = (Arrangement.Vertical)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                              final Function1 var7 = onNavigate;
                              int $changed$iv = 48;
                              int $i$f$Column = 0;
                              $composer.startReplaceableGroup(-483455358);
                              ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                              Modifier modifier$iv = (Modifier)Modifier.Companion;
                              Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
                              MeasurePolicy measurePolicy$iv = ColumnKt.columnMeasurePolicy(var78, horizontalAlignment$iv, $composer, 14 & $changed$iv >> 3 | 112 & $changed$iv >> 3);
                              int $changed$iv$ivx = 112 & $changed$iv << 3;
                              int $i$f$Layout = 0;
                              $composer.startReplaceableGroup(-1323940314);
                              ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                              int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                              CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                              Function0 factory$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
                              Function3 skippableUpdate$iv$iv$ivx = LayoutKt.modifierMaterializerOf(modifier$iv);
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
                              ColumnScope var145 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                              int var31 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, 2028800319, "C179@7708L1034,200@8763L1034:HomeScreen.kt#k2q6ai");
                              Modifier modifier$iv = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                              int $this$dp$iv = 10;
                              int $i$f$getDp = 0;
                              Arrangement.Horizontal horizontalArrangement$iv = (Arrangement.Horizontal)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                              byte $changed$ivxxx = 54;
                              int $i$f$Row = 0;
                              $composer.startReplaceableGroup(693286680);
                              ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                              Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getTop();
                              MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, verticalAlignment$iv, $composer, 14 & $changed$ivxxx >> 3 | 112 & $changed$ivxxx >> 3);
                              int $changed$iv$ivxx = 112 & $changed$ivxxx << 3;
                              int $i$f$Layout = 0;
                              $composer.startReplaceableGroup(-1323940314);
                              ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                              int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                              CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                              Function0 factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                              Function3 skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(modifier$iv);
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

                              skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                              $composer.startReplaceableGroup(2058660585);
                              int $changed$ivxxxx = 14 & $changed$iv$iv$ivxx >> 9;
                              int var54 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                              int $changedxx = 6 | 112 & $changed$ivxxx >> 6;
                              RowScope $this$invoke_u24lambda_u246_u24lambda_u242 = (RowScope)RowScopeInstance.INSTANCE;
                              int var58 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, -1324366, "C189@8235L32,183@7897L396,197@8661L33,191@8318L402:HomeScreen.kt#k2q6ai");
                              String var146 = "Centro Médico";
                              String var10001 = "Agenda del día";
                              ImageVector var10002 = MedicalServicesKt.getMedicalServices(Icons.INSTANCE.getDefault());
                              long var10003 = ColorKt.getViernesPrimary();
                              Modifier var10004 = RowScope.weight$default($this$invoke_u24lambda_u246_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                              $composer.startReplaceableGroup(-1524053350);
                              ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
                              boolean invalid$ivxxx = $composer.changed(var7);
                              int $i$f$cache = 0;
                              Object it$iv = $composer.rememberedValue();
                              int var63 = 0;
                              Object var10005;
                              if (!invalid$ivxxx && it$iv != Composer.Companion.getEmpty()) {
                                 var10005 = it$iv;
                              } else {
                                 Modifier var64 = var10004;
                                 long var65 = var10003;
                                 ImageVector var67 = var10002;
                                 String var68 = "Agenda del día";
                                 String var69 = "Centro Médico";
                                 int var70 = 0;
                                 Function0 value$iv = new Function0<Unit>() {
                                    public final void invoke() {
                                       var7.invoke("medical_center");
                                    }
                                 };
                                 var146 = var69;
                                 var10001 = var68;
                                 var10002 = var67;
                                 var10003 = var65;
                                 var10004 = var64;
                                 $composer.updateRememberedValue(value$iv);
                                 var10005 = value$iv;
                              }

                              Function0 var73 = (Function0)var10005;
                              $composer.endReplaceableGroup();
                              HomeScreenKt.ActionCard-fWhpE4E(var146, var10001, var10002, var10003, var10004, var73, $composer, 3126, 0);
                              var146 = "Escanear Receta";
                              var10001 = "OCR & Verificación";
                              var10002 = DocumentScannerKt.getDocumentScanner(Icons.INSTANCE.getDefault());
                              var10003 = ColorKt.getViernesAccent();
                              var10004 = RowScope.weight$default($this$invoke_u24lambda_u246_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                              $composer.startReplaceableGroup(-1524039717);
                              ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
                              invalid$ivxxx = $composer.changed(var7);
                              $i$f$cache = 0;
                              it$iv = $composer.rememberedValue();
                              var63 = 0;
                              if (!invalid$ivxxx && it$iv != Composer.Companion.getEmpty()) {
                                 var10005 = it$iv;
                              } else {
                                 Modifier var121 = var10004;
                                 long var124 = var10003;
                                 ImageVector var127 = var10002;
                                 String var130 = "OCR & Verificación";
                                 String var133 = "Escanear Receta";
                                 int var136 = 0;
                                 Function0 value$iv = new Function0<Unit>() {
                                    public final void invoke() {
                                       var7.invoke("recipe_import/1");
                                    }
                                 };
                                 var146 = var133;
                                 var10001 = var130;
                                 var10002 = var127;
                                 var10003 = var124;
                                 var10004 = var121;
                                 $composer.updateRememberedValue(value$iv);
                                 var10005 = value$iv;
                              }

                              var73 = (Function0)var10005;
                              $composer.endReplaceableGroup();
                              HomeScreenKt.ActionCard-fWhpE4E(var146, var10001, var10002, var10003, var10004, var73, $composer, 3126, 0);
                              ComposerKt.sourceInformationMarkerEnd($composer);
                              ComposerKt.sourceInformationMarkerEnd($composer);
                              $composer.endReplaceableGroup();
                              $composer.endNode();
                              $composer.endReplaceableGroup();
                              $composer.endReplaceableGroup();
                              modifier$iv = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                              int $this$dp$iv = 10;
                              int $i$f$getDp = 0;
                              Arrangement.Horizontal horizontalArrangement$ivx = (Arrangement.Horizontal)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                              $changed$ivxxx = 54;
                              $i$f$Row = 0;
                              $composer.startReplaceableGroup(693286680);
                              ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                              Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getTop();
                              measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$ivx, verticalAlignment$iv, $composer, 14 & $changed$ivxxx >> 3 | 112 & $changed$ivxxx >> 3);
                              $changed$iv$ivxx = 112 & $changed$ivxxx << 3;
                              $i$f$Layout = 0;
                              $composer.startReplaceableGroup(-1323940314);
                              ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                              compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                              localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                              factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                              skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(modifier$iv);
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
                              var47 = 0;
                              Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                              Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                              block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                              var49 = 0;
                              var51 = 0;
                              if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                                 $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                                 $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                              }

                              skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                              $composer.startReplaceableGroup(2058660585);
                              $changed$ivxxxx = 14 & $changed$iv$iv$ivxx >> 9;
                              var54 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                              $changedxx = 6 | 112 & $changed$ivxxx >> 6;
                              $this$invoke_u24lambda_u246_u24lambda_u242 = (RowScope)RowScopeInstance.INSTANCE;
                              var58 = 0;
                              ComposerKt.sourceInformationMarkerStart($composer, -277806, "C210@9299L29,204@8952L402,218@9717L32,212@9379L396:HomeScreen.kt#k2q6ai");
                              var146 = "Inventario & Retiros";
                              var10001 = "Existencias y farmacia";
                              var10002 = Inventory2Kt.getInventory2(Icons.INSTANCE.getDefault());
                              var10003 = ColorKt.getStatusPending();
                              var10004 = RowScope.weight$default($this$invoke_u24lambda_u246_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                              $composer.startReplaceableGroup(-1524019305);
                              ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
                              invalid$ivxxx = $composer.changed(var7);
                              $i$f$cache = 0;
                              it$iv = $composer.rememberedValue();
                              var63 = 0;
                              if (!invalid$ivxxx && it$iv != Composer.Companion.getEmpty()) {
                                 var10005 = it$iv;
                              } else {
                                 Modifier var122 = var10004;
                                 long var125 = var10003;
                                 ImageVector var128 = var10002;
                                 String var131 = "Existencias y farmacia";
                                 String var134 = "Inventario & Retiros";
                                 int var137 = 0;
                                 Function0 value$iv = new Function0<Unit>() {
                                    public final void invoke() {
                                       var7.invoke("inventory/1");
                                    }
                                 };
                                 var146 = var134;
                                 var10001 = var131;
                                 var10002 = var128;
                                 var10003 = var125;
                                 var10004 = var122;
                                 $composer.updateRememberedValue(value$iv);
                                 var10005 = value$iv;
                              }

                              var73 = (Function0)var10005;
                              $composer.endReplaceableGroup();
                              HomeScreenKt.ActionCard-fWhpE4E(var146, var10001, var10002, var10003, var10004, var73, $composer, 3126, 0);
                              var146 = "Citas Médicas";
                              var10001 = "Especialidades y fechas";
                              var10002 = EventKt.getEvent(Icons.INSTANCE.getDefault());
                              var10003 = ColorKt.getStatusConfirmed();
                              var10004 = RowScope.weight$default($this$invoke_u24lambda_u246_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
                              $composer.startReplaceableGroup(-1524005926);
                              ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
                              invalid$ivxxx = $composer.changed(var7);
                              $i$f$cache = 0;
                              it$iv = $composer.rememberedValue();
                              var63 = 0;
                              if (!invalid$ivxxx && it$iv != Composer.Companion.getEmpty()) {
                                 var10005 = it$iv;
                              } else {
                                 Modifier var123 = var10004;
                                 long var126 = var10003;
                                 ImageVector var129 = var10002;
                                 String var132 = "Especialidades y fechas";
                                 String var135 = "Citas Médicas";
                                 int var138 = 0;
                                 Function0 value$iv = new Function0<Unit>() {
                                    public final void invoke() {
                                       var7.invoke("appointments/1");
                                    }
                                 };
                                 var146 = var135;
                                 var10001 = var132;
                                 var10002 = var129;
                                 var10003 = var126;
                                 var10004 = var123;
                                 $composer.updateRememberedValue(value$iv);
                                 var10005 = value$iv;
                              }

                              var73 = (Function0)var10005;
                              $composer.endReplaceableGroup();
                              HomeScreenKt.ActionCard-fWhpE4E(var146, var10001, var10002, var10003, var10004, var73, $composer, 3126, 0);
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
                     }), 3, (Object)null);
                     LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$HomeScreenKt.INSTANCE.getLambda-4$app_debug(), 3, (Object)null);
                     if (HomeScreenKt.HomeScreen$lambda$2(upcomingIntakes$delegate).isEmpty()) {
                        LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$HomeScreenKt.INSTANCE.getLambda-6$app_debug(), 3, (Object)null);
                     } else {
                        List items$iv = HomeScreenKt.HomeScreen$lambda$2(upcomingIntakes$delegate);
                        Function1 var6 = onNavigate;
                        Function1 key$iv = null;
                        Function1 contentType$iv = HomeScreenKt$HomeScreen$2$1$invoke$$inlined$items$default$1.INSTANCE;
                        int $i$f$items = 0;
                        $this$LazyColumn.items(items$iv.size(), (Function1)null, new HomeScreenKt$HomeScreen$2$1$invoke$$inlined$items$default$3(contentType$iv, items$iv), (Function4)ComposableLambdaKt.composableLambdaInstance(-632812321, true, new HomeScreenKt$HomeScreen$2$1$invoke$$inlined$items$default$4(items$iv, var6)));
                     }

                     LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$HomeScreenKt.INSTANCE.getLambda-7$app_debug(), 3, (Object)null);
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

      ScopeUpdateScope var18 = $composer.endRestartGroup();
      if (var18 != null) {
         var18.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               HomeScreenKt.HomeScreen(patientRepo, intakeRepo, huoController, onNavigate, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void PatientQuickCard(@NotNull final Patient patient, @Nullable final Modifier modifier, @NotNull final Function0<Unit> onClick, @Nullable Composer $composer, final int $changed, final int var5) {
      Intrinsics.checkNotNullParameter(patient, "patient");
      Intrinsics.checkNotNullParameter(onClick, "onClick");
      $composer = $composer.startRestartGroup(2002555679);
      ComposerKt.sourceInformation($composer, "C(PatientQuickCard)P(2)276@11659L13,277@11704L40,275@11615L1164:HomeScreen.kt#k2q6ai");
      int $dirty = $changed;
      if ((var5 & 1) != 0) {
         $dirty = $changed | 6;
      } else if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(patient) ? 4 : 2);
      }

      if ((var5 & 2) != 0) {
         $dirty |= 48;
      } else if (($changed & 112) == 0) {
         $dirty |= $composer.changed(modifier) ? 32 : 16;
      }

      if ((var5 & 4) != 0) {
         $dirty |= 384;
      } else if (($changed & 896) == 0) {
         $dirty |= $composer.changedInstance(onClick) ? 256 : 128;
      }

      if (($dirty & 731) == 146 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if ((var5 & 2) != 0) {
            modifier = (Modifier)Modifier.Companion;
         }

         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(2002555679, $dirty, -1, "com.viernes.mobile.ui.screens.PatientQuickCard (HomeScreen.kt:274)");
         }

         Modifier var10000 = modifier;
         boolean var10001 = false;
         Object var10002 = null;
         Object var10003 = null;
         $composer.startReplaceableGroup(-1171299655);
         ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
         boolean invalid$iv = ($dirty & 896) == 256;
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
            int var14 = 0;
            Function0 value$iv = new Function0<Unit>() {
               public final void invoke() {
                  onClick.invoke();
               }
            };
            var10000 = modifier;
            var10001 = var17;
            var10002 = var18;
            var10003 = var19;
            $composer.updateRememberedValue(value$iv);
            var10004 = value$iv;
         }

         Function0 var8 = (Function0)var10004;
         $composer.endReplaceableGroup();
         Modifier var7 = ClickableKt.clickable-XHw0xAI$default(var10000, var10001, (String)var10002, (Role)var10003, var8, 7, (Object)null);
         CardColors var22 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
         invalid$iv = (boolean)12;
         $i$f$cache = 0;
         RoundedCornerShape $this$cache$iv = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)invalid$iv));
         CardKt.Card(var7, (Shape)$this$cache$iv, var22, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 2062533265, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
               ComposerKt.sourceInformation($composer, "C280@11804L969:HomeScreen.kt#k2q6ai");
               if (($changed & 81) == 16 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(2062533265, $changed, -1, "com.viernes.mobile.ui.screens.PatientQuickCard.<anonymous> (HomeScreen.kt:280)");
                  }

                  Modifier var10000 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  int $this$dp$iv = 14;
                  int $i$f$getDp = 0;
                  Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                  Patient var7 = patient;
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
                  ColumnScope var79 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  int var31 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -2051256422, "C285@11932L595,300@12540L40,303@12690L10,301@12593L170:HomeScreen.kt#k2q6ai");
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

                  skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int var52 = 14 & $changed$iv$iv$iv >> 9;
                  int var54 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                  int var55 = 6 | 112 & $changed$iv >> 6;
                  RowScope var80 = (RowScope)RowScopeInstance.INSTANCE;
                  int var58 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 1725707515, "C286@12002L207,292@12226L39,295@12378L10,293@12282L231:HomeScreen.kt#k2q6ai");
                  ImageVector var59 = PersonKt.getPerson(Icons.INSTANCE.getDefault());
                  long var60 = ColorKt.getViernesPrimary();
                  Modifier var81 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 20;
                  int $i$f$getDp = 0;
                  Modifier var64 = SizeKt.size-3ABfNKs(var81, Dp.constructor-impl((float)$this$dp$iv));
                  IconKt.Icon-ww6aTOc(var59, (String)null, var64, var60, $composer, 3504, 0);
                  var81 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 6;
                  int $i$f$getDp = 0;
                  SpacerKt.Spacer(SizeKt.width-3ABfNKs(var81, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                  String var77 = var7.getDisplayName();
                  TextStyle var78 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                  FontWeight var66 = FontWeight.Companion.getSemiBold();
                  long var67 = ColorKt.getTextPrimary();
                  TextKt.Text--4IGK_g(var77, (Modifier)null, var67, 0L, (FontStyle)null, var66, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var78, $composer, 196992, 0, 65498);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  $composer.endReplaceableGroup();
                  $composer.endNode();
                  $composer.endReplaceableGroup();
                  $composer.endReplaceableGroup();
                  var81 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 4;
                  int $i$f$getDp = 0;
                  SpacerKt.Spacer(SizeKt.height-3ABfNKs(var81, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                  TextStyle var74 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                  long var69 = ColorKt.getTextSecondary();
                  TextKt.Text--4IGK_g("Toca para ver tratamientos", (Modifier)null, var69, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var74, $composer, 390, 0, 65530);
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

      ScopeUpdateScope var25 = $composer.endRestartGroup();
      if (var25 != null) {
         var25.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               HomeScreenKt.PatientQuickCard(patient, modifier, onClick, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1), var5);
            }
         });
      }

   }

   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void ActionCard_fWhpE4E/* $FF was: ActionCard-fWhpE4E*/(@NotNull final String title, @NotNull final String subtitle, @NotNull final ImageVector icon, final long color, @Nullable final Modifier modifier, @NotNull final Function0<Unit> onClick, @Nullable Composer $composer, final int $changed, final int var9) {
      Intrinsics.checkNotNullParameter(title, "title");
      Intrinsics.checkNotNullParameter(subtitle, "subtitle");
      Intrinsics.checkNotNullParameter(icon, "icon");
      Intrinsics.checkNotNullParameter(onClick, "onClick");
      $composer = $composer.startRestartGroup(-1751073247);
      ComposerKt.sourceInformation($composer, "C(ActionCard)P(5,4,1,0:c#ui.graphics.Color)320@13004L13,321@13049L40,319@12960L1083:HomeScreen.kt#k2q6ai");
      int $dirty = $changed;
      if ((var9 & 1) != 0) {
         $dirty = $changed | 6;
      } else if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(title) ? 4 : 2);
      }

      if ((var9 & 2) != 0) {
         $dirty |= 48;
      } else if (($changed & 112) == 0) {
         $dirty |= $composer.changed(subtitle) ? 32 : 16;
      }

      if ((var9 & 4) != 0) {
         $dirty |= 384;
      } else if (($changed & 896) == 0) {
         $dirty |= $composer.changed(icon) ? 256 : 128;
      }

      if ((var9 & 8) != 0) {
         $dirty |= 3072;
      } else if (($changed & 7168) == 0) {
         $dirty |= $composer.changed(color) ? 2048 : 1024;
      }

      if ((var9 & 16) != 0) {
         $dirty |= 24576;
      } else if (($changed & '\ue000') == 0) {
         $dirty |= $composer.changed(modifier) ? 16384 : 8192;
      }

      if ((var9 & 32) != 0) {
         $dirty |= 196608;
      } else if (($changed & 458752) == 0) {
         $dirty |= $composer.changedInstance(onClick) ? 131072 : 65536;
      }

      if (($dirty & 374491) == 74898 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if ((var9 & 16) != 0) {
            modifier = (Modifier)Modifier.Companion;
         }

         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(-1751073247, $dirty, -1, "com.viernes.mobile.ui.screens.ActionCard (HomeScreen.kt:318)");
         }

         Modifier var10000 = modifier;
         boolean var10001 = false;
         Object var10002 = null;
         Object var10003 = null;
         $composer.startReplaceableGroup(378136487);
         ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
         boolean invalid$iv = ($dirty & 458752) == 131072;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var17 = 0;
         Object var10004;
         if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
            var10004 = it$iv;
         } else {
            Object var23 = null;
            Object var22 = null;
            boolean var21 = false;
            int var18 = 0;
            Function0 value$iv = new Function0<Unit>() {
               public final void invoke() {
                  onClick.invoke();
               }
            };
            var10000 = modifier;
            var10001 = var21;
            var10002 = var22;
            var10003 = var23;
            $composer.updateRememberedValue(value$iv);
            var10004 = value$iv;
         }

         Function0 var12 = (Function0)var10004;
         $composer.endReplaceableGroup();
         Modifier var11 = ClickableKt.clickable-XHw0xAI$default(var10000, var10001, (String)var10002, (Role)var10003, var12, 7, (Object)null);
         CardColors var26 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
         invalid$iv = (boolean)12;
         $i$f$cache = 0;
         RoundedCornerShape $this$cache$iv = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)invalid$iv));
         CardKt.Card(var11, (Shape)$this$cache$iv, var26, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, -632965869, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
               ComposerKt.sourceInformation($composer, "C324@13149L888:HomeScreen.kt#k2q6ai");
               if (($changed & 81) == 16 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-632965869, $changed, -1, "com.viernes.mobile.ui.screens.ActionCard.<anonymous> (HomeScreen.kt:324)");
                  }

                  Modifier var10000 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  int $this$dp$iv = 14;
                  int $i$f$getDp = 0;
                  Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                  Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                  long var7 = color;
                  ImageVector var9 = icon;
                  String var10 = title;
                  String var11 = subtitle;
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
                  Function0 factory$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
                  Function3 skippableUpdate$iv$iv$ivx = LayoutKt.modifierMaterializerOf(modifier$iv);
                  int $changed$iv$iv$ivx = 6 | 7168 & $changed$iv$iv << 9;
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

                  skippableUpdate$iv$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int var29 = 14 & $changed$iv$iv$ivx >> 9;
                  int var31 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                  int var32 = 6 | 112 & $changed$iv >> 6;
                  RowScope var104 = (RowScope)RowScopeInstance.INSTANCE;
                  int var35 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -806879594, "C330@13334L368,339@13715L40,340@13768L259:HomeScreen.kt#k2q6ai");
                  Modifier var105 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 40;
                  int $i$f$getDp = 0;
                  var105 = SizeKt.size-3ABfNKs(var105, Dp.constructor-impl((float)$this$dp$iv));
                  $this$dp$iv = 8;
                  $i$f$getDp = 0;
                  Modifier modifier$ivx = BackgroundKt.background-bw27NRU$default(ClipKt.clip(var105, (Shape)RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv))), Color.copy-wmQWz5c$default(var7, 0.15F, 0.0F, 0.0F, 0.0F, 14, (Object)null), (Shape)null, 2, (Object)null);
                  Alignment contentAlignment$iv = Alignment.Companion.getCenter();
                  byte $changed$ivxx = 48;
                  int $i$f$Box = 0;
                  $composer.startReplaceableGroup(733328855);
                  ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
                  boolean propagateMinConstraints$iv = false;
                  MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(contentAlignment$iv, propagateMinConstraints$iv, $composer, 14 & $changed$ivxx >> 3 | 112 & $changed$ivxx >> 3);
                  int $changed$iv$ivx = 112 & $changed$ivxx << 3;
                  int $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  Function0 factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                  Function3 skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(modifier$ivx);
                  int $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$ivx << 9;
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
                  int var51 = 0;
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                  Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                  int var53 = 0;
                  int var55 = 0;
                  if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                     $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                     $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                  }

                  skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int $changed$ivxxx = 14 & $changed$iv$iv$ivxx >> 9;
                  int var58 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                  int $changedxx = 6 | 112 & $changed$ivxx >> 6;
                  BoxScope var107 = (BoxScope)BoxScopeInstance.INSTANCE;
                  int var62 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 1296952568, "C337@13604L84:HomeScreen.kt#k2q6ai");
                  Modifier var108 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 24;
                  int $i$f$getDp = 0;
                  Modifier var65 = SizeKt.size-3ABfNKs(var108, Dp.constructor-impl((float)$this$dp$iv));
                  IconKt.Icon-ww6aTOc(var9, (String)null, var65, var7, $composer, 432, 0);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  $composer.endReplaceableGroup();
                  $composer.endNode();
                  $composer.endReplaceableGroup();
                  $composer.endReplaceableGroup();
                  var108 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 12;
                  int $i$f$getDp = 0;
                  SpacerKt.Spacer(SizeKt.width-3ABfNKs(var108, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                  $changed$ivxx = 0;
                  $i$f$Box = 0;
                  $composer.startReplaceableGroup(-483455358);
                  ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                  Modifier modifier$iv = (Modifier)Modifier.Companion;
                  Arrangement.Vertical verticalArrangement$iv = Arrangement.INSTANCE.getTop();
                  Alignment.Horizontal horizontalAlignment$iv = Alignment.Companion.getStart();
                  measurePolicy$iv = ColumnKt.columnMeasurePolicy(verticalArrangement$iv, horizontalAlignment$iv, $composer, 14 & $changed$ivxx >> 3 | 112 & $changed$ivxx >> 3);
                  $changed$iv$ivx = 112 & $changed$ivxx << 3;
                  $i$f$Layout = 0;
                  $composer.startReplaceableGroup(-1323940314);
                  ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                  compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                  localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                  factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                  skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(modifier$iv);
                  $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$ivx << 9;
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
                  var51 = 0;
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                  block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                  var53 = 0;
                  var55 = 0;
                  if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                     $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                     $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                  }

                  skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  $changed$ivxxx = 14 & $changed$iv$iv$ivxx >> 9;
                  var58 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                  $changedxx = 6 | 112 & $changed$ivxx >> 6;
                  ColumnScope var110 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  var62 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 1297144272, "C341@13834L10,341@13793L114,342@13968L10,342@13924L89:HomeScreen.kt#k2q6ai");
                  TextStyle var101 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleSmall();
                  FontWeight var103 = FontWeight.Companion.getBold();
                  long var66 = ColorKt.getTextPrimary();
                  TextKt.Text--4IGK_g(var10, (Modifier)null, var66, 0L, (FontStyle)null, var103, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var101, $composer, 196992, 0, 65498);
                  var101 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getLabelSmall();
                  long var68 = ColorKt.getTextSecondary();
                  TextKt.Text--4IGK_g(var11, (Modifier)null, var68, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var101, $composer, 384, 0, 65530);
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

      ScopeUpdateScope var29 = $composer.endRestartGroup();
      if (var29 != null) {
         var29.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               HomeScreenKt.ActionCard-fWhpE4E(title, subtitle, icon, color, modifier, onClick, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1), var9);
            }
         });
      }

   }

   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void IntakeItemCard(@NotNull final Intake intake, @NotNull final Function0<Unit> onClick, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(intake, "intake");
      Intrinsics.checkNotNullParameter(onClick, "onClick");
      $composer = $composer.startRestartGroup(79275318);
      ComposerKt.sourceInformation($composer, "C(IntakeItemCard)356@14216L13,357@14261L40,353@14131L1717:HomeScreen.kt#k2q6ai");
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
            ComposerKt.traceEventStart(79275318, $dirty, -1, "com.viernes.mobile.ui.screens.IntakeItemCard (HomeScreen.kt:352)");
         }

         Modifier var10000 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
         boolean var10001 = false;
         Object var10002 = null;
         Object var10003 = null;
         $composer.startReplaceableGroup(-773069680);
         ComposerKt.sourceInformation($composer, "CC(remember):HomeScreen.kt#9igjgp");
         boolean invalid$iv = ($dirty & 112) == 32;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var11 = 0;
         Object var10004;
         if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
            var10004 = it$iv;
         } else {
            Object var17 = null;
            Object var16 = null;
            boolean var15 = false;
            Modifier var14 = var10000;
            int var12 = 0;
            Function0 value$iv = new Function0<Unit>() {
               public final void invoke() {
                  onClick.invoke();
               }
            };
            var10000 = var14;
            var10001 = var15;
            var10002 = var16;
            var10003 = var17;
            $composer.updateRememberedValue(value$iv);
            var10004 = value$iv;
         }

         Function0 var6 = (Function0)var10004;
         $composer.endReplaceableGroup();
         Modifier var5 = ClickableKt.clickable-XHw0xAI$default(var10000, var10001, (String)var10002, (Role)var10003, var6, 7, (Object)null);
         CardColors var20 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
         invalid$iv = (boolean)12;
         $i$f$cache = 0;
         RoundedCornerShape $this$cache$iv = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)invalid$iv));
         CardKt.Card(var5, (Shape)$this$cache$iv, var20, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1871900584, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
               ComposerKt.sourceInformation($composer, "C360@14361L1481:HomeScreen.kt#k2q6ai");
               if (($changed & 81) == 16 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(1871900584, $changed, -1, "com.viernes.mobile.ui.screens.IntakeItemCard.<anonymous> (HomeScreen.kt:360)");
                  }

                  Modifier var10000 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  int $this$dp$iv = 14;
                  int $i$f$getDp = 0;
                  Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                  Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                  Intake var7 = intake;
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
                  Function0 factory$iv$iv$ivx = ComposeUiNode.Companion.getConstructor();
                  Function3 skippableUpdate$iv$iv$ivx = LayoutKt.modifierMaterializerOf(modifier$iv);
                  int $changed$iv$iv$ivx = 6 | 7168 & $changed$iv$iv << 9;
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
                  RowScope $this$invoke_u24lambda_u242 = (RowScope)RowScopeInstance.INSTANCE;
                  int var31 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 1940386204, "C366@14546L592,380@15151L40,381@15204L534,394@15751L81:HomeScreen.kt#k2q6ai");
                  var10000 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 48;
                  int $i$f$getDp = 0;
                  Modifier modifier$ivx = BackgroundKt.background-bw27NRU$default(ClipKt.clip(SizeKt.size-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), (Shape)RoundedCornerShapeKt.getCircleShape()), var7.isDelayed() ? Color.copy-wmQWz5c$default(ColorKt.getStatusDelayed(), 0.2F, 0.0F, 0.0F, 0.0F, 14, (Object)null) : Color.copy-wmQWz5c$default(ColorKt.getStatusPending(), 0.2F, 0.0F, 0.0F, 0.0F, 14, (Object)null), (Shape)null, 2, (Object)null);
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
                  Function0 factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                  Function3 skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(modifier$ivx);
                  int $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$ivx << 9;
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

                  skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  int $changed$ivxxx = 14 & $changed$iv$iv$ivxx >> 9;
                  int var54 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
                  int $changedxx = 6 | 112 & $changed$iv >> 6;
                  BoxScope var104 = (BoxScope)BoxScopeInstance.INSTANCE;
                  int var58 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 1296900997, "C373@14870L254:HomeScreen.kt#k2q6ai");
                  String var105 = var7.getScheduledTime();
                  if (var105 == null) {
                     var105 = "--:--";
                  }

                  String var59 = var105;
                  FontWeight var60 = FontWeight.Companion.getBold();
                  long var61 = var7.isDelayed() ? ColorKt.getStatusDelayed() : ColorKt.getStatusPending();
                  long var63 = TextUnitKt.getSp(13);
                  TextKt.Text--4IGK_g(var59, (Modifier)null, var61, var63, (FontStyle)null, var60, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 199680, 0, 131026);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  $composer.endReplaceableGroup();
                  $composer.endNode();
                  $composer.endReplaceableGroup();
                  $composer.endReplaceableGroup();
                  Modifier var106 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 14;
                  int $i$f$getDp = 0;
                  SpacerKt.Spacer(SizeKt.width-3ABfNKs(var106, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
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
                  factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                  skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(modifier$ivxx);
                  $changed$iv$iv$ivxx = 6 | 7168 & $changed$iv$ivx << 9;
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
                  var47 = 0;
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                  Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                  block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                  var49 = 0;
                  var51 = 0;
                  if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                     $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                     $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                  }

                  skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                  $composer.startReplaceableGroup(2058660585);
                  $changed$ivxxx = 14 & $changed$iv$iv$ivxx >> 9;
                  var54 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                  $changedxx = 6 | 112 & $changed$iv >> 6;
                  ColumnScope var107 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  var58 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 1297295348, "C384@15385L10,382@15261L255,390@15643L10,388@15533L191:HomeScreen.kt#k2q6ai");
                  String var108 = var7.getMedicationName();
                  var59 = var108 + " (" + var7.getDoseText() + ")";
                  TextStyle var101 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                  FontWeight var65 = FontWeight.Companion.getBold();
                  long var66 = ColorKt.getTextPrimary();
                  TextKt.Text--4IGK_g(var59, (Modifier)null, var66, 0L, (FontStyle)null, var65, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var101, $composer, 196992, 0, 65498);
                  var59 = "Paciente: " + var7.getPatientName();
                  var101 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                  long var68 = ColorKt.getTextSecondary();
                  TextKt.Text--4IGK_g(var59, (Modifier)null, var68, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var101, $composer, 384, 0, 65530);
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

      ScopeUpdateScope var23 = $composer.endRestartGroup();
      if (var23 != null) {
         var23.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               HomeScreenKt.IntakeItemCard(intake, onClick, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   private static final List<Patient> HomeScreen$lambda$1(State<? extends List<Patient>> $patients$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$patients$delegate.getValue();
   }

   private static final List<Intake> HomeScreen$lambda$2(State<? extends List<Intake>> $upcomingIntakes$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$upcomingIntakes$delegate.getValue();
   }

   private static final HuoState HomeScreen$lambda$3(State<? extends HuoState> $huoState$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (HuoState)$huoState$delegate.getValue();
   }
}
