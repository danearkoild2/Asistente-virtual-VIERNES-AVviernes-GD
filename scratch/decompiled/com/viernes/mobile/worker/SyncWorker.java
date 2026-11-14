package com.viernes.mobile.worker;

import android.content.Context;
import androidx.compose.runtime.internal.StabilityInferred;
import androidx.work.BackoffPolicy;
import androidx.work.Constraints;
import androidx.work.CoroutineWorker;
import androidx.work.Data;
import androidx.work.ExistingPeriodicWorkPolicy;
import androidx.work.ListenableWorker;
import androidx.work.NetworkType;
import androidx.work.OneTimeWorkRequest;
import androidx.work.PeriodicWorkRequest;
import androidx.work.WorkManager;
import androidx.work.WorkRequest;
import androidx.work.WorkerParameters;
import androidx.work.ListenableWorker.Result;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.repository.SyncRepository;
import java.util.concurrent.TimeUnit;
import kotlin.Metadata;
import kotlin.Pair;
import kotlin.ResultKt;
import kotlin.TuplesKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.Boxing;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000 \n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0003\b\u0007\u0018\u0000 \n2\u00020\u0001:\u0001\nB\u0015\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005¢\u0006\u0002\u0010\u0006J\u000e\u0010\u0007\u001a\u00020\bH\u0096@¢\u0006\u0002\u0010\t¨\u0006\u000b"},
   d2 = {"Lcom/viernes/mobile/worker/SyncWorker;", "Landroidx/work/CoroutineWorker;", "appContext", "Landroid/content/Context;", "workerParams", "Landroidx/work/WorkerParameters;", "(Landroid/content/Context;Landroidx/work/WorkerParameters;)V", "doWork", "Landroidx/work/ListenableWorker$Result;", "(Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "Companion", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
@SourceDebugExtension({"SMAP\nSyncWorker.kt\nKotlin\n*S Kotlin\n*F\n+ 1 SyncWorker.kt\ncom/viernes/mobile/worker/SyncWorker\n+ 2 Data.kt\nandroidx/work/DataKt\n*L\n1#1,63:1\n31#2,5:64\n31#2,5:69\n*S KotlinDebug\n*F\n+ 1 SyncWorker.kt\ncom/viernes/mobile/worker/SyncWorker\n*L\n20#1:64,5\n25#1:69,5\n*E\n"})
public final class SyncWorker extends CoroutineWorker {
   @NotNull
   public static final Companion Companion = new Companion((DefaultConstructorMarker)null);
   public static final int $stable;
   @NotNull
   private static final String UNIQUE_WORK_NAME = "ViernesBackgroundSyncWorker";

   public SyncWorker(@NotNull Context appContext, @NotNull WorkerParameters workerParams) {
      Intrinsics.checkNotNullParameter(appContext, "appContext");
      Intrinsics.checkNotNullParameter(workerParams, "workerParams");
      super(appContext, workerParams);
   }

   @Nullable
   public Object doWork(@NotNull Continuation<? super ListenableWorker.Result> var1) {
      label77: {
         if (var1 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label77;
            }
         }

         $continuation = new ContinuationImpl(var1) {
            Object L$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return SyncWorker.this.doWork((Continuation)this);
            }
         };
      }

      ListenableWorker.Result var4;
      Exception var10000;
      label70: {
         Object $result = $continuation.result;
         Object var15 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
         Object var29;
         switch ($continuation.label) {
            case 0:
               ResultKt.throwOnFailure($result);
               ViernesDatabase.Companion var30 = ViernesDatabase.Companion;
               Context var34 = this.getApplicationContext();
               Intrinsics.checkNotNullExpressionValue(var34, "getApplicationContext(...)");
               ViernesDatabase db = var30.getInstance(var34);
               SyncRepository syncRepo = new SyncRepository(db);

               try {
                  $continuation.L$0 = this;
                  $continuation.label = 1;
                  var29 = syncRepo.processQueue($continuation);
               } catch (Exception var17) {
                  var10000 = var17;
                  boolean var35 = false;
                  break label70;
               }

               if (var29 == var15) {
                  return var15;
               }
               break;
            case 1:
               this = (SyncWorker)$continuation.L$0;

               try {
                  ResultKt.throwOnFailure($result);
                  var29 = $result;
                  break;
               } catch (Exception var18) {
                  var10000 = var18;
                  boolean var10001 = false;
                  break label70;
               }
            default:
               throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
         }

         try {
            int processed = ((Number)var29).intValue();
            Pair[] pairs$iv = new Pair[]{TuplesKt.to("synced_count", Boxing.boxInt(processed))};
            pairs$iv = pairs$iv;
            int $i$f$workDataOf = 0;
            Data.Builder dataBuilder$iv = new Data.Builder();
            int var26 = 0;

            for(int var27 = pairs$iv.length; var26 < var27; ++var26) {
               Pair pair$iv = pairs$iv[var26];
               dataBuilder$iv.put((String)pair$iv.getFirst(), pair$iv.getSecond());
            }

            Data var33 = dataBuilder$iv.build();
            Intrinsics.checkNotNullExpressionValue(var33, "dataBuilder.build()");
            ListenableWorker.Result var19 = Result.success(var33);
            Intrinsics.checkNotNull(var19);
            var4 = var19;
            return var4;
         } catch (Exception var16) {
            var10000 = var16;
            boolean var36 = false;
         }
      }

      Exception e = var10000;
      ListenableWorker.Result var32;
      if (this.getRunAttemptCount() < 3) {
         var32 = Result.retry();
      } else {
         Pair[] pairs$iv = new Pair[1];
         String var10003 = e.getMessage();
         if (var10003 == null) {
            var10003 = "Unknown sync failure";
         }

         pairs$iv[0] = TuplesKt.to("error", var10003);
         pairs$iv = pairs$iv;
         int $i$f$workDataOf = 0;
         Data.Builder dataBuilder$iv = new Data.Builder();
         int var10 = 0;

         for(int pair$iv = pairs$iv.length; var10 < pair$iv; ++var10) {
            Pair pair$iv = pairs$iv[var10];
            dataBuilder$iv.put((String)pair$iv.getFirst(), pair$iv.getSecond());
         }

         Data var31 = dataBuilder$iv.build();
         Intrinsics.checkNotNullExpressionValue(var31, "dataBuilder.build()");
         var32 = Result.failure(var31);
      }

      ListenableWorker.Result pairs$iv = var32;
      Intrinsics.checkNotNull(pairs$iv);
      var4 = pairs$iv;
      return var4;
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000 \n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u0086\u0003\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0005\u001a\u00020\u00062\u0006\u0010\u0007\u001a\u00020\bJ\u000e\u0010\t\u001a\u00020\u00062\u0006\u0010\u0007\u001a\u00020\bR\u000e\u0010\u0003\u001a\u00020\u0004X\u0082T¢\u0006\u0002\n\u0000¨\u0006\n"},
      d2 = {"Lcom/viernes/mobile/worker/SyncWorker$Companion;", "", "()V", "UNIQUE_WORK_NAME", "", "schedulePeriodicSync", "", "context", "Landroid/content/Context;", "triggerImmediateSync", "app_debug"}
   )
   @SourceDebugExtension({"SMAP\nSyncWorker.kt\nKotlin\n*S Kotlin\n*F\n+ 1 SyncWorker.kt\ncom/viernes/mobile/worker/SyncWorker$Companion\n+ 2 PeriodicWorkRequest.kt\nandroidx/work/PeriodicWorkRequestKt\n+ 3 OneTimeWorkRequest.kt\nandroidx/work/OneTimeWorkRequestKt\n*L\n1#1,63:1\n272#2:64\n100#3:65\n*S KotlinDebug\n*F\n+ 1 SyncWorker.kt\ncom/viernes/mobile/worker/SyncWorker$Companion\n*L\n38#1:64\n55#1:65\n*E\n"})
   public static final class Companion {
      private Companion() {
      }

      public final void schedulePeriodicSync(@NotNull Context context) {
         Intrinsics.checkNotNullParameter(context, "context");
         Constraints constraints = (new Constraints.Builder()).setRequiredNetworkType(NetworkType.CONNECTED).build();
         long repeatInterval$iv = 15L;
         TimeUnit repeatIntervalTimeUnit$iv = TimeUnit.MINUTES;
         int $i$f$PeriodicWorkRequestBuilder = 0;
         PeriodicWorkRequest syncRequest = (PeriodicWorkRequest)((PeriodicWorkRequest.Builder)((PeriodicWorkRequest.Builder)(new PeriodicWorkRequest.Builder(SyncWorker.class, repeatInterval$iv, repeatIntervalTimeUnit$iv)).setConstraints(constraints)).setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 1L, TimeUnit.MINUTES)).build();
         WorkManager.getInstance(context).enqueueUniquePeriodicWork("ViernesBackgroundSyncWorker", ExistingPeriodicWorkPolicy.KEEP, syncRequest);
      }

      public final void triggerImmediateSync(@NotNull Context context) {
         Intrinsics.checkNotNullParameter(context, "context");
         Constraints constraints = (new Constraints.Builder()).setRequiredNetworkType(NetworkType.CONNECTED).build();
         int $i$f$OneTimeWorkRequestBuilder = 0;
         OneTimeWorkRequest oneTimeRequest = (OneTimeWorkRequest)((OneTimeWorkRequest.Builder)(new OneTimeWorkRequest.Builder(SyncWorker.class)).setConstraints(constraints)).build();
         WorkManager.getInstance(context).enqueue((WorkRequest)oneTimeRequest);
      }

      // $FF: synthetic method
      public Companion(DefaultConstructorMarker $constructor_marker) {
         this();
      }
   }
}
