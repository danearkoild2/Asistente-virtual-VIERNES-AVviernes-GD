package com.viernes.mobile.data.repository;

import androidx.compose.runtime.internal.StabilityInferred;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.local.dao.AuditDao;
import com.viernes.mobile.data.local.dao.InventoryDao;
import com.viernes.mobile.data.local.entity.AuditRecordEntity;
import com.viernes.mobile.data.local.entity.InventoryEntity;
import com.viernes.mobile.data.local.entity.InventoryMovementEntity;
import com.viernes.mobile.domain.model.Inventory;
import com.viernes.mobile.domain.model.InventoryMovement;
import com.viernes.mobile.domain.model.MovementType;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.Boxing;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlinx.coroutines.flow.Flow;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000N\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0006\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004J\u001a\u0010\u0007\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\n0\t0\b2\u0006\u0010\u000b\u001a\u00020\fJ\u001a\u0010\r\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u000e0\t0\b2\u0006\u0010\u000b\u001a\u00020\fJ6\u0010\u000f\u001a\u00020\u00102\u0006\u0010\u000b\u001a\u00020\f2\u0006\u0010\u0011\u001a\u00020\f2\u0006\u0010\u0012\u001a\u00020\u00102\u0006\u0010\u0013\u001a\u00020\u00142\u0006\u0010\u0015\u001a\u00020\u0014H\u0086@¢\u0006\u0002\u0010\u0016J\u0014\u0010\u0017\u001a\u00020\n*\u00020\u00182\u0006\u0010\u0019\u001a\u00020\u0014H\u0002J\f\u0010\u0017\u001a\u00020\u000e*\u00020\u001aH\u0002R\u000e\u0010\u0005\u001a\u00020\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\u001b"},
   d2 = {"Lcom/viernes/mobile/data/repository/InventoryRepository;", "", "db", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "(Lcom/viernes/mobile/data/local/ViernesDatabase;)V", "dao", "Lcom/viernes/mobile/data/local/dao/InventoryDao;", "getInventoryForPatient", "Lkotlinx/coroutines/flow/Flow;", "", "Lcom/viernes/mobile/domain/model/Inventory;", "patientId", "", "getMovementsForPatient", "Lcom/viernes/mobile/domain/model/InventoryMovement;", "manualReconciliation", "", "medicationId", "physicalCount", "reason", "", "userId", "(JJDLjava/lang/String;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "toDomain", "Lcom/viernes/mobile/data/local/entity/InventoryEntity;", "medName", "Lcom/viernes/mobile/data/local/entity/InventoryMovementEntity;", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
@SourceDebugExtension({"SMAP\nAdditionalRepositories.kt\nKotlin\n*S Kotlin\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/InventoryRepository\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt\n+ 4 SafeCollector.common.kt\nkotlinx/coroutines/flow/internal/SafeCollector_commonKt\n*L\n1#1,402:1\n49#2:403\n51#2:407\n49#2:408\n51#2:412\n46#3:404\n51#3:406\n46#3:409\n51#3:411\n105#4:405\n105#4:410\n*S KotlinDebug\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/InventoryRepository\n*L\n181#1:403\n181#1:407\n189#1:408\n189#1:412\n181#1:404\n181#1:406\n189#1:409\n189#1:411\n181#1:405\n189#1:410\n*E\n"})
public final class InventoryRepository {
   @NotNull
   private final ViernesDatabase db;
   @NotNull
   private final InventoryDao dao;
   public static final int $stable = 8;

   public InventoryRepository(@NotNull ViernesDatabase db) {
      Intrinsics.checkNotNullParameter(db, "db");
      super();
      this.db = db;
      this.dao = this.db.inventoryDao();
   }

   @NotNull
   public final Flow<List<Inventory>> getInventoryForPatient(long patientId) {
      Flow $this$map$iv = this.dao.getInventoryForPatient(patientId);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new InventoryRepository$getInventoryForPatient$$inlined$map$1($this$map$iv, this);
   }

   @NotNull
   public final Flow<List<InventoryMovement>> getMovementsForPatient(long patientId) {
      Flow $this$map$iv = this.dao.getMovementsForPatient(patientId);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new InventoryRepository$getMovementsForPatient$$inlined$map$1($this$map$iv, this);
   }

   @Nullable
   public final Object manualReconciliation(long patientId, long medicationId, double physicalCount, @NotNull String reason, @NotNull String userId, @NotNull Continuation<? super Double> var9) {
      label79: {
         if (var9 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label79;
            }
         }

         $continuation = new ContinuationImpl(var9) {
            Object L$0;
            Object L$1;
            Object L$2;
            Object L$3;
            long J$0;
            long J$1;
            double D$0;
            double D$1;
            double D$2;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return InventoryRepository.this.manualReconciliation(0L, 0L, (double)0.0F, (String)null, (String)null, (Continuation)this);
            }
         };
      }

      double currentQty;
      long invId;
      Object var20;
      label82: {
         double delta;
         String nowStr;
         Object var10000;
         label83: {
            Object $result = $continuation.result;
            var20 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
            switch ($continuation.label) {
               case 0:
                  ResultKt.throwOnFailure($result);
                  InventoryDao var22 = this.dao;
                  $continuation.L$0 = this;
                  $continuation.L$1 = reason;
                  $continuation.L$2 = userId;
                  $continuation.J$0 = patientId;
                  $continuation.J$1 = medicationId;
                  $continuation.D$0 = physicalCount;
                  $continuation.label = 1;
                  var10000 = var22.getInventoryItem(patientId, medicationId, $continuation);
                  if (var10000 == var20) {
                     return var20;
                  }
                  break;
               case 1:
                  physicalCount = $continuation.D$0;
                  medicationId = $continuation.J$1;
                  patientId = $continuation.J$0;
                  userId = (String)$continuation.L$2;
                  reason = (String)$continuation.L$1;
                  this = (InventoryRepository)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break;
               case 2:
                  delta = $continuation.D$2;
                  currentQty = $continuation.D$1;
                  physicalCount = $continuation.D$0;
                  medicationId = $continuation.J$1;
                  patientId = $continuation.J$0;
                  nowStr = (String)$continuation.L$3;
                  userId = (String)$continuation.L$2;
                  reason = (String)$continuation.L$1;
                  this = (InventoryRepository)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break label83;
               case 3:
                  invId = $continuation.J$1;
                  currentQty = $continuation.D$1;
                  physicalCount = $continuation.D$0;
                  patientId = $continuation.J$0;
                  userId = (String)$continuation.L$2;
                  reason = (String)$continuation.L$1;
                  this = (InventoryRepository)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  break label82;
               case 4:
                  physicalCount = $continuation.D$0;
                  ResultKt.throwOnFailure($result);
                  return Boxing.boxDouble(physicalCount);
               default:
                  throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
            }

            InventoryEntity var10001;
            long var10003;
            String var10006;
            String var10007;
            label57: {
               InventoryEntity currentInv = (InventoryEntity)var10000;
               currentQty = currentInv != null ? currentInv.getAvailableQuantity() : (double)0.0F;
               delta = physicalCount - currentQty;
               nowStr = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
               var23 = this.dao;
               var10001 = new InventoryEntity;
               var10003 = currentInv != null ? currentInv.getId() : 0L;
               var10006 = currentInv != null ? currentInv.getPresentation() : null;
               if (currentInv != null) {
                  var10007 = currentInv.getInventoryUnit();
                  if (var10007 != null) {
                     break label57;
                  }
               }

               var10007 = "unidades";
            }

            var10001.<init>(var10003, patientId, medicationId, var10006, var10007, physicalCount, nowStr, userId, (String)null, nowStr, 256, (DefaultConstructorMarker)null);
            $continuation.L$0 = this;
            $continuation.L$1 = reason;
            $continuation.L$2 = userId;
            $continuation.L$3 = nowStr;
            $continuation.J$0 = patientId;
            $continuation.J$1 = medicationId;
            $continuation.D$0 = physicalCount;
            $continuation.D$1 = currentQty;
            $continuation.D$2 = delta;
            $continuation.label = 2;
            var10000 = var23.insertOrUpdate(var10001, $continuation);
            if (var10000 == var20) {
               return var20;
            }
         }

         invId = ((Number)var10000).longValue();
         InventoryDao var24 = this.dao;
         InventoryMovementEntity var26 = new InventoryMovementEntity(0L, invId, patientId, medicationId, "MANUAL_ADJUSTMENT", delta, physicalCount, "Conciliación física: " + reason + " (Ajuste: " + (delta >= (double)0.0F ? "+" + delta : String.valueOf(delta)) + ")", userId, nowStr, 1, (DefaultConstructorMarker)null);
         $continuation.L$0 = this;
         $continuation.L$1 = reason;
         $continuation.L$2 = userId;
         $continuation.L$3 = null;
         $continuation.J$0 = patientId;
         $continuation.D$0 = physicalCount;
         $continuation.D$1 = currentQty;
         $continuation.J$1 = invId;
         $continuation.label = 3;
         if (var24.insertMovement(var26, $continuation) == var20) {
            return var20;
         }
      }

      AuditDao var25 = this.db.auditDao();
      AuditRecordEntity var27 = new AuditRecordEntity(0L, userId, Boxing.boxLong(patientId), "INVENTORY", Boxing.boxLong(invId), "RECONCILIATION", "Ajuste manual de existencias de " + currentQty + " a " + physicalCount + ". Razón: " + reason, (String)null, 129, (DefaultConstructorMarker)null);
      $continuation.L$0 = null;
      $continuation.L$1 = null;
      $continuation.L$2 = null;
      $continuation.D$0 = physicalCount;
      $continuation.label = 4;
      if (var25.insert(var27, $continuation) == var20) {
         return var20;
      } else {
         return Boxing.boxDouble(physicalCount);
      }
   }

   private final Inventory toDomain(InventoryEntity $this$toDomain, String medName) {
      return new Inventory($this$toDomain.getId(), $this$toDomain.getPatientId(), $this$toDomain.getMedicationId(), $this$toDomain.getPresentation(), $this$toDomain.getInventoryUnit(), $this$toDomain.getAvailableQuantity(), $this$toDomain.getLastReconciliationDate(), $this$toDomain.getReconciledBy(), $this$toDomain.getNotes(), $this$toDomain.getUpdatedAt(), medName);
   }

   private final InventoryMovement toDomain(InventoryMovementEntity $this$toDomain) {
      return new InventoryMovement($this$toDomain.getId(), $this$toDomain.getInventoryId(), $this$toDomain.getPatientId(), $this$toDomain.getMedicationId(), MovementType.Companion.from($this$toDomain.getMovementType()), $this$toDomain.getQuantity(), $this$toDomain.getBalanceAfter(), $this$toDomain.getReason(), $this$toDomain.getUserResponsible(), $this$toDomain.getMovementDate());
   }

   // $FF: synthetic method
   public static final ViernesDatabase access$getDb$p(InventoryRepository $this) {
      return $this.db;
   }

   // $FF: synthetic method
   public static final Inventory access$toDomain(InventoryRepository $this, InventoryEntity $receiver, String medName) {
      return $this.toDomain($receiver, medName);
   }

   // $FF: synthetic method
   public static final InventoryMovement access$toDomain(InventoryRepository $this, InventoryMovementEntity $receiver) {
      return $this.toDomain($receiver);
   }
}
