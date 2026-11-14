package com.viernes.mobile.data.local.entity;

import androidx.compose.runtime.internal.StabilityInferred;
import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;
import kotlin.Metadata;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000*\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b2\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001B«\u0001\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\u0006\u0010\u0005\u001a\u00020\u0006\u0012\u0006\u0010\u0007\u001a\u00020\u0006\u0012\u0006\u0010\b\u001a\u00020\u0006\u0012\u0006\u0010\t\u001a\u00020\u0006\u0012\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u0006\u0012\b\b\u0002\u0010\u000e\u001a\u00020\u0006\u0012\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u0006\u0012\b\b\u0002\u0010\u0011\u001a\u00020\u0006\u0012\n\b\u0002\u0010\u0012\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u0006¢\u0006\u0002\u0010\u0014J\t\u0010'\u001a\u00020\u0003HÆ\u0003J\u000b\u0010(\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\t\u0010)\u001a\u00020\u0006HÆ\u0003J\u000b\u0010*\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010+\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\t\u0010,\u001a\u00020\u0006HÆ\u0003J\u000b\u0010-\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010.\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\t\u0010/\u001a\u00020\u0003HÆ\u0003J\t\u00100\u001a\u00020\u0006HÆ\u0003J\t\u00101\u001a\u00020\u0006HÆ\u0003J\t\u00102\u001a\u00020\u0006HÆ\u0003J\t\u00103\u001a\u00020\u0006HÆ\u0003J\u000b\u00104\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u00105\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u00106\u001a\u0004\u0018\u00010\u0006HÆ\u0003J¹\u0001\u00107\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00062\b\b\u0002\u0010\u0007\u001a\u00020\u00062\b\b\u0002\u0010\b\u001a\u00020\u00062\b\b\u0002\u0010\t\u001a\u00020\u00062\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u00062\b\b\u0002\u0010\u000e\u001a\u00020\u00062\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u00062\b\b\u0002\u0010\u0011\u001a\u00020\u00062\n\b\u0002\u0010\u0012\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u0006HÆ\u0001J\u0013\u00108\u001a\u0002092\b\u0010:\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010;\u001a\u00020<HÖ\u0001J\t\u0010=\u001a\u00020\u0006HÖ\u0001R\u0013\u0010\n\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u0016R\u0011\u0010\u0005\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0016R\u0011\u0010\u0007\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0016R\u0013\u0010\u000b\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u0019\u0010\u0016R\u0013\u0010\u0012\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0016R\u0011\u0010\u0011\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u001b\u0010\u0016R\u0013\u0010\r\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u0016R\u0013\u0010\u0010\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u001d\u0010\u0016R\u0016\u0010\u0002\u001a\u00020\u00038\u0006X\u0087\u0004¢\u0006\b\n\u0000\u001a\u0004\b\u001e\u0010\u001fR\u0011\u0010\t\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b \u0010\u0016R\u0013\u0010\u000f\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b!\u0010\u0016R\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\"\u0010\u001fR\u0013\u0010\f\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b#\u0010\u0016R\u0011\u0010\b\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b$\u0010\u0016R\u0011\u0010\u000e\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b%\u0010\u0016R\u0013\u0010\u0013\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b&\u0010\u0016¨\u0006>"},
   d2 = {"Lcom/viernes/mobile/data/local/entity/AppointmentEntity;", "", "id", "", "patientId", "appointmentDate", "", "appointmentTime", "specialtyOrDoctor", "medicalCenter", "addressOrLocation", "consultationReason", "preparationInstructions", "documentAttachments", "status", "notesPostVisit", "followUpDate", "createdBy", "createdAt", "updatedAt", "(JJLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getAddressOrLocation", "()Ljava/lang/String;", "getAppointmentDate", "getAppointmentTime", "getConsultationReason", "getCreatedAt", "getCreatedBy", "getDocumentAttachments", "getFollowUpDate", "getId", "()J", "getMedicalCenter", "getNotesPostVisit", "getPatientId", "getPreparationInstructions", "getSpecialtyOrDoctor", "getStatus", "getUpdatedAt", "component1", "component10", "component11", "component12", "component13", "component14", "component15", "component16", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "", "other", "hashCode", "", "toString", "app_debug"}
)
@Entity(
   tableName = "appointments",
   indices = {@Index({"patientId", "appointmentDate"})},
   foreignKeys = {@ForeignKey(
   entity = PatientEntity.class,
   parentColumns = {"id"},
   childColumns = {"patientId"},
   onDelete = 5
)}
)
@StabilityInferred(
   parameters = 1
)
public final class AppointmentEntity {
   @PrimaryKey(
      autoGenerate = true
   )
   private final long id;
   private final long patientId;
   @NotNull
   private final String appointmentDate;
   @NotNull
   private final String appointmentTime;
   @NotNull
   private final String specialtyOrDoctor;
   @NotNull
   private final String medicalCenter;
   @Nullable
   private final String addressOrLocation;
   @Nullable
   private final String consultationReason;
   @Nullable
   private final String preparationInstructions;
   @Nullable
   private final String documentAttachments;
   @NotNull
   private final String status;
   @Nullable
   private final String notesPostVisit;
   @Nullable
   private final String followUpDate;
   @NotNull
   private final String createdBy;
   @Nullable
   private final String createdAt;
   @Nullable
   private final String updatedAt;
   public static final int $stable;

