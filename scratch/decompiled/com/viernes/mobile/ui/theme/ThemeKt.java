package com.viernes.mobile.ui.theme;

import android.app.Activity;
import android.content.Context;
import android.view.View;
import android.view.Window;
import androidx.compose.foundation.DarkThemeKt;
import androidx.compose.material3.ColorScheme;
import androidx.compose.material3.ColorSchemeKt;
import androidx.compose.material3.MaterialThemeKt;
import androidx.compose.material3.Shapes;
import androidx.compose.runtime.Composable;
import androidx.compose.runtime.ComposableInferredTarget;
import androidx.compose.runtime.Composer;
import androidx.compose.runtime.ComposerKt;
import androidx.compose.runtime.CompositionLocal;
import androidx.compose.runtime.EffectsKt;
import androidx.compose.runtime.RecomposeScopeImplKt;
import androidx.compose.runtime.ScopeUpdateScope;
import androidx.compose.ui.platform.AndroidCompositionLocals_androidKt;
import androidx.core.view.WindowCompat;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 2,
   xi = 48,
   d1 = {"\u0000 \n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000b\n\u0000\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\u001a*\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00052\u0011\u0010\u0006\u001a\r\u0012\u0004\u0012\u00020\u00030\u0007¢\u0006\u0002\b\bH\u0007¢\u0006\u0002\u0010\t\"\u000e\u0010\u0000\u001a\u00020\u0001X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\n"},
   d2 = {"DarkColorScheme", "Landroidx/compose/material3/ColorScheme;", "ViernesMobileTheme", "", "darkTheme", "", "content", "Lkotlin/Function0;", "Landroidx/compose/runtime/Composable;", "(ZLkotlin/jvm/functions/Function2;Landroidx/compose/runtime/Composer;II)V", "app_debug"}
)
@SourceDebugExtension({"SMAP\nTheme.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Theme.kt\ncom/viernes/mobile/ui/theme/ThemeKt\n+ 2 CompositionLocal.kt\nandroidx/compose/runtime/CompositionLocal\n*L\n1#1,53:1\n74#2:54\n*S KotlinDebug\n*F\n+ 1 Theme.kt\ncom/viernes/mobile/ui/theme/ThemeKt\n*L\n36#1:54\n*E\n"})
public final class ThemeKt {
   @NotNull
   private static final ColorScheme DarkColorScheme = ColorSchemeKt.darkColorScheme-C-Xl9yA$default(ColorKt.getViernesPrimary(), ColorKt.getTextPrimary(), ColorKt.getViernesPrimaryDark(), ColorKt.getTextPrimary(), 0L, ColorKt.getViernesAccent(), ColorKt.getTextPrimary(), 0L, 0L, 0L, 0L, 0L, 0L, ColorKt.getBackgroundDark(), ColorKt.getTextPrimary(), ColorKt.getSurfaceDark(), ColorKt.getTextPrimary(), ColorKt.getSurfaceElevated(), ColorKt.getTextSecondary(), 0L, 0L, 0L, ColorKt.getStatusDelayed(), ColorKt.getTextPrimary(), 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, -13099120, 15, (Object)null);

   @Composable
   @ComposableInferredTarget(
      scheme = "[0[0]]"
   )
   public static final void ViernesMobileTheme(final boolean darkTheme, @NotNull final Function2<? super Composer, ? super Integer, Unit> content, @Nullable Composer $composer, final int $changed, final int var4) {
      Intrinsics.checkNotNullParameter(content, "content");
      $composer = $composer.startRestartGroup(-907027100);
      ComposerKt.sourceInformation($composer, "C(ViernesMobileTheme)P(1)30@934L21,35@1122L7,46@1579L114:Theme.kt#kd0rz8");
      int $dirty = $changed;
      if ((var4 & 2) != 0) {
         $dirty = $changed | 48;
      } else if (($changed & 112) == 0) {
         $dirty = $changed | ($composer.changedInstance(content) ? 32 : 16);
      }

      if (($dirty & 81) == 16 && $composer.getSkipping()) {
         $composer.skipToGroupEnd();
      } else {
         $composer.startDefaults();
         if (($changed & 1) != 0 && !$composer.getDefaultsInvalid()) {
            $composer.skipToGroupEnd();
            if ((var4 & 1) != 0) {
               $dirty &= -15;
            }
         } else if ((var4 & 1) != 0) {
            darkTheme = DarkThemeKt.isSystemInDarkTheme($composer, 0);
            $dirty &= -15;
         }

         $composer.endDefaults();
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventStart(-907027100, $dirty, -1, "com.viernes.mobile.ui.theme.ViernesMobileTheme (Theme.kt:32)");
         }

         ColorScheme colorScheme = DarkColorScheme;
         CompositionLocal this_$iv = (CompositionLocal)AndroidCompositionLocals_androidKt.getLocalView();
         int $changed$iv = 0;
         int $i$f$getCurrent = 0;
         ComposerKt.sourceInformationMarkerStart($composer, 2023513938, "CC:CompositionLocal.kt#9igjgp");
         Object var11 = $composer.consume(this_$iv);
         ComposerKt.sourceInformationMarkerEnd($composer);
         final View view = (View)var11;
         $composer.startReplaceableGroup(-1824313388);
         ComposerKt.sourceInformation($composer, "37@1168L399");
         if (!view.isInEditMode()) {
            EffectsKt.SideEffect(new Function0<Unit>() {
               public final void invoke() {
                  Context var10000 = view.getContext();
                  Intrinsics.checkNotNull(var10000, "null cannot be cast to non-null type android.app.Activity");
                  Window window = ((Activity)var10000).getWindow();
                  window.setStatusBarColor(androidx.compose.ui.graphics.ColorKt.toArgb-8_81llA(ColorKt.getBackgroundDark()));
                  window.setNavigationBarColor(androidx.compose.ui.graphics.ColorKt.toArgb-8_81llA(ColorKt.getBackgroundDark()));
                  WindowCompat.getInsetsController(window, view).setAppearanceLightStatusBars(false);
                  WindowCompat.getInsetsController(window, view).setAppearanceLightNavigationBars(false);
               }
            }, $composer, 0);
         }

         $composer.endReplaceableGroup();
         MaterialThemeKt.MaterialTheme(colorScheme, (Shapes)null, TypeKt.getTypography(), content, $composer, 390 | 7168 & $dirty << 6, 2);
         if (ComposerKt.isTraceInProgress()) {
            ComposerKt.traceEventEnd();
         }
      }

      ScopeUpdateScope var10000 = $composer.endRestartGroup();
      if (var10000 != null) {
         var10000.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               ThemeKt.ViernesMobileTheme(darkTheme, content, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1), var4);
            }
         });
      }

   }
}
