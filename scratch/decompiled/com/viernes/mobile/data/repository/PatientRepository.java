package com.viernes.mobile.data.repository;

import androidx.compose.runtime.internal.StabilityInferred;
import com.google.gson.Gson;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.local.dao.AuditDao;
import com.viernes.mobile.data.local.dao.PatientDao;
import com.viernes.mobile.data.local.dao.SyncQueueDao;
import com.viernes.mobile.data.local.entity.AuditRecordEntity;
import com.viernes.mobile.data.local.entity.PatientEntity;
import com.viernes.mobile.data.local.entity.SyncQueueEntity;
import com.viernes.mobile.domain.model.Patient;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
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
   d1 = {"\u0000D\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0002\b\u0007\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004J.\u0010\u0007\u001a\u00020\b2\u0006\u0010\t\u001a\u00020\n2\u0006\u0010\u000b\u001a\u00020\f2\u0006\u0010\r\u001a\u00020\n2\u0006\u0010\u000e\u001a\u00020\u0001H\u0082@¢\u0006\u0002\u0010\u000fJ\u0012\u0010\u0010\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00130\u00120\u0011J\u0018\u0010\u0014\u001a\u0004\u0018\u00010\u00132\u0006\u0010\u000b\u001a\u00020\fH\u0086@¢\u0006\u0002\u0010\u0015J \u0010\u0016\u001a\u00020\f2\u0006\u0010\u0017\u001a\u00020\u00132\b\b\u0002\u0010\u0018\u001a\u00020\nH\u0086@¢\u0006\u0002\u0010\u0019J\f\u0010\u001a\u001a\u00020\u0013*\u00020\u001bH\u0002J\f\u0010\u001c\u001a\u00020\u001b*\u00020\u0013H\u0002R\u000e\u0010\u0005\u001a\u00020\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\u001d"},
   d2 = {"Lcom/viernes/mobile/data/repository/PatientRepository;", "", "db", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "(Lcom/viernes/mobile/data/local/ViernesDatabase;)V", "dao", "Lcom/viernes/mobile/data/local/dao/PatientDao;", "enqueueSync", "", "type", "", "id", "", "op", "data", "(Ljava/lang/String;JLjava/lang/String;Ljava/lang/Object;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getActivePatients", "Lkotlinx/coroutines/flow/Flow;", "", "Lcom/viernes/mobile/domain/model/Patient;", "getPatientById", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "savePatient", "patient", "userId", "(Lcom/viernes/mobile/domain/model/Patient;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "toDomain", "Lcom/viernes/mobile/data/local/entity/PatientEntity;", "toEntity", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
@SourceDebugExtension({"SMAP\nRepositories.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Repositories.kt\ncom/viernes/mobile/data/repository/PatientRepository\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt\n+ 4 SafeCollector.common.kt\nkotlinx/coroutines/flow/internal/SafeCollector_commonKt\n*L\n1#1,402:1\n49#2:403\n51#2:407\n46#3:404\n51#3:406\n105#4:405\n*S KotlinDebug\n*F\n+ 1 Repositories.kt\ncom/viernes/mobile/data/repository/PatientRepository\n*L\n16#1:403\n16#1:407\n16#1:404\n16#1:406\n16#1:405\n*E\n"})
public final class PatientRepository {
   @NotNull
   private final ViernesDatabase db;
   @NotNull
   private final PatientDao dao;
   public static final int $stable = 8;

   public PatientRepository(@NotNull ViernesDatabase db) {
      Intrinsics.checkNotNullParameter(db, "db");
      super();
      this.db = db;
      this.dao = this.db.patientDao();
   }

   @NotNull
   public final Flow<List<Patient>> getActivePatients() {
      Flow $this$map$iv = this.dao.getAllActivePatients();
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new PatientRepository$getActivePatients$$inlined$map$1($this$map$iv, this);
   }

   @Nullable
   public final Object getPatientById(long id, @NotNull Continuation<? super Patient> var3) {
      label25: {
         if (var3 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label25;
            }
         }

         $continuation = new ContinuationImpl(var3) {
            Object L$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return PatientRepository.this.getPatientById(0L, (Continuation)this);
            }
         };
      }

      Object $result = $continuation.result;
      Object var6 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      Object var10000;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            PatientDao var7 = this.dao;
            $continuation.L$0 = this;
            $continuation.label = 1;
            var10000 = var7.getPatientById(id, $continuation);
            if (var10000 == var6) {
               return var6;
            }
            break;
         case 1:
            this = (PatientRepository)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            var10000 = $result;
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      return (PatientEntity)var10000 != null ? this.toDomain((PatientEntity)var10000) : null;
   }

   @Nullable
   public final Object savePatient(@NotNull Patient patient, @NotNull String userId, @NotNull Continuation<? super Long> var3) {
      label51: {
         if (var3 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label51;
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
               return PatientRepository.this.savePatient((Patient)null, (String)null, (Continuation)this);
            }
         };
      }

      long id;
      Object var9;
      label55: {
         Object $result = $continuation.result;
         var9 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
         Object var10000;
         switch ($continuation.label) {
            case 0:
               ResultKt.throwOnFailure($result);
               PatientEntity entity = this.toEntity(patient);
               PatientDao var10 = this.dao;
               $continuation.L$0 = this;
               $continuation.L$1 = patient;
               $continuation.L$2 = userId;
               $continuation.label = 1;
               var10000 = var10.insert(entity, $continuation);
               if (var10000 == var9) {
                  return var9;
               }
               break;
            case 1:
               userId = (String)$continuation.L$2;
               patient = (Patient)$continuation.L$1;
               this = (PatientRepository)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               var10000 = $result;
               break;
            case 2:
               id = $continuation.J$0;
               patient = (Patient)$continuation.L$1;
               this = (PatientRepository)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               break label55;
            case 3:
               id = $continuation.J$0;
               ResultKt.throwOnFailure($result);
               return Boxing.boxLong(id);
            default:
               throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
         }

         id = ((Number)var10000).longValue();
         AuditDao var11 = this.db.auditDao();
         AuditRecordEntity var10001 = new AuditRecordEntity(0L, userId, Boxing.boxLong(id), "PATIENT", Boxing.boxLong(id), patient.getId() == 0L ? "CREATE" : "UPDATE", "Paciente guardado: " + patient.getDisplayName(), (String)null, 129, (DefaultConstructorMarker)null);
         $continuation.L$0 = this;
         $continuation.L$1 = patient;
         $continuation.L$2 = null;
         $continuation.J$0 = id;
         $continuation.label = 2;
         if (var11.insert(var10001, $continuation) == var9) {
            return var9;
         }
      }

      String var10003 = patient.getId() == 0L ? "INSERT" : "UPDATE";
      $continuation.L$0 = null;
      $continuation.L$1 = null;
      $continuation.J$0 = id;
      $continuation.label = 3;
      if (this.enqueueSync("PATIENT", id, var10003, patient, $continuation) == var9) {
         return var9;
      } else {
         return Boxing.boxLong(id);
      }
   }

   // $FF: synthetic method
   public static Object savePatient$default(PatientRepository var0, Patient var1, String var2, Continuation var3, int var4, Object var5) {
      if ((var4 & 2) != 0) {
         var2 = "mobile_user";
      }

      return var0.savePatient(var1, var2, var3);
   }

   private final Object enqueueSync(String type, long id, String op, Object data, Continuation<? super Unit> $completion) {
      SyncQueueDao var10000 = this.db.syncQueueDao();
      String var10007 = (new Gson()).toJson(data);
      Intrinsics.checkNotNullExpressionValue(var10007, "toJson(...)");
      String var10008 = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
      Intrinsics.checkNotNullExpressionValue(var10008, "format(...)");
      Object var7 = var10000.enqueue(new SyncQueueEntity(0L, type, id, op, var10007, var10008, 0, (String)null, 193, (DefaultConstructorMarker)null), $completion);
      return var7 == IntrinsicsKt.getCOROUTINE_SUSPENDED() ? var7 : Unit.INSTANCE;
   }

   private final Patient toDomain(PatientEntity $this$toDomain) {
      return new Patient($this$toDomain.getId(), $this$toDomain.getProvisionalLabel(), $this$toDomain.getLegalName(), $this$toDomain.getBirthDate(), $this$toDomain.getContactInfo(), $this$toDomain.getEmergencyContact(), $this$toDomain.getDeclaredAllergies(), $this$toDomain.getAllergiesVerified(), $this$toDomain.getMedicalNotes(), $this$toDomain.getStatus(), $this$toDomain.getCreatedAt(), $this$toDomain.getUpdatedAt(), $this$toDomain.getCreatedBy());
   }

   private final PatientEntity toEntity(Patient $this$toEntity) {
      PatientEntity var10000 = new PatientEntity;
      long var10002 = $this$toEntity.getId();
      String var10003 = $this$toEntity.getProvisionalLabel();
      String var10004 = $this$toEntity.getLegalName();
      String var10005 = $this$toEntity.getBirthDate();
      String var10006 = $this$toEntity.getContactInfo();
      String var10007 = $this$toEntity.getEmergencyContact();
      String var10008 = $this$toEntity.getDeclaredAllergies();
      boolean var10009 = $this$toEntity.getAllergiesVerified();
      String var10010 = $this$toEntity.getMedicalNotes();
      String var10011 = $this$toEntity.getStatus();
      String var10012 = $this$toEntity.getCreatedAt();
      if (var10012 == null) {
         var10012 = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
      }

      var10000.<init>(var10002, var10003, var10004, var10005, var10006, var10007, var10008, var10009, var10010, var10011, var10012, LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME), $this$toEntity.getCreatedBy());
      return var10000;
   }

   // $FF: synthetic method
   public static final Object access$enqueueSync(PatientRepository $this, String type, long id, String op, Object data, Continuation $completion) {
      return $this.enqueueSync(type, id, op, data, $completion);
   }

   // $FF: synthetic method
   public static final Patient access$toDomain(PatientRepository $this, PatientEntity $receiver) {
      return $this.toDomain($receiver);
   }
}
