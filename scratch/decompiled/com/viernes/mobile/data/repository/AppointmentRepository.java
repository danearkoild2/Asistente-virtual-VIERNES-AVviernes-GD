package com.viernes.mobile.data.repository;

import androidx.compose.runtime.internal.StabilityInferred;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.local.dao.AppointmentDao;
import com.viernes.mobile.data.local.dao.AuditDao;
import com.viernes.mobile.data.local.entity.AppointmentEntity;
import com.viernes.mobile.data.local.entity.AuditRecordEntity;
import com.viernes.mobile.domain.model.AppointmentStatus;
import com.viernes.mobile.domain.model.MedicalAppointment;
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
   d1 = {"\u0000>\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004J\u001a\u0010\u0007\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\n0\t0\b2\u0006\u0010\u000b\u001a\u00020\fJ \u0010\r\u001a\u00020\f2\u0006\u0010\u000e\u001a\u00020\n2\b\b\u0002\u0010\u000f\u001a\u00020\u0010H\u0086@¢\u0006\u0002\u0010\u0011J\f\u0010\u0012\u001a\u00020\n*\u00020\u0013H\u0002J\f\u0010\u0014\u001a\u00020\u0013*\u00020\nH\u0002R\u000e\u0010\u0005\u001a\u00020\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\u0015"},
   d2 = {"Lcom/viernes/mobile/data/repository/AppointmentRepository;", "", "db", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "(Lcom/viernes/mobile/data/local/ViernesDatabase;)V", "dao", "Lcom/viernes/mobile/data/local/dao/AppointmentDao;", "getAppointmentsForPatient", "Lkotlinx/coroutines/flow/Flow;", "", "Lcom/viernes/mobile/domain/model/MedicalAppointment;", "patientId", "", "saveAppointment", "appointment", "userId", "", "(Lcom/viernes/mobile/domain/model/MedicalAppointment;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "toDomain", "Lcom/viernes/mobile/data/local/entity/AppointmentEntity;", "toEntity", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
@SourceDebugExtension({"SMAP\nAdditionalRepositories.kt\nKotlin\n*S Kotlin\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/AppointmentRepository\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt\n+ 4 SafeCollector.common.kt\nkotlinx/coroutines/flow/internal/SafeCollector_commonKt\n*L\n1#1,402:1\n49#2:403\n51#2:407\n46#3:404\n51#3:406\n105#4:405\n*S KotlinDebug\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/AppointmentRepository\n*L\n17#1:403\n17#1:407\n17#1:404\n17#1:406\n17#1:405\n*E\n"})
public final class AppointmentRepository {
   @NotNull
   private final ViernesDatabase db;
   @NotNull
   private final AppointmentDao dao;
   public static final int $stable = 8;

   public AppointmentRepository(@NotNull ViernesDatabase db) {
      Intrinsics.checkNotNullParameter(db, "db");
      super();
      this.db = db;
      this.dao = this.db.appointmentDao();
   }

   @NotNull
   public final Flow<List<MedicalAppointment>> getAppointmentsForPatient(long patientId) {
      Flow $this$map$iv = this.dao.getAppointmentsForPatient(patientId);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new AppointmentRepository$getAppointmentsForPatient$$inlined$map$1($this$map$iv, this);
   }

   @Nullable
   public final Object saveAppointment(@NotNull MedicalAppointment appointment, @NotNull String userId, @NotNull Continuation<? super Long> var3) {
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
               return AppointmentRepository.this.saveAppointment((MedicalAppointment)null, (String)null, (Continuation)this);
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
            AppointmentEntity entity = this.toEntity(appointment);
            AppointmentDao var10 = this.dao;
            $continuation.L$0 = this;
            $continuation.L$1 = appointment;
            $continuation.L$2 = userId;
            $continuation.label = 1;
            var10000 = var10.insert(entity, $continuation);
            if (var10000 == var9) {
               return var9;
            }
            break;
         case 1:
            userId = (String)$continuation.L$2;
            appointment = (MedicalAppointment)$continuation.L$1;
            this = (AppointmentRepository)$continuation.L$0;
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
      AuditRecordEntity var10001 = new AuditRecordEntity(0L, userId, Boxing.boxLong(appointment.getPatientId()), "APPOINTMENT", Boxing.boxLong(id), appointment.getId() == 0L ? "CREATE" : "UPDATE", "Cita médica: " + appointment.getSpecialtyOrDoctor() + " en " + appointment.getMedicalCenter(), (String)null, 129, (DefaultConstructorMarker)null);
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
   public static Object saveAppointment$default(AppointmentRepository var0, MedicalAppointment var1, String var2, Continuation var3, int var4, Object var5) {
      if ((var4 & 2) != 0) {
         var2 = "mobile_user";
      }

      return var0.saveAppointment(var1, var2, var3);
   }

   private final MedicalAppointment toDomain(AppointmentEntity $this$toDomain) {
      return new MedicalAppointment($this$toDomain.getId(), $this$toDomain.getPatientId(), $this$toDomain.getAppointmentDate(), $this$toDomain.getAppointmentTime(), $this$toDomain.getSpecialtyOrDoctor(), $this$toDomain.getMedicalCenter(), $this$toDomain.getAddressOrLocation(), $this$toDomain.getConsultationReason(), $this$toDomain.getPreparationInstructions(), $this$toDomain.getDocumentAttachments(), AppointmentStatus.Companion.from($this$toDomain.getStatus()), $this$toDomain.getNotesPostVisit(), $this$toDomain.getFollowUpDate(), $this$toDomain.getCreatedBy(), $this$toDomain.getCreatedAt(), $this$toDomain.getUpdatedAt());
   }

   private final AppointmentEntity toEntity(MedicalAppointment $this$toEntity) {
      AppointmentEntity var10000 = new AppointmentEntity;
      long var10002 = $this$toEntity.getId();
      long var10003 = $this$toEntity.getPatientId();
      String var10004 = $this$toEntity.getAppointmentDate();
      String var10005 = $this$toEntity.getAppointmentTime();
      String var10006 = $this$toEntity.getSpecialtyOrDoctor();
      String var10007 = $this$toEntity.getMedicalCenter();
      String var10008 = $this$toEntity.getAddressOrLocation();
      String var10009 = $this$toEntity.getConsultationReason();
      String var10010 = $this$toEntity.getPreparationInstructions();
      String var10011 = $this$toEntity.getDocumentAttachments();
      String var10012 = $this$toEntity.getStatus().getValue();
      String var10013 = $this$toEntity.getNotesPostVisit();
      String var10014 = $this$toEntity.getFollowUpDate();
      String var10015 = $this$toEntity.getCreatedBy();
      String var10016 = $this$toEntity.getCreatedAt();
      if (var10016 == null) {
         var10016 = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
      }

      var10000.<init>(var10002, var10003, var10004, var10005, var10006, var10007, var10008, var10009, var10010, var10011, var10012, var10013, var10014, var10015, var10016, LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
      return var10000;
   }

   // $FF: synthetic method
   public static final MedicalAppointment access$toDomain(AppointmentRepository $this, AppointmentEntity $receiver) {
      return $this.toDomain($receiver);
   }
}
