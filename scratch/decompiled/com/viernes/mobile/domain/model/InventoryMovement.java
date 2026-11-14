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
   d1 = {"\u00008\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0006\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u001d\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001B_\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\u0006\u0010\u0005\u001a\u00020\u0003\u0012\u0006\u0010\u0006\u001a\u00020\u0003\u0012\b\b\u0002\u0010\u0007\u001a\u00020\b\u0012\u0006\u0010\t\u001a\u00020\n\u0012\u0006\u0010\u000b\u001a\u00020\n\u0012\u0006\u0010\f\u001a\u00020\r\u0012\b\b\u0002\u0010\u000e\u001a\u00020\r\u0012\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\r¢\u0006\u0002\u0010\u0010J\t\u0010\u001f\u001a\u00020\u0003HÆ\u0003J\u000b\u0010 \u001a\u0004\u0018\u00010\rHÆ\u0003J\t\u0010!\u001a\u00020\u0003HÆ\u0003J\t\u0010\"\u001a\u00020\u0003HÆ\u0003J\t\u0010#\u001a\u00020\u0003HÆ\u0003J\t\u0010$\u001a\u00020\bHÆ\u0003J\t\u0010%\u001a\u00020\nHÆ\u0003J\t\u0010&\u001a\u00020\nHÆ\u0003J\t\u0010'\u001a\u00020\rHÆ\u0003J\t\u0010(\u001a\u00020\rHÆ\u0003Jo\u0010)\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00032\b\b\u0002\u0010\u0006\u001a\u00020\u00032\b\b\u0002\u0010\u0007\u001a\u00020\b2\b\b\u0002\u0010\t\u001a\u00020\n2\b\b\u0002\u0010\u000b\u001a\u00020\n2\b\b\u0002\u0010\f\u001a\u00020\r2\b\b\u0002\u0010\u000e\u001a\u00020\r2\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\rHÆ\u0001J\u0013\u0010*\u001a\u00020+2\b\u0010,\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010-\u001a\u00020.HÖ\u0001J\t\u0010/\u001a\u00020\rHÖ\u0001R\u0011\u0010\u000b\u001a\u00020\n¢\u0006\b\n\u0000\u001a\u0004\b\u0011\u0010\u0012R\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0013\u0010\u0014R\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u0014R\u0011\u0010\u0006\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0016\u0010\u0014R\u0013\u0010\u000f\u001a\u0004\u0018\u00010\r¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0018R\u0011\u0010\u0007\u001a\u00020\b¢\u0006\b\n\u0000\u001a\u0004\b\u0019\u0010\u001aR\u0011\u0010\u0005\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u001b\u0010\u0014R\u0011\u0010\t\u001a\u00020\n¢\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u0012R\u0011\u0010\f\u001a\u00020\r¢\u0006\b\n\u0000\u001a\u0004\b\u001d\u0010\u0018R\u0011\u0010\u000e\u001a\u00020\r¢\u0006\b\n\u0000\u001a\u0004\b\u001e\u0010\u0018¨\u00060"},
   d2 = {"Lcom/viernes/mobile/domain/model/InventoryMovement;", "", "id", "", "inventoryId", "patientId", "medicationId", "movementType", "Lcom/viernes/mobile/domain/model/MovementType;", "quantity", "", "balanceAfter", "reason", "", "userResponsible", "movementDate", "(JJJJLcom/viernes/mobile/domain/model/MovementType;DDLjava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getBalanceAfter", "()D", "getId", "()J", "getInventoryId", "getMedicationId", "getMovementDate", "()Ljava/lang/String;", "getMovementType", "()Lcom/viernes/mobile/domain/model/MovementType;", "getPatientId", "getQuantity", "getReason", "getUserResponsible", "component1", "component10", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "", "other", "hashCode", "", "toString", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class InventoryMovement {
   private final long id;
   private final long inventoryId;
   private final long patientId;
   private final long medicationId;
   @NotNull
   private final MovementType movementType;
   private final double quantity;
   private final double balanceAfter;
   @NotNull
   private final String reason;
   @NotNull
   private final String userResponsible;
   @Nullable
   private final String movementDate;
   public static final int $stable;

   public InventoryMovement(long id, long inventoryId, long patientId, long medicationId, @NotNull MovementType movementType, double quantity, double balanceAfter, @NotNull String reason, @NotNull String userResponsible, @Nullable String movementDate) {
      Intrinsics.checkNotNullParameter(movementType, "movementType");
      Intrinsics.checkNotNullParameter(reason, "reason");
      Intrinsics.checkNotNullParameter(userResponsible, "userResponsible");
      super();
      this.id = id;
      this.inventoryId = inventoryId;
      this.patientId = patientId;
      this.medicationId = medicationId;
      this.movementType = movementType;
      this.quantity = quantity;
      this.balanceAfter = balanceAfter;
      this.reason = reason;
      this.userResponsible = userResponsible;
      this.movementDate = movementDate;
   }

   // $FF: synthetic method
   public InventoryMovement(long var1, long var3, long var5, long var7, MovementType var9, double var10, double var12, String var14, String var15, String var16, int var17, DefaultConstructorMarker var18) {
      if ((var17 & 1) != 0) {
         var1 = 0L;
      }

      if ((var17 & 16) != 0) {
         var9 = MovementType.MANUAL_ADJUSTMENT;
      }

      if ((var17 & 256) != 0) {
         var15 = "system";
      }

      if ((var17 & 512) != 0) {
         var16 = null;
      }

      this(var1, var3, var5, var7, var9, var10, var12, var14, var15, var16);
   }

   public final long getId() {
      return this.id;
   }

   public final long getInventoryId() {
      return this.inventoryId;
   }

   public final long getPatientId() {
      return this.patientId;
   }

   public final long getMedicationId() {
      return this.medicationId;
   }

   @NotNull
   public final MovementType getMovementType() {
      return this.movementType;
   }

   public final double getQuantity() {
      return this.quantity;
   }

   public final double getBalanceAfter() {
      return this.balanceAfter;
   }

   @NotNull
   public final String getReason() {
      return this.reason;
   }

   @NotNull
   public final String getUserResponsible() {
      return this.userResponsible;
   }

   @Nullable
   public final String getMovementDate() {
      return this.movementDate;
   }

   public final long component1() {
      return this.id;
   }

   public final long component2() {
      return this.inventoryId;
   }

   public final long component3() {
      return this.patientId;
   }

   public final long component4() {
      return this.medicationId;
   }

   @NotNull
   public final MovementType component5() {
      return this.movementType;
   }

   public final double component6() {
      return this.quantity;
   }

   public final double component7() {
      return this.balanceAfter;
   }

   @NotNull
   public final String component8() {
      return this.reason;
   }

   @NotNull
   public final String component9() {
      return this.userResponsible;
   }

   @Nullable
   public final String component10() {
      return this.movementDate;
   }

   @NotNull
   public final InventoryMovement copy(long id, long inventoryId, long patientId, long medicationId, @NotNull MovementType movementType, double quantity, double balanceAfter, @NotNull String reason, @NotNull String userResponsible, @Nullable String movementDate) {
      Intrinsics.checkNotNullParameter(movementType, "movementType");
      Intrinsics.checkNotNullParameter(reason, "reason");
      Intrinsics.checkNotNullParameter(userResponsible, "userResponsible");
      return new InventoryMovement(id, inventoryId, patientId, medicationId, movementType, quantity, balanceAfter, reason, userResponsible, movementDate);
   }

   // $FF: synthetic method
   public static InventoryMovement copy$default(InventoryMovement var0, long var1, long var3, long var5, long var7, MovementType var9, double var10, double var12, String var14, String var15, String var16, int var17, Object var18) {
      if ((var17 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var17 & 2) != 0) {
         var3 = var0.inventoryId;
      }

      if ((var17 & 4) != 0) {
         var5 = var0.patientId;
      }

      if ((var17 & 8) != 0) {
         var7 = var0.medicationId;
      }

      if ((var17 & 16) != 0) {
         var9 = var0.movementType;
      }

      if ((var17 & 32) != 0) {
         var10 = var0.quantity;
      }

      if ((var17 & 64) != 0) {
         var12 = var0.balanceAfter;
      }

      if ((var17 & 128) != 0) {
         var14 = var0.reason;
      }

      if ((var17 & 256) != 0) {
         var15 = var0.userResponsible;
      }

      if ((var17 & 512) != 0) {
         var16 = var0.movementDate;
      }

      return var0.copy(var1, var3, var5, var7, var9, var10, var12, var14, var15, var16);
   }

   @NotNull
   public String toString() {
      return "InventoryMovement(id=" + this.id + ", inventoryId=" + this.inventoryId + ", patientId=" + this.patientId + ", medicationId=" + this.medicationId + ", movementType=" + this.movementType + ", quantity=" + this.quantity + ", balanceAfter=" + this.balanceAfter + ", reason=" + this.reason + ", userResponsible=" + this.userResponsible + ", movementDate=" + this.movementDate + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + Long.hashCode(this.inventoryId);
      result = result * 31 + Long.hashCode(this.patientId);
      result = result * 31 + Long.hashCode(this.medicationId);
      result = result * 31 + this.movementType.hashCode();
      result = result * 31 + Double.hashCode(this.quantity);
      result = result * 31 + Double.hashCode(this.balanceAfter);
      result = result * 31 + this.reason.hashCode();
      result = result * 31 + this.userResponsible.hashCode();
      result = result * 31 + (this.movementDate == null ? 0 : this.movementDate.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof InventoryMovement)) {
         return false;
      } else {
         InventoryMovement var2 = (InventoryMovement)other;
         if (this.id != var2.id) {
            return false;
         } else if (this.inventoryId != var2.inventoryId) {
            return false;
         } else if (this.patientId != var2.patientId) {
            return false;
         } else if (this.medicationId != var2.medicationId) {
            return false;
         } else if (this.movementType != var2.movementType) {
            return false;
         } else if (Double.compare(this.quantity, var2.quantity) != 0) {
            return false;
         } else if (Double.compare(this.balanceAfter, var2.balanceAfter) != 0) {
            return false;
         } else if (!Intrinsics.areEqual(this.reason, var2.reason)) {
            return false;
         } else if (!Intrinsics.areEqual(this.userResponsible, var2.userResponsible)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.movementDate, var2.movementDate);
         }
      }
   }
}
