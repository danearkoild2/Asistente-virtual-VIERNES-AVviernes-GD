package com.viernes.mobile.receiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.PowerManager;
import android.util.Log;
import androidx.compose.runtime.internal.StabilityInferred;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlinx.coroutines.BuildersKt;
import kotlinx.coroutines.CoroutineScope;
import kotlinx.coroutines.CoroutineScopeKt;
import kotlinx.coroutines.CoroutineStart;
import kotlinx.coroutines.Dispatchers;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000 \n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u0007\u0018\u0000 \t2\u00020\u0001:\u0001\tB\u0005¢\u0006\u0002\u0010\u0002J\u0018\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u00062\u0006\u0010\u0007\u001a\u00020\bH\u0016¨\u0006\n"},
   d2 = {"Lcom/viernes/mobile/receiver/AlarmReceiver;", "Landroid/content/BroadcastReceiver;", "()V", "onReceive", "", "context", "Landroid/content/Context;", "intent", "Landroid/content/Intent;", "Companion", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class AlarmReceiver extends BroadcastReceiver {
   @NotNull
   public static final Companion Companion = new Companion((DefaultConstructorMarker)null);
   public static final int $stable;
   @NotNull
   private static final String TAG = "AlarmReceiver";

   public AlarmReceiver() {
   }

   public void onReceive(@NotNull final Context context, @NotNull Intent intent) {
      Intrinsics.checkNotNullParameter(context, "context");
      Intrinsics.checkNotNullParameter(intent, "intent");
      final long intakeId = intent.getLongExtra("intakeId", -1L);
      if (intakeId == -1L) {
         Log.e("AlarmReceiver", "Alarma recibida sin intakeId válido.");
      } else {
         Object var10000 = context.getSystemService("power");
         Intrinsics.checkNotNull(var10000, "null cannot be cast to non-null type android.os.PowerManager");
         PowerManager powerManager = (PowerManager)var10000;
         final PowerManager.WakeLock wakeLock = powerManager.newWakeLock(1, "VIERNES:MedicineAlarmWakeLock");
         wakeLock.acquire(30000L);
         final BroadcastReceiver.PendingResult pendingResult = this.goAsync();
         BuildersKt.launch$default(CoroutineScopeKt.CoroutineScope((CoroutineContext)Dispatchers.getIO()), (CoroutineContext)null, (CoroutineStart)null, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
            Object L$0;
            Object L$1;
            Object L$2;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object param1) {
               // $FF: Couldn't be decompiled
            }

            @NotNull
            public final Continuation<Unit> create(@Nullable Object value, @NotNull Continuation<?> $completion) {
               return (Continuation)(new <anonymous constructor>($completion));
            }

            @Nullable
            public final Object invoke(@NotNull CoroutineScope p1, @Nullable Continuation<? super Unit> p2) {
               return ((<undefinedtype>)this.create(p1, p2)).invokeSuspend(Unit.INSTANCE);
            }
         }, 3, (Object)null);
      }
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0012\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\b\u0086\u0003\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002R\u000e\u0010\u0003\u001a\u00020\u0004X\u0082T¢\u0006\u0002\n\u0000¨\u0006\u0005"},
      d2 = {"Lcom/viernes/mobile/receiver/AlarmReceiver$Companion;", "", "()V", "TAG", "", "app_debug"}
   )
   public static final class Companion {
      private Companion() {
      }

      // $FF: synthetic method
      public Companion(DefaultConstructorMarker $constructor_marker) {
         this();
      }
   }
}
