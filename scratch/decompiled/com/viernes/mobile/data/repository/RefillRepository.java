package com.viernes.mobile.data.repository;

import androidx.compose.runtime.internal.StabilityInferred;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.local.dao.AuditDao;
import com.viernes.mobile.data.local.dao.InventoryDao;
import com.viernes.mobile.data.local.dao.RefillDao;
import com.viernes.mobile.data.local.entity.AuditRecordEntity;
import com.viernes.mobile.data.local.entity.InventoryEntity;
import com.viernes.mobile.data.local.entity.InventoryMovementEntity;
import com.viernes.mobile.data.local.entity.RefillEntity;
import com.viernes.mobile.domain.model.Refill;
import com.viernes.mobile.domain.model.RefillStatus;
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
   d1 = {"\u0000J\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\u0006\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0005\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004J\u001a\u0010\u0007\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\n0\t0\b2\u0006\u0010\u000b\u001a\u00020\fJ(\u0010\r\u001a\u00020\u000e2\u0006\u0010\u000f\u001a\u00020\f2\u0006\u0010\u0010\u001a\u00020\u00112\b\b\u0002\u0010\u0012\u001a\u00020\u0013H\u0086@¢\u0006\u0002\u0010\u0014J \u0010\u0015\u001a\u00020\f2\u0006\u0010\u0016\u001a\u00020\n2\b\b\u0002\u0010\u0012\u001a\u00020\u0013H\u0086@¢\u0006\u0002\u0010\u0017J\f\u0010\u0018\u001a\u00020\n*\u00020\u0019H\u0002J\f\u0010\u001a\u001a\u00020\u0019*\u00020\nH\u0002R\u000e\u0010\u0005\u001a\u00020\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\u001b"},
   d2 = {"Lcom/viernes/mobile/data/repository/RefillRepository;", "", "db", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "(Lcom/viernes/mobile/data/local/ViernesDatabase;)V", "dao", "Lcom/viernes/mobile/data/local/dao/RefillDao;", "getRefillsForPatient", "Lkotlinx/coroutines/flow/Flow;", "", "Lcom/viernes/mobile/domain/model/Refill;", "patientId", "", "recordPickup", "", "refillId", "quantityReceived", "", "userId", "", "(JDLjava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "saveRefill", "refill", "(Lcom/viernes/mobile/domain/model/Refill;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "toDomain", "Lcom/viernes/mobile/data/local/entity/RefillEntity;", "toEntity", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
@SourceDebugExtension({"SMAP\nAdditionalRepositories.kt\nKotlin\n*S Kotlin\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/RefillRepository\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt\n+ 4 SafeCollector.common.kt\nkotlinx/coroutines/flow/internal/SafeCollector_commonKt\n*L\n1#1,402:1\n49#2:403\n51#2:407\n46#3:404\n51#3:406\n105#4:405\n*S KotlinDebug\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/RefillRepository\n*L\n78#1:403\n78#1:407\n78#1:404\n78#1:406\n78#1:405\n*E\n"})
public final class RefillRepository {
   @NotNull
   private final ViernesDatabase db;
   @NotNull
   private final RefillDao dao;
   public static final int $stable = 8;

   public RefillRepository(@NotNull ViernesDatabase db) {
      Intrinsics.checkNotNullParameter(db, "db");
      super();
      this.db = db;
      this.dao = this.db.refillDao();
   }

   @NotNull
   public final Flow<List<Refill>> getRefillsForPatient(long patientId) {
      Flow $this$map$iv = this.dao.getRefillsForPatient(patientId);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new RefillRepository$getRefillsForPatient$$inlined$map$1($this$map$iv, this);
   }

   @Nullable
   public final Object saveRefill(@NotNull Refill refill, @NotNull String userId, @NotNull Continuation<? super Long> var3) {
      label32: {
         if (var3 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label32;
            }
         }

         $continuation = new ContinuationImpl(var3) {
            Object L$0;
            Object L$1;
            Object L$2;
            long J$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return RefillRepository.this.saveRefill((Refill)null, (String)null, (Continuation)this);
            }
         };
      }

      Object $result = $continuation.result;
      Object var9 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      long id;
      Object var10000;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            RefillEntity entity = this.toEntity(refill);
            RefillDao var10 = this.dao;
            $continuation.L$0 = this;
            $continuation.L$1 = refill;
            $continuation.L$2 = userId;
            $continuation.label = 1;
            var10000 = var10.insert(entity, $continuation);
            if (var10000 == var9) {
               return var9;
            }
            break;
         case 1:
            userId = (String)$continuation.L$2;
            refill = (Refill)$continuation.L$1;
            this = (RefillRepository)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            var10000 = $result;
            break;
         case 2:
            id = $continuation.J$0;
            ResultKt.throwOnFailure($result);
            return Boxing.boxLong(id);
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      id = ((Number)var10000).longValue();
      AuditDao var11 = this.db.auditDao();
      AuditRecordEntity var10001 = new AuditRecordEntity(0L, userId, Boxing.boxLong(refill.getPatientId()), "REFILL", Boxing.boxLong(id), refill.getId() == 0L ? "CREATE" : "UPDATE", "Retiro programado: " + refill.getMedicationName() + " (" + refill.getRequestedQuantity() + ")", (String)null, 129, (DefaultConstructorMarker)null);
      $continuation.L$0 = null;
      $continuation.L$1 = null;
      $continuation.L$2 = null;
      $continuation.J$0 = id;
      $continuation.label = 2;
      if (var11.insert(var10001, $continuation) == var9) {
         return var9;
      } else {
         return Boxing.boxLong(id);
      }
   }

   // $FF: synthetic method
   public static Object saveRefill$default(RefillRepository var0, Refill var1, String var2, Continuation var3, int var4, Object var5) {
      if ((var4 & 2) != 0) {
         var2 = "mobile_user";
      }

      return var0.saveRefill(var1, var2, var3);
   }

   @Nullable
   public final Object recordPickup(long refillId, double quantityReceived, @NotNull String userId, @NotNull Continuation<? super Boolean> var6) {
      label86: {
         if (var6 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label86;
            }
         }

         $continuation = new ContinuationImpl(var6) {
            Object L$0;
            Object L$1;
            Object L$2;
            Object L$3;
            double D$0;
            double D$1;
            long J$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return RefillRepository.this.recordPickup(0L, (double)0.0F, (String)null, (Continuation)this);
            }
         };
      }

      Object var10000;
      label102: {
         RefillEntity refill;
         String nowStr;
         long medId;
         double newQty;
         Object var23;
         label103: {
            label90: {
               label91: {
                  Object $result = $continuation.result;
                  var23 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                  switch ($continuation.label) {
                     case 0:
                        ResultKt.throwOnFailure($result);
                        RefillDao var30 = this.dao;
                        $continuation.L$0 = this;
                        $continuation.L$1 = userId;
                        $continuation.D$0 = quantityReceived;
                        $continuation.label = 1;
                        var10000 = var30.getRefillById(refillId, $continuation);
                        if (var10000 == var23) {
                           return var23;
                        }
                        break;
                     case 1:
                        quantityReceived = $continuation.D$0;
                        userId = (String)$continuation.L$1;
                        this = (RefillRepository)$continuation.L$0;
                        ResultKt.throwOnFailure($result);
                        var10000 = $result;
                        break;
                     case 2:
                        quantityReceived = $continuation.D$0;
                        nowStr = (String)$continuation.L$3;
                        refill = (RefillEntity)$continuation.L$2;
                        userId = (String)$continuation.L$1;
                        this = (RefillRepository)$continuation.L$0;
                        ResultKt.throwOnFailure($result);
                        break label91;
                     case 3:
                        int var25 = 0;
                        medId = $continuation.J$0;
                        quantityReceived = $continuation.D$0;
                        nowStr = (String)$continuation.L$3;
                        refill = (RefillEntity)$continuation.L$2;
                        userId = (String)$continuation.L$1;
                        this = (RefillRepository)$continuation.L$0;
                        ResultKt.throwOnFailure($result);
                        var10000 = $result;
                        break label90;
                     case 4:
                        int var24 = 0;
                        newQty = $continuation.D$1;
                        medId = $continuation.J$0;
                        quantityReceived = $continuation.D$0;
                        nowStr = (String)$continuation.L$3;
                        refill = (RefillEntity)$continuation.L$2;
                        userId = (String)$continuation.L$1;
                        this = (RefillRepository)$continuation.L$0;
                        ResultKt.throwOnFailure($result);
                        var10000 = $result;
                        break label103;
                     case 5:
                        int var13 = 0;
                        ResultKt.throwOnFailure($result);
                        var10000 = $result;
                        break label102;
                     default:
                        throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                  }

                  RefillEntity var31 = (RefillEntity)var10000;
                  if (var31 == null) {
                     return Boxing.boxBoolean(false);
                  }

                  refill = var31;
                  nowStr = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
                  RefillDao var32 = this.dao;
                  String var9 = RefillStatus.PICKED_UP.getValue();
                  String var10 = String.valueOf(quantityReceived);
                  RefillEntity var10001 = RefillEntity.copy$default(refill, 0L, 0L, (Long)null, (String)null, (String)null, (String)null, (String)null, (String)null, var10, (String)null, var9, (String)null, (String)null, (String)null, (String)null, nowStr, 31487, (Object)null);
                  $continuation.L$0 = this;
                  $continuation.L$1 = userId;
                  $continuation.L$2 = refill;
                  $continuation.L$3 = nowStr;
                  $continuation.D$0 = quantityReceived;
                  $continuation.label = 2;
                  if (var32.update(var10001, $continuation) == var23) {
                     return var23;
                  }
               }

               Long var33 = refill.getMedicationId();
               if (var33 == null) {
                  return Boxing.boxBoolean(true);
               }

               medId = ((Number)var33).longValue();
               int var26 = 0;
               InventoryDao var34 = this.db.inventoryDao();
               long var37 = refill.getPatientId();
               $continuation.L$0 = this;
               $continuation.L$1 = userId;
               $continuation.L$2 = refill;
               $continuation.L$3 = nowStr;
               $continuation.D$0 = quantityReceived;
               $continuation.J$0 = medId;
               $continuation.label = 3;
               var10000 = var34.getInventoryItem(var37, medId, $continuation);
               if (var10000 == var23) {
                  return var23;
               }
            }

            InventoryEntity inv = (InventoryEntity)var10000;
            double currentQty = inv != null ? inv.getAvailableQuantity() : (double)0.0F;
            newQty = currentQty + quantityReceived;
            InventoryDao var35 = this.db.inventoryDao();
            InventoryEntity var38 = new InventoryEntity;
            long var10003 = inv != null ? inv.getId() : 0L;
            long var10004 = refill.getPatientId();
            String var10007 = refill.getMeasurementUnit();
            if (var10007 == null) {
               var10007 = "unidades";
            }

            var38.<init>(var10003, var10004, medId, (String)null, var10007, newQty, (String)null, (String)null, (String)null, nowStr, 456, (DefaultConstructorMarker)null);
            $continuation.L$0 = this;
            $continuation.L$1 = userId;
            $continuation.L$2 = refill;
            $continuation.L$3 = nowStr;
            $continuation.D$0 = quantityReceived;
            $continuation.J$0 = medId;
            $continuation.D$1 = newQty;
            $continuation.label = 4;
            var10000 = var35.insertOrUpdate(var38, $continuation);
            if (var10000 == var23) {
               return var23;
            }
         }

         long invId = ((Number)var10000).longValue();
         InventoryDao var36 = this.db.inventoryDao();
         InventoryMovementEntity var39 = new InventoryMovementEntity(0L, invId, refill.getPatientId(), medId, "REFILL_ENTRY", quantityReceived, newQty, "Ingreso por retiro farmacéutico #" + refill.getId() + " (" + refill.getPharmacyCenter() + ")", userId, nowStr, 1, (DefaultConstructorMarker)null);
         $continuation.L$0 = null;
         $continuation.L$1 = null;
         $continuation.L$2 = null;
         $continuation.L$3 = null;
         $continuation.label = 5;
         var10000 = var36.insertMovement(var39, $continuation);
         if (var10000 == var23) {
            return var23;
         }
      }

      Boxing.boxLong(((Number)var10000).longValue());
      return Boxing.boxBoolean(true);
   }

   // $FF: synthetic method
   public static Object recordPickup$default(RefillRepository var0, long var1, double var3, String var5, Continuation var6, int var7, Object var8) {
      if ((var7 & 4) != 0) {
         var5 = "mobile_user";
      }

      return var0.recordPickup(var1, var3, var5, var6);
   }

   private final Refill toDomain(RefillEntity $this$toDomain) {
      return new Refill($this$toDomain.getId(), $this$toDomain.getPatientId(), $this$toDomain.getMedicationId(), $this$toDomain.getMedicationName(), $this$toDomain.getPharmacyCenter(), $this$toDomain.getScheduledDate(), $this$toDomain.getDeadlineDate(), $this$toDomain.getRequestedQuantity(), $this$toDomain.getWithdrawnQuantity(), $this$toDomain.getMeasurementUnit(), RefillStatus.Companion.from($this$toDomain.getStatus()), $this$toDomain.getRecipeReference(), $this$toDomain.getResponsiblePerson(), $this$toDomain.getNotes(), $this$toDomain.getCreatedAt(), $this$toDomain.getUpdatedAt());
   }

   private final RefillEntity toEntity(Refill $this$toEntity) {
      RefillEntity var10000 = new RefillEntity;
      long var10002 = $this$toEntity.getId();
      long var10003 = $this$toEntity.getPatientId();
      Long var10004 = $this$toEntity.getMedicationId();
      String var10005 = $this$toEntity.getMedicationName();
      String var10006 = $this$toEntity.getPharmacyCenter();
      String var10007 = $this$toEntity.getScheduledDate();
      String var10008 = $this$toEntity.getDeadlineDate();
      String var10009 = $this$toEntity.getRequestedQuantity();
      String var10010 = $this$toEntity.getWithdrawnQuantity();
      String var10011 = $this$toEntity.getMeasurementUnit();
      String var10012 = $this$toEntity.getStatus().getValue();
      String var10013 = $this$toEntity.getRecipeReference();
      String var10014 = $this$toEntity.getResponsiblePerson();
      String var10015 = $this$toEntity.getNotes();
      String var10016 = $this$toEntity.getCreatedAt();
      if (var10016 == null) {
         var10016 = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
      }

      var10000.<init>(var10002, var10003, var10004, var10005, var10006, var10007, var10008, var10009, var10010, var10011, var10012, var10013, var10014, var10015, var10016, LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
      return var10000;
   }

   // $FF: synthetic method
   public static final Refill access$toDomain(RefillRepository $this, RefillEntity $receiver) {
      return $this.toDomain($receiver);
   }
}
