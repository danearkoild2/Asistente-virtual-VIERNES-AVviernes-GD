package com.viernes.mobile.ui.screens;

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
import androidx.compose.material.icons.Icons;
import androidx.compose.material.icons.filled.FaceKt;
import androidx.compose.material.icons.filled.PlayArrowKt;
import androidx.compose.material3.AppBarKt;
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
import androidx.compose.ui.graphics.Color;
import androidx.compose.ui.graphics.Shape;
import androidx.compose.ui.graphics.vector.ImageVector;
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
import androidx.compose.ui.unit.TextUnitKt;
import com.viernes.mobile.avatar.HuoAvatarController;
import com.viernes.mobile.avatar.HuoLive2DViewKt;
import com.viernes.mobile.avatar.HuoState;
import com.viernes.mobile.ui.theme.ColorKt;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.coroutines.CoroutineContext;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.functions.Function3;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.reflect.KProperty;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 2,
   xi = 48,
   d1 = {"\u0000\"\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\u001a#\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\f\u0010\u0004\u001a\b\u0012\u0004\u0012\u00020\u00010\u0005H\u0007¢\u0006\u0002\u0010\u0006¨\u0006\u0007²\u0006\n\u0010\b\u001a\u00020\tX\u008a\u0084\u0002²\u0006\n\u0010\n\u001a\u00020\u000bX\u008a\u0084\u0002²\u0006\n\u0010\f\u001a\u00020\u000bX\u008a\u0084\u0002"},
   d2 = {"HuoAvatarScreen", "", "huoController", "Lcom/viernes/mobile/avatar/HuoAvatarController;", "onNavigateBack", "Lkotlin/Function0;", "(Lcom/viernes/mobile/avatar/HuoAvatarController;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "app_debug", "state", "Lcom/viernes/mobile/avatar/HuoState;", "currentMotion", "", "currentExpression"}
)
@SourceDebugExtension({"SMAP\nHuoAvatarScreen.kt\nKotlin\n*S Kotlin\n*F\n+ 1 HuoAvatarScreen.kt\ncom/viernes/mobile/ui/screens/HuoAvatarScreenKt\n+ 2 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,150:1\n81#2:151\n81#2:152\n81#2:153\n*S KotlinDebug\n*F\n+ 1 HuoAvatarScreen.kt\ncom/viernes/mobile/ui/screens/HuoAvatarScreenKt\n*L\n30#1:151\n31#1:152\n32#1:153\n*E\n"})
public final class HuoAvatarScreenKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void HuoAvatarScreen(@NotNull final HuoAvatarController huoController, @NotNull final Function0<Unit> onNavigateBack, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(huoController, "huoController");
      Intrinsics.checkNotNullParameter(onNavigateBack, "onNavigateBack");
      $composer = $composer.startRestartGroup(-1578702795);
      ComposerKt.sourceInformation($composer, "C(HuoAvatarScreen)29@1137L16,30@1207L16,31@1285L16,33@1307L5351:HuoAvatarScreen.kt#k2q6ai");
      if (ComposerKt.isTraceInProgress()) {
         ComposerKt.traceEventStart(-1578702795, $changed, -1, "com.viernes.mobile.ui.screens.HuoAvatarScreen (HuoAvatarScreen.kt:28)");
      }

      final State state$delegate = SnapshotStateKt.collectAsState(huoController.getCurrentState(), (CoroutineContext)null, $composer, 8, 1);
      final State currentMotion$delegate = SnapshotStateKt.collectAsState(huoController.getCurrentMotion(), (CoroutineContext)null, $composer, 8, 1);
      final State currentExpression$delegate = SnapshotStateKt.collectAsState(huoController.getCurrentExpression(), (CoroutineContext)null, $composer, 8, 1);
      ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 1240589041, true, new Function2<Composer, Integer, Unit>() {
         @Composable
         @ComposableTarget(
            applier = "androidx.compose.ui.UiComposable"
         )
         public final void invoke(@Nullable Composer $composer, int $changed) {
            ComposerKt.sourceInformation($composer, "C42@1760L48,35@1348L474:HuoAvatarScreen.kt#k2q6ai");
            if (($changed & 11) == 2 && $composer.getSkipping()) {
               $composer.skipToGroupEnd();
            } else {
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventStart(1240589041, $changed, -1, "com.viernes.mobile.ui.screens.HuoAvatarScreen.<anonymous> (HuoAvatarScreen.kt:35)");
               }

               AppBarKt.TopAppBar(ComposableSingletons$HuoAvatarScreenKt.INSTANCE.getLambda-1$app_debug(), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -2011671753, true, new Function2<Composer, Integer, Unit>() {
                  @Composable
                  @ComposableTarget(
                     applier = "androidx.compose.ui.UiComposable"
                  )
                  public final void invoke(@Nullable Composer $composer, int $changed) {
                     ComposerKt.sourceInformation($composer, "C38@1530L167:HuoAvatarScreen.kt#k2q6ai");
                     if (($changed & 11) == 2 && $composer.getSkipping()) {
                        $composer.skipToGroupEnd();
                     } else {
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventStart(-2011671753, $changed, -1, "com.viernes.mobile.ui.screens.HuoAvatarScreen.<anonymous>.<anonymous> (HuoAvatarScreen.kt:38)");
                        }

                        IconButtonKt.IconButton(onNavigateBack, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$HuoAvatarScreenKt.INSTANCE.getLambda-2$app_debug(), $composer, 196608, 30);
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
      }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, 2106509510, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
         @Composable
         @ComposableTarget(
            applier = "androidx.compose.ui.UiComposable"
         )
         public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
            Intrinsics.checkNotNullParameter(padding, "padding");
            ComposerKt.sourceInformation($composer, "C47@1901L4751:HuoAvatarScreen.kt#k2q6ai");
            int $dirty = $changed;
            if (($changed & 14) == 0) {
               $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
            }

            if (($dirty & 91) == 18 && $composer.getSkipping()) {
               $composer.skipToGroupEnd();
            } else {
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventStart(2106509510, $dirty, -1, "com.viernes.mobile.ui.screens.HuoAvatarScreen.<anonymous> (HuoAvatarScreen.kt:47)");
               }

               Modifier modifier$iv = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
               final HuoAvatarController var8 = huoController;
               final State var9 = state$delegate;
               final State var10 = currentMotion$delegate;
               final State var11 = currentExpression$delegate;
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
               ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
               int var32 = 6 | 112 & $changed$iv >> 6;
               ColumnScope $this$invoke_u24lambda_u241 = (ColumnScope)ColumnScopeInstance.INSTANCE;
               int var35 = 0;
               ComposerKt.sourceInformationMarkerStart($composer, -1127872326, "C53@2074L1144,83@3389L40,81@3293L3349:HuoAvatarScreen.kt#k2q6ai");
               Modifier modifier$ivx = BackgroundKt.background-bw27NRU$default(ColumnScope.weight$default($this$invoke_u24lambda_u241, SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), 1.0F, false, 2, (Object)null), ColorKt.getBackgroundDark(), (Shape)null, 2, (Object)null);
               int $this$dp$iv = 0;
               int $i$f$Box = 0;
               $composer.startReplaceableGroup(733328855);
               ComposerKt.sourceInformation($composer, "CC(Box)P(2,1,3)71@3309L67,72@3381L130:Box.kt#2w3rfo");
               Alignment contentAlignment$iv = Alignment.Companion.getTopStart();
               boolean propagateMinConstraints$iv = false;
               MeasurePolicy measurePolicy$iv = BoxKt.rememberBoxMeasurePolicy(contentAlignment$iv, propagateMinConstraints$iv, $composer, 14 & $this$dp$iv >> 3 | 112 & $this$dp$iv >> 3);
               int $changed$iv$ivx = 112 & $this$dp$iv << 3;
               int $i$f$Layout = 0;
               $composer.startReplaceableGroup(-1323940314);
               ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
               int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
               CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
               Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
               Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$ivx);
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

               skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
               $composer.startReplaceableGroup(2058660585);
               int var56 = 14 & $changed$iv$iv$iv >> 9;
               int var58 = 0;
               ComposerKt.sourceInformationMarkerStart($composer, -1253629263, "C73@3426L9:Box.kt#2w3rfo");
               int var59 = 6 | 112 & $this$dp$iv >> 6;
               BoxScope $this$invoke_u24lambda_u241_u24lambda_u240 = (BoxScope)BoxScopeInstance.INSTANCE;
               int var62 = 0;
               ComposerKt.sourceInformationMarkerStart($composer, -1961792186, "C59@2263L134,69@2637L60,65@2459L745:HuoAvatarScreen.kt#k2q6ai");
               HuoLive2DViewKt.HuoLive2DView(var8, SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), $composer, 56, 0);
               Modifier var10001 = (Modifier)Modifier.Companion;
               int $this$dp$iv = 16;
               int $i$f$getDp = 0;
               Modifier var65 = $this$invoke_u24lambda_u241_u24lambda_u240.align(PaddingKt.padding-3ABfNKs(var10001, Dp.constructor-impl((float)$this$dp$iv)), Alignment.Companion.getTopEnd());
               CardColors var75 = CardDefaults.INSTANCE.cardColors-ro_MJ88(Color.copy-wmQWz5c$default(ColorKt.getSurfaceDark(), 0.85F, 0.0F, 0.0F, 0.0F, 14, (Object)null), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
               int $this$dp$iv = 8;
               int $i$f$getDp = 0;
               RoundedCornerShape var76 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
               CardKt.Card(var65, (Shape)var76, var75, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1558025908, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                  @Composable
                  @ComposableTarget(
                     applier = "androidx.compose.ui.UiComposable"
                  )
                  public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                     Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                     ComposerKt.sourceInformation($composer, "C72@2792L394:HuoAvatarScreen.kt#k2q6ai");
                     if (($changed & 81) == 16 && $composer.getSkipping()) {
                        $composer.skipToGroupEnd();
                     } else {
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventStart(1558025908, $changed, -1, "com.viernes.mobile.ui.screens.HuoAvatarScreen.<anonymous>.<anonymous>.<anonymous>.<anonymous> (HuoAvatarScreen.kt:72)");
                        }

                        Modifier var10000 = (Modifier)Modifier.Companion;
                        int $this$dp$iv = 10;
                        int $i$f$getDp = 0;
                        Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                        State var7 = var9;
                        State var8 = var10;
                        State var9x = var11;
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
                        ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                        int var30 = 6 | 112 & $changed$iv >> 6;
                        ColumnScope var42 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                        int var33 = 0;
                        ComposerKt.sourceInformationMarkerStart($composer, -500314234, "C73@2861L100,74@2986L75,75@3086L78:HuoAvatarScreen.kt#k2q6ai");
                        String var34 = "Estado: " + HuoAvatarScreenKt.HuoAvatarScreen$lambda$0(var7).name();
                        FontWeight var35 = FontWeight.Companion.getBold();
                        long var36 = ColorKt.getViernesAccent();
                        long var38 = TextUnitKt.getSp(12);
                        TextKt.Text--4IGK_g(var34, (Modifier)null, var36, var38, (FontStyle)null, var35, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 200064, 0, 131026);
                        TextKt.Text--4IGK_g("Movimiento: " + HuoAvatarScreenKt.HuoAvatarScreen$lambda$1(var8), (Modifier)null, ColorKt.getTextSecondary(), TextUnitKt.getSp(11), (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 3456, 0, 131058);
                        TextKt.Text--4IGK_g("Expresión: " + HuoAvatarScreenKt.HuoAvatarScreen$lambda$2(var9x), (Modifier)null, ColorKt.getTextSecondary(), TextUnitKt.getSp(11), (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 3456, 0, 131058);
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
               ComposerKt.sourceInformationMarkerEnd($composer);
               ComposerKt.sourceInformationMarkerEnd($composer);
               $composer.endReplaceableGroup();
               $composer.endNode();
               $composer.endReplaceableGroup();
               $composer.endReplaceableGroup();
               modifier$ivx = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
               CardColors var73 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
               $this$dp$iv = 20;
               $i$f$Box = 0;
               float var10000 = Dp.constructor-impl((float)$this$dp$iv);
               $this$dp$iv = 20;
               $i$f$Box = 0;
               RoundedCornerShape var74 = RoundedCornerShapeKt.RoundedCornerShape-a9UjIt4$default(var10000, Dp.constructor-impl((float)$this$dp$iv), 0.0F, 0.0F, 12, (Object)null);
               CardKt.Card(modifier$ivx, (Shape)var74, var73, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, -1586169170, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                  @Composable
                  @ComposableTarget(
                     applier = "androidx.compose.ui.UiComposable"
                  )
                  public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                     Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                     ComposerKt.sourceInformation($composer, "C86@3540L3088:HuoAvatarScreen.kt#k2q6ai");
                     if (($changed & 81) == 16 && $composer.getSkipping()) {
                        $composer.skipToGroupEnd();
                     } else {
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventStart(-1586169170, $changed, -1, "com.viernes.mobile.ui.screens.HuoAvatarScreen.<anonymous>.<anonymous>.<anonymous> (HuoAvatarScreen.kt:86)");
                        }

                        Modifier var10000 = (Modifier)Modifier.Companion;
                        int $this$dp$iv = 16;
                        int $i$f$getDp = 0;
                        Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                        final HuoAvatarController var7 = var8;
                        State var8x = var10;
                        State var9 = var11;
                        int $changed$iv = 6;
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

                        skippableUpdate$iv$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivx >> 3);
                        $composer.startReplaceableGroup(2058660585);
                        int var27 = 14 & $changed$iv$iv$ivx >> 9;
                        int var29 = 0;
                        ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                        int var30 = 6 | 112 & $changed$iv >> 6;
                        ColumnScope var120 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                        int var33 = 0;
                        ComposerKt.sourceInformationMarkerStart($composer, -659559081, "C89@3721L10,87@3605L258,93@3884L40,97@4084L21,94@3945L1122,115@5089L41,119@5266L10,117@5152L256,123@5429L40,127@5629L21,124@5490L1120:HuoAvatarScreen.kt#k2q6ai");
                        TextStyle var34 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleSmall();
                        FontWeight var35 = FontWeight.Companion.getBold();
                        long var36 = ColorKt.getTextPrimary();
                        TextKt.Text--4IGK_g("Movimientos Originales de HUO", (Modifier)null, var36, 0L, (FontStyle)null, var35, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var34, $composer, 196998, 0, 65498);
                        Modifier var121 = (Modifier)Modifier.Companion;
                        int $this$dp$iv = 8;
                        int $i$f$getDp = 0;
                        SpacerKt.Spacer(SizeKt.height-3ABfNKs(var121, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                        Modifier $this$dp$ivxxx = ScrollKt.horizontalScroll$default(SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), ScrollKt.rememberScrollState(0, $composer, 0, 1), false, (FlingBehavior)null, false, 14, (Object)null);
                        $i$f$getDp = 8;
                        int $i$f$getDp = 0;
                        Arrangement.Horizontal $i$f$getDpxxxxx = (Arrangement.Horizontal)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                        byte $changed$ivxxx = 48;
                        int $i$f$Row = 0;
                        $composer.startReplaceableGroup(693286680);
                        ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                        Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getTop();
                        MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy($i$f$getDpxxxxx, verticalAlignment$iv, $composer, 14 & $changed$ivxxx >> 3 | 112 & $changed$ivxxx >> 3);
                        int $changed$iv$ivxx = 112 & $changed$ivxxx << 3;
                        int $i$f$Layout = 0;
                        $composer.startReplaceableGroup(-1323940314);
                        ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                        int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                        CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                        Function0 factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                        Function3 skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf($this$dp$ivxxx);
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
                        int $changed$ivxxxx = 14 & $changed$iv$iv$ivxx >> 9;
                        int var58 = 0;
                        ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                        int $changedxx = 6 | 112 & $changed$ivxxx >> 6;
                        Composer $composerx = $composer;
                        RowScope var122 = (RowScope)RowScopeInstance.INSTANCE;
                        int var62 = 0;
                        ComposerKt.sourceInformationMarkerStart($composer, -498939353, "C:HuoAvatarScreen.kt#k2q6ai");
                        $composer.startReplaceableGroup(2062116125);
                        ComposerKt.sourceInformation($composer, "*104@4531L169,101@4310L709");
                        Iterable $this$forEach$iv = (Iterable)var7.getAvailableMotions();
                        int $i$f$forEach = 0;

                        for(Object element$iv : $this$forEach$iv) {
                           final String motion = (String)element$iv;
                           int var68 = 0;
                           Function0 var123 = new Function0<Unit>() {
                              public final void invoke() {
                                 var7.triggerMotion(motion);
                              }
                           };
                           int $this$dp$iv = 8;
                           int $i$f$getDp = 0;
                           ButtonKt.OutlinedButton(var123, (Modifier)null, false, (Shape)RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv)), ButtonDefaults.INSTANCE.outlinedButtonColors-ro_MJ88(0L, Intrinsics.areEqual(HuoAvatarScreenKt.HuoAvatarScreen$lambda$1(var8x), motion) ? ColorKt.getViernesPrimary() : ColorKt.getTextSecondary(), 0L, 0L, $composerx, ButtonDefaults.$stable << 12, 13), (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, (Function3)ComposableLambdaKt.composableLambda($composerx, -1555767898, true, new Function3<RowScope, Composer, Integer, Unit>() {
                              @Composable
                              @ComposableTarget(
                                 applier = "androidx.compose.ui.UiComposable"
                              )
                              public final void invoke(@NotNull RowScope $this$OutlinedButton, @Nullable Composer $composer, int $changed) {
                                 Intrinsics.checkNotNullParameter($this$OutlinedButton, "$this$OutlinedButton");
                                 ComposerKt.sourceInformation($composer, "C108@4765L89,109@4887L39,110@4959L30:HuoAvatarScreen.kt#k2q6ai");
                                 if (($changed & 81) == 16 && $composer.getSkipping()) {
                                    $composer.skipToGroupEnd();
                                 } else {
                                    if (ComposerKt.isTraceInProgress()) {
                                       ComposerKt.traceEventStart(-1555767898, $changed, -1, "com.viernes.mobile.ui.screens.HuoAvatarScreen.<anonymous>.<anonymous>.<anonymous>.<anonymous>.<anonymous>.<anonymous>.<anonymous> (HuoAvatarScreen.kt:108)");
                                    }

                                    ImageVector var10000 = PlayArrowKt.getPlayArrow(Icons.INSTANCE.getDefault());
                                    Modifier var10002 = (Modifier)Modifier.Companion;
                                    int $this$dp$iv = 14;
                                    int $i$f$getDp = 0;
                                    IconKt.Icon-ww6aTOc(var10000, (String)null, SizeKt.size-3ABfNKs(var10002, Dp.constructor-impl((float)$this$dp$iv)), 0L, $composer, 432, 8);
                                    Modifier var8x = (Modifier)Modifier.Companion;
                                    $this$dp$iv = 4;
                                    $i$f$getDp = 0;
                                    SpacerKt.Spacer(SizeKt.width-3ABfNKs(var8x, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                                    TextKt.Text--4IGK_g(motion, (Modifier)null, 0L, TextUnitKt.getSp(12), (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 3072, 0, 131062);
                                    if (ComposerKt.isTraceInProgress()) {
                                       ComposerKt.traceEventEnd();
                                    }
                                 }

                              }
                           }), $composerx, 805306368, 486);
                        }

                        $composerx.endReplaceableGroup();
                        ComposerKt.sourceInformationMarkerEnd($composerx);
                        ComposerKt.sourceInformationMarkerEnd($composer);
                        $composer.endReplaceableGroup();
                        $composer.endNode();
                        $composer.endReplaceableGroup();
                        $composer.endReplaceableGroup();
                        Modifier var124 = (Modifier)Modifier.Companion;
                        int $this$dp$iv = 14;
                        int $i$f$getDp = 0;
                        SpacerKt.Spacer(SizeKt.height-3ABfNKs(var124, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                        TextStyle modifier$ivxx = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleSmall();
                        FontWeight $this$dp$ivxxxxxx = FontWeight.Companion.getBold();
                        var36 = ColorKt.getTextPrimary();
                        TextKt.Text--4IGK_g("Expresiones Faciales de HUO", (Modifier)null, var36, 0L, (FontStyle)null, $this$dp$ivxxxxxx, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, modifier$ivxx, $composer, 196998, 0, 65498);
                        var124 = (Modifier)Modifier.Companion;
                        int $this$dp$iv = 8;
                        int $i$f$getDp = 0;
                        SpacerKt.Spacer(SizeKt.height-3ABfNKs(var124, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                        Modifier var78 = ScrollKt.horizontalScroll$default(SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), ScrollKt.rememberScrollState(0, $composer, 0, 1), false, (FlingBehavior)null, false, 14, (Object)null);
                        $i$f$getDp = 8;
                        int $i$f$getDp = 0;
                        Arrangement.Horizontal var86 = (Arrangement.Horizontal)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                        $changed$ivxxx = 48;
                        $i$f$Row = 0;
                        $composer.startReplaceableGroup(693286680);
                        ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                        Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getTop();
                        measurePolicy$iv = RowKt.rowMeasurePolicy(var86, verticalAlignment$iv, $composer, 14 & $changed$ivxxx >> 3 | 112 & $changed$ivxxx >> 3);
                        $changed$iv$ivxx = 112 & $changed$ivxxx << 3;
                        $i$f$Layout = 0;
                        $composer.startReplaceableGroup(-1323940314);
                        ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                        compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                        localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                        factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                        skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(var78);
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
                        $changed$ivxxxx = 14 & $changed$iv$iv$ivxx >> 9;
                        var58 = 0;
                        ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                        $changedxx = 6 | 112 & $changed$ivxxx >> 6;
                        $composerx = $composer;
                        RowScope var126 = (RowScope)RowScopeInstance.INSTANCE;
                        var62 = 0;
                        ComposerKt.sourceInformationMarkerStart($composer, -497406775, "C:HuoAvatarScreen.kt#k2q6ai");
                        $composer.startReplaceableGroup(2062165687);
                        ComposerKt.sourceInformation($composer, "*134@6080L170,131@5857L705");
                        $this$forEach$iv = (Iterable)var7.getAvailableExpressions();
                        $i$f$forEach = 0;

                        for(Object element$iv : $this$forEach$iv) {
                           final String expr = (String)element$iv;
                           int var117 = 0;
                           Function0 var127 = new Function0<Unit>() {
                              public final void invoke() {
                                 var7.triggerExpression(expr);
                              }
                           };
                           int $this$dp$iv = 8;
                           int $i$f$getDp = 0;
                           ButtonKt.OutlinedButton(var127, (Modifier)null, false, (Shape)RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv)), ButtonDefaults.INSTANCE.outlinedButtonColors-ro_MJ88(0L, Intrinsics.areEqual(HuoAvatarScreenKt.HuoAvatarScreen$lambda$2(var9), expr) ? ColorKt.getViernesAccent() : ColorKt.getTextSecondary(), 0L, 0L, $composerx, ButtonDefaults.$stable << 12, 13), (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, (Function3)ComposableLambdaKt.composableLambda($composerx, 379874013, true, new Function3<RowScope, Composer, Integer, Unit>() {
                              @Composable
                              @ComposableTarget(
                                 applier = "androidx.compose.ui.UiComposable"
                              )
                              public final void invoke(@NotNull RowScope $this$OutlinedButton, @Nullable Composer $composer, int $changed) {
                                 Intrinsics.checkNotNullParameter($this$OutlinedButton, "$this$OutlinedButton");
                                 ComposerKt.sourceInformation($composer, "C138@6315L84,139@6432L39,140@6504L28:HuoAvatarScreen.kt#k2q6ai");
                                 if (($changed & 81) == 16 && $composer.getSkipping()) {
                                    $composer.skipToGroupEnd();
                                 } else {
                                    if (ComposerKt.isTraceInProgress()) {
                                       ComposerKt.traceEventStart(379874013, $changed, -1, "com.viernes.mobile.ui.screens.HuoAvatarScreen.<anonymous>.<anonymous>.<anonymous>.<anonymous>.<anonymous>.<anonymous>.<anonymous> (HuoAvatarScreen.kt:138)");
                                    }

                                    ImageVector var10000 = FaceKt.getFace(Icons.INSTANCE.getDefault());
                                    Modifier var10002 = (Modifier)Modifier.Companion;
                                    int $this$dp$iv = 14;
                                    int $i$f$getDp = 0;
                                    IconKt.Icon-ww6aTOc(var10000, (String)null, SizeKt.size-3ABfNKs(var10002, Dp.constructor-impl((float)$this$dp$iv)), 0L, $composer, 432, 8);
                                    Modifier var8x = (Modifier)Modifier.Companion;
                                    $this$dp$iv = 4;
                                    $i$f$getDp = 0;
                                    SpacerKt.Spacer(SizeKt.width-3ABfNKs(var8x, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                                    TextKt.Text--4IGK_g(expr, (Modifier)null, 0L, TextUnitKt.getSp(12), (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 3072, 0, 131062);
                                    if (ComposerKt.isTraceInProgress()) {
                                       ComposerKt.traceEventEnd();
                                    }
                                 }

                              }
                           }), $composerx, 805306368, 486);
                        }

                        $composerx.endReplaceableGroup();
                        ComposerKt.sourceInformationMarkerEnd($composerx);
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

      ScopeUpdateScope var10000 = $composer.endRestartGroup();
      if (var10000 != null) {
         var10000.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               HuoAvatarScreenKt.HuoAvatarScreen(huoController, onNavigateBack, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   private static final HuoState HuoAvatarScreen$lambda$0(State<? extends HuoState> $state$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (HuoState)$state$delegate.getValue();
   }

   private static final String HuoAvatarScreen$lambda$1(State<String> $currentMotion$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (String)$currentMotion$delegate.getValue();
   }

   private static final String HuoAvatarScreen$lambda$2(State<String> $currentExpression$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (String)$currentExpression$delegate.getValue();
   }
}
