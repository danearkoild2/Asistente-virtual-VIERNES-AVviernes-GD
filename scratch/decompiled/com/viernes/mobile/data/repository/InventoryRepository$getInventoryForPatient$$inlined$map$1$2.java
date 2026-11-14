package com.viernes.mobile.data.repository;

import com.viernes.mobile.data.local.dao.MedicationDao;
import com.viernes.mobile.data.local.entity.InventoryEntity;
import com.viernes.mobile.data.local.entity.MedicationEntity;
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
@SourceDebugExtension({"SMAP\nEmitters.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt$unsafeTransform$1$1\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/InventoryRepository\n+ 4 _Collections.kt\nkotlin/collections/CollectionsKt___CollectionsKt\n*L\n1#1,218:1\n50#2:219\n182#3:220\n183#3,2:224\n1549#4:221\n1620#4,2:222\n1622#4:226\n*S KotlinDebug\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/InventoryRepository\n*L\n182#1:221\n182#1:222,2\n182#1:226\n*E\n"})
public final class InventoryRepository$getInventoryForPatient$$inlined$map$1$2<T> implements FlowCollector {
   // $FF: synthetic field
   final FlowCollector $this_unsafeFlow;
   // $FF: synthetic field
   final InventoryRepository this$0;

   public InventoryRepository$getInventoryForPatient$$inlined$map$1$2(FlowCollector $receiver, InventoryRepository var2) {
      this.$this_unsafeFlow = $receiver;
      this.this$0 = var2;
   }

   @Nullable
   public final Object emit(Object value, @NotNull Continuation var2) {
      label64: {
         if (var2 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label64;
            }
         }

         $continuation = new InventoryRepository$getInventoryForPatient$$inlined$map$1$2$1(this, var2);
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
            int var24 = 0;
            var9 = $this$map_u24lambda_u245;
            Continuation var10001 = $continuation;
            List list = (List)value;
            int var25 = 0;
            Iterable $this$map$iv = (Iterable)list;
            int $i$f$map = 0;
            destination$iv$iv = (Collection)(new ArrayList(CollectionsKt.collectionSizeOrDefault($this$map$iv, 10)));
            int $i$f$mapTo = 0;
            var17 = $this$map$iv.iterator();
            break;
         case 1:
            InventoryEntity entity;
            Collection var20;
            InventoryRepository var10000;
            String var10002;
            label38: {
               int var23 = 0;
               int var11 = 0;
               int $i$f$map = 0;
               int $i$f$mapTo = 0;
               int var21 = 0;
               var20 = (Collection)$continuation.L$5;
               entity = (InventoryEntity)$continuation.L$4;
               var17 = (Iterator)$continuation.L$3;
               destination$iv$iv = (Collection)$continuation.L$2;
               var9 = (FlowCollector)$continuation.L$1;
               this = (InventoryRepository$getInventoryForPatient$$inlined$map$1$2)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               MedicationEntity var22 = (MedicationEntity)$result;
               var10000 = this.this$0;
               if (var22 != null) {
                  var10002 = var22.getTranscribedName();
                  if (var10002 != null) {
                     break label38;
                  }
               }

               var10002 = "Medicamento";
            }

            var20.add(InventoryRepository.access$toDomain(var10000, entity, var10002));
            break;
         case 2:
            int var8 = 0;
            ResultKt.throwOnFailure($result);
            return Unit.INSTANCE;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      InventoryEntity entity;
      InventoryRepository var33;
      String var36;
      for(; var17.hasNext(); destination$iv$iv.add(InventoryRepository.access$toDomain(var33, entity, var36))) {
         Object item$iv$iv = var17.next();
         entity = (InventoryEntity)item$iv$iv;
         int var29 = 0;
         MedicationDao var31 = InventoryRepository.access$getDb$p(this.this$0).medicationDao();
         long var34 = entity.getMedicationId();
         $continuation.L$0 = this;
         $continuation.L$1 = var9;
         $continuation.L$2 = destination$iv$iv;
         $continuation.L$3 = var17;
         $continuation.L$4 = entity;
         $continuation.L$5 = destination$iv$iv;
         $continuation.label = 1;
         Object var32 = var31.getMedicationById(var34, $continuation);
         if (var32 == var5) {
            return var5;
         }

         MedicationEntity med = (MedicationEntity)var32;
         var33 = this.this$0;
         if (med != null) {
            var36 = med.getTranscribedName();
            if (var36 != null) {
               continue;
            }
         }

         var36 = "Medicamento";
      }

      List var35 = (List)destination$iv$iv;
      $continuation.L$0 = null;
      $continuation.L$1 = null;
      $continuation.L$2 = null;
      $continuation.L$3 = null;
      $continuation.L$4 = null;
      $continuation.L$5 = null;
      $continuation.label = 2;
      if (var9.emit(var35, $continuation) == var5) {
         return var5;
      } else {
         return Unit.INSTANCE;
      }
   }
}
