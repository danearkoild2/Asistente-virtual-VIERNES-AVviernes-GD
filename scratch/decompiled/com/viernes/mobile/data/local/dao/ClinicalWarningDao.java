package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import com.viernes.mobile.data.local.entity.ClinicalWarningEntity;
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
   d1 = {"\u0000(\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0002\b\u0005\bg\u0018\u00002\u00020\u0001J\u0016\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u001c\u0010\u0007\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\n0\t0\b2\u0006\u0010\u000b\u001a\u00020\u0005H'J\u0016\u0010\f\u001a\u00020\u00052\u0006\u0010\r\u001a\u00020\nH§@¢\u0006\u0002\u0010\u000e¨\u0006\u000f"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/ClinicalWarningDao;", "", "acknowledgeWarning", "", "warningId", "", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getActiveWarningsForPatient", "Lkotlinx/coroutines/flow/Flow;", "", "Lcom/viernes/mobile/data/local/entity/ClinicalWarningEntity;", "patientId", "insert", "warning", "(Lcom/viernes/mobile/data/local/entity/ClinicalWarningEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_debug"}
)
@Dao
public interface ClinicalWarningDao {
   @Query("SELECT * FROM clinical_warnings WHERE patientId = :patientId AND acknowledged = 0 ORDER BY id DESC")
   @NotNull
   Flow<List<ClinicalWarningEntity>> getActiveWarningsForPatient(long var1);

   @Insert(
      onConflict = 1
   )
   @Nullable
   Object insert(@NotNull ClinicalWarningEntity var1, @NotNull Continuation<? super Long> var2);

   @Query("UPDATE clinical_warnings SET acknowledged = 1 WHERE id = :warningId")
   @Nullable
   Object acknowledgeWarning(long var1, @NotNull Continuation<? super Unit> var3);
}
