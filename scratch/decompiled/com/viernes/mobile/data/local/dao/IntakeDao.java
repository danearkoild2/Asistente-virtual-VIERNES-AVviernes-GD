package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;
import com.viernes.mobile.data.local.entity.IntakeEntity;
import java.util.List;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000:\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0000\n\u0002\u0010\u000e\n\u0002\b\t\n\u0002\u0010\u000b\n\u0002\b\u0004\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0002\b\u0007\n\u0002\u0018\u0002\n\u0002\b\u000e\bg\u0018\u00002\u00020\u0001J\u001e\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0006\u001a\u00020\u0007H§@¢\u0006\u0002\u0010\bJ8\u0010\t\u001a\u00020\u00032\u0006\u0010\n\u001a\u00020\u00052\u0006\u0010\u000b\u001a\u00020\u00072\u0006\u0010\f\u001a\u00020\u00072\u0006\u0010\r\u001a\u00020\u00072\b\u0010\u000e\u001a\u0004\u0018\u00010\u0007H§@¢\u0006\u0002\u0010\u000fJ&\u0010\u0010\u001a\u00020\u00112\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0012\u001a\u00020\u00072\u0006\u0010\u0013\u001a\u00020\u0007H§@¢\u0006\u0002\u0010\u0014J$\u0010\u0015\u001a\b\u0012\u0004\u0012\u00020\u00170\u00162\u0006\u0010\u0018\u001a\u00020\u00072\u0006\u0010\u0019\u001a\u00020\u0007H§@¢\u0006\u0002\u0010\u001aJ$\u0010\u001b\u001a\b\u0012\u0004\u0012\u00020\u00170\u00162\u0006\u0010\u0018\u001a\u00020\u00072\u0006\u0010\u0019\u001a\u00020\u0007H§@¢\u0006\u0002\u0010\u001aJ\u0018\u0010\u001c\u001a\u0004\u0018\u00010\u00172\u0006\u0010\n\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u001dJ$\u0010\u001e\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00170\u00160\u001f2\u0006\u0010 \u001a\u00020\u00052\u0006\u0010\u0012\u001a\u00020\u0007H'J$\u0010!\u001a\b\u0012\u0004\u0012\u00020\u00170\u00162\u0006\u0010 \u001a\u00020\u00052\u0006\u0010\u0012\u001a\u00020\u0007H§@¢\u0006\u0002\u0010\bJ\u001c\u0010\"\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00170\u00160\u001f2\u0006\u0010\u0018\u001a\u00020\u0007H'J\u0016\u0010#\u001a\u00020\u00052\u0006\u0010$\u001a\u00020\u0017H§@¢\u0006\u0002\u0010%J\"\u0010&\u001a\b\u0012\u0004\u0012\u00020\u00050\u00162\f\u0010'\u001a\b\u0012\u0004\u0012\u00020\u00170\u0016H§@¢\u0006\u0002\u0010(J\u0016\u0010)\u001a\u00020\u00032\u0006\u0010\n\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u001dJ\u001e\u0010*\u001a\u00020\u00032\u0006\u0010\n\u001a\u00020\u00052\u0006\u0010+\u001a\u00020\u0007H§@¢\u0006\u0002\u0010\bJ\u0016\u0010,\u001a\u00020\u00032\u0006\u0010$\u001a\u00020\u0017H§@¢\u0006\u0002\u0010%¨\u0006-"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/IntakeDao;", "", "cancelFuturePendingIntakes", "", "medicationId", "", "fromDate", "", "(JLjava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "confirmIntake", "intakeId", "status", "confirmedAt", "confirmedBy", "notes", "(JLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "existsIntake", "", "date", "time", "(JLjava/lang/String;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getDelayedIntakes", "", "Lcom/viernes/mobile/data/local/entity/IntakeEntity;", "today", "currentTime", "(Ljava/lang/String;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getDueUnnotifiedIntakes", "getIntakeById", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getIntakesForDate", "Lkotlinx/coroutines/flow/Flow;", "patientId", "getIntakesForDateSync", "getUpcomingPendingIntakes", "insert", "intake", "(Lcom/viernes/mobile/data/local/entity/IntakeEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "insertAll", "intakes", "(Ljava/util/List;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "markNotificationSent", "skipIntake", "reason", "update", "app_debug"}
)
@Dao
public interface IntakeDao {
   @Query("SELECT * FROM intakes WHERE patientId = :patientId AND scheduledDate = :date ORDER BY scheduledTime ASC")
   @NotNull
   Flow<List<IntakeEntity>> getIntakesForDate(long var1, @NotNull String var3);

