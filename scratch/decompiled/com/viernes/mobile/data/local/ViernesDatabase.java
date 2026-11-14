package com.viernes.mobile.data.local;

import android.content.Context;
import androidx.compose.runtime.internal.StabilityInferred;
import androidx.room.Database;
import androidx.room.RoomDatabase;
import androidx.sqlite.db.SupportSQLiteDatabase;
import com.viernes.mobile.data.local.dao.AppointmentDao;
import com.viernes.mobile.data.local.dao.AuditDao;
import com.viernes.mobile.data.local.dao.CaregiverDao;
import com.viernes.mobile.data.local.dao.ClinicalWarningDao;
import com.viernes.mobile.data.local.dao.IntakeDao;
import com.viernes.mobile.data.local.dao.InventoryDao;
import com.viernes.mobile.data.local.dao.MedicationDao;
import com.viernes.mobile.data.local.dao.PatientDao;
import com.viernes.mobile.data.local.dao.RefillDao;
import com.viernes.mobile.data.local.dao.SyncQueueDao;
import com.viernes.mobile.data.local.dao.TreatmentVersionDao;
import com.viernes.mobile.data.local.entity.AppointmentEntity;
import com.viernes.mobile.data.local.entity.AuditRecordEntity;
import com.viernes.mobile.data.local.entity.CaregiverEntity;
import com.viernes.mobile.data.local.entity.ClinicalWarningEntity;
import com.viernes.mobile.data.local.entity.IntakeEntity;
import com.viernes.mobile.data.local.entity.InventoryEntity;
import com.viernes.mobile.data.local.entity.InventoryMovementEntity;
import com.viernes.mobile.data.local.entity.MedicationEntity;
import com.viernes.mobile.data.local.entity.PatientEntity;
import com.viernes.mobile.data.local.entity.RefillEntity;
import com.viernes.mobile.data.local.entity.SyncQueueEntity;
import com.viernes.mobile.data.local.entity.TreatmentVersionEntity;
import java.time.LocalDate;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.Boxing;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlinx.coroutines.BuildersKt;
import kotlinx.coroutines.CoroutineScope;
import kotlinx.coroutines.CoroutineScopeKt;
import kotlinx.coroutines.CoroutineStart;
import kotlinx.coroutines.Dispatchers;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000P\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\b'\u0018\u0000 \u00192\u00020\u0001:\u0001\u0019B\u0005¢\u0006\u0002\u0010\u0002J\b\u0010\u0003\u001a\u00020\u0004H&J\b\u0010\u0005\u001a\u00020\u0006H&J\b\u0010\u0007\u001a\u00020\bH&J\b\u0010\t\u001a\u00020\nH&J\b\u0010\u000b\u001a\u00020\fH&J\b\u0010\r\u001a\u00020\u000eH&J\b\u0010\u000f\u001a\u00020\u0010H&J\b\u0010\u0011\u001a\u00020\u0012H&J\b\u0010\u0013\u001a\u00020\u0014H&J\b\u0010\u0015\u001a\u00020\u0016H&J\b\u0010\u0017\u001a\u00020\u0018H&¨\u0006\u001a"},
   d2 = {"Lcom/viernes/mobile/data/local/ViernesDatabase;", "Landroidx/room/RoomDatabase;", "()V", "appointmentDao", "Lcom/viernes/mobile/data/local/dao/AppointmentDao;", "auditDao", "Lcom/viernes/mobile/data/local/dao/AuditDao;", "caregiverDao", "Lcom/viernes/mobile/data/local/dao/CaregiverDao;", "clinicalWarningDao", "Lcom/viernes/mobile/data/local/dao/ClinicalWarningDao;", "intakeDao", "Lcom/viernes/mobile/data/local/dao/IntakeDao;", "inventoryDao", "Lcom/viernes/mobile/data/local/dao/InventoryDao;", "medicationDao", "Lcom/viernes/mobile/data/local/dao/MedicationDao;", "patientDao", "Lcom/viernes/mobile/data/local/dao/PatientDao;", "refillDao", "Lcom/viernes/mobile/data/local/dao/RefillDao;", "syncQueueDao", "Lcom/viernes/mobile/data/local/dao/SyncQueueDao;", "treatmentVersionDao", "Lcom/viernes/mobile/data/local/dao/TreatmentVersionDao;", "Companion", "app_debug"}
)
@Database(
   entities = {PatientEntity.class, MedicationEntity.class, TreatmentVersionEntity.class, IntakeEntity.class, AppointmentEntity.class, RefillEntity.class, InventoryEntity.class, InventoryMovementEntity.class, CaregiverEntity.class, ClinicalWarningEntity.class, AuditRecordEntity.class, SyncQueueEntity.class},
   version = 1,
   exportSchema = false
)
@StabilityInferred(
   parameters = 1
)
public abstract class ViernesDatabase extends RoomDatabase {
   @NotNull
   public static final Companion Companion = new Companion((DefaultConstructorMarker)null);
   public static final int $stable;
   @Nullable
   private static volatile ViernesDatabase INSTANCE;

