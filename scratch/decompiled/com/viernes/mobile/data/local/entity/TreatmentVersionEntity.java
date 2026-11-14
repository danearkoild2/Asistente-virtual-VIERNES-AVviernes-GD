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
   d1 = {"\u0000(\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0010\b\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u001a\n\u0002\u0010\u000b\n\u0002\b\u0004\b\u0087\b\u0018\u00002\u00020\u0001BS\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\b\b\u0002\u0010\u0005\u001a\u00020\u0006\u0012\u0006\u0010\u0007\u001a\u00020\b\u0012\b\b\u0002\u0010\t\u001a\u00020\b\u0012\b\b\u0002\u0010\n\u001a\u00020\b\u0012\b\b\u0002\u0010\u000b\u001a\u00020\b\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\b¢\u0006\u0002\u0010\rJ\t\u0010\u0019\u001a\u00020\u0003HÆ\u0003J\t\u0010\u001a\u001a\u00020\u0003HÆ\u0003J\t\u0010\u001b\u001a\u00020\u0006HÆ\u0003J\t\u0010\u001c\u001a\u00020\bHÆ\u0003J\t\u0010\u001d\u001a\u00020\bHÆ\u0003J\t\u0010\u001e\u001a\u00020\bHÆ\u0003J\t\u0010\u001f\u001a\u00020\bHÆ\u0003J\u000b\u0010 \u001a\u0004\u0018\u00010\bHÆ\u0003J[\u0010!\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00062\b\b\u0002\u0010\u0007\u001a\u00020\b2\b\b\u0002\u0010\t\u001a\u00020\b2\b\b\u0002\u0010\n\u001a\u00020\b2\b\b\u0002\u0010\u000b\u001a\u00020\b2\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\bHÆ\u0001J\u0013\u0010\"\u001a\u00020#2\b\u0010$\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010%\u001a\u00020\u0006HÖ\u0001J\t\u0010&\u001a\u00020\bHÖ\u0001R\u0011\u0010\t\u001a\u00020\b¢\u0006\b\n\u0000\u001a\u0004\b\u000e\u0010\u000fR\u0013\u0010\f\u001a\u0004\u0018\u00010\b¢\u0006\b\n\u0000\u001a\u0004\b\u0010\u0010\u000fR\u0016\u0010\u0002\u001a\u00020\u00038\u0006X\u0087\u0004¢\u0006\b\n\u0000\u001a\u0004\b\u0011\u0010\u0012R\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0013\u0010\u0012R\u0011\u0010\u000b\u001a\u00020\b¢\u0006\b\n\u0000\u001a\u0004\b\u0014\u0010\u000fR\u0011\u0010\n\u001a\u00020\b¢\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u000fR\u0011\u0010\u0007\u001a\u00020\b¢\u0006\b\n\u0000\u001a\u0004\b\u0016\u0010\u000fR\u0011\u0010\u0005\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0018¨\u0006'"},
   d2 = {"Lcom/viernes/mobile/data/local/entity/TreatmentVersionEntity;", "", "id", "", "medicationId", "versionNumber", "", "reasonForChange", "", "changedBy", "previousStateJson", "newStateJson", "createdAt", "(JJILjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getChangedBy", "()Ljava/lang/String;", "getCreatedAt", "getId", "()J", "getMedicationId", "getNewStateJson", "getPreviousStateJson", "getReasonForChange", "getVersionNumber", "()I", "component1", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "copy", "equals", "", "other", "hashCode", "toString", "app_debug"}
)
@Entity(
   tableName = "treatment_versions",
   indices = {@Index({"medicationId"})},
   foreignKeys = {@ForeignKey(
   entity = MedicationEntity.class,
   parentColumns = {"id"},
   childColumns = {"medicationId"},
   onDelete = 5
)}
)
@StabilityInferred(
   parameters = 1
)
public final class TreatmentVersionEntity {
   @PrimaryKey(
      autoGenerate = true
   )
   private final long id;
   private final long medicationId;
   private final int versionNumber;
   @NotNull
   private final String reasonForChange;
   @NotNull
   private final String changedBy;
   @NotNull
   private final String previousStateJson;
   @NotNull
   private final String newStateJson;
   @Nullable
   private final String createdAt;
   public static final int $stable;

   public TreatmentVersionEntity(long id, long medicationId, int versionNumber, @NotNull String reasonForChange, @NotNull String changedBy, @NotNull String previousStateJson, @NotNull String newStateJson, @Nullable String createdAt) {
      Intrinsics.checkNotNullParameter(reasonForChange, "reasonForChange");
      Intrinsics.checkNotNullParameter(changedBy, "changedBy");
      Intrinsics.checkNotNullParameter(previousStateJson, "previousStateJson");
      Intrinsics.checkNotNullParameter(newStateJson, "newStateJson");
      super();
      this.id = id;
      this.medicationId = medicationId;
      this.versionNumber = versionNumber;
      this.reasonForChange = reasonForChange;
      this.changedBy = changedBy;
      this.previousStateJson = previousStateJson;
      this.newStateJson = newStateJson;
      this.createdAt = createdAt;
   }

