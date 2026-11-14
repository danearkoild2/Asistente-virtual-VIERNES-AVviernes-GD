package com.viernes.mobile.data.local.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;
import com.viernes.mobile.data.local.entity.AppointmentEntity;
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
   d1 = {"\u00006\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010 \n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\b\u0005\bg\u0018\u00002\u00020\u0001J\u0016\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J\u0018\u0010\u0007\u001a\u0004\u0018\u00010\b2\u0006\u0010\u0004\u001a\u00020\u0005H§@¢\u0006\u0002\u0010\u0006J$\u0010\t\u001a\b\u0012\u0004\u0012\u00020\b0\n2\u0006\u0010\u000b\u001a\u00020\u00052\u0006\u0010\f\u001a\u00020\rH§@¢\u0006\u0002\u0010\u000eJ\u001c\u0010\u000f\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\b0\n0\u00102\u0006\u0010\u000b\u001a\u00020\u0005H'J\u0016\u0010\u0011\u001a\u00020\u00052\u0006\u0010\u0012\u001a\u00020\bH§@¢\u0006\u0002\u0010\u0013J\u0016\u0010\u0014\u001a\u00020\u00032\u0006\u0010\u0012\u001a\u00020\bH§@¢\u0006\u0002\u0010\u0013¨\u0006\u0015"},
   d2 = {"Lcom/viernes/mobile/data/local/dao/AppointmentDao;", "", "delete", "", "id", "", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getAppointmentById", "Lcom/viernes/mobile/data/local/entity/AppointmentEntity;", "getAppointmentsForDateSync", "", "patientId", "date", "", "(JLjava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getAppointmentsForPatient", "Lkotlinx/coroutines/flow/Flow;", "insert", "appointment", "(Lcom/viernes/mobile/data/local/entity/AppointmentEntity;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "update", "app_debug"}
)
@Dao
public interface AppointmentDao {
   @Query("SELECT * FROM appointments WHERE patientId = :patientId ORDER BY appointmentDate ASC, appointmentTime ASC")
   @NotNull
   Flow<List<AppointmentEntity>> getAppointmentsForPatient(long var1);

   @Query("SELECT * FROM appointments WHERE patientId = :patientId AND appointmentDate = :date")
   @Nullable
   Object getAppointmentsForDateSync(long var1, @NotNull String var3, @NotNull Continuation<? super List<AppointmentEntity>> var4);

   @Query("SELECT * FROM appointments WHERE id = :id")
   @Nullable
   Object getAppointmentById(long var1, @NotNull Continuation<? super AppointmentEntity> var3);

   @Insert(
      onConflict = 1
   )
   @Nullable
   Object insert(@NotNull AppointmentEntity var1, @NotNull Continuation<? super Long> var2);

   @Update
   @Nullable
   Object update(@NotNull AppointmentEntity var1, @NotNull Continuation<? super Unit> var2);

   @Query("DELETE FROM appointments WHERE id = :id")
   @Nullable
   Object delete(long var1, @NotNull Continuation<? super Unit> var3);
}
