package com.viernes.mobile.data.repository;

import com.viernes.mobile.data.local.dao.MedicationDao;
import com.viernes.mobile.data.local.dao.PatientDao;
import com.viernes.mobile.data.local.entity.IntakeEntity;
import com.viernes.mobile.data.local.entity.MedicationEntity;
import com.viernes.mobile.data.local.entity.PatientEntity;
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
import kotlin.jvm.internal.SourceDebugExtension;
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
@SourceDebugExtension({"SMAP\nEmitters.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt$unsafeTransform$1$1\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Repositories.kt\ncom/viernes/mobile/data/repository/IntakeRepository\n+ 4 _Collections.kt\nkotlin/collections/CollectionsKt___CollectionsKt\n*L\n1#1,218:1\n50#2:219\n240#3:220\n241#3,7:224\n1549#4:221\n1620#4,2:222\n1622#4:231\n*S KotlinDebug\n*F\n+ 1 Repositories.kt\ncom/viernes/mobile/data/repository/IntakeRepository\n*L\n240#1:221\n240#1:222,2\n240#1:231\n*E\n"})
public final class IntakeRepository$getUpcomingPendingIntakes$$inlined$map$1$2<T> implements FlowCollector {
   // $FF: synthetic field
   final FlowCollector $this_unsafeFlow;
   // $FF: synthetic field
   final IntakeRepository this$0;

   public IntakeRepository$getUpcomingPendingIntakes$$inlined$map$1$2(FlowCollector $receiver, IntakeRepository var2) {
      this.$this_unsafeFlow = $receiver;
      this.this$0 = var2;
   }

   @Nullable
   public final Object emit(Object value, @NotNull Continuation var2) {
      label137: {
         if (var2 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label137;
            }
         }

         $continuation = new IntakeRepository$getUpcomingPendingIntakes$$inlined$map$1$2$1(this, var2);
      }

      Object $result = $continuation.result;
      Object var5 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      FlowCollector var9;
      Collection destination$iv$iv;
      Iterator var17;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            FlowCollector $this$map_u24lambda_u245 = this.$this_unsafeFlow;
            int var26 = 0;
            var9 = $this$map_u24lambda_u245;
            Continuation var50 = $continuation;
            List list = (List)value;
            int var28 = 0;
            Iterable $this$map$iv = (Iterable)list;
            int $i$f$map = 0;
            destination$iv$iv = (Collection)(new ArrayList(CollectionsKt.collectionSizeOrDefault($this$map$iv, 10)));
            int $i$f$mapTo = 0;
            var17 = $this$map$iv.iterator();
            break;
         case 1:
            int var25 = 0;
            int var27 = 0;
            int $i$f$map = 0;
            int $i$f$mapTo = 0;
            int var36 = 0;
            Collection var35 = (Collection)$continuation.L$5;
            IntakeEntity entity = (IntakeEntity)$continuation.L$4;
            var17 = (Iterator)$continuation.L$3;
            destination$iv$iv = (Collection)$continuation.L$2;
            var9 = (FlowCollector)$continuation.L$1;
            this = (IntakeRepository$getUpcomingPendingIntakes$$inlined$map$1$2)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            MedicationEntity var38 = (MedicationEntity)$result;
            PatientDao var42 = IntakeRepository.access$getDb$p(this.this$0).patientDao();
            long var10001 = entity.getPatientId();
            $continuation.L$0 = this;
            $continuation.L$1 = var9;
            $continuation.L$2 = destination$iv$iv;
            $continuation.L$3 = var17;
            $continuation.L$4 = entity;
            $continuation.L$5 = var35;
            $continuation.L$6 = var38;
            $continuation.label = 2;
            Object var43 = var42.getPatientById(var10001, $continuation);
            if (var43 == var5) {
               return var5;
            }

            PatientEntity var40;
            String var54;
            label93: {
               var40 = (PatientEntity)var43;
               var44 = this.this$0;
               if (var38 != null) {
                  var54 = var38.getTranscribedName();
                  if (var54 != null) {
                     break label93;
                  }
               }

               var54 = "Medicamento";
            }