   public ViernesDatabase() {
   }

   @NotNull
   public abstract PatientDao patientDao();

   @NotNull
   public abstract MedicationDao medicationDao();

   @NotNull
   public abstract TreatmentVersionDao treatmentVersionDao();

   @NotNull
   public abstract IntakeDao intakeDao();

   @NotNull
   public abstract AppointmentDao appointmentDao();

   @NotNull
   public abstract RefillDao refillDao();

   @NotNull
   public abstract InventoryDao inventoryDao();

   @NotNull
   public abstract CaregiverDao caregiverDao();

   @NotNull
   public abstract ClinicalWarningDao clinicalWarningDao();

   @NotNull
   public abstract AuditDao auditDao();

   @NotNull
   public abstract SyncQueueDao syncQueueDao();

   // $FF: synthetic method
   public static final void access$setINSTANCE$cp(ViernesDatabase var0) {
      INSTANCE = var0;
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\"\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0002\b\u0004\b\u0086\u0003\u0018\u00002\u00020\u0001:\u0001\fB\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0005\u001a\u00020\u00042\u0006\u0010\u0006\u001a\u00020\u0007J\u0016\u0010\b\u001a\u00020\t2\u0006\u0010\n\u001a\u00020\u0004H\u0082@¢\u0006\u0002\u0010\u000bR\u0010\u0010\u0003\u001a\u0004\u0018\u00010\u0004X\u0082\u000e¢\u0006\u0002\n\u0000¨\u0006\r"},
      d2 = {"Lcom/viernes/mobile/data/local/ViernesDatabase$Companion;", "", "()V", "INSTANCE", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "getInstance", "context", "Landroid/content/Context;", "seedInitialData", "", "database", "(Lcom/viernes/mobile/data/local/ViernesDatabase;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "DatabasePrepopulateCallback", "app_debug"}
   )
   public static final class Companion {
      private Companion() {
      }

      @NotNull
      public final ViernesDatabase getInstance(@NotNull Context param1) {
         // $FF: Couldn't be decompiled
      }

