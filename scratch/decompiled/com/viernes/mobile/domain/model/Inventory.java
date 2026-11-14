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
   d1 = {"\u00002\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0003\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0010\u0006\n\u0002\b!\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001Bw\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\u0006\u0010\u0005\u001a\u00020\u0003\u0012\n\b\u0002\u0010\u0006\u001a\u0004\u0018\u00010\u0007\u0012\u0006\u0010\b\u001a\u00020\u0007\u0012\b\b\u0002\u0010\t\u001a\u00020\n\u0012\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u0007\u0012\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u0007\u0012\b\b\u0002\u0010\u000f\u001a\u00020\u0007¢\u0006\u0002\u0010\u0010J\t\u0010\u001f\u001a\u00020\u0003HÆ\u0003J\u000b\u0010 \u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u0010!\u001a\u00020\u0007HÆ\u0003J\t\u0010\"\u001a\u00020\u0003HÆ\u0003J\t\u0010#\u001a\u00020\u0003HÆ\u0003J\u000b\u0010$\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\t\u0010%\u001a\u00020\u0007HÆ\u0003J\t\u0010&\u001a\u00020\nHÆ\u0003J\u000b\u0010'\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010(\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u000b\u0010)\u001a\u0004\u0018\u00010\u0007HÆ\u0003J\u0081\u0001\u0010*\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00032\n\b\u0002\u0010\u0006\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\b\u001a\u00020\u00072\b\b\u0002\u0010\t\u001a\u00020\n2\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u00072\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u00072\b\b\u0002\u0010\u000f\u001a\u00020\u0007HÆ\u0001J\u0013\u0010+\u001a\u00020,2\b\u0010-\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010.\u001a\u00020/HÖ\u0001J\t\u00100\u001a\u00020\u0007HÖ\u0001R\u0011\u0010\t\u001a\u00020\n¢\u0006\b\n\u0000\u001a\u0004\b\u0011\u0010\u0012R\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0013\u0010\u0014R\u0011\u0010\b\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u0016R\u0013\u0010\u000b\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0016R\u0011\u0010\u0005\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0014R\u0011\u0010\u000f\u001a\u00020\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u0019\u0010\u0016R\u0013\u0010\r\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0016R\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u001b\u0010\u0014R\u0013\u0010\u0006\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u0016R\u0013\u0010\f\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001d\u0010\u0016R\u0013\u0010\u000e\u001a\u0004\u0018\u00010\u0007¢\u0006\b\n\u0000\u001a\u0004\b\u001e\u0010\u0016¨\u00061"},
   d2 = {"Lcom/viernes/mobile/domain/model/Inventory;", "", "id", "", "patientId", "medicationId", "presentation", "", "inventoryUnit", "availableQuantity", "", "lastReconciliationDate", "reconciledBy", "notes", "updatedAt", "medicationName", "(JJJLjava/lang/String;Ljava/lang/String;DLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getAvailableQuantity", "()D", "getId", "()J", "getInventoryUnit", "()Ljava/lang/String;", "getLastReconciliationDate", "getMedicationId", "getMedicationName", "getNotes", "getPatientId", "getPresentation", "getReconciledBy", "getUpdatedAt", "component1", "component10", "component11", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "", "other", "hashCode", "", "toString", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class Inventory {
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
   @NotNull
   private final String medicationName;
   public static final int $stable;

   public Inventory(long id, long patientId, long medicationId, @Nullable String presentation, @NotNull String inventoryUnit, double availableQuantity, @Nullable String lastReconciliationDate, @Nullable String reconciledBy, @Nullable String notes, @Nullable String updatedAt, @NotNull String medicationName) {
      Intrinsics.checkNotNullParameter(inventoryUnit, "inventoryUnit");
      Intrinsics.checkNotNullParameter(medicationName, "medicationName");
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
      this.medicationName = medicationName;
   }

   // $FF: synthetic method
   public Inventory(long var1, long var3, long var5, String var7, String var8, double var9, String var11, String var12, String var13, String var14, String var15, int var16, DefaultConstructorMarker var17) {
      if ((var16 & 1) != 0) {
         var1 = 0L;
      }

      if ((var16 & 8) != 0) {
         var7 = null;
      }

      if ((var16 & 32) != 0) {
         var9 = (double)0.0F;
      }

      if ((var16 & 64) != 0) {
         var11 = null;
      }

      if ((var16 & 128) != 0) {
         var12 = null;
      }

      if ((var16 & 256) != 0) {
         var13 = null;
      }

      if ((var16 & 512) != 0) {
         var14 = null;
      }

      if ((var16 & 1024) != 0) {
         var15 = "";
      }

      this(var1, var3, var5, var7, var8, var9, var11, var12, var13, var14, var15);
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

   @NotNull
   public final String getMedicationName() {
      return this.medicationName;
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
   public final String component11() {
      return this.medicationName;
   }

   @NotNull
   public final Inventory copy(long id, long patientId, long medicationId, @Nullable String presentation, @NotNull String inventoryUnit, double availableQuantity, @Nullable String lastReconciliationDate, @Nullable String reconciledBy, @Nullable String notes, @Nullable String updatedAt, @NotNull String medicationName) {
      Intrinsics.checkNotNullParameter(inventoryUnit, "inventoryUnit");
      Intrinsics.checkNotNullParameter(medicationName, "medicationName");
      return new Inventory(id, patientId, medicationId, presentation, inventoryUnit, availableQuantity, lastReconciliationDate, reconciledBy, notes, updatedAt, medicationName);
   }

   // $FF: synthetic method
   public static Inventory copy$default(Inventory var0, long var1, long var3, long var5, String var7, String var8, double var9, String var11, String var12, String var13, String var14, String var15, int var16, Object var17) {
      if ((var16 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var16 & 2) != 0) {
         var3 = var0.patientId;
      }

      if ((var16 & 4) != 0) {
         var5 = var0.medicationId;
      }

      if ((var16 & 8) != 0) {
         var7 = var0.presentation;
      }

      if ((var16 & 16) != 0) {
         var8 = var0.inventoryUnit;
      }

      if ((var16 & 32) != 0) {
         var9 = var0.availableQuantity;
      }

      if ((var16 & 64) != 0) {
         var11 = var0.lastReconciliationDate;
      }

      if ((var16 & 128) != 0) {
         var12 = var0.reconciledBy;
      }

      if ((var16 & 256) != 0) {
         var13 = var0.notes;
      }

      if ((var16 & 512) != 0) {
         var14 = var0.updatedAt;
      }

      if ((var16 & 1024) != 0) {
         var15 = var0.medicationName;
      }

      return var0.copy(var1, var3, var5, var7, var8, var9, var11, var12, var13, var14, var15);
   }

   @NotNull
   public String toString() {
      return "Inventory(id=" + this.id + ", patientId=" + this.patientId + ", medicationId=" + this.medicationId + ", presentation=" + this.presentation + ", inventoryUnit=" + this.inventoryUnit + ", availableQuantity=" + this.availableQuantity + ", lastReconciliationDate=" + this.lastReconciliationDate + ", reconciledBy=" + this.reconciledBy + ", notes=" + this.notes + ", updatedAt=" + this.updatedAt + ", medicationName=" + this.medicationName + ")";
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
      result = result * 31 + this.medicationName.hashCode();
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof Inventory)) {
         return false;
      } else {
         Inventory var2 = (Inventory)other;
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
         } else if (!Intrinsics.areEqual(this.updatedAt, var2.updatedAt)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.medicationName, var2.medicationName);
         }
      }
   }
}
