package com.viernes.mobile.data.repository;

import com.viernes.mobile.data.local.dao.MedicationDao;
import com.viernes.mobile.data.local.dao.PatientDao;
import com.viernes.mobile.data.local.entity.IntakeEntity;
import com.viernes.mobile.data.local.entity.MedicationEntity;
import com.viernes.mobile.data.local.entity.PatientEntity;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.collections.CollectionsKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.text.StringsKt;
import kotlinx.coroutines.flow.FlowCollector;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 3,
   xi = 48,
   d1 = {"\u0000\n\n\u0000\n\u0002\u0010\u0002\n\u0002\b\u0007\u0010\u0000\u001a\u00020\u0001\"\u0004\b\u0000\u0010\u0002\"\u0004\b\u0001\u0010\u00032\u0006\u0010\u0004\u001a\u0002H\u0002H\u008a@¢\u0006\u0004\b\u0005\u0010\u0006¨\u0006\b"},
   d2 = {"<anonymous>", "", "T", "R", "value", "emit", "(Ljava/lang/Object;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "kotlinx/coroutines/flow/FlowKt__EmittersKt$unsafeTransform$1$1", "kotlinx/coroutines/flow/FlowKt__TransformKt$map$$inlined$unsafeTransform$1$2"}
)
@SourceDebugExtension({"SMAP\nEmitters.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt$unsafeTransform$1$1\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Repositories.kt\ncom/viernes/mobile/data/repository/IntakeRepository\n+ 4 _Collections.kt\nkotlin/collections/CollectionsKt___CollectionsKt\n*L\n1#1,218:1\n50#2:219\n221#3:220\n222#3,12:224\n1549#4:221\n1620#4,2:222\n1622#4:236\n*S KotlinDebug\n*F\n+ 1 Repositories.kt\ncom/viernes/mobile/data/repository/IntakeRepository\n*L\n221#1:221\n221#1:222,2\n221#1:236\n*E\n"})
public final class IntakeRepository$getIntakesForDate$$inlined$map$1$2<T> implements FlowCollector {
   // $FF: synthetic field
   final FlowCollector $this_unsafeFlow;
   // $FF: synthetic field
   final IntakeRepository this$0;

   public IntakeRepository$getIntakesForDate$$inlined$map$1$2(FlowCollector $receiver, IntakeRepository var2) {
      this.$this_unsafeFlow = $receiver;
      this.this$0 = var2;
   }

   @Nullable
   public final Object emit(Object value, @NotNull Continuation var2) {
      label119: {
         if (var2 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label119;
            }
         }

         $continuation = new IntakeRepository$getIntakesForDate$$inlined$map$1$2$1(this, var2);
      }

      Object $result = $continuation.result;
      Object var5 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      FlowCollector var9;
      Collection destination$iv$iv;
      Iterator var17;
      IntakeEntity entity;
      Collection var20;
      MedicationEntity med;
      Object var10000;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            FlowCollector $this$map_u24lambda_u245 = this.$this_unsafeFlow;
            int var28 = 0;
            var9 = $this$map_u24lambda_u245;
            Continuation var50 = $continuation;
            List list = (List)value;
            int var30 = 0;
            Iterable $this$map$iv = (Iterable)list;
            int $i$f$map = 0;
            destination$iv$iv = (Collection)(new ArrayList(CollectionsKt.collectionSizeOrDefault($this$map$iv, 10)));
            int $i$f$mapTo = 0;
            var17 = $this$map$iv.iterator();
            if (!var17.hasNext()) {
               List var57 = (List)destination$iv$iv;
               $continuation.L$0 = null;
               $continuation.L$1 = null;
               $continuation.L$2 = null;
               $continuation.L$3 = null;
               $continuation.L$4 = null;
               $continuation.L$5 = null;
               $continuation.L$6 = null;
               $continuation.label = 3;
               if ($this$map_u24lambda_u245.emit(var57, $continuation) == var5) {
                  return var5;
               }

               return Unit.INSTANCE;
            }

            Object var18 = var17.next();
            entity = (IntakeEntity)var18;
            var20 = destination$iv$iv;
            boolean var37 = false;
            MedicationDao var40 = IntakeRepository.access$getDb$p(this.this$0).medicationDao();
            long var51 = entity.getMedicationId();
            $continuation.L$0 = this;
            $continuation.L$1 = $this$map_u24lambda_u245;
            $continuation.L$2 = destination$iv$iv;
            $continuation.L$3 = var17;
            $continuation.L$4 = entity;
            $continuation.L$5 = destination$iv$iv;
            $continuation.L$6 = null;
            $continuation.label = 1;
            Object var41 = var40.getMedicationById(var51, $continuation);
            if (var41 == var5) {
               return var5;
            }

