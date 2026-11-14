package com.viernes.mobile.ui;

import android.app.Application;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Build.VERSION;
import androidx.activity.ComponentActivity;
import androidx.activity.compose.ComponentActivityKt;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContract;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.compose.runtime.Composable;
import androidx.compose.runtime.ComposableTarget;
import androidx.compose.runtime.Composer;
import androidx.compose.runtime.ComposerKt;
import androidx.compose.runtime.CompositionContext;
import androidx.compose.runtime.internal.ComposableLambdaKt;
import androidx.compose.runtime.internal.StabilityInferred;
import androidx.compose.ui.Modifier;
import androidx.core.content.ContextCompat;
import androidx.navigation.NavHostController;
import androidx.navigation.Navigator;
import androidx.navigation.compose.NavHostControllerKt;
import com.viernes.mobile.ViernesApplication;
import com.viernes.mobile.assistant.ViernesAiAssistant;
import com.viernes.mobile.assistant.VoiceManager;
import com.viernes.mobile.avatar.HuoAvatarController;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.repository.AppointmentRepository;
import com.viernes.mobile.data.repository.IntakeRepository;
import com.viernes.mobile.data.repository.InventoryRepository;
import com.viernes.mobile.data.repository.MedicationRepository;
import com.viernes.mobile.data.repository.PatientRepository;
import com.viernes.mobile.data.repository.RefillRepository;
import com.viernes.mobile.ui.navigation.Screen;
import com.viernes.mobile.ui.navigation.ViernesNavGraphKt;
import com.viernes.mobile.ui.theme.ThemeKt;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.text.StringsKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000>\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0003\b\u0007\u0018\u00002\u00020\u0001B\u0005¢\u0006\u0002\u0010\u0002J\b\u0010\n\u001a\u00020\u000bH\u0002J\u0019\u0010\f\u001a\u0004\u0018\u00010\r2\b\u0010\u000e\u001a\u0004\u0018\u00010\u000fH\u0002¢\u0006\u0002\u0010\u0010J\u0012\u0010\u0011\u001a\u00020\u000b2\b\u0010\u0012\u001a\u0004\u0018\u00010\u0013H\u0014J\b\u0010\u0014\u001a\u00020\u000bH\u0014J\u0010\u0010\u0015\u001a\u00020\u000b2\u0006\u0010\u000e\u001a\u00020\u000fH\u0014R\u000e\u0010\u0003\u001a\u00020\u0004X\u0082.¢\u0006\u0002\n\u0000R\u0014\u0010\u0005\u001a\b\u0012\u0004\u0012\u00020\u00070\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\b\u001a\u00020\tX\u0082.¢\u0006\u0002\n\u0000¨\u0006\u0016"},
   d2 = {"Lcom/viernes/mobile/ui/MainActivity;", "Landroidx/activity/ComponentActivity;", "()V", "huoController", "Lcom/viernes/mobile/avatar/HuoAvatarController;", "requestNotificationPermissionLauncher", "Landroidx/activity/result/ActivityResultLauncher;", "", "voiceManager", "Lcom/viernes/mobile/assistant/VoiceManager;", "checkNotificationPermission", "", "extractIntakeId", "", "intent", "Landroid/content/Intent;", "(Landroid/content/Intent;)Ljava/lang/Long;", "onCreate", "savedInstanceState", "Landroid/os/Bundle;", "onDestroy", "onNewIntent", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
public final class MainActivity extends ComponentActivity {
   private VoiceManager voiceManager;
   private HuoAvatarController huoController;
   @NotNull
   private final ActivityResultLauncher<String> requestNotificationPermissionLauncher = this.registerForActivityResult((ActivityResultContract)(new ActivityResultContracts.RequestPermission()), MainActivity::requestNotificationPermissionLauncher$lambda$0);
   public static final int $stable = 8;

   public MainActivity() {
   }

   protected void onCreate(@Nullable Bundle savedInstanceState) {
      super.onCreate(savedInstanceState);
      Application var10000 = this.getApplication();
      Intrinsics.checkNotNull(var10000, "null cannot be cast to non-null type com.viernes.mobile.ViernesApplication");
      ViernesApplication app = (ViernesApplication)var10000;
      ViernesDatabase db = app.getDatabase();
      final PatientRepository patientRepo = new PatientRepository(db);
      final MedicationRepository medRepo = new MedicationRepository(db);
      final IntakeRepository intakeRepo = new IntakeRepository(db);
      final AppointmentRepository appointmentRepo = new AppointmentRepository(db);
      final RefillRepository refillRepo = new RefillRepository(db);
      final InventoryRepository inventoryRepo = new InventoryRepository(db);
      this.voiceManager = new VoiceManager((Context)this);
      this.huoController = new HuoAvatarController((Context)this);
      final ViernesAiAssistant assistant = new ViernesAiAssistant(db, (String)null, (String)null, 6, (DefaultConstructorMarker)null);
      this.checkNotificationPermission();
      final Long incomingIntakeId = this.extractIntakeId(this.getIntent());
      ComponentActivityKt.setContent$default(this, (CompositionContext)null, (Function2)ComposableLambdaKt.composableLambdaInstance(619489271, true, new Function2<Composer, Integer, Unit>() {
         @Composable
         @ComposableTarget(
            applier = "androidx.compose.ui.UiComposable"
         )
         public final void invoke(@Nullable Composer $composer, int $changed) {
            ComposerKt.sourceInformation($composer, "C56@2141L908:MainActivity.kt#qnltj5");
            if (($changed & 11) == 2 && $composer.getSkipping()) {
               $composer.skipToGroupEnd();
            } else {
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventStart(619489271, $changed, -1, "com.viernes.mobile.ui.MainActivity.onCreate.<anonymous> (MainActivity.kt:56)");
               }

               ThemeKt.ViernesMobileTheme(false, (Function2)ComposableLambdaKt.composableLambda($composer, -2043212130, true, new Function2<Composer, Integer, Unit>() {
                  @Composable
                  @ComposableTarget(
                     applier = "androidx.compose.ui.UiComposable"
                  )
                  public final void invoke(@Nullable Composer $composer, int $changed) {
                     ComposerKt.sourceInformation($composer, "C57@2198L23,65@2469L566:MainActivity.kt#qnltj5");
                     if (($changed & 11) == 2 && $composer.getSkipping()) {
                        $composer.skipToGroupEnd();
                     } else {
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventStart(-2043212130, $changed, -1, "com.viernes.mobile.ui.MainActivity.onCreate.<anonymous>.<anonymous> (MainActivity.kt:57)");
                        }

                        NavHostController navController = NavHostControllerKt.rememberNavController(new Navigator[0], $composer, 8);
                        String startDestination = incomingIntakeId != null ? Screen.IntakeDetailConfirm.INSTANCE.createRoute(incomingIntakeId) : Screen.Home.INSTANCE.getRoute();
                        PatientRepository var10001 = patientRepo;
                        MedicationRepository var10002 = medRepo;
                        IntakeRepository var10003 = intakeRepo;
                        AppointmentRepository var10004 = appointmentRepo;
                        RefillRepository var10005 = refillRepo;
                        InventoryRepository var10006 = inventoryRepo;
                        VoiceManager var10007 = MainActivity.this.voiceManager;
                        if (var10007 == null) {
                           Intrinsics.throwUninitializedPropertyAccessException("voiceManager");
                           var10007 = null;
                        }

                        HuoAvatarController var10008 = MainActivity.this.huoController;
                        if (var10008 == null) {
                           Intrinsics.throwUninitializedPropertyAccessException("huoController");
                           var10008 = null;
                        }

                        ViernesNavGraphKt.ViernesNavGraph(navController, var10001, var10002, var10003, var10004, var10005, var10006, var10007, var10008, assistant, (Modifier)null, startDestination, $composer, 1224736776, 0, 1024);
                        if (ComposerKt.isTraceInProgress()) {
                           ComposerKt.traceEventEnd();
                        }
                     }

                  }
               }), $composer, 48, 1);
               if (ComposerKt.isTraceInProgress()) {
                  ComposerKt.traceEventEnd();
               }
            }

         }
      }), 1, (Object)null);
   }

   protected void onNewIntent(@NotNull Intent intent) {
      Intrinsics.checkNotNullParameter(intent, "intent");
      super.onNewIntent(intent);
      this.setIntent(intent);
   }

   private final void checkNotificationPermission() {
      if (VERSION.SDK_INT >= 33) {
         String permission = "android.permission.POST_NOTIFICATIONS";
         if (ContextCompat.checkSelfPermission((Context)this, permission) != 0) {
            this.requestNotificationPermissionLauncher.launch(permission);
         }
      }

   }

   private final Long extractIntakeId(Intent intent) {
      if (intent == null) {
         return null;
      } else {
         if (intent.hasExtra("intakeId")) {
            long id = intent.getLongExtra("intakeId", -1L);
            if (id != -1L) {
               return id;
            }
         }

         Uri data = intent.getData();
         if (data != null && Intrinsics.areEqual(data.getScheme(), "viernes") && Intrinsics.areEqual(data.getHost(), "intake")) {
            String path = data.getLastPathSegment();
            return path != null ? StringsKt.toLongOrNull(path) : null;
         } else {
            return null;
         }
      }
   }

   protected void onDestroy() {
      super.onDestroy();
      VoiceManager var10000 = this.voiceManager;
      if (var10000 == null) {
         Intrinsics.throwUninitializedPropertyAccessException("voiceManager");
         var10000 = null;
      }

      var10000.release();
      HuoAvatarController var1 = this.huoController;
      if (var1 == null) {
         Intrinsics.throwUninitializedPropertyAccessException("huoController");
         var1 = null;
      }

      var1.release();
   }

   private static final void requestNotificationPermissionLauncher$lambda$0(boolean isGranted) {
   }
}
