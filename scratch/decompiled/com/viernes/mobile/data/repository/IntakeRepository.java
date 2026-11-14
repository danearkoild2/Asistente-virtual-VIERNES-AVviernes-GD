package com.viernes.mobile.data.repository;

import androidx.compose.runtime.internal.StabilityInferred;
import com.google.gson.Gson;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.local.dao.AuditDao;
import com.viernes.mobile.data.local.dao.IntakeDao;
import com.viernes.mobile.data.local.dao.InventoryDao;
import com.viernes.mobile.data.local.dao.MedicationDao;
import com.viernes.mobile.data.local.dao.PatientDao;
import com.viernes.mobile.data.local.dao.SyncQueueDao;
import com.viernes.mobile.data.local.entity.AuditRecordEntity;
import com.viernes.mobile.data.local.entity.IntakeEntity;
import com.viernes.mobile.data.local.entity.InventoryEntity;
import com.viernes.mobile.data.local.entity.InventoryMovementEntity;
import com.viernes.mobile.data.local.entity.MedicationEntity;
import com.viernes.mobile.data.local.entity.PatientEntity;
import com.viernes.mobile.data.local.entity.SyncQueueEntity;
import com.viernes.mobile.domain.model.Intake;
import com.viernes.mobile.domain.model.IntakeStatus;
import com.viernes.mobile.domain.model.Medication;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
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
import kotlin.coroutines.jvm.internal.Boxing;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.ranges.RangesKt;
import kotlin.text.StringsKt;
import kotlinx.coroutines.flow.Flow;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000f\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000b\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0003\n\u0002\u0010 \n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\b\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0010\u0002\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0002\b\u0005\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004J2\u0010\u0007\u001a\u00020\b2\u0006\u0010\t\u001a\u00020\n2\u0006\u0010\u000b\u001a\u00020\f2\u0006\u0010\r\u001a\u00020\u000e2\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u000eH\u0086@¢\u0006\u0002\u0010\u0010J&\u0010\u0011\u001a\b\u0012\u0004\u0012\u00020\n0\u00122\u0006\u0010\u0013\u001a\u00020\u00142\b\b\u0002\u0010\u0015\u001a\u00020\u0016H\u0086@¢\u0006\u0002\u0010\u0017J\u0018\u0010\u0018\u001a\u0004\u0018\u00010\u00192\u0006\u0010\u001a\u001a\u00020\nH\u0086@¢\u0006\u0002\u0010\u001bJ\"\u0010\u001c\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00190\u00120\u001d2\u0006\u0010\u001e\u001a\u00020\n2\u0006\u0010\u001f\u001a\u00020\u000eJ\u001a\u0010 \u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00190\u00120\u001d2\u0006\u0010!\u001a\u00020\u000eJ&\u0010\"\u001a\u00020#2\u0006\u0010\t\u001a\u00020\n2\u0006\u0010$\u001a\u00020\u000e2\u0006\u0010%\u001a\u00020\u000eH\u0086@¢\u0006\u0002\u0010&J.\u0010'\u001a\u00020\u0019*\u00020(2\u0006\u0010)\u001a\u00020\u000e2\b\u0010*\u001a\u0004\u0018\u00010\u000e2\u0006\u0010+\u001a\u00020\u000e2\u0006\u0010,\u001a\u00020\bH\u0002R\u000e\u0010\u0005\u001a\u00020\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006-"},
   d2 = {"Lcom/viernes/mobile/data/repository/IntakeRepository;", "", "db", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "(Lcom/viernes/mobile/data/local/ViernesDatabase;)V", "dao", "Lcom/viernes/mobile/data/local/dao/IntakeDao;", "confirmIntake", "", "intakeId", "", "status", "Lcom/viernes/mobile/domain/model/IntakeStatus;", "takenBy", "", "notes", "(JLcom/viernes/mobile/domain/model/IntakeStatus;Ljava/lang/String;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "generateIntakesForMedication", "", "medication", "Lcom/viernes/mobile/domain/model/Medication;", "daysAhead", "", "(Lcom/viernes/mobile/domain/model/Medication;ILkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getIntakeById", "Lcom/viernes/mobile/domain/model/Intake;", "id", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getIntakesForDate", "Lkotlinx/coroutines/flow/Flow;", "patientId", "date", "getUpcomingPendingIntakes", "today", "skipIntake", "", "reason", "skippedBy", "(JLjava/lang/String;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "toDomain", "Lcom/viernes/mobile/data/local/entity/IntakeEntity;", "medName", "activeIng", "patientName", "delayed", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
@SourceDebugExtension({"SMAP\nRepositories.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Repositories.kt\ncom/viernes/mobile/data/repository/IntakeRepository\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt\n+ 4 SafeCollector.common.kt\nkotlinx/coroutines/flow/internal/SafeCollector_commonKt\n+ 5 _Collections.kt\nkotlin/collections/CollectionsKt___CollectionsKt\n*L\n1#1,402:1\n49#2:403\n51#2:407\n49#2:408\n51#2:412\n46#3:404\n51#3:406\n46#3:409\n51#3:411\n105#4:405\n105#4:410\n1549#5:413\n1620#5,3:414\n766#5:417\n857#5,2:418\n*S KotlinDebug\n*F\n+ 1 Repositories.kt\ncom/viernes/mobile/data/repository/IntakeRepository\n*L\n220#1:403\n220#1:407\n239#1:408\n239#1:412\n220#1:404\n220#1:406\n239#1:409\n239#1:411\n220#1:405\n239#1:410\n354#1:413\n354#1:414,3\n354#1:417\n354#1:418,2\n*E\n"})
public final class IntakeRepository {
   @NotNull
   private final ViernesDatabase db;
   @NotNull
   private final IntakeDao dao;
   public static final int $stable = 8;

   public IntakeRepository(@NotNull ViernesDatabase db) {
      Intrinsics.checkNotNullParameter(db, "db");
      super();
      this.db = db;
      this.dao = this.db.intakeDao();
   }

   @NotNull
   public final Flow<List<Intake>> getIntakesForDate(long patientId, @NotNull String date) {
      Intrinsics.checkNotNullParameter(date, "date");
      Flow $this$map$iv = this.dao.getIntakesForDate(patientId, date);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new IntakeRepository$getIntakesForDate$$inlined$map$1($this$map$iv, this);
   }

   @NotNull
   public final Flow<List<Intake>> getUpcomingPendingIntakes(@NotNull String today) {
      Intrinsics.checkNotNullParameter(today, "today");
      Flow $this$map$iv = this.dao.getUpcomingPendingIntakes(today);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new IntakeRepository$getUpcomingPendingIntakes$$inlined$map$1($this$map$iv, this);
   }

   @Nullable
   public final Object getIntakeById(long id, @NotNull Continuation<? super Intake> var3) {
      label66: {
         if (var3 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label66;
            }
         }

         $continuation = new ContinuationImpl(var3) {
            Object L$0;
            Object L$1;
            Object L$2;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return IntakeRepository.this.getIntakeById(0L, (Continuation)this);
            }
         };
      }

      IntakeEntity entity;
      MedicationEntity med;
      Object var10000;
      label59: {
         Object var9;
         label70: {
            Object $result = $continuation.result;
            var9 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
            switch ($continuation.label) {
               case 0:
                  ResultKt.throwOnFailure($result);
                  IntakeDao var12 = this.dao;
                  $continuation.L$0 = this;
                  $continuation.label = 1;
                  var10000 = var12.getIntakeById(id, $continuation);
                  if (var10000 == var9) {
                     return var9;
                  }
                  break;
               case 1:
                  this = (IntakeRepository)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break;
               case 2:
                  entity = (IntakeEntity)$continuation.L$1;
                  this = (IntakeRepository)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break label70;
               case 3:
                  med = (MedicationEntity)$continuation.L$2;
                  entity = (IntakeEntity)$continuation.L$1;
                  this = (IntakeRepository)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break label59;
               default:
                  throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
            }

            IntakeEntity var13 = (IntakeEntity)var10000;
            if (var13 == null) {
               return null;
            }

            entity = var13;
            MedicationDao var14 = this.db.medicationDao();
            long var10001 = entity.getMedicationId();
            $continuation.L$0 = this;
            $continuation.L$1 = entity;
            $continuation.label = 2;
            var10000 = var14.getMedicationById(var10001, $continuation);
            if (var10000 == var9) {
               return var9;
            }
         }

         med = (MedicationEntity)var10000;
         PatientDao var15 = this.db.patientDao();
         long var16 = entity.getPatientId();
         $continuation.L$0 = this;
         $continuation.L$1 = entity;
         $continuation.L$2 = med;
         $continuation.label = 3;
         var10000 = var15.getPatientById(var16, $continuation);
         if (var10000 == var9) {
            return var9;
         }
      }

      PatientEntity patient;
      String var10002;
      label46: {
         patient = (PatientEntity)var10000;
         if (med != null) {
            var10002 = med.getTranscribedName();
            if (var10002 != null) {
               break label46;
            }
         }

         var10002 = "Medicamento";
      }

      String var10003 = med != null ? med.getActiveIngredient() : null;
      String var10004;
      if (patient != null) {
         var10004 = patient.getDisplayName();
         if (var10004 != null) {
            return this.toDomain(entity, var10002, var10003, var10004, false);
         }
      }

      var10004 = "";
      return this.toDomain(entity, var10002, var10003, var10004, false);
   }

   @Nullable
   public final Object confirmIntake(long intakeId, @NotNull IntakeStatus status, @NotNull String takenBy, @Nullable String notes, @NotNull Continuation<? super Boolean> var6) {
      label103: {
         if (var6 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label103;
            }
         }

         $continuation = new ContinuationImpl(var6) {
            Object L$0;
            Object L$1;
            Object L$2;
            Object L$3;
            Object L$4;
            long J$0;
            double D$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return IntakeRepository.this.confirmIntake(0L, (IntakeStatus)null, (String)null, (String)null, (Continuation)this);
            }
         };
      }

      String nowStr;
      IntakeEntity intake;
      Object var14;
      label119: {
         InventoryEntity inv;
         double newQty;
         label120: {
            Object var10000;
            label121: {
               label108: {
                  label85: {
                     Object $result = $continuation.result;
                     var14 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                     switch ($continuation.label) {
                        case 0:
                           ResultKt.throwOnFailure($result);
                           nowStr = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
                           IntakeDao var17 = this.dao;
                           String var10002 = status.getValue();
                           Intrinsics.checkNotNull(nowStr);
                           $continuation.L$0 = this;
                           $continuation.L$1 = status;
                           $continuation.L$2 = takenBy;
                           $continuation.L$3 = notes;
                           $continuation.L$4 = nowStr;
                           $continuation.J$0 = intakeId;
                           $continuation.label = 1;
                           if (var17.confirmIntake(intakeId, var10002, nowStr, takenBy, notes, $continuation) == var14) {
                              return var14;
                           }
                           break;
                        case 1:
                           intakeId = $continuation.J$0;
                           nowStr = (String)$continuation.L$4;
                           notes = (String)$continuation.L$3;
                           takenBy = (String)$continuation.L$2;
                           status = (IntakeStatus)$continuation.L$1;
                           this = (IntakeRepository)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           break;
                        case 2:
                           intakeId = $continuation.J$0;
                           nowStr = (String)$continuation.L$4;
                           notes = (String)$continuation.L$3;
                           takenBy = (String)$continuation.L$2;
                           status = (IntakeStatus)$continuation.L$1;
                           this = (IntakeRepository)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           var10000 = $result;
                           break label85;
                        case 3:
                           intakeId = $continuation.J$0;
                           intake = (IntakeEntity)$continuation.L$4;
                           nowStr = (String)$continuation.L$3;
                           takenBy = (String)$continuation.L$2;
                           status = (IntakeStatus)$continuation.L$1;
                           this = (IntakeRepository)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           break label108;
                        case 4:
                           intakeId = $continuation.J$0;
                           intake = (IntakeEntity)$continuation.L$3;
                           nowStr = (String)$continuation.L$2;
                           takenBy = (String)$continuation.L$1;
                           this = (IntakeRepository)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           var10000 = $result;
                           break label121;
                        case 5:
                           newQty = $continuation.D$0;
                           intakeId = $continuation.J$0;
                           inv = (InventoryEntity)$continuation.L$4;
                           intake = (IntakeEntity)$continuation.L$3;
                           nowStr = (String)$continuation.L$2;
                           takenBy = (String)$continuation.L$1;
                           this = (IntakeRepository)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           break label120;
                        case 6:
                           intakeId = $continuation.J$0;
                           intake = (IntakeEntity)$continuation.L$2;
                           nowStr = (String)$continuation.L$1;
                           this = (IntakeRepository)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           break label119;
                        case 7:
                           ResultKt.throwOnFailure($result);
                           return Boxing.boxBoolean(true);
                        default:
                           throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                     }

                     IntakeDao var18 = this.dao;
                     $continuation.L$0 = this;
                     $continuation.L$1 = status;
                     $continuation.L$2 = takenBy;
                     $continuation.L$3 = notes;
                     $continuation.L$4 = nowStr;
                     $continuation.J$0 = intakeId;
                     $continuation.label = 2;
                     var10000 = var18.getIntakeById(intakeId, $continuation);
                     if (var10000 == var14) {
                        return var14;
                     }
                  }

                  intake = (IntakeEntity)var10000;
                  if (intake == null) {
                     return Boxing.boxBoolean(true);
                  }

                  AuditDao var19 = this.db.auditDao();
                  AuditRecordEntity var10001 = new AuditRecordEntity;
                  Long var10005 = Boxing.boxLong(intake.getPatientId());
                  Long var10007 = Boxing.boxLong(intakeId);
                  String var10009 = status.getValue();
                  String var10011 = notes;
                  if (notes == null) {
                     var10011 = "Sin notas";
                  }

                  var10001.<init>(0L, takenBy, var10005, "INTAKE", var10007, "CONFIRM_INTAKE", "Toma registrada como " + var10009 + " por " + takenBy + ". Notas: " + var10011, (String)null, 129, (DefaultConstructorMarker)null);
                  $continuation.L$0 = this;
                  $continuation.L$1 = status;
                  $continuation.L$2 = takenBy;
                  $continuation.L$3 = nowStr;
                  $continuation.L$4 = intake;
                  $continuation.J$0 = intakeId;
                  $continuation.label = 3;
                  if (var19.insert(var10001, $continuation) == var14) {
                     return var14;
                  }
               }

               if (status != IntakeStatus.CONFIRMED) {
                  break label119;
               }

               InventoryDao var20 = this.db.inventoryDao();
               long var24 = intake.getPatientId();
               long var28 = intake.getMedicationId();
               $continuation.L$0 = this;
               $continuation.L$1 = takenBy;
               $continuation.L$2 = nowStr;
               $continuation.L$3 = intake;
               $continuation.L$4 = null;
               $continuation.J$0 = intakeId;
               $continuation.label = 4;
               var10000 = var20.getInventoryItem(var24, var28, $continuation);
               if (var10000 == var14) {
                  return var14;
               }
            }

            inv = (InventoryEntity)var10000;
            if (inv == null || !(inv.getAvailableQuantity() > (double)0.0F)) {
               break label119;
            }

            newQty = RangesKt.coerceAtLeast(inv.getAvailableQuantity() - (double)1.0F, (double)0.0F);
            InventoryDao var21 = this.db.inventoryDao();
            InventoryEntity var25 = InventoryEntity.copy$default(inv, 0L, 0L, 0L, (String)null, (String)null, newQty, (String)null, (String)null, (String)null, (String)null, 991, (Object)null);
            $continuation.L$0 = this;
            $continuation.L$1 = takenBy;
            $continuation.L$2 = nowStr;
            $continuation.L$3 = intake;
            $continuation.L$4 = inv;
            $continuation.J$0 = intakeId;
            $continuation.D$0 = newQty;
            $continuation.label = 5;
            if (var21.insertOrUpdate(var25, $continuation) == var14) {
               return var14;
            }
         }

         InventoryDao var22 = this.db.inventoryDao();
         InventoryMovementEntity var26 = new InventoryMovementEntity(0L, inv.getId(), intake.getPatientId(), intake.getMedicationId(), "INTAKE_EXIT", (double)-1.0F, newQty, "Toma administrada #" + intakeId, takenBy, nowStr, 1, (DefaultConstructorMarker)null);
         $continuation.L$0 = this;
         $continuation.L$1 = nowStr;
         $continuation.L$2 = intake;
         $continuation.L$3 = null;
         $continuation.L$4 = null;
         $continuation.J$0 = intakeId;
         $continuation.label = 6;
         if (var22.insertMovement(var26, $continuation) == var14) {
            return var14;
         }
      }

      SyncQueueDao var23 = this.db.syncQueueDao();
      String var15 = (new Gson()).toJson(intake);
      Intrinsics.checkNotNullExpressionValue(var15, "toJson(...)");
      Intrinsics.checkNotNull(nowStr);
      SyncQueueEntity var27 = new SyncQueueEntity(0L, "INTAKE", intakeId, "UPDATE", var15, nowStr, 0, (String)null, 193, (DefaultConstructorMarker)null);
      $continuation.L$0 = null;
      $continuation.L$1 = null;
      $continuation.L$2 = null;
      $continuation.L$3 = null;
      $continuation.L$4 = null;
      $continuation.label = 7;
      if (var23.enqueue(var27, $continuation) == var14) {
         return var14;
      } else {
         return Boxing.boxBoolean(true);
      }
   }

   // $FF: synthetic method
   public static Object confirmIntake$default(IntakeRepository var0, long var1, IntakeStatus var3, String var4, String var5, Continuation var6, int var7, Object var8) {
      if ((var7 & 8) != 0) {
         var5 = null;
      }

      return var0.confirmIntake(var1, var3, var4, var5, var6);
   }

   @Nullable
   public final Object skipIntake(long intakeId, @NotNull String reason, @NotNull String skippedBy, @NotNull Continuation<? super Unit> var5) {
      label45: {
         if (var5 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label45;
            }
         }

         $continuation = new ContinuationImpl(var5) {
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
               return IntakeRepository.this.skipIntake(0L, (String)null, (String)null, (Continuation)this);
            }
         };
      }

      Object var9;
      Object var10000;
      label37: {
         Object $result = $continuation.result;
         var9 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
         switch ($continuation.label) {
            case 0:
               ResultKt.throwOnFailure($result);
               LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
               IntakeDao var10 = this.dao;
               $continuation.L$0 = this;
               $continuation.L$1 = reason;
               $continuation.L$2 = skippedBy;
               $continuation.J$0 = intakeId;
               $continuation.label = 1;
               if (var10.skipIntake(intakeId, reason, $continuation) == var9) {
                  return var9;
               }
               break;
            case 1:
               intakeId = $continuation.J$0;
               skippedBy = (String)$continuation.L$2;
               reason = (String)$continuation.L$1;
               this = (IntakeRepository)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               break;
            case 2:
               intakeId = $continuation.J$0;
               skippedBy = (String)$continuation.L$2;
               reason = (String)$continuation.L$1;
               this = (IntakeRepository)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               var10000 = $result;
               break label37;
            case 3:
               ResultKt.throwOnFailure($result);
               return Unit.INSTANCE;
            default:
               throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
         }

         IntakeDao var11 = this.dao;
         $continuation.L$0 = this;
         $continuation.L$1 = reason;
         $continuation.L$2 = skippedBy;
         $continuation.J$0 = intakeId;
         $continuation.label = 2;
         var10000 = var11.getIntakeById(intakeId, $continuation);
         if (var10000 == var9) {
            return var9;
         }
      }

      IntakeEntity intake = (IntakeEntity)var10000;
      if (intake == null) {
         return Unit.INSTANCE;
      } else {
         AuditDao var12 = this.db.auditDao();
         AuditRecordEntity var10001 = new AuditRecordEntity(0L, skippedBy, Boxing.boxLong(intake.getPatientId()), "INTAKE", Boxing.boxLong(intakeId), "SKIP_INTAKE", "Toma omitida por " + skippedBy + ". Motivo clínico/personal: " + reason, (String)null, 129, (DefaultConstructorMarker)null);
         $continuation.L$0 = null;
         $continuation.L$1 = null;
         $continuation.L$2 = null;
         $continuation.label = 3;
         if (var12.insert(var10001, $continuation) == var9) {
            return var9;
         } else {
            return Unit.INSTANCE;
         }
      }
   }

   @Nullable
   public final Object generateIntakesForMedication(@NotNull Medication medication, int daysAhead, @NotNull Continuation<? super List<Long>> var3) {
      label129: {
         if (var3 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label129;
            }
         }

         $continuation = new ContinuationImpl(var3) {
            Object L$0;
            Object L$1;
            Object L$2;
            Object L$3;
            Object L$4;
            Object L$5;
            Object L$6;
            Object L$7;
            int I$0;
            int I$1;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return IntakeRepository.this.generateIntakesForMedication((Medication)null, 0, (Continuation)this);
            }
         };
      }

      Object $result = $continuation.result;
      Object var18 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      List hours;
      List createdIds;
      LocalDate today;
      int dayOffset;
      String dateStr;
      Iterator $i$f$mapTo;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            if (!medication.isVerifiedAndActive()) {
               throw new IllegalStateException("El tratamiento '" + medication.getTranscribedName() + "' no está verificado/activo.");
            }

            String hoursStr = medication.getExactScheduleHours();
            CharSequence var19 = (CharSequence)hoursStr;
            if (var19 == null || StringsKt.isBlank(var19)) {
               throw new IllegalStateException("El tratamiento no cuenta con horarios exactos confirmados.");
            }

            CharSequence var41 = (CharSequence)hoursStr;
            String[] var20 = new String[]{","};
            Iterable $this$map$iv = (Iterable)StringsKt.split$default(var41, var20, false, 0, 6, (Object)null);
            int $i$f$map = 0;
            Collection destination$iv$iv = (Collection)(new ArrayList(CollectionsKt.collectionSizeOrDefault($this$map$iv, 10)));
            int $i$f$mapTo = 0;

            for(Object item$iv$iv : $this$map$iv) {
               String id = (String)item$iv$iv;
               int var14 = 0;
               destination$iv$iv.add(StringsKt.trim((CharSequence)id).toString());
            }

            $this$map$iv = (Iterable)((List)destination$iv$iv);
            $i$f$map = 0;
            destination$iv$iv = (Collection)(new ArrayList());
            $i$f$mapTo = 0;

            for(Object element$iv$iv : $this$map$iv) {
               String it = (String)element$iv$iv;
               int var39 = 0;
               if (((CharSequence)it).length() > 0) {
                  destination$iv$iv.add(element$iv$iv);
               }
            }

            hours = (List)destination$iv$iv;
            createdIds = (List)(new ArrayList());
            today = LocalDate.now();
            dayOffset = 0;
            if (dayOffset >= daysAhead) {
               return createdIds;
            }

            String var42 = today.plusDays((long)dayOffset).toString();
            Intrinsics.checkNotNullExpressionValue(var42, "toString(...)");
            dateStr = var42;
            $i$f$mapTo = hours.iterator();
            break;
         case 1:
            dayOffset = $continuation.I$1;
            daysAhead = $continuation.I$0;
            String h = (String)$continuation.L$7;
            $i$f$mapTo = (Iterator)$continuation.L$6;
            dateStr = (String)$continuation.L$5;
            today = (LocalDate)$continuation.L$4;
            createdIds = (List)$continuation.L$3;
            hours = (List)$continuation.L$2;
            medication = (Medication)$continuation.L$1;
            this = (IntakeRepository)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            boolean var12 = (Boolean)$result;
            if (!var12) {
               IntakeDao var10000 = this.dao;
               IntakeEntity var10001 = new IntakeEntity;
               long var10004 = medication.getPatientId();
               long var10005 = medication.getId();
               String var10009 = medication.getPrescribedDose();
               if (var10009 == null) {
                  var10009 = medication.getIndicatedQuantity();
                  if (var10009 == null) {
                     var10009 = "Dosis indicada";
                  }
               }

               var10001.<init>(0L, var10004, var10005, dateStr, h, (String)null, var10009, (String)null, (String)null, "PENDING", (String)null, (String)null, false, (String)null, (String)null, 32161, (DefaultConstructorMarker)null);
               $continuation.L$0 = this;
               $continuation.L$1 = medication;
               $continuation.L$2 = hours;
               $continuation.L$3 = createdIds;
               $continuation.L$4 = today;
               $continuation.L$5 = dateStr;
               $continuation.L$6 = $i$f$mapTo;
               $continuation.L$7 = null;
               $continuation.I$0 = daysAhead;
               $continuation.I$1 = dayOffset;
               $continuation.label = 2;
               Object var40 = var10000.insert(var10001, $continuation);
               if (var40 == var18) {
                  return var18;
               }

               long var35 = ((Number)var40).longValue();
               createdIds.add(Boxing.boxLong(var35));
            }
            break;
         case 2:
            dayOffset = $continuation.I$1;
            daysAhead = $continuation.I$0;
            $i$f$mapTo = (Iterator)$continuation.L$6;
            dateStr = (String)$continuation.L$5;
            today = (LocalDate)$continuation.L$4;
            createdIds = (List)$continuation.L$3;
            hours = (List)$continuation.L$2;
            medication = (Medication)$continuation.L$1;
            this = (IntakeRepository)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            long var13 = ((Number)$result).longValue();
            createdIds.add(Boxing.boxLong(var13));
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      while(true) {
         while(!$i$f$mapTo.hasNext()) {
            ++dayOffset;
            if (dayOffset >= daysAhead) {
               return createdIds;
            }

            String var43 = today.plusDays((long)dayOffset).toString();
            Intrinsics.checkNotNullExpressionValue(var43, "toString(...)");
            dateStr = var43;
            $i$f$mapTo = hours.iterator();
         }

         String h = (String)$i$f$mapTo.next();
         IntakeDao var44 = this.dao;
         long var48 = medication.getId();
         $continuation.L$0 = this;
         $continuation.L$1 = medication;
         $continuation.L$2 = hours;
         $continuation.L$3 = createdIds;
         $continuation.L$4 = today;
         $continuation.L$5 = dateStr;
         $continuation.L$6 = $i$f$mapTo;
         $continuation.L$7 = h;
         $continuation.I$0 = daysAhead;
         $continuation.I$1 = dayOffset;
         $continuation.label = 1;
         Object var45 = var44.existsIntake(var48, dateStr, h, $continuation);
         if (var45 == var18) {
            return var18;
         }

         boolean exists = (Boolean)var45;
         if (!exists) {
            IntakeDao var46 = this.dao;
            IntakeEntity var49 = new IntakeEntity;
            long var50 = medication.getPatientId();
            long var51 = medication.getId();
            String var52 = medication.getPrescribedDose();
            if (var52 == null) {
               var52 = medication.getIndicatedQuantity();
               if (var52 == null) {
                  var52 = "Dosis indicada";
               }
            }

            var49.<init>(0L, var50, var51, dateStr, h, (String)null, var52, (String)null, (String)null, "PENDING", (String)null, (String)null, false, (String)null, (String)null, 32161, (DefaultConstructorMarker)null);
            $continuation.L$0 = this;
            $continuation.L$1 = medication;
            $continuation.L$2 = hours;
            $continuation.L$3 = createdIds;
            $continuation.L$4 = today;
            $continuation.L$5 = dateStr;
            $continuation.L$6 = $i$f$mapTo;
            $continuation.L$7 = null;
            $continuation.I$0 = daysAhead;
            $continuation.I$1 = dayOffset;
            $continuation.label = 2;
            Object var47 = var46.insert(var49, $continuation);
            if (var47 == var18) {
               return var18;
            }

            long id = ((Number)var47).longValue();
            createdIds.add(Boxing.boxLong(id));
         }
      }
   }

   // $FF: synthetic method
   public static Object generateIntakesForMedication$default(IntakeRepository var0, Medication var1, int var2, Continuation var3, int var4, Object var5) {
      if ((var4 & 2) != 0) {
         var2 = 7;
      }

      return var0.generateIntakesForMedication(var1, var2, var3);
   }

   private final Intake toDomain(IntakeEntity $this$toDomain, String medName, String activeIng, String patientName, boolean delayed) {
      return new Intake($this$toDomain.getId(), $this$toDomain.getPatientId(), $this$toDomain.getMedicationId(), $this$toDomain.getScheduledDate(), $this$toDomain.getScheduledTime(), $this$toDomain.getPeriod(), $this$toDomain.getDoseText(), $this$toDomain.getConfirmedAt(), $this$toDomain.getConfirmedBy(), IntakeStatus.Companion.from($this$toDomain.getStatus()), $this$toDomain.getNotes(), $this$toDomain.getSkipReason(), $this$toDomain.getNotificationSent(), $this$toDomain.getNotificationSentAt(), $this$toDomain.getCreatedAt(), medName, activeIng, patientName, delayed);
   }

   // $FF: synthetic method
   public static final ViernesDatabase access$getDb$p(IntakeRepository $this) {
      return $this.db;
   }

   // $FF: synthetic method
   public static final Intake access$toDomain(IntakeRepository $this, IntakeEntity $receiver, String medName, String activeIng, String patientName, boolean delayed) {
      return $this.toDomain($receiver, medName, activeIng, patientName, delayed);
   }
}
