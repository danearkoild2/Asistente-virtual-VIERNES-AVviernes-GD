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
   d1 = {"\u0000*\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0002\b4\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001B\u00ad\u0001\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\n\b\u0002\u0010\u0005\u001a\u0004\u0018\u00010\u0003\u0012\u0006\u0010\u0006\u001a\u00020\u0007\u0012\u0006\u0010\b\u001a\u00020\u0007\u0012\u0006\u0010\t\u001a\u00020\u0007\u0012\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u0007\u0012\u0006\u0010\u000b\u001a\u00020\u0007\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u0007\u0012\b\b\u0002\u0010\u000e\u001a\u00020\u0007\u0012\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u0011\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u0012\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u0007¢\u0006\u0002\u0010\u0014J\t\u0010)\u001a\u00020\u0003HÆ\u0003J\u000b\u0010*\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u0010+\u001a\u00020\u0007HÆ\u0003J\u000b\u0010,\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010-\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010.\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010/\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u00100\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u00101\u001a\u00020\u0003HÆ\u0003J\u0010\u00102\u001a\u0004\u0018\u00010\u0003HÆ\u0003¢\u0006\u0002\u0010\u001cJ\t\u00103\u001a\u00020\u0007HÆ\u0003J\t\u00104\u001a\u00020\u0007HÆ\u0003J\t\u00105\u001a\u00020\u0007HÆ\u0003J\u000b\u00106\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u00107\u001a\u00020\u0007HÆ\u0003J\u000b\u00108\u001a\u0004\u0018\u00010\u0007HÆ\u0003JÀ\u0001\u00109\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\n\b\u0002\u0010\u0005\u001a\u0004\u0018\u00010\u00032\b\b\u0002\u0010\u0006\u001a\u00020\u00072\b\b\u0002\u0010\b\u001a\u00020\u00072\b\b\u0002\u0010\t\u001a\u00020\u00072\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\u000b\u001a\u00020\u00072\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\u000e\u001a\u00020\u00072\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u0011\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u0012\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u0007HÆ\u0001¢\u0006\u0002\u0010:J\u0013\u0010;\u001a\u00020<2\b\u0010=\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010>\u001a\u00020?HÖ\u0001J\t\u0010@\u001a\u00020\u0007HÖ\u0001R\u0013\u0010\u0012\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u0016R\u0013\u0010\n\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0016R\u0016\u0010\u0002\u001a\u00020\u00038\u0006X\u0087\u0004¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0019R\u0013\u0010\r\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0016R\u0015\u0010\u0005\u001a\u0004\u0018\u00010\u0003¢\u0006\n\n\u0002\u0010\u001d\u001a\u0004\b\u001b\u0010\u001cR\u0011\u0010\u0006\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001e\u0010\u0016R\u0013\u0010\u0011\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001f\u0010\u0016R\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b \u0010\u0019R\u0011\u0010\b\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b!\u0010\u0016R\u0013\u0010\u000f\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\"\u0010\u0016R\u0011\u0010\u000b\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b#\u0010\u0016R\u0013\u0010\u0010\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b$\u0010\u0016R\u0011\u0010\t\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b%\u0010\u0016R\u0011\u0010\u000e\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b&\u0010\u0016R\u0013\u0010\u0013\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b'\u0010\u0016R\u0013\u0010\f\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b(\u0010\u0016¨\u0006A"},
   d2 = {"Lcom/viernes/mobile/data/local/entity/RefillEntity;", "", "id", "", "patientId", "medicationId", "medicationName", "", "pharmacyCenter", "scheduledDate", "deadlineDate", "requestedQuantity", "withdrawnQuantity", "measurementUnit", "status", "recipeReference", "responsiblePerson", "notes", "createdAt", "updatedAt", "(JJLjava/lang/Long;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getCreatedAt", "()Ljava/lang/String;", "getDeadlineDate", "getId", "()J", "getMeasurementUnit", "getMedicationId", "()Ljava/lang/Long;", "Ljava/lang/Long;", "getMedicationName", "getNotes", "getPatientId", "getPharmacyCenter", "getRecipeReference", "getRequestedQuantity", "getResponsiblePerson", "getScheduledDate", "getStatus", "getUpdatedAt", "getWithdrawnQuantity", "component1", "component10", "component11", "component12", "component13", "component14", "component15", "component16", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "(JJLjava/lang/Long;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Lcom/viernes/mobile/data/local/entity/RefillEntity;", "equals", "", "other", "hashCode", "", "toString", "app_debug"}
)
@Entity(
   tableName = "refills",
   indices = {@Index({"patientId", "scheduledDate"}), @Index({"medicationId"})},
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
public final class RefillEntity {
   @PrimaryKey(
      autoGenerate = true
   )
   private final long id;
   private final long patientId;
   @Nullable
   private final Long medicationId;
   @NotNull
   private final String medicationName;
   @NotNull
   private final String pharmacyCenter;
   @NotNull
   private final String scheduledDate;
   @Nullable
   private final String deadlineDate;
   @NotNull
   private final String requestedQuantity;
   @Nullable
   private final String withdrawnQuantity;
   @Nullable
   private final String measurementUnit;
   @NotNull
   private final String status;
   @Nullable
   private final String recipeReference;
   @Nullable
   private final String responsiblePerson;
   @Nullable
   private final String notes;
   @Nullable
   private final String createdAt;
   @Nullable
   private final String updatedAt;
   public static final int $stable;

   public RefillEntity(long id, long patientId, @Nullable Long medicationId, @NotNull String medicationName, @NotNull String pharmacyCenter, @NotNull String scheduledDate, @Nullable String deadlineDate, @NotNull String requestedQuantity, @Nullable String withdrawnQuantity, @Nullable String measurementUnit, @NotNull String status, @Nullable String recipeReference, @Nullable String responsiblePerson, @Nullable String notes, @Nullable String createdAt, @Nullable String updatedAt) {
      Intrinsics.checkNotNullParameter(medicationName, "medicationName");
      Intrinsics.checkNotNullParameter(pharmacyCenter, "pharmacyCenter");
      Intrinsics.checkNotNullParameter(scheduledDate, "scheduledDate");
      Intrinsics.checkNotNullParameter(requestedQuantity, "requestedQuantity");
      Intrinsics.checkNotNullParameter(status, "status");
      super();
      this.id = id;
      this.patientId = patientId;
      this.medicationId = medicationId;
      this.medicationName = medicationName;
      this.pharmacyCenter = pharmacyCenter;
      this.scheduledDate = scheduledDate;
      this.deadlineDate = deadlineDate;
      this.requestedQuantity = requestedQuantity;
      this.withdrawnQuantity = withdrawnQuantity;
      this.measurementUnit = measurementUnit;
      this.status = status;
      this.recipeReference = recipeReference;
      this.responsiblePerson = responsiblePerson;
      this.notes = notes;
      this.createdAt = createdAt;
      this.updatedAt = updatedAt;
   }

   // $FF: synthetic method
   public RefillEntity(long var1, long var3, Long var5, String var6, String var7, String var8, String var9, String var10, String var11, String var12, String var13, String var14, String var15, String var16, String var17, String var18, int var19, DefaultConstructorMarker var20) {
      if ((var19 & 1) != 0) {
         var1 = 0L;
      }

      if ((var19 & 4) != 0) {
         var5 = null;
      }

      if ((var19 & 64) != 0) {
         var9 = null;
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
         var16 = null;
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

   @Nullable
   public final Long getMedicationId() {
      return this.medicationId;
   }

   @NotNull
   public final String getMedicationName() {
      return this.medicationName;
   }

   @NotNull
   public final String getPharmacyCenter() {
      return this.pharmacyCenter;
   }

   @NotNull
   public final String getScheduledDate() {
      return this.scheduledDate;
   }

   @Nullable
   public final String getDeadlineDate() {
      return this.deadlineDate;
   }

   @NotNull
   public final String getRequestedQuantity() {
      return this.requestedQuantity;
   }

   @Nullable
   public final String getWithdrawnQuantity() {
      return this.withdrawnQuantity;
   }

   @Nullable
   public final String getMeasurementUnit() {
      return this.measurementUnit;
   }

   @NotNull
   public final String getStatus() {
      return this.status;
   }

   @Nullable
   public final String getRecipeReference() {
      return this.recipeReference;
   }

   @Nullable
   public final String getResponsiblePerson() {
      return this.responsiblePerson;
   }

   @Nullable
   public final String getNotes() {
      return this.notes;
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

   @Nullable
   public final Long component3() {
      return this.medicationId;
   }

   @NotNull
   public final String component4() {
      return this.medicationName;
   }

   @NotNull
   public final String component5() {
      return this.pharmacyCenter;
   }

   @NotNull
   public final String component6() {
      return this.scheduledDate;
   }

   @Nullable
   public final String component7() {
      return this.deadlineDate;
   }

   @NotNull
   public final String component8() {
      return this.requestedQuantity;
   }

   @Nullable
   public final String component9() {
      return this.withdrawnQuantity;
   }

   @Nullable
   public final String component10() {
      return this.measurementUnit;
   }

   @NotNull
   public final String component11() {
      return this.status;
   }

   @Nullable
   public final String component12() {
      return this.recipeReference;
   }

   @Nullable
   public final String component13() {
      return this.responsiblePerson;
   }

   @Nullable
   public final String component14() {
      return this.notes;
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
   public final RefillEntity copy(long id, long patientId, @Nullable Long medicationId, @NotNull String medicationName, @NotNull String pharmacyCenter, @NotNull String scheduledDate, @Nullable String deadlineDate, @NotNull String requestedQuantity, @Nullable String withdrawnQuantity, @Nullable String measurementUnit, @NotNull String status, @Nullable String recipeReference, @Nullable String responsiblePerson, @Nullable String notes, @Nullable String createdAt, @Nullable String updatedAt) {
      Intrinsics.checkNotNullParameter(medicationName, "medicationName");
      Intrinsics.checkNotNullParameter(pharmacyCenter, "pharmacyCenter");
      Intrinsics.checkNotNullParameter(scheduledDate, "scheduledDate");
      Intrinsics.checkNotNullParameter(requestedQuantity, "requestedQuantity");
      Intrinsics.checkNotNullParameter(status, "status");
      return new RefillEntity(id, patientId, medicationId, medicationName, pharmacyCenter, scheduledDate, deadlineDate, requestedQuantity, withdrawnQuantity, measurementUnit, status, recipeReference, responsiblePerson, notes, createdAt, updatedAt);
   }

   // $FF: synthetic method
   public static RefillEntity copy$default(RefillEntity var0, long var1, long var3, Long var5, String var6, String var7, String var8, String var9, String var10, String var11, String var12, String var13, String var14, String var15, String var16, String var17, String var18, int var19, Object var20) {
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
         var6 = var0.medicationName;
      }

      if ((var19 & 16) != 0) {
         var7 = var0.pharmacyCenter;
      }

      if ((var19 & 32) != 0) {
         var8 = var0.scheduledDate;
      }

      if ((var19 & 64) != 0) {
         var9 = var0.deadlineDate;
      }

      if ((var19 & 128) != 0) {
         var10 = var0.requestedQuantity;
      }

      if ((var19 & 256) != 0) {
         var11 = var0.withdrawnQuantity;
      }

      if ((var19 & 512) != 0) {
         var12 = var0.measurementUnit;
      }

      if ((var19 & 1024) != 0) {
         var13 = var0.status;
      }

      if ((var19 & 2048) != 0) {
         var14 = var0.recipeReference;
      }

      if ((var19 & 4096) != 0) {
         var15 = var0.responsiblePerson;
      }

      if ((var19 & 8192) != 0) {
         var16 = var0.notes;
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
      return "RefillEntity(id=" + this.id + ", patientId=" + this.patientId + ", medicationId=" + this.medicationId + ", medicationName=" + this.medicationName + ", pharmacyCenter=" + this.pharmacyCenter + ", scheduledDate=" + this.scheduledDate + ", deadlineDate=" + this.deadlineDate + ", requestedQuantity=" + this.requestedQuantity + ", withdrawnQuantity=" + this.withdrawnQuantity + ", measurementUnit=" + this.measurementUnit + ", status=" + this.status + ", recipeReference=" + this.recipeReference + ", responsiblePerson=" + this.responsiblePerson + ", notes=" + this.notes + ", createdAt=" + this.createdAt + ", updatedAt=" + this.updatedAt + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + Long.hashCode(this.patientId);
      result = result * 31 + (this.medicationId == null ? 0 : this.medicationId.hashCode());
      result = result * 31 + this.medicationName.hashCode();
      result = result * 31 + this.pharmacyCenter.hashCode();
      result = result * 31 + this.scheduledDate.hashCode();
      result = result * 31 + (this.deadlineDate == null ? 0 : this.deadlineDate.hashCode());
      result = result * 31 + this.requestedQuantity.hashCode();
      result = result * 31 + (this.withdrawnQuantity == null ? 0 : this.withdrawnQuantity.hashCode());
      result = result * 31 + (this.measurementUnit == null ? 0 : this.measurementUnit.hashCode());
      result = result * 31 + this.status.hashCode();
      result = result * 31 + (this.recipeReference == null ? 0 : this.recipeReference.hashCode());
      result = result * 31 + (this.responsiblePerson == null ? 0 : this.responsiblePerson.hashCode());
      result = result * 31 + (this.notes == null ? 0 : this.notes.hashCode());
      result = result * 31 + (this.createdAt == null ? 0 : this.createdAt.hashCode());
      result = result * 31 + (this.updatedAt == null ? 0 : this.updatedAt.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof RefillEntity)) {
         return false;
      } else {
         RefillEntity var2 = (RefillEntity)other;
         if (this.id != var2.id) {
            return false;
         } else if (this.patientId != var2.patientId) {
            return false;
         } else if (!Intrinsics.areEqual(this.medicationId, var2.medicationId)) {
            return false;
         } else if (!Intrinsics.areEqual(this.medicationName, var2.medicationName)) {
            return false;
         } else if (!Intrinsics.areEqual(this.pharmacyCenter, var2.pharmacyCenter)) {
            return false;
         } else if (!Intrinsics.areEqual(this.scheduledDate, var2.scheduledDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.deadlineDate, var2.deadlineDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.requestedQuantity, var2.requestedQuantity)) {
            return false;
         } else if (!Intrinsics.areEqual(this.withdrawnQuantity, var2.withdrawnQuantity)) {
            return false;
         } else if (!Intrinsics.areEqual(this.measurementUnit, var2.measurementUnit)) {
            return false;
         } else if (!Intrinsics.areEqual(this.status, var2.status)) {
            return false;
         } else if (!Intrinsics.areEqual(this.recipeReference, var2.recipeReference)) {
            return false;
         } else if (!Intrinsics.areEqual(this.responsiblePerson, var2.responsiblePerson)) {
            return false;
         } else if (!Intrinsics.areEqual(this.notes, var2.notes)) {
            return false;
         } else if (!Intrinsics.areEqual(this.createdAt, var2.createdAt)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.updatedAt, var2.updatedAt);
         }
      }
   }
}
