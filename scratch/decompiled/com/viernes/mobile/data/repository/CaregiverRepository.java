package com.viernes.mobile.data.repository;

import androidx.compose.runtime.internal.StabilityInferred;
import com.google.gson.Gson;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.local.dao.AuditDao;
import com.viernes.mobile.data.local.dao.CaregiverDao;
import com.viernes.mobile.data.local.entity.AuditRecordEntity;
import com.viernes.mobile.data.local.entity.CaregiverEntity;
import com.viernes.mobile.domain.model.CaregiverAssignment;
import com.viernes.mobile.domain.model.CaregiverRole;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.collections.ArraysKt;
import kotlin.collections.CollectionsKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.Boxing;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlinx.coroutines.flow.Flow;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000R\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0010\t\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010 \n\u0002\b\u0003\n\u0002\u0010\u000b\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004JF\u0010\u0007\u001a\u00020\b2\u0006\u0010\t\u001a\u00020\n2\u0006\u0010\u000b\u001a\u00020\n2\u0006\u0010\f\u001a\u00020\r2\u0006\u0010\u000e\u001a\u00020\u000f2\f\u0010\u0010\u001a\b\u0012\u0004\u0012\u00020\n0\u00112\b\b\u0002\u0010\u0012\u001a\u00020\nH\u0086@¢\u0006\u0002\u0010\u0013J&\u0010\u0014\u001a\u00020\u00152\u0006\u0010\t\u001a\u00020\n2\u0006\u0010\f\u001a\u00020\r2\u0006\u0010\u0016\u001a\u00020\nH\u0086@¢\u0006\u0002\u0010\u0017J\u001a\u0010\u0018\u001a\u000e\u0012\n\u0012\b\u0012\u0004\u0012\u00020\u001a0\u00110\u00192\u0006\u0010\f\u001a\u00020\rJ\f\u0010\u001b\u001a\u00020\u001a*\u00020\u001cH\u0002R\u000e\u0010\u0005\u001a\u00020\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\u001d"},
   d2 = {"Lcom/viernes/mobile/data/repository/CaregiverRepository;", "", "db", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "(Lcom/viernes/mobile/data/local/ViernesDatabase;)V", "dao", "Lcom/viernes/mobile/data/local/dao/CaregiverDao;", "assignCaregiver", "", "userId", "", "name", "patientId", "", "role", "Lcom/viernes/mobile/domain/model/CaregiverRole;", "permissions", "", "assignedBy", "(Ljava/lang/String;Ljava/lang/String;JLcom/viernes/mobile/domain/model/CaregiverRole;Ljava/util/List;Ljava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "checkPermission", "", "permission", "(Ljava/lang/String;JLjava/lang/String;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "getCaregiversForPatient", "Lkotlinx/coroutines/flow/Flow;", "Lcom/viernes/mobile/domain/model/CaregiverAssignment;", "toDomain", "Lcom/viernes/mobile/data/local/entity/CaregiverEntity;", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
@SourceDebugExtension({"SMAP\nAdditionalRepositories.kt\nKotlin\n*S Kotlin\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/CaregiverRepository\n+ 2 Transform.kt\nkotlinx/coroutines/flow/FlowKt__TransformKt\n+ 3 Emitters.kt\nkotlinx/coroutines/flow/FlowKt__EmittersKt\n+ 4 SafeCollector.common.kt\nkotlinx/coroutines/flow/internal/SafeCollector_commonKt\n*L\n1#1,402:1\n49#2:403\n51#2:407\n46#3:404\n51#3:406\n105#4:405\n*S KotlinDebug\n*F\n+ 1 AdditionalRepositories.kt\ncom/viernes/mobile/data/repository/CaregiverRepository\n*L\n276#1:403\n276#1:407\n276#1:404\n276#1:406\n276#1:405\n*E\n"})
public final class CaregiverRepository {
   @NotNull
   private final ViernesDatabase db;
   @NotNull
   private final CaregiverDao dao;
   public static final int $stable = 8;

   public CaregiverRepository(@NotNull ViernesDatabase db) {
      Intrinsics.checkNotNullParameter(db, "db");
      super();
      this.db = db;
      this.dao = this.db.caregiverDao();
   }

   @NotNull
   public final Flow<List<CaregiverAssignment>> getCaregiversForPatient(long patientId) {
      Flow $this$map$iv = this.dao.getCaregiversForPatient(patientId);
      int $i$f$map = 0;
      int $i$f$unsafeTransform = 0;
      int $i$f$unsafeFlow = 0;
      return new CaregiverRepository$getCaregiversForPatient$$inlined$map$1($this$map$iv, this);
   }

   @Nullable
   public final Object assignCaregiver(@NotNull String userId, @NotNull String name, long patientId, @NotNull CaregiverRole role, @NotNull List<String> permissions, @NotNull String assignedBy, @NotNull Continuation<? super Unit> var8) {
      label27: {
         if (var8 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label27;
            }
         }

         $continuation = new ContinuationImpl(var8) {
            Object L$0;
            Object L$1;
            Object L$2;
            Object L$3;
            Object L$4;
            long J$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return CaregiverRepository.this.assignCaregiver((String)null, (String)null, 0L, (CaregiverRole)null, (List)null, (String)null, (Continuation)this);
            }
         };
      }

      Object $result = $continuation.result;
      Object var12 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            CaregiverDao var10000 = this.dao;
            String var10007 = role.getValue();
            String var9 = (new Gson()).toJson(permissions);
            Intrinsics.checkNotNullExpressionValue(var9, "toJson(...)");
            CaregiverEntity var10001 = new CaregiverEntity(0L, userId, name, patientId, var10007, var9, LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME), 1, (DefaultConstructorMarker)null);
            $continuation.L$0 = this;
            $continuation.L$1 = userId;
            $continuation.L$2 = name;
            $continuation.L$3 = role;
            $continuation.L$4 = assignedBy;
            $continuation.J$0 = patientId;
            $continuation.label = 1;
            if (var10000.insertOrUpdate(var10001, $continuation) == var12) {
               return var12;
            }
            break;
         case 1:
            patientId = $continuation.J$0;
            assignedBy = (String)$continuation.L$4;
            role = (CaregiverRole)$continuation.L$3;
            name = (String)$continuation.L$2;
            userId = (String)$continuation.L$1;
            this = (CaregiverRepository)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            break;
         case 2:
            ResultKt.throwOnFailure($result);
            return Unit.INSTANCE;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      AuditDao var13 = this.db.auditDao();
      AuditRecordEntity var14 = new AuditRecordEntity(0L, assignedBy, Boxing.boxLong(patientId), "CAREGIVER", (Long)null, "ASSIGN", "Cuidador " + name + " (" + userId + ") asignado con rol " + role.getValue(), (String)null, 129, (DefaultConstructorMarker)null);
      $continuation.L$0 = null;
      $continuation.L$1 = null;
      $continuation.L$2 = null;
      $continuation.L$3 = null;
      $continuation.L$4 = null;
      $continuation.label = 2;
      if (var13.insert(var14, $continuation) == var12) {
         return var12;
      } else {
         return Unit.INSTANCE;
      }
   }

   // $FF: synthetic method
   public static Object assignCaregiver$default(CaregiverRepository var0, String var1, String var2, long var3, CaregiverRole var5, List var6, String var7, Continuation var8, int var9, Object var10) {
      if ((var9 & 32) != 0) {
         var7 = "system";
      }

      return var0.assignCaregiver(var1, var2, var3, var5, var6, var7, var8);
   }

   @Nullable
   public final Object checkPermission(@NotNull String userId, long patientId, @NotNull String permission, @NotNull Continuation<? super Boolean> var5) {
      label39: {
         if (var5 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label39;
            }
         }

         $continuation = new ContinuationImpl(var5) {
            Object L$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return CaregiverRepository.this.checkPermission((String)null, 0L, (String)null, (Continuation)this);
            }
         };
      }

      Object $result = $continuation.result;
      Object var12 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      Object var10000;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            String[] var6 = new String[]{"system", "admin", "director"};
            if (CollectionsKt.listOf(var6).contains(userId)) {
               return Boxing.boxBoolean(true);
            }

            CaregiverDao var16 = this.dao;
            $continuation.L$0 = permission;
            $continuation.label = 1;
            var10000 = var16.getAssignment(userId, patientId, $continuation);
            if (var10000 == var12) {
               return var12;
            }
            break;
         case 1:
            permission = (String)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            var10000 = $result;
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      CaregiverEntity var17 = (CaregiverEntity)var10000;
      if (var17 == null) {
         return Boxing.boxBoolean(false);
      } else {
         CaregiverEntity assignment = var17;
         if (Intrinsics.areEqual(assignment.getRole(), "ADMIN")) {
            return Boxing.boxBoolean(true);
         } else {
            List perms;
            try {
               Object perms = (new Gson()).fromJson(assignment.getPermissionsJson(), String[].class);
               Intrinsics.checkNotNullExpressionValue(perms, "fromJson(...)");
               perms = ArraysKt.toList(perms);
            } catch (Exception var13) {
               perms = CollectionsKt.emptyList();
            }

            return Boxing.boxBoolean(perms.contains(permission));
         }
      }
   }

   private final CaregiverAssignment toDomain(CaregiverEntity $this$toDomain) {
      List perms;
      try {
         Object var10000 = (new Gson()).fromJson($this$toDomain.getPermissionsJson(), String[].class);
         Intrinsics.checkNotNullExpressionValue(var10000, "fromJson(...)");
         perms = ArraysKt.toList(var10000);
      } catch (Exception var5) {
         perms = CollectionsKt.emptyList();
      }

      return new CaregiverAssignment($this$toDomain.getId(), $this$toDomain.getUserId(), $this$toDomain.getCaregiverName(), $this$toDomain.getPatientId(), CaregiverRole.Companion.from($this$toDomain.getRole()), perms, $this$toDomain.getAssignedAt());
   }

   // $FF: synthetic method
   public static final CaregiverAssignment access$toDomain(CaregiverRepository $this, CaregiverEntity $receiver) {
      return $this.toDomain($receiver);
   }
}
