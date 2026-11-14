package com.viernes.mobile.domain.model;

import androidx.compose.runtime.internal.StabilityInferred;
import kotlin.Metadata;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u00002\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0002\b\u0006\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0010\u000b\n\u0002\b4\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001BÍ\u0001\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\u0006\u0010\u0005\u001a\u00020\u0003\u0012\u0006\u0010\u0006\u001a\u00020\u0007\u0012\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\t\u001a\u0004\u0018\u00010\u0007\u0012\u0006\u0010\n\u001a\u00020\u0007\u0012\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0007\u0012\b\b\u0002\u0010\r\u001a\u00020\u000e\u0012\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u0007\u0012\b\b\u0002\u0010\u0011\u001a\u00020\u0012\u0012\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u0014\u001a\u0004\u0018\u00010\u0007\u0012\b\b\u0002\u0010\u0015\u001a\u00020\u0007\u0012\n\b\u0002\u0010\u0016\u001a\u0004\u0018\u00010\u0007\u0012\b\b\u0002\u0010\u0017\u001a\u00020\u0007\u0012\b\b\u0002\u0010\u0018\u001a\u00020\u0012¢\u0006\u0002\u0010\u0019J\t\u00100\u001a\u00020\u0003HÆ\u0003J\t\u00101\u001a\u00020\u000eHÆ\u0003J\u000b\u00102\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u00103\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u00104\u001a\u00020\u0012HÆ\u0003J\u000b\u00105\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u00106\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u00107\u001a\u00020\u0007HÆ\u0003J\u000b\u00108\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u00109\u001a\u00020\u0007HÆ\u0003J\t\u0010:\u001a\u00020\u0012HÆ\u0003J\t\u0010;\u001a\u00020\u0003HÆ\u0003J\t\u0010<\u001a\u00020\u0003HÆ\u0003J\t\u0010=\u001a\u00020\u0007HÆ\u0003J\u000b\u0010>\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010?\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u0010@\u001a\u00020\u0007HÆ\u0003J\u000b\u0010A\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010B\u001a\u0004\u0018\u00010\u0007HÆ\u0003JÙ\u0001\u0010C\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00032\b\b\u0002\u0010\u0006\u001a\u00020\u00072\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\t\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\n\u001a\u00020\u00072\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\r\u001a\u00020\u000e2\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\u0011\u001a\u00020\u00122\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u0014\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\u0015\u001a\u00020\u00072\n\b\u0002\u0010\u0016\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\u0017\u001a\u00020\u00072\b\b\u0002\u0010\u0018\u001a\u00020\u0012HÆ\u0001J\u0013\u0010D\u001a\u00020\u00122\b\u0010E\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010F\u001a\u00020GHÖ\u0001J\t\u0010H\u001a\u00020\u0007HÖ\u0001R\u0013\u0010\u0016\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u001bR\u0013\u0010\u000b\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u001bR\u0013\u0010\f\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001d\u0010\u001bR\u0013\u0010\u0014\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001e\u0010\u001bR\u0011\u0010\n\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001f\u0010\u001bR\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b \u0010!R\u0011\u0010\u0018\u001a\u00020\u0012¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\"R\u0011\u0010\u0005\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b#\u0010!R\u0011\u0010\u0015\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b$\u0010\u001bR\u0013\u0010\u000f\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b%\u0010\u001bR\u0011\u0010\u0011\u001a\u00020\u0012¢\u0006\b\n\u0000\u001a\u0004\b&\u0010\"R\u0013\u0010\u0013\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b'\u0010\u001bR\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b(\u0010!R\u0011\u0010\u0017\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b)\u0010\u001bR\u0013\u0010\t\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b*\u0010\u001bR\u0011\u0010\u0006\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b+\u0010\u001bR\u0013\u0010\b\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b,\u0010\u001bR\u0013\u0010\u0010\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b-\u0010\u001bR\u0011\u0010\r\u001a\u00020\u000e¢\u0006\b\n\u0000\u001a\u0004\b.\u0010/¨\u0006I"},
   d2 = {"Lcom/viernes/mobile/domain/model/Intake;", "", "id", "", "patientId", "medicationId", "scheduledDate", "", "scheduledTime", "period", "doseText", "confirmedAt", "confirmedBy", "status", "Lcom/viernes/mobile/domain/model/IntakeStatus;", "notes", "skipReason", "notificationSent", "", "notificationSentAt", "createdAt", "medicationName", "activeIngredient", "patientName", "isDelayed", "(JJJLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Lcom/viernes/mobile/domain/model/IntakeStatus;Ljava/lang/String;Ljava/lang/String;ZLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Z)V", "getActiveIngredient", "()Ljava/lang/String;", "getConfirmedAt", "getConfirmedBy", "getCreatedAt", "getDoseText", "getId", "()J", "()Z", "getMedicationId", "getMedicationName", "getNotes", "getNotificationSent", "getNotificationSentAt", "getPatientId", "getPatientName", "getPeriod", "getScheduledDate", "getScheduledTime", "getSkipReason", "getStatus", "()Lcom/viernes/mobile/domain/model/IntakeStatus;", "component1", "component10", "component11", "component12", "component13", "component14", "component15", "component16", "component17", "component18", "component19", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "other", "hashCode", "", "toString", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class Intake {
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
   private final IntakeStatus status;
   @Nullable
   private final String notes;
   @Nullable
   private final String skipReason;
   private final boolean notificationSent;
   @Nullable
   private final String notificationSentAt;
   @Nullable
   private final String createdAt;
   @NotNull
   private final String medicationName;
   @Nullable
   private final String activeIngredient;
   @NotNull
   private final String patientName;
   private final boolean isDelayed;
   public static final int $stable;

   public Intake(long id, long patientId, long medicationId, @NotNull String scheduledDate, @Nullable String scheduledTime, @Nullable String period, @NotNull String doseText, @Nullable String confirmedAt, @Nullable String confirmedBy, @NotNull IntakeStatus status, @Nullable String notes, @Nullable String skipReason, boolean notificationSent, @Nullable String notificationSentAt, @Nullable String createdAt, @NotNull String medicationName, @Nullable String activeIngredient, @NotNull String patientName, boolean isDelayed) {
      Intrinsics.checkNotNullParameter(scheduledDate, "scheduledDate");
      Intrinsics.checkNotNullParameter(doseText, "doseText");
      Intrinsics.checkNotNullParameter(status, "status");
      Intrinsics.checkNotNullParameter(medicationName, "medicationName");
      Intrinsics.checkNotNullParameter(patientName, "patientName");
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
      this.medicationName = medicationName;
      this.activeIngredient = activeIngredient;
      this.patientName = patientName;
      this.isDelayed = isDelayed;
   }

   // $FF: synthetic method
   public Intake(long var1, long var3, long var5, String var7, String var8, String var9, String var10, String var11, String var12, IntakeStatus var13, String var14, String var15, boolean var16, String var17, String var18, String var19, String var20, String var21, boolean var22, int var23, DefaultConstructorMarker var24) {
      if ((var23 & 1) != 0) {
         var1 = 0L;
      }

      if ((var23 & 16) != 0) {
         var8 = null;
      }

      if ((var23 & 32) != 0) {
         var9 = null;
      }

      if ((var23 & 128) != 0) {
         var11 = null;
      }

      if ((var23 & 256) != 0) {
         var12 = null;
      }

      if ((var23 & 512) != 0) {
         var13 = IntakeStatus.PENDING;
      }

      if ((var23 & 1024) != 0) {
         var14 = null;
      }

      if ((var23 & 2048) != 0) {
         var15 = null;
      }

      if ((var23 & 4096) != 0) {
         var16 = false;
      }

      if ((var23 & 8192) != 0) {
         var17 = null;
      }

      if ((var23 & 16384) != 0) {
         var18 = null;
      }

      if ((var23 & '耀') != 0) {
         var19 = "";
      }

      if ((var23 & 65536) != 0) {
         var20 = null;
      }

      if ((var23 & 131072) != 0) {
         var21 = "";
      }

      if ((var23 & 262144) != 0) {
         var22 = false;
      }

      this(var1, var3, var5, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21, var22);
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
   public final IntakeStatus getStatus() {
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

   @NotNull
   public final String getMedicationName() {
      return this.medicationName;
   }

   @Nullable
   public final String getActiveIngredient() {
      return this.activeIngredient;
   }

   @NotNull
   public final String getPatientName() {
      return this.patientName;
   }

   public final boolean isDelayed() {
      return this.isDelayed;
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
   public final IntakeStatus component10() {
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
   public final String component16() {
      return this.medicationName;
   }

   @Nullable
   public final String component17() {
      return this.activeIngredient;
   }

   @NotNull
   public final String component18() {
      return this.patientName;
   }

   public final boolean component19() {
      return this.isDelayed;
   }

   @NotNull
   public final Intake copy(long id, long patientId, long medicationId, @NotNull String scheduledDate, @Nullable String scheduledTime, @Nullable String period, @NotNull String doseText, @Nullable String confirmedAt, @Nullable String confirmedBy, @NotNull IntakeStatus status, @Nullable String notes, @Nullable String skipReason, boolean notificationSent, @Nullable String notificationSentAt, @Nullable String createdAt, @NotNull String medicationName, @Nullable String activeIngredient, @NotNull String patientName, boolean isDelayed) {
      Intrinsics.checkNotNullParameter(scheduledDate, "scheduledDate");
      Intrinsics.checkNotNullParameter(doseText, "doseText");
      Intrinsics.checkNotNullParameter(status, "status");
      Intrinsics.checkNotNullParameter(medicationName, "medicationName");
      Intrinsics.checkNotNullParameter(patientName, "patientName");
      return new Intake(id, patientId, medicationId, scheduledDate, scheduledTime, period, doseText, confirmedAt, confirmedBy, status, notes, skipReason, notificationSent, notificationSentAt, createdAt, medicationName, activeIngredient, patientName, isDelayed);
   }

   // $FF: synthetic method
   public static Intake copy$default(Intake var0, long var1, long var3, long var5, String var7, String var8, String var9, String var10, String var11, String var12, IntakeStatus var13, String var14, String var15, boolean var16, String var17, String var18, String var19, String var20, String var21, boolean var22, int var23, Object var24) {
      if ((var23 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var23 & 2) != 0) {
         var3 = var0.patientId;
      }

      if ((var23 & 4) != 0) {
         var5 = var0.medicationId;
      }

      if ((var23 & 8) != 0) {
         var7 = var0.scheduledDate;
      }

      if ((var23 & 16) != 0) {
         var8 = var0.scheduledTime;
      }

      if ((var23 & 32) != 0) {
         var9 = var0.period;
      }

      if ((var23 & 64) != 0) {
         var10 = var0.doseText;
      }

      if ((var23 & 128) != 0) {
         var11 = var0.confirmedAt;
      }

      if ((var23 & 256) != 0) {
         var12 = var0.confirmedBy;
      }

      if ((var23 & 512) != 0) {
         var13 = var0.status;
      }

      if ((var23 & 1024) != 0) {
         var14 = var0.notes;
      }

      if ((var23 & 2048) != 0) {
         var15 = var0.skipReason;
      }

      if ((var23 & 4096) != 0) {
         var16 = var0.notificationSent;
      }

      if ((var23 & 8192) != 0) {
         var17 = var0.notificationSentAt;
      }

      if ((var23 & 16384) != 0) {
         var18 = var0.createdAt;
      }

      if ((var23 & '耀') != 0) {
         var19 = var0.medicationName;
      }

      if ((var23 & 65536) != 0) {
         var20 = var0.activeIngredient;
      }

      if ((var23 & 131072) != 0) {
         var21 = var0.patientName;
      }

      if ((var23 & 262144) != 0) {
         var22 = var0.isDelayed;
      }

      return var0.copy(var1, var3, var5, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21, var22);
   }

   @NotNull
   public String toString() {
      return "Intake(id=" + this.id + ", patientId=" + this.patientId + ", medicationId=" + this.medicationId + ", scheduledDate=" + this.scheduledDate + ", scheduledTime=" + this.scheduledTime + ", period=" + this.period + ", doseText=" + this.doseText + ", confirmedAt=" + this.confirmedAt + ", confirmedBy=" + this.confirmedBy + ", status=" + this.status + ", notes=" + this.notes + ", skipReason=" + this.skipReason + ", notificationSent=" + this.notificationSent + ", notificationSentAt=" + this.notificationSentAt + ", createdAt=" + this.createdAt + ", medicationName=" + this.medicationName + ", activeIngredient=" + this.activeIngredient + ", patientName=" + this.patientName + ", isDelayed=" + this.isDelayed + ")";
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
      result = result * 31 + this.medicationName.hashCode();
      result = result * 31 + (this.activeIngredient == null ? 0 : this.activeIngredient.hashCode());
      result = result * 31 + this.patientName.hashCode();
      result = result * 31 + Boolean.hashCode(this.isDelayed);
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof Intake)) {
         return false;
      } else {
         Intake var2 = (Intake)other;
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
         } else if (this.status != var2.status) {
            return false;
         } else if (!Intrinsics.areEqual(this.notes, var2.notes)) {
            return false;
         } else if (!Intrinsics.areEqual(this.skipReason, var2.skipReason)) {
            return false;
         } else if (this.notificationSent != var2.notificationSent) {
            return false;
         } else if (!Intrinsics.areEqual(this.notificationSentAt, var2.notificationSentAt)) {
            return false;
         } else if (!Intrinsics.areEqual(this.createdAt, var2.createdAt)) {
            return false;
         } else if (!Intrinsics.areEqual(this.medicationName, var2.medicationName)) {
            return false;
         } else if (!Intrinsics.areEqual(this.activeIngredient, var2.activeIngredient)) {
            return false;
         } else if (!Intrinsics.areEqual(this.patientName, var2.patientName)) {
            return false;
         } else {
            return this.isDelayed == var2.isDelayed;
         }
      }
   }
}