   public AppointmentEntity(long id, long patientId, @NotNull String appointmentDate, @NotNull String appointmentTime, @NotNull String specialtyOrDoctor, @NotNull String medicalCenter, @Nullable String addressOrLocation, @Nullable String consultationReason, @Nullable String preparationInstructions, @Nullable String documentAttachments, @NotNull String status, @Nullable String notesPostVisit, @Nullable String followUpDate, @NotNull String createdBy, @Nullable String createdAt, @Nullable String updatedAt) {
      Intrinsics.checkNotNullParameter(appointmentDate, "appointmentDate");
      Intrinsics.checkNotNullParameter(appointmentTime, "appointmentTime");
      Intrinsics.checkNotNullParameter(specialtyOrDoctor, "specialtyOrDoctor");
      Intrinsics.checkNotNullParameter(medicalCenter, "medicalCenter");
      Intrinsics.checkNotNullParameter(status, "status");
      Intrinsics.checkNotNullParameter(createdBy, "createdBy");
      super();
      this.id = id;
      this.patientId = patientId;
      this.appointmentDate = appointmentDate;
      this.appointmentTime = appointmentTime;
      this.specialtyOrDoctor = specialtyOrDoctor;
      this.medicalCenter = medicalCenter;
      this.addressOrLocation = addressOrLocation;
      this.consultationReason = consultationReason;
      this.preparationInstructions = preparationInstructions;
      this.documentAttachments = documentAttachments;
      this.status = status;
      this.notesPostVisit = notesPostVisit;
      this.followUpDate = followUpDate;
      this.createdBy = createdBy;
      this.createdAt = createdAt;
      this.updatedAt = updatedAt;
   }

   // $FF: synthetic method
   public AppointmentEntity(long var1, long var3, String var5, String var6, String var7, String var8, String var9, String var10, String var11, String var12, String var13, String var14, String var15, String var16, String var17, String var18, int var19, DefaultConstructorMarker var20) {
      if ((var19 & 1) != 0) {
         var1 = 0L;
      }

      if ((var19 & 64) != 0) {
         var9 = null;
      }

      if ((var19 & 128) != 0) {
         var10 = null;
      }

      if ((var19 & 256) != 0) {
         var11 = null;
      }

      if ((var19 & 512) != 0) {
         var12 = null;
      }

      if ((var19 & 1024) != 0) {
         var13 = "SCHEDULED";
      }

      if ((var19 & 2048) != 0) {
         var14 = null;
      }

      if ((var19 & 4096) != 0) {
         var15 = null;
      }

      if ((var19 & 8192) != 0) {
         var16 = "system";
      }

      if ((var19 & 16384) != 0) {
         var17 = null;
      }

      if ((var19 & '耀') != 0) {
         var18 = null;
      }

      this(var1, var3, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18);
   }

   public final long getId() {
      return this.id;
   }

   public final long getPatientId() {
      return this.patientId;
   }

   @NotNull
   public final String getAppointmentDate() {
      return this.appointmentDate;
   }

   @NotNull
   public final String getAppointmentTime() {
      return this.appointmentTime;
   }

   @NotNull
   public final String getSpecialtyOrDoctor() {
      return this.specialtyOrDoctor;
   }

   @NotNull
   public final String getMedicalCenter() {
      return this.medicalCenter;
   }

