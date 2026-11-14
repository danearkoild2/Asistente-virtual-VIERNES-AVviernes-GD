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
   d1 = {"\u0000*\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0002\b\t\n\u0002\u0010\u000b\n\u0002\b(\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001B£\u0001\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\u0006\u0010\u0005\u001a\u00020\u0003\u0012\u0006\u0010\u0006\u001a\u00020\u0007\u0012\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\t\u001a\u0004\u0018\u00010\u0007\u0012\u0006\u0010\n\u001a\u00020\u0007\u0012\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0007\u0012\b\b\u0002\u0010\r\u001a\u00020\u0007\u0012\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u0007\u0012\b\b\u0002\u0010\u0010\u001a\u00020\u0011\u0012\n\b\u0002\u0010\u0012\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u0007¢\u0006\u0002\u0010\u0014J\t\u0010'\u001a\u00020\u0003HÆ\u0003J\t\u0010(\u001a\u00020\u0007HÆ\u0003J\u000b\u0010)\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010*\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u0010+\u001a\u00020\u0011HÆ\u0003J\u000b\u0010,\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010-\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u0010.\u001a\u00020\u0003HÆ\u0003J\t\u0010/\u001a\u00020\u0003HÆ\u0003J\t\u00100\u001a\u00020\u0007HÆ\u0003J\u000b\u00101\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u00102\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u00103\u001a\u00020\u0007HÆ\u0003J\u000b\u00104\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u00105\u001a\u0004\u0018\u00010\u0007HÆ\u0003J¯\u0001\u00106\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00032\b\b\u0002\u0010\u0006\u001a\u00020\u00072\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\t\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\n\u001a\u00020\u00072\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\r\u001a\u00020\u00072\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\u0010\u001a\u00020\u00112\n\b\u0002\u0010\u0012\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u0007HÆ\u0001J\u0013\u00107\u001a\u00020\u00112\b\u00108\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u00109\u001a\u00020:HÖ\u0001J\t\u0010;\u001a\u00020\u0007HÖ\u0001R\u0013\u0010\u000b\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u0016R\u0013\u0010\f\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0016R\u0013\u0010\u0013\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0016R\u0011\u0010\n\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0019\u0010\u0016R\u0016\u0010\u0002\u001a\u00020\u00038\u0006X\u0087\u0004¢\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u001bR\u0011\u0010\u0005\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u001bR\u0013\u0010\u000e\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001d\u0010\u0016R\u0011\u0010\u0010\u001a\u00020\u0011¢\u0006\b\n\u0000\u001a\u0004\b\u001e\u0010\u001fR\u0013\u0010\u0012\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b \u0010\u0016R\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b!\u0010\u001bR\u0013\u0010\t\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\"\u0010\u0016R\u0011\u0010\u0006\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b#\u0010\u0016R\u0013\u0010\b\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b$\u0010\u0016R\u0013\u0010\u000f\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b%\u0010\u0016R\u0011\u0010\r\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b&\u0010\u0016¨\u0006<"},
   d2 = {"Lcom/viernes/mobile/data/local/entity/IntakeEntity;", "", "id", "", "patientId", "medicationId", "scheduledDate", "", "scheduledTime", "period", "doseText", "confirmedAt", "confirmedBy", "status", "notes", "skipReason", "notificationSent", "", "notificationSentAt", "createdAt", "(JJJLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;ZLjava/lang/String;Ljava/lang/String;)V", "getConfirmedAt", "()Ljava/lang/String;", "getConfirmedBy", "getCreatedAt", "getDoseText", "getId", "()J", "getMedicationId", "getNotes", "getNotificationSent", "()Z", "getNotificationSentAt", "getPatientId", "getPeriod", "getScheduledDate", "getScheduledTime", "getSkipReason", "getStatus", "component1", "component10", "component11", "component12", "component13", "component14", "component15", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "other", "hashCode", "", "toString", "app_debug"}
)
@Entity(
   tableName = "intakes",
   indices = {@Index({"patientId", "scheduledDate"}), @Index({"medicationId"}), @Index({"status"})},
   foreignKeys = {@ForeignKey(
   entity = PatientEntity.class,
   parentColumns = {"id"},
   childColumns = {"patientId"},
   onDelete = 5
), @ForeignKey(
   entity = MedicationEntity.class,
   parentColumns = {"id"},
   childColumns = {"medicationId"},
   onDelete = 5
)}
)
@StabilityInferred(
   parameters = 1
)
public final class IntakeEntity {
   @PrimaryKey(
      autoGenerate = true
   )
   private final long id;
   private final long patientId;
   private final long medicationId;
   @NotNull
   private final String scheduledDate;
   @Nullable
   private final String scheduledTime;
   @Nullable
   private final String period;
   @NotNull
   private final String doseText;
   @Nullable
   private final String confirmedAt;
   @Nullable
   private final String confirmedBy;
   @NotNull
   private final String status;
   @Nullable
   private final String notes;
   @Nullable
   private final String skipReason;
   private final boolean notificationSent;
   @Nullable
   private final String notificationSentAt;
   @Nullable
   private final String createdAt;
   public static final int $stable;