      private final Object seedInitialData(ViernesDatabase database, Continuation<? super Unit> var2) {
         label71: {
            if (var2 instanceof Continuation $continuation) {
               if (($continuation.label & Integer.MIN_VALUE) != 0) {
                  $continuation.label -= Integer.MIN_VALUE;
                  break label71;
               }
            }

            $continuation = new ContinuationImpl(var2) {
               Object L$0;
               Object L$1;
               Object L$2;
               Object L$3;
               long J$0;
               long J$1;
               // $FF: synthetic field
               Object result;
               int label;

               @Nullable
               public final Object invokeSuspend(@NotNull Object $result) {
                  this.result = $result;
                  this.label |= Integer.MIN_VALUE;
                  return Companion.this.seedInitialData((ViernesDatabase)null, (Continuation)this);
               }
            };
         }

         AuditDao auditDao;
         long papaId;
         long papaMetforminaId;
         Object var16;
         label81: {
            IntakeDao intakeDao;
            Object var10000;
            label82: {
               MedicationDao medDao;
               label58: {
                  long mamaId;
                  label57: {
                     Object $result = $continuation.result;
                     var16 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                     PatientDao patientDao;
                     switch ($continuation.label) {
                        case 0:
                           ResultKt.throwOnFailure($result);
                           patientDao = database.patientDao();
                           medDao = database.medicationDao();
                           intakeDao = database.intakeDao();
                           auditDao = database.auditDao();
                           PatientEntity var10001 = new PatientEntity(0L, "Mamá", "Mamá", (String)null, (String)null, (String)null, "Ninguna declarada", true, "Control de diabetes e hipertensión arterial.", "active", (String)null, (String)null, (String)null, 7225, (DefaultConstructorMarker)null);
                           $continuation.L$0 = patientDao;
                           $continuation.L$1 = medDao;
                           $continuation.L$2 = intakeDao;
                           $continuation.L$3 = auditDao;
                           $continuation.label = 1;
                           var10000 = patientDao.insert(var10001, $continuation);
                           if (var10000 == var16) {
                              return var16;
                           }
                           break;
                        case 1:
                           auditDao = (AuditDao)$continuation.L$3;
                           intakeDao = (IntakeDao)$continuation.L$2;
                           medDao = (MedicationDao)$continuation.L$1;
                           patientDao = (PatientDao)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           var10000 = $result;
                           break;
                        case 2:
                           mamaId = $continuation.J$0;
                           auditDao = (AuditDao)$continuation.L$2;
                           intakeDao = (IntakeDao)$continuation.L$1;
                           medDao = (MedicationDao)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           var10000 = $result;
                           break label57;
                        case 3:
                           papaId = $continuation.J$0;
                           auditDao = (AuditDao)$continuation.L$2;
                           intakeDao = (IntakeDao)$continuation.L$1;
                           medDao = (MedicationDao)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           break label58;
                        case 4:
                           papaId = $continuation.J$0;
                           auditDao = (AuditDao)$continuation.L$1;
                           intakeDao = (IntakeDao)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           var10000 = $result;
                           break label82;
                        case 5:
                           papaMetforminaId = $continuation.J$1;
                           papaId = $continuation.J$0;
                           auditDao = (AuditDao)$continuation.L$0;
                           ResultKt.throwOnFailure($result);
                           break label81;
                        case 6:
                           ResultKt.throwOnFailure($result);
                           return Unit.INSTANCE;
                        default:
                           throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                     }

                     mamaId = ((Number)var10000).longValue();
                     PatientEntity var20 = new PatientEntity(0L, "Papá", "Papá", (String)null, (String)null, (String)null, "Ninguna declarada", true, "Control metabólico y neurológico.", "active", (String)null, (String)null, (String)null, 7225, (DefaultConstructorMarker)null);
                     $continuation.L$0 = medDao;
                     $continuation.L$1 = intakeDao;
                     $continuation.L$2 = auditDao;
                     $continuation.L$3 = null;
                     $continuation.J$0 = mamaId;
                     $continuation.label = 2;
                     var10000 = patientDao.insert(var20, $continuation);
                     if (var10000 == var16) {
                        return var16;
                     }
                  }

                  papaId = ((Number)var10000).longValue();
                  MedicationEntity var21 = new MedicationEntity(0L, mamaId, "Metformina", "Glucophage", "Metformina clorhidrato", (String)null, "500 mg", "Mañana: 2, Noche: 2", "tabletas", "500 mg", (String)null, (String)null, "07:00, 18:00", (String)null, "diabetes", (String)null, (String)null, (String)null, (String)null, "ACTIVE", "active", (String)null, (String)null, "cuidador_autorizado", (String)null, false, (String)null, (String)null, 258452513, (DefaultConstructorMarker)null);
                  $continuation.L$0 = medDao;
                  $continuation.L$1 = intakeDao;
                  $continuation.L$2 = auditDao;
                  $continuation.J$0 = papaId;
                  $continuation.label = 3;
                  if (medDao.insert(var21, $continuation) == var16) {
                     return var16;
                  }
               }

               MedicationEntity var22 = new MedicationEntity(0L, papaId, "Metformina", "Metformina", "Metformina", (String)null, "850 mg", "Mañana: 1, Noche: 1", "tabletas", "850 mg", (String)null, (String)null, "07:00, 18:00", (String)null, "diabetes", (String)null, (String)null, (String)null, (String)null, "ACTIVE", "active", (String)null, (String)null, "cuidador_autorizado", (String)null, false, (String)null, (String)null, 258452513, (DefaultConstructorMarker)null);
               $continuation.L$0 = intakeDao;
               $continuation.L$1 = auditDao;
               $continuation.L$2 = null;
               $continuation.J$0 = papaId;
               $continuation.label = 4;
               var10000 = medDao.insert(var22, $continuation);
               if (var10000 == var16) {
                  return var16;
               }
            }

            papaMetforminaId = ((Number)var10000).longValue();
            String var19 = LocalDate.now().toString();
            Intrinsics.checkNotNullExpressionValue(var19, "toString(...)");
            String todayStr = var19;
            IntakeEntity var23 = new IntakeEntity(0L, papaId, papaMetforminaId, todayStr, "18:00", (String)null, "850 mg", (String)null, (String)null, "PENDING", (String)null, (String)null, false, (String)null, (String)null, 28065, (DefaultConstructorMarker)null);
            $continuation.L$0 = auditDao;
            $continuation.L$1 = null;
            $continuation.J$0 = papaId;
            $continuation.J$1 = papaMetforminaId;
            $continuation.label = 5;
            if (intakeDao.insert(var23, $continuation) == var16) {
               return var16;
            }
         }

         AuditRecordEntity var24 = new AuditRecordEntity(0L, "system", Boxing.boxLong(papaId), "MEDICATION", Boxing.boxLong(papaMetforminaId), "INITIAL_SEED", "Inicialización segura offline con pacientes y tratamientos verificados", (String)null, 129, (DefaultConstructorMarker)null);
         $continuation.L$0 = null;
         $continuation.label = 6;
         if (auditDao.insert(var24, $continuation) == var16) {
            return var16;
         } else {
            return Unit.INSTANCE;
         }
      }

