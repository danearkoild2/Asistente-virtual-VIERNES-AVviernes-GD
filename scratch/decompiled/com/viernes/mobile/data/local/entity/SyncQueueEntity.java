package com.viernes.mobile.data.local.entity;

import androidx.compose.runtime.internal.StabilityInferred;
import androidx.room.Entity;
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
   d1 = {"\u0000(\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0005\n\u0002\u0010\b\n\u0002\b\u0017\n\u0002\u0010\u000b\n\u0002\b\u0004\b\u0087\b\u0018\u00002\u00020\u0001BM\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u0012\u0006\u0010\u0006\u001a\u00020\u0003\u0012\u0006\u0010\u0007\u001a\u00020\u0005\u0012\u0006\u0010\b\u001a\u00020\u0005\u0012\u0006\u0010\t\u001a\u00020\u0005\u0012\b\b\u0002\u0010\n\u001a\u00020\u000b\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0005¢\u0006\u0002\u0010\rJ\t\u0010\u0019\u001a\u00020\u0003HÆ\u0003J\t\u0010\u001a\u001a\u00020\u0005HÆ\u0003J\t\u0010\u001b\u001a\u00020\u0003HÆ\u0003J\t\u0010\u001c\u001a\u00020\u0005HÆ\u0003J\t\u0010\u001d\u001a\u00020\u0005HÆ\u0003J\t\u0010\u001e\u001a\u00020\u0005HÆ\u0003J\t\u0010\u001f\u001a\u00020\u000bHÆ\u0003J\u000b\u0010 \u001a\u0004\u0018\u00010\u0005HÆ\u0003J[\u0010!\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00052\b\b\u0002\u0010\u0006\u001a\u00020\u00032\b\b\u0002\u0010\u0007\u001a\u00020\u00052\b\b\u0002\u0010\b\u001a\u00020\u00052\b\b\u0002\u0010\t\u001a\u00020\u00052\b\b\u0002\u0010\n\u001a\u00020\u000b2\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0005HÆ\u0001J\u0013\u0010\"\u001a\u00020#2\b\u0010$\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010%\u001a\u00020\u000bHÖ\u0001J\t\u0010&\u001a\u00020\u0005HÖ\u0001R\u0011\u0010\n\u001a\u00020\u000b¢\u0006\b\n\u0000\u001a\u0004\b\u000e\u0010\u000fR\u0011\u0010\t\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0010\u0010\u0011R\u0011\u0010\u0006\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0012\u0010\u0013R\u0011\u0010\u0004\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0014\u0010\u0011R\u0016\u0010\u0002\u001a\u00020\u00038\u0006X\u0087\u0004¢\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u0013R\u0013\u0010\f\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0016\u0010\u0011R\u0011\u0010\u0007\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0011R\u0011\u0010\b\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0011¨\u0006'"},
   d2 = {"Lcom/viernes/mobile/data/local/entity/SyncQueueEntity;", "", "id", "", "entityType", "", "entityId", "operation", "payloadJson", "createdAt", "attempts", "", "lastError", "(JLjava/lang/String;JLjava/lang/String;Ljava/lang/String;Ljava/lang/String;ILjava/lang/String;)V", "getAttempts", "()I", "getCreatedAt", "()Ljava/lang/String;", "getEntityId", "()J", "getEntityType", "getId", "getLastError", "getOperation", "getPayloadJson", "component1", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "copy", "equals", "", "other", "hashCode", "toString", "app_debug"}
)
@Entity(
   tableName = "sync_queue"
)
@StabilityInferred(
   parameters = 1
)
public final class SyncQueueEntity {
   @PrimaryKey(
      autoGenerate = true
   )
   private final long id;
   @NotNull
   private final String entityType;
   private final long entityId;
   @NotNull
   private final String operation;
   @NotNull
   private final String payloadJson;
   @NotNull
   private final String createdAt;
   private final int attempts;
   @Nullable
   private final String lastError;
   public static final int $stable;

   public SyncQueueEntity(long id, @NotNull String entityType, long entityId, @NotNull String operation, @NotNull String payloadJson, @NotNull String createdAt, int attempts, @Nullable String lastError) {
      Intrinsics.checkNotNullParameter(entityType, "entityType");
      Intrinsics.checkNotNullParameter(operation, "operation");
      Intrinsics.checkNotNullParameter(payloadJson, "payloadJson");
      Intrinsics.checkNotNullParameter(createdAt, "createdAt");
      super();
      this.id = id;
      this.entityType = entityType;
      this.entityId = entityId;
      this.operation = operation;
      this.payloadJson = payloadJson;
      this.createdAt = createdAt;
      this.attempts = attempts;
      this.lastError = lastError;
   }