   @Nullable
   public final String getAddressOrLocation() {
      return this.addressOrLocation;
   }

   @Nullable
   public final String getConsultationReason() {
      return this.consultationReason;
   }

   @Nullable
   public final String getPreparationInstructions() {
      return this.preparationInstructions;
   }

   @Nullable
   public final String getDocumentAttachments() {
      return this.documentAttachments;
   }

   @NotNull
   public final String getStatus() {
      return this.status;
   }

   @Nullable
   public final String getNotesPostVisit() {
      return this.notesPostVisit;
   }

   @Nullable
   public final String getFollowUpDate() {
      return this.followUpDate;
   }

   @NotNull
   public final String getCreatedBy() {
      return this.createdBy;
   }

   @Nullable
   public final String getCreatedAt() {
      return this.createdAt;
   }

   @Nullable
   public final String getUpdatedAt() {
      return this.updatedAt;
   }

   public final long component1() {
      return this.id;
   }

   public final long component2() {
      return this.patientId;
   }

   @NotNull
   public final String component3() {
      return this.appointmentDate;
   }

   @NotNull
   public final String component4() {
      return this.appointmentTime;
   }

   @NotNull
   public final String component5() {
      return this.specialtyOrDoctor;
   }

   @NotNull
   public final String component6() {
      return this.medicalCenter;
   }

   @Nullable
   public final String component7() {
      return this.addressOrLocation;
   }

   @Nullable
   public final String component8() {
      return this.consultationReason;
   }

   @Nullable
   public final String component9() {
      return this.preparationInstructions;
   }

   @Nullable
   public final String component10() {
      return this.documentAttachments;
   }

   @NotNull
   public final String component11() {
      return this.status;
   }

   @Nullable
   public final String component12() {
      return this.notesPostVisit;
   }

   @Nullable
   public final String component13() {
      return this.followUpDate;
   }

   @NotNull
   public final String component14() {
      return this.createdBy;
   }

   @Nullable
   public final String component15() {
      return this.createdAt;
   }

   @Nullable
   public final String component16() {
      return this.updatedAt;
   }

   @NotNull
   public final AppointmentEntity copy(long id, long patientId, @NotNull String appointmentDate, @NotNull String appointmentTime, @NotNull String specialtyOrDoctor, @NotNull String medicalCenter, @Nullable String addressOrLocation, @Nullable String consultationReason, @Nullable String preparationInstructions, @Nullable String documentAttachments, @NotNull String status, @Nullable String notesPostVisit, @Nullable String followUpDate, @NotNull String createdBy, @Nullable String createdAt, @Nullable String updatedAt) {
      Intrinsics.checkNotNullParameter(appointmentDate, "appointmentDate");
      Intrinsics.checkNotNullParameter(appointmentTime, "appointmentTime");
      Intrinsics.checkNotNullParameter(specialtyOrDoctor, "specialtyOrDoctor");
      Intrinsics.checkNotNullParameter(medicalCenter, "medicalCenter");
      Intrinsics.checkNotNullParameter(status, "status");
      Intrinsics.checkNotNullParameter(createdBy, "createdBy");
      return new AppointmentEntity(id, patientId, appointmentDate, appointmentTime, specialtyOrDoctor, medicalCenter, addressOrLocation, consultationReason, preparationInstructions, documentAttachments, status, notesPostVisit, followUpDate, createdBy, createdAt, updatedAt);
   }

   // $FF: synthetic method
   public static AppointmentEntity copy$default(AppointmentEntity var0, long var1, long var3, String var5, String var6, String var7, String var8, String var9, String var10, String var11, String var12, String var13, String var14, String var15, String var16, String var17, String var18, int var19, Object var20) {
      if ((var19 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var19 & 2) != 0) {
         var3 = var0.patientId;
      }

      if ((var19 & 4) != 0) {
         var5 = var0.appointmentDate;
      }

      if ((var19 & 8) != 0) {
         var6 = var0.appointmentTime;
      }

      if ((var19 & 16) != 0) {
         var7 = var0.specialtyOrDoctor;
      }

      if ((var19 & 32) != 0) {
         var8 = var0.medicalCenter;
      }

      if ((var19 & 64) != 0) {
         var9 = var0.addressOrLocation;
      }

      if ((var19 & 128) != 0) {
         var10 = var0.consultationReason;
      }

      if ((var19 & 256) != 0) {
         var11 = var0.preparationInstructions;
      }

      if ((var19 & 512) != 0) {
         var12 = var0.documentAttachments;
      }

      if ((var19 & 1024) != 0) {
         var13 = var0.status;
      }

      if ((var19 & 2048) != 0) {
         var14 = var0.notesPostVisit;
      }

      if ((var19 & 4096) != 0) {
         var15 = var0.followUpDate;
      }

      if ((var19 & 8192) != 0) {
         var16 = var0.createdBy;
      }

      if ((var19 & 16384) != 0) {
         var17 = var0.createdAt;
      }

      if ((var19 & '耀') != 0) {
         var18 = var0.updatedAt;
      }

      return var0.copy(var1, var3, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18);
   }

