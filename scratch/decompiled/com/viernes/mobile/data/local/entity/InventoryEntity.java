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
   d1 = {"\u00002\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0010\u0006\n\u0002\b\u001e\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001Bm\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\u0006\u0010\u0005\u001a\u00020\u0003\u0012\n\b\u0002\u0010\u0006\u001a\u0004\u0018\u00010\u0007\u0012\u0006\u0010\b\u001a\u00020\u0007\u0012\b\b\u0002\u0010\t\u001a\u00020\n\u0012\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u0007¢\u0006\u0002\u0010\u000fJ\t\u0010\u001d\u001a\u00020\u0003HÆ\u0003J\u000b\u0010\u001e\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u0010\u001f\u001a\u00020\u0003HÆ\u0003J\t\u0010 \u001a\u00020\u0003HÆ\u0003J\u000b\u0010!\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u0010\"\u001a\u00020\u0007HÆ\u0003J\t\u0010#\u001a\u00020\nHÆ\u0003J\u000b\u0010$\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010%\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010&\u001a\u0004\u0018\u00010\u0007HÆ\u0003Jw\u0010'\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00032\n\b\u0002\u0010\u0006\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\b\u001a\u00020\u00072\b\b\u0002\u0010\t\u001a\u00020\n2\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u0007HÆ\u0001J\u0013\u0010(\u001a\u00020)2\b\u0010*\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010+\u001a\u00020,HÖ\u0001J\t\u0010-\u001a\u00020\u0007HÖ\u0001R\u0011\u0010\t\u001a\u00020\n¢\u0006\b\n\u0000\u001a\u0004\b\u0010\u0010\u0011R\u0016\u0010\u0002\u001a\u00020\u00038\u0006X\u0087\u0004¢\u0006\b\n\u0000\u001a\u0004\b\u0012\u0010\u0013R\u0011\u0010\b\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0014\u0010\u0015R\u0013\u0010\u000b\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0016\u0010\u0015R\u0011\u0010\u0005\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0013R\u0013\u0010\r\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0015R\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0019\u0010\u0013R\u0013\u0010\u0006\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0015R\u0013\u0010\f\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001b\u0010\u0015R\u0013\u0010\u000e\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u0015¨\u0006."},
   d2 = {"Lcom/viernes/mobile/data/local/entity/InventoryEntity;", "", "id", "", "patientId", "medicationId", "presentation", "", "inventoryUnit", "availableQuantity", "", "lastReconciliationDate", "reconciledBy", "notes", "updatedAt", "(JJJLjava/lang/String;Ljava/lang/String;DLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getAvailableQuantity", "()D", "getId", "()J", "getInventoryUnit", "()Ljava/lang/String;", "getLastReconciliationDate", "getMedicationId", "getNotes", "getPatientId", "getPresentation", "getReconciledBy", "getUpdatedAt", "component1", "component10", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "", "other", "hashCode", "", "toString", "app_debug"}
)
@Entity(
   tableName = "inventory",
   indices = {@Index(
   value = {"patientId", "medicationId"},
   unique = true
), @Index({"patientId"})},
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
public final class InventoryEntity {
   @PrimaryKey(
      autoGenerate = true
   )
   private final long id;
   private final long patientId;
   private final long medicationId;
   @Nullable
   private final String presentation;
   @NotNull
   private final String inventoryUnit;
   private final double availableQuantity;
   @Nullable
   private final String lastReconciliationDate;
   @Nullable
   private final String reconciledBy;
   @Nullable
   private final String notes;
   @Nullable
   private final String updatedAt;
   public static final int $stable;

   public InventoryEntity(long id, long patientId, long medicationId, @Nullable String presentation, @NotNull String inventoryUnit, double availableQuantity, @Nullable String lastReconciliationDate, @Nullable String reconciledBy, @Nullable String notes, @Nullable String updatedAt) {
      Intrinsics.checkNotNullParameter(inventoryUnit, "inventoryUnit");
      super();
      this.id = id;
      this.patientId = patientId;
      this.medicationId = medicationId;
      this.presentation = presentation;
      this.inventoryUnit = inventoryUnit;
      this.availableQuantity = availableQuantity;
      this.lastReconciliationDate = lastReconciliationDate;
      this.reconciledBy = reconciledBy;
      this.notes = notes;
      this.updatedAt = updatedAt;
   }

   // $FF: synthetic method
   public InventoryEntity(long var1, long var3, long var5, String var7, String var8, double var9, String var11, String var12, String var13, String var14, int var15, DefaultConstructorMarker var16) {
      if ((var15 & 1) != 0) {
         var1 = 0L;
      }

      if ((var15 & 8) != 0) {
         var7 = null;
      }

      if ((var15 & 32) != 0) {
         var9 = (double)0.0F;
      }

      if ((var15 & 64) != 0) {
         var11 = null;
      }

      if ((var15 & 128) != 0) {
         var12 = null;
      }

      if ((var15 & 256) != 0) {
         var13 = null;
      }

      if ((var15 & 512) != 0) {
         var14 = null;
      }

      this(var1, var3, var5, var7, var8, var9, var11, var12, var13, var14);
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

   @Nullable
   public final String getPresentation() {
      return this.presentation;
   }

   @NotNull
   public final String getInventoryUnit() {
      return this.inventoryUnit;
   }

   public final double getAvailableQuantity() {
      return this.availableQuantity;
   }

   @Nullable
   public final String getLastReconciliationDate() {
      return this.lastReconciliationDate;
   }

   @Nullable
   public final String getReconciledBy() {
      return this.reconciledBy;
   }

   @Nullable
   public final String getNotes() {
      return this.notes;
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

   public final long component3() {
      return this.medicationId;
   }

   @Nullable
   public final String component4() {
      return this.presentation;
   }

   @NotNull
   public final String component5() {
      return this.inventoryUnit;
   }

   public final double component6() {
      return this.availableQuantity;
   }

   @Nullable
   public final String component7() {
      return this.lastReconciliationDate;
   }

   @Nullable
   public final String component8() {
      return this.reconciledBy;
   }

   @Nullable
   public final String component9() {
      return this.notes;
   }

   @Nullable
   public final String component10() {
      return this.updatedAt;
   }

   @NotNull
   public final InventoryEntity copy(long id, long patientId, long medicationId, @Nullable String presentation, @NotNull String inventoryUnit, double availableQuantity, @Nullable String lastReconciliationDate, @Nullable String reconciledBy, @Nullable String notes, @Nullable String updatedAt) {
      Intrinsics.checkNotNullParameter(inventoryUnit, "inventoryUnit");
      return new InventoryEntity(id, patientId, medicationId, presentation, inventoryUnit, availableQuantity, lastReconciliationDate, reconciledBy, notes, updatedAt);
   }

   // $FF: synthetic method
   public static InventoryEntity copy$default(InventoryEntity var0, long var1, long var3, long var5, String var7, String var8, double var9, String var11, String var12, String var13, String var14, int var15, Object var16) {
      if ((var15 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var15 & 2) != 0) {
         var3 = var0.patientId;
      }

      if ((var15 & 4) != 0) {
         var5 = var0.medicationId;
      }

      if ((var15 & 8) != 0) {
         var7 = var0.presentation;
      }

      if ((var15 & 16) != 0) {
         var8 = var0.inventoryUnit;
      }

      if ((var15 & 32) != 0) {
         var9 = var0.availableQuantity;
      }

      if ((var15 & 64) != 0) {
         var11 = var0.lastReconciliationDate;
      }

      if ((var15 & 128) != 0) {
         var12 = var0.reconciledBy;
      }

      if ((var15 & 256) != 0) {
         var13 = var0.notes;
      }

      if ((var15 & 512) != 0) {
         var14 = var0.updatedAt;
      }

      return var0.copy(var1, var3, var5, var7, var8, var9, var11, var12, var13, var14);
   }

   @NotNull
   public String toString() {
      return "InventoryEntity(id=" + this.id + ", patientId=" + this.patientId + ", medicationId=" + this.medicationId + ", presentation=" + this.presentation + ", inventoryUnit=" + this.inventoryUnit + ", availableQuantity=" + this.availableQuantity + ", lastReconciliationDate=" + this.lastReconciliationDate + ", reconciledBy=" + this.reconciledBy + ", notes=" + this.notes + ", updatedAt=" + this.updatedAt + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + Long.hashCode(this.patientId);
      result = result * 31 + Long.hashCode(this.medicationId);
      result = result * 31 + (this.presentation == null ? 0 : this.presentation.hashCode());
      result = result * 31 + this.inventoryUnit.hashCode();
      result = result * 31 + Double.hashCode(this.availableQuantity);
      result = result * 31 + (this.lastReconciliationDate == null ? 0 : this.lastReconciliationDate.hashCode());
      result = result * 31 + (this.reconciledBy == null ? 0 : this.reconciledBy.hashCode());
      result = result * 31 + (this.notes == null ? 0 : this.notes.hashCode());
      result = result * 31 + (this.updatedAt == null ? 0 : this.updatedAt.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof InventoryEntity)) {
         return false;
      } else {
         InventoryEntity var2 = (InventoryEntity)other;
         if (this.id != var2.id) {
            return false;
         } else if (this.patientId != var2.patientId) {
            return false;
         } else if (this.medicationId != var2.medicationId) {
            return false;
         } else if (!Intrinsics.areEqual(this.presentation, var2.presentation)) {
            return false;
         } else if (!Intrinsics.areEqual(this.inventoryUnit, var2.inventoryUnit)) {
            return false;
         } else if (Double.compare(this.availableQuantity, var2.availableQuantity) != 0) {
            return false;
         } else if (!Intrinsics.areEqual(this.lastReconciliationDate, var2.lastReconciliationDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.reconciledBy, var2.reconciledBy)) {
            return false;
         } else if (!Intrinsics.areEqual(this.notes, var2.notes)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.updatedAt, var2.updatedAt);
         }
      }
   }
}
