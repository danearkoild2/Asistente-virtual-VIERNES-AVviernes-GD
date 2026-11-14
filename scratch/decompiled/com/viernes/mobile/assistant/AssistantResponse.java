package com.viernes.mobile.assistant;

import androidx.compose.runtime.internal.StabilityInferred;
import kotlin.Metadata;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000\"\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u000e\n\u0002\b\t\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001B\u0019\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\n\b\u0002\u0010\u0004\u001a\u0004\u0018\u00010\u0003¢\u0006\u0002\u0010\u0005J\t\u0010\t\u001a\u00020\u0003HÆ\u0003J\u000b\u0010\n\u001a\u0004\u0018\u00010\u0003HÆ\u0003J\u001f\u0010\u000b\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\n\b\u0002\u0010\u0004\u001a\u0004\u0018\u00010\u0003HÆ\u0001J\u0013\u0010\f\u001a\u00020\r2\b\u0010\u000e\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010\u000f\u001a\u00020\u0010HÖ\u0001J\t\u0010\u0011\u001a\u00020\u0003HÖ\u0001R\u0013\u0010\u0004\u001a\u0004\u0018\u00010\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0006\u0010\u0007R\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\b\u0010\u0007¨\u0006\u0012"},
   d2 = {"Lcom/viernes/mobile/assistant/AssistantResponse;", "", "text", "", "actionExecuted", "(Ljava/lang/String;Ljava/lang/String;)V", "getActionExecuted", "()Ljava/lang/String;", "getText", "component1", "component2", "copy", "equals", "", "other", "hashCode", "", "toString", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class AssistantResponse {
   @NotNull
   private final String text;
   @Nullable
   private final String actionExecuted;
   public static final int $stable;

   public AssistantResponse(@NotNull String text, @Nullable String actionExecuted) {
      Intrinsics.checkNotNullParameter(text, "text");
      super();
      this.text = text;
      this.actionExecuted = actionExecuted;
   }

   // $FF: synthetic method
   public AssistantResponse(String var1, String var2, int var3, DefaultConstructorMarker var4) {
      if ((var3 & 2) != 0) {
         var2 = null;
      }

      this(var1, var2);
   }

   @NotNull
   public final String getText() {
      return this.text;
   }

   @Nullable
   public final String getActionExecuted() {
      return this.actionExecuted;
   }

   @NotNull
   public final String component1() {
      return this.text;
   }

   @Nullable
   public final String component2() {
      return this.actionExecuted;
   }

   @NotNull
   public final AssistantResponse copy(@NotNull String text, @Nullable String actionExecuted) {
      Intrinsics.checkNotNullParameter(text, "text");
      return new AssistantResponse(text, actionExecuted);
   }

   // $FF: synthetic method
   public static AssistantResponse copy$default(AssistantResponse var0, String var1, String var2, int var3, Object var4) {
      if ((var3 & 1) != 0) {
         var1 = var0.text;
      }

      if ((var3 & 2) != 0) {
         var2 = var0.actionExecuted;
      }

      return var0.copy(var1, var2);
   }

   @NotNull
   public String toString() {
      return "AssistantResponse(text=" + this.text + ", actionExecuted=" + this.actionExecuted + ")";
   }

   public int hashCode() {
      int result = this.text.hashCode();
      result = result * 31 + (this.actionExecuted == null ? 0 : this.actionExecuted.hashCode());
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof AssistantResponse)) {
         return false;
      } else {
         AssistantResponse var2 = (AssistantResponse)other;
         if (!Intrinsics.areEqual(this.text, var2.text)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.actionExecuted, var2.actionExecuted);
         }
      }
   }
}
