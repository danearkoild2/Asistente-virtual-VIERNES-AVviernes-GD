package com.viernes.mobile.ui.screens;

import androidx.compose.foundation.layout.ColumnScope;
import androidx.compose.foundation.layout.RowScope;
import androidx.compose.runtime.Composer;
import androidx.compose.runtime.internal.ComposableLambdaKt;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.functions.Function3;
import org.jetbrains.annotations.NotNull;

@Metadata(
   mv = {1, 9, 0},
   k = 3,
   xi = 48
)
public final class ComposableSingletons$SettingsScreenKt {
   @NotNull
   public static final ComposableSingletons$SettingsScreenKt INSTANCE = new ComposableSingletons$SettingsScreenKt();
   @NotNull
   public static Function2<Composer, Integer, Unit> lambda-1;
   @NotNull
   public static Function2<Composer, Integer, Unit> lambda-2;
   @NotNull
   public static Function3<ColumnScope, Composer, Integer, Unit> lambda-3;
   @NotNull
   public static Function3<RowScope, Composer, Integer, Unit> lambda-4;
   @NotNull
   public static Function3<RowScope, Composer, Integer, Unit> lambda-5;

   public ComposableSingletons$SettingsScreenKt() {
   }

   @NotNull
   public final Function2<Composer, Integer, Unit> getLambda_1$app_debug/* $FF was: getLambda-1$app_debug*/() {
      return lambda-1;
   }

   @NotNull
   public final Function2<Composer, Integer, Unit> getLambda_2$app_debug/* $FF was: getLambda-2$app_debug*/() {
      return lambda-2;
   }

   @NotNull
   public final Function3<ColumnScope, Composer, Integer, Unit> getLambda_3$app_debug/* $FF was: getLambda-3$app_debug*/() {
      return lambda-3;
   }

   @NotNull
   public final Function3<RowScope, Composer, Integer, Unit> getLambda_4$app_debug/* $FF was: getLambda-4$app_debug*/() {
      return lambda-4;
   }

   @NotNull
   public final Function3<RowScope, Composer, Integer, Unit> getLambda_5$app_debug/* $FF was: getLambda-5$app_debug*/() {
      return lambda-5;
   }

   static {
      lambda-1 = (Function2)ComposableLambdaKt.composableLambdaInstance(-415381124, false, null.INSTANCE);
      lambda-2 = (Function2)ComposableLambdaKt.composableLambdaInstance(-533732837, false, null.INSTANCE);
      lambda-3 = (Function3)ComposableLambdaKt.composableLambdaInstance(1530212149, false, null.INSTANCE);
      lambda-4 = (Function3)ComposableLambdaKt.composableLambdaInstance(-996362835, false, null.INSTANCE);
      lambda-5 = (Function3)ComposableLambdaKt.composableLambdaInstance(914752724, false, null.INSTANCE);
   }
}
