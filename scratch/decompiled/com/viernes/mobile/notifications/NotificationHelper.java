package com.viernes.mobile.notifications;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build.VERSION;
import androidx.compose.runtime.internal.StabilityInferred;
import androidx.core.app.NotificationCompat;
import com.viernes.mobile.R.drawable;
import com.viernes.mobile.R.string;
import com.viernes.mobile.ui.MainActivity;
import kotlin.Metadata;
import kotlin.collections.CollectionsKt;
import kotlin.jvm.internal.Intrinsics;
import org.jetbrains.annotations.NotNull;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u00000\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0003\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\t\n\u0002\b\b\n\u0002\u0010\u000b\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0007\u001a\u00020\b2\u0006\u0010\t\u001a\u00020\nJ&\u0010\u000b\u001a\u00020\b2\u0006\u0010\t\u001a\u00020\n2\u0006\u0010\f\u001a\u00020\r2\u0006\u0010\u000e\u001a\u00020\u00042\u0006\u0010\u000f\u001a\u00020\u0004J@\u0010\u0010\u001a\u00020\b2\u0006\u0010\t\u001a\u00020\n2\u0006\u0010\u0011\u001a\u00020\r2\u0006\u0010\u000e\u001a\u00020\u00042\u0006\u0010\u0012\u001a\u00020\u00042\u0006\u0010\u0013\u001a\u00020\u00042\u0006\u0010\u0014\u001a\u00020\u00042\b\b\u0002\u0010\u0015\u001a\u00020\u0016R\u000e\u0010\u0003\u001a\u00020\u0004X\u0086T¢\u0006\u0002\n\u0000R\u000e\u0010\u0005\u001a\u00020\u0004X\u0086T¢\u0006\u0002\n\u0000R\u000e\u0010\u0006\u001a\u00020\u0004X\u0086T¢\u0006\u0002\n\u0000¨\u0006\u0017"},
   d2 = {"Lcom/viernes/mobile/notifications/NotificationHelper;", "", "()V", "CHANNEL_APPOINTMENTS", "", "CHANNEL_MEDICINE", "CHANNEL_WARNINGS", "createNotificationChannels", "", "context", "Landroid/content/Context;", "showClinicalWarningNotification", "warningId", "", "patientName", "message", "showMedicineReminder", "intakeId", "medicationName", "doseText", "scheduledTime", "hideSensitiveDetails", "", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class NotificationHelper {
   @NotNull
   public static final NotificationHelper INSTANCE = new NotificationHelper();
   @NotNull
   public static final String CHANNEL_MEDICINE = "channel_medicine_reminders";
   @NotNull
   public static final String CHANNEL_APPOINTMENTS = "channel_appointments";
   @NotNull
   public static final String CHANNEL_WARNINGS = "channel_clinical_warnings";
   public static final int $stable;

   private NotificationHelper() {
   }

   public final void createNotificationChannels(@NotNull Context context) {
      Intrinsics.checkNotNullParameter(context, "context");
      if (VERSION.SDK_INT >= 26) {
         Object var10000 = context.getSystemService("notification");
         Intrinsics.checkNotNull(var10000, "null cannot be cast to non-null type android.app.NotificationManager");
         NotificationManager notificationManager = (NotificationManager)var10000;
         NotificationChannel $this$createNotificationChannels_u24lambda_u240 = new NotificationChannel("channel_medicine_reminders", (CharSequence)context.getString(string.notification_channel_medicine), 4);
         int $this$createNotificationChannels_u24lambda_u242 = 0;
         $this$createNotificationChannels_u24lambda_u240.setDescription(context.getString(string.notification_channel_medicine_desc));
         $this$createNotificationChannels_u24lambda_u240.enableLights(true);
         $this$createNotificationChannels_u24lambda_u240.enableVibration(true);
         $this$createNotificationChannels_u24lambda_u240.setLockscreenVisibility(0);
         NotificationChannel $this$createNotificationChannels_u24lambda_u240 = new NotificationChannel("channel_appointments", (CharSequence)context.getString(string.notification_channel_appointments), 3);
         int var7 = 0;
         $this$createNotificationChannels_u24lambda_u240.setDescription(context.getString(string.notification_channel_appointments_desc));
         NotificationChannel[] $this$createNotificationChannels_u24lambda_u241 = new NotificationChannel("channel_clinical_warnings", (CharSequence)context.getString(string.notification_channel_warnings), 4);
         int var8 = 0;
         ((NotificationChannel)$this$createNotificationChannels_u24lambda_u241).setDescription(context.getString(string.notification_channel_warnings_desc));
         $this$createNotificationChannels_u24lambda_u241 = new NotificationChannel[]{$this$createNotificationChannels_u24lambda_u240, $this$createNotificationChannels_u24lambda_u240, $this$createNotificationChannels_u24lambda_u241};
         notificationManager.createNotificationChannels(CollectionsKt.listOf($this$createNotificationChannels_u24lambda_u241));
      }

   }

   public final void showMedicineReminder(@NotNull Context context, long intakeId, @NotNull String patientName, @NotNull String medicationName, @NotNull String doseText, @NotNull String scheduledTime, boolean hideSensitiveDetails) {
      Intrinsics.checkNotNullParameter(context, "context");
      Intrinsics.checkNotNullParameter(patientName, "patientName");
      Intrinsics.checkNotNullParameter(medicationName, "medicationName");
      Intrinsics.checkNotNullParameter(doseText, "doseText");
      Intrinsics.checkNotNullParameter(scheduledTime, "scheduledTime");
      Object var10000 = context.getSystemService("notification");
      Intrinsics.checkNotNull(var10000, "null cannot be cast to non-null type android.app.NotificationManager");
      NotificationManager notificationManager = (NotificationManager)var10000;
      Intent $this$showMedicineReminder_u24lambda_u243 = new Intent(context, MainActivity.class);
      int var13 = 0;
      $this$showMedicineReminder_u24lambda_u243.setAction("android.intent.action.VIEW");
      $this$showMedicineReminder_u24lambda_u243.setData(Uri.parse("viernes://intake/" + intakeId));
      $this$showMedicineReminder_u24lambda_u243.setFlags(335544320);
      $this$showMedicineReminder_u24lambda_u243.putExtra("intakeId", intakeId);
      PendingIntent pendingIntent = PendingIntent.getActivity(context, (int)intakeId, $this$showMedicineReminder_u24lambda_u243, 201326592);
      String title = "VIERNES — Recordatorio de medicamentos";
      String body = hideSensitiveDetails ? "Es hora de revisar la toma programada de " + patientName + " (" + scheduledTime + ").\nAbre VIERNES para consultar el medicamento y registrar el resultado." : "Toma para " + patientName + " a las " + scheduledTime + ": " + medicationName + " (" + doseText + ").\nToca para registrar el resultado.";
      Uri defaultSound = RingtoneManager.getDefaultUri(2);
      Notification var18 = (new NotificationCompat.Builder(context, "channel_medicine_reminders")).setSmallIcon(drawable.ic_stat_medicine).setContentTitle((CharSequence)title).setContentText((CharSequence)body).setStyle((NotificationCompat.Style)(new NotificationCompat.BigTextStyle()).bigText((CharSequence)body)).setPriority(1).setCategory("reminder").setVisibility(hideSensitiveDetails ? 0 : 1).setAutoCancel(true).setSound(defaultSound).setContentIntent(pendingIntent).build();
      Intrinsics.checkNotNullExpressionValue(var18, "build(...)");
      Notification notification = var18;
      notificationManager.notify((int)intakeId, notification);
   }

   // $FF: synthetic method
   public static void showMedicineReminder$default(NotificationHelper var0, Context var1, long var2, String var4, String var5, String var6, String var7, boolean var8, int var9, Object var10) {
      if ((var9 & 64) != 0) {
         var8 = true;
      }

      var0.showMedicineReminder(var1, var2, var4, var5, var6, var7, var8);
   }

   public final void showClinicalWarningNotification(@NotNull Context context, long warningId, @NotNull String patientName, @NotNull String message) {
      Intrinsics.checkNotNullParameter(context, "context");
      Intrinsics.checkNotNullParameter(patientName, "patientName");
      Intrinsics.checkNotNullParameter(message, "message");
      Object var10000 = context.getSystemService("notification");
      Intrinsics.checkNotNull(var10000, "null cannot be cast to non-null type android.app.NotificationManager");
      NotificationManager notificationManager = (NotificationManager)var10000;
      Intent $this$showClinicalWarningNotification_u24lambda_u244 = new Intent(context, MainActivity.class);
      int var10 = 0;
      $this$showClinicalWarningNotification_u24lambda_u244.setFlags(335544320);
      PendingIntent pendingIntent = PendingIntent.getActivity(context, (int)warningId, $this$showClinicalWarningNotification_u24lambda_u244, 201326592);
      Notification var12 = (new NotificationCompat.Builder(context, "channel_clinical_warnings")).setSmallIcon(drawable.ic_stat_medicine).setContentTitle((CharSequence)"VIERNES — Advertencia de Seguridad Clínica").setContentText((CharSequence)("Alerta para " + patientName + ": " + message)).setStyle((NotificationCompat.Style)(new NotificationCompat.BigTextStyle()).bigText((CharSequence)("Alerta para " + patientName + ":\n" + message))).setPriority(1).setAutoCancel(true).setContentIntent(pendingIntent).build();
      Intrinsics.checkNotNullExpressionValue(var12, "build(...)");
      Notification notification = var12;
      notificationManager.notify((int)(warningId + (long)900000), notification);
   }
}
