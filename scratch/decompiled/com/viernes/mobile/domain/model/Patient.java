package com.viernes.mobile.domain.model;

import androidx.compose.runtime.internal.StabilityInferred;
import kotlin.Metadata;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.text.StringsKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000(\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0006\n\u0002\u0010\u000b\n\u0002\b)\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001B\u0095\u0001\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u0012\n\b\u0002\u0010\u0006\u001a\u0004\u0018\u00010\u0005\u0012\n\b\u0002\u0010\u0007\u001a\u0004\u0018\u00010\u0005\u0012\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u0005\u0012\n\b\u0002\u0010\t\u001a\u0004\u0018\u00010\u0005\u0012\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u0005\u0012\b\b\u0002\u0010\u000b\u001a\u00020\f\u0012\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u0005\u0012\b\b\u0002\u0010\u000e\u001a\u00020\u0005\u0012\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u0005\u0012\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u0005\u0012\b\b\u0002\u0010\u0011\u001a\u00020\u0005¢\u0006\u0002\u0010\u0012J\t\u0010%\u001a\u00020\u0003HÆ\u0003J\t\u0010&\u001a\u00020\u0005HÆ\u0003J\u000b\u0010'\u001a\u0004\u0018\u00010\u0005HÆ\u0003J\u000b\u0010(\u001a\u0004\u0018\u00010\u0005HÆ\u0003J\t\u0010)\u001a\u00020\u0005HÆ\u0003J\t\u0010*\u001a\u00020\u0005HÆ\u0003J\u000b\u0010+\u001a\u0004\u0018\u00010\u0005HÆ\u0003J\u000b\u0010,\u001a\u0004\u0018\u00010\u0005HÆ\u0003J\u000b\u0010-\u001a\u0004\u0018\u00010\u0005HÆ\u0003J\u000b\u0010.\u001a\u0004\u0018\u00010\u0005HÆ\u0003J\u000b\u0010/\u001a\u0004\u0018\u00010\u0005HÆ\u0003J\t\u00100\u001a\u00020\fHÆ\u0003J\u000b\u00101\u001a\u0004\u0018\u00010\u0005HÆ\u0003J\u009b\u0001\u00102\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00052\n\b\u0002\u0010\u0006\u001a\u0004\u0018\u00010\u00052\n\b\u0002\u0010\u0007\u001a\u0004\u0018\u00010\u00052\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u00052\n\b\u0002\u0010\t\u001a\u0004\u0018\u00010\u00052\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u00052\b\b\u0002\u0010\u000b\u001a\u00020\f2\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u00052\b\b\u0002\u0010\u000e\u001a\u00020\u00052\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u00052\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u00052\b\b\u0002\u0010\u0011\u001a\u00020\u0005HÆ\u0001J\u0013\u00103\u001a\u00020\f2\b\u00104\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u00105\u001a\u000206HÖ\u0001J\t\u00107\u001a\u00020\u0005HÖ\u0001R\u0011\u0010\u000b\u001a\u00020\f¢\u0006\b\n\u0000\u001a\u0004\b\u0013\u0010\u0014R\u0013\u0010\u0007\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u0016R\u0013\u0010\b\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0017\u0010\u0016R\u0013\u0010\u000f\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0016R\u0011\u0010\u0011\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u0019\u0010\u0016R\u0013\u0010\n\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0016R\u0011\u0010\u001b\u001a\u00020\u00058F¢\u0006\u0006\u001a\u0004\b\u001c\u0010\u0016R\u0013\u0010\t\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b\u001d\u0010\u0016R\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u001e\u0010\u001fR\u0013\u0010\u0006\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b \u0010\u0016R\u0013\u0010\r\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b!\u0010\u0016R\u0011\u0010\u0004\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b\"\u0010\u0016R\u0011\u0010\u000e\u001a\u00020\u0005¢\u0006\b\n\u0000\u001a\u0004\b#\u0010\u0016R\u0013\u0010\u0010\u001a\u0004\u0018\u00010\u0005¢\u0006\b\n\u0000\u001a\u0004\b$\u0010\u0016¨\u00068"},
   d2 = {"Lcom/viernes/mobile/domain/model/Patient;", "", "id", "", "provisionalLabel", "", "legalName", "birthDate", "contactInfo", "emergencyContact", "declaredAllergies", "allergiesVerified", "", "medicalNotes", "status", "createdAt", "updatedAt", "createdBy", "(JLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;ZLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getAllergiesVerified", "()Z", "getBirthDate", "()Ljava/lang/String;", "getContactInfo", "getCreatedAt", "getCreatedBy", "getDeclaredAllergies", "displayName", "getDisplayName", "getEmergencyContact", "getId", "()J", "getLegalName", "getMedicalNotes", "getProvisionalLabel", "getStatus", "getUpdatedAt", "component1", "component10", "component11", "component12", "component13", "component2", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "other", "hashCode", "", "toString", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
@SourceDebugExtension({"SMAP\nModels.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Models.kt\ncom/viernes/mobile/domain/model/Patient\n+ 2 fake.kt\nkotlin/jvm/internal/FakeKt\n*L\n1#1,212:1\n1#2:213\n*E\n"})
public final class Patient {
   private final long id;
   @NotNull
   private final String provisionalLabel;
   @Nullable
   private final String legalName;
   @Nullable
   private final String birthDate;
   @Nullable
   private final String contactInfo;
   @Nullable
   private final String emergencyContact;
   @Nullable
   private final String declaredAllergies;
   private final boolean allergiesVerified;
   @Nullable
   private final String medicalNotes;
   @NotNull
   private final String status;
   @Nullable
   private final String createdAt;
   @Nullable
   private final String updatedAt;
   @NotNull
   private final String createdBy;
   public static final int $stable;

   public Patient(long id, @NotNull String provisionalLabel, @Nullable String legalName, @Nullable String birthDate, @Nullable String contactInfo, @Nullable String emergencyContact, @Nullable String declaredAllergies, boolean allergiesVerified, @Nullable String medicalNotes, @NotNull String status, @Nullable String createdAt, @Nullable String updatedAt, @NotNull String createdBy) {
      Intrinsics.checkNotNullParameter(provisionalLabel, "provisionalLabel");
      Intrinsics.checkNotNullParameter(status, "status");
      Intrinsics.checkNotNullParameter(createdBy, "createdBy");
      super();
      this.id = id;
      this.provisionalLabel = provisionalLabel;
      this.legalName = legalName;
      this.birthDate = birthDate;
      this.contactInfo = contactInfo;
      this.emergencyContact = emergencyContact;
      this.declaredAllergies = declaredAllergies;
      this.allergiesVerified = allergiesVerified;
      this.medicalNotes = medicalNotes;
      this.status = status;
      this.createdAt = createdAt;
      this.updatedAt = updatedAt;
      this.createdBy = createdBy;
   }

   // $FF: synthetic method
   public Patient(long var1, String var3, String var4, String var5, String var6, String var7, String var8, boolean var9, String var10, String var11, String var12, String var13, String var14, int var15, DefaultConstructorMarker var16) {
      if ((var15 & 1) != 0) {
         var1 = 0L;
      }

      if ((var15 & 4) != 0) {
         var4 = null;
      }

      if ((var15 & 8) != 0) {
         var5 = null;
      }

      if ((var15 & 16) != 0) {
         var6 = null;
      }

      if ((var15 & 32) != 0) {
         var7 = null;
      }

      if ((var15 & 64) != 0) {
         var8 = null;
      }

      if ((var15 & 128) != 0) {
         var9 = false;
      }

      if ((var15 & 256) != 0) {
         var10 = null;
      }

      if ((var15 & 512) != 0) {
         var11 = "active";
      }

      if ((var15 & 1024) != 0) {
         var12 = null;
      }

      if ((var15 & 2048) != 0) {
         var13 = null;
      }

      if ((var15 & 4096) != 0) {
         var14 = "system";
      }

      this(var1, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14);
   }

   public final long getId() {
      return this.id;
   }

   @NotNull
   public final String getProvisionalLabel() {
      return this.provisionalLabel;
   }

   @Nullable
   public final String getLegalName() {
      return this.legalName;
   }

   @Nullable
   public final String getBirthDate() {
      return this.birthDate;
   }

   @Nullable
   public final String getContactInfo() {
      return this.contactInfo;
   }

   @Nullable
   public final String getEmergencyContact() {
      return this.emergencyContact;
   }

   @Nullable
   public final String getDeclaredAllergies() {
      return this.declaredAllergies;
   }

   public final boolean getAllergiesVerified() {
      return this.allergiesVerified;
   }

   @Nullable
   public final String getMedicalNotes() {
      return this.medicalNotes;
   }

   @NotNull
   public final String getStatus() {
      return this.status;
   }

   @Nullable
   public final String getCreatedAt() {
      return this.createdAt;
   }

   @Nullable
   public final String getUpdatedAt() {
      return this.updatedAt;
   }

   @NotNull
   public final String getCreatedBy() {
      return this.createdBy;
   }

   @NotNull
   public final String getDisplayName() {
      CharSequence var1 = (CharSequence)this.legalName;
      String var10000;
      if (var1 != null && !StringsKt.isBlank(var1)) {
         var10000 = StringsKt.trim((CharSequence)this.legalName).toString() + " (" + this.provisionalLabel + ")";
      } else {
         var1 = (CharSequence)this.provisionalLabel;
         Object var4;
         if (StringsKt.isBlank(var1)) {
            int var2 = 0;
            var4 = "Paciente Sin Identificar";
         } else {
            var4 = var1;
         }

         var10000 = (String)var4;
      }

      return var10000;
   }

   public final long component1() {
      return this.id;
   }

   @NotNull
   public final String component2() {
      return this.provisionalLabel;
   }

   @Nullable
   public final String component3() {
      return this.legalName;
   }

   @Nullable
   public final String component4() {
      return this.birthDate;
   }

   @Nullable
   public final String component5() {
      return this.contactInfo;
   }

   @Nullable
   public final String component6() {
      return this.emergencyContact;
   }

   @Nullable
   public final String component7() {
      return this.declaredAllergies;
   }

   public final boolean component8() {
      return this.allergiesVerified;
   }

   @Nullable
   public final String component9() {
      return this.medicalNotes;
   }

   @NotNull
   public final String component10() {
      return this.status;
   }

   @Nullable
   public final String component11() {
      return this.createdAt;
   }

   @Nullable
   public final String component12() {
      return this.updatedAt;
   }

   @NotNull
   public final String component13() {
      return this.createdBy;
   }

   @NotNull
   public final Patient copy(long id, @NotNull String provisionalLabel, @Nullable String legalName, @Nullable String birthDate, @Nullable String contactInfo, @Nullable String emergencyContact, @Nullable String declaredAllergies, boolean allergiesVerified, @Nullable String medicalNotes, @NotNull String status, @Nullable String createdAt, @Nullable String updatedAt, @NotNull String createdBy) {
      Intrinsics.checkNotNullParameter(provisionalLabel, "provisionalLabel");
      Intrinsics.checkNotNullParameter(status, "status");
      Intrinsics.checkNotNullParameter(createdBy, "createdBy");
      return new Patient(id, provisionalLabel, legalName, birthDate, contactInfo, emergencyContact, declaredAllergies, allergiesVerified, medicalNotes, status, createdAt, updatedAt, createdBy);
   }

   // $FF: synthetic method
   public static Patient copy$default(Patient var0, long var1, String var3, String var4, String var5, String var6, String var7, String var8, boolean var9, String var10, String var11, String var12, String var13, String var14, int var15, Object var16) {
      if ((var15 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var15 & 2) != 0) {
         var3 = var0.provisionalLabel;
      }

      if ((var15 & 4) != 0) {
         var4 = var0.legalName;
      }

      if ((var15 & 8) != 0) {
         var5 = var0.birthDate;
      }

      if ((var15 & 16) != 0) {
         var6 = var0.contactInfo;
      }

      if ((var15 & 32) != 0) {
         var7 = var0.emergencyContact;
      }

      if ((var15 & 64) != 0) {
         var8 = var0.declaredAllergies;
      }

      if ((var15 & 128) != 0) {
         var9 = var0.allergiesVerified;
      }

      if ((var15 & 256) != 0) {
         var10 = var0.medicalNotes;
      }

      if ((var15 & 512) != 0) {
         var11 = var0.status;
      }

      if ((var15 & 1024) != 0) {
         var12 = var0.createdAt;
      }

      if ((var15 & 2048) != 0) {
         var13 = var0.updatedAt;
      }

      if ((var15 & 4096) != 0) {
         var14 = var0.createdBy;
      }

      return var0.copy(var1, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14);
   }

   @NotNull
   public String toString() {
      return "Patient(id=" + this.id + ", provisionalLabel=" + this.provisionalLabel + ", legalName=" + this.legalName + ", birthDate=" + this.birthDate + ", contactInfo=" + this.contactInfo + ", emergencyContact=" + this.emergencyContact + ", declaredAllergies=" + this.declaredAllergies + ", allergiesVerified=" + this.allergiesVerified + ", medicalNotes=" + this.medicalNotes + ", status=" + this.status + ", createdAt=" + this.createdAt + ", updatedAt=" + this.updatedAt + ", createdBy=" + this.createdBy + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + this.provisionalLabel.hashCode();
      result = result * 31 + (this.legalName == null ? 0 : this.legalName.hashCode());
      result = result * 31 + (this.birthDate == null ? 0 : this.birthDate.hashCode());
      result = result * 31 + (this.contactInfo == null ? 0 : this.contactInfo.hashCode());
      result = result * 31 + (this.emergencyContact == null ? 0 : this.emergencyContact.hashCode());
      result = result * 31 + (this.declaredAllergies == null ? 0 : this.declaredAllergies.hashCode());
      result = result * 31 + Boolean.hashCode(this.allergiesVerified);
      result = result * 31 + (this.medicalNotes == null ? 0 : this.medicalNotes.hashCode());
      result = result * 31 + this.status.hashCode();
      result = result * 31 + (this.createdAt == null ? 0 : this.createdAt.hashCode());
      result = result * 31 + (this.updatedAt == null ? 0 : this.updatedAt.hashCode());
      result = result * 31 + this.createdBy.hashCode();
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof Patient)) {
         return false;
      } else {
         Patient var2 = (Patient)other;
         if (this.id != var2.id) {
            return false;
         } else if (!Intrinsics.areEqual(this.provisionalLabel, var2.provisionalLabel)) {
            return false;
         } else if (!Intrinsics.areEqual(this.legalName, var2.legalName)) {
            return false;
         } else if (!Intrinsics.areEqual(this.birthDate, var2.birthDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.contactInfo, var2.contactInfo)) {
            return false;
         } else if (!Intrinsics.areEqual(this.emergencyContact, var2.emergencyContact)) {
            return false;
         } else if (!Intrinsics.areEqual(this.declaredAllergies, var2.declaredAllergies)) {
            return false;
         } else if (this.allergiesVerified != var2.allergiesVerified) {
            return false;
         } else if (!Intrinsics.areEqual(this.medicalNotes, var2.medicalNotes)) {
            return false;
         } else if (!Intrinsics.areEqual(this.status, var2.status)) {
            return false;
         } else if (!Intrinsics.areEqual(this.createdAt, var2.createdAt)) {
            return false;
         } else if (!Intrinsics.areEqual(this.updatedAt, var2.updatedAt)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.createdBy, var2.createdBy);
         }
      }
   }
}
