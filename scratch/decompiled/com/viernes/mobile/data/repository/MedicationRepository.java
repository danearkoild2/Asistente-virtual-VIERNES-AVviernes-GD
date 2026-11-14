package com.viernes.mobile.data.repository;

import androidx.compose.runtime.internal.StabilityInferred;
import com.google.gson.Gson;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.local.dao.AuditDao;
import com.viernes.mobile.data.local.dao.MedicationDao;
import com.viernes.mobile.data.local.dao.SyncQueueDao;
import com.viernes.mobile.data.local.dao.TreatmentVersionDao;
import com.viernes.mobile.data.local.entity.AuditRecordEntity;
import com.viernes.mobile.data.local.entity.MedicationEntity;
import com.viernes.mobile.data.local.entity.SyncQueueEntity;
import com.viernes.mobile.data.local.entity.TreatmentVersionEntity;
import com.viernes.mobile.domain.model.Medication;
import com.viernes.mobile.domain.model.VerificationStatus;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collection;
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
import kotlinx.coroutines.flow.Flow;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000J\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004J\u001c\u0010\u0007\u001a\b\u0012\u0004\u0012\u00020\t0\b2\u0006\u0010\n\u001a\u00020\u000bH\u0086@¢\u0006\u0002\u0010\fJ\u0018\u0010\r\u001a\u0004\u0018\u00010\t2\u0006\u0010\u000e\u001a\u00020\u000bH\u0086@¢\u0006\u0002\u0010\fJ\u001a\u0010\u000f\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\t0\b0\u00102\u0006\u0010\n\u001a\u00020\u000bJ \u0010\u0011\u001a\u00020\u000b2\u0006\u0010\u0012\u001a\u00020\t2\b\b\u0002\u0010\u0013\u001a\u00020\u0014H\u0086@¢\u0006\u0002\u0010\u0015J\u001e\u0010\u0016\u001a\u00020\u00172\u0006\u0010\u0018\u001a\u00020\u000b2\u0006\u0010\u0019\u001a\u00020\u0014H\u0086@¢\u0006\u0002\u0010\u001aJ\f\u0010\u001b\u001a\u00020\t*\u00020\u001cH\u0002J\f\u0010\u001d\u001a\u00020\u001c*\u00020\tH\u0002R\u000e\u0010\u0005\u001a\u00020\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\u001e"},
   d2 = {"Lcom/viernes/mobile/data/repository/MedicationRepository;", "", "db", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "(Lcom/viernes/mobile/data/local/ViernesDatabase;)V", "dao", "Lcom/viernes/mobile/data/local/dao/MedicationDao;", "getActiveVerifiedMedications", "", "Lcom/viernes/mobile/domain/model/Medication;", "patientId", "", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getMedicationById", "id", "getMedicationsForPatient", "Lkotlinx/coroutines/flow/Flow;", "saveMedication", "medication", "userId", "", "(Lcom/viernes/mobile/domain/model/Medication;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "verifyAndActivate", "", "medicationId", "confirmedBy", "(JLjava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "toDomain", "Lcom/viernes/mobile/data/local/entity/MedicationEntity;", "toEntity", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
@SourceDebugExtension({"SMAP\nRepositories.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Repositories.kt\ncom/viernes/mobile/data/repository/MedicationRepository\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt\n+ 4 SafeCollector.common.kt\nkotlinx/coroutines/flow/internal/SafeCollector_commonKt\n+ 5 _Collections.kt\nkotlin/collections/CollectionsKt___CollectionsKt\n*L\n1#1,402:1\n49#2:403\n51#2:407\n46#3:404\n51#3:406\n105#4:405\n1549#5:408\n1620#5,3:409\n*S KotlinDebug\n*F\n+ 1 Repositories.kt\ncom/viernes/mobile/data/repository/MedicationRepository\n*L\n88#1:403\n88#1:407\n88#1:404\n88#1:406\n88#1:405\n93#1:408\n93#1:409,3\n*E\n"})
public final class MedicationRepository {
   @NotNull
   private final ViernesDatabase db;
   @NotNull
   private final MedicationDao dao;
   public static final int $stable = 8;

   public MedicationRepository(@NotNull ViernesDatabase db) {
      Intrinsics.checkNotNullParameter(db, "db");
      super();
      this.db = db;
      this.dao = this.db.medicationDao();
   }

   @NotNull
   public final Flow<List<Medication>> getMedicationsForPatient(long patientId) {
      Flow $this$map$iv = this.dao.getMedicationsForPatient(patientId);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new MedicationRepository$getMedicationsForPatient$$inlined$map$1($this$map$iv, this);
   }

   @Nullable
   public final Object getMedicationById(long id, @NotNull Continuation<? super Medication> var3) {
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
               return MedicationRepository.this.getMedicationById(0L, (Continuation)this);
            }
         };
      }

      Object $result = $continuation.result;
      Object var6 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      Object var10000;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            MedicationDao var7 = this.dao;
            $continuation.L$0 = this;
            $continuation.label = 1;
            var10000 = var7.getMedicationById(id, $continuation);
            if (var10000 == var6) {
               return var6;
            }
            break;
         case 1:
            this = (MedicationRepository)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            var10000 = $result;
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      return (MedicationEntity)var10000 != null ? this.toDomain((MedicationEntity)var10000) : null;
   }

   @Nullable
   public final Object getActiveVerifiedMedications(long patientId, @NotNull Continuation<? super List<Medication>> var3) {
      label29: {
         if (var3 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label29;
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
               return MedicationRepository.this.getActiveVerifiedMedications(0L, (Continuation)this);
            }
         };
      }

      Object $result = $continuation.result;
      Object var16 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      Object var10000;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            MedicationDao var17 = this.dao;
            $continuation.L$0 = this;
            $continuation.label = 1;
            var10000 = var17.getActiveVerifiedMedications(patientId, $continuation);
            if (var10000 == var16) {
               return var16;
            }
            break;
         case 1:
            this = (MedicationRepository)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            var10000 = $result;
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      Iterable $this$map$iv = (Iterable)var10000;
      int $i$f$map = 0;
      Collection destination$iv$iv = (Collection)(new ArrayList(CollectionsKt.collectionSizeOrDefault($this$map$iv, 10)));
      int $i$f$mapTo = 0;

      for(Object item$iv$iv : $this$map$iv) {
         MedicationEntity it = (MedicationEntity)item$iv$iv;
         int var12 = 0;
         destination$iv$iv.add(this.toDomain(it));
      }

      return (List)destination$iv$iv;
   }

   @Nullable
   public final Object saveMedication(@NotNull Medication medication, @NotNull String userId, @NotNull Continuation<? super Long> var3) {
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
            long J$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return MedicationRepository.this.saveMedication((Medication)null, (String)null, (Continuation)this);
            }
         };
      }

      long id;
      Object var11;
      label70: {
         label71: {
            Object $result = $continuation.result;
            var11 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
            Object var10000;
            switch ($continuation.label) {
               case 0:
                  ResultKt.throwOnFailure($result);
                  MedicationEntity entity = this.toEntity(medication);
                  MedicationDao var12 = this.dao;
                  $continuation.L$0 = this;
                  $continuation.L$1 = medication;
                  $continuation.L$2 = userId;
                  $continuation.label = 1;
                  var10000 = var12.insert(entity, $continuation);
                  if (var10000 == var11) {
                     return var11;
                  }
                  break;
               case 1:
                  userId = (String)$continuation.L$2;
                  medication = (Medication)$continuation.L$1;
                  this = (MedicationRepository)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  var10000 = $result;
                  break;
               case 2:
                  id = $continuation.J$0;
                  userId = (String)$continuation.L$2;
                  medication = (Medication)$continuation.L$1;
                  this = (MedicationRepository)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  break label71;
               case 3:
                  id = $continuation.J$0;
                  medication = (Medication)$continuation.L$1;
                  this = (MedicationRepository)$continuation.L$0;
                  ResultKt.throwOnFailure($result);
                  break label70;
               case 4:
                  id = $continuation.J$0;
                  ResultKt.throwOnFailure($result);
                  return Boxing.boxLong(id);
               default:
                  throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
            }

            id = ((Number)var10000).longValue();
            String var10005 = medication.getId() == 0L ? "Creación inicial del tratamiento" : "Actualización médica";
            String var10008 = (new Gson()).toJson(medication);
            Intrinsics.checkNotNullExpressionValue(var10008, "toJson(...)");
            TreatmentVersionEntity version = new TreatmentVersionEntity(0L, id, 0, var10005, userId, (String)null, var10008, LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME), 37, (DefaultConstructorMarker)null);
            TreatmentVersionDao var13 = this.db.treatmentVersionDao();
            $continuation.L$0 = this;
            $continuation.L$1 = medication;
            $continuation.L$2 = userId;
            $continuation.J$0 = id;
            $continuation.label = 2;
            if (var13.insert(version, $continuation) == var11) {
               return var11;
            }
         }

         AuditDao var14 = this.db.auditDao();
         AuditRecordEntity var10001 = new AuditRecordEntity(0L, userId, Boxing.boxLong(medication.getPatientId()), "MEDICATION", Boxing.boxLong(id), medication.getId() == 0L ? "CREATE" : "UPDATE", "Medicamento: " + medication.getTranscribedName() + " (Estado: " + medication.getVerificationStatus().getValue() + ")", (String)null, 129, (DefaultConstructorMarker)null);
         $continuation.L$0 = this;
         $continuation.L$1 = medication;
         $continuation.L$2 = null;
         $continuation.J$0 = id;
         $continuation.label = 3;
         if (var14.insert(var10001, $continuation) == var11) {
            return var11;
         }
      }

      SyncQueueDao var15 = this.db.syncQueueDao();
      String var10006 = medication.getId() == 0L ? "INSERT" : "UPDATE";
      String var8 = (new Gson()).toJson(medication);
      Intrinsics.checkNotNullExpressionValue(var8, "toJson(...)");
      String var17 = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
      Intrinsics.checkNotNullExpressionValue(var17, "format(...)");
      SyncQueueEntity var16 = new SyncQueueEntity(0L, "MEDICATION", id, var10006, var8, var17, 0, (String)null, 193, (DefaultConstructorMarker)null);
      $continuation.L$0 = null;
      $continuation.L$1 = null;
      $continuation.J$0 = id;
      $continuation.label = 4;
      if (var15.enqueue(var16, $continuation) == var11) {
         return var11;
      } else {
         return Boxing.boxLong(id);
      }
   }

   // $FF: synthetic method
   public static Object saveMedication$default(MedicationRepository var0, Medication var1, String var2, Continuation var3, int var4, Object var5) {
      if ((var4 & 2) != 0) {
         var2 = "mobile_user";
      }

      return var0.saveMedication(var1, var2, var3);
   }

   @Nullable
   public final Object verifyAndActivate(long medicationId, @NotNull String confirmedBy, @NotNull Continuation<? super Unit> var4) {
      label45: {
         if (var4 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label45;
            }
         }

         $continuation = new ContinuationImpl(var4) {
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
               return MedicationRepository.this.verifyAndActivate(0L, (String)null, (Continuation)this);
            }
         };
      }

      MedicationEntity med;
      Object var8;
      label48: {
         Object $result = $continuation.result;
         var8 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
         Object var10000;
         switch ($continuation.label) {
            case 0:
               ResultKt.throwOnFailure($result);
               MedicationDao var9 = this.dao;
               $continuation.L$0 = this;
               $continuation.L$1 = confirmedBy;
               $continuation.J$0 = medicationId;
               $continuation.label = 1;
               var10000 = var9.getMedicationById(medicationId, $continuation);
               if (var10000 == var8) {
                  return var8;
               }
               break;
            case 1:
               medicationId = $continuation.J$0;
               confirmedBy = (String)$continuation.L$1;
               this = (MedicationRepository)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               var10000 = $result;
               break;
            case 2:
               medicationId = $continuation.J$0;
               med = (MedicationEntity)$continuation.L$2;
               confirmedBy = (String)$continuation.L$1;
               this = (MedicationRepository)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               break label48;
            case 3:
               ResultKt.throwOnFailure($result);
               return Unit.INSTANCE;
            default:
               throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
         }

         MedicationEntity var10 = (MedicationEntity)var10000;
         if (var10 == null) {
            return Unit.INSTANCE;
         }

         med = var10;
         MedicationDao var11 = this.dao;
         String var10002 = VerificationStatus.ACTIVE.getValue();
         $continuation.L$0 = this;
         $continuation.L$1 = confirmedBy;
         $continuation.L$2 = med;
         $continuation.J$0 = medicationId;
         $continuation.label = 2;
         if (var11.updateVerificationStatus(medicationId, var10002, "active", confirmedBy, $continuation) == var8) {
            return var8;
         }
      }

      AuditDao var12 = this.db.auditDao();
      AuditRecordEntity var10001 = new AuditRecordEntity(0L, confirmedBy, Boxing.boxLong(med.getPatientId()), "MEDICATION", Boxing.boxLong(medicationId), "VERIFY_TREATMENT", "Tratamiento verificado y activado clínicamente por " + confirmedBy, (String)null, 129, (DefaultConstructorMarker)null);
      $continuation.L$0 = null;
      $continuation.L$1 = null;
      $continuation.L$2 = null;
      $continuation.label = 3;
      if (var12.insert(var10001, $continuation) == var8) {
         return var8;
      } else {
         return Unit.INSTANCE;
      }
   }

   private final Medication toDomain(MedicationEntity $this$toDomain) {
      return new Medication($this$toDomain.getId(), $this$toDomain.getPatientId(), $this$toDomain.getTranscribedName(), $this$toDomain.getCommercialName(), $this$toDomain.getActiveIngredient(), $this$toDomain.getPharmaceuticalForm(), $this$toDomain.getConcentration(), $this$toDomain.getIndicatedQuantity(), $this$toDomain.getMeasurementUnit(), $this$toDomain.getPrescribedDose(), $this$toDomain.getAdministrationRoute(), $this$toDomain.getTranscribedSchedules(), $this$toDomain.getExactScheduleHours(), $this$toDomain.getSpecialInstructions(), $this$toDomain.getTranscribedFunction(), $this$toDomain.getStartDate(), $this$toDomain.getEndDate(), $this$toDomain.getPrescriberSource(), $this$toDomain.getDocumentRef(), VerificationStatus.Companion.from($this$toDomain.getVerificationStatus()), $this$toDomain.getTreatmentStatus(), $this$toDomain.getLastReviewDate(), $this$toDomain.getCreatedBy(), $this$toDomain.getConfirmedBy(), $this$toDomain.getNotes(), $this$toDomain.getDuplicateWarning(), $this$toDomain.getCreatedAt(), $this$toDomain.getUpdatedAt());
   }

   private final MedicationEntity toEntity(Medication $this$toEntity) {
      MedicationEntity var10000 = new MedicationEntity;
      long var10002 = $this$toEntity.getId();
      long var10003 = $this$toEntity.getPatientId();
      String var10004 = $this$toEntity.getTranscribedName();
      String var10005 = $this$toEntity.getCommercialName();
      String var10006 = $this$toEntity.getActiveIngredient();
      String var10007 = $this$toEntity.getPharmaceuticalForm();
      String var10008 = $this$toEntity.getConcentration();
      String var10009 = $this$toEntity.getIndicatedQuantity();
      String var10010 = $this$toEntity.getMeasurementUnit();
      String var10011 = $this$toEntity.getPrescribedDose();
      String var10012 = $this$toEntity.getAdministrationRoute();
      String var10013 = $this$toEntity.getTranscribedSchedules();
      String var10014 = $this$toEntity.getExactScheduleHours();
      String var10015 = $this$toEntity.getSpecialInstructions();
      String var10016 = $this$toEntity.getTranscribedFunction();
      String var10017 = $this$toEntity.getStartDate();
      String var10018 = $this$toEntity.getEndDate();
      String var10019 = $this$toEntity.getPrescriberSource();
      String var10020 = $this$toEntity.getDocumentRef();
      String var10021 = $this$toEntity.getVerificationStatus().getValue();
      String var10022 = $this$toEntity.getTreatmentStatus();
      String var10023 = $this$toEntity.getLastReviewDate();
      String var10024 = $this$toEntity.getCreatedBy();
      String var10025 = $this$toEntity.getConfirmedBy();
      String var10026 = $this$toEntity.getNotes();
      boolean var10027 = $this$toEntity.getDuplicateWarning();
      String var10028 = $this$toEntity.getCreatedAt();
      if (var10028 == null) {
         var10028 = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
      }

      var10000.<init>(var10002, var10003, var10004, var10005, var10006, var10007, var10008, var10009, var10010, var10011, var10012, var10013, var10014, var10015, var10016, var10017, var10018, var10019, var10020, var10021, var10022, var10023, var10024, var10025, var10026, var10027, var10028, LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
      return var10000;
   }

   // $FF: synthetic method
   public static final Medication access$toDomain(MedicationRepository $this, MedicationEntity $receiver) {
      return $this.toDomain($receiver);
   }
}
