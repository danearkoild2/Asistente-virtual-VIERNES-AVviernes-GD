package com.viernes.mobile.avatar;

import android.content.Context;
import androidx.compose.runtime.internal.StabilityInferred;
import java.util.List;
import kotlin.Metadata;
import kotlin.collections.CollectionsKt;
import kotlin.jvm.internal.Intrinsics;
import kotlin.ranges.RangesKt;
import kotlinx.coroutines.flow.MutableStateFlow;
import kotlinx.coroutines.flow.StateFlow;
import kotlinx.coroutines.flow.StateFlowKt;
import org.jetbrains.annotations.NotNull;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000B\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0010\u000e\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0007\n\u0000\n\u0002\u0010 \n\u0002\b\u0005\n\u0002\u0018\u0002\n\u0002\b\t\n\u0002\u0010\u0002\n\u0002\b\t\b\u0007\u0018\u00002\u00020\u0001B\r\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004J\u0006\u0010\u001d\u001a\u00020\u001eJ\u000e\u0010\u001f\u001a\u00020\u001e2\u0006\u0010 \u001a\u00020\fJ\u000e\u0010!\u001a\u00020\u001e2\u0006\u0010\"\u001a\u00020\nJ\u000e\u0010#\u001a\u00020\u001e2\u0006\u0010$\u001a\u00020\u0007J\u000e\u0010%\u001a\u00020\u001e2\u0006\u0010&\u001a\u00020\u0007R\u0014\u0010\u0005\u001a\b\u0012\u0004\u0012\u00020\u00070\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u0014\u0010\b\u001a\b\u0012\u0004\u0012\u00020\u00070\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u0014\u0010\t\u001a\b\u0012\u0004\u0012\u00020\n0\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u0014\u0010\u000b\u001a\b\u0012\u0004\u0012\u00020\f0\u0006X\u0082\u0004¢\u0006\u0002\n\u0000R\u0017\u0010\r\u001a\b\u0012\u0004\u0012\u00020\u00070\u000e¢\u0006\b\n\u0000\u001a\u0004\b\u000f\u0010\u0010R\u0017\u0010\u0011\u001a\b\u0012\u0004\u0012\u00020\u00070\u000e¢\u0006\b\n\u0000\u001a\u0004\b\u0012\u0010\u0010R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u0017\u0010\u0013\u001a\b\u0012\u0004\u0012\u00020\u00070\u0014¢\u0006\b\n\u0000\u001a\u0004\b\u0015\u0010\u0016R\u0017\u0010\u0017\u001a\b\u0012\u0004\u0012\u00020\u00070\u0014¢\u0006\b\n\u0000\u001a\u0004\b\u0018\u0010\u0016R\u0017\u0010\u0019\u001a\b\u0012\u0004\u0012\u00020\n0\u0014¢\u0006\b\n\u0000\u001a\u0004\b\u001a\u0010\u0016R\u0017\u0010\u001b\u001a\b\u0012\u0004\u0012\u00020\f0\u0014¢\u0006\b\n\u0000\u001a\u0004\b\u001c\u0010\u0016¨\u0006'"},
   d2 = {"Lcom/viernes/mobile/avatar/HuoAvatarController;", "", "context", "Landroid/content/Context;", "(Landroid/content/Context;)V", "_currentExpression", "Lkotlinx/coroutines/flow/MutableStateFlow;", "", "_currentMotion", "_currentState", "Lcom/viernes/mobile/avatar/HuoState;", "_mouthOpen", "", "availableExpressions", "", "getAvailableExpressions", "()Ljava/util/List;", "availableMotions", "getAvailableMotions", "currentExpression", "Lkotlinx/coroutines/flow/StateFlow;", "getCurrentExpression", "()Lkotlinx/coroutines/flow/StateFlow;", "currentMotion", "getCurrentMotion", "currentState", "getCurrentState", "mouthOpen", "getMouthOpen", "release", "", "setSpeechAmplitude", "amplitude", "setState", "state", "triggerExpression", "expressionName", "triggerMotion", "motionName", "app_debug"}
)
@StabilityInferred(
   parameters = 0
)
public final class HuoAvatarController {
   @NotNull
   private final Context context;
   @NotNull
   private final MutableStateFlow<HuoState> _currentState;
   @NotNull
   private final StateFlow<HuoState> currentState;
   @NotNull
   private final MutableStateFlow<String> _currentExpression;
   @NotNull
   private final StateFlow<String> currentExpression;
   @NotNull
   private final MutableStateFlow<String> _currentMotion;
   @NotNull
   private final StateFlow<String> currentMotion;
   @NotNull
   private final MutableStateFlow<Float> _mouthOpen;
   @NotNull
   private final StateFlow<Float> mouthOpen;
   @NotNull
   private final List<String> availableExpressions;
   @NotNull
   private final List<String> availableMotions;
   public static final int $stable = 8;