   // $FF: synthetic method
   public TreatmentVersionEntity(long var1, long var3, int var5, String var6, String var7, String var8, String var9, String var10, int var11, DefaultConstructorMarker var12) {
      if ((var11 & 1) != 0) {
         var1 = 0L;
      }

      if ((var11 & 4) != 0) {
         var5 = 1;
      }

      if ((var11 & 16) != 0) {
         var7 = "system";
      }

      if ((var11 & 32) != 0) {
         var8 = "{}";
      }

      if ((var11 & 64) != 0) {
         var9 = "{}";
      }

      if ((var11 & 128) != 0) {
         var10 = null;
      }

      this(var1, var3, var5, var6, var7, var8, var9, var10);
   }

   public final long getId() {
      return this.id;
   }

   public final long getMedicationId() {
      return this.medicationId;
   }

   public final int getVersionNumber() {
      return this.versionNumber;
   }

   @NotNull
   public final String getReasonForChange() {
      return this.reasonForChange;
   }

   @NotNull
   public final String getChangedBy() {
      return this.changedBy;
   }

   @NotNull
   public final String getPreviousStateJson() {
      return this.previousStateJson;
   }

   @NotNull
   public final String getNewStateJson() {
      return this.newStateJson;
   }

   @Nullable
   public final String getCreatedAt() {
      return this.createdAt;
   }

   public final long component1() {
      return this.id;
   }

   public final long component2() {
      return this.medicationId;
   }

   public final int component3() {
      return this.versionNumber;
   }

   @NotNull
   public final String component4() {
      return this.reasonForChange;
   }

   @NotNull
   public final String component5() {
      return this.changedBy;
   }

   @NotNull
   public final String component6() {
      return this.previousStateJson;
   }

   @NotNull
   public final String component7() {
      return this.newStateJson;
   }

   @Nullable
   public final String component8() {
      return this.createdAt;
   }

   @NotNull
   public final TreatmentVersionEntity copy(long id, long medicationId, int versionNumber, @NotNull String reasonForChange, @NotNull String changedBy, @NotNull String previousStateJson, @NotNull String newStateJson, @Nullable String createdAt) {
      Intrinsics.checkNotNullParameter(reasonForChange, "reasonForChange");
      Intrinsics.checkNotNullParameter(changedBy, "changedBy");
      Intrinsics.checkNotNullParameter(previousStateJson, "previousStateJson");
      Intrinsics.checkNotNullParameter(newStateJson, "newStateJson");
      return new TreatmentVersionEntity(id, medicationId, versionNumber, reasonForChange, changedBy, previousStateJson, newStateJson, createdAt);
   }

   // $FF: synthetic method
   public static TreatmentVersionEntity copy$default(TreatmentVersionEntity var0, long var1, long var3, int var5, String var6, String var7, String var8, String var9, String var10, int var11, Object var12) {
      if ((var11 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var11 & 2) != 0) {
         var3 = var0.medicationId;
      }

      if ((var11 & 4) != 0) {
         var5 = var0.versionNumber;
      }

      if ((var11 & 8) != 0) {
         var6 = var0.reasonForChange;
      }

      if ((var11 & 16) != 0) {
         var7 = var0.changedBy;
      }

      if ((var11 & 32) != 0) {
         var8 = var0.previousStateJson;
      }

      if ((var11 & 64) != 0) {
         var9 = var0.newStateJson;
      }

      if ((var11 & 128) != 0) {
         var10 = var0.createdAt;
      }

      return var0.copy(var1, var3, var5, var6, var7, var8, var9, var10);
   }

   @NotNull
   public String toString() {
      return "TreatmentVersionEntity(id=" + this.id + ", medicationId=" + this.medicationId + ", versionNumber=" + this.versionNumber + ", reasonForChange=" + this.reasonForChange + ", changedBy=" + this.changedBy + ", previousStateJson=" + this.previousStateJson + ", newStateJson=" + this.newStateJson + ", createdAt=" + this.createdAt + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + Long.hashCode(this.medicationId);
      result = result * 31 + Integer.hashCode(this.versionNumber);
      result = result * 31 + this.reasonForChange.hashCode();
      result = result * 31 + this.changedBy.hashCode();
      result = result * 31 + this.previousStateJson.hashCode();
      result = result * 31 + this.newStateJson.hashCode();
      result = result * 31 + (this.createdAt == null ? 0 : this.createdAt.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof TreatmentVersionEntity)) {
         return false;
      } else {
         TreatmentVersionEntity var2 = (TreatmentVersionEntity)other;
         if (this.id != var2.id) {
            return false;
         } else if (this.medicationId != var2.medicationId) {
            return false;
         } else if (this.versionNumber != var2.versionNumber) {
            return false;
         } else if (!Intrinsics.areEqual(this.reasonForChange, var2.reasonForChange)) {
            return false;
         } else if (!Intrinsics.areEqual(this.changedBy, var2.changedBy)) {
            return false;
         } else if (!Intrinsics.areEqual(this.previousStateJson, var2.previousStateJson)) {
            return false;
         } else if (!Intrinsics.areEqual(this.newStateJson, var2.newStateJson)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.createdAt, var2.createdAt);
         }
      }
   }
}
