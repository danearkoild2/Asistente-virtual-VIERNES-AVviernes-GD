package com.viernes.mobile.ui.navigation;

import androidx.compose.runtime.internal.StabilityInferred;
import kotlin.Metadata;
import kotlin.jvm.internal.DefaultConstructorMarker;
import org.jetbrains.annotations.NotNull;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000`\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0016\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\b7\u0018\u00002\u00020\u0001:\u0013\u0007\b\t\n\u000b\f\r\u000e\u000f\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019B\u000f\b\u0004\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004R\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0005\u0010\u0006\u0082\u0001\u0013\u001a\u001b\u001c\u001d\u001e\u001f !\"#$%&'()*+,¨\u0006-"},
   d2 = {"Lcom/viernes/mobile/ui/navigation/Screen;", "", "route", "", "(Ljava/lang/String;)V", "getRoute", "()Ljava/lang/String;", "Appointments", "Caregivers", "Chat", "History", "Home", "HuoAvatar", "IntakeAgenda", "IntakeDetailConfirm", "Inventory", "MedicalCenter", "PatientDetail", "PatientList", "PrivacyPermissions", "RecipeImport", "Refills", "Settings", "SyncStatus", "TreatmentDetail", "TreatmentList", "Lcom/viernes/mobile/ui/navigation/Screen$Appointments;", "Lcom/viernes/mobile/ui/navigation/Screen$Caregivers;", "Lcom/viernes/mobile/ui/navigation/Screen$Chat;", "Lcom/viernes/mobile/ui/navigation/Screen$History;", "Lcom/viernes/mobile/ui/navigation/Screen$Home;", "Lcom/viernes/mobile/ui/navigation/Screen$HuoAvatar;", "Lcom/viernes/mobile/ui/navigation/Screen$IntakeAgenda;", "Lcom/viernes/mobile/ui/navigation/Screen$IntakeDetailConfirm;", "Lcom/viernes/mobile/ui/navigation/Screen$Inventory;", "Lcom/viernes/mobile/ui/navigation/Screen$MedicalCenter;", "Lcom/viernes/mobile/ui/navigation/Screen$PatientDetail;", "Lcom/viernes/mobile/ui/navigation/Screen$PatientList;", "Lcom/viernes/mobile/ui/navigation/Screen$PrivacyPermissions;", "Lcom/viernes/mobile/ui/navigation/Screen$RecipeImport;", "Lcom/viernes/mobile/ui/navigation/Screen$Refills;", "Lcom/viernes/mobile/ui/navigation/Screen$Settings;", "Lcom/viernes/mobile/ui/navigation/Screen$SyncStatus;", "Lcom/viernes/mobile/ui/navigation/Screen$TreatmentDetail;", "Lcom/viernes/mobile/ui/navigation/Screen$TreatmentList;", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public abstract sealed class Screen {
   @NotNull
   private final String route;
   public static final int $stable;

   private Screen(String route) {
      this.route = route;
   }

   @NotNull
   public final String getRoute() {
      return this.route;
   }

   // $FF: synthetic method
   public Screen(String route, DefaultConstructorMarker $constructor_marker) {
      this(route);
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002¨\u0006\u0003"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$Home;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class Home extends Screen {
      @NotNull
      public static final Home INSTANCE = new Home();
      public static final int $stable;

      private Home() {
         super("home", (DefaultConstructorMarker)null);
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002¨\u0006\u0003"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$MedicalCenter;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class MedicalCenter extends Screen {
      @NotNull
      public static final MedicalCenter INSTANCE = new MedicalCenter();
      public static final int $stable;

      private MedicalCenter() {
         super("medical_center", (DefaultConstructorMarker)null);
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002¨\u0006\u0003"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$PatientList;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class PatientList extends Screen {
      @NotNull
      public static final PatientList INSTANCE = new PatientList();
      public static final int $stable;

      private PatientList() {
         super("patients", (DefaultConstructorMarker)null);
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$PatientDetail;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "patientId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class PatientDetail extends Screen {
      @NotNull
      public static final PatientDetail INSTANCE = new PatientDetail();
      public static final int $stable;

      private PatientDetail() {
         super("patient/{patientId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long patientId) {
         return "patient/" + patientId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$TreatmentList;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "patientId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class TreatmentList extends Screen {
      @NotNull
      public static final TreatmentList INSTANCE = new TreatmentList();
      public static final int $stable;

      private TreatmentList() {
         super("treatments/{patientId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long patientId) {
         return "treatments/" + patientId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$TreatmentDetail;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "medicationId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class TreatmentDetail extends Screen {
      @NotNull
      public static final TreatmentDetail INSTANCE = new TreatmentDetail();
      public static final int $stable;

      private TreatmentDetail() {
         super("treatment_detail/{medicationId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long medicationId) {
         return "treatment_detail/" + medicationId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$IntakeAgenda;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "patientId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class IntakeAgenda extends Screen {
      @NotNull
      public static final IntakeAgenda INSTANCE = new IntakeAgenda();
      public static final int $stable;

      private IntakeAgenda() {
         super("intake_agenda/{patientId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long patientId) {
         return "intake_agenda/" + patientId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$IntakeDetailConfirm;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "intakeId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class IntakeDetailConfirm extends Screen {
      @NotNull
      public static final IntakeDetailConfirm INSTANCE = new IntakeDetailConfirm();
      public static final int $stable;

      private IntakeDetailConfirm() {
         super("intake_confirm/{intakeId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long intakeId) {
         return "intake_confirm/" + intakeId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$Appointments;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "patientId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class Appointments extends Screen {
      @NotNull
      public static final Appointments INSTANCE = new Appointments();
      public static final int $stable;

      private Appointments() {
         super("appointments/{patientId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long patientId) {
         return "appointments/" + patientId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$Inventory;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "patientId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class Inventory extends Screen {
      @NotNull
      public static final Inventory INSTANCE = new Inventory();
      public static final int $stable;

      private Inventory() {
         super("inventory/{patientId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long patientId) {
         return "inventory/" + patientId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$Refills;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "patientId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class Refills extends Screen {
      @NotNull
      public static final Refills INSTANCE = new Refills();
      public static final int $stable;

      private Refills() {
         super("refills/{patientId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long patientId) {
         return "refills/" + patientId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$History;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "patientId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class History extends Screen {
      @NotNull
      public static final History INSTANCE = new History();
      public static final int $stable;

      private History() {
         super("history/{patientId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long patientId) {
         return "history/" + patientId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$Caregivers;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "patientId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class Caregivers extends Screen {
      @NotNull
      public static final Caregivers INSTANCE = new Caregivers();
      public static final int $stable;

      private Caregivers() {
         super("caregivers/{patientId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long patientId) {
         return "caregivers/" + patientId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$RecipeImport;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "createRoute", "", "patientId", "", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class RecipeImport extends Screen {
      @NotNull
      public static final RecipeImport INSTANCE = new RecipeImport();
      public static final int $stable;

      private RecipeImport() {
         super("recipe_import/{patientId}", (DefaultConstructorMarker)null);
      }

      @NotNull
      public final String createRoute(long patientId) {
         return "recipe_import/" + patientId;
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002¨\u0006\u0003"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$Chat;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class Chat extends Screen {
      @NotNull
      public static final Chat INSTANCE = new Chat();
      public static final int $stable;

      private Chat() {
         super("chat", (DefaultConstructorMarker)null);
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002¨\u0006\u0003"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$HuoAvatar;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class HuoAvatar extends Screen {
      @NotNull
      public static final HuoAvatar INSTANCE = new HuoAvatar();
      public static final int $stable;

      private HuoAvatar() {
         super("avatar", (DefaultConstructorMarker)null);
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002¨\u0006\u0003"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$Settings;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class Settings extends Screen {
      @NotNull
      public static final Settings INSTANCE = new Settings();
      public static final int $stable;

      private Settings() {
         super("settings", (DefaultConstructorMarker)null);
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002¨\u0006\u0003"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$PrivacyPermissions;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class PrivacyPermissions extends Screen {
      @NotNull
      public static final PrivacyPermissions INSTANCE = new PrivacyPermissions();
      public static final int $stable;

      private PrivacyPermissions() {
         super("privacy_permissions", (DefaultConstructorMarker)null);
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002¨\u0006\u0003"},
      d2 = {"Lcom/viernes/mobile/ui/navigation/Screen$SyncStatus;", "Lcom/viernes/mobile/ui/navigation/Screen;", "()V", "app_debug"}
   )
   @StabilityInferred(
      parameters = 1
   )
   public static final class SyncStatus extends Screen {
      @NotNull
      public static final SyncStatus INSTANCE = new SyncStatus();
      public static final int $stable;

      private SyncStatus() {
         super("sync_status", (DefaultConstructorMarker)null);
      }
   }
}