   @NotNull
   public String toString() {
      return "AppointmentEntity(id=" + this.id + ", patientId=" + this.patientId + ", appointmentDate=" + this.appointmentDate + ", appointmentTime=" + this.appointmentTime + ", specialtyOrDoctor=" + this.specialtyOrDoctor + ", medicalCenter=" + this.medicalCenter + ", addressOrLocation=" + this.addressOrLocation + ", consultationReason=" + this.consultationReason + ", preparationInstructions=" + this.preparationInstructions + ", documentAttachments=" + this.documentAttachments + ", status=" + this.status + ", notesPostVisit=" + this.notesPostVisit + ", followUpDate=" + this.followUpDate + ", createdBy=" + this.createdBy + ", createdAt=" + this.createdAt + ", updatedAt=" + this.updatedAt + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + Long.hashCode(this.patientId);
      result = result * 31 + this.appointmentDate.hashCode();
      result = result * 31 + this.appointmentTime.hashCode();
      result = result * 31 + this.specialtyOrDoctor.hashCode();
      result = result * 31 + this.medicalCenter.hashCode();
      result = result * 31 + (this.addressOrLocation == null ? 0 : this.addressOrLocation.hashCode());
      result = result * 31 + (this.consultationReason == null ? 0 : this.consultationReason.hashCode());
      result = result * 31 + (this.preparationInstructions == null ? 0 : this.preparationInstructions.hashCode());
      result = result * 31 + (this.documentAttachments == null ? 0 : this.documentAttachments.hashCode());
      result = result * 31 + this.status.hashCode();
      result = result * 31 + (this.notesPostVisit == null ? 0 : this.notesPostVisit.hashCode());
      result = result * 31 + (this.followUpDate == null ? 0 : this.followUpDate.hashCode());
      result = result * 31 + this.createdBy.hashCode();
      result = result * 31 + (this.createdAt == null ? 0 : this.createdAt.hashCode());
      result = result * 31 + (this.updatedAt == null ? 0 : this.updatedAt.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof AppointmentEntity)) {
         return false;
      } else {
         AppointmentEntity var2 = (AppointmentEntity)other;
         if (this.id != var2.id) {
            return false;
         } else if (this.patientId != var2.patientId) {
            return false;
         } else if (!Intrinsics.areEqual(this.appointmentDate, var2.appointmentDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.appointmentTime, var2.appointmentTime)) {
            return false;
         } else if (!Intrinsics.areEqual(this.specialtyOrDoctor, var2.specialtyOrDoctor)) {
            return false;
         } else if (!Intrinsics.areEqual(this.medicalCenter, var2.medicalCenter)) {
            return false;
         } else if (!Intrinsics.areEqual(this.addressOrLocation, var2.addressOrLocation)) {
            return false;
         } else if (!Intrinsics.areEqual(this.consultationReason, var2.consultationReason)) {
            return false;
         } else if (!Intrinsics.areEqual(this.preparationInstructions, var2.preparationInstructions)) {
            return false;
         } else if (!Intrinsics.areEqual(this.documentAttachments, var2.documentAttachments)) {
            return false;
         } else if (!Intrinsics.areEqual(this.status, var2.status)) {
            return false;
         } else if (!Intrinsics.areEqual(this.notesPostVisit, var2.notesPostVisit)) {
            return false;
         } else if (!Intrinsics.areEqual(this.followUpDate, var2.followUpDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.createdBy, var2.createdBy)) {
            return false;
         } else if (!Intrinsics.areEqual(this.createdAt, var2.createdAt)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.updatedAt, var2.updatedAt);
         }
      }
   }
}