   // $FF: synthetic method
   public SyncQueueEntity(long var1, String var3, long var4, String var6, String var7, String var8, int var9, String var10, int var11, DefaultConstructorMarker var12) {
      if ((var11 & 1) != 0) {
         var1 = 0L;
      }

      if ((var11 & 64) != 0) {
         var9 = 0;
      }

      if ((var11 & 128) != 0) {
         var10 = null;
      }

      this(var1, var3, var4, var6, var7, var8, var9, var10);
   }

   public final long getId() {
      return this.id;
   }

   @NotNull
   public final String getEntityType() {
      return this.entityType;
   }

   public final long getEntityId() {
      return this.entityId;
   }

   @NotNull
   public final String getOperation() {
      return this.operation;
   }

   @NotNull
   public final String getPayloadJson() {
      return this.payloadJson;
   }

   @NotNull
   public final String getCreatedAt() {
      return this.createdAt;
   }

   public final int getAttempts() {
      return this.attempts;
   }

   @Nullable
   public final String getLastError() {
      return this.lastError;
   }

   public final long component1() {
      return this.id;
   }

   @NotNull
   public final String component2() {
      return this.entityType;
   }

   public final long component3() {
      return this.entityId;
   }

   @NotNull
   public final String component4() {
      return this.operation;
   }

   @NotNull
   public final String component5() {
      return this.payloadJson;
   }

   @NotNull
   public final String component6() {
      return this.createdAt;
   }

   public final int component7() {
      return this.attempts;
   }

   @Nullable
   public final String component8() {
      return this.lastError;
   }

   @NotNull
   public final SyncQueueEntity copy(long id, @NotNull String entityType, long entityId, @NotNull String operation, @NotNull String payloadJson, @NotNull String createdAt, int attempts, @Nullable String lastError) {
      Intrinsics.checkNotNullParameter(entityType, "entityType");
      Intrinsics.checkNotNullParameter(operation, "operation");
      Intrinsics.checkNotNullParameter(payloadJson, "payloadJson");
      Intrinsics.checkNotNullParameter(createdAt, "createdAt");
      return new SyncQueueEntity(id, entityType, entityId, operation, payloadJson, createdAt, attempts, lastError);
   }

   // $FF: synthetic method
   public static SyncQueueEntity copy$default(SyncQueueEntity var0, long var1, String var3, long var4, String var6, String var7, String var8, int var9, String var10, int var11, Object var12) {
      if ((var11 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var11 & 2) != 0) {
         var3 = var0.entityType;
      }

      if ((var11 & 4) != 0) {
         var4 = var0.entityId;
      }

      if ((var11 & 8) != 0) {
         var6 = var0.operation;
      }

      if ((var11 & 16) != 0) {
         var7 = var0.payloadJson;
      }

      if ((var11 & 32) != 0) {
         var8 = var0.createdAt;
      }

      if ((var11 & 64) != 0) {
         var9 = var0.attempts;
      }

      if ((var11 & 128) != 0) {
         var10 = var0.lastError;
      }

      return var0.copy(var1, var3, var4, var6, var7, var8, var9, var10);
   }

   @NotNull
   public String toString() {
      return "SyncQueueEntity(id=" + this.id + ", entityType=" + this.entityType + ", entityId=" + this.entityId + ", operation=" + this.operation + ", payloadJson=" + this.payloadJson + ", createdAt=" + this.createdAt + ", attempts=" + this.attempts + ", lastError=" + this.lastError + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + this.entityType.hashCode();
      result = result * 31 + Long.hashCode(this.entityId);
      result = result * 31 + this.operation.hashCode();
      result = result * 31 + this.payloadJson.hashCode();
      result = result * 31 + this.createdAt.hashCode();
      result = result * 31 + Integer.hashCode(this.attempts);
      result = result * 31 + (this.lastError == null ? 0 : this.lastError.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof SyncQueueEntity)) {
         return false;
      } else {
         SyncQueueEntity var2 = (SyncQueueEntity)other;
         if (this.id != var2.id) {
            return false;
         } else if (!Intrinsics.areEqual(this.entityType, var2.entityType)) {
            return false;
         } else if (this.entityId != var2.entityId) {
            return false;
         } else if (!Intrinsics.areEqual(this.operation, var2.operation)) {
            return false;
         } else if (!Intrinsics.areEqual(this.payloadJson, var2.payloadJson)) {
            return false;
         } else if (!Intrinsics.areEqual(this.createdAt, var2.createdAt)) {
            return false;
         } else if (this.attempts != var2.attempts) {
            return false;
         } else {
            return Intrinsics.areEqual(this.lastError, var2.lastError);
         }
      }
   }
}
