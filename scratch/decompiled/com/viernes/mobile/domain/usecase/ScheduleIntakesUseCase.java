package com.viernes.mobile.domain.usecase;

import androidx.compose.runtime.internal.StabilityInferred;
import com.viernes.mobile.data.repository.IntakeRepository;
import com.viernes.mobile.data.repository.MedicationRepository;
import com.viernes.mobile.domain.model.Medication;
import java.util.List;
import kotlin.Metadata;
import kotlin.Result;
import kotlin.ResultKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.internal.Intrinsics;
import kotlin.text.StringsKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u00000\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0003\b\u0007\u0018\u00002\u00020\u0001B\u0015\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005¢\u0006\u0002\u0010\u0006J4\u0010\u0007\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\n0\t0\b2\u0006\u0010\u000b\u001a\u00020\n2\b\b\u0002\u0010\f\u001a\u00020\rH\u0086Bø\u0001\u0000ø\u0001\u0001¢\u0006\u0004\b\u000e\u0010\u000fR\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000\u0082\u0002\u000b\n\u0002\b!\n\u0005\b¡\u001e0\u0001¨\u0006\u0010"},
   d2 = {"Lcom/viernes/mobile/domain/usecase/ScheduleIntakesUseCase;", "", "medicationRepo", "Lcom/viernes/mobile/data/repository/MedicationRepository;", "intakeRepo", "Lcom/viernes/mobile/data/repository/IntakeRepository;", "(Lcom/viernes/mobile/data/repository/MedicationRepository;Lcom/viernes/mobile/data/repository/IntakeRepository;)V", "invoke", "Lkotlin/Result;", "", "", "medicationId", "daysAhead", "", "invoke-0E7RQCE", "(JILkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class ScheduleIntakesUseCase {
   @NotNull
   private final MedicationRepository medicationRepo;
   @NotNull
   private final IntakeRepository intakeRepo;
   public static final int $stable;

   public ScheduleIntakesUseCase(@NotNull MedicationRepository medicationRepo, @NotNull IntakeRepository intakeRepo) {
      Intrinsics.checkNotNullParameter(medicationRepo, "medicationRepo");
      Intrinsics.checkNotNullParameter(intakeRepo, "intakeRepo");
      super();
      this.medicationRepo = medicationRepo;
      this.intakeRepo = intakeRepo;
   }

   @Nullable
   public final Object invoke_0E7RQCE/* $FF was: invoke-0E7RQCE*/(long medicationId, int daysAhead, @NotNull Continuation<? super Result<? extends List<Long>>> var4) {
      label76: {
         if (var4 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label76;
            }
         }

         $continuation = new ContinuationImpl(var4) {
            Object L$0;
            long J$0;
            int I$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               Object var10000 = ScheduleIntakesUseCase.this.invoke-0E7RQCE(0L, 0, (Continuation)this);
               return var10000 == IntrinsicsKt.getCOROUTINE_SUSPENDED() ? var10000 : Result.box-impl(var10000);
            }
         };
      }

      Object var14;
      Exception var10000;
      label67: {
         label82: {
            Object $result = $continuation.result;
            Object var10 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
            Object var17;
            switch ($continuation.label) {
               case 0:
                  ResultKt.throwOnFailure($result);
                  MedicationRepository var18 = this.medicationRepo;
                  $continuation.L$0 = this;
                  $continuation.J$0 = medicationId;
                  $continuation.I$0 = daysAhead;
                  $continuation.label = 1;
                  var17 = var18.getMedicationById(medicationId, $continuation);
                  if (var17 == var10) {
                     return var10;
                  }
                  break;
               case 1:
                  daysAhead = $continuation.I$0;
                  medicationId = $continuation.J$0;
                  this = (ScheduleIntakesUseCase)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  var17 = $result;
                  break;
               case 2:
                  try {
                     ResultKt.throwOnFailure($result);
                     var16 = $result;
                     break label82;
                  } catch (Exception var13) {
                     var10000 = var13;
                     boolean var10001 = false;
                     break label67;
                  }
               default:
                  throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
            }

            Medication var19 = (Medication)var17;
            if (var19 == null) {
               Result.Companion var25 = Result.Companion;
               return Result.constructor-impl(ResultKt.createFailure((Throwable)(new IllegalArgumentException("Medicamento #" + medicationId + " no encontrado."))));
            }

            Medication medication = var19;
            if (!medication.isVerifiedAndActive()) {
               Result.Companion var24 = Result.Companion;
               String var10002 = medication.getTranscribedName();
               return Result.constructor-impl(ResultKt.createFailure((Throwable)(new IllegalStateException("Seguridad médica: El tratamiento '" + var10002 + "' se encuentra en estado '" + medication.getVerificationStatus().getValue() + "' y NO puede generar órdenes de administración hasta su verificación formal."))));
            }

            CharSequence var6 = (CharSequence)medication.getExactScheduleHours();
            if (var6 == null || StringsKt.isBlank(var6)) {
               Result.Companion var23 = Result.Companion;
               return Result.constructor-impl(ResultKt.createFailure((Throwable)(new IllegalStateException("El tratamiento '" + medication.getTranscribedName() + "' no tiene horarios exactos confirmados (exactScheduleHours está vacío)."))));
            }

            try {
               IntakeRepository var20 = this.intakeRepo;
               $continuation.L$0 = null;
               $continuation.label = 2;
               var16 = var20.generateIntakesForMedication(medication, daysAhead, $continuation);
            } catch (Exception var12) {
               var10000 = var12;
               boolean var26 = false;
               break label67;
            }

            if (var16 == var10) {
               return var10;
            }
         }

         try {
            List generated = (List)var16;
            Result.Companion var22 = Result.Companion;
            var14 = Result.constructor-impl(generated);
            return var14;
         } catch (Exception var11) {
            var10000 = var11;
            boolean var27 = false;
         }
      }

      Exception e = var10000;
      Result.Companion var21 = Result.Companion;
      var14 = Result.constructor-impl(ResultKt.createFailure((Throwable)e));
      return var14;
   }

   // $FF: synthetic method
   public static Object invoke_0E7RQCE$default/* $FF was: invoke-0E7RQCE$default*/(ScheduleIntakesUseCase var0, long var1, int var3, Continuation var4, int var5, Object var6) {
      if ((var5 & 2) != 0) {
         var3 = 7;
      }

      return var0.invoke-0E7RQCE(var1, var3, var4);
   }
}
