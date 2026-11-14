package com.viernes.mobile.data.repository;

import kotlin.Metadata;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.coroutines.jvm.internal.DebugMetadata;
import kotlin.jvm.internal.SourceDebugExtension;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 3,
   xi = 48
)
@DebugMetadata(
   f = "Repositories.kt",
   l = {224, 225, 219},
   i = {0, 0, 0, 1, 1, 1, 1},
   s = {"L$0", "L$2", "L$4", "L$0", "L$2", "L$4", "L$6"},
   n = {"this", "destination$iv$iv", "entity", "this", "destination$iv$iv", "entity", "med"},
   m = "emit",
   c = "com.viernes.mobile.data.repository.IntakeRepository$getIntakesForDate$$inlined$map$1$2"
)
@SourceDebugExtension({"SMAP\nEmitters.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt$unsafeTransform$1$1$emit$1\n*L\n1#1,218:1\n*E\n"})
public final class IntakeRepository$getIntakesForDate$$inlined$map$1$2$1 extends ContinuationImpl {
   // $FF: synthetic field
   Object result;
   int label;
   Object L$0;
   // $FF: synthetic field
   final IntakeRepository$getIntakesForDate$$inlined$map$1$2 this$0;
   Object L$1;
   Object L$2;
   Object L$3;
   Object L$4;
   Object L$5;
   Object L$6;

   public IntakeRepository$getIntakesForDate$$inlined$map$1$2$1(IntakeRepository$getIntakesForDate$$inlined$map$1$2 this$0, Continuation $completion) {
      super($completion);
      this.this$0 = this$0;
   }

   @Nullable
   public final Object invokeSuspend(@NotNull Object $result) {
      this.result = $result;
      this.label |= Integer.MIN_VALUE;
      return this.this$0.emit((Object)null, (Continuation)this);
   }
}
