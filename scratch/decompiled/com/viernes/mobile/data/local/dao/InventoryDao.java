package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import com.viernes.mobile.data.local.entity.InventoryEntity;
import com.viernes.mobile.data.local.entity.InventoryMovementEntity;
import java.util.List;
import kotlin.Metadata;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000(\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0004\n\u0002\u0018\u0002\n\u0002\b\u0007\bg\u0018\u00002\u00020\u0001J\u001c\u0010\u0002\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00050\u00040\u00032\u0006\u0010\u0006\u001a\u00020\u0007H'J \u0010\b\u001a\u0004\u0018\u00010\u00052\u0006\u0010\u0006\u001a\u00020\u00072\u0006\u0010\t\u001a\u00020\u0007H§@¢\u0006\u0002\u0010\nJ\u001c\u0010\u000b\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\f0\u00040\u00032\u0006\u0010\u0006\u001a\u00020\u0007H'J\u0016\u0010\r\u001a\u00020\u00072\u0006\u0010\u000e\u001a\u00020\fH§@¢\u0006\u0002\u0010\u000fJ\u0016\u0010\u0010\u001a\u00020\u00072\u0006\u0010\u0011\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0012¨\u0006\u0013"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/InventoryDao;", "", "getInventoryForPatient", "Lkotlinx/coroutines/flow/Flow;", "", "Lcom/viernes/mobile/data/local/entity/InventoryEntity;", "patientId", "", "getInventoryItem", "medicationId", "(JJLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getMovementsForPatient", "Lcom/viernes/mobile/data/local/entity/InventoryMovementEntity;", "insertMovement", "movement", "(Lcom/viernes/mobile/data/local/entity/InventoryMovementEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "insertOrUpdate", "inventory", "(Lcom/viernes/mobile/data/local/entity/InventoryEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_debug"}
)
@Dao
public interface InventoryDao {
   @Query("SELECT * FROM inventory WHERE patientId = :patientId ORDER BY id ASC")
   @NotNull
   Flow<List<InventoryEntity>> getInventoryForPatient(long var1);

   @Query("SELECT * FROM inventory WHERE patientId = :patientId AND medicationId = :medicationId")
   @Nullable
   Object getInventoryItem(long var1, long var3, @NotNull Continuation<? super InventoryEntity> var5);

   @Insert(
      onConflict = 1
   )
   @Nullable
   Object insertOrUpdate(@NotNull InventoryEntity var1, @NotNull Continuation<? super Long> var2);

   @Insert
   @Nullable
   Object insertMovement(@NotNull InventoryMovementEntity var1, @NotNull Continuation<? super Long> var2);

   @Query("SELECT * FROM inventory_movements WHERE patientId = :patientId ORDER BY id DESC LIMIT 50")
   @NotNull
   Flow<List<InventoryMovementEntity>> getMovementsForPatient(long var1);
}
