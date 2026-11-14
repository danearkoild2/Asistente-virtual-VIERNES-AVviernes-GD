package com.viernes.mobile.notifications;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Build.VERSION;
import android.util.Log;
import androidx.compose.runtime.internal.StabilityInferred;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.local.dao.IntakeDao;
import com.viernes.mobile.data.local.dao.MedicationDao;
import com.viernes.mobile.data.local.dao.PatientDao;
import com.viernes.mobile.data.local.entity.IntakeEntity;
import com.viernes.mobile.data.local.entity.MedicationEntity;
import com.viernes.mobile.data.local.entity.PatientEntity;
import com.viernes.mobile.domain.model.Intake;
import com.viernes.mobile.domain.model.IntakeStatus;
import com.viernes.mobile.receiver.AlarmReceiver;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Iterator;
import java.util.List;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.text.StringsKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u00004\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0010\u000b\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0000\bÇ\u0002\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0006\u001a\u00020\u00072\u0006\u0010\b\u001a\u00020\tJ\u0016\u0010\n\u001a\u00020\u000b2\u0006\u0010\b\u001a\u00020\t2\u0006\u0010\f\u001a\u00020\rJ\u0016\u0010\u000e\u001a\u00020\u000b2\u0006\u0010\b\u001a\u00020\tH\u0086@¢\u0006\u0002\u0010\u000fJ\u0016\u0010\u0010\u001a\u00020\u000b2\u0006\u0010\b\u001a\u00020\t2\u0006\u0010\u0011\u001a\u00020\u0012R\u000e\u0010\u0003\u001a\u00020\u0004X\u0086T¢\u0006\u0002\n\u0000R\u000e\u0010\u0005\u001a\u00020\u0004X\u0082T¢\u0006\u0002\n\u0000¨\u0006\u0013"},
   d2 = {"Lcom/viernes/mobile/notifications/AlarmScheduler;", "", "()V", "ACTION_MEDICINE_ALARM", "", "TAG", "canScheduleExact", "", "context", "Landroid/content/Context;", "cancelIntakeAlarm", "", "intakeId", "", "rescheduleAllPendingAlarms", "(Landroid/content/Context;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "scheduleIntakeAlarm", "intake", "Lcom/viernes/mobile/domain/model/Intake;", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class AlarmScheduler {
   @NotNull
   public static final AlarmScheduler INSTANCE = new AlarmScheduler();
   @NotNull
   private static final String TAG = "AlarmScheduler";
   @NotNull
   public static final String ACTION_MEDICINE_ALARM = "com.viernes.mobile.ACTION_MEDICINE_ALARM";
   public static final int $stable;

   private AlarmScheduler() {
   }

   public final boolean canScheduleExact(@NotNull Context context) {
      Intrinsics.checkNotNullParameter(context, "context");
      if (VERSION.SDK_INT >= 31) {
         Object var10000 = context.getSystemService("alarm");
         Intrinsics.checkNotNull(var10000, "null cannot be cast to non-null type android.app.AlarmManager");
         AlarmManager alarmManager = (AlarmManager)var10000;
         return alarmManager.canScheduleExactAlarms();
      } else {
         return true;
      }
   }

   public final void scheduleIntakeAlarm(@NotNull Context context, @NotNull Intake intake) {
      Intrinsics.checkNotNullParameter(context, "context");
      Intrinsics.checkNotNullParameter(intake, "intake");
      String timeStr = intake.getScheduledTime();
      CharSequence var4 = (CharSequence)timeStr;
      if (var4 == null || StringsKt.isBlank(var4)) {
         Log.d("AlarmScheduler", "Intake #" + intake.getId() + " no tiene hora exacta confirmada. Omitiendo alarma.");
      } else {
         try {
            LocalDate date = LocalDate.parse((CharSequence)intake.getScheduledDate());
            LocalTime time = LocalTime.parse((CharSequence)timeStr, DateTimeFormatter.ofPattern("HH:mm"));
            LocalDateTime targetDateTime = LocalDateTime.of(date, time);
            ZoneId zoneId = ZoneId.systemDefault();
            long triggerEpochMillis = targetDateTime.atZone(zoneId).toInstant().toEpochMilli();
            long nowMillis = System.currentTimeMillis();
            if (triggerEpochMillis <= nowMillis) {
               long var20 = intake.getId();
               Log.d("AlarmScheduler", "Intake #" + var20 + " ya venció (" + targetDateTime + "). No se programa retrospectivamente.");
               return;
            }

            Object var10000 = context.getSystemService("alarm");
            Intrinsics.checkNotNull(var10000, "null cannot be cast to non-null type android.app.AlarmManager");
            AlarmManager alarmManager = (AlarmManager)var10000;
            Intent $this$scheduleIntakeAlarm_u24lambda_u240 = new Intent(context, AlarmReceiver.class);
            int var16 = 0;
            $this$scheduleIntakeAlarm_u24lambda_u240.setAction("com.viernes.mobile.ACTION_MEDICINE_ALARM");
            $this$scheduleIntakeAlarm_u24lambda_u240.putExtra("intakeId", intake.getId());
            $this$scheduleIntakeAlarm_u24lambda_u240.putExtra("patientId", intake.getPatientId());
            $this$scheduleIntakeAlarm_u24lambda_u240.putExtra("medicationId", intake.getMedicationId());
            $this$scheduleIntakeAlarm_u24lambda_u240.putExtra("scheduledTime", timeStr);
            PendingIntent pendingIntent = PendingIntent.getBroadcast(context, (int)intake.getId(), $this$scheduleIntakeAlarm_u24lambda_u240, 201326592);
            if (VERSION.SDK_INT >= 23) {
               alarmManager.setExactAndAllowWhileIdle(0, triggerEpochMillis, pendingIntent);
            } else {
               alarmManager.setExact(0, triggerEpochMillis, pendingIntent);
            }

            long var10001 = intake.getId();
            Log.i("AlarmScheduler", "Alarma programada exitosamente para Intake #" + var10001 + " a las " + targetDateTime);
         } catch (Exception e) {
            Log.e("AlarmScheduler", "Error programando alarma para Intake #" + intake.getId() + ": " + e.getMessage(), (Throwable)e);
         }

      }
   }

   public final void cancelIntakeAlarm(@NotNull Context context, long intakeId) {
      Intrinsics.checkNotNullParameter(context, "context");

      try {
         Object var10000 = context.getSystemService("alarm");
         Intrinsics.checkNotNull(var10000, "null cannot be cast to non-null type android.app.AlarmManager");
         AlarmManager alarmManager = (AlarmManager)var10000;
         Intent $this$cancelIntakeAlarm_u24lambda_u241 = new Intent(context, AlarmReceiver.class);
         int var8 = 0;
         $this$cancelIntakeAlarm_u24lambda_u241.setAction("com.viernes.mobile.ACTION_MEDICINE_ALARM");
         PendingIntent pendingIntent = PendingIntent.getBroadcast(context, (int)intakeId, $this$cancelIntakeAlarm_u24lambda_u241, 603979776);
         if (pendingIntent != null) {
            alarmManager.cancel(pendingIntent);
            pendingIntent.cancel();
            Log.d("AlarmScheduler", "Alarma cancelada para Intake #" + intakeId);
         }
      } catch (Exception e) {
         Log.e("AlarmScheduler", "Error al cancelar alarma para Intake #" + intakeId + ": " + e.getMessage());
      }

   }

   @Nullable
   public final Object rescheduleAllPendingAlarms(@NotNull Context context, @NotNull Continuation<? super Unit> var2) {
      label76: {
         if (var2 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label76;
            }
         }

         $continuation = new ContinuationImpl(var2) {
            Object L$0;
            Object L$1;
            Object L$2;
            Object L$3;
            Object L$4;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return AlarmScheduler.this.rescheduleAllPendingAlarms((Context)null, (Continuation)this);
            }
         };
      }

      Object $result = $continuation.result;
      Object var12 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      ViernesDatabase db;
      Iterator var6;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            db = ViernesDatabase.Companion.getInstance(context);
            String var23 = LocalDate.now().toString();
            Intrinsics.checkNotNullExpressionValue(var23, "toString(...)");
            String today = var23;
            var23 = LocalTime.now().toString();
            Intrinsics.checkNotNullExpressionValue(var23, "toString(...)");
            StringsKt.take(var23, 5);
            PatientDao var25 = db.patientDao();
            $continuation.L$0 = this;
            $continuation.L$1 = context;
            $continuation.L$2 = db;
            $continuation.L$3 = today;
            $continuation.label = 1;
            Object var26 = var25.getPatientById(1L, $continuation);
            if (var26 == var12) {
               return var12;
            }

            PatientEntity var27 = (PatientEntity)var26;
            IntakeDao var28 = db.intakeDao();
            $continuation.L$0 = this;
            $continuation.L$1 = context;
            $continuation.L$2 = db;
            $continuation.L$3 = null;
            $continuation.label = 2;
            Object var29 = var28.getDueUnnotifiedIntakes(today, "23:59", $continuation);
            if (var29 == var12) {
               return var12;
            }

            List futureIntakes = (List)var29;
            Log.i("AlarmScheduler", "Restaurando alarmas locales para " + futureIntakes.size() + " tomas pendientes...");
            var6 = futureIntakes.iterator();
            break;
         case 1:
            String today = (String)$continuation.L$3;
            db = (ViernesDatabase)$continuation.L$2;
            context = (Context)$continuation.L$1;
            this = (AlarmScheduler)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            PatientEntity var10000 = (PatientEntity)$result;
            IntakeDao var21 = db.intakeDao();
            $continuation.L$0 = this;
            $continuation.L$1 = context;
            $continuation.L$2 = db;
            $continuation.L$3 = null;
            $continuation.label = 2;
            Object var22 = var21.getDueUnnotifiedIntakes(today, "23:59", $continuation);
            if (var22 == var12) {
               return var12;
            }

            List var14 = (List)var22;
            Log.i("AlarmScheduler", "Restaurando alarmas locales para " + var14.size() + " tomas pendientes...");
            var6 = var14.iterator();
            break;
         case 2:
            db = (ViernesDatabase)$continuation.L$2;
            context = (Context)$continuation.L$1;
            this = (AlarmScheduler)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            List var5 = (List)$result;
            Log.i("AlarmScheduler", "Restaurando alarmas locales para " + var5.size() + " tomas pendientes...");
            var6 = var5.iterator();
            break;
         case 3:
            IntakeEntity intakeEntity = (IntakeEntity)$continuation.L$4;
            var6 = (Iterator)$continuation.L$3;
            db = (ViernesDatabase)$continuation.L$2;
            context = (Context)$continuation.L$1;
            this = (AlarmScheduler)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            MedicationEntity var8 = (MedicationEntity)$result;
            if (var8 != null) {
               if (!Intrinsics.areEqual(var8.getVerificationStatus(), "ACTIVE")) {
                  if (Intrinsics.areEqual(var8.getVerificationStatus(), "VERIFIED_PENDING_ACTIVATION")) {
                     Intake var9 = new Intake(intakeEntity.getId(), intakeEntity.getPatientId(), intakeEntity.getMedicationId(), intakeEntity.getScheduledDate(), intakeEntity.getScheduledTime(), (String)null, intakeEntity.getDoseText(), (String)null, (String)null, (IntakeStatus)null, (String)null, (String)null, false, (String)null, (String)null, (String)null, (String)null, (String)null, false, 524192, (DefaultConstructorMarker)null);
                     this.scheduleIntakeAlarm(context, var9);
                  }
               } else {
                  Intake var18 = new Intake(intakeEntity.getId(), intakeEntity.getPatientId(), intakeEntity.getMedicationId(), intakeEntity.getScheduledDate(), intakeEntity.getScheduledTime(), (String)null, intakeEntity.getDoseText(), (String)null, (String)null, (IntakeStatus)null, (String)null, (String)null, false, (String)null, (String)null, (String)null, (String)null, (String)null, false, 524192, (DefaultConstructorMarker)null);
                  this.scheduleIntakeAlarm(context, var18);
               }
            }
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      while(var6.hasNext()) {
         IntakeEntity intakeEntity = (IntakeEntity)var6.next();
         MedicationDao var30 = db.medicationDao();
         long var10001 = intakeEntity.getMedicationId();
         $continuation.L$0 = this;
         $continuation.L$1 = context;
         $continuation.L$2 = db;
         $continuation.L$3 = var6;
         $continuation.L$4 = intakeEntity;
         $continuation.label = 3;
         Object var31 = var30.getMedicationById(var10001, $continuation);
         if (var31 == var12) {
            return var12;
         }

         MedicationEntity med = (MedicationEntity)var31;
         if (med != null) {
            if (!Intrinsics.areEqual(med.getVerificationStatus(), "ACTIVE")) {
               if (Intrinsics.areEqual(med.getVerificationStatus(), "VERIFIED_PENDING_ACTIVATION")) {
                  Intake intake = new Intake(intakeEntity.getId(), intakeEntity.getPatientId(), intakeEntity.getMedicationId(), intakeEntity.getScheduledDate(), intakeEntity.getScheduledTime(), (String)null, intakeEntity.getDoseText(), (String)null, (String)null, (IntakeStatus)null, (String)null, (String)null, false, (String)null, (String)null, (String)null, (String)null, (String)null, false, 524192, (DefaultConstructorMarker)null);
                  this.scheduleIntakeAlarm(context, intake);
               }
            } else {
               Intake var20 = new Intake(intakeEntity.getId(), intakeEntity.getPatientId(), intakeEntity.getMedicationId(), intakeEntity.getScheduledDate(), intakeEntity.getScheduledTime(), (String)null, intakeEntity.getDoseText(), (String)null, (String)null, (IntakeStatus)null, (String)null, (String)null, false, (String)null, (String)null, (String)null, (String)null, (String)null, false, 524192, (DefaultConstructorMarker)null);
               this.scheduleIntakeAlarm(context, var20);
            }
         }
      }

      return Unit.INSTANCE;
   }
}
