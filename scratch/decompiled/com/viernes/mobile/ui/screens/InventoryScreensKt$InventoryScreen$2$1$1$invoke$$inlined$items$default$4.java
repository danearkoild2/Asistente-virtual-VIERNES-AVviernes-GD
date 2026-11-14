package com.viernes.mobile.ui.screens;

import androidx.compose.foundation.lazy.LazyItemScope;
import androidx.compose.runtime.Composable;
import androidx.compose.runtime.Composer;
import androidx.compose.runtime.ComposerKt;
import androidx.compose.runtime.MutableState;
import com.viernes.mobile.domain.model.Inventory;
import java.util.List;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function4;
import kotlin.jvm.internal.Lambda;
import kotlin.jvm.internal.SourceDebugExtension;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 3,
   xi = 48,
   d1 = {"\u0000\u0016\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\b\n\u0002\b\u0003\u0010\u0000\u001a\u00020\u0001\"\u0004\b\u0000\u0010\u0002*\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H\u000b¢\u0006\u0004\b\u0006\u0010\u0007¨\u0006\b"},
   d2 = {"<anonymous>", "", "T", "Landroidx/compose/foundation/lazy/LazyItemScope;", "it", "", "invoke", "(Landroidx/compose/foundation/lazy/LazyItemScope;ILandroidx/compose/runtime/Composer;I)V", "androidx/compose/foundation/lazy/LazyDslKt$items$4"}
)
@SourceDebugExtension({"SMAP\nLazyDsl.kt\nKotlin\n*S Kotlin\n*F\n+ 1 LazyDsl.kt\nandroidx/compose/foundation/lazy/LazyDslKt$items$4\n+ 2 InventoryScreens.kt\ncom/viernes/mobile/ui/screens/InventoryScreensKt$InventoryScreen$2$1$1\n+ 3 Composer.kt\nandroidx/compose/runtime/ComposerKt\n*L\n1#1,426:1\n87#2,3:427\n95#2:436\n1116#3,6:430\n*S KotlinDebug\n*F\n+ 1 InventoryScreens.kt\ncom/viernes/mobile/ui/screens/InventoryScreensKt$InventoryScreen$2$1$1\n*L\n89#1:430,6\n*E\n"})
public final class InventoryScreensKt$InventoryScreen$2$1$1$invoke$$inlined$items$default$4 extends Lambda implements Function4<LazyItemScope, Integer, Composer, Integer, Unit> {
   // $FF: synthetic field
   final List $items;
   // $FF: synthetic field
   final MutableState $selectedItemForReconciliation$delegate$inlined;
   // $FF: synthetic field
   final MutableState $newQtyText$delegate$inlined;
   // $FF: synthetic field
   final MutableState $reasonText$delegate$inlined;

   public InventoryScreensKt$InventoryScreen$2$1$1$invoke$$inlined$items$default$4(List $items, MutableState var2, MutableState var3, MutableState var4) {
      super(4);
      this.$items = $items;
      this.$selectedItemForReconciliation$delegate$inlined = var2;
      this.$newQtyText$delegate$inlined = var3;
      this.$reasonText$delegate$inlined = var4;
   }

   @Composable
   public final void invoke(@NotNull LazyItemScope $this$items, int it, @Nullable Composer $composer, int $changed) {
      // $FF: Couldn't be decompiled
   }
}
