package com.viernes.mobile.assistant;

import androidx.compose.runtime.internal.StabilityInferred;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.viernes.mobile.data.local.ViernesDatabase;
import com.viernes.mobile.data.local.dao.AppointmentDao;
import com.viernes.mobile.data.local.dao.IntakeDao;
import com.viernes.mobile.data.local.dao.MedicationDao;
import com.viernes.mobile.data.local.dao.PatientDao;
import com.viernes.mobile.data.local.entity.IntakeEntity;
import com.viernes.mobile.data.local.entity.MedicationEntity;
import com.viernes.mobile.data.local.entity.PatientEntity;
import java.time.LocalDate;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.TimeUnit;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.Unit;
import kotlin.collections.CollectionsKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.text.StringsKt;
import kotlinx.coroutines.BuildersKt;
import kotlinx.coroutines.CoroutineScope;
import kotlinx.coroutines.Dispatchers;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okhttp3.ResponseBody;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u00002\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\t\n\u0002\b\n\b\u0007\u0018\u00002\u00020\u0001B%\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\n\b\u0002\u0010\u0004\u001a\u0004\u0018\u00010\u0005\u0012\n\b\u0002\u0010\u0006\u001a\u0004\u0018\u00010\u0005¢\u0006\u0002\u0010\u0007J\u0018\u0010\f\u001a\u00020\r2\b\u0010\u000e\u001a\u0004\u0018\u00010\u000fH\u0082@¢\u0006\u0002\u0010\u0010J \u0010\u0011\u001a\u00020\r2\u0006\u0010\u0012\u001a\u00020\u00052\b\u0010\u000e\u001a\u0004\u0018\u00010\u000fH\u0082@¢\u0006\u0002\u0010\u0013J\"\u0010\u0014\u001a\u00020\r2\u0006\u0010\u0015\u001a\u00020\u00052\n\b\u0002\u0010\u000e\u001a\u0004\u0018\u00010\u000fH\u0086@¢\u0006\u0002\u0010\u0013J \u0010\u0016\u001a\u00020\r2\u0006\u0010\u0017\u001a\u00020\u00052\b\u0010\u0018\u001a\u0004\u0018\u00010\u000fH\u0082@¢\u0006\u0002\u0010\u0013R\u0010\u0010\u0004\u001a\u0004\u0018\u00010\u0005X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\b\u001a\u00020\tX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\n\u001a\u00020\u000bX\u0082\u0004¢\u0006\u0002\n\u0000R\u0010\u0010\u0006\u001a\u0004\u0018\u00010\u0005X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\u0019"},
   d2 = {"Lcom/viernes/mobile/assistant/ViernesAiAssistant;", "", "db", "Lcom/viernes/mobile/data/local/ViernesDatabase;", "apiKey", "", "serverUrl", "(Lcom/viernes/mobile/data/local/ViernesDatabase;Ljava/lang/String;Ljava/lang/String;)V", "gson", "Lcom/google/gson/Gson;", "httpClient", "Lokhttp3/OkHttpClient;", "handleLocalAppointmentQuery", "Lcom/viernes/mobile/assistant/AssistantResponse;", "selectedPatientId", "", "(Ljava/lang/Long;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "handleLocalMedicalQuery", "message", "(Ljava/lang/String;Ljava/lang/Long;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "processUserMessage", "userMessage", "queryRemoteLlm", "prompt", "patientId", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
@SourceDebugExtension({"SMAP\nViernesAiAssistant.kt\nKotlin\n*S Kotlin\n*F\n+ 1 ViernesAiAssistant.kt\ncom/viernes/mobile/assistant/ViernesAiAssistant\n+ 2 fake.kt\nkotlin/jvm/internal/FakeKt\n*L\n1#1,181:1\n1#2:182\n*E\n"})
public final class ViernesAiAssistant {
   @NotNull
   private final ViernesDatabase db;
   @Nullable
   private final String apiKey;
   @Nullable
   private final String serverUrl;
   @NotNull
   private final OkHttpClient httpClient;
   @NotNull
   private final Gson gson;
   public static final int $stable = 8;

   public ViernesAiAssistant(@NotNull ViernesDatabase db, @Nullable String apiKey, @Nullable String serverUrl) {
      Intrinsics.checkNotNullParameter(db, "db");
      super();
      this.db = db;
      this.apiKey = apiKey;
      this.serverUrl = serverUrl;
      this.httpClient = (new OkHttpClient.Builder()).connectTimeout(15L, TimeUnit.SECONDS).readTimeout(30L, TimeUnit.SECONDS).build();
      this.gson = new Gson();
   }

   // $FF: synthetic method
   public ViernesAiAssistant(ViernesDatabase var1, String var2, String var3, int var4, DefaultConstructorMarker var5) {
      if ((var4 & 2) != 0) {
         var2 = null;
      }

      if ((var4 & 4) != 0) {
         var3 = null;
      }

      this(var1, var2, var3);
   }

   @Nullable
   public final Object processUserMessage(@NotNull final String userMessage, @Nullable final Long selectedPatientId, @NotNull Continuation<? super AssistantResponse> $completion) {
      return BuildersKt.withContext((CoroutineContext)Dispatchers.getIO(), new Function2<CoroutineScope, Continuation<? super AssistantResponse>, Object>((Continuation)null) {
         int label;

         @Nullable
         public final Object invokeSuspend(@NotNull Object $result) {
            Exception var10000;
            label101: {
               Object var4 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
               Object var10;
               switch (this.label) {
                  case 0:
                     ResultKt.throwOnFailure($result);
                     String var13 = StringsKt.trim((CharSequence)userMessage).toString().toLowerCase(Locale.ROOT);
                     Intrinsics.checkNotNullExpressionValue(var13, "toLowerCase(...)");
                     String query = var13;
                     if (StringsKt.contains$default((CharSequence)query, (CharSequence)"toma", false, 2, (Object)null) || StringsKt.contains$default((CharSequence)query, (CharSequence)"medicamento", false, 2, (Object)null) || StringsKt.contains$default((CharSequence)query, (CharSequence)"pastilla", false, 2, (Object)null) || StringsKt.contains$default((CharSequence)query, (CharSequence)"agenda", false, 2, (Object)null) || StringsKt.contains$default((CharSequence)query, (CharSequence)"papá", false, 2, (Object)null) || StringsKt.contains$default((CharSequence)query, (CharSequence)"mamá", false, 2, (Object)null)) {
                        ViernesAiAssistant var16 = ViernesAiAssistant.this;
                        String var21 = userMessage;
                        Long var23 = selectedPatientId;
                        Continuation var24 = (Continuation)this;
                        this.label = 1;
                        var10 = var16.handleLocalMedicalQuery(var21, var23, var24);
                        if (var10 == var4) {
                           return var4;
                        }

                        return var10;
                     }

                     if (StringsKt.contains$default((CharSequence)query, (CharSequence)"cita", false, 2, (Object)null) || StringsKt.contains$default((CharSequence)query, (CharSequence)"médico", false, 2, (Object)null) || StringsKt.contains$default((CharSequence)query, (CharSequence)"doctor", false, 2, (Object)null)) {
                        ViernesAiAssistant var15 = ViernesAiAssistant.this;
                        Long var20 = selectedPatientId;
                        Continuation var22 = (Continuation)this;
                        this.label = 2;
                        var10 = var15.handleLocalAppointmentQuery(var20, var22);
                        if (var10 == var4) {
                           return var4;
                        }

                        return var10;
                     }

                     CharSequence var3 = (CharSequence)ViernesAiAssistant.this.apiKey;
                     if (var3 == null || StringsKt.isBlank(var3)) {
                        var3 = (CharSequence)ViernesAiAssistant.this.serverUrl;
                        if (var3 == null || StringsKt.isBlank(var3)) {
                           return new AssistantResponse("Hola, soy VIERNES. Tu centro médico local está activo. Puedes preguntarme por las tomas de hoy, consultar el inventario, citas médicas o confirmar medicamentos programados.", (String)null);
                        }
                     }

                     try {
                        ViernesAiAssistant var14 = ViernesAiAssistant.this;
                        String var18 = userMessage;
                        Long var10002 = selectedPatientId;
                        Continuation var10003 = (Continuation)this;
                        this.label = 3;
                        var10 = var14.queryRemoteLlm(var18, var10002, var10003);
                     } catch (Exception var6) {
                        var10000 = var6;
                        boolean var17 = false;
                        break label101;
                     }

                     if (var10 == var4) {
                        return var4;
                     }
                     break;
                  case 1:
                     ResultKt.throwOnFailure($result);
                     var10 = $result;
                     return var10;
                  case 2:
                     ResultKt.throwOnFailure($result);
                     var10 = $result;
                     return var10;
                  case 3:
                     try {
                        ResultKt.throwOnFailure($result);
                        var10 = $result;
                        break;
                     } catch (Exception var7) {
                        var10000 = var7;
                        boolean var10001 = false;
                        break label101;
                     }
                  default:
                     throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
               }

               try {
                  return var10;
               } catch (Exception var5) {
                  var10000 = var5;
                  boolean var19 = false;
               }
            }

            Exception e = var10000;
            return new AssistantResponse("No fue posible conectar con el servicio de IA externo (" + e.getMessage() + "). El centro médico y recordatorios locales continúan operando con normalidad.", (String)null);
         }

         @NotNull
         public final Continuation<Unit> create(@Nullable Object value, @NotNull Continuation<?> $completion) {
            return (Continuation)(new <anonymous constructor>($completion));
         }

         @Nullable
         public final Object invoke(@NotNull CoroutineScope p1, @Nullable Continuation<? super AssistantResponse> p2) {
            return ((<undefinedtype>)this.create(p1, p2)).invokeSuspend(Unit.INSTANCE);
         }
      }, $completion);
   }

   // $FF: synthetic method
   public static Object processUserMessage$default(ViernesAiAssistant var0, String var1, Long var2, Continuation var3, int var4, Object var5) {
      if ((var4 & 2) != 0) {
         var2 = null;
      }

      return var0.processUserMessage(var1, var2, var3);
   }

   private final Object handleLocalMedicalQuery(String var1, Long selectedPatientId, Continuation<? super AssistantResponse> var3) {
      label313: {
         if (var3 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label313;
            }
         }

         $continuation = new ContinuationImpl(var3) {
            Object L$0;
            Object L$1;
            Object L$2;
            Object L$3;
            Object L$4;
            Object L$5;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return ViernesAiAssistant.this.handleLocalMedicalQuery((String)null, (Long)null, (Continuation)this);
            }
         };
      }

      String todayStr;
      StringBuilder responseBuilder;
      Iterator var7;
      PatientEntity patient;
      List intakes;
      Object var22;
      Object var10000;
      label316: {
         Object $result = $continuation.result;
         var22 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
         switch ($continuation.label) {
            case 0:
               ResultKt.throwOnFailure($result);
               String var69 = LocalDate.now().toString();
               Intrinsics.checkNotNullExpressionValue(var69, "toString(...)");
               todayStr = var69;
               PatientDao var70 = this.db.patientDao();
               long var98 = selectedPatientId != null ? selectedPatientId : 1L;
               $continuation.L$0 = this;
               $continuation.L$1 = todayStr;
               $continuation.label = 1;
               Object var71 = var70.getPatientById(var98, $continuation);
               if (var71 == var22) {
                  return var22;
               }

               PatientEntity var72 = (PatientEntity)var71;
               ViernesAiAssistant $this$handleLocalMedicalQuery_u24lambda_u241;
               Object var75;
               if (var72 != null) {
                  PatientEntity it = var72;
                  int meds = 0;
                  List var73 = CollectionsKt.listOf(it);
                  if (var73 != null) {
                     List var26 = var73;
                     responseBuilder = new StringBuilder();
                     var7 = var26.iterator();
                     break;
                  }

                  $this$handleLocalMedicalQuery_u24lambda_u241 = this;
                  meds = 0;
                  PatientDao var74 = $this$handleLocalMedicalQuery_u24lambda_u241.db.patientDao();
                  $continuation.L$0 = this;
                  $continuation.L$1 = todayStr;
                  $continuation.L$2 = $this$handleLocalMedicalQuery_u24lambda_u241;
                  $continuation.label = 2;
                  var75 = var74.getPatientById(1L, $continuation);
                  if (var75 == var22) {
                     return var22;
                  }
               } else {
                  $this$handleLocalMedicalQuery_u24lambda_u241 = this;
                  boolean var39 = false;
                  PatientDao var76 = $this$handleLocalMedicalQuery_u24lambda_u241.db.patientDao();
                  $continuation.L$0 = this;
                  $continuation.L$1 = todayStr;
                  $continuation.L$2 = $this$handleLocalMedicalQuery_u24lambda_u241;
                  $continuation.label = 2;
                  var75 = var76.getPatientById(1L, $continuation);
                  if (var75 == var22) {
                     return var22;
                  }
               }

               PatientEntity p1 = (PatientEntity)var75;
               PatientDao var77 = $this$handleLocalMedicalQuery_u24lambda_u241.db.patientDao();
               $continuation.L$0 = this;
               $continuation.L$1 = todayStr;
               $continuation.L$2 = p1;
               $continuation.label = 3;
               Object var78 = var77.getPatientById(2L, $continuation);
               if (var78 == var22) {
                  return var22;
               }

               PatientEntity p2 = (PatientEntity)var78;
               PatientEntity[] var51 = new PatientEntity[]{p1, p2};
               List patients = CollectionsKt.listOfNotNull(var51);
               responseBuilder = new StringBuilder();
               var7 = patients.iterator();
               break;
            case 1:
               todayStr = (String)$continuation.L$1;
               this = (ViernesAiAssistant)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               PatientEntity var62 = (PatientEntity)$result;
               ViernesAiAssistant var30;
               Object var65;
               if ((PatientEntity)$result != null) {
                  PatientEntity var29 = var62;
                  boolean var34 = false;
                  List var63 = CollectionsKt.listOf(var29);
                  if (var63 != null) {
                     List var24 = var63;
                     responseBuilder = new StringBuilder();
                     var7 = var24.iterator();
                     break;
                  }

                  var30 = this;
                  var34 = false;
                  PatientDao var64 = var30.db.patientDao();
                  $continuation.L$0 = this;
                  $continuation.L$1 = todayStr;
                  $continuation.L$2 = var30;
                  $continuation.label = 2;
                  var65 = var64.getPatientById(1L, $continuation);
                  if (var65 == var22) {
                     return var22;
                  }
               } else {
                  var30 = this;
                  boolean var36 = false;
                  PatientDao var66 = var30.db.patientDao();
                  $continuation.L$0 = this;
                  $continuation.L$1 = todayStr;
                  $continuation.L$2 = var30;
                  $continuation.label = 2;
                  var65 = var66.getPatientById(1L, $continuation);
                  if (var65 == var22) {
                     return var22;
                  }
               }

               PatientEntity var42 = (PatientEntity)var65;
               PatientDao var67 = var30.db.patientDao();
               $continuation.L$0 = this;
               $continuation.L$1 = todayStr;
               $continuation.L$2 = var42;
               $continuation.label = 3;
               Object var68 = var67.getPatientById(2L, $continuation);
               if (var68 == var22) {
                  return var22;
               }

               PatientEntity var46 = (PatientEntity)var68;
               PatientEntity[] var50 = new PatientEntity[]{var42, var46};
               List var25 = CollectionsKt.listOfNotNull(var50);
               responseBuilder = new StringBuilder();
               var7 = var25.iterator();
               break;
            case 2:
               int var33 = 0;
               ViernesAiAssistant $this$handleLocalMedicalQuery_u24lambda_u241 = (ViernesAiAssistant)$continuation.L$2;
               todayStr = (String)$continuation.L$1;
               this = (ViernesAiAssistant)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               PatientEntity var41 = (PatientEntity)$result;
               PatientDao var60 = $this$handleLocalMedicalQuery_u24lambda_u241.db.patientDao();
               $continuation.L$0 = this;
               $continuation.L$1 = todayStr;
               $continuation.L$2 = var41;
               $continuation.label = 3;
               Object var61 = var60.getPatientById(2L, $continuation);
               if (var61 == var22) {
                  return var22;
               }

               PatientEntity var45 = (PatientEntity)var61;
               PatientEntity[] var49 = new PatientEntity[]{var41, var45};
               List var23 = CollectionsKt.listOfNotNull(var49);
               responseBuilder = new StringBuilder();
               var7 = var23.iterator();
               break;
            case 3:
               int var10 = 0;
               PatientEntity p1 = (PatientEntity)$continuation.L$2;
               todayStr = (String)$continuation.L$1;
               this = (ViernesAiAssistant)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               PatientEntity var12 = (PatientEntity)$result;
               PatientEntity[] var13 = new PatientEntity[]{p1, var12};
               List var5 = CollectionsKt.listOfNotNull(var13);
               responseBuilder = new StringBuilder();
               var7 = var5.iterator();
               break;
            case 4:
               patient = (PatientEntity)$continuation.L$4;
               var7 = (Iterator)$continuation.L$3;
               responseBuilder = (StringBuilder)$continuation.L$2;
               todayStr = (String)$continuation.L$1;
               this = (ViernesAiAssistant)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               intakes = (List)$result;
               MedicationDao var59 = this.db.medicationDao();
               long var10001 = patient.getId();
               $continuation.L$0 = this;
               $continuation.L$1 = todayStr;
               $continuation.L$2 = responseBuilder;
               $continuation.L$3 = var7;
               $continuation.L$4 = patient;
               $continuation.L$5 = intakes;
               $continuation.label = 5;
               var10000 = var59.getMedicationsListSync(var10001, $continuation);
               if (var10000 == var22) {
                  return var22;
               }
               break label316;
            case 5:
               intakes = (List)$continuation.L$5;
               patient = (PatientEntity)$continuation.L$4;
               var7 = (Iterator)$continuation.L$3;
               responseBuilder = (StringBuilder)$continuation.L$2;
               todayStr = (String)$continuation.L$1;
               this = (ViernesAiAssistant)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               var10000 = $result;
               break label316;
            default:
               throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
         }

         if (!var7.hasNext()) {
            String var106 = responseBuilder.toString();
            Intrinsics.checkNotNullExpressionValue(var106, "toString(...)");
            return new AssistantResponse(StringsKt.trimEnd((CharSequence)var106).toString(), "QUERY_DAILY_INTAKES");
         }

         patient = (PatientEntity)var7.next();
         IntakeDao var79 = this.db.intakeDao();
         long var99 = patient.getId();
         $continuation.L$0 = this;
         $continuation.L$1 = todayStr;
         $continuation.L$2 = responseBuilder;
         $continuation.L$3 = var7;
         $continuation.L$4 = patient;
         $continuation.L$5 = null;
         $continuation.label = 4;
         Object var80 = var79.getIntakesForDateSync(var99, todayStr, $continuation);
         if (var80 == var22) {
            return var22;
         }

         intakes = (List)var80;
         MedicationDao var81 = this.db.medicationDao();
         var99 = patient.getId();
         $continuation.L$0 = this;
         $continuation.L$1 = todayStr;
         $continuation.L$2 = responseBuilder;
         $continuation.L$3 = var7;
         $continuation.L$4 = patient;
         $continuation.L$5 = intakes;
         $continuation.label = 5;
         var10000 = var81.getMedicationsListSync(var99, $continuation);
         if (var10000 == var22) {
            return var22;
         }
      }

      while(true) {
         List meds = (List)var10000;
         responseBuilder.append("\ud83d\udccb Paciente " + patient.getDisplayName() + ":\n");
         if (intakes.isEmpty()) {
            responseBuilder.append("  • No hay tomas registradas para hoy (" + todayStr + ").\n");
            responseBuilder.append("\n");
            if (!var7.hasNext()) {
               String var105 = responseBuilder.toString();
               Intrinsics.checkNotNullExpressionValue(var105, "toString(...)");
               return new AssistantResponse(StringsKt.trimEnd((CharSequence)var105).toString(), "QUERY_DAILY_INTAKES");
            }

            patient = (PatientEntity)var7.next();
            IntakeDao var95 = this.db.intakeDao();
            long var103 = patient.getId();
            $continuation.L$0 = this;
            $continuation.L$1 = todayStr;
            $continuation.L$2 = responseBuilder;
            $continuation.L$3 = var7;
            $continuation.L$4 = patient;
            $continuation.L$5 = null;
            $continuation.label = 4;
            Object var96 = var95.getIntakesForDateSync(var103, todayStr, $continuation);
            if (var96 == var22) {
               return var22;
            }

            intakes = (List)var96;
            MedicationDao var97 = this.db.medicationDao();
            var103 = patient.getId();
            $continuation.L$0 = this;
            $continuation.L$1 = todayStr;
            $continuation.L$2 = responseBuilder;
            $continuation.L$3 = var7;
            $continuation.L$4 = patient;
            $continuation.L$5 = intakes;
            $continuation.label = 5;
            var10000 = var97.getMedicationsListSync(var103, $continuation);
            if (var10000 == var22) {
               return var22;
            }
         } else {
            label298:
            for(IntakeEntity itk : intakes) {
               for(Object var17 : (Iterable)meds) {
                  MedicationEntity it = (MedicationEntity)var17;
                  int var19 = 0;
                  if (it.getId() == itk.getMedicationId()) {
                     MedicationEntity var52 = (MedicationEntity)var17;
                     String var82;
                     if (var52 != null) {
                        var82 = var52.getTranscribedName();
                        if (var82 == null) {
                           var82 = "Medicamento";
                        }
                     } else {
                        var82 = "Medicamento";
                     }

                     String var14 = var82;
                     String var57 = itk.getStatus();
                     switch (var57.hashCode()) {
                        case -1429540080:
                           var82 = !var57.equals("SKIPPED") ? itk.getStatus() : "⚠️ Omitida";
                           break;
                        case 35394935:
                           if (!var57.equals("PENDING")) {
                              var82 = itk.getStatus();
                           } else {
                              var82 = itk.getScheduledTime();
                              if (var82 == null) {
                                 var82 = "horario sin fijar";
                              }

                              var82 = "⏰ Pendiente a las " + var82;
                           }
                           break;
                        case 1982485311:
                           if (!var57.equals("CONFIRMED")) {
                              var82 = itk.getStatus();
                           } else {
                              var82 = itk.getConfirmedAt();
                              if (var82 != null) {
                                 var82 = StringsKt.takeLast(var82, 8);
                                 var82 = var82 == null ? "✅ Administrada (" + "" + ")" : "✅ Administrada (" + var82 + ")";
                              } else {
                                 var82 = "✅ Administrada (" + "" + ")";
                              }
                           }
                           break;
                        default:
                           var82 = itk.getStatus();
                     }

                     String var55 = var82;
                     responseBuilder.append("  • " + var14 + " (" + itk.getDoseText() + "): " + var55 + "\n");
                     continue label298;
                  }
               }

               MedicationEntity med = (MedicationEntity)null;
               String var87;
               if (med != null) {
                  var87 = med.getTranscribedName();
                  if (var87 == null) {
                     var87 = "Medicamento";
                  }
               } else {
                  var87 = "Medicamento";
               }

               String medName = var87;
               String var58 = itk.getStatus();
               switch (var58.hashCode()) {
                  case -1429540080:
                     var87 = !var58.equals("SKIPPED") ? itk.getStatus() : "⚠️ Omitida";
                     break;
                  case 35394935:
                     if (!var58.equals("PENDING")) {
                        var87 = itk.getStatus();
                     } else {
                        var87 = itk.getScheduledTime();
                        if (var87 == null) {
                           var87 = "horario sin fijar";
                        }

                        var87 = "⏰ Pendiente a las " + var87;
                     }
                     break;
                  case 1982485311:
                     if (!var58.equals("CONFIRMED")) {
                        var87 = itk.getStatus();
                     } else {
                        var87 = itk.getConfirmedAt();
                        if (var87 != null) {
                           var87 = StringsKt.takeLast(var87, 8);
                           var87 = var87 == null ? "✅ Administrada (" + "" + ")" : "✅ Administrada (" + var87 + ")";
                        } else {
                           var87 = "✅ Administrada (" + "" + ")";
                        }
                     }
                     break;
                  default:
                     var87 = itk.getStatus();
               }

               String statusText = var87;
               responseBuilder.append("  • " + medName + " (" + itk.getDoseText() + "): " + statusText + "\n");
            }

            responseBuilder.append("\n");
            if (!var7.hasNext()) {
               String var10002 = responseBuilder.toString();
               Intrinsics.checkNotNullExpressionValue(var10002, "toString(...)");
               return new AssistantResponse(StringsKt.trimEnd((CharSequence)var10002).toString(), "QUERY_DAILY_INTAKES");
            }

            patient = (PatientEntity)var7.next();
            IntakeDao var92 = this.db.intakeDao();
            long var101 = patient.getId();
            $continuation.L$0 = this;
            $continuation.L$1 = todayStr;
            $continuation.L$2 = responseBuilder;
            $continuation.L$3 = var7;
            $continuation.L$4 = patient;
            $continuation.L$5 = null;
            $continuation.label = 4;
            Object var93 = var92.getIntakesForDateSync(var101, todayStr, $continuation);
            if (var93 == var22) {
               return var22;
            }

            intakes = (List)var93;
            MedicationDao var94 = this.db.medicationDao();
            var101 = patient.getId();
            $continuation.L$0 = this;
            $continuation.L$1 = todayStr;
            $continuation.L$2 = responseBuilder;
            $continuation.L$3 = var7;
            $continuation.L$4 = patient;
            $continuation.L$5 = intakes;
            $continuation.label = 5;
            var10000 = var94.getMedicationsListSync(var101, $continuation);
            if (var10000 == var22) {
               return var22;
            }
         }
      }
   }

   private final Object handleLocalAppointmentQuery(Long selectedPatientId, Continuation<? super AssistantResponse> var2) {
      label54: {
         if (var2 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label54;
            }
         }

         $continuation = new ContinuationImpl(var2) {
            Object L$0;
            long J$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return ViernesAiAssistant.this.handleLocalAppointmentQuery((Long)null, (Continuation)this);
            }
         };
      }

      List appts;
      Object var10000;
      label48: {
         Object $result = $continuation.result;
         Object var11 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
         long pId;
         switch ($continuation.label) {
            case 0:
               ResultKt.throwOnFailure($result);
               String var13 = LocalDate.now().toString();
               Intrinsics.checkNotNullExpressionValue(var13, "toString(...)");
               String todayStr = var13;
               pId = selectedPatientId != null ? selectedPatientId : 1L;
               AppointmentDao var14 = this.db.appointmentDao();
               $continuation.L$0 = this;
               $continuation.J$0 = pId;
               $continuation.label = 1;
               var10000 = var14.getAppointmentsForDateSync(pId, todayStr, $continuation);
               if (var10000 == var11) {
                  return var11;
               }
               break;
            case 1:
               pId = $continuation.J$0;
               this = (ViernesAiAssistant)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               var10000 = $result;
               break;
            case 2:
               appts = (List)$continuation.L$0;
               ResultKt.throwOnFailure($result);
               var10000 = $result;
               break label48;
            default:
               throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
         }

         appts = (List)var10000;
         PatientDao var15 = this.db.patientDao();
         $continuation.L$0 = appts;
         $continuation.label = 2;
         var10000 = var15.getPatientById(pId, $continuation);
         if (var10000 == var11) {
            return var11;
         }
      }

      PatientEntity patient = (PatientEntity)var10000;
      AssistantResponse var16;
      if (appts.isEmpty()) {
         String var10002;
         label38: {
            var16 = new AssistantResponse;
            if (patient != null) {
               var10002 = patient.getDisplayName();
               if (var10002 != null) {
                  break label38;
               }
            }

            var10002 = "el paciente";
         }

         var16.<init>("No hay citas médicas programadas para " + var10002 + " en la fecha de hoy.", "QUERY_APPOINTMENTS");
      } else {
         String details = CollectionsKt.joinToString$default((Iterable)appts, (CharSequence)"\n", (CharSequence)null, (CharSequence)null, 0, (CharSequence)null, null.INSTANCE, 30, (Object)null);
         var16 = new AssistantResponse("Citas para hoy de " + (patient != null ? patient.getDisplayName() : null) + ":\n" + details, "QUERY_APPOINTMENTS");
      }

      return var16;
   }

   private final Object queryRemoteLlm(String prompt, Long patientId, Continuation<? super AssistantResponse> $completion) {
      String var10000 = this.serverUrl;
      if (var10000 == null) {
         var10000 = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + this.apiKey;
      }

      Response response;
      label44: {
         String url = var10000;
         String systemContext = "Eres VIERNES Mobile, el asistente médico y personal inteligente nativo. Prioriza la seguridad clínica, la precisión y la amabilidad. No inventes dosis médicas.";
         JsonObject $this$queryRemoteLlm_u24lambda_u247 = new JsonObject();
         int var9 = 0;
         JsonArray $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246 = new JsonArray();
         int var12 = 0;
         JsonObject $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245 = new JsonObject();
         int var15 = 0;
         $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245.addProperty("role", "user");
         JsonArray $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244 = new JsonArray();
         int var18 = 0;
         JsonObject $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244_u24lambda_u243 = new JsonObject();
         int var21 = 0;
         $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244_u24lambda_u243.addProperty("text", systemContext + "\nUsuario pregunta: " + prompt);
         $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244.add((JsonElement)$this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244_u24lambda_u243);
         $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245.add("parts", (JsonElement)$this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244);
         $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246.add((JsonElement)$this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245);
         $this$queryRemoteLlm_u24lambda_u247.add("contents", (JsonElement)$this$queryRemoteLlm_u24lambda_u247_u24lambda_u246);
         Request.Builder var35 = (new Request.Builder()).url(url);
         RequestBody.Companion var10001 = RequestBody.Companion;
         String var10002 = $this$queryRemoteLlm_u24lambda_u247.toString();
         Intrinsics.checkNotNullExpressionValue(var10002, "toString(...)");
         Request request = var35.post(var10001.create(var10002, MediaType.Companion.get("application/json"))).build();
         response = this.httpClient.newCall(request).execute();
         ResponseBody var36 = response.body();
         if (var36 != null) {
            var10000 = var36.string();
            if (var10000 != null) {
               break label44;
            }
         }

         var10000 = "";
      }

      String responseBody = var10000;
      if (!response.isSuccessful()) {
         return new AssistantResponse("El servicio de IA respondió con estado " + response.code() + ".", (String)null);
      } else {
         label38: {
            JsonObject json = (JsonObject)this.gson.fromJson(responseBody, JsonObject.class);
            JsonArray $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245 = json.getAsJsonArray("candidates");
            if ($this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245 != null) {
               JsonElement $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245 = $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245.get(0);
               if ($this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245 != null) {
                  JsonObject var31 = $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245.getAsJsonObject();
                  if (var31 != null) {
                     JsonObject $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244 = var31.getAsJsonObject("content");
                     if ($this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244 != null) {
                        JsonArray $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244 = $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244.getAsJsonArray("parts");
                        if ($this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244 != null) {
                           JsonElement var33 = $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244.get(0);
                           if (var33 != null) {
                              JsonObject $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244_u24lambda_u243 = var33.getAsJsonObject();
                              if ($this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244_u24lambda_u243 != null) {
                                 JsonElement $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244_u24lambda_u243 = $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244_u24lambda_u243.get("text");
                                 if ($this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244_u24lambda_u243 != null) {
                                    var10000 = $this$queryRemoteLlm_u24lambda_u247_u24lambda_u246_u24lambda_u245_u24lambda_u244_u24lambda_u243.getAsString();
                                    break label38;
                                 }
                              }
                           }
                        }
                     }
                  }
               }
            }

            var10000 = null;
         }

         String var29 = var10000;
         String candidateText = var29 == null ? "No se recibió respuesta de texto." : var29;
         return new AssistantResponse(candidateText, "REMOTE_LLM_CHAT");
      }
   }
}
