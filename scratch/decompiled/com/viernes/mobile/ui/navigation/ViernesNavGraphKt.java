package com.viernes.mobile.ui.navigation;

import android.os.Bundle;
import androidx.compose.animation.AnimatedContentScope;
import androidx.compose.runtime.Composable;
import androidx.compose.runtime.ComposableTarget;
import androidx.compose.runtime.Composer;
import androidx.compose.runtime.ComposerKt;
import androidx.compose.runtime.RecomposeScopeImplKt;
import androidx.compose.runtime.ScopeUpdateScope;
import androidx.compose.runtime.internal.ComposableLambdaKt;
import androidx.compose.ui.Alignment;
import androidx.compose.ui.Modifier;
import androidx.navigation.NamedNavArgumentKt;
import androidx.navigation.NavBackStackEntry;
import androidx.navigation.NavController;
import androidx.navigation.NavDeepLinkDslBuilderKt;
import androidx.navigation.NavGraphBuilder;
import androidx.navigation.NavHostController;
import androidx.navigation.NavOptions;
import androidx.navigation.Navigator;
import androidx.navigation.compose.NavGraphBuilderKt;
import androidx.navigation.compose.NavHostKt;
import com.viernes.mobile.assistant.ViernesAiAssistant;
import com.viernes.mobile.assistant.VoiceManager;
import com.viernes.mobile.avatar.HuoAvatarController;
import com.viernes.mobile.data.repository.AppointmentRepository;
import com.viernes.mobile.data.repository.IntakeRepository;
import com.viernes.mobile.data.repository.InventoryRepository;
import com.viernes.mobile.data.repository.MedicationRepository;
import com.viernes.mobile.data.repository.PatientRepository;
import com.viernes.mobile.data.repository.RefillRepository;
import com.viernes.mobile.ui.screens.ChatScreenKt;
import com.viernes.mobile.ui.screens.HomeScreenKt;
import com.viernes.mobile.ui.screens.HuoAvatarScreenKt;
import com.viernes.mobile.ui.screens.IntakeDetailConfirmScreenKt;
import com.viernes.mobile.ui.screens.InventoryScreensKt;
import com.viernes.mobile.ui.screens.MedicalCenterScreenKt;
import com.viernes.mobile.ui.screens.PatientScreensKt;
import com.viernes.mobile.ui.screens.SettingsScreenKt;
import com.viernes.mobile.ui.screens.TreatmentScreensKt;
import java.util.List;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.collections.CollectionsKt;
import kotlin.jvm.functions.Function0;
import kotlin.jvm.functions.Function1;
import kotlin.jvm.functions.Function2;
import kotlin.jvm.functions.Function4;
import kotlin.jvm.internal.Intrinsics;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 2,
   xi = 48,
   d1 = {"\u0000R\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0002\u001aq\u0010\u0000\u001a\u00020\u00012\u0006\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0006\u001a\u00020\u00072\u0006\u0010\b\u001a\u00020\t2\u0006\u0010\n\u001a\u00020\u000b2\u0006\u0010\f\u001a\u00020\r2\u0006\u0010\u000e\u001a\u00020\u000f2\u0006\u0010\u0010\u001a\u00020\u00112\u0006\u0010\u0012\u001a\u00020\u00132\u0006\u0010\u0014\u001a\u00020\u00152\b\b\u0002\u0010\u0016\u001a\u00020\u00172\b\b\u0002\u0010\u0018\u001a\u00020\u0019H\u0007¢\u0006\u0002\u0010\u001a¨\u0006\u001b"},
   d2 = {"ViernesNavGraph", "", "navController", "Landroidx/navigation/NavHostController;", "patientRepo", "Lcom/viernes/mobile/data/repository/PatientRepository;", "medRepo", "Lcom/viernes/mobile/data/repository/MedicationRepository;", "intakeRepo", "Lcom/viernes/mobile/data/repository/IntakeRepository;", "appointmentRepo", "Lcom/viernes/mobile/data/repository/AppointmentRepository;", "refillRepo", "Lcom/viernes/mobile/data/repository/RefillRepository;", "inventoryRepo", "Lcom/viernes/mobile/data/repository/InventoryRepository;", "voiceManager", "Lcom/viernes/mobile/assistant/VoiceManager;", "huoController", "Lcom/viernes/mobile/avatar/HuoAvatarController;", "assistant", "Lcom/viernes/mobile/assistant/ViernesAiAssistant;", "modifier", "Landroidx/compose/ui/Modifier;", "startDestination", "", "(Landroidx/navigation/NavHostController;Lcom/viernes/mobile/data/repository/PatientRepository;Lcom/viernes/mobile/data/repository/MedicationRepository;Lcom/viernes/mobile/data/repository/IntakeRepository;Lcom/viernes/mobile/data/repository/AppointmentRepository;Lcom/viernes/mobile/data/repository/RefillRepository;Lcom/viernes/mobile/data/repository/InventoryRepository;Lcom/viernes/mobile/assistant/VoiceManager;Lcom/viernes/mobile/avatar/HuoAvatarController;Lcom/viernes/mobile/assistant/ViernesAiAssistant;Landroidx/compose/ui/Modifier;Ljava/lang/String;Landroidx/compose/runtime/Composer;III)V", "app_debug"}
)
public final class ViernesNavGraphKt {
   @Composable
   @ComposableTarget(
      applier = "androidx.compose.ui.UiComposable"
   )
   public static final void ViernesNavGraph(@NotNull final NavHostController navController, @NotNull final PatientRepository patientRepo, @NotNull final MedicationRepository medRepo, @NotNull final IntakeRepository intakeRepo, @NotNull final AppointmentRepository appointmentRepo, @NotNull final RefillRepository refillRepo, @NotNull final InventoryRepository inventoryRepo, @NotNull final VoiceManager voiceManager, @NotNull final HuoAvatarController huoController, @NotNull final ViernesAiAssistant assistant, @Nullable final Modifier modifier, @Nullable final String startDestination, @Nullable Composer $composer, final int $changed, final int $changed1, final int var15) {
      Intrinsics.checkNotNullParameter(navController, "navController");
      Intrinsics.checkNotNullParameter(patientRepo, "patientRepo");
      Intrinsics.checkNotNullParameter(medRepo, "medRepo");
      Intrinsics.checkNotNullParameter(intakeRepo, "intakeRepo");
      Intrinsics.checkNotNullParameter(appointmentRepo, "appointmentRepo");
      Intrinsics.checkNotNullParameter(refillRepo, "refillRepo");
      Intrinsics.checkNotNullParameter(inventoryRepo, "inventoryRepo");
      Intrinsics.checkNotNullParameter(voiceManager, "voiceManager");
      Intrinsics.checkNotNullParameter(huoController, "huoController");
      Intrinsics.checkNotNullParameter(assistant, "assistant");
      $composer = $composer.startRestartGroup(-449161803);
      ComposerKt.sourceInformation($composer, "C(ViernesNavGraph)P(7,8,5,3!1,9,4,11,2)31@1102L4389:ViernesNavGraph.kt#y6y2ch");
      int $dirty1 = $changed1;
      if ((var15 & 1024) != 0) {
         modifier = (Modifier)Modifier.Companion;
      }

      if ((var15 & 2048) != 0) {
         startDestination = Screen.Home.INSTANCE.getRoute();
         $dirty1 = $changed1 & -113;
      }

      if (ComposerKt.isTraceInProgress()) {
         ComposerKt.traceEventStart(-449161803, $changed, $dirty1, "com.viernes.mobile.ui.navigation.ViernesNavGraph (ViernesNavGraph.kt:30)");
      }

      NavHostKt.NavHost(navController, startDestination, modifier, (Alignment)null, (String)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, new Function1<NavGraphBuilder, Unit>() {
         public final void invoke(@NotNull NavGraphBuilder $this$NavHost) {
            Intrinsics.checkNotNullParameter($this$NavHost, "$this$NavHost");
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.Home.INSTANCE.getRoute(), (List)null, (List)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(-502843497, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry it, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(it, "it");
                  ComposerKt.sourceInformation($composer, "C37@1283L228:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-502843497, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:37)");
                  }

                  HomeScreenKt.HomeScreen(patientRepo, intakeRepo, huoController, new Function1<String, Unit>() {
                     public final void invoke(@NotNull String route) {
                        Intrinsics.checkNotNullParameter(route, "route");
                        NavController.navigate$default((NavController)navController, route, (NavOptions)null, (Navigator.Extras)null, 6, (Object)null);
                     }
                  }, $composer, 512);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 126, (Object)null);
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.MedicalCenter.INSTANCE.getRoute(), (List)null, (List)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(-458282930, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry it, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(it, "it");
                  ComposerKt.sourceInformation($composer, "C46@1584L364:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-458282930, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:46)");
                  }

                  MedicalCenterScreenKt.MedicalCenterScreen(patientRepo, medRepo, intakeRepo, appointmentRepo, refillRepo, inventoryRepo, new Function1<String, Unit>() {
                     public final void invoke(@NotNull String route) {
                        Intrinsics.checkNotNullParameter(route, "route");
                        NavController.navigate$default((NavController)navController, route, (NavOptions)null, (Navigator.Extras)null, 6, (Object)null);
                     }
                  }, $composer, 0);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 126, (Object)null);
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.PatientDetail.INSTANCE.getRoute(), CollectionsKt.listOf(NamedNavArgumentKt.navArgument("patientId", null.INSTANCE)), (List)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(-1282093745, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry backStackEntry, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(backStackEntry, "backStackEntry");
                  ComposerKt.sourceInformation($composer, "C62@2236L297:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-1282093745, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:61)");
                  }

                  Bundle var10000 = backStackEntry.getArguments();
                  long patientId = var10000 != null ? var10000.getLong("patientId") : 1L;
                  PatientScreensKt.PatientDetailScreen(patientId, patientRepo, new Function1<Long, Unit>() {
                     public final void invoke(long pId) {
                        NavController.navigate$default((NavController)navController, Screen.TreatmentList.INSTANCE.createRoute(pId), (NavOptions)null, (Navigator.Extras)null, 6, (Object)null);
                     }
                  }, new Function0<Unit>() {
                     public final void invoke() {
                        navController.popBackStack();
                     }
                  }, $composer, 0);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 124, (Object)null);
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.TreatmentList.INSTANCE.getRoute(), CollectionsKt.listOf(NamedNavArgumentKt.navArgument("patientId", null.INSTANCE)), (List)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(-2105904560, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry backStackEntry, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(backStackEntry, "backStackEntry");
                  ComposerKt.sourceInformation($composer, "C75@2821L330:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-2105904560, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:74)");
                  }

                  Bundle var10000 = backStackEntry.getArguments();
                  long patientId = var10000 != null ? var10000.getLong("patientId") : 1L;
                  TreatmentScreensKt.TreatmentListScreen(patientId, patientRepo, medRepo, new Function1<Long, Unit>() {
                     public final void invoke(long mId) {
                        NavController.navigate$default((NavController)navController, Screen.TreatmentDetail.INSTANCE.createRoute(mId), (NavOptions)null, (Navigator.Extras)null, 6, (Object)null);
                     }
                  }, new Function0<Unit>() {
                     public final void invoke() {
                        navController.popBackStack();
                     }
                  }, $composer, 0);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 124, (Object)null);
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.TreatmentDetail.INSTANCE.getRoute(), CollectionsKt.listOf(NamedNavArgumentKt.navArgument("medicationId", null.INSTANCE)), (List)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(1365251921, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry backStackEntry, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(backStackEntry, "backStackEntry");
                  ComposerKt.sourceInformation($composer, "C89@3450L223:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(1365251921, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:88)");
                  }

