package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;
import com.viernes.mobile.data.local.entity.PatientEntity;
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
   d1 = {"\u0000(\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0002\b\u0006\bg\u0018\u00002\u00020\u0001J\u0016\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u0014\u0010\u0007\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\n0\t0\bH'J\u0018\u0010\u000b\u001a\u0004\u0018\u00010\n2\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u0016\u0010\f\u001a\u00020\u00052\u0006\u0010\r\u001a\u00020\nH§@¢\u0006\u0002\u0010\u000eJ\u0016\u0010\u000f\u001a\u00020\u00032\u0006\u0010\r\u001a\u00020\nH§@¢\u0006\u0002\u0010\u000e¨\u0006\u0010"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/PatientDao;", "", "delete", "", "patientId", "", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getAllActivePatients", "Lkotlinx/coroutines/flow/Flow;", "", "Lcom/viernes/mobile/data/local/entity/PatientEntity;", "getPatientById", "insert", "patient", "(Lcom/viernes/mobile/data/local/entity/PatientEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "update", "app_debug"}
)
@Dao
public interface PatientDao {
   @Query("SELECT * FROM patients WHERE status = 'active' ORDER BY id ASC")
   @NotNull
   Flow<List<PatientEntity>> getAllActivePatients();

   @Query("SELECT * FROM patients WHERE id = :patientId")
   @Nullable
   Object getPatientById(long var1, @NotNull Continuation<? super PatientEntity> var3);

   @Insert(
      onConflict = 1
   )
   @Nullable
   Object insert(@NotNull PatientEntity var1, @NotNull Continuation<? super Long> var2);

   @Update
   @Nullable
   Object update(@NotNull PatientEntity var1, @NotNull Continuation<? super Unit> var2);

   @Query("DELETE FROM patients WHERE id = :patientId")
   @Nullable
   Object delete(long var1, @NotNull Continuation<? super Unit> var3);
}
