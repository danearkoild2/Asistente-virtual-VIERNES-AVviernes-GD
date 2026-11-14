package com.viernes.mobile.ui.screens;

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
public final class ComposableSingletons$PatientScreensKt {
   @NotNull
   public static final ComposableSingletons$PatientScreensKt INSTANCE = new ComposableSingletons$PatientScreensKt();
   @NotNull
   public static Function2<Composer, Integer, Unit> lambda-1;
   @NotNull
   public static Function3<RowScope, Composer, Integer, Unit> lambda-2;

   public ComposableSingletons$PatientScreensKt() {
   }

   @NotNull
   public final Function2<Composer, Integer, Unit> getLambda_1$app_debug/* $FF was: getLambda-1$app_debug*/() {
      return lambda-1;
   }

   @NotNull
   public final Function3<RowScope, Composer, Integer, Unit> getLambda_2$app_debug/* $FF was: getLambda-2$app_debug*/() {
      return lambda-2;
   }

   static {
      lambda-1 = (Function2)ComposableLambdaKt.composableLambdaInstance(1667888295, false, null.INSTANCE);
      lambda-2 = (Function3)ComposableLambdaKt.composableLambdaInstance(-307753153, false, null.INSTANCE);
   }
}