   public IntakeEntity(long id, long patientId, long medicationId, @NotNull String scheduledDate, @Nullable String scheduledTime, @Nullable String period, @NotNull String doseText, @Nullable String confirmedAt, @Nullable String confirmedBy, @NotNull String status, @Nullable String notes, @Nullable String skipReason, boolean notificationSent, @Nullable String notificationSentAt, @Nullable String createdAt) {
      Intrinsics.checkNotNullParameter(scheduledDate, "scheduledDate");
      Intrinsics.checkNotNullParameter(doseText, "doseText");
      Intrinsics.checkNotNullParameter(status, "status");
      super();
      this.id = id;
      this.patientId = patientId;
      this.medicationId = medicationId;
      this.scheduledDate = scheduledDate;
      this.scheduledTime = scheduledTime;
      this.period = period;
      this.doseText = doseText;
      this.confirmedAt = confirmedAt;
      this.confirmedBy = confirmedBy;
      this.status = status;
      this.notes = notes;
      this.skipReason = skipReason;
      this.notificationSent = notificationSent;
      this.notificationSentAt = notificationSentAt;
      this.createdAt = createdAt;
   }

   // $FF: synthetic method
   public IntakeEntity(long var1, long var3, long var5, String var7, String var8, String var9, String var10, String var11, String var12, String var13, String var14, String var15, boolean var16, String var17, String var18, int var19, DefaultConstructorMarker var20) {
      if ((var19 & 1) != 0) {
         var1 = 0L;
      }

      if ((var19 & 16) != 0) {
         var8 = null;
      }

      if ((var19 & 32) != 0) {
         var9 = null;
      }

      if ((var19 & 128) != 0) {
         var11 = null;
      }

      if ((var19 & 256) != 0) {
         var12 = null;
      }

      if ((var19 & 512) != 0) {
         var13 = "PENDING";
      }

      if ((var19 & 1024) != 0) {
         var14 = null;
      }

      if ((var19 & 2048) != 0) {
         var15 = null;
      }

      if ((var19 & 4096) != 0) {
         var16 = false;
      }

      if ((var19 & 8192) != 0) {
         var17 = null;
      }

      if ((var19 & 16384) != 0) {
         var18 = null;
      }

      this(var1, var3, var5, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18);
   }

   public final long getId() {
      return this.id;
   }

   public final long getPatientId() {
      return this.patientId;
   }

   public final long getMedicationId() {
      return this.medicationId;
   }

   @NotNull
   public final String getScheduledDate() {
      return this.scheduledDate;
   }

   @Nullable
   public final String getScheduledTime() {
      return this.scheduledTime;
   }

   @Nullable
   public final String getPeriod() {
      return this.period;
   }

   @NotNull
   public final String getDoseText() {
      return this.doseText;
   }

   @Nullable
   public final String getConfirmedAt() {
      return this.confirmedAt;
   }

   @Nullable
   public final String getConfirmedBy() {
      return this.confirmedBy;
   }

   @NotNull
   public final String getStatus() {
      return this.status;
   }

   @Nullable
   public final String getNotes() {
      return this.notes;
   }

   @Nullable
   public final String getSkipReason() {
      return this.skipReason;
   }

   public final boolean getNotificationSent() {
      return this.notificationSent;
   }

   @Nullable
   public final String getNotificationSentAt() {
      return this.notificationSentAt;
   }

   @Nullable
   public final String getCreatedAt() {
      return this.createdAt;
   }

   public final long component1() {
      return this.id;
   }

   public final long component2() {
      return this.patientId;
   }

   public final long component3() {
      return this.medicationId;
   }

   @NotNull
   public final String component4() {
      return this.scheduledDate;
   }

   @Nullable
   public final String component5() {
      return this.scheduledTime;
   }

   @Nullable
   public final String component6() {
      return this.period;
   }

   @NotNull
   public final String component7() {
      return this.doseText;
   }

   @Nullable
   public final String component8() {
      return this.confirmedAt;
   }

   @Nullable
   public final String component9() {
      return this.confirmedBy;
   }

   @NotNull
   public final String component10() {
      return this.status;
   }

   @Nullable
   public final String component11() {
      return this.notes;
   }

   @Nullable
   public final String component12() {
      return this.skipReason;
   }

   public final boolean component13() {
      return this.notificationSent;
   }

   @Nullable
   public final String component14() {
      return this.notificationSentAt;
   }

   @Nullable
   public final String component15() {
      return this.createdAt;
   }

   @NotNull
   public final IntakeEntity copy(long id, long patientId, long medicationId, @NotNull String scheduledDate, @Nullable String scheduledTime, @Nullable String period, @NotNull String doseText, @Nullable String confirmedAt, @Nullable String confirmedBy, @NotNull String status, @Nullable String notes, @Nullable String skipReason, boolean notificationSent, @Nullable String notificationSentAt, @Nullable String createdAt) {
      Intrinsics.checkNotNullParameter(scheduledDate, "scheduledDate");
      Intrinsics.checkNotNullParameter(doseText, "doseText");
      Intrinsics.checkNotNullParameter(status, "status");
      return new IntakeEntity(id, patientId, medicationId, scheduledDate, scheduledTime, period, doseText, confirmedAt, confirmedBy, status, notes, skipReason, notificationSent, notificationSentAt, createdAt);
   }