   public HuoAvatarController(@NotNull Context context) {
      Intrinsics.checkNotNullParameter(context, "context");
      super();
      this.context = context;
      this._currentState = StateFlowKt.MutableStateFlow(HuoState.IDLE);
      this.currentState = (StateFlow)this._currentState;
      this._currentExpression = StateFlowKt.MutableStateFlow("default");
      this.currentExpression = (StateFlow)this._currentExpression;
      this._currentMotion = StateFlowKt.MutableStateFlow("Scene1");
      this.currentMotion = (StateFlow)this._currentMotion;
      this._mouthOpen = StateFlowKt.MutableStateFlow(0.0F);
      this.mouthOpen = (StateFlow)this._mouthOpen;
      String[] var2 = new String[]{"angry", "baozhen", "cry", "qizi1", "qizi2", "white eyes"};
      this.availableExpressions = CollectionsKt.listOf(var2);
      var2 = new String[]{"Scene1", "haoqi", "keshui", "linghun", "qizi", "yaotou", "zhentou"};
      this.availableMotions = CollectionsKt.listOf(var2);
   }

   @NotNull
   public final StateFlow<HuoState> getCurrentState() {
      return this.currentState;
   }

   @NotNull
   public final StateFlow<String> getCurrentExpression() {
      return this.currentExpression;
   }

   @NotNull
   public final StateFlow<String> getCurrentMotion() {
      return this.currentMotion;
   }

   @NotNull
   public final StateFlow<Float> getMouthOpen() {
      return this.mouthOpen;
   }

   @NotNull
   public final List<String> getAvailableExpressions() {
      return this.availableExpressions;
   }

   @NotNull
   public final List<String> getAvailableMotions() {
      return this.availableMotions;
   }

   public final void setState(@NotNull HuoState state) {
      Intrinsics.checkNotNullParameter(state, "state");
      this._currentState.setValue(state);
      switch (HuoAvatarController.WhenMappings.$EnumSwitchMapping$0[state.ordinal()]) {
         case 1:
            this._currentMotion.setValue("Scene1");
            this._currentExpression.setValue("default");
            this._mouthOpen.setValue(0.0F);
            break;
         case 2:
            this._currentMotion.setValue("haoqi");
            this._currentExpression.setValue("default");
            break;
         case 3:
            this._currentMotion.setValue("keshui");
            this._currentExpression.setValue("default");
            break;
         case 4:
            this._currentMotion.setValue("yaotou");
            break;
         case 5:
            this._currentMotion.setValue("zhentou");
            this._currentExpression.setValue("qizi1");
      }

   }

   public final void setSpeechAmplitude(float amplitude) {
      if (this._currentState.getValue() == HuoState.SPEAKING) {
         this._mouthOpen.setValue(RangesKt.coerceIn(amplitude, 0.0F, 1.0F));
      } else {
         this._mouthOpen.setValue(0.0F);
      }

   }

   public final void triggerMotion(@NotNull String motionName) {
      Intrinsics.checkNotNullParameter(motionName, "motionName");
      if (this.availableMotions.contains(motionName)) {
         this._currentMotion.setValue(motionName);
      }

   }

   public final void triggerExpression(@NotNull String expressionName) {
      Intrinsics.checkNotNullParameter(expressionName, "expressionName");
      if (this.availableExpressions.contains(expressionName) || Intrinsics.areEqual(expressionName, "default")) {
         this._currentExpression.setValue(expressionName);
      }

   }

   public final void release() {
      this.setState(HuoState.IDLE);
   }

   // $FF: synthetic class
   @Metadata(
      mv = {1, 9, 0},
      k = 3,
      xi = 48
   )
   public class WhenMappings {
      // $FF: synthetic field
      public static final int[] $EnumSwitchMapping$0;

      static {
         int[] var0 = new int[HuoState.values().length];

         try {
            var0[HuoState.IDLE.ordinal()] = 1;
         } catch (NoSuchFieldError var6) {
         }

         try {
            var0[HuoState.LISTENING.ordinal()] = 2;
         } catch (NoSuchFieldError var5) {
         }

         try {
            var0[HuoState.THINKING.ordinal()] = 3;
         } catch (NoSuchFieldError var4) {
         }

         try {
            var0[HuoState.SPEAKING.ordinal()] = 4;
         } catch (NoSuchFieldError var3) {
         }

         try {
            var0[HuoState.ALERT.ordinal()] = 5;
         } catch (NoSuchFieldError var2) {
         }

         $EnumSwitchMapping$0 = var0;
      }
   }
}
