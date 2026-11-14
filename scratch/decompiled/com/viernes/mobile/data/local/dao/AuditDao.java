package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import com.viernes.mobile.data.local.entity.AuditRecordEntity;
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
   d1 = {"\u0000 \n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0004\bg\u0018\u00002\u00020\u0001J\u001c\u0010\u0002\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00050\u00040\u00032\u0006\u0010\u0006\u001a\u00020\u0007H'J\u0016\u0010\b\u001a\u00020\u00072\u0006\u0010\t\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\n¨\u0006\u000b"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/AuditDao;", "", "getAuditLogsForPatient", "Lkotlinx/coroutines/flow/Flow;", "", "Lcom/viernes/mobile/data/local/entity/AuditRecordEntity;", "patientId", "", "insert", "record", "(Lcom/viernes/mobile/data/local/entity/AuditRecordEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_debug"}
)
@Dao
public interface AuditDao {
   @Query("SELECT * FROM audit_records WHERE patientId = :patientId ORDER BY id DESC LIMIT 100")
   @NotNull
   Flow<List<AuditRecordEntity>> getAuditLogsForPatient(long var1);

   @Insert
   @Nullable
   Object insert(@NotNull AuditRecordEntity var1, @NotNull Continuation<? super Long> var2);
}
