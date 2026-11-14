package com.viernes.mobile.ui.screens;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build.VERSION;
import android.widget.Toast;
import androidx.compose.foundation.BorderStroke;
import androidx.compose.foundation.ScrollKt;
import androidx.compose.foundation.gestures.FlingBehavior;
import androidx.compose.foundation.interaction.MutableInteractionSource;
import androidx.compose.foundation.layout.Arrangement;
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
import androidx.compose.material3.MaterialTheme;
import androidx.compose.material3.ScaffoldKt;
import androidx.compose.material3.SwitchDefaults;
import androidx.compose.material3.SwitchKt;
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
import androidx.compose.ui.platform.AndroidCompositionLocals_androidKt;
import androidx.compose.ui.text.TextStyle;
import androidx.compose.ui.text.font.FontFamily;
import androidx.compose.ui.text.font.FontStyle;
import androidx.compose.ui.text.font.FontWeight;
import androidx.compose.ui.text.style.TextAlign;
import androidx.compose.ui.text.style.TextDecoration;
import androidx.compose.ui.unit.Dp;
import com.viernes.mobile.notifications.AlarmScheduler;
import com.viernes.mobile.ui.theme.ColorKt;
import com.viernes.mobile.worker.SyncWorker;
import kotlin.Metadata;
import kotlin.Unit;
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
   d1 = {"\u0000\u0016\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\u000b\n\u0000\u001a\u001b\u0010\u0000\u001a\u00020\u00012\f\u0010\u0002\u001a\b\u0012\u0004\u0012\u00020\u00010\u0003H\u0007¢\u0006\u0002\u0010\u0004¨\u0006\u0005²\u0006\n\u0010\u0006\u001a\u00020\u0007X\u008a\u008e\u0002²\u0006\n\u0010\b\u001a\u00020\u0007X\u008a\u008e\u0002"},
   d2 = {"SettingsScreen", "", "onNavigateBack", "Lkotlin/Function0;", "(Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "app_debug", "hideSensitiveDataOnLockscreen", "", "exactAlarmAllowed"}
)
@SourceDebugExtension({"SMAP\nSettingsScreen.kt\nKotlin\n*S Kotlin\n*F\n+ 1 SettingsScreen.kt\ncom/viernes/mobile/ui/screens/SettingsScreenKt\n+ 2 CompositionLocal.kt\nandroidx/compose/runtime/CompositionLocal\n+ 3 Composer.kt\nandroidx/compose/runtime/ComposerKt\n+ 4 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,176:1\n74#2:177\n1116#3,6:178\n1116#3,6:184\n81#4:190\n107#4,2:191\n81#4:193\n107#4,2:194\n*S KotlinDebug\n*F\n+ 1 SettingsScreen.kt\ncom/viernes/mobile/ui/screens/SettingsScreenKt\n*L\n31#1:177\n32#1:178,6\n33#1:184,6\n32#1:190\n32#1:191,2\n33#1:193\n33#1:194,2\n*E\n"})
public final class SettingsScreenKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void SettingsScreen(@NotNull final Function0<Unit> onNavigateBack, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(onNavigateBack, "onNavigateBack");
      $composer = $composer.startRestartGroup(-738591748);
      ComposerKt.sourceInformation($composer, "C(SettingsScreen)30@1064L7,31@1113L33,32@1176L69,34@1251L7123:SettingsScreen.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changedInstance(onNavigateBack) ? 4 : 2);
      }

      if (($dirty & 11) == 2 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(-738591748, $dirty, -1, "com.viernes.mobile.ui.screens.SettingsScreen (SettingsScreen.kt:29)");
         }

         CompositionLocal this_$iv = (CompositionLocal)AndroidCompositionLocals_androidKt.getLocalContext();
         int $changed$iv = 0;
         int $i$f$getCurrent = 0;
         ComposerKt.sourceInformationMarkerStart($composer, 2023513938, "CC:CompositionLocal.kt#9igjgp");
         Object var8 = $composer.consume(this_$iv);
         ComposerKt.sourceInformationMarkerEnd($composer);
         final Context context = (Context)var8;
         $composer.startReplaceableGroup(1462477092);
         ComposerKt.sourceInformation($composer, "CC(remember):SettingsScreen.kt#9igjgp");
         boolean var18 = false;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var11 = 0;
         Object var10000;
         if (it$iv == Composer.Companion.getEmpty()) {
            int var12 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default(true, (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState exactAlarmAllowed$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         $composer.startReplaceableGroup(1462479144);
         ComposerKt.sourceInformation($composer, "CC(remember):SettingsScreen.kt#9igjgp");
         $i$f$cache = 0;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var23 = 0;
         if (it$iv == Composer.Companion.getEmpty()) {
            int var13 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default(AlarmScheduler.INSTANCE.canScheduleExact(context), (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState $this$cache$iv = (MutableState)var10000;
         $composer.endReplaceableGroup();
         ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 1846913976, true, new Function2<Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@Nullable Composer $composer, int $changed) {
               ComposerKt.sourceInformation($composer, "C43@1697L48,36@1292L467:SettingsScreen.kt#k2q6ai");
               if (($changed & 11) == 2 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(1846913976, $changed, -1, "com.viernes.mobile.ui.screens.SettingsScreen.<anonymous> (SettingsScreen.kt:36)");
                  }

                  AppBarKt.TopAppBar(ComposableSingletons$SettingsScreenKt.INSTANCE.getLambda-1$app_debug(), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -29518722, true, new Function2<Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@Nullable Composer $composer, int $changed) {
                        ComposerKt.sourceInformation($composer, "C39@1467L167:SettingsScreen.kt#k2q6ai");
                        if (($changed & 11) == 2 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(-29518722, $changed, -1, "com.viernes.mobile.ui.screens.SettingsScreen.<anonymous>.<anonymous> (SettingsScreen.kt:39)");
                           }

                           IconButtonKt.IconButton(onNavigateBack, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$SettingsScreenKt.INSTANCE.getLambda-2$app_debug(), $composer, 196608, 30);
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
         }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, -690184371, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter(padding, "padding");
               ComposerKt.sourceInformation($composer, "C53@2007L21,48@1838L6530:SettingsScreen.kt#k2q6ai");
               int $dirty = $changed;
               if (($changed & 14) == 0) {
                  $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
               }

               if (($dirty & 91) == 18 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-690184371, $dirty, -1, "com.viernes.mobile.ui.screens.SettingsScreen.<anonymous> (SettingsScreen.kt:48)");
                  }

                  Modifier var10000 = PaddingKt.padding(SizeKt.fillMaxSize$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null), padding);
                  int $this$dp$iv = 16;
                  int $i$f$getDp = 0;
                  Modifier modifier$iv = ScrollKt.verticalScroll$default(PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv)), ScrollKt.rememberScrollState(0, $composer, 0, 1), false, (FlingBehavior)null, false, 14, (Object)null);
                  $i$f$getDp = 16;
                  int $i$f$getDp = 0;
                  Arrangement.Vertical verticalArrangement$iv = (Arrangement.Vertical)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$i$f$getDp));
                  final MutableState var8 = $this$cache$iv;
                  final Context var9 = context;
                  final MutableState var10 = exactAlarmAllowed$delegate;
                  int $changed$iv = 48;
                  int $i$f$Column = 0;
                  $composer.startReplaceableGroup(-483455358);
                  ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
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
                  ColumnScope var59 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  int var34 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -688755612, "C59@2280L40,57@2184L1117,79@3470L40,77@3374L2067,119@5605L40,117@5509L1435,148@7101L40,146@7005L1353:SettingsScreen.kt#k2q6ai");
                  Modifier var35 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  CardColors var36 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  int $this$dp$iv = 16;
                  int $i$f$getDp = 0;
                  RoundedCornerShape var39 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var35, (Shape)var39, var36, (CardElevation)null, (BorderStroke)null, ComposableSingletons$SettingsScreenKt.INSTANCE.getLambda-3$app_debug(), $composer, 196614, 24);
                  var35 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  var36 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  $this$dp$iv = 16;
                  $i$f$getDp = 0;
                  var39 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var35, (Shape)var39, var36, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1340685548, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                        Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                        ComposerKt.sourceInformation($composer, "C82@3594L1833:SettingsScreen.kt#k2q6ai");
                        if (($changed & 81) == 16 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(1340685548, $changed, -1, "com.viernes.mobile.ui.screens.SettingsScreen.<anonymous>.<anonymous>.<anonymous> (SettingsScreen.kt:82)");
                           }

                           Modifier var10000 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 16;
                           int $i$f$getDp = 0;
                           Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                           MutableState var7 = var8;
                           final Context var8x = var9;
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

                           skippableUpdate$iv$iv$ivx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivx >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           int var26 = 14 & $changed$iv$iv$ivx >> 9;
                           int var28 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                           int var29 = 6 | 112 & $changed$iv >> 6;
                           ColumnScope var98 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int var32 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -1625272946, "C83@3659L954:SettingsScreen.kt#k2q6ai");
                           Modifier modifier$ivxx = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                           Arrangement.Horizontal horizontalArrangement$iv = (Arrangement.Horizontal)Arrangement.INSTANCE.getSpaceBetween();
                           Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                           short $changed$ivxx = 438;
                           int $i$f$Row = 0;
                           $composer.startReplaceableGroup(693286680);
                           ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                           MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, verticalAlignment$iv, $composer, 14 & $changed$ivxx >> 3 | 112 & $changed$ivxx >> 3);
                           int $changed$iv$ivxx = 112 & $changed$ivxx << 3;
                           int $i$f$Layout = 0;
                           $composer.startReplaceableGroup(-1323940314);
                           ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                           int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                           CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                           Function0 factory$iv$iv$iv = ComposeUiNode.Companion.getConstructor();
                           Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$ivxx);
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
                           int var48 = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           int var50 = 0;
                           int var52 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           int var53 = 14 & $changed$iv$iv$iv >> 9;
                           int var55 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                           int var56 = 6 | 112 & $changed$ivxx >> 6;
                           RowScope $this$invoke_u24lambda_u242_u24lambda_u241 = (RowScope)RowScopeInstance.INSTANCE;
                           int var59 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -1904527517, "C88@3917L674:SettingsScreen.kt#k2q6ai");
                           Modifier modifier$ivx = RowScope.weight$default($this$invoke_u24lambda_u242_u24lambda_u241, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
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
                           int var75 = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           int var77 = 0;
                           int var79 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           int var80 = 14 & $changed$iv$iv$ivxx >> 9;
                           int var82 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                           int var83 = 6 | 112 & $changed$iv >> 6;
                           var98 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int var86 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 575877667, "C89@3986L85,93@4416L10,90@4100L465:SettingsScreen.kt#k2q6ai");
                           FontWeight var87 = FontWeight.Companion.getBold();
                           long var88 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g("Permiso de Alarmas Exactas", (Modifier)null, var88, 0L, (FontStyle)null, var87, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 196998, 0, 131034);
                           String var97 = SettingsScreenKt.SettingsScreen$lambda$4(var7) ? "Concedido: las tomas a las 18:00 o cualquier hora se dispararán al minuto exacto." : "Restringido: el sistema operativo podría retrasar las notificaciones.";
                           TextStyle var90 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                           long var91 = SettingsScreenKt.SettingsScreen$lambda$4(var7) ? ColorKt.getStatusConfirmed() : ColorKt.getStatusDelayed();
                           TextKt.Text--4IGK_g(var97, (Modifier)null, var91, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var90, $composer, 0, 0, 65530);
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
                           $composer.startReplaceableGroup(640338757);
                           ComposerKt.sourceInformation($composer, "100@4735L41,108@5221L44,101@4801L586");
                           if (!SettingsScreenKt.SettingsScreen$lambda$4(var7) && VERSION.SDK_INT >= 31) {
                              Modifier var100 = (Modifier)Modifier.Companion;
                              int $this$dp$iv = 10;
                              int $i$f$getDp = 0;
                              SpacerKt.Spacer(SizeKt.height-3ABfNKs(var100, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                              ButtonKt.Button(new Function0<Unit>() {
                                 public final void invoke() {
                                    Intent $this$invoke_u24lambda_u240 = new Intent("android.settings.REQUEST_SCHEDULE_EXACT_ALARM");
                                    Context var3 = var8x;
                                    int var5 = 0;
                                    $this$invoke_u24lambda_u240.setData(Uri.parse("package:" + var3.getPackageName()));
                                    var8x.startActivity($this$invoke_u24lambda_u240);
                                 }
                              }, (Modifier)null, false, (Shape)null, ButtonDefaults.INSTANCE.buttonColors-ro_MJ88(ColorKt.getStatusDelayed(), 0L, 0L, 0L, $composer, 6 | ButtonDefaults.$stable << 12, 14), (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$SettingsScreenKt.INSTANCE.getLambda-4$app_debug(), $composer, 805306368, 494);
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
                  var35 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  var36 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  $this$dp$iv = 16;
                  $i$f$getDp = 0;
                  var39 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var35, (Shape)var39, var36, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, -664805331, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                        Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                        ComposerKt.sourceInformation($composer, "C122@5729L1201:SettingsScreen.kt#k2q6ai");
                        if (($changed & 81) == 16 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(-664805331, $changed, -1, "com.viernes.mobile.ui.screens.SettingsScreen.<anonymous>.<anonymous>.<anonymous> (SettingsScreen.kt:122)");
                           }

                           Modifier var10000 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 16;
                           int $i$f$getDp = 0;
                           Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                           final MutableState var7 = var10;
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
                           ColumnScope var101 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int var31 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -1623174618, "C123@5794L1118:SettingsScreen.kt#k2q6ai");
                           Modifier modifier$ivxx = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                           Arrangement.Horizontal horizontalArrangement$iv = (Arrangement.Horizontal)Arrangement.INSTANCE.getSpaceBetween();
                           Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                           short $changed$ivxx = 438;
                           int $i$f$Row = 0;
                           $composer.startReplaceableGroup(693286680);
                           ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                           MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, verticalAlignment$iv, $composer, 14 & $changed$ivxx >> 3 | 112 & $changed$ivxx >> 3);
                           int $changed$iv$ivxx = 112 & $changed$ivxx << 3;
                           int $i$f$Layout = 0;
                           $composer.startReplaceableGroup(-1323940314);
                           ComposerKt.sourceInformation($composer, "CC(Layout)P(!1,2)78@3182L23,80@3272L420:Layout.kt#80mrfh");
                           int compositeKeyHash$iv$iv = ComposablesKt.getCurrentCompositeKeyHash($composer, 0);
                           CompositionLocalMap localMap$iv$iv = $composer.getCurrentCompositionLocalMap();
                           Function0 factory$iv$iv$ivxx = ComposeUiNode.Companion.getConstructor();
                           Function3 skippableUpdate$iv$iv$iv = LayoutKt.modifierMaterializerOf(modifier$ivxx);
                           int $changed$iv$iv$iv = 6 | 7168 & $changed$iv$ivxx << 9;
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

                           skippableUpdate$iv$iv$iv.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$iv >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           int var52 = 14 & $changed$iv$iv$iv >> 9;
                           int var54 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -326681643, "C92@4661L9:Row.kt#2w3rfo");
                           int var55 = 6 | 112 & $changed$ivxx >> 6;
                           RowScope $this$invoke_u24lambda_u243_u24lambda_u242 = (RowScope)RowScopeInstance.INSTANCE;
                           int var58 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, -1902404513, "C128@6052L530,138@6730L38,139@6822L42,136@6607L283:SettingsScreen.kt#k2q6ai");
                           Modifier modifier$ivx = RowScope.weight$default($this$invoke_u24lambda_u243_u24lambda_u242, (Modifier)Modifier.Companion, 1.0F, false, 2, (Object)null);
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
                           Function3 skippableUpdate$iv$iv$ivxx = LayoutKt.modifierMaterializerOf(modifier$ivx);
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
                           int var74 = 0;
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, measurePolicy$iv, ComposeUiNode.Companion.getSetMeasurePolicy());
                           Updater.set-impl($this$Layout_u24lambda_u240$iv$iv, localMap$iv$iv, ComposeUiNode.Companion.getSetResolvedCompositionLocals());
                           Function2 block$iv$iv$iv = ComposeUiNode.Companion.getSetCompositeKeyHash();
                           int var76 = 0;
                           int var78 = 0;
                           if ($this$Layout_u24lambda_u240$iv$iv.getInserting() || !Intrinsics.areEqual($this$Layout_u24lambda_u240$iv$iv.rememberedValue(), compositeKeyHash$iv$iv)) {
                              $this$Layout_u24lambda_u240$iv$iv.updateRememberedValue(compositeKeyHash$iv$iv);
                              $this$Layout_u24lambda_u240$iv$iv.apply(compositeKeyHash$iv$iv, block$iv$iv$iv);
                           }

                           skippableUpdate$iv$iv$ivxx.invoke(SkippableUpdater.box-impl(SkippableUpdater.constructor-impl($composer)), $composer, 112 & $changed$iv$iv$ivxx >> 3);
                           $composer.startReplaceableGroup(2058660585);
                           int var79 = 14 & $changed$iv$iv$ivxx >> 9;
                           int var81 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                           int var82 = 6 | 112 & $changed$iv >> 6;
                           var101 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                           int var85 = 0;
                           ComposerKt.sourceInformationMarkerStart($composer, 577991123, "C129@6121L87,132@6451L10,130@6237L319:SettingsScreen.kt#k2q6ai");
                           FontWeight var86 = FontWeight.Companion.getBold();
                           long var87 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g("Proteger Nombres de Fármacos", (Modifier)null, var87, 0L, (FontStyle)null, var86, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 196998, 0, 131034);
                           TextStyle var99 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                           var87 = ColorKt.getTextSecondary();
                           TextKt.Text--4IGK_g("Oculta el nombre específico del medicamento en la pantalla de bloqueo para proteger la confidencialidad médica.", (Modifier)null, var87, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var99, $composer, 390, 0, 65530);
                           ComposerKt.sourceInformationMarkerEnd($composer);
                           ComposerKt.sourceInformationMarkerEnd($composer);
                           $composer.endReplaceableGroup();
                           $composer.endNode();
                           $composer.endReplaceableGroup();
                           $composer.endReplaceableGroup();
                           boolean var103 = SettingsScreenKt.SettingsScreen$lambda$1(var7);
                           $composer.startReplaceableGroup(-476988988);
                           ComposerKt.sourceInformation($composer, "CC(remember):SettingsScreen.kt#9igjgp");
                           boolean invalid$iv = false;
                           $changed$iv = 0;
                           Object it$iv = $composer.rememberedValue();
                           int var97 = 0;
                           Object var10001;
                           if (it$iv == Composer.Companion.getEmpty()) {
                              boolean var89 = var103;
                              $changed$iv$ivx = 0;
                              Function1 value$iv = new Function1<Boolean, Unit>() {
                                 public final void invoke(boolean it) {
                                    SettingsScreenKt.SettingsScreen$lambda$2(var7, it);
                                 }
                              };
                              var103 = var89;
                              $composer.updateRememberedValue(value$iv);
                              var10001 = value$iv;
                           } else {
                              var10001 = it$iv;
                           }

                           Function1 var93 = (Function1)var10001;
                           $composer.endReplaceableGroup();
                           SwitchKt.Switch(var103, var93, (Modifier)null, (Function2)null, false, SwitchDefaults.INSTANCE.colors-V1nXRL4(ColorKt.getViernesPrimary(), 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, $composer, 6, SwitchDefaults.$stable << 18, 65534), (MutableInteractionSource)null, $composer, 48, 92);
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
                  var35 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  var36 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
                  $this$dp$iv = 16;
                  $i$f$getDp = 0;
                  var39 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                  CardKt.Card(var35, (Shape)var39, var36, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, 1624671086, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
                        Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
                        ComposerKt.sourceInformation($composer, "C151@7225L1119:SettingsScreen.kt#k2q6ai");
                        if (($changed & 81) == 16 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(1624671086, $changed, -1, "com.viernes.mobile.ui.screens.SettingsScreen.<anonymous>.<anonymous>.<anonymous> (SettingsScreen.kt:151)");
                           }

                           Modifier var10000 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 16;
                           int $i$f$getDp = 0;
                           Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                           final Context var7 = var9;
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
                           ComposerKt.sourceInformationMarkerStart($composer, -1621693128, "C152@7290L84,155@7561L10,153@7395L255,158@7671L41,164@8045L45,159@7733L593:SettingsScreen.kt#k2q6ai");
                           FontWeight var32 = FontWeight.Companion.getBold();
                           long var33 = ColorKt.getTextPrimary();
                           TextKt.Text--4IGK_g("Sincronización en la Nube", (Modifier)null, var33, 0L, (FontStyle)null, var32, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 196998, 0, 131034);
                           TextStyle var38 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                           var33 = ColorKt.getTextSecondary();
                           TextKt.Text--4IGK_g("Sincroniza cambios pendientes cuando haya conectividad con el servidor central seguro.", (Modifier)null, var33, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var38, $composer, 390, 0, 65530);
                           Modifier var42 = (Modifier)Modifier.Companion;
                           int $this$dp$iv = 12;
                           int $i$f$getDp = 0;
                           SpacerKt.Spacer(SizeKt.height-3ABfNKs(var42, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                           ButtonKt.Button(new Function0<Unit>() {
                              public final void invoke() {
                                 SyncWorker.Companion.triggerImmediateSync(var7);
                                 Toast.makeText(var7, (CharSequence)"Sincronización en segundo plano iniciada.", 0).show();
                              }
                           }, (Modifier)null, false, (Shape)null, ButtonDefaults.INSTANCE.buttonColors-ro_MJ88(ColorKt.getViernesPrimary(), 0L, 0L, 0L, $composer, 6 | ButtonDefaults.$stable << 12, 14), (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$SettingsScreenKt.INSTANCE.getLambda-5$app_debug(), $composer, 805306368, 494);
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
      }

      ScopeUpdateScope var25 = $composer.endRestartGroup();
      if (var25 != null) {
         var25.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               SettingsScreenKt.SettingsScreen(onNavigateBack, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   private static final boolean SettingsScreen$lambda$1(MutableState<Boolean> $hideSensitiveDataOnLockscreen$delegate) {
      State $this$getValue$iv = (State)$hideSensitiveDataOnLockscreen$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Boolean)$this$getValue$iv.getValue();
   }

   private static final void SettingsScreen$lambda$2(MutableState<Boolean> $hideSensitiveDataOnLockscreen$delegate, boolean value) {
      Object var3 = null;
      Object var4 = null;
      Object value$iv = value;
      int $i$f$setValue = 0;
      $hideSensitiveDataOnLockscreen$delegate.setValue(value$iv);
   }

   private static final boolean SettingsScreen$lambda$4(MutableState<Boolean> $exactAlarmAllowed$delegate) {
      State $this$getValue$iv = (State)$exactAlarmAllowed$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Boolean)$this$getValue$iv.getValue();
   }

   private static final void SettingsScreen$lambda$5(MutableState<Boolean> $exactAlarmAllowed$delegate, boolean value) {
      Object var3 = null;
      Object var4 = null;
      Object value$iv = value;
      int $i$f$setValue = 0;
      $exactAlarmAllowed$delegate.setValue(value$iv);
   }
}
