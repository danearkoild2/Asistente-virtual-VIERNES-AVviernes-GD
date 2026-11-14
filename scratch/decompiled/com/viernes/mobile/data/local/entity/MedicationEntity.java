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
   d1 = {"\u0000*\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0017\n\u0002\u0010\u000b\n\u0002\bB\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001BÃ\u0002\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\u0006\u0010\u0005\u001a\u00020\u0006\u0012\n\b\u0002\u0010\u0007\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\t\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u0011\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u0012\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u0014\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u0015\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u0016\u001a\u0004\u0018\u00010\u0006\u0012\b\b\u0002\u0010\u0017\u001a\u00020\u0006\u0012\b\b\u0002\u0010\u0018\u001a\u00020\u0006\u0012\n\b\u0002\u0010\u0019\u001a\u0004\u0018\u00010\u0006\u0012\b\b\u0002\u0010\u001a\u001a\u00020\u0006\u0012\n\b\u0002\u0010\u001b\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010\u001c\u001a\u0004\u0018\u00010\u0006\u0012\b\b\u0002\u0010\u001d\u001a\u00020\u001e\u0012\n\b\u0002\u0010\u001f\u001a\u0004\u0018\u00010\u0006\u0012\n\b\u0002\u0010 \u001a\u0004\u0018\u00010\u0006¢\u0006\u0002\u0010!J\t\u0010A\u001a\u00020\u0003HÆ\u0003J\u000b\u0010B\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010C\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010D\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010E\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010F\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010G\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010H\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010I\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010J\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010K\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\t\u0010L\u001a\u00020\u0003HÆ\u0003J\t\u0010M\u001a\u00020\u0006HÆ\u0003J\t\u0010N\u001a\u00020\u0006HÆ\u0003J\u000b\u0010O\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\t\u0010P\u001a\u00020\u0006HÆ\u0003J\u000b\u0010Q\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010R\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\t\u0010S\u001a\u00020\u001eHÆ\u0003J\u000b\u0010T\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010U\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\t\u0010V\u001a\u00020\u0006HÆ\u0003J\u000b\u0010W\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010X\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010Y\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010Z\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010[\u001a\u0004\u0018\u00010\u0006HÆ\u0003J\u000b\u0010\\\u001a\u0004\u0018\u00010\u0006HÆ\u0003JË\u0002\u0010]\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00062\n\b\u0002\u0010\u0007\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\b\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\t\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\n\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u000b\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\f\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\r\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u000f\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u0010\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u0011\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u0012\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u0013\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u0014\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u0015\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u0016\u001a\u0004\u0018\u00010\u00062\b\b\u0002\u0010\u0017\u001a\u00020\u00062\b\b\u0002\u0010\u0018\u001a\u00020\u00062\n\b\u0002\u0010\u0019\u001a\u0004\u0018\u00010\u00062\b\b\u0002\u0010\u001a\u001a\u00020\u00062\n\b\u0002\u0010\u001b\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010\u001c\u001a\u0004\u0018\u00010\u00062\b\b\u0002\u0010\u001d\u001a\u00020\u001e2\n\b\u0002\u0010\u001f\u001a\u0004\u0018\u00010\u00062\n\b\u0002\u0010 \u001a\u0004\u0018\u00010\u0006HÆ\u0001J\u0013\u0010^\u001a\u00020\u001e2\b\u0010_\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010`\u001a\u00020aHÖ\u0001J\t\u0010b\u001a\u00020\u0006HÖ\u0001R\u0013\u0010\b\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b\"\u0010#R\u0013\u0010\u000e\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b$\u0010#R\u0013\u0010\u0007\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b%\u0010#R\u0013\u0010\n\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b&\u0010#R\u0013\u0010\u001b\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b'\u0010#R\u0013\u0010\u001f\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b(\u0010#R\u0011\u0010\u001a\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b)\u0010#R\u0013\u0010\u0016\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b*\u0010#R\u0011\u0010\u001d\u001a\u00020\u001e¢\u0006\b\n\u0000\u001a\u0004\b+\u0010,R\u0013\u0010\u0014\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b-\u0010#R\u0013\u0010\u0010\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b.\u0010#R\u0016\u0010\u0002\u001a\u00020\u00038\u0006X\u0087\u0004¢\u0006\b\n\u0000\u001a\u0004\b/\u00100R\u0013\u0010\u000b\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b1\u0010#R\u0013\u0010\u0019\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b2\u0010#R\u0013\u0010\f\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b3\u0010#R\u0013\u0010\u001c\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b4\u0010#R\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b5\u00100R\u0013\u0010\t\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b6\u0010#R\u0013\u0010\r\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b7\u0010#R\u0013\u0010\u0015\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b8\u0010#R\u0013\u0010\u0011\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b9\u0010#R\u0013\u0010\u0013\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b:\u0010#R\u0013\u0010\u0012\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b;\u0010#R\u0011\u0010\u0005\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b<\u0010#R\u0013\u0010\u000f\u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b=\u0010#R\u0011\u0010\u0018\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b>\u0010#R\u0013\u0010 \u001a\u0004\u0018\u00010\u0006¢\u0006\b\n\u0000\u001a\u0004\b?\u0010#R\u0011\u0010\u0017\u001a\u00020\u0006¢\u0006\b\n\u0000\u001a\u0004\b@\u0010#¨\u0006c"},
   d2 = {"Lcom/viernes/mobile/data/local/entity/MedicationEntity;", "", "id", "", "patientId", "transcribedName", "", "commercialName", "activeIngredient", "pharmaceuticalForm", "concentration", "indicatedQuantity", "measurementUnit", "prescribedDose", "administrationRoute", "transcribedSchedules", "exactScheduleHours", "specialInstructions", "transcribedFunction", "startDate", "endDate", "prescriberSource", "documentRef", "verificationStatus", "treatmentStatus", "lastReviewDate", "createdBy", "confirmedBy", "notes", "duplicateWarning", "", "createdAt", "updatedAt", "(JJLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;ZLjava/lang/String;Ljava/lang/String;)V", "getActiveIngredient", "()Ljava/lang/String;", "getAdministrationRoute", "getCommercialName", "getConcentration", "getConfirmedBy", "getCreatedAt", "getCreatedBy", "getDocumentRef", "getDuplicateWarning", "()Z", "getEndDate", "getExactScheduleHours", "getId", "()J", "getIndicatedQuantity", "getLastReviewDate", "getMeasurementUnit", "getNotes", "getPatientId", "getPharmaceuticalForm", "getPrescribedDose", "getPrescriberSource", "getSpecialInstructions", "getStartDate", "getTranscribedFunction", "getTranscribedName", "getTranscribedSchedules", "getTreatmentStatus", "getUpdatedAt", "getVerificationStatus", "component1", "component10", "component11", "component12", "component13", "component14", "component15", "component16", "component17", "component18", "component19", "component2", "component20", "component21", "component22", "component23", "component24", "component25", "component26", "component27", "component28", "component3", "component4", "component5", "component6", "component7", "component8", "component9", "copy", "equals", "other", "hashCode", "", "toString", "app_debug"}
)
@Entity(
   tableName = "medications",
   indices = {@Index({"patientId"})},
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
public final class MedicationEntity {
   @PrimaryKey(
      autoGenerate = true
   )
   private final long id;
   private final long patientId;
   @NotNull
   private final String transcribedName;
   @Nullable
   private final String commercialName;
   @Nullable
   private final String activeIngredient;
   @Nullable
   private final String pharmaceuticalForm;
   @Nullable
   private final String concentration;
   @Nullable
   private final String indicatedQuantity;
   @Nullable
   private final String measurementUnit;
   @Nullable
   private final String prescribedDose;
   @Nullable
   private final String administrationRoute;
   @Nullable
   private final String transcribedSchedules;
   @Nullable
   private final String exactScheduleHours;
   @Nullable
   private final String specialInstructions;
   @Nullable
   private final String transcribedFunction;
   @Nullable
   private final String startDate;
   @Nullable
   private final String endDate;
   @Nullable
   private final String prescriberSource;
   @Nullable
   private final String documentRef;
   @NotNull
   private final String verificationStatus;
   @NotNull
   private final String treatmentStatus;
   @Nullable
   private final String lastReviewDate;
   @NotNull
   private final String createdBy;
   @Nullable
   private final String confirmedBy;
   @Nullable
   private final String notes;
   private final boolean duplicateWarning;
   @Nullable
   private final String createdAt;
   @Nullable
   private final String updatedAt;
   public static final int $stable;

   public MedicationEntity(long id, long patientId, @NotNull String transcribedName, @Nullable String commercialName, @Nullable String activeIngredient, @Nullable String pharmaceuticalForm, @Nullable String concentration, @Nullable String indicatedQuantity, @Nullable String measurementUnit, @Nullable String prescribedDose, @Nullable String administrationRoute, @Nullable String transcribedSchedules, @Nullable String exactScheduleHours, @Nullable String specialInstructions, @Nullable String transcribedFunction, @Nullable String startDate, @Nullable String endDate, @Nullable String prescriberSource, @Nullable String documentRef, @NotNull String verificationStatus, @NotNull String treatmentStatus, @Nullable String lastReviewDate, @NotNull String createdBy, @Nullable String confirmedBy, @Nullable String notes, boolean duplicateWarning, @Nullable String createdAt, @Nullable String updatedAt) {
      Intrinsics.checkNotNullParameter(transcribedName, "transcribedName");
      Intrinsics.checkNotNullParameter(verificationStatus, "verificationStatus");
      Intrinsics.checkNotNullParameter(treatmentStatus, "treatmentStatus");
      Intrinsics.checkNotNullParameter(createdBy, "createdBy");
      super();
      this.id = id;
      this.patientId = patientId;
      this.transcribedName = transcribedName;
      this.commercialName = commercialName;
      this.activeIngredient = activeIngredient;
      this.pharmaceuticalForm = pharmaceuticalForm;
      this.concentration = concentration;
      this.indicatedQuantity = indicatedQuantity;
      this.measurementUnit = measurementUnit;
      this.prescribedDose = prescribedDose;
      this.administrationRoute = administrationRoute;
      this.transcribedSchedules = transcribedSchedules;
      this.exactScheduleHours = exactScheduleHours;
      this.specialInstructions = specialInstructions;
      this.transcribedFunction = transcribedFunction;
      this.startDate = startDate;
      this.endDate = endDate;
      this.prescriberSource = prescriberSource;
      this.documentRef = documentRef;
      this.verificationStatus = verificationStatus;
      this.treatmentStatus = treatmentStatus;
      this.lastReviewDate = lastReviewDate;
      this.createdBy = createdBy;
      this.confirmedBy = confirmedBy;
      this.notes = notes;
      this.duplicateWarning = duplicateWarning;
      this.createdAt = createdAt;
      this.updatedAt = updatedAt;
   }

   // $FF: synthetic method
   public MedicationEntity(long var1, long var3, String var5, String var6, String var7, String var8, String var9, String var10, String var11, String var12, String var13, String var14, String var15, String var16, String var17, String var18, String var19, String var20, String var21, String var22, String var23, String var24, String var25, String var26, String var27, boolean var28, String var29, String var30, int var31, DefaultConstructorMarker var32) {
      if ((var31 & 1) != 0) {
         var1 = 0L;
      }

      if ((var31 & 8) != 0) {
         var6 = null;
      }

      if ((var31 & 16) != 0) {
         var7 = null;
      }

      if ((var31 & 32) != 0) {
         var8 = null;
      }

      if ((var31 & 64) != 0) {
         var9 = null;
      }

      if ((var31 & 128) != 0) {
         var10 = null;
      }

      if ((var31 & 256) != 0) {
         var11 = null;
      }

      if ((var31 & 512) != 0) {
         var12 = null;
      }

      if ((var31 & 1024) != 0) {
         var13 = null;
      }

      if ((var31 & 2048) != 0) {
         var14 = null;
      }

      if ((var31 & 4096) != 0) {
         var15 = null;
      }

      if ((var31 & 8192) != 0) {
         var16 = null;
      }

      if ((var31 & 16384) != 0) {
         var17 = null;
      }

      if ((var31 & '耀') != 0) {
         var18 = null;
      }

      if ((var31 & 65536) != 0) {
         var19 = null;
      }

      if ((var31 & 131072) != 0) {
         var20 = null;
      }

      if ((var31 & 262144) != 0) {
         var21 = null;
      }

      if ((var31 & 524288) != 0) {
         var22 = "PENDING_CLINICAL_VERIFICATION";
      }

      if ((var31 & 1048576) != 0) {
         var23 = "draft";
      }

      if ((var31 & 2097152) != 0) {
         var24 = null;
      }

      if ((var31 & 4194304) != 0) {
         var25 = "usuario_transcripcion";
      }

      if ((var31 & 8388608) != 0) {
         var26 = null;
      }

      if ((var31 & 16777216) != 0) {
         var27 = null;
      }

      if ((var31 & 33554432) != 0) {
         var28 = false;
      }

      if ((var31 & 67108864) != 0) {
         var29 = null;
      }

      if ((var31 & 134217728) != 0) {
         var30 = null;
      }

      this(var1, var3, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21, var22, var23, var24, var25, var26, var27, var28, var29, var30);
   }

   public final long getId() {
      return this.id;
   }

   public final long getPatientId() {
      return this.patientId;
   }

   @NotNull
   public final String getTranscribedName() {
      return this.transcribedName;
   }

   @Nullable
   public final String getCommercialName() {
      return this.commercialName;
   }

   @Nullable
   public final String getActiveIngredient() {
      return this.activeIngredient;
   }

   @Nullable
   public final String getPharmaceuticalForm() {
      return this.pharmaceuticalForm;
   }

   @Nullable
   public final String getConcentration() {
      return this.concentration;
   }

   @Nullable
   public final String getIndicatedQuantity() {
      return this.indicatedQuantity;
   }

   @Nullable
   public final String getMeasurementUnit() {
      return this.measurementUnit;
   }

   @Nullable
   public final String getPrescribedDose() {
      return this.prescribedDose;
   }

   @Nullable
   public final String getAdministrationRoute() {
      return this.administrationRoute;
   }

   @Nullable
   public final String getTranscribedSchedules() {
      return this.transcribedSchedules;
   }

   @Nullable
   public final String getExactScheduleHours() {
      return this.exactScheduleHours;
   }

   @Nullable
   public final String getSpecialInstructions() {
      return this.specialInstructions;
   }

   @Nullable
   public final String getTranscribedFunction() {
      return this.transcribedFunction;
   }

   @Nullable
   public final String getStartDate() {
      return this.startDate;
   }

   @Nullable
   public final String getEndDate() {
      return this.endDate;
   }

   @Nullable
   public final String getPrescriberSource() {
      return this.prescriberSource;
   }

   @Nullable
   public final String getDocumentRef() {
      return this.documentRef;
   }

   @NotNull
   public final String getVerificationStatus() {
      return this.verificationStatus;
   }

   @NotNull
   public final String getTreatmentStatus() {
      return this.treatmentStatus;
   }

   @Nullable
   public final String getLastReviewDate() {
      return this.lastReviewDate;
   }

   @NotNull
   public final String getCreatedBy() {
      return this.createdBy;
   }

   @Nullable
   public final String getConfirmedBy() {
      return this.confirmedBy;
   }

   @Nullable
   public final String getNotes() {
      return this.notes;
   }

   public final boolean getDuplicateWarning() {
      return this.duplicateWarning;
   }

   @Nullable
   public final String getCreatedAt() {
      return this.createdAt;
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

   @NotNull
   public final String component3() {
      return this.transcribedName;
   }

   @Nullable
   public final String component4() {
      return this.commercialName;
   }

   @Nullable
   public final String component5() {
      return this.activeIngredient;
   }

   @Nullable
   public final String component6() {
      return this.pharmaceuticalForm;
   }

   @Nullable
   public final String component7() {
      return this.concentration;
   }

   @Nullable
   public final String component8() {
      return this.indicatedQuantity;
   }

   @Nullable
   public final String component9() {
      return this.measurementUnit;
   }

   @Nullable
   public final String component10() {
      return this.prescribedDose;
   }

   @Nullable
   public final String component11() {
      return this.administrationRoute;
   }

   @Nullable
   public final String component12() {
      return this.transcribedSchedules;
   }

   @Nullable
   public final String component13() {
      return this.exactScheduleHours;
   }

   @Nullable
   public final String component14() {
      return this.specialInstructions;
   }

   @Nullable
   public final String component15() {
      return this.transcribedFunction;
   }

   @Nullable
   public final String component16() {
      return this.startDate;
   }

   @Nullable
   public final String component17() {
      return this.endDate;
   }

   @Nullable
   public final String component18() {
      return this.prescriberSource;
   }

   @Nullable
   public final String component19() {
      return this.documentRef;
   }

   @NotNull
   public final String component20() {
      return this.verificationStatus;
   }

   @NotNull
   public final String component21() {
      return this.treatmentStatus;
   }

   @Nullable
   public final String component22() {
      return this.lastReviewDate;
   }

   @NotNull
   public final String component23() {
      return this.createdBy;
   }

   @Nullable
   public final String component24() {
      return this.confirmedBy;
   }

   @Nullable
   public final String component25() {
      return this.notes;
   }

   public final boolean component26() {
      return this.duplicateWarning;
   }

   @Nullable
   public final String component27() {
      return this.createdAt;
   }

   @Nullable
   public final String component28() {
      return this.updatedAt;
   }

   @NotNull
   public final MedicationEntity copy(long id, long patientId, @NotNull String transcribedName, @Nullable String commercialName, @Nullable String activeIngredient, @Nullable String pharmaceuticalForm, @Nullable String concentration, @Nullable String indicatedQuantity, @Nullable String measurementUnit, @Nullable String prescribedDose, @Nullable String administrationRoute, @Nullable String transcribedSchedules, @Nullable String exactScheduleHours, @Nullable String specialInstructions, @Nullable String transcribedFunction, @Nullable String startDate, @Nullable String endDate, @Nullable String prescriberSource, @Nullable String documentRef, @NotNull String verificationStatus, @NotNull String treatmentStatus, @Nullable String lastReviewDate, @NotNull String createdBy, @Nullable String confirmedBy, @Nullable String notes, boolean duplicateWarning, @Nullable String createdAt, @Nullable String updatedAt) {
      Intrinsics.checkNotNullParameter(transcribedName, "transcribedName");
      Intrinsics.checkNotNullParameter(verificationStatus, "verificationStatus");
      Intrinsics.checkNotNullParameter(treatmentStatus, "treatmentStatus");
      Intrinsics.checkNotNullParameter(createdBy, "createdBy");
      return new MedicationEntity(id, patientId, transcribedName, commercialName, activeIngredient, pharmaceuticalForm, concentration, indicatedQuantity, measurementUnit, prescribedDose, administrationRoute, transcribedSchedules, exactScheduleHours, specialInstructions, transcribedFunction, startDate, endDate, prescriberSource, documentRef, verificationStatus, treatmentStatus, lastReviewDate, createdBy, confirmedBy, notes, duplicateWarning, createdAt, updatedAt);
   }

   // $FF: synthetic method
   public static MedicationEntity copy$default(MedicationEntity var0, long var1, long var3, String var5, String var6, String var7, String var8, String var9, String var10, String var11, String var12, String var13, String var14, String var15, String var16, String var17, String var18, String var19, String var20, String var21, String var22, String var23, String var24, String var25, String var26, String var27, boolean var28, String var29, String var30, int var31, Object var32) {
      if ((var31 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var31 & 2) != 0) {
         var3 = var0.patientId;
      }

      if ((var31 & 4) != 0) {
         var5 = var0.transcribedName;
      }

      if ((var31 & 8) != 0) {
         var6 = var0.commercialName;
      }

      if ((var31 & 16) != 0) {
         var7 = var0.activeIngredient;
      }

      if ((var31 & 32) != 0) {
         var8 = var0.pharmaceuticalForm;
      }

      if ((var31 & 64) != 0) {
         var9 = var0.concentration;
      }

      if ((var31 & 128) != 0) {
         var10 = var0.indicatedQuantity;
      }

      if ((var31 & 256) != 0) {
         var11 = var0.measurementUnit;
      }

      if ((var31 & 512) != 0) {
         var12 = var0.prescribedDose;
      }

      if ((var31 & 1024) != 0) {
         var13 = var0.administrationRoute;
      }

      if ((var31 & 2048) != 0) {
         var14 = var0.transcribedSchedules;
      }

      if ((var31 & 4096) != 0) {
         var15 = var0.exactScheduleHours;
      }

      if ((var31 & 8192) != 0) {
         var16 = var0.specialInstructions;
      }

      if ((var31 & 16384) != 0) {
         var17 = var0.transcribedFunction;
      }

      if ((var31 & '耀') != 0) {
         var18 = var0.startDate;
      }

      if ((var31 & 65536) != 0) {
         var19 = var0.endDate;
      }

      if ((var31 & 131072) != 0) {
         var20 = var0.prescriberSource;
      }

      if ((var31 & 262144) != 0) {
         var21 = var0.documentRef;
      }

      if ((var31 & 524288) != 0) {
         var22 = var0.verificationStatus;
      }

      if ((var31 & 1048576) != 0) {
         var23 = var0.treatmentStatus;
      }

      if ((var31 & 2097152) != 0) {
         var24 = var0.lastReviewDate;
      }

      if ((var31 & 4194304) != 0) {
         var25 = var0.createdBy;
      }

      if ((var31 & 8388608) != 0) {
         var26 = var0.confirmedBy;
      }

      if ((var31 & 16777216) != 0) {
         var27 = var0.notes;
      }

      if ((var31 & 33554432) != 0) {
         var28 = var0.duplicateWarning;
      }

      if ((var31 & 67108864) != 0) {
         var29 = var0.createdAt;
      }

      if ((var31 & 134217728) != 0) {
         var30 = var0.updatedAt;
      }

      return var0.copy(var1, var3, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21, var22, var23, var24, var25, var26, var27, var28, var29, var30);
   }

   @NotNull
   public String toString() {
      return "MedicationEntity(id=" + this.id + ", patientId=" + this.patientId + ", transcribedName=" + this.transcribedName + ", commercialName=" + this.commercialName + ", activeIngredient=" + this.activeIngredient + ", pharmaceuticalForm=" + this.pharmaceuticalForm + ", concentration=" + this.concentration + ", indicatedQuantity=" + this.indicatedQuantity + ", measurementUnit=" + this.measurementUnit + ", prescribedDose=" + this.prescribedDose + ", administrationRoute=" + this.administrationRoute + ", transcribedSchedules=" + this.transcribedSchedules + ", exactScheduleHours=" + this.exactScheduleHours + ", specialInstructions=" + this.specialInstructions + ", transcribedFunction=" + this.transcribedFunction + ", startDate=" + this.startDate + ", endDate=" + this.endDate + ", prescriberSource=" + this.prescriberSource + ", documentRef=" + this.documentRef + ", verificationStatus=" + this.verificationStatus + ", treatmentStatus=" + this.treatmentStatus + ", lastReviewDate=" + this.lastReviewDate + ", createdBy=" + this.createdBy + ", confirmedBy=" + this.confirmedBy + ", notes=" + this.notes + ", duplicateWarning=" + this.duplicateWarning + ", createdAt=" + this.createdAt + ", updatedAt=" + this.updatedAt + ")";
   }

   public int hashCode() {
      int result = Long.hashCode(this.id);
      result = result * 31 + Long.hashCode(this.patientId);
      result = result * 31 + this.transcribedName.hashCode();
      result = result * 31 + (this.commercialName == null ? 0 : this.commercialName.hashCode());
      result = result * 31 + (this.activeIngredient == null ? 0 : this.activeIngredient.hashCode());
      result = result * 31 + (this.pharmaceuticalForm == null ? 0 : this.pharmaceuticalForm.hashCode());
      result = result * 31 + (this.concentration == null ? 0 : this.concentration.hashCode());
      result = result * 31 + (this.indicatedQuantity == null ? 0 : this.indicatedQuantity.hashCode());
      result = result * 31 + (this.measurementUnit == null ? 0 : this.measurementUnit.hashCode());
      result = result * 31 + (this.prescribedDose == null ? 0 : this.prescribedDose.hashCode());
      result = result * 31 + (this.administrationRoute == null ? 0 : this.administrationRoute.hashCode());
      result = result * 31 + (this.transcribedSchedules == null ? 0 : this.transcribedSchedules.hashCode());
      result = result * 31 + (this.exactScheduleHours == null ? 0 : this.exactScheduleHours.hashCode());
      result = result * 31 + (this.specialInstructions == null ? 0 : this.specialInstructions.hashCode());
      result = result * 31 + (this.transcribedFunction == null ? 0 : this.transcribedFunction.hashCode());
      result = result * 31 + (this.startDate == null ? 0 : this.startDate.hashCode());
      result = result * 31 + (this.endDate == null ? 0 : this.endDate.hashCode());
      result = result * 31 + (this.prescriberSource == null ? 0 : this.prescriberSource.hashCode());
      result = result * 31 + (this.documentRef == null ? 0 : this.documentRef.hashCode());
      result = result * 31 + this.verificationStatus.hashCode();
      result = result * 31 + this.treatmentStatus.hashCode();
      result = result * 31 + (this.lastReviewDate == null ? 0 : this.lastReviewDate.hashCode());
      result = result * 31 + this.createdBy.hashCode();
      result = result * 31 + (this.confirmedBy == null ? 0 : this.confirmedBy.hashCode());
      result = result * 31 + (this.notes == null ? 0 : this.notes.hashCode());
      result = result * 31 + Boolean.hashCode(this.duplicateWarning);
      result = result * 31 + (this.createdAt == null ? 0 : this.createdAt.hashCode());
      result = result * 31 + (this.updatedAt == null ? 0 : this.updatedAt.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof MedicationEntity)) {
         return false;
      } else {
         MedicationEntity var2 = (MedicationEntity)other;
         if (this.id != var2.id) {
            return false;
         } else if (this.patientId != var2.patientId) {
            return false;
         } else if (!Intrinsics.areEqual(this.transcribedName, var2.transcribedName)) {
            return false;
         } else if (!Intrinsics.areEqual(this.commercialName, var2.commercialName)) {
            return false;
         } else if (!Intrinsics.areEqual(this.activeIngredient, var2.activeIngredient)) {
            return false;
         } else if (!Intrinsics.areEqual(this.pharmaceuticalForm, var2.pharmaceuticalForm)) {
            return false;
         } else if (!Intrinsics.areEqual(this.concentration, var2.concentration)) {
            return false;
         } else if (!Intrinsics.areEqual(this.indicatedQuantity, var2.indicatedQuantity)) {
            return false;
         } else if (!Intrinsics.areEqual(this.measurementUnit, var2.measurementUnit)) {
            return false;
         } else if (!Intrinsics.areEqual(this.prescribedDose, var2.prescribedDose)) {
            return false;
         } else if (!Intrinsics.areEqual(this.administrationRoute, var2.administrationRoute)) {
            return false;
         } else if (!Intrinsics.areEqual(this.transcribedSchedules, var2.transcribedSchedules)) {
            return false;
         } else if (!Intrinsics.areEqual(this.exactScheduleHours, var2.exactScheduleHours)) {
            return false;
         } else if (!Intrinsics.areEqual(this.specialInstructions, var2.specialInstructions)) {
            return false;
         } else if (!Intrinsics.areEqual(this.transcribedFunction, var2.transcribedFunction)) {
            return false;
         } else if (!Intrinsics.areEqual(this.startDate, var2.startDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.endDate, var2.endDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.prescriberSource, var2.prescriberSource)) {
            return false;
         } else if (!Intrinsics.areEqual(this.documentRef, var2.documentRef)) {
            return false;
         } else if (!Intrinsics.areEqual(this.verificationStatus, var2.verificationStatus)) {
            return false;
         } else if (!Intrinsics.areEqual(this.treatmentStatus, var2.treatmentStatus)) {
            return false;
         } else if (!Intrinsics.areEqual(this.lastReviewDate, var2.lastReviewDate)) {
            return false;
         } else if (!Intrinsics.areEqual(this.createdBy, var2.createdBy)) {
            return false;
         } else if (!Intrinsics.areEqual(this.confirmedBy, var2.confirmedBy)) {
            return false;
         } else if (!Intrinsics.areEqual(this.notes, var2.notes)) {
            return false;
         } else if (this.duplicateWarning != var2.duplicateWarning) {
            return false;
         } else if (!Intrinsics.areEqual(this.createdAt, var2.createdAt)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.updatedAt, var2.updatedAt);
         }
      }
   }
}
