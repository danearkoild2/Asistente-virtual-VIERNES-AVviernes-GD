package com.viernes.mobile.domain.usecase;

import androidx.compose.runtime.internal.StabilityInferred;
import com.viernes.mobile.data.repository.InventoryRepository;
import com.viernes.mobile.data.repository.MedicationRepository;
import com.viernes.mobile.domain.model.Medication;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import kotlin.Metadata;
import kotlin.ResultKt;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.coroutines.jvm.internal.ContinuationImpl;
import kotlin.jvm.internal.Intrinsics;
import kotlin.text.StringsKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000*\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010 \n\u0002\u0010\u000e\n\u0000\n\u0002\u0010\t\n\u0002\b\u0002\b\u0007\u0018\u00002\u00020\u0001B\u0015\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005¢\u0006\u0002\u0010\u0006J\u001c\u0010\u0007\u001a\b\u0012\u0004\u0012\u00020\t0\b2\u0006\u0010\n\u001a\u00020\u000bH\u0086@¢\u0006\u0002\u0010\fR\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\r"},
   d2 = {"Lcom/viernes/mobile/domain/usecase/SafetyCheckUseCase;", "", "medicationRepo", "Lcom/viernes/mobile/data/repository/MedicationRepository;", "inventoryRepo", "Lcom/viernes/mobile/data/repository/InventoryRepository;", "(Lcom/viernes/mobile/data/repository/MedicationRepository;Lcom/viernes/mobile/data/repository/InventoryRepository;)V", "checkPatientTreatments", "", "", "patientId", "", "(JLkotlin/coroutines/Continuation;)Ljava/lang/Object;", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class SafetyCheckUseCase {
   @NotNull
   private final MedicationRepository medicationRepo;
   @NotNull
   private final InventoryRepository inventoryRepo;
   public static final int $stable;

   public SafetyCheckUseCase(@NotNull MedicationRepository medicationRepo, @NotNull InventoryRepository inventoryRepo) {
      Intrinsics.checkNotNullParameter(medicationRepo, "medicationRepo");
      Intrinsics.checkNotNullParameter(inventoryRepo, "inventoryRepo");
      super();
      this.medicationRepo = medicationRepo;
      this.inventoryRepo = inventoryRepo;
   }

   @Nullable
   public final Object checkPatientTreatments(long patientId, @NotNull Continuation<? super List<String>> var3) {
      label86: {
         if (var3 instanceof Continuation $continuation) {
            if (($continuation.label & Integer.MIN_VALUE) != 0) {
               $continuation.label -= Integer.MIN_VALUE;
               break label86;
            }
         }

         $continuation = new ContinuationImpl(var3) {
            Object L$0;
            // $FF: synthetic field
            Object result;
            int label;

            @Nullable
            public final Object invokeSuspend(@NotNull Object $result) {
               this.result = $result;
               this.label |= Integer.MIN_VALUE;
               return SafetyCheckUseCase.this.checkPatientTreatments(0L, (Continuation)this);
            }
         };
      }

      Object $result = $continuation.result;
      Object var13 = IntrinsicsKt.getCOROUTINE_SUSPENDED();
      List warnings;
      Object var10000;
      switch ($continuation.label) {
         case 0:
            ResultKt.throwOnFailure($result);
            warnings = (List)(new ArrayList());
            MedicationRepository var18 = this.medicationRepo;
            $continuation.L$0 = warnings;
            $continuation.label = 1;
            var10000 = var18.getActiveVerifiedMedications(patientId, $continuation);
            if (var10000 == var13) {
               return var13;
            }
            break;
         case 1:
            warnings = (List)$continuation.L$0;
            ResultKt.throwOnFailure($result);
            var10000 = $result;
            break;
         default:
            throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
      }

      List meds = (List)var10000;
      Map seenIngredients = (Map)(new LinkedHashMap());

      for(Medication med : meds) {
         label78: {
            String var19 = med.getActiveIngredient();
            if (var19 != null) {
               var19 = StringsKt.trim((CharSequence)var19).toString();
               if (var19 != null) {
                  var21 = var19.toLowerCase(Locale.ROOT);
                  Intrinsics.checkNotNullExpressionValue(var21, "toLowerCase(...)");
                  break label78;
               }
            }

            var21 = null;
         }

         String ingredient = var21;
         CharSequence var10 = (CharSequence)ingredient;
         if (var10 != null && !StringsKt.isBlank(var10) && !Intrinsics.areEqual(ingredient, "si") && !Intrinsics.areEqual(ingredient, "no")) {
            if (seenIngredients.containsKey(ingredient)) {
               warnings.add("Posible duplicación de principio activo: '" + ingredient + "' presente en '" + med.getTranscribedName() + "' y '" + seenIngredients.get(ingredient) + "'");
            } else {
               seenIngredients.put(ingredient, med.getTranscribedName());
            }
         }
      }

      for(Medication med : meds) {
         CharSequence ingredient = (CharSequence)med.getConcentration();
         if (ingredient == null || StringsKt.isBlank(ingredient)) {
            ingredient = (CharSequence)med.getPrescribedDose();
            if (ingredient == null || StringsKt.isBlank(ingredient)) {
               warnings.add("Dosis o concentración no especificada para '" + med.getTranscribedName() + "'. Requiere confirmación médica.");
            }
         }
      }

      return warnings;
   }
}
