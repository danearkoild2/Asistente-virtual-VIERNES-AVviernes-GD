package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import com.viernes.mobile.data.local.entity.SyncQueueEntity;
import java.util.List;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000.\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\t\n\u0000\n\u0002\u0010 \n\u0002\b\u0004\n\u0002\u0010\u000e\n\u0002\b\u0002\bg\u0018\u00002\u00020\u0001J\u0016\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u0016\u0010\u0007\u001a\u00020\b2\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u0014\u0010\t\u001a\b\u0012\u0004\u0012\u00020\u00050\nH§@¢\u0006\u0002\u0010\u000bJ\u001e\u0010\f\u001a\u00020\u00032\u0006\u0010\r\u001a\u00020\b2\u0006\u0010\u000e\u001a\u00020\u000fH§@¢\u0006\u0002\u0010\u0010¨\u0006\u0011"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/SyncQueueDao;", "", "delete", "", "item", "Lcom/viernes/mobile/data/local/entity/SyncQueueEntity;", "(Lcom/viernes/mobile/data/local/entity/SyncQueueEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "enqueue", "", "getPendingSyncItems", "", "(Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "recordAttemptFailure", "id", "error", "", "(JLjava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_debug"}
)
@Dao
public interface SyncQueueDao {
   @Query("SELECT * FROM sync_queue ORDER BY id ASC LIMIT 50")
   @Nullable
   Object getPendingSyncItems(@NotNull Continuation<? super List<SyncQueueEntity>> var1);

   @Insert
   @Nullable
   Object enqueue(@NotNull SyncQueueEntity var1, @NotNull Continuation<? super Long> var2);

   @Delete
   @Nullable
   Object delete(@NotNull SyncQueueEntity var1, @NotNull Continuation<? super Unit> var2);

   @Query("UPDATE sync_queue SET attempts = attempts + 1, lastError = :error WHERE id = :id")
   @Nullable
   Object recordAttemptFailure(long var1, @NotNull String var3, @NotNull Continuation<? super Unit> var4);
}
