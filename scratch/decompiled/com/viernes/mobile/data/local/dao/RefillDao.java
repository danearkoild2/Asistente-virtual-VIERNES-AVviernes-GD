package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;
import com.viernes.mobile.data.local.entity.RefillEntity;
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
   d1 = {"\u00006\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0010 \n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0004\n\u0002\u0010\u0002\n\u0000\bg\u0018\u00002\u00020\u0001J\u0018\u0010\u0002\u001a\u0004\u0018\u00010\u00032\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J$\u0010\u0007\u001a\b\u0012\u0004\u0012\u00020\u00030\b2\u0006\u0010\t\u001a\u00020\u00052\u0006\u0010\n\u001a\u00020\u000bH§@¢\u0006\u0002\u0010\fJ\u001c\u0010\r\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00030\b0\u000e2\u0006\u0010\t\u001a\u00020\u0005H'J\u0016\u0010\u000f\u001a\u00020\u00052\u0006\u0010\u0010\u001a\u00020\u0003H§@¢\u0006\u0002\u0010\u0011J\u0016\u0010\u0012\u001a\u00020\u00132\u0006\u0010\u0010\u001a\u00020\u0003H§@¢\u0006\u0002\u0010\u0011¨\u0006\u0014"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/RefillDao;", "", "getRefillById", "Lcom/viernes/mobile/data/local/entity/RefillEntity;", "id", "", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getRefillsForDateSync", "", "patientId", "date", "", "(JLjava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getRefillsForPatient", "Lkotlinx/coroutines/flow/Flow;", "insert", "refill", "(Lcom/viernes/mobile/data/local/entity/RefillEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "update", "", "app_debug"}
)
@Dao
public interface RefillDao {
   @Query("SELECT * FROM refills WHERE patientId = :patientId ORDER BY scheduledDate ASC")
   @NotNull
   Flow<List<RefillEntity>> getRefillsForPatient(long var1);

   @Query("SELECT * FROM refills WHERE patientId = :patientId AND scheduledDate = :date")
   @Nullable
   Object getRefillsForDateSync(long var1, @NotNull String var3, @NotNull Continuation<? super List<RefillEntity>> var4);

   @Query("SELECT * FROM refills WHERE id = :id")
   @Nullable
   Object getRefillById(long var1, @NotNull Continuation<? super RefillEntity> var3);

   @Insert(
      onConflict = 1
   )
   @Nullable
   Object insert(@NotNull RefillEntity var1, @NotNull Continuation<? super Long> var2);

   @Update
   @Nullable
   Object update(@NotNull RefillEntity var1, @NotNull Continuation<? super Unit> var2);
}