   @Query("SELECT * FROM intakes WHERE patientId = :patientId AND scheduledDate = :date ORDER BY scheduledTime ASC")
   @Nullable
   Object getIntakesForDateSync(long var1, @NotNull String var3, @NotNull Continuation<? super List<IntakeEntity>> var4);

   @Query("SELECT * FROM intakes WHERE id = :intakeId")
   @Nullable
   Object getIntakeById(long var1, @NotNull Continuation<? super IntakeEntity> var3);

   @Query("SELECT * FROM intakes WHERE status = 'PENDING' AND scheduledDate = :today AND scheduledTime <= :currentTime AND notificationSent = 0")
   @Nullable
   Object getDueUnnotifiedIntakes(@NotNull String var1, @NotNull String var2, @NotNull Continuation<? super List<IntakeEntity>> var3);

   @Query("SELECT * FROM intakes WHERE status = 'PENDING' AND (scheduledDate < :today OR (scheduledDate = :today AND scheduledTime < :currentTime))")
   @Nullable
   Object getDelayedIntakes(@NotNull String var1, @NotNull String var2, @NotNull Continuation<? super List<IntakeEntity>> var3);

   @Query("SELECT * FROM intakes WHERE status = 'PENDING' AND scheduledDate >= :today ORDER BY scheduledDate ASC, scheduledTime ASC LIMIT 10")
   @NotNull
   Flow<List<IntakeEntity>> getUpcomingPendingIntakes(@NotNull String var1);

   @Insert(
      onConflict = 1
   )
   @Nullable
   Object insert(@NotNull IntakeEntity var1, @NotNull Continuation<? super Long> var2);

   @Insert(
      onConflict = 1
   )
   @Nullable
   Object insertAll(@NotNull List<IntakeEntity> var1, @NotNull Continuation<? super List<Long>> var2);

   @Update
   @Nullable
   Object update(@NotNull IntakeEntity var1, @NotNull Continuation<? super Unit> var2);

   @Query("UPDATE intakes SET status = :status, confirmedAt = :confirmedAt, confirmedBy = :confirmedBy, notes = :notes WHERE id = :intakeId")
   @Nullable
   Object confirmIntake(long var1, @NotNull String var3, @NotNull String var4, @NotNull String var5, @Nullable String var6, @NotNull Continuation<? super Unit> var7);

   @Query("UPDATE intakes SET status = 'SKIPPED', notes = :reason WHERE id = :intakeId")
   @Nullable
   Object skipIntake(long var1, @NotNull String var3, @NotNull Continuation<? super Unit> var4);

   @Query("UPDATE intakes SET notificationSent = 1, notificationSentAt = datetime('now', 'localtime') WHERE id = :intakeId")
   @Nullable
   Object markNotificationSent(long var1, @NotNull Continuation<? super Unit> var3);

   @Query("SELECT EXISTS(SELECT 1 FROM intakes WHERE medicationId = :medicationId AND scheduledDate = :date AND scheduledTime = :time)")
   @Nullable
   Object existsIntake(long var1, @NotNull String var3, @NotNull String var4, @NotNull Continuation<? super Boolean> var5);

   @Query("DELETE FROM intakes WHERE medicationId = :medicationId AND scheduledDate >= :fromDate AND status = 'PENDING'")
   @Nullable
   Object cancelFuturePendingIntakes(long var1, @NotNull String var3, @NotNull Continuation<? super Unit> var4);
}
