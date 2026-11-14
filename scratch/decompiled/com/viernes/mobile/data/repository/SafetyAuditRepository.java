package com.viernes.mobile.data.repository;

import androidx.compose.runtime.internal.StabilityInferred;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.domain.model.AuditRecord;
import com.viernes.mobile.domain.model.ClinicalWarning;
import java.util.List;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlinx.coroutines.flow.Flow;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u00006\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010 \n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004J\u0016\u0010\u0005\u001a\u00020\u00062\u0006\u0010\u0007\u001a\u00020\bH\u0086@¢\u0006\u0002\u0010\tJ\u001a\u0010\n\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\r0\f0\u000b2\u0006\u0010\u000e\u001a\u00020\bJ\u001a\u0010\u000f\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u00100\f0\u000b2\u0006\u0010\u000e\u001a\u00020\bR\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\u0011"},
   d2 = {"Lcom/viernes/mobile/data/repository/SafetyAuditRepository;", "", "db", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "(Lcom/viernes/mobile/data/local/ViernesDatabase;)V", "acknowledgeWarning", "", "warningId", "", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getActiveWarnings", "Lkotlinx/coroutines/flow/Flow;", "", "Lcom/viernes/mobile/domain/model/ClinicalWarning;", "patientId", "getAuditLogs", "Lcom/viernes/mobile/domain/model/AuditRecord;", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
@SourceDebugExtension({"SMAP\nAdditionalRepositories.kt\nKotlin\n*S Kotlin\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/SafetyAuditRepository\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt\n+ 4 SafeCollector.common.kt\nkotlinx/coroutines/flow/internal/SafeCollector_commonKt\n*L\n1#1,402:1\n49#2:403\n51#2:407\n49#2:408\n51#2:412\n46#3:404\n51#3:406\n46#3:409\n51#3:411\n105#4:405\n105#4:410\n*S KotlinDebug\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/SafetyAuditRepository\n*L\n340#1:403\n340#1:407\n363#1:408\n363#1:412\n340#1:404\n340#1:406\n363#1:409\n363#1:411\n340#1:405\n363#1:410\n*E\n"})
public final class SafetyAuditRepository {
   @NotNull
   private final ViernesDatabase db;
   public static final int $stable;

   public SafetyAuditRepository(@NotNull ViernesDatabase db) {
      Intrinsics.checkNotNullParameter(db, "db");
      super();
      this.db = db;
   }

   @NotNull
   public final Flow<List<ClinicalWarning>> getActiveWarnings(long patientId) {
      Flow $this$map$iv = this.db.clinicalWarningDao().getActiveWarningsForPatient(patientId);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new SafetyAuditRepository$getActiveWarnings$$inlined$map$1($this$map$iv);
   }

   @NotNull
   public final Flow<List<AuditRecord>> getAuditLogs(long patientId) {
      Flow $this$map$iv = this.db.auditDao().getAuditLogsForPatient(patientId);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new SafetyAuditRepository$getAuditLogs$$inlined$map$1($this$map$iv);
   }

   @Nullable
   public final Object acknowledgeWarning(long warningId, @NotNull Continuation<? super Unit> $completion) {
      Object var10000 = this.db.clinicalWarningDao().acknowledgeWarning(warningId, $completion);
      return var10000 == IntrinsicsKt.getCOROUTINE_SUSPENDED() ? var10000 : Unit.INSTANCE;
   }
}
