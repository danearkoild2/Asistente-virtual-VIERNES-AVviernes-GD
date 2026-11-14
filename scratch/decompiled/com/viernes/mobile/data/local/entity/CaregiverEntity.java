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
   d1 = {"\u0000(\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0018\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001BG\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u0012\u0006\u0010\u0006\u001a\u00020\u0005\u0012\u0006\u0010\u0007\u001a\u00020\u0003\u0012\b\b\u0002\u0010\b\u001a\u00020\u0005\u0012\b\b\u0002\u0010\t\u001a\u00020\u0005\u0012\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u0005¢\u0006\u0002\u0010\u000bJ\t\u0010\u0015\u001a\u00020\u0003HÆ\u0003J\t\u0010\u0016\u001a\u00020\u0005HÆ\u0003J\t\u0010\u0017\u001a\u00020\u0005HÆ\u0003J\t\u0010\u0018\u001a\u00020\u0003HÆ\u0003J\t\u0010\u0019\u001a\u00020\u0005HÆ\u0003J\t\u0010\u001a\u001a\u00020\u0005HÆ\u0003J\u000b\u0010\u001b\u001a\u0004\u0018\u00010\u0005HÆ\u0003JQ\u0010\u001c\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00052\b\b\u0002\u0010\u0006\u001a\u00020\u00052\b\b\u0002\u0010\u0007\u001a\u00020\u00032\b\b\u0002\u0010\b\u001a\u00020\u00052\b\b\u0002\u0010\t\u001a\u00020\u00052\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u0005HÆ\u0001J\u0013\u0010\u001d\u001a\u00020\u001e2\b\u0010\u001f\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010 \u001a\u00020!HÖ\u0001J\t\u0010\"\u001a\u00020\u0005HÖ\u0001R\u0013\u0010\n\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\f\u0010\rR\u0011\u0010\u0006\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u000e\u0010\rR\u0016\u0010\u0002\u001a\u00020\u00038\u0006X\u0087\u0004¢\u0006\b\n\u0000\u001a\u0004\b\u000f\u0010\u0010R\u0011\u0010\u0007\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0011\u0010\u0010R\u0011\u0010\t\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0012\u0010\rR\u0011\u0010\b\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0013\u0010\rR\u0011\u0010\u0004\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0014\u0010\r¨\u0006#"},
   d2 = {"Lcom/viernes/mobile/data/local/entity/CaregiverEntity;", "", "id", "", "userId", "", "caregiverName", "patientId", "role", "permissionsJson", "assignedAt", "(JLjava/lang/String;Ljava/lang/String;JLjava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getAssignedAt", "()Ljava/lang/String;", "getCaregiverName", "getId", "()J", "getPatientId", "getPermissionsJson", "getRole", "getUserId", "component1", "component2", "component3", "component4", "component5", "component6", "component7", "copy", "equals", "", "other", "hashCode", "", "toString", "app_debug"}
)
@Entity(
   tableName = "caregiver_assignments",
   indices = {@Index(
   value = {"userId", "patientId"},
   unique = true
), @Index({"patientId"})},
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
public final class CaregiverEntity {
   @PrimaryKey(
      autoGenerate = true
   )
   private final long id;
   @NotNull
   private final String userId;
   @NotNull
   private final String caregiverName;
   private final long patientId;
   @NotNull
   private final String role;
   @NotNull
   private final String permissionsJson;
   @Nullable
   private final String assignedAt;
   public static final int $stable;

   public CaregiverEntity(long id, @NotNull String userId, @NotNull String caregiverName, long patientId, @NotNull String role, @NotNull String permissionsJson, @Nullable String assignedAt) {
      Intrinsics.checkNotNullParameter(userId, "userId");
      Intrinsics.checkNotNullParameter(caregiverName, "caregiverName");
      Intrinsics.checkNotNullParameter(role, "role");
      Intrinsics.checkNotNullParameter(permissionsJson, "permissionsJson");
      super();
      this.id = id;
      this.userId = userId;
      this.caregiverName = caregiverName;
      this.patientId = patientId;
      this.role = role;
      this.permissionsJson = permissionsJson;
      this.assignedAt = assignedAt;
   }

   // $FF: synthetic method
   public CaregiverEntity(long var1, String var3, String var4, long var5, String var7, String var8, String var9, int var10, DefaultConstructorMarker var11) {
      if ((var10 & 1) != 0) {
         var1 = 0L;
      }

      if ((var10 & 16) != 0) {
         var7 = "AUTHORIZED_CAREGIVER";
      }

      if ((var10 & 32) != 0) {
         var8 = "[]";
      }

      if ((var10 & 64) != 0) {
         var9 = null;
      }

      this(var1, var3, var4, var5, var7, var8, var9);
   }

   public final long getId() {
      return this.id;
   }

   @NotNull
   public final String getUserId() {
      return this.userId;
   }

   @NotNull
   public final String getCaregiverName() {
      return this.caregiverName;
   }

   public final long getPatientId() {
      return this.patientId;
   }

   @NotNull
   public final String getRole() {
      return this.role;
   }

   @NotNull
   public final String getPermissionsJson() {
      return this.permissionsJson;
   }

   @Nullable
   public final String getAssignedAt() {
      return this.assignedAt;
   }

   public final long component1() {
      return this.id;
   }

   @NotNull
   public final String component2() {
      return this.userId;
   }

   @NotNull
   public final String component3() {
      return this.caregiverName;
   }

   public final long component4() {
      return this.patientId;
   }

   @NotNull
   public final String component5() {
      return this.role;
   }

   @NotNull
   public final String component6() {
      return this.permissionsJson;
   }

   @Nullable
   public final String component7() {
      return this.assignedAt;
   }

   @NotNull
   public final CaregiverEntity copy(long id, @NotNull String userId, @NotNull String caregiverName, long patientId, @NotNull String role, @NotNull String permissionsJson, @Nullable String assignedAt) {
      Intrinsics.checkNotNullParameter(userId, "userId");
      Intrinsics.checkNotNullParameter(caregiverName, "caregiverName");
      Intrinsics.checkNotNullParameter(role, "role");
      Intrinsics.checkNotNullParameter(permissionsJson, "permissionsJson");
      return new CaregiverEntity(id, userId, caregiverName, patientId, role, permissionsJson, assignedAt);
   }

   // $FF: synthetic method
   public static CaregiverEntity copy$default(CaregiverEntity var0, long var1, String var3, String var4, long var5, String var7, String var8, String var9, int var10, Object var11) {
      if ((var10 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var10 & 2) != 0) {
         var3 = var0.userId;
      }

      if ((var10 & 4) != 0) {
         var4 = var0.caregiverName;
      }

      if ((var10 & 8) != 0) {
         var5 = var0.patientId;
      }

      if ((var10 & 16) != 0) {
         var7 = var0.role;
      }

      if ((var10 & 32) != 0) {
         var8 = var0.permissionsJson;
      }

      if ((var10 & 64) != 0) {
         var9 = var0.assignedAt;
      }

      return var0.copy(var1, var3, var4, var5, var7, var8, var9);
   }

   @NotNull
   public String toString() {
      return "CaregiverEntity(id=" + this.id + ", userId=" + this.userId + ", caregiverName=" + this.caregiverName + ", patientId=" + this.patientId + ", role=" + this.role + ", permissionsJson=" + this.permissionsJson + ", assignedAt=" + this.assignedAt + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + this.userId.hashCode();
      result = result * 31 + this.caregiverName.hashCode();
      result = result * 31 + Long.hashCode(this.patientId);
      result = result * 31 + this.role.hashCode();
      result = result * 31 + this.permissionsJson.hashCode();
      result = result * 31 + (this.assignedAt == null ? 0 : this.assignedAt.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof CaregiverEntity)) {
         return false;
      } else {
         CaregiverEntity var2 = (CaregiverEntity)other;
         if (this.id != var2.id) {
            return false;
         } else if (!Intrinsics.areEqual(this.userId, var2.userId)) {
            return false;
         } else if (!Intrinsics.areEqual(this.caregiverName, var2.caregiverName)) {
            return false;
         } else if (this.patientId != var2.patientId) {
            return false;
         } else if (!Intrinsics.areEqual(this.role, var2.role)) {
            return false;
         } else if (!Intrinsics.areEqual(this.permissionsJson, var2.permissionsJson)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.assignedAt, var2.assignedAt);
         }
      }
   }
}
