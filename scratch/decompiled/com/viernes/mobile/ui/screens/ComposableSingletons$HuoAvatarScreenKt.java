package com.viernes.mobile.ui.screens;

import androidx.compose.runtime.Composer;
import androidx.compose.runtime.internal.ComposableLambdaKt;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.jvm.functions.Function2;
import org.jetbrains.annotations.NotNull;

@Metadata(
   mv = {1, 9, 0},
   k = 3,
   xi = 48
)
public final class ComposableSingletons$HuoAvatarScreenKt {
   @NotNull
   public static final ComposableSingletons$HuoAvatarScreenKt INSTANCE = new ComposableSingletons$HuoAvatarScreenKt();
   @NotNull
   public static Function2<Composer, Integer, Unit> lambda-1;
   @NotNull
   public static Function2<Composer, Integer, Unit> lambda-2;

   public ComposableSingletons$HuoAvatarScreenKt() {
   }

   @NotNull
   public final Function2<Composer, Integer, Unit> getLambda_1$app_debug/* $FF was: getLambda-1$app_debug*/() {
      return lambda-1;
   }

   @NotNull
   public final Function2<Composer, Integer, Unit> getLambda_2$app_debug/* $FF was: getLambda-2$app_debug*/() {
      return lambda-2;
   }

   static {
      lambda-1 = (Function2)ComposableLambdaKt.composableLambdaInstance(1634702773, false, null.INSTANCE);
      lambda-2 = (Function2)ComposableLambdaKt.composableLambdaInstance(-200418028, false, null.INSTANCE);
   }
}
