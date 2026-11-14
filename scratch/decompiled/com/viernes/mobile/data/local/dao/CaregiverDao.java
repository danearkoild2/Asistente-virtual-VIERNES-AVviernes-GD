package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import com.viernes.mobile.data.local.entity.CaregiverEntity;
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
   d1 = {"\u00000\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\b\u0004\n\u0002\u0010\u0002\n\u0000\bg\u0018\u00002\u00020\u0001J \u0010\u0002\u001a\u0004\u0018\u00010\u00032\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0006\u001a\u00020\u0007H§@¢\u0006\u0002\u0010\bJ\u001c\u0010\t\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00030\u000b0\n2\u0006\u0010\u0006\u001a\u00020\u0007H'J\u0016\u0010\f\u001a\u00020\u00072\u0006\u0010\r\u001a\u00020\u0003H§@¢\u0006\u0002\u0010\u000eJ\u001e\u0010\u000f\u001a\u00020\u00102\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0006\u001a\u00020\u0007H§@¢\u0006\u0002\u0010\b¨\u0006\u0011"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/CaregiverDao;", "", "getAssignment", "Lcom/viernes/mobile/data/local/entity/CaregiverEntity;", "userId", "", "patientId", "", "(Ljava/lang/String;JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getCaregiversForPatient", "Lkotlinx/coroutines/flow/Flow;", "", "insertOrUpdate", "caregiver", "(Lcom/viernes/mobile/data/local/entity/CaregiverEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "removeAssignment", "", "app_debug"}
)
@Dao
public interface CaregiverDao {
   @Query("SELECT * FROM caregiver_assignments WHERE patientId = :patientId")
   @NotNull
   Flow<List<CaregiverEntity>> getCaregiversForPatient(long var1);

   @Query("SELECT * FROM caregiver_assignments WHERE userId = :userId AND patientId = :patientId")
   @Nullable
   Object getAssignment(@NotNull String var1, long var2, @NotNull Continuation<? super CaregiverEntity> var4);

   @Insert(
      onConflict = 1
   )
   @Nullable
   Object insertOrUpdate(@NotNull CaregiverEntity var1, @NotNull Continuation<? super Long> var2);

   @Query("DELETE FROM caregiver_assignments WHERE userId = :userId AND patientId = :patientId")
   @Nullable
   Object removeAssignment(@NotNull String var1, long var2, @NotNull Continuation<? super Unit> var4);
}
