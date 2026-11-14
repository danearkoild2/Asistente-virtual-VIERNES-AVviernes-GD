package com.viernes.mobile.domain.model;

import androidx.compose.runtime.internal.StabilityInferred;
import java.util.List;
import kotlin.Metadata;
import kotlin.collections.CollectionsKt;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u00006\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010 \n\u0002\b\u0016\n\u0002\u0010\u000b\n\u0002\b\u0004\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001BM\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u0012\u0006\u0010\u0006\u001a\u00020\u0005\u0012\u0006\u0010\u0007\u001a\u00020\u0003\u0012\b\b\u0002\u0010\b\u001a\u00020\t\u0012\u000e\b\u0002\u0010\n\u001a\b\u0012\u0004\u0012\u00020\u00050\u000b\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0005¢\u0006\u0002\u0010\rJ\t\u0010\u0019\u001a\u00020\u0003HÆ\u0003J\t\u0010\u001a\u001a\u00020\u0005HÆ\u0003J\t\u0010\u001b\u001a\u00020\u0005HÆ\u0003J\t\u0010\u001c\u001a\u00020\u0003HÆ\u0003J\t\u0010\u001d\u001a\u00020\tHÆ\u0003J\u000f\u0010\u001e\u001a\b\u0012\u0004\u0012\u00020\u00050\u000bHÆ\u0003J\u000b\u0010\u001f\u001a\u0004\u0018\u00010\u0005HÆ\u0003JW\u0010 \u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00052\b\b\u0002\u0010\u0006\u001a\u00020\u00052\b\b\u0002\u0010\u0007\u001a\u00020\u00032\b\b\u0002\u0010\b\u001a\u00020\t2\u000e\b\u0002\u0010\n\u001a\b\u0012\u0004\u0012\u00020\u00050\u000b2\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0005HÆ\u0001J\u0013\u0010!\u001a\u00020\"2\b\u0010#\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\u000e\u0010$\u001a\u00020\"2\u0006\u0010%\u001a\u00020\u0005J\t\u0010&\u001a\u00020'HÖ\u0001J\t\u0010(\u001a\u00020\u0005HÖ\u0001R\u0013\u0010\f\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u000e\u0010\u000fR\u0011\u0010\u0006\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0010\u0010\u000fR\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0011\u0010\u0012R\u0011\u0010\u0007\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0013\u0010\u0012R\u0017\u0010\n\u001a\b\u0012\u0004\u0012\u00020\u00050\u000b¢\u0006\b\n\u0000\u001a\u0004\b\u0014\u0010\u0015R\u0011\u0010\b\u001a\u00020\t¢\u0006\b\n\u0000\u001a\u0004\b\u0016\u0010\u0017R\u0011\u0010\u0004\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u000f¨\u0006)"},
   d2 = {"Lcom/viernes/mobile/domain/model/CaregiverAssignment;", "", "id", "", "userId", "", "caregiverName", "patientId", "role", "Lcom/viernes/mobile/domain/model/CaregiverRole;", "permissions", "", "assignedAt", "(JLjava/lang/String;Ljava/lang/String;JLcom/viernes/mobile/domain/model/CaregiverRole;Ljava/util/List;Ljava/lang/String;)V", "getAssignedAt", "()Ljava/lang/String;", "getCaregiverName", "getId", "()J", "getPatientId", "getPermissions", "()Ljava/util/List;", "getRole", "()Lcom/viernes/mobile/domain/model/CaregiverRole;", "getUserId", "component1", "component2", "component3", "component4", "component5", "component6", "component7", "copy", "equals", "", "other", "hasPermission", "permission", "hashCode", "", "toString", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
public final class CaregiverAssignment {
   private final long id;
   @NotNull
   private final String userId;
   @NotNull
   private final String caregiverName;
   private final long patientId;
   @NotNull
   private final CaregiverRole role;
   @NotNull
   private final List<String> permissions;
   @Nullable
   private final String assignedAt;
   public static final int $stable = 8;

   public CaregiverAssignment(long id, @NotNull String userId, @NotNull String caregiverName, long patientId, @NotNull CaregiverRole role, @NotNull List<String> permissions, @Nullable String assignedAt) {
      Intrinsics.checkNotNullParameter(userId, "userId");
      Intrinsics.checkNotNullParameter(caregiverName, "caregiverName");
      Intrinsics.checkNotNullParameter(role, "role");
      Intrinsics.checkNotNullParameter(permissions, "permissions");
      super();
      this.id = id;
      this.userId = userId;
      this.caregiverName = caregiverName;
      this.patientId = patientId;
      this.role = role;
      this.permissions = permissions;
      this.assignedAt = assignedAt;
   }

   // $FF: synthetic method
   public CaregiverAssignment(long var1, String var3, String var4, long var5, CaregiverRole var7, List var8, String var9, int var10, DefaultConstructorMarker var11) {
      if ((var10 & 1) != 0) {
         var1 = 0L;
      }

      if ((var10 & 16) != 0) {
         var7 = CaregiverRole.AUTHORIZED_CAREGIVER;
      }

      if ((var10 & 32) != 0) {
         var8 = CollectionsKt.emptyList();
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
   public final CaregiverRole getRole() {
      return this.role;
   }

   @NotNull
   public final List<String> getPermissions() {
      return this.permissions;
   }

   @Nullable
   public final String getAssignedAt() {
      return this.assignedAt;
   }

   public final boolean hasPermission(@NotNull String permission) {
      Intrinsics.checkNotNullParameter(permission, "permission");
      return this.role == CaregiverRole.ADMIN ? true : this.permissions.contains(permission);
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
   public final CaregiverRole component5() {
      return this.role;
   }

   @NotNull
   public final List<String> component6() {
      return this.permissions;
   }

   @Nullable
   public final String component7() {
      return this.assignedAt;
   }

   @NotNull
   public final CaregiverAssignment copy(long id, @NotNull String userId, @NotNull String caregiverName, long patientId, @NotNull CaregiverRole role, @NotNull List<String> permissions, @Nullable String assignedAt) {
      Intrinsics.checkNotNullParameter(userId, "userId");
      Intrinsics.checkNotNullParameter(caregiverName, "caregiverName");
      Intrinsics.checkNotNullParameter(role, "role");
      Intrinsics.checkNotNullParameter(permissions, "permissions");
      return new CaregiverAssignment(id, userId, caregiverName, patientId, role, permissions, assignedAt);
   }

   // $FF: synthetic method
   public static CaregiverAssignment copy$default(CaregiverAssignment var0, long var1, String var3, String var4, long var5, CaregiverRole var7, List var8, String var9, int var10, Object var11) {
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
         var8 = var0.permissions;
      }

      if ((var10 & 64) != 0) {
         var9 = var0.assignedAt;
      }

      return var0.copy(var1, var3, var4, var5, var7, var8, var9);
   }

   @NotNull
   public String toString() {
      return "CaregiverAssignment(id=" + this.id + ", userId=" + this.userId + ", caregiverName=" + this.caregiverName + ", patientId=" + this.patientId + ", role=" + this.role + ", permissions=" + this.permissions + ", assignedAt=" + this.assignedAt + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + this.userId.hashCode();
      result = result * 31 + this.caregiverName.hashCode();
      result = result * 31 + Long.hashCode(this.patientId);
      result = result * 31 + this.role.hashCode();
      result = result * 31 + this.permissions.hashCode();
      result = result * 31 + (this.assignedAt == null ? 0 : this.assignedAt.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof CaregiverAssignment)) {
         return false;
      } else {
         CaregiverAssignment var2 = (CaregiverAssignment)other;
         if (this.id != var2.id) {
            return false;
         } else if (!Intrinsics.areEqual(this.userId, var2.userId)) {
            return false;
         } else if (!Intrinsics.areEqual(this.caregiverName, var2.caregiverName)) {
            return false;
         } else if (this.patientId != var2.patientId) {
            return false;
         } else if (this.role != var2.role) {
            return false;
         } else if (!Intrinsics.areEqual(this.permissions, var2.permissions)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.assignedAt, var2.assignedAt);
         }
      }
   }
}
