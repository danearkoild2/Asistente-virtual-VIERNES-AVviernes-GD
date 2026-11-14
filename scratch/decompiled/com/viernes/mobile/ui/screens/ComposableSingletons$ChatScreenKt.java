package com.viernes.mobile.ui.screens;

import androidx.compose.foundation.lazy.LazyItemScope;
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
public final class ComposableSingletons$ChatScreenKt {
   @NotNull
   public static final ComposableSingletons$ChatScreenKt INSTANCE = new ComposableSingletons$ChatScreenKt();
   @NotNull
   public static Function2<Composer, Integer, Unit> lambda-1;
   @NotNull
   public static Function3<LazyItemScope, Composer, Integer, Unit> lambda-2;
   @NotNull
   public static Function3<LazyItemScope, Composer, Integer, Unit> lambda-3;
   @NotNull
   public static Function2<Composer, Integer, Unit> lambda-4;

   public ComposableSingletons$ChatScreenKt() {
   }

   @NotNull
   public final Function2<Composer, Integer, Unit> getLambda_1$app_debug/* $FF was: getLambda-1$app_debug*/() {
      return lambda-1;
   }

   @NotNull
   public final Function3<LazyItemScope, Composer, Integer, Unit> getLambda_2$app_debug/* $FF was: getLambda-2$app_debug*/() {
      return lambda-2;
   }

   @NotNull
   public final Function3<LazyItemScope, Composer, Integer, Unit> getLambda_3$app_debug/* $FF was: getLambda-3$app_debug*/() {
      return lambda-3;
   }

   @NotNull
   public final Function2<Composer, Integer, Unit> getLambda_4$app_debug/* $FF was: getLambda-4$app_debug*/() {
      return lambda-4;
   }

   static {
      lambda-1 = (Function2)ComposableLambdaKt.composableLambdaInstance(880143239, false, null.INSTANCE);
      lambda-2 = (Function3)ComposableLambdaKt.composableLambdaInstance(344180931, false, null.INSTANCE);
      lambda-3 = (Function3)ComposableLambdaKt.composableLambdaInstance(485281146, false, null.INSTANCE);
      lambda-4 = (Function2)ComposableLambdaKt.composableLambdaInstance(1423088140, false, null.INSTANCE);
   }
}