            med = (MedicationEntity)var41;
            PatientDao var42 = IntakeRepository.access$getDb$p(this.this$0).patientDao();
            var51 = entity.getPatientId();
            $continuation.L$0 = this;
            $continuation.L$1 = $this$map_u24lambda_u245;
            $continuation.L$2 = destination$iv$iv;
            $continuation.L$3 = var17;
            $continuation.L$4 = entity;
            $continuation.L$5 = destination$iv$iv;
            $continuation.L$6 = med;
            $continuation.label = 2;
            var10000 = var42.getPatientById(var51, $continuation);
            if (var10000 == var5) {
               return var5;
            }
            break;
         case 1:
            int var27 = 0;
            int var29 = 0;
            int $i$f$map = 0;
            int $i$f$mapTo = 0;
            int var36 = 0;
            var20 = (Collection)$continuation.L$5;
            entity = (IntakeEntity)$continuation.L$4;
            var17 = (Iterator)$continuation.L$3;
            destination$iv$iv = (Collection)$continuation.L$2;
            var9 = (FlowCollector)$continuation.L$1;
            this = (IntakeRepository$getIntakesForDate$$inlined$map$1$2)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            med = (MedicationEntity)$result;
            PatientDao var39 = IntakeRepository.access$getDb$p(this.this$0).patientDao();
            long var10001 = entity.getPatientId();
            $continuation.L$0 = this;
            $continuation.L$1 = var9;
            $continuation.L$2 = destination$iv$iv;
            $continuation.L$3 = var17;
            $continuation.L$4 = entity;
            $continuation.L$5 = var20;
            $continuation.L$6 = med;
            $continuation.label = 2;
            var10000 = var39.getPatientById(var10001, $continuation);
            if (var10000 == var5) {
               return var5;
            }
            break;
         case 2:
            int var26 = 0;
            int var11 = 0;
            int $i$f$map = 0;
            int $i$f$mapTo = 0;
            int var21 = 0;
            med = (MedicationEntity)$continuation.L$6;
            var20 = (Collection)$continuation.L$5;
            entity = (IntakeEntity)$continuation.L$4;
            var17 = (Iterator)$continuation.L$3;
            destination$iv$iv = (Collection)$continuation.L$2;
            var9 = (FlowCollector)$continuation.L$1;
            this = (IntakeRepository$getIntakesForDate$$inlined$map$1$2)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            var10000 = $result;
            break;
         case 3:
            int var8 = 0;
            ResultKt.throwOnFailure($result);
            return Unit.INSTANCE;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      do {
         PatientEntity patient;
         label72: {
            patient = (PatientEntity)var10000;
            String var43 = LocalTime.now().toString();
            Intrinsics.checkNotNullExpressionValue(var43, "toString(...)");
            String nowTime = StringsKt.take(var43, 5);
            if (Intrinsics.areEqual(entity.getStatus(), "PENDING") && entity.getScheduledTime() != null) {
               var43 = entity.getScheduledDate();
               String var53 = LocalDate.now().toString();
               Intrinsics.checkNotNullExpressionValue(var53, "toString(...)");
               if (var43.compareTo(var53) < 0 || Intrinsics.areEqual(entity.getScheduledDate(), LocalDate.now().toString()) && entity.getScheduledTime().compareTo(nowTime) < 0) {
                  var45 = true;
                  break label72;
               }
            }

            var45 = false;
         }

         boolean isDelayed;
         String var10002;
         label62: {
            isDelayed = var45;
            var46 = this.this$0;
            if (med != null) {
               var10002 = med.getTranscribedName();
               if (var10002 != null) {
                  break label62;
               }
            }

            var10002 = "Medicamento";
         }

         String var10003;
         String var10004;
         label56: {
            var10003 = med != null ? med.getActiveIngredient() : null;
            if (patient != null) {
               var10004 = patient.getDisplayName();
               if (var10004 != null) {
                  break label56;
               }
            }

            var10004 = "";
         }

         var20.add(IntakeRepository.access$toDomain(var46, entity, var10002, var10003, var10004, isDelayed));
         if (!var17.hasNext()) {
            List var56 = (List)destination$iv$iv;
            $continuation.L$0 = null;
            $continuation.L$1 = null;
            $continuation.L$2 = null;
            $continuation.L$3 = null;
            $continuation.L$4 = null;
            $continuation.L$5 = null;
            $continuation.L$6 = null;
            $continuation.label = 3;
            if (var9.emit(var56, $continuation) == var5) {
               return var5;
            }

            return Unit.INSTANCE;
         }

         Object item$iv$iv = var17.next();
         entity = (IntakeEntity)item$iv$iv;
         var20 = destination$iv$iv;
         int var38 = 0;
         MedicationDao var47 = IntakeRepository.access$getDb$p(this.this$0).medicationDao();
         long var54 = entity.getMedicationId();
         $continuation.L$0 = this;
         $continuation.L$1 = var9;
         $continuation.L$2 = destination$iv$iv;
         $continuation.L$3 = var17;
         $continuation.L$4 = entity;
         $continuation.L$5 = destination$iv$iv;
         $continuation.L$6 = null;
         $continuation.label = 1;
         Object var48 = var47.getMedicationById(var54, $continuation);
         if (var48 == var5) {
            return var5;
         }

         med = (MedicationEntity)var48;
         PatientDao var49 = IntakeRepository.access$getDb$p(this.this$0).patientDao();
         var54 = entity.getPatientId();
         $continuation.L$0 = this;
         $continuation.L$1 = var9;
         $continuation.L$2 = destination$iv$iv;
         $continuation.L$3 = var17;
         $continuation.L$4 = entity;
         $continuation.L$5 = destination$iv$iv;
         $continuation.L$6 = med;
         $continuation.label = 2;
         var10000 = var49.getPatientById(var54, $continuation);
      } while(var10000 != var5);

      return var5;
   }
}