            String var56;
            String var58;
            label111: {
               var56 = var38 != null ? var38.getActiveIngredient() : null;
               if (var40 != null) {
                  var58 = var40.getDisplayName();
                  if (var58 != null) {
                     break label111;
                  }
               }

               var58 = "";
            }

            var35.add(IntakeRepository.access$toDomain(var44, entity, var54, var56, var58, false));
            break;
         case 2:
            IntakeEntity entity;
            Collection var20;
            MedicationEntity med;
            PatientEntity var23;
            IntakeRepository var10000;
            String var10002;
            label55: {
               int var24 = 0;
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
               this = (IntakeRepository$getUpcomingPendingIntakes$$inlined$map$1$2)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               var23 = (PatientEntity)$result;
               var10000 = this.this$0;
               if (med != null) {
                  var10002 = med.getTranscribedName();
                  if (var10002 != null) {
                     break label55;
                  }
               }

               var10002 = "Medicamento";
            }

            String var10003;
            String var10004;
            label73: {
               var10003 = med != null ? med.getActiveIngredient() : null;
               if (var23 != null) {
                  var10004 = var23.getDisplayName();
                  if (var10004 != null) {
                     break label73;
                  }
               }

               var10004 = "";
            }

            var20.add(IntakeRepository.access$toDomain(var10000, entity, var10002, var10003, var10004, false));
            break;
         case 3:
            int var8 = 0;
            ResultKt.throwOnFailure($result);
            return Unit.INSTANCE;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      IntakeEntity entity;
      IntakeRepository var49;
      String var55;
      String var57;
      String var59;
      for(; var17.hasNext(); destination$iv$iv.add(IntakeRepository.access$toDomain(var49, entity, var55, var57, var59, false))) {
         Object item$iv$iv = var17.next();
         entity = (IntakeEntity)item$iv$iv;
         int var37 = 0;
         MedicationDao var45 = IntakeRepository.access$getDb$p(this.this$0).medicationDao();
         long var51 = entity.getMedicationId();
         $continuation.L$0 = this;
         $continuation.L$1 = var9;
         $continuation.L$2 = destination$iv$iv;
         $continuation.L$3 = var17;
         $continuation.L$4 = entity;
         $continuation.L$5 = destination$iv$iv;
         $continuation.L$6 = null;
         $continuation.label = 1;
         Object var46 = var45.getMedicationById(var51, $continuation);
         if (var46 == var5) {
            return var5;
         }

         MedicationEntity med = (MedicationEntity)var46;
         PatientDao var47 = IntakeRepository.access$getDb$p(this.this$0).patientDao();
         var51 = entity.getPatientId();
         $continuation.L$0 = this;
         $continuation.L$1 = var9;
         $continuation.L$2 = destination$iv$iv;
         $continuation.L$3 = var17;
         $continuation.L$4 = entity;
         $continuation.L$5 = destination$iv$iv;
         $continuation.L$6 = med;
         $continuation.label = 2;
         Object var48 = var47.getPatientById(var51, $continuation);
         if (var48 == var5) {
            return var5;
         }

         PatientEntity patient;
         label50: {
            patient = (PatientEntity)var48;
            var49 = this.this$0;
            if (med != null) {
               var55 = med.getTranscribedName();
               if (var55 != null) {
                  break label50;
               }
            }

            var55 = "Medicamento";
         }

         var57 = med != null ? med.getActiveIngredient() : null;
         if (patient != null) {
            var59 = patient.getDisplayName();
            if (var59 != null) {
               continue;
            }
         }

         var59 = "";
      }

      List var53 = (List)destination$iv$iv;
      $continuation.L$0 = null;
      $continuation.L$1 = null;
      $continuation.L$2 = null;
      $continuation.L$3 = null;
      $continuation.L$4 = null;
      $continuation.L$5 = null;
      $continuation.L$6 = null;
      $continuation.label = 3;
      if (var9.emit(var53, $continuation) == var5) {
         return var5;
      } else {
         return Unit.INSTANCE;
      }
   }
}
