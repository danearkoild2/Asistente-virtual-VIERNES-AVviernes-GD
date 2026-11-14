package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;
import com.viernes.mobile.data.local.entity.MedicationEntity;
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
   d1 = {"\u00004\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0007\n\u0002\u0010\u000e\n\u0002\b\u0004\bg\u0018\u00002\u00020\u0001J\u0016\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u001c\u0010\u0007\u001a\b\u0012\u0004\u0012\u00020\t0\b2\u0006\u0010\n\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u0018\u0010\u000b\u001a\u0004\u0018\u00010\t2\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u001c\u0010\f\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\t0\b0\r2\u0006\u0010\n\u001a\u00020\u0005H'J\u001c\u0010\u000e\u001a\b\u0012\u0004\u0012\u00020\t0\b2\u0006\u0010\n\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u0016\u0010\u000f\u001a\u00020\u00052\u0006\u0010\u0010\u001a\u00020\tH§@¢\u0006\u0002\u0010\u0011J\u0016\u0010\u0012\u001a\u00020\u00032\u0006\u0010\u0010\u001a\u00020\tH§@¢\u0006\u0002\u0010\u0011J.\u0010\u0013\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0014\u001a\u00020\u00152\u0006\u0010\u0016\u001a\u00020\u00152\u0006\u0010\u0017\u001a\u00020\u0015H§@¢\u0006\u0002\u0010\u0018¨\u0006\u0019"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/MedicationDao;", "", "delete", "", "medicationId", "", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getActiveVerifiedMedications", "", "Lcom/viernes/mobile/data/local/entity/MedicationEntity;", "patientId", "getMedicationById", "getMedicationsForPatient", "Lkotlinx/coroutines/flow/Flow;", "getMedicationsListSync", "insert", "medication", "(Lcom/viernes/mobile/data/local/entity/MedicationEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "update", "updateVerificationStatus", "status", "", "treatmentStatus", "confirmedBy", "(JLjava/lang/String;Ljava/lang/String;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_debug"}
)
@Dao
public interface MedicationDao {
   @Query("SELECT * FROM medications WHERE patientId = :patientId ORDER BY id ASC")
   @NotNull
   Flow<List<MedicationEntity>> getMedicationsForPatient(long var1);

   @Query("SELECT * FROM medications WHERE patientId = :patientId")
   @Nullable
   Object getMedicationsListSync(long var1, @NotNull Continuation<? super List<MedicationEntity>> var3);

   @Query("SELECT * FROM medications WHERE id = :medicationId")
   @Nullable
   Object getMedicationById(long var1, @NotNull Continuation<? super MedicationEntity> var3);

   @Query("SELECT * FROM medications WHERE patientId = :patientId AND verificationStatus IN ('ACTIVE', 'VERIFIED_PENDING_ACTIVATION') AND treatmentStatus = 'active'")
   @Nullable
   Object getActiveVerifiedMedications(long var1, @NotNull Continuation<? super List<MedicationEntity>> var3);

   @Insert(
      onConflict = 1
   )
   @Nullable
   Object insert(@NotNull MedicationEntity var1, @NotNull Continuation<? super Long> var2);

   @Update
   @Nullable
   Object update(@NotNull MedicationEntity var1, @NotNull Continuation<? super Unit> var2);

   @Query("UPDATE medications SET verificationStatus = :status, treatmentStatus = :treatmentStatus, confirmedBy = :confirmedBy, lastReviewDate = datetime('now', 'localtime') WHERE id = :medicationId")
   @Nullable
   Object updateVerificationStatus(long var1, @NotNull String var3, @NotNull String var4, @NotNull String var5, @NotNull Continuation<? super Unit> var6);

   @Query("DELETE FROM medications WHERE id = :medicationId")
   @Nullable
   Object delete(long var1, @NotNull Continuation<? super Unit> var3);
}