   // $FF: synthetic method
   public static IntakeEntity copy$default(IntakeEntity var0, long var1, long var3, long var5, String var7, String var8, String var9, String var10, String var11, String var12, String var13, String var14, String var15, boolean var16, String var17, String var18, int var19, Object var20) {
      if ((var19 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var19 & 2) != 0) {
         var3 = var0.patientId;
      }

      if ((var19 & 4) != 0) {
         var5 = var0.medicationId;
      }

      if ((var19 & 8) != 0) {
         var7 = var0.scheduledDate;
      }

      if ((var19 & 16) != 0) {
         var8 = var0.scheduledTime;
      }

      if ((var19 & 32) != 0) {
         var9 = var0.period;
      }

      if ((var19 & 64) != 0) {
         var10 = var0.doseText;
      }

      if ((var19 & 128) != 0) {
         var11 = var0.confirmedAt;
      }

      if ((var19 & 256) != 0) {
         var12 = var0.confirmedBy;
      }

      if ((var19 & 512) != 0) {
         var13 = var0.status;
      }

      if ((var19 & 1024) != 0) {
         var14 = var0.notes;
      }

      if ((var19 & 2048) != 0) {
         var15 = var0.skipReason;
      }

      if ((var19 & 4096) != 0) {
         var16 = var0.notificationSent;
      }

      if ((var19 & 8192) != 0) {
         var17 = var0.notificationSentAt;
      }

      if ((var19 & 16384) != 0) {
         var18 = var0.createdAt;
      }

      return var0.copy(var1, var3, var5, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18);
   }

   @NotNull
   public String toString() {
      return "IntakeEntity(id=" + this.id + ", patientId=" + this.patientId + ", medicationId=" + this.medicationId + ", scheduledDate=" + this.scheduledDate + ", scheduledTime=" + this.scheduledTime + ", period=" + this.period + ", doseText=" + this.doseText + ", confirmedAt=" + this.confirmedAt + ", confirmedBy=" + this.confirmedBy + ", status=" + this.status + ", notes=" + this.notes + ", skipReason=" + this.skipReason + ", notificationSent=" + this.notificationSent + ", notificationSentAt=" + this.notificationSentAt + ", createdAt=" + this.createdAt + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + Long.hashCode(this.patientId);
      result = result * 31 + Long.hashCode(this.medicationId);
      result = result * 31 + this.scheduledDate.hashCode();
      result = result * 31 + (this.scheduledTime == null ? 0 : this.scheduledTime.hashCode());
      result = result * 31 + (this.period == null ? 0 : this.period.hashCode());
      result = result * 31 + this.doseText.hashCode();
      result = result * 31 + (this.confirmedAt == null ? 0 : this.confirmedAt.hashCode());
      result = result * 31 + (this.confirmedBy == null ? 0 : this.confirmedBy.hashCode());
      result = result * 31 + this.status.hashCode();
      result = result * 31 + (this.notes == null ? 0 : this.notes.hashCode());
      result = result * 31 + (this.skipReason == null ? 0 : this.skipReason.hashCode());
      result = result * 31 + Boolean.hashCode(this.notificationSent);
      result = result * 31 + (this.notificationSentAt == null ? 0 : this.notificationSentAt.hashCode());
      result = result * 31 + (this.createdAt == null ? 0 : this.createdAt.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof IntakeEntity)) {
         return false;
      } else {
         IntakeEntity var2 = (IntakeEntity)other;
         if (this.id != var2.id) {
            return false;
         } else if (this.patientId != var2.patientId) {
            return false;
         } else if (this.medicationId != var2.medicationId) {
            return false;
         } else if (!Intrinsics.areEqual(this.scheduledDate, var2.scheduledDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.scheduledTime, var2.scheduledTime)) {
            return false;
         } else if (!Intrinsics.areEqual(this.period, var2.period)) {
            return false;
         } else if (!Intrinsics.areEqual(this.doseText, var2.doseText)) {
            return false;
         } else if (!Intrinsics.areEqual(this.confirmedAt, var2.confirmedAt)) {
            return false;
         } else if (!Intrinsics.areEqual(this.confirmedBy, var2.confirmedBy)) {
            return false;
         } else if (!Intrinsics.areEqual(this.status, var2.status)) {
            return false;
         } else if (!Intrinsics.areEqual(this.notes, var2.notes)) {
            return false;
         } else if (!Intrinsics.areEqual(this.skipReason, var2.skipReason)) {
            return false;
         } else if (this.notificationSent != var2.notificationSent) {
            return false;
         } else if (!Intrinsics.areEqual(this.notificationSentAt, var2.notificationSentAt)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.createdAt, var2.createdAt);
         }
      }
   }
}
