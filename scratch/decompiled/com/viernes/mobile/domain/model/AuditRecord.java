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
   d1 = {"\u0000(\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u001e\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001BY\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\b\b\u0002\u0010\u0004\u001a\u00020\u0005\u0012\n\b\u0002\u0010\u0006\u001a\u0004\u0018\u00010\u0003\u0012\u0006\u0010\u0007\u001a\u00020\u0005\u0012\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u0003\u0012\u0006\u0010\t\u001a\u00020\u0005\u0012\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u0005\u0012\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u0005¢\u0006\u0002\u0010\fJ\t\u0010\u0019\u001a\u00020\u0003HÆ\u0003J\t\u0010\u001a\u001a\u00020\u0005HÆ\u0003J\u0010\u0010\u001b\u001a\u0004\u0018\u00010\u0003HÆ\u0003¢\u0006\u0002\u0010\u0011J\t\u0010\u001c\u001a\u00020\u0005HÆ\u0003J\u0010\u0010\u001d\u001a\u0004\u0018\u00010\u0003HÆ\u0003¢\u0006\u0002\u0010\u0011J\t\u0010\u001e\u001a\u00020\u0005HÆ\u0003J\u000b\u0010\u001f\u001a\u0004\u0018\u00010\u0005HÆ\u0003J\u000b\u0010 \u001a\u0004\u0018\u00010\u0005HÆ\u0003Jf\u0010!\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00052\n\b\u0002\u0010\u0006\u001a\u0004\u0018\u00010\u00032\b\b\u0002\u0010\u0007\u001a\u00020\u00052\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u00032\b\b\u0002\u0010\t\u001a\u00020\u00052\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u00052\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u0005HÆ\u0001¢\u0006\u0002\u0010\"J\u0013\u0010#\u001a\u00020$2\b\u0010%\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010&\u001a\u00020'HÖ\u0001J\t\u0010(\u001a\u00020\u0005HÖ\u0001R\u0011\u0010\t\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\r\u0010\u000eR\u0013\u0010\n\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u000f\u0010\u000eR\u0015\u0010\b\u001a\u0004\u0018\u00010\u0003¢\u0006\n\n\u0002\u0010\u0012\u001a\u0004\b\u0010\u0010\u0011R\u0011\u0010\u0007\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0013\u0010\u000eR\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0014\u0010\u0015R\u0015\u0010\u0006\u001a\u0004\u0018\u00010\u0003¢\u0006\n\n\u0002\u0010\u0012\u001a\u0004\b\u0016\u0010\u0011R\u0013\u0010\u000b\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u000eR\u0011\u0010\u0004\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u000e¨\u0006)"},
   d2 = {"Lcom/viernes/mobile/domain/model/AuditRecord;", "", "id", "", "userId", "", "patientId", "entityName", "entityId", "action", "details", "timestamp", "(JLjava/lang/String;Ljava/lang/Long;Ljava/lang/String;Ljava/lang/Long;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getAction", "()Ljava/lang/String;", "getDetails", "getEntityId", "()Ljava/lang/Long;", "Ljava/lang/Long;", "getEntityName", "getId", "()J", "getPatientId", "getTimestamp", "getUserId", "component1", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "copy", "(JLjava/lang/String;Ljava/lang/Long;Ljava/lang/String;Ljava/lang/Long;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Lcom/viernes/mobile/domain/model/AuditRecord;", "equals", "", "other", "hashCode", "", "toString", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class AuditRecord {
   private final long id;
   @NotNull
   private final String userId;
   @Nullable
   private final Long patientId;
   @NotNull
   private final String entityName;
   @Nullable
   private final Long entityId;
   @NotNull
   private final String action;
   @Nullable
   private final String details;
   @Nullable
   private final String timestamp;
   public static final int $stable;

   public AuditRecord(long id, @NotNull String userId, @Nullable Long patientId, @NotNull String entityName, @Nullable Long entityId, @NotNull String action, @Nullable String details, @Nullable String timestamp) {
      Intrinsics.checkNotNullParameter(userId, "userId");
      Intrinsics.checkNotNullParameter(entityName, "entityName");
      Intrinsics.checkNotNullParameter(action, "action");
      super();
      this.id = id;
      this.userId = userId;
      this.patientId = patientId;
      this.entityName = entityName;
      this.entityId = entityId;
      this.action = action;
      this.details = details;
      this.timestamp = timestamp;
   }

   // $FF: synthetic method
   public AuditRecord(long var1, String var3, Long var4, String var5, Long var6, String var7, String var8, String var9, int var10, DefaultConstructorMarker var11) {
      if ((var10 & 1) != 0) {
         var1 = 0L;
      }

      if ((var10 & 2) != 0) {
         var3 = "system";
      }

      if ((var10 & 4) != 0) {
         var4 = null;
      }

      if ((var10 & 16) != 0) {
         var6 = null;
      }

      if ((var10 & 64) != 0) {
         var8 = null;
      }

      if ((var10 & 128) != 0) {
         var9 = null;
      }

      this(var1, var3, var4, var5, var6, var7, var8, var9);
   }

   public final long getId() {
      return this.id;
   }

   @NotNull
   public final String getUserId() {
      return this.userId;
   }

   @Nullable
   public final Long getPatientId() {
      return this.patientId;
   }

   @NotNull
   public final String getEntityName() {
      return this.entityName;
   }

   @Nullable
   public final Long getEntityId() {
      return this.entityId;
   }

   @NotNull
   public final String getAction() {
      return this.action;
   }

   @Nullable
   public final String getDetails() {
      return this.details;
   }

   @Nullable
   public final String getTimestamp() {
      return this.timestamp;
   }

   public final long component1() {
      return this.id;
   }

   @NotNull
   public final String component2() {
      return this.userId;
   }

   @Nullable
   public final Long component3() {
      return this.patientId;
   }

   @NotNull
   public final String component4() {
      return this.entityName;
   }

   @Nullable
   public final Long component5() {
      return this.entityId;
   }

   @NotNull
   public final String component6() {
      return this.action;
   }

   @Nullable
   public final String component7() {
      return this.details;
   }

   @Nullable
   public final String component8() {
      return this.timestamp;
   }

   @NotNull
   public final AuditRecord copy(long id, @NotNull String userId, @Nullable Long patientId, @NotNull String entityName, @Nullable Long entityId, @NotNull String action, @Nullable String details, @Nullable String timestamp) {
      Intrinsics.checkNotNullParameter(userId, "userId");
      Intrinsics.checkNotNullParameter(entityName, "entityName");
      Intrinsics.checkNotNullParameter(action, "action");
      return new AuditRecord(id, userId, patientId, entityName, entityId, action, details, timestamp);
   }

   // $FF: synthetic method
   public static AuditRecord copy$default(AuditRecord var0, long var1, String var3, Long var4, String var5, Long var6, String var7, String var8, String var9, int var10, Object var11) {
      if ((var10 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var10 & 2) != 0) {
         var3 = var0.userId;
      }

      if ((var10 & 4) != 0) {
         var4 = var0.patientId;
      }

      if ((var10 & 8) != 0) {
         var5 = var0.entityName;
      }

      if ((var10 & 16) != 0) {
         var6 = var0.entityId;
      }

      if ((var10 & 32) != 0) {
         var7 = var0.action;
      }

      if ((var10 & 64) != 0) {
         var8 = var0.details;
      }

      if ((var10 & 128) != 0) {
         var9 = var0.timestamp;
      }

      return var0.copy(var1, var3, var4, var5, var6, var7, var8, var9);
   }

   @NotNull
   public String toString() {
      return "AuditRecord(id=" + this.id + ", userId=" + this.userId + ", patientId=" + this.patientId + ", entityName=" + this.entityName + ", entityId=" + this.entityId + ", action=" + this.action + ", details=" + this.details + ", timestamp=" + this.timestamp + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + this.userId.hashCode();
      result = result * 31 + (this.patientId == null ? 0 : this.patientId.hashCode());
      result = result * 31 + this.entityName.hashCode();
      result = result * 31 + (this.entityId == null ? 0 : this.entityId.hashCode());
      result = result * 31 + this.action.hashCode();
      result = result * 31 + (this.details == null ? 0 : this.details.hashCode());
      result = result * 31 + (this.timestamp == null ? 0 : this.timestamp.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof AuditRecord)) {
         return false;
      } else {
         AuditRecord var2 = (AuditRecord)other;
         if (this.id != var2.id) {
            return false;
         } else if (!Intrinsics.areEqual(this.userId, var2.userId)) {
            return false;
         } else if (!Intrinsics.areEqual(this.patientId, var2.patientId)) {
            return false;
         } else if (!Intrinsics.areEqual(this.entityName, var2.entityName)) {
            return false;
         } else if (!Intrinsics.areEqual(this.entityId, var2.entityId)) {
            return false;
         } else if (!Intrinsics.areEqual(this.action, var2.action)) {
            return false;
         } else if (!Intrinsics.areEqual(this.details, var2.details)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.timestamp, var2.timestamp);
         }
      }
   }
}
