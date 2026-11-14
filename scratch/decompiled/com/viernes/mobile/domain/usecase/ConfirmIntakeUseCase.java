package com.viernes.mobile.domain.usecase;

import androidx.compose.runtime.internal.StabilityInferred;
import com.viernes.mobile.data.repository.CaregiverRepository;
import com.viernes.mobile.data.repository.IntakeRepository;
import com.viernes.mobile.domain.model.Intake;
import com.viernes.mobile.domain.model.IntakeStatus;
import kotlin.Metadata;
import kotlin.Result;
import kotlin.ResultKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.Boxing;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.internal.Intrinsics;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u00006\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010\u000b\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0004\b\u0007\u0018\u00002\u00020\u0001B\u0015\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005¢\u0006\u0002\u0010\u0006J@\u0010\u0007\u001a\b\u0012\u0004\u0012\u00020\t0\b2\u0006\u0010\n\u001a\u00020\u000b2\u0006\u0010\f\u001a\u00020\r2\u0006\u0010\u000e\u001a\u00020\u000f2\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\rH\u0086Bø\u0001\u0000ø\u0001\u0001¢\u0006\u0004\b\u0011\u0010\u0012R\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000\u0082\u0002\u000b\n\u0002\b!\n\u0005\b¡\u001e0\u0001¨\u0006\u0013"},
   d2 = {"Lcom/viernes/mobile/domain/usecase/ConfirmIntakeUseCase;", "", "intakeRepo", "Lcom/viernes/mobile/data/repository/IntakeRepository;", "caregiverRepo", "Lcom/viernes/mobile/data/repository/CaregiverRepository;", "(Lcom/viernes/mobile/data/repository/IntakeRepository;Lcom/viernes/mobile/data/repository/CaregiverRepository;)V", "invoke", "Lkotlin/Result;", "", "intakeId", "", "userId", "", "status", "Lcom/viernes/mobile/domain/model/IntakeStatus;", "notes", "invoke-yxL6bBk", "(JLjava/lang/String;Lcom/viernes/mobile/domain/model/IntakeStatus;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class ConfirmIntakeUseCase {
   @NotNull
   private final IntakeRepository intakeRepo;
   @NotNull
   private final CaregiverRepository caregiverRepo;
   public static final int $stable;

   public ConfirmIntakeUseCase(@NotNull IntakeRepository intakeRepo, @NotNull CaregiverRepository caregiverRepo) {
      Intrinsics.checkNotNullParameter(intakeRepo, "intakeRepo");
      Intrinsics.checkNotNullParameter(caregiverRepo, "caregiverRepo");
      super();
      this.intakeRepo = intakeRepo;
      this.caregiverRepo = caregiverRepo;
   }

   @Nullable
   public final Object invoke_yxL6bBk/* $FF was: invoke-yxL6bBk*/(long intakeId, @NotNull String userId, @NotNull IntakeStatus status, @Nullable String notes, @NotNull Continuation<? super Result<Boolean>> var6) {
      label60: {
         if (var6 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label60;
            }
         }

         $continuation = new ContinuationImpl(var6) {
            Object L$0;
            Object L$1;
            Object L$2;
            Object L$3;
            Object L$4;
            long J$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               Object var10000 = ConfirmIntakeUseCase.this.invoke-yxL6bBk(0L, (String)null, (IntakeStatus)null, (String)null, (Continuation)this);
               return var10000 == IntrinsicsKt.getCOROUTINE_SUSPENDED() ? var10000 : Result.box-impl(var10000);
            }
         };
      }

      Object var10000;
      label64: {
         Intake intake;
         Object var12;
         label65: {
            Object $result = $continuation.result;
            var12 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
            switch ($continuation.label) {
               case 0:
                  ResultKt.throwOnFailure($result);
                  IntakeRepository var15 = this.intakeRepo;
                  $continuation.L$0 = this;
                  $continuation.L$1 = userId;
                  $continuation.L$2 = status;
                  $continuation.L$3 = notes;
                  $continuation.J$0 = intakeId;
                  $continuation.label = 1;
                  var10000 = var15.getIntakeById(intakeId, $continuation);
                  if (var10000 == var12) {
                     return var12;
                  }
                  break;
               case 1:
                  intakeId = $continuation.J$0;
                  notes = (String)$continuation.L$3;
                  status = (IntakeStatus)$continuation.L$2;
                  userId = (String)$continuation.L$1;
                  this = (ConfirmIntakeUseCase)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break;
               case 2:
                  intakeId = $continuation.J$0;
                  intake = (Intake)$continuation.L$4;
                  notes = (String)$continuation.L$3;
                  status = (IntakeStatus)$continuation.L$2;
                  userId = (String)$continuation.L$1;
                  this = (ConfirmIntakeUseCase)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break label65;
               case 3:
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break label64;
               default:
                  throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
            }

            Intake var16 = (Intake)var10000;
            if (var16 == null) {
               Result.Companion var22 = Result.Companion;
               return Result.constructor-impl(ResultKt.createFailure((Throwable)(new IllegalArgumentException("La toma especificada #" + intakeId + " no existe."))));
            }

            intake = var16;
            CaregiverRepository var17 = this.caregiverRepo;
            long var10002 = intake.getPatientId();
            $continuation.L$0 = this;
            $continuation.L$1 = userId;
            $continuation.L$2 = status;
            $continuation.L$3 = notes;
            $continuation.L$4 = intake;
            $continuation.J$0 = intakeId;
            $continuation.label = 2;
            var10000 = var17.checkPermission(userId, var10002, "confirm_intake", $continuation);
            if (var10000 == var12) {
               return var12;
            }
         }

         boolean hasPermission = (Boolean)var10000;
         if (!hasPermission) {
            Result.Companion var21 = Result.Companion;
            return Result.constructor-impl(ResultKt.createFailure((Throwable)(new SecurityException("El usuario " + userId + " no tiene permiso para confirmar tomas de este paciente."))));
         }

         if (intake.getStatus() == IntakeStatus.CONFIRMED && status == IntakeStatus.CONFIRMED) {
            Result.Companion var20 = Result.Companion;
            return Result.constructor-impl(ResultKt.createFailure((Throwable)(new IllegalStateException("Esta dosis ya fue confirmada previamente como administrada."))));
         }

         IntakeRepository var18 = this.intakeRepo;
         $continuation.L$0 = null;
         $continuation.L$1 = null;
         $continuation.L$2 = null;
         $continuation.L$3 = null;
         $continuation.L$4 = null;
         $continuation.label = 3;
         var10000 = var18.confirmIntake(intakeId, status, userId, notes, $continuation);
         if (var10000 == var12) {
            return var12;
         }
      }

      boolean success = (Boolean)var10000;
      Result.Companion var19 = Result.Companion;
      return Result.constructor-impl(Boxing.boxBoolean(success));
   }

   // $FF: synthetic method
   public static Object invoke_yxL6bBk$default/* $FF was: invoke-yxL6bBk$default*/(ConfirmIntakeUseCase var0, long var1, String var3, IntakeStatus var4, String var5, Continuation var6, int var7, Object var8) {
      if ((var7 & 8) != 0) {
         var5 = null;
      }

      return var0.invoke-yxL6bBk(var1, var3, var4, var5, var6);
   }
}
