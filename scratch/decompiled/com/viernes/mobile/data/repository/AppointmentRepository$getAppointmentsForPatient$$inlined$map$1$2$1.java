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
   f = "AdditionalRepositories.kt",
   l = {219},
   i = {},
   s = {},
   n = {},
   m = "emit",
   c = "com.viernes.mobile.data.repository.AppointmentRepository$getAppointmentsForPatient$$inlined$map$1$2"
)
@SourceDebugExtension({"SMAP\nEmitters.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt$unsafeTransform$1$1$emit$1\n*L\n1#1,218:1\n*E\n"})
public final class AppointmentRepository$getAppointmentsForPatient$$inlined$map$1$2$1 extends ContinuationImpl {
   // $FF: synthetic field
   Object result;
   int label;
   Object L$0;
   // $FF: synthetic field
   final AppointmentRepository$getAppointmentsForPatient$$inlined$map$1$2 this$0;

   public AppointmentRepository$getAppointmentsForPatient$$inlined$map$1$2$1(AppointmentRepository$getAppointmentsForPatient$$inlined$map$1$2 this$0, Continuation $completion) {
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
