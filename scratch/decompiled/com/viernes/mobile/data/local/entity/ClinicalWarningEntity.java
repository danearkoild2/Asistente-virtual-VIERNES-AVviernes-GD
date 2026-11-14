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
   d1 = {"\u0000*\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0006\n\u0002\u0010\u000b\n\u0002\b\u001d\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001Bi\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\b\b\u0002\u0010\u0005\u001a\u00020\u0006\u0012\u0006\u0010\u0007\u001a\u00020\u0006\u0012\b\b\u0002\u0010\b\u001a\u00020\u0006\u0012\u0006\u0010\t\u001a\u00020\u0006\u0012\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u0006\u0012\b\b\u0002\u0010\f\u001a\u00020\r\u0012\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u0006¢\u0006\u0002\u0010\u000fJ\t\u0010\u001d\u001a\u00020\u0003HÆ\u0003J\u000b\u0010\u001e\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\t\u0010\u001f\u001a\u00020\u0003HÆ\u0003J\t\u0010 \u001a\u00020\u0006HÆ\u0003J\t\u0010!\u001a\u00020\u0006HÆ\u0003J\t\u0010\"\u001a\u00020\u0006HÆ\u0003J\t\u0010#\u001a\u00020\u0006HÆ\u0003J\u000b\u0010$\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010%\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\t\u0010&\u001a\u00020\rHÆ\u0003Js\u0010'\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00062\b\b\u0002\u0010\u0007\u001a\u00020\u00062\b\b\u0002\u0010\b\u001a\u00020\u00062\b\b\u0002\u0010\t\u001a\u00020\u00062\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u00062\b\b\u0002\u0010\f\u001a\u00020\r2\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u0006HÆ\u0001J\u0013\u0010(\u001a\u00020\r2\b\u0010)\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010*\u001a\u00020+HÖ\u0001J\t\u0010,\u001a\u00020\u0006HÖ\u0001R\u0011\u0010\f\u001a\u00020\r¢\u0006\b\n\u0000\u001a\u0004\b\u0010\u0010\u0011R\u0013\u0010\u000e\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u0012\u0010\u0013R\u0016\u0010\u0002\u001a\u00020\u00038\u0006X\u0087\u0004¢\u0006\b\n\u0000\u001a\u0004\b\u0014\u0010\u0015R\u0011\u0010\u0005\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u0016\u0010\u0013R\u0011\u0010\t\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0013R\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0015R\u0013\u0010\u000b\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u0019\u0010\u0013R\u0011\u0010\b\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0013R\u0013\u0010\n\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u001b\u0010\u0013R\u0011\u0010\u0007\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u0013¨\u0006-"},
   d2 = {"Lcom/viernes/mobile/data/local/entity/ClinicalWarningEntity;", "", "id", "", "patientId", "medicationIdsJson", "", "warningType", "severity", "message", "source", "recommendation", "acknowledged", "", "createdAt", "(JJLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;ZLjava/lang/String;)V", "getAcknowledged", "()Z", "getCreatedAt", "()Ljava/lang/String;", "getId", "()J", "getMedicationIdsJson", "getMessage", "getPatientId", "getRecommendation", "getSeverity", "getSource", "getWarningType", "component1", "component10", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "other", "hashCode", "", "toString", "app_debug"}
)
@Entity(
   tableName = "clinical_warnings",
   indices = {@Index({"patientId", "acknowledged"})},
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
public final class ClinicalWarningEntity {
   @PrimaryKey(
      autoGenerate = true
   )
   private final long id;
   private final long patientId;
   @NotNull
   private final String medicationIdsJson;
   @NotNull
   private final String warningType;
   @NotNull
   private final String severity;
   @NotNull
   private final String message;
   @Nullable
   private final String source;
   @Nullable
   private final String recommendation;
   private final boolean acknowledged;
   @Nullable
   private final String createdAt;
   public static final int $stable;

   public ClinicalWarningEntity(long id, long patientId, @NotNull String medicationIdsJson, @NotNull String warningType, @NotNull String severity, @NotNull String message, @Nullable String source, @Nullable String recommendation, boolean acknowledged, @Nullable String createdAt) {
      Intrinsics.checkNotNullParameter(medicationIdsJson, "medicationIdsJson");
      Intrinsics.checkNotNullParameter(warningType, "warningType");
      Intrinsics.checkNotNullParameter(severity, "severity");
      Intrinsics.checkNotNullParameter(message, "message");
      super();
      this.id = id;
      this.patientId = patientId;
      this.medicationIdsJson = medicationIdsJson;
      this.warningType = warningType;
      this.severity = severity;
      this.message = message;
      this.source = source;
      this.recommendation = recommendation;
      this.acknowledged = acknowledged;
      this.createdAt = createdAt;
   }

   // $FF: synthetic method
   public ClinicalWarningEntity(long var1, long var3, String var5, String var6, String var7, String var8, String var9, String var10, boolean var11, String var12, int var13, DefaultConstructorMarker var14) {
      if ((var13 & 1) != 0) {
         var1 = 0L;
      }

      if ((var13 & 4) != 0) {
         var5 = "[]";
      }

      if ((var13 & 16) != 0) {
         var7 = "WARNING";
      }

      if ((var13 & 64) != 0) {
         var9 = null;
      }

      if ((var13 & 128) != 0) {
         var10 = null;
      }

      if ((var13 & 256) != 0) {
         var11 = false;
      }

      if ((var13 & 512) != 0) {
         var12 = null;
      }

      this(var1, var3, var5, var6, var7, var8, var9, var10, var11, var12);
   }

   public final long getId() {
      return this.id;
   }

   public final long getPatientId() {
      return this.patientId;
   }

   @NotNull
   public final String getMedicationIdsJson() {
      return this.medicationIdsJson;
   }

   @NotNull
   public final String getWarningType() {
      return this.warningType;
   }

   @NotNull
   public final String getSeverity() {
      return this.severity;
   }

   @NotNull
   public final String getMessage() {
      return this.message;
   }

   @Nullable
   public final String getSource() {
      return this.source;
   }

   @Nullable
   public final String getRecommendation() {
      return this.recommendation;
   }

   public final boolean getAcknowledged() {
      return this.acknowledged;
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

   @NotNull
   public final String component3() {
      return this.medicationIdsJson;
   }

   @NotNull
   public final String component4() {
      return this.warningType;
   }

   @NotNull
   public final String component5() {
      return this.severity;
   }

   @NotNull
   public final String component6() {
      return this.message;
   }

   @Nullable
   public final String component7() {
      return this.source;
   }

   @Nullable
   public final String component8() {
      return this.recommendation;
   }

   public final boolean component9() {
      return this.acknowledged;
   }

   @Nullable
   public final String component10() {
      return this.createdAt;
   }

   @NotNull
   public final ClinicalWarningEntity copy(long id, long patientId, @NotNull String medicationIdsJson, @NotNull String warningType, @NotNull String severity, @NotNull String message, @Nullable String source, @Nullable String recommendation, boolean acknowledged, @Nullable String createdAt) {
      Intrinsics.checkNotNullParameter(medicationIdsJson, "medicationIdsJson");
      Intrinsics.checkNotNullParameter(warningType, "warningType");
      Intrinsics.checkNotNullParameter(severity, "severity");
      Intrinsics.checkNotNullParameter(message, "message");
      return new ClinicalWarningEntity(id, patientId, medicationIdsJson, warningType, severity, message, source, recommendation, acknowledged, createdAt);
   }

   // $FF: synthetic method
   public static ClinicalWarningEntity copy$default(ClinicalWarningEntity var0, long var1, long var3, String var5, String var6, String var7, String var8, String var9, String var10, boolean var11, String var12, int var13, Object var14) {
      if ((var13 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var13 & 2) != 0) {
         var3 = var0.patientId;
      }

      if ((var13 & 4) != 0) {
         var5 = var0.medicationIdsJson;
      }

      if ((var13 & 8) != 0) {
         var6 = var0.warningType;
      }

      if ((var13 & 16) != 0) {
         var7 = var0.severity;
      }

      if ((var13 & 32) != 0) {
         var8 = var0.message;
      }

      if ((var13 & 64) != 0) {
         var9 = var0.source;
      }

      if ((var13 & 128) != 0) {
         var10 = var0.recommendation;
      }

      if ((var13 & 256) != 0) {
         var11 = var0.acknowledged;
      }

      if ((var13 & 512) != 0) {
         var12 = var0.createdAt;
      }

      return var0.copy(var1, var3, var5, var6, var7, var8, var9, var10, var11, var12);
   }

   @NotNull
   public String toString() {
      return "ClinicalWarningEntity(id=" + this.id + ", patientId=" + this.patientId + ", medicationIdsJson=" + this.medicationIdsJson + ", warningType=" + this.warningType + ", severity=" + this.severity + ", message=" + this.message + ", source=" + this.source + ", recommendation=" + this.recommendation + ", acknowledged=" + this.acknowledged + ", createdAt=" + this.createdAt + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + Long.hashCode(this.patientId);
      result = result * 31 + this.medicationIdsJson.hashCode();
      result = result * 31 + this.warningType.hashCode();
      result = result * 31 + this.severity.hashCode();
      result = result * 31 + this.message.hashCode();
      result = result * 31 + (this.source == null ? 0 : this.source.hashCode());
      result = result * 31 + (this.recommendation == null ? 0 : this.recommendation.hashCode());
      result = result * 31 + Boolean.hashCode(this.acknowledged);
      result = result * 31 + (this.createdAt == null ? 0 : this.createdAt.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof ClinicalWarningEntity)) {
         return false;
      } else {
         ClinicalWarningEntity var2 = (ClinicalWarningEntity)other;
         if (this.id != var2.id) {
            return false;
         } else if (this.patientId != var2.patientId) {
            return false;
         } else if (!Intrinsics.areEqual(this.medicationIdsJson, var2.medicationIdsJson)) {
            return false;
         } else if (!Intrinsics.areEqual(this.warningType, var2.warningType)) {
            return false;
         } else if (!Intrinsics.areEqual(this.severity, var2.severity)) {
            return false;
         } else if (!Intrinsics.areEqual(this.message, var2.message)) {
            return false;
         } else if (!Intrinsics.areEqual(this.source, var2.source)) {
            return false;
         } else if (!Intrinsics.areEqual(this.recommendation, var2.recommendation)) {
            return false;
         } else if (this.acknowledged != var2.acknowledged) {
            return false;
         } else {
            return Intrinsics.areEqual(this.createdAt, var2.createdAt);
         }
      }
   }
}