      // $FF: synthetic method
      public Companion(DefaultConstructorMarker $constructor_marker) {
         this();
      }

      @Metadata(
         mv = {1, 9, 0},
         k = 1,
         xi = 48,
         d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\b\u0002\u0018\u00002\u00020\u0001B\u0005¢\u0006\u0002\u0010\u0002J\u0010\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006H\u0016¨\u0006\u0007"},
         d2 = {"Lcom/viernes/mobile/data/local/ViernesDatabase$Companion$DatabasePrepopulateCallback;", "Landroidx/room/RoomDatabase$Callback;", "()V", "onCreate", "", "db", "Landroidx/sqlite/db/SupportSQLiteDatabase;", "app_debug"}
      )
      private static final class DatabasePrepopulateCallback extends RoomDatabase.Callback {
         public DatabasePrepopulateCallback() {
         }

         public void onCreate(@NotNull SupportSQLiteDatabase db) {
            Intrinsics.checkNotNullParameter(db, "db");
            super.onCreate(db);
            BuildersKt.launch$default(CoroutineScopeKt.CoroutineScope((CoroutineContext)Dispatchers.getIO()), (CoroutineContext)null, (CoroutineStart)null, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
               int label;

               @Nullable
               public final Object invokeSuspend(@NotNull Object $result) {
                  Object var4 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
                  switch (this.label) {
                     case 0:
                        ResultKt.throwOnFailure($result);
                        ViernesDatabase var10000 = ViernesDatabase.INSTANCE;
                        if (var10000 != null) {
                           ViernesDatabase database = var10000;
                           int var5 = 0;
                           Companion var6 = ViernesDatabase.Companion;
                           this.label = 1;
                           if (var6.seedInitialData(database, this) == var4) {
                              return var4;
                           }
                        }
                        break;
                     case 1:
                        int var3 = 0;
                        ResultKt.throwOnFailure($result);
                        break;
                     default:
                        throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                  }

                  return Unit.INSTANCE;
               }

               @NotNull
               public final Continuation<Unit> create(@Nullable Object value, @NotNull Continuation<?> $completion) {
                  return (Continuation)(new <anonymous constructor>($completion));
               }

               @Nullable
               public final Object invoke(@NotNull CoroutineScope p1, @Nullable Continuation<? super Unit> p2) {
                  return ((<undefinedtype>)this.create(p1, p2)).invokeSuspend(Unit.INSTANCE);
               }
            }, 3, (Object)null);
         }
      }
   }
}