                  Bundle var10000 = backStackEntry.getArguments();
                  long medicationId = var10000 != null ? var10000.getLong("medicationId") : 1L;
                  TreatmentScreensKt.TreatmentDetailScreen(medicationId, medRepo, intakeRepo, new Function0<Unit>() {
                     public final void invoke() {
                        navController.popBackStack();
                     }
                  }, $composer, 0);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 124, (Object)null);
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.IntakeDetailConfirm.INSTANCE.getRoute(), CollectionsKt.listOf(NamedNavArgumentKt.navArgument("intakeId", null.INSTANCE)), CollectionsKt.listOf(NavDeepLinkDslBuilderKt.navDeepLink(null.INSTANCE)), (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(541441106, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry backStackEntry, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(backStackEntry, "backStackEntry");
                  ComposerKt.sourceInformation($composer, "C105@4086L219:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(541441106, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:104)");
                  }

                  Bundle var10000 = backStackEntry.getArguments();
                  long intakeId = var10000 != null ? var10000.getLong("intakeId") : 1L;
                  IntakeDetailConfirmScreenKt.IntakeDetailConfirmScreen(intakeId, intakeRepo, medRepo, new Function0<Unit>() {
                     public final void invoke() {
                        navController.popBackStack();
                     }
                  }, $composer, 0);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 120, (Object)null);
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.Inventory.INSTANCE.getRoute(), CollectionsKt.listOf(NamedNavArgumentKt.navArgument("patientId", null.INSTANCE)), (List)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(-282369709, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry backStackEntry, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(backStackEntry, "backStackEntry");
                  ComposerKt.sourceInformation($composer, "C118@4589L225:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-282369709, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:117)");
                  }

                  Bundle var10000 = backStackEntry.getArguments();
                  long patientId = var10000 != null ? var10000.getLong("patientId") : 1L;
                  InventoryScreensKt.InventoryScreen(patientId, inventoryRepo, patientRepo, new Function0<Unit>() {
                     public final void invoke() {
                        navController.popBackStack();
                     }
                  }, $composer, 0);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 124, (Object)null);
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.Chat.INSTANCE.getRoute(), (List)null, (List)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(-1106180524, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry it, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(it, "it");
                  ComposerKt.sourceInformation($composer, "C127@4878L222:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-1106180524, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:127)");
                  }

                  ChatScreenKt.ChatScreen(assistant, voiceManager, huoController, new Function0<Unit>() {
                     public final void invoke() {
                        navController.popBackStack();
                     }
                  }, $composer, 584);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 126, (Object)null);
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.HuoAvatar.INSTANCE.getRoute(), (List)null, (List)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(-1929991339, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry it, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(it, "it");
                  ComposerKt.sourceInformation($composer, "C136@5169L143:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(-1929991339, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:136)");
                  }

                  HuoAvatarScreenKt.HuoAvatarScreen(huoController, new Function0<Unit>() {
                     public final void invoke() {
                        navController.popBackStack();
                     }
                  }, $composer, 8);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 126, (Object)null);
            NavGraphBuilderKt.composable$default($this$NavHost, Screen.Settings.INSTANCE.getRoute(), (List)null, (List)null, (Function1)null, (Function1)null, (Function1)null, (Function1)null, (Function4)ComposableLambdaKt.composableLambdaInstance(1541165142, true, new Function4<AnimatedContentScope, NavBackStackEntry, Composer, Integer, Unit>() {
               @Composable
               @ComposableTarget(
                  applier = "androidx.compose.ui.UiComposable"
               )
               public final void invoke(@NotNull AnimatedContentScope $this$composable, @NotNull NavBackStackEntry it, @Nullable Composer $composer, int $changed) {
                  Intrinsics.checkNotNullParameter($this$composable, "$this$composable");
                  Intrinsics.checkNotNullParameter(it, "it");
                  ComposerKt.sourceInformation($composer, "C143@5380L95:ViernesNavGraph.kt#y6y2ch");
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventStart(1541165142, $changed, -1, "com.viernes.mobile.ui.navigation.ViernesNavGraph.<anonymous>.<anonymous> (ViernesNavGraph.kt:143)");
                  }

                  SettingsScreenKt.SettingsScreen(new Function0<Unit>() {
                     public final void invoke() {
                        navController.popBackStack();
                     }
                  }, $composer, 0);
                  if (ComposerKt.isTraceInProgress()) {
                     ComposerKt.traceEventEnd();
                  }

               }
            }), 126, (Object)null);
         }
      }, $composer, 8 | 112 & $dirty1 | 896 & $dirty1 << 6, 504);
      if (ComposerKt.isTraceInProgress()) {
         ComposerKt.traceEventEnd();
      }

      ScopeUpdateScope var10000 = $composer.endRestartGroup();
      if (var10000 != null) {
         var10000.updateScope(new Function2<Composer, Integer, Unit>() {
            public final void invoke(@Nullable Composer $composer, int $force) {
               ViernesNavGraphKt.ViernesNavGraph(navController, patientRepo, medRepo, intakeRepo, appointmentRepo, refillRepo, inventoryRepo, voiceManager, huoController, assistant, modifier, startDestination, $composer, RecomposeScopeImplKt.updateChangedFlags($changed | 1), RecomposeScopeImplKt.updateChangedFlags($changed1), var15);
            }
         });
      }

   }
}
