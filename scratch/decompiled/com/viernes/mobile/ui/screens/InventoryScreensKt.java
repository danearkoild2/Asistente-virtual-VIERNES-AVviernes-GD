package com.viernes.mobile.ui.screens;

import android.content.Context;
import android.widget.Toast;
import androidx.compose.foundation.BorderStroke;
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
import androidx.compose.foundation.lazy.LazyDslKt;
import androidx.compose.foundation.lazy.LazyListScope;
import androidx.compose.foundation.lazy.LazyListState;
import androidx.compose.foundation.shape.RoundedCornerShape;
import androidx.compose.foundation.shape.RoundedCornerShapeKt;
import androidx.compose.foundation.text.KeyboardActions;
import androidx.compose.foundation.text.KeyboardOptions;
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
import androidx.compose.material3.MaterialTheme;
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
import androidx.compose.ui.platform.AndroidCompositionLocals_androidKt;
import androidx.compose.ui.text.TextStyle;
import androidx.compose.ui.text.font.FontFamily;
import androidx.compose.ui.text.font.FontStyle;
import androidx.compose.ui.text.font.FontWeight;
import androidx.compose.ui.text.input.VisualTransformation;
import androidx.compose.ui.text.style.TextAlign;
import androidx.compose.ui.text.style.TextDecoration;
import androidx.compose.ui.unit.Dp;
import androidx.compose.ui.window.DialogProperties;
import com.viernes.mobile.data.repository.InventoryRepository;
import com.viernes.mobile.data.repository.PatientRepository;
import com.viernes.mobile.domain.model.Inventory;
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
   d1 = {"\u00008\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\t\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0010 \n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\u001a#\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\f\u0010\u0004\u001a\b\u0012\u0004\u0012\u00020\u00010\u0005H\u0007¢\u0006\u0002\u0010\u0006\u001a3\u0010\u0007\u001a\u00020\u00012\u0006\u0010\b\u001a\u00020\t2\u0006\u0010\n\u001a\u00020\u000b2\u0006\u0010\f\u001a\u00020\r2\f\u0010\u000e\u001a\b\u0012\u0004\u0012\u00020\u00010\u0005H\u0007¢\u0006\u0002\u0010\u000f¨\u0006\u0010²\u0006\u0010\u0010\u0011\u001a\b\u0012\u0004\u0012\u00020\u00030\u0012X\u008a\u0084\u0002²\u0006\f\u0010\u0013\u001a\u0004\u0018\u00010\u0003X\u008a\u008e\u0002²\u0006\n\u0010\u0014\u001a\u00020\u0015X\u008a\u008e\u0002²\u0006\n\u0010\u0016\u001a\u00020\u0015X\u008a\u008e\u0002"},
   d2 = {"InventoryCard", "", "item", "Lcom/viernes/mobile/domain/model/Inventory;", "onReconcile", "Lkotlin/Function0;", "(Lcom/viernes/mobile/domain/model/Inventory;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "InventoryScreen", "patientId", "", "inventoryRepo", "Lcom/viernes/mobile/data/repository/InventoryRepository;", "patientRepo", "Lcom/viernes/mobile/data/repository/PatientRepository;", "onNavigateBack", "(JLcom/viernes/mobile/data/repository/InventoryRepository;Lcom/viernes/mobile/data/repository/PatientRepository;Lkotlin/jvm/functions/Function0;Landroidx/compose/runtime/Composer;I)V", "app_debug", "inventoryList", "", "selectedItemForReconciliation", "newQtyText", "", "reasonText"}
)
@SourceDebugExtension({"SMAP\nInventoryScreens.kt\nKotlin\n*S Kotlin\n*F\n+ 1 InventoryScreens.kt\ncom/viernes/mobile/ui/screens/InventoryScreensKt\n+ 2 CompositionLocal.kt\nandroidx/compose/runtime/CompositionLocal\n+ 3 Effects.kt\nandroidx/compose/runtime/EffectsKt\n+ 4 Composables.kt\nandroidx/compose/runtime/ComposablesKt\n+ 5 Composer.kt\nandroidx/compose/runtime/ComposerKt\n+ 6 Effects.kt\nandroidx/compose/runtime/EffectsKt$rememberCoroutineScope$1\n+ 7 Dp.kt\nandroidx/compose/ui/unit/DpKt\n+ 8 SnapshotState.kt\nandroidx/compose/runtime/SnapshotStateKt__SnapshotStateKt\n*L\n1#1,208:1\n74#2:209\n487#3,4:210\n491#3,2:218\n495#3:224\n25#4:214\n1116#5,3:215\n1119#5,3:221\n1116#5,6:225\n1116#5,6:231\n1116#5,6:237\n1116#5,6:243\n487#6:220\n154#7:249\n81#8:250\n81#8:251\n107#8,2:252\n81#8:254\n107#8,2:255\n81#8:257\n107#8,2:258\n*S KotlinDebug\n*F\n+ 1 InventoryScreens.kt\ncom/viernes/mobile/ui/screens/InventoryScreensKt\n*L\n36#1:209\n37#1:210,4\n37#1:218,2\n37#1:224\n37#1:214\n37#1:215,3\n37#1:221,3\n39#1:225,6\n40#1:231,6\n41#1:237,6\n105#1:243,6\n37#1:220\n168#1:249\n38#1:250\n39#1:251\n39#1:252,2\n40#1:254\n40#1:255,2\n41#1:257\n41#1:258,2\n*E\n"})
public final class InventoryScreensKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void InventoryScreen(final long patientId, @NotNull final InventoryRepository inventoryRepo, @NotNull final PatientRepository patientRepo, @NotNull final Function0<Unit> onNavigateBack, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(inventoryRepo, "inventoryRepo");
      Intrinsics.checkNotNullParameter(patientRepo, "patientRepo");
      Intrinsics.checkNotNullParameter(onNavigateBack, "onNavigateBack");
      $composer = $composer.startRestartGroup(-1738390874);
      ComposerKt.sourceInformation($composer, "C(InventoryScreen)P(2!1,3)35@1340L7,36@1373L24,37@1471L37,38@1550L45,39@1618L31,40@1672L31,42@1709L2263,*104@4120L40,103@4076L2502:InventoryScreens.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(patientId) ? 4 : 2);
      }

      if (($changed & 112) == 0) {
         $dirty |= $composer.changed(inventoryRepo) ? 32 : 16;
      }

      if (($changed & 7168) == 0) {
         $dirty |= $composer.changedInstance(onNavigateBack) ? 2048 : 1024;
      }

      if (($dirty & 5211) == 1042 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(-1738390874, $dirty, -1, "com.viernes.mobile.ui.screens.InventoryScreen (InventoryScreens.kt:34)");
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
         boolean reasonText$delegate = false;
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
            CoroutineScope var27 = EffectsKt.createCompositionCoroutineScope((CoroutineContext)EmptyCoroutineContext.INSTANCE, $composer);
            Object value$iv$iv$iv = new CompositionScopedCoroutineScopeCanceller(var27);
            $composer.updateRememberedValue(value$iv$iv$iv);
            var10000 = value$iv$iv$iv;
         } else {
            var10000 = it$iv$iv$iv;
         }

         Object var23 = var10000;
         $composer.endReplaceableGroup();
         CompositionScopedCoroutineScopeCanceller wrapper$iv = (CompositionScopedCoroutineScopeCanceller)var23;
         CoroutineScope invalid$iv = wrapper$iv.getCoroutineScope();
         $composer.endReplaceableGroup();
         final CoroutineScope coroutineScope = invalid$iv;
         final State inventoryList$delegate = SnapshotStateKt.collectAsState(inventoryRepo.getInventoryForPatient(patientId), CollectionsKt.emptyList(), (CoroutineContext)null, $composer, 56, 2);
         $composer.startReplaceableGroup(-674730975);
         ComposerKt.sourceInformation($composer, "CC(remember):InventoryScreens.kt#9igjgp");
         boolean $this$cache$iv = false;
         $i$f$remember = 0;
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

         final MutableState var33 = (MutableState)var10000;
         $composer.endReplaceableGroup();
         $composer.startReplaceableGroup(-674728813);
         ComposerKt.sourceInformation($composer, "CC(remember):InventoryScreens.kt#9igjgp");
         $i$f$remember = 0;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         $i$f$cache = 0;
         if (it$iv == Composer.Companion.getEmpty()) {
            int var50 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default("", (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState composer$iv = (MutableState)var10000;
         $composer.endReplaceableGroup();
         $composer.startReplaceableGroup(-674727085);
         ComposerKt.sourceInformation($composer, "CC(remember):InventoryScreens.kt#9igjgp");
         $i$f$cache = 0;
         int $i$f$cache = 0;
         Object it$iv = $composer.rememberedValue();
         int var52 = 0;
         if (it$iv == Composer.Companion.getEmpty()) {
            var20 = 0;
            Object value$iv = SnapshotStateKt.mutableStateOf$default("", (SnapshotMutationPolicy)null, 2, (Object)null);
            $composer.updateRememberedValue(value$iv);
            var10000 = value$iv;
         } else {
            var10000 = it$iv;
         }

         final MutableState reasonText$delegate = (MutableState)var10000;
         $composer.endReplaceableGroup();
         ScaffoldKt.Scaffold-TvnljyQ((Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -2129147550, true, new Function2<Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@Nullable Composer $composer, int $changed) {
               ComposerKt.sourceInformation($composer, "C51@2159L48,44@1750L471:InventoryScreens.kt#k2q6ai");
               if (($changed & 11) == 2 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-2129147550, $changed, -1, "com.viernes.mobile.ui.screens.InventoryScreen.<anonymous> (InventoryScreens.kt:44)");
                  }

                  AppBarKt.TopAppBar(ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-1$app_debug(), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, 1948469160, true, new Function2<Composer, Integer, Unit>() {
                     @Composable
                     @ComposableTarget(
                        applier = "androidx.compose.ui.UiComposable"
                     )
                     public final void invoke(@Nullable Composer $composer, int $changed) {
                        ComposerKt.sourceInformation($composer, "C47@1929L167:InventoryScreens.kt#k2q6ai");
                        if (($changed & 11) == 2 && $composer.getSkipping()) {
                           $composer.skipToGroupEnd();
                        } else {
                           if (ComposerKt.isTraceInProgress()) {
                              ComposerKt.traceEventStart(1948469160, $changed, -1, "com.viernes.mobile.ui.screens.InventoryScreen.<anonymous>.<anonymous> (InventoryScreens.kt:47)");
                           }

                           IconButtonKt.IconButton(onNavigateBack, (Modifier)null, false, (IconButtonColors)null, (MutableInteractionSource)null, ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-2$app_debug(), $composer, 196608, 30);
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
         }), (Function2)null, (Function2)null, (Function2)null, 0, ColorKt.getBackgroundDark(), 0L, (WindowInsets)null, (Function3)ComposableLambdaKt.composableLambda($composer, -775569353, true, new Function3<PaddingValues, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull PaddingValues padding, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter(padding, "padding");
               ComposerKt.sourceInformation($composer, "C62@2527L1439,56@2300L1666:InventoryScreens.kt#k2q6ai");
               int $dirty = $changed;
               if (($changed & 14) == 0) {
                  $dirty = $changed | ($composer.changed(padding) ? 4 : 2);
               }

               if (($dirty & 91) == 18 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-775569353, $dirty, -1, "com.viernes.mobile.ui.screens.InventoryScreen.<anonymous> (InventoryScreens.kt:56)");
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
                  $composer.startReplaceableGroup(1075871666);
                  ComposerKt.sourceInformation($composer, "CC(remember):InventoryScreens.kt#9igjgp");
                  boolean invalid$iv = $composer.changed(inventoryList$delegate);
                  final State var8 = inventoryList$delegate;
                  final MutableState var9 = var33;
                  final MutableState var10 = composer$iv;
                  final MutableState var11 = reasonText$delegate;
                  int $i$f$cache = 0;
                  Object it$iv = $composer.rememberedValue();
                  int var14 = 0;
                  Object var10008;
                  if (!invalid$iv && it$iv != Composer.Companion.getEmpty()) {
                     var10008 = it$iv;
                  } else {
                     boolean var24 = false;
                     Object var23 = null;
                     Object var22 = null;
                     Arrangement.Vertical var21 = var10004;
                     boolean var20 = false;
                     Object var19 = null;
                     Object var18 = null;
                     Modifier var17 = var10000;
                     int var15 = 0;
                     Function1 value$iv = new Function1<LazyListScope, Unit>() {
                        public final void invoke(@NotNull LazyListScope $this$LazyColumn) {
                           Intrinsics.checkNotNullParameter($this$LazyColumn, "$this$LazyColumn");
                           LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-3$app_debug(), 3, (Object)null);
                           if (InventoryScreensKt.InventoryScreen$lambda$0(var8).isEmpty()) {
                              LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-5$app_debug(), 3, (Object)null);
                           } else {
                              List items$iv = InventoryScreensKt.InventoryScreen$lambda$0(var8);
                              MutableState var6 = var9;
                              MutableState var7 = var10;
                              MutableState var8x = var11;
                              Function1 key$iv = null;
                              Function1 contentType$iv = InventoryScreensKt$InventoryScreen$2$1$1$invoke$$inlined$items$default$1.INSTANCE;
                              int $i$f$items = 0;
                              $this$LazyColumn.items(items$iv.size(), (Function1)null, new InventoryScreensKt$InventoryScreen$2$1$1$invoke$$inlined$items$default$3(contentType$iv, items$iv), (Function4)ComposableLambdaKt.composableLambdaInstance(-632812321, true, new InventoryScreensKt$InventoryScreen$2$1$1$invoke$$inlined$items$default$4(items$iv, var6, var7, var8x)));
                           }

                           LazyListScope.item$default($this$LazyColumn, (Object)null, (Object)null, ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-6$app_debug(), 3, (Object)null);
                        }
                     };
                     var10000 = var17;
                     var10001 = var18;
                     var10002 = var19;
                     var10003 = var20;
                     var10004 = var21;
                     var10005 = var22;
                     var10006 = var23;
                     var10007 = var24;
                     $composer.updateRememberedValue(value$iv);
                     var10008 = value$iv;
                  }

                  Function1 var27 = (Function1)var10008;
                  $composer.endReplaceableGroup();
                  LazyDslKt.LazyColumn(var10000, (LazyListState)var10001, (PaddingValues)var10002, var10003, var10004, (Alignment.Horizontal)var10005, (FlingBehavior)var10006, var10007, var27, $composer, 24576, 238);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }
               }

            }
         }), $composer, 806879280, 445);
         Inventory var64 = InventoryScreen$lambda$2(var33);
         if (var64 != null) {
            final Inventory item = var64;
            int var49 = 0;
            $composer.startReplaceableGroup(1075921243);
            ComposerKt.sourceInformation($composer, "CC(remember):InventoryScreens.kt#9igjgp");
            var20 = 0;
            int $i$f$cache = 0;
            Object it$iv = $composer.rememberedValue();
            int var59 = 0;
            Object var65;
            if (it$iv == Composer.Companion.getEmpty()) {
               int var60 = 0;
               Object value$iv = new Function0<Unit>() {
                  public final void invoke() {
                     InventoryScreensKt.InventoryScreen$lambda$3(var33, (Inventory)null);
                  }
               };
               $composer.updateRememberedValue(value$iv);
               var65 = value$iv;
            } else {
               var65 = it$iv;
            }

            Function0 var26 = (Function0)var65;
            $composer.endReplaceableGroup();
            AndroidAlertDialog_androidKt.AlertDialog-Oix01E0(var26, (Function2)ComposableLambdaKt.composableLambda($composer, -1618661481, true, new Function2<Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@Nullable Composer $composer, int $changed) {
                  ComposerKt.sourceInformation($composer, "C145@6247L45,128@5296L1077:InventoryScreens.kt#k2q6ai");
                  if (($changed & 11) == 2 && $composer.getSkipping()) {
                     $composer.skipToGroupEnd();
                  } else {
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventStart(-1618661481, $changed, -1, "com.viernes.mobile.ui.screens.InventoryScreen.<anonymous>.<anonymous> (InventoryScreens.kt:128)");
                     }

                     ButtonKt.Button(new Function0<Unit>() {
                        public final void invoke() {
                           final Double count = StringsKt.toDoubleOrNull(InventoryScreensKt.InventoryScreen$lambda$5(composer$iv));
                           if (count != null && !StringsKt.isBlank((CharSequence)InventoryScreensKt.InventoryScreen$lambda$8(reasonText$delegate))) {
                              BuildersKt.launch$default(coroutineScope, (CoroutineContext)null, (CoroutineStart)null, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
                                 int label;

                                 @Nullable
                                 public final Object invokeSuspend(@NotNull Object $result) {
                                    Object var2 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                                    switch (this.label) {
                                       case 0:
                                          ResultKt.throwOnFailure($result);
                                          InventoryRepository var10000 = inventoryRepo;
                                          long var10001 = patientId;
                                          long var10002 = item.getMedicationId();
                                          double var10003 = count;
                                          String var10004 = InventoryScreensKt.InventoryScreen$lambda$8(reasonText$delegate);
                                          Continuation var10006 = (Continuation)this;
                                          this.label = 1;
                                          if (var10000.manualReconciliation(var10001, var10002, var10003, var10004, "cuidador_movil", var10006) == var2) {
                                             return var2;
                                          }
                                          break;
                                       case 1:
                                          ResultKt.throwOnFailure($result);
                                          break;
                                       default:
                                          throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                                    }

                                    Toast.makeText(context, (CharSequence)"Inventario conciliado exitosamente.", 0).show();
                                    InventoryScreensKt.InventoryScreen$lambda$3(var33, (Inventory)null);
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
                     }, (Modifier)null, false, (Shape)null, ButtonDefaults.INSTANCE.buttonColors-ro_MJ88(ColorKt.getViernesPrimary(), 0L, 0L, 0L, $composer, 6 | ButtonDefaults.$stable << 12, 14), (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-7$app_debug(), $composer, 805306368, 494);
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventEnd();
                     }
                  }

               }
            }), (Modifier)null, (Function2)ComposableLambdaKt.composableLambda($composer, -1488796903, true, new Function2<Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@Nullable Composer $composer, int $changed) {
                  ComposerKt.sourceInformation($composer, "C151@6456L40,151@6435L119:InventoryScreens.kt#k2q6ai");
                  if (($changed & 11) == 2 && $composer.getSkipping()) {
                     $composer.skipToGroupEnd();
                  } else {
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventStart(-1488796903, $changed, -1, "com.viernes.mobile.ui.screens.InventoryScreen.<anonymous>.<anonymous> (InventoryScreens.kt:151)");
                     }

                     $composer.startReplaceableGroup(-1355222310);
                     ComposerKt.sourceInformation($composer, "CC(remember):InventoryScreens.kt#9igjgp");
                     boolean var5 = false;
                     final MutableState var6 = var33;
                     int $i$f$cache = 0;
                     Object it$iv = $composer.rememberedValue();
                     int var9 = 0;
                     Object var10000;
                     if (it$iv == Composer.Companion.getEmpty()) {
                        int var10 = 0;
                        Object value$iv = new Function0<Unit>() {
                           public final void invoke() {
                              InventoryScreensKt.InventoryScreen$lambda$3(var6, (Inventory)null);
                           }
                        };
                        $composer.updateRememberedValue(value$iv);
                        var10000 = value$iv;
                     } else {
                        var10000 = it$iv;
                     }

                     Function0 var3 = (Function0)var10000;
                     $composer.endReplaceableGroup();
                     ButtonKt.TextButton(var3, (Modifier)null, false, (Shape)null, (ButtonColors)null, (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-8$app_debug(), $composer, 805306374, 510);
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventEnd();
                     }
                  }

               }
            }), (Function2)null, (Function2)ComposableLambdaKt.composableLambda($composer, -1358932325, true, new Function2<Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@Nullable Composer $composer, int $changed) {
                  ComposerKt.sourceInformation($composer, "C105@4184L51:InventoryScreens.kt#k2q6ai");
                  if (($changed & 11) == 2 && $composer.getSkipping()) {
                     $composer.skipToGroupEnd();
                  } else {
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventStart(-1358932325, $changed, -1, "com.viernes.mobile.ui.screens.InventoryScreen.<anonymous>.<anonymous> (InventoryScreens.kt:105)");
                     }

                     TextKt.Text--4IGK_g("Conciliación Física: " + item.getMedicationName(), (Modifier)null, 0L, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, (TextStyle)null, $composer, 0, 0, 131070);
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventEnd();
                     }
                  }

               }
            }), (Function2)ComposableLambdaKt.composableLambda($composer, 853483612, true, new Function2<Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@Nullable Composer $composer, int $changed) {
                  ComposerKt.sourceInformation($composer, "C107@4276L958:InventoryScreens.kt#k2q6ai");
                  if (($changed & 11) == 2 && $composer.getSkipping()) {
                     $composer.skipToGroupEnd();
                  } else {
                     if (ComposerKt.isTraceInProgress()) {
                        ComposerKt.traceEventStart(853483612, $changed, -1, "com.viernes.mobile.ui.screens.InventoryScreen.<anonymous>.<anonymous> (InventoryScreens.kt:107)");
                     }

                     int $this$dp$iv = 10;
                     int $i$f$getDp = 0;
                     Arrangement.Vertical verticalArrangement$iv = (Arrangement.Vertical)Arrangement.INSTANCE.spacedBy-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
                     Inventory var6 = item;
                     final MutableState var7 = composer$iv;
                     final MutableState var8 = reasonText$delegate;
                     int $changed$iv = 48;
                     int $i$f$Column = 0;
                     $composer.startReplaceableGroup(-483455358);
                     ComposerKt.sourceInformation($composer, "CC(Column)P(2,3,1)77@3865L61,78@3931L133:Column.kt#2w3rfo");
                     Modifier modifier$iv = (Modifier)Modifier.Companion;
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
                     ComposerKt.sourceInformationMarkerStart($composer, 276693656, "C79@3979L9:Column.kt#2w3rfo");
                     int var29 = 6 | 112 & $changed$iv >> 6;
                     ColumnScope var10000 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                     int var32 = 0;
                     ComposerKt.sourceInformationMarkerStart($composer, -1316775146, "C111@4561L10,108@4356L247,115@4727L19,113@4624L270,121@5018L19,119@4915L301:InventoryScreens.kt#k2q6ai");
                     TextKt.Text--4IGK_g("Existencias en sistema: " + var6.getAvailableQuantity() + " " + var6.getInventoryUnit(), (Modifier)null, ColorKt.getTextSecondary(), 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall(), $composer, 384, 0, 65530);
                     String var33 = InventoryScreensKt.InventoryScreen$lambda$5(var7);
                     Modifier var34 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                     String var55 = var33;
                     $composer.startReplaceableGroup(-1427938908);
                     ComposerKt.sourceInformation($composer, "CC(remember):InventoryScreens.kt#9igjgp");
                     boolean invalid$ivx = false;
                     int $i$f$cache = 0;
                     Object it$iv = $composer.rememberedValue();
                     int var39 = 0;
                     Object var57;
                     if (it$iv == Composer.Companion.getEmpty()) {
                        int var41 = 0;
                        Function1 var10001 = new Function1<String, Unit>() {
                           public final void invoke(@NotNull String it) {
                              Intrinsics.checkNotNullParameter(it, "it");
                              InventoryScreensKt.InventoryScreen$lambda$6(var7, it);
                           }
                        };
                        var55 = var33;
                        Object value$iv = var10001;
                        $composer.updateRememberedValue(value$iv);
                        var57 = value$iv;
                     } else {
                        var57 = it$iv;
                     }

                     Function1 var43 = (Function1)var57;
                     $composer.endReplaceableGroup();
                     OutlinedTextFieldKt.OutlinedTextField(var55, var43, var34, false, false, (TextStyle)null, ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-9$app_debug(), (Function2)null, (Function2)null, (Function2)null, (Function2)null, (Function2)null, (Function2)null, false, (VisualTransformation)null, (KeyboardOptions)null, (KeyboardActions)null, false, 0, 0, (MutableInteractionSource)null, (Shape)null, (TextFieldColors)null, $composer, 1573296, 0, 0, 8388536);
                     var33 = InventoryScreensKt.InventoryScreen$lambda$8(var8);
                     var34 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                     var55 = var33;
                     $composer.startReplaceableGroup(-1427929596);
                     ComposerKt.sourceInformation($composer, "CC(remember):InventoryScreens.kt#9igjgp");
                     invalid$ivx = false;
                     $i$f$cache = 0;
                     it$iv = $composer.rememberedValue();
                     var39 = 0;
                     if (it$iv == Composer.Companion.getEmpty()) {
                        int var52 = 0;
                        Function1 var58 = new Function1<String, Unit>() {
                           public final void invoke(@NotNull String it) {
                              Intrinsics.checkNotNullParameter(it, "it");
                              InventoryScreensKt.InventoryScreen$lambda$9(var8, it);
                           }
                        };
                        var55 = var33;
                        Object value$iv = var58;
                        $composer.updateRememberedValue(value$iv);
                        var57 = value$iv;
                     } else {
                        var57 = it$iv;
                     }

                     var43 = (Function1)var57;
                     $composer.endReplaceableGroup();
                     OutlinedTextFieldKt.OutlinedTextField(var55, var43, var34, false, false, (TextStyle)null, ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-10$app_debug(), (Function2)null, (Function2)null, (Function2)null, (Function2)null, (Function2)null, (Function2)null, false, (VisualTransformation)null, (KeyboardOptions)null, (KeyboardActions)null, false, 0, 0, (MutableInteractionSource)null, (Shape)null, (TextFieldColors)null, $composer, 1573296, 0, 0, 8388536);
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

      ScopeUpdateScope var66 = $composer.endRestartGroup();
      if (var66 != null) {
         var66.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               InventoryScreensKt.InventoryScreen(patientId, inventoryRepo, patientRepo, onNavigateBack, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void InventoryCard(@NotNull final Inventory item, @NotNull final Function0<Unit> onReconcile, @Nullable Composer $composer, final int $changed) {
      Intrinsics.checkNotNullParameter(item, "item");
      Intrinsics.checkNotNullParameter(onReconcile, "onReconcile");
      $composer = $composer.startRestartGroup(885296177);
      ComposerKt.sourceInformation($composer, "C(InventoryCard)166@6756L40,164@6676L1835:InventoryScreens.kt#k2q6ai");
      int $dirty = $changed;
      if (($changed & 14) == 0) {
         $dirty = $changed | ($composer.changed(item) ? 4 : 2);
      }

      if (($changed & 112) == 0) {
         $dirty |= $composer.changedInstance(onReconcile) ? 32 : 16;
      }

      if (($dirty & 91) == 18 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(885296177, $dirty, -1, "com.viernes.mobile.ui.screens.InventoryCard (InventoryScreens.kt:163)");
         }

         Modifier var5 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
         CardColors var6 = CardDefaults.INSTANCE.cardColors-ro_MJ88(ColorKt.getSurfaceDark(), 0L, 0L, 0L, $composer, 6 | CardDefaults.$stable << 12, 14);
         int $this$dp$iv = 12;
         int $i$f$getDp = 0;
         RoundedCornerShape var7 = RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv));
         CardKt.Card(var5, (Shape)var7, var6, (CardElevation)null, (BorderStroke)null, (Function3)ComposableLambdaKt.composableLambda($composer, -2060630877, true, new Function3<ColumnScope, Composer, Integer, Unit>() {
            @Composable
            @ComposableTarget(
               applier = "androidx.compose.ui.UiComposable"
            )
            public final void invoke(@NotNull ColumnScope $this$Card, @Nullable Composer $composer, int $changed) {
               Intrinsics.checkNotNullParameter($this$Card, "$this$Card");
               ComposerKt.sourceInformation($composer, "C169@6856L1649:InventoryScreens.kt#k2q6ai");
               if (($changed & 81) == 16 && $composer.getSkipping()) {
                  $composer.skipToGroupEnd();
               } else {
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-2060630877, $changed, -1, "com.viernes.mobile.ui.screens.InventoryCard.<anonymous> (InventoryScreens.kt:169)");
                  }

                  Modifier var10000 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 14;
                  int $i$f$getDp = 0;
                  Modifier modifier$iv = PaddingKt.padding-3ABfNKs(var10000, Dp.constructor-impl((float)$this$dp$iv));
                  Inventory var7 = item;
                  Function0 var8 = onReconcile;
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
                  ColumnScope var81 = (ColumnScope)ColumnScopeInstance.INSTANCE;
                  int var32 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, -923632929, "C170@6913L799,188@7725L40,191@7957L10,189@7778L252,194@8043L41,195@8097L398:InventoryScreens.kt#k2q6ai");
                  Modifier modifier$ivx = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  Arrangement.Horizontal horizontalArrangement$iv = (Arrangement.Horizontal)Arrangement.INSTANCE.getSpaceBetween();
                  Alignment.Vertical verticalAlignment$iv = Alignment.Companion.getCenterVertically();
                  short $changed$ivx = 438;
                  int $i$f$Row = 0;
                  $composer.startReplaceableGroup(693286680);
                  ComposerKt.sourceInformation($composer, "CC(Row)P(2,1,3)90@4553L58,91@4616L130:Row.kt#2w3rfo");
                  MeasurePolicy measurePolicy$iv = RowKt.rowMeasurePolicy(horizontalArrangement$iv, verticalAlignment$iv, $composer, 14 & $changed$ivx >> 3 | 112 & $changed$ivx >> 3);
                  int $changed$iv$ivx = 112 & $changed$ivx << 3;
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
                  int var56 = 6 | 112 & $changed$ivx >> 6;
                  RowScope var82 = (RowScope)RowScopeInstance.INSTANCE;
                  int var59 = 0;
                  ComposerKt.sourceInformationMarkerStart($composer, 579500951, "C177@7227L10,175@7131L235,183@7509L10,181@7383L315:InventoryScreens.kt#k2q6ai");
                  String var60 = var7.getMedicationName();
                  TextStyle var61 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                  FontWeight var62 = FontWeight.Companion.getBold();
                  long var63 = ColorKt.getViernesPrimaryLight();
                  TextKt.Text--4IGK_g(var60, (Modifier)null, var63, 0L, (FontStyle)null, var62, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var61, $composer, 196992, 0, 65498);
                  double var83 = var7.getAvailableQuantity();
                  var60 = var83 + " " + var7.getInventoryUnit();
                  var61 = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getTitleMedium();
                  var62 = FontWeight.Companion.getBold();
                  var63 = var7.getAvailableQuantity() <= (double)5.0F ? ColorKt.getStatusDelayed() : ColorKt.getStatusConfirmed();
                  TextKt.Text--4IGK_g(var60, (Modifier)null, var63, 0L, (FontStyle)null, var62, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, var61, $composer, 196608, 0, 65498);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  ComposerKt.sourceInformationMarkerEnd($composer);
                  $composer.endReplaceableGroup();
                  $composer.endNode();
                  $composer.endReplaceableGroup();
                  $composer.endReplaceableGroup();
                  Modifier var84 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 6;
                  int $i$f$getDp = 0;
                  SpacerKt.Spacer(SizeKt.height-3ABfNKs(var84, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                  String var85 = var7.getLastReconciliationDate();
                  if (var85 == null) {
                     var85 = "No registrada";
                  }

                  String var10001 = var7.getReconciledBy();
                  if (var10001 == null) {
                     var10001 = "Sistema";
                  }

                  String $this$dp$ivxx = "Última conciliación: " + var85 + " por " + var10001;
                  TextStyle $i$f$getDpxx = MaterialTheme.INSTANCE.getTypography($composer, MaterialTheme.$stable).getBodySmall();
                  long var65 = ColorKt.getTextSecondary();
                  TextKt.Text--4IGK_g($this$dp$ivxx, (Modifier)null, var65, 0L, (FontStyle)null, (FontWeight)null, (FontFamily)null, 0L, (TextDecoration)null, (TextAlign)null, 0L, 0, false, 0, 0, (Function1)null, $i$f$getDpxx, $composer, 384, 0, 65530);
                  Modifier var86 = (Modifier)Modifier.Companion;
                  int $this$dp$iv = 10;
                  int $i$f$getDp = 0;
                  SpacerKt.Spacer(SizeKt.height-3ABfNKs(var86, Dp.constructor-impl((float)$this$dp$iv)), $composer, 6);
                  Modifier var87 = SizeKt.fillMaxWidth$default((Modifier)Modifier.Companion, 0.0F, 1, (Object)null);
                  $this$dp$iv = 8;
                  $i$f$getDp = 0;
                  ButtonKt.OutlinedButton(var8, var87, false, (Shape)RoundedCornerShapeKt.RoundedCornerShape-0680j_4(Dp.constructor-impl((float)$this$dp$iv)), (ButtonColors)null, (ButtonElevation)null, (BorderStroke)null, (PaddingValues)null, (MutableInteractionSource)null, ComposableSingletons$InventoryScreensKt.INSTANCE.getLambda-11$app_debug(), $composer, 805306416, 500);
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

      ScopeUpdateScope var10000 = $composer.endRestartGroup();
      if (var10000 != null) {
         var10000.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               InventoryScreensKt.InventoryCard(item, onReconcile, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1));
            }
         });
      }

   }

   private static final List<Inventory> InventoryScreen$lambda$0(State<? extends List<Inventory>> $inventoryList$delegate) {
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (List)$inventoryList$delegate.getValue();
   }

   private static final Inventory InventoryScreen$lambda$2(MutableState<Inventory> $selectedItemForReconciliation$delegate) {
      State $this$getValue$iv = (State)$selectedItemForReconciliation$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (Inventory)$this$getValue$iv.getValue();
   }

   private static final void InventoryScreen$lambda$3(MutableState<Inventory> $selectedItemForReconciliation$delegate, Inventory value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $selectedItemForReconciliation$delegate.setValue(value);
   }

   private static final String InventoryScreen$lambda$5(MutableState<String> $newQtyText$delegate) {
      State $this$getValue$iv = (State)$newQtyText$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (String)$this$getValue$iv.getValue();
   }

   private static final void InventoryScreen$lambda$6(MutableState<String> $newQtyText$delegate, String value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $newQtyText$delegate.setValue(value);
   }

   private static final String InventoryScreen$lambda$8(MutableState<String> $reasonText$delegate) {
      State $this$getValue$iv = (State)$reasonText$delegate;
      Object var2 = null;
      KProperty property$iv = null;
      int $i$f$getValue = 0;
      return (String)$this$getValue$iv.getValue();
   }

   private static final void InventoryScreen$lambda$9(MutableState<String> $reasonText$delegate, String value) {
      Object var3 = null;
      KProperty property$iv = null;
      int $i$f$setValue = 0;
      $reasonText$delegate.setValue(value);
   }
}
