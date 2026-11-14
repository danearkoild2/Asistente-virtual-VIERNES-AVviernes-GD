package com.viernes.mobile.data.repository;

import com.viernes.mobile.data.local.entity.RefillEntity;
import java.util.ArrayList;
import java.util.Collection;
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
@SourceDebugExtension({"SMAP\nEmitters.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt$unsafeTransform$1$1\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/RefillRepository\n+ 4 _Collections.kt\nkotlin/collections/CollectionsKt___CollectionsKt\n*L\n1#1,218:1\n50#2:219\n78#3:220\n1549#4:221\n1620#4,3:222\n*S KotlinDebug\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/RefillRepository\n*L\n78#1:221\n78#1:222,3\n*E\n"})
public final class RefillRepository$getRefillsForPatient$$inlined$map$1$2<T> implements FlowCollector {
   // $FF: synthetic field
   final FlowCollector $this_unsafeFlow;
   // $FF: synthetic field
   final RefillRepository this$0;

   public RefillRepository$getRefillsForPatient$$inlined$map$1$2(FlowCollector $receiver, RefillRepository var2) {
      this.$this_unsafeFlow = $receiver;
      this.this$0 = var2;
   }

   @Nullable
   public final Object emit(Object value, @NotNull Continuation var2) {
      label29: {
         if (var2 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label29;
            }
         }

         $continuation = new RefillRepository$getRefillsForPatient$$inlined$map$1$2$1(this, var2);
      }

      Object $result = $continuation.result;
      Object var5 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            FlowCollector $this$map_u24lambda_u245 = this.$this_unsafeFlow;
            int var22 = 0;
            Continuation var10001 = $continuation;
            List list = (List)value;
            int var11 = 0;
            Iterable $this$map$iv = (Iterable)list;
            int $i$f$map = 0;
            Collection destination$iv$iv = (Collection)(new ArrayList(CollectionsKt.collectionSizeOrDefault($this$map$iv, 10)));
            int $i$f$mapTo = 0;

            for(Object item$iv$iv : $this$map$iv) {
               RefillEntity it = (RefillEntity)item$iv$iv;
               int var21 = 0;
               destination$iv$iv.add(RefillRepository.access$toDomain(this.this$0, it));
            }

            List var23 = (List)destination$iv$iv;
            $continuation.label = 1;
            if ($this$map_u24lambda_u245.emit(var23, $continuation) == var5) {
               return var5;
            }
            break;
         case 1:
            int var8 = 0;
            ResultKt.throwOnFailure($result);
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      return Unit.INSTANCE;
   }
}
