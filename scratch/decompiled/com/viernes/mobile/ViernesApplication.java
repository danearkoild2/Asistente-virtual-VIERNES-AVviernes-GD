package com.viernes.mobile;

import android.app.Application;
import android.content.Context;
import android.util.Log;
import androidx.compose.runtime.internal.StabilityInferred;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.notifications.AlarmScheduler;
import com.viernes.mobile.notifications.NotificationHelper;
import com.viernes.mobile.worker.SyncWorker;
import kotlin.Lazy;
import kotlin.LazyKt;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function2;
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
   d1 = {"\u0000\u001a\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0005\n\u0002\u0010\u0002\n\u0000\b\u0007\u0018\u00002\u00020\u0001B\u0005¢\u0006\u0002\u0010\u0002J\b\u0010\t\u001a\u00020\nH\u0016R\u001b\u0010\u0003\u001a\u00020\u00048FX\u0086\u0084\u0002¢\u0006\f\n\u0004\b\u0007\u0010\b\u001a\u0004\b\u0005\u0010\u0006¨\u0006\u000b"},
   d2 = {"Lcom/viernes/mobile/ViernesApplication;", "Landroid/app/Application;", "()V", "database", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "getDatabase", "()Lcom/viernes/mobile/data/local/ViernesDatabase;", "database$delegate", "Lkotlin/Lazy;", "onCreate", "", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
public final class ViernesApplication extends Application {
   @NotNull
   private final Lazy database$delegate = LazyKt.lazy(new Function0<ViernesDatabase>() {
      @NotNull
      public final ViernesDatabase invoke() {
         return ViernesDatabase.Companion.getInstance((Context)ViernesApplication.this);
      }
   });
   public static final int $stable = 8;

   public ViernesApplication() {
   }

   @NotNull
   public final ViernesDatabase getDatabase() {
      Lazy var1 = this.database$delegate;
      return (ViernesDatabase)var1.getValue();
   }

   public void onCreate() {
      super.onCreate();
      NotificationHelper.INSTANCE.createNotificationChannels((Context)this);
      SyncWorker.Companion.schedulePeriodicSync((Context)this);
      BuildersKt.launch$default(CoroutineScopeKt.CoroutineScope((CoroutineContext)Dispatchers.getIO()), (CoroutineContext)null, (CoroutineStart)null, new Function2<CoroutineScope, Continuation<? super Unit>, Object>((Continuation)null) {
         int label;

         @Nullable
         public final Object invokeSuspend(@NotNull Object $result) {
            Exception var10000;
            label34: {
               Object var3 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
               switch (this.label) {
                  case 0:
                     ResultKt.throwOnFailure($result);

                     try {
                        AlarmScheduler var7 = AlarmScheduler.INSTANCE;
                        Context var10 = (Context)ViernesApplication.this;
                        Continuation var10002 = (Continuation)this;
                        this.label = 1;
                        var8 = var7.rescheduleAllPendingAlarms(var10, var10002);
                     } catch (Exception var5) {
                        var10000 = var5;
                        boolean var9 = false;
                        break label34;
                     }

                     if (var8 == var3) {
                        return var3;
                     }
                     break;
                  case 1:
                     try {
                        ResultKt.throwOnFailure($result);
                        break;
                     } catch (Exception var6) {
                        var10000 = var6;
                        boolean var10001 = false;
                        break label34;
                     }
                  default:
                     throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
               }

               try {
                  return Unit.INSTANCE;
               } catch (Exception var4) {
                  var10000 = var4;
                  boolean var11 = false;
               }
            }

            Exception e = var10000;
            Log.e("ViernesApp", "Error al inicializar alarmas: " + e.getMessage());
            return Unit.INSTANCE;
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
