package com.viernes.mobile.ui.screens;

import androidx.compose.runtime.internal.StabilityInferred;
import java.time.LocalTime;
import java.util.UUID;
import kotlin.Metadata;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.text.StringsKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000\"\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u000f\n\u0002\u0010\u000b\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\b\u0087\b\u0018\u00002\u00020\u0001B)\u0012\b\b\u0002\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0003\u0012\u0006\u0010\u0005\u001a\u00020\u0003\u0012\b\b\u0002\u0010\u0006\u001a\u00020\u0003¢\u0006\u0002\u0010\u0007J\t\u0010\r\u001a\u00020\u0003HÆ\u0003J\t\u0010\u000e\u001a\u00020\u0003HÆ\u0003J\t\u0010\u000f\u001a\u00020\u0003HÆ\u0003J\t\u0010\u0010\u001a\u00020\u0003HÆ\u0003J1\u0010\u0011\u001a\u00020\u00002\b\b\u0002\u0010\u0002\u001a\u00020\u00032\b\b\u0002\u0010\u0004\u001a\u00020\u00032\b\b\u0002\u0010\u0005\u001a\u00020\u00032\b\b\u0002\u0010\u0006\u001a\u00020\u0003HÆ\u0001J\u0013\u0010\u0012\u001a\u00020\u00132\b\u0010\u0014\u001a\u0004\u0018\u00010\u0001HÖ\u0003J\t\u0010\u0015\u001a\u00020\u0016HÖ\u0001J\t\u0010\u0017\u001a\u00020\u0003HÖ\u0001R\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\b\u0010\tR\u0011\u0010\u0004\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\n\u0010\tR\u0011\u0010\u0005\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u000b\u0010\tR\u0011\u0010\u0006\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\f\u0010\t¨\u0006\u0018"},
   d2 = {"Lcom/viernes/mobile/ui/screens/ChatMessage;", "", "id", "", "sender", "text", "timestamp", "(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V", "getId", "()Ljava/lang/String;", "getSender", "getText", "getTimestamp", "component1", "component2", "component3", "component4", "copy", "equals", "", "other", "hashCode", "", "toString", "app_debug"}
)
@StabilityInferred(
   parameters = 1
)
public final class ChatMessage {
   @NotNull
   private final String id;
   @NotNull
   private final String sender;
   @NotNull
   private final String text;
   @NotNull
   private final String timestamp;
   public static final int $stable;

   public ChatMessage(@NotNull String id, @NotNull String sender, @NotNull String text, @NotNull String timestamp) {
      Intrinsics.checkNotNullParameter(id, "id");
      Intrinsics.checkNotNullParameter(sender, "sender");
      Intrinsics.checkNotNullParameter(text, "text");
      Intrinsics.checkNotNullParameter(timestamp, "timestamp");
      super();
      this.id = id;
      this.sender = sender;
      this.text = text;
      this.timestamp = timestamp;
   }

   // $FF: synthetic method
   public ChatMessage(String var1, String var2, String var3, String var4, int var5, DefaultConstructorMarker var6) {
      if ((var5 & 1) != 0) {
         String var10000 = UUID.randomUUID().toString();
         Intrinsics.checkNotNullExpressionValue(var10000, "toString(...)");
         var1 = var10000;
      }

      if ((var5 & 8) != 0) {
         String var7 = LocalTime.now().toString();
         Intrinsics.checkNotNullExpressionValue(var7, "toString(...)");
         var4 = StringsKt.take(var7, 5);
      }

      this(var1, var2, var3, var4);
   }

   @NotNull
   public final String getId() {
      return this.id;
   }

   @NotNull
   public final String getSender() {
      return this.sender;
   }

   @NotNull
   public final String getText() {
      return this.text;
   }

   @NotNull
   public final String getTimestamp() {
      return this.timestamp;
   }

   @NotNull
   public final String component1() {
      return this.id;
   }

   @NotNull
   public final String component2() {
      return this.sender;
   }

   @NotNull
   public final String component3() {
      return this.text;
   }

   @NotNull
   public final String component4() {
      return this.timestamp;
   }

   @NotNull
   public final ChatMessage copy(@NotNull String id, @NotNull String sender, @NotNull String text, @NotNull String timestamp) {
      Intrinsics.checkNotNullParameter(id, "id");
      Intrinsics.checkNotNullParameter(sender, "sender");
      Intrinsics.checkNotNullParameter(text, "text");
      Intrinsics.checkNotNullParameter(timestamp, "timestamp");
      return new ChatMessage(id, sender, text, timestamp);
   }

   // $FF: synthetic method
   public static ChatMessage copy$default(ChatMessage var0, String var1, String var2, String var3, String var4, int var5, Object var6) {
      if ((var5 & 1) != 0) {
         var1 = var0.id;
      }

      if ((var5 & 2) != 0) {
         var2 = var0.sender;
      }

      if ((var5 & 4) != 0) {
         var3 = var0.text;
      }

      if ((var5 & 8) != 0) {
         var4 = var0.timestamp;
      }

      return var0.copy(var1, var2, var3, var4);
   }

   @NotNull
   public String toString() {
      return "ChatMessage(id=" + this.id + ", sender=" + this.sender + ", text=" + this.text + ", timestamp=" + this.timestamp + ")";
   }

   public int hashCode() {
      int result = this.id.hashCode();
      result = result * 31 + this.sender.hashCode();
      result = result * 31 + this.text.hashCode();
      result = result * 31 + this.timestamp.hashCode();
      return result;
   }

   public boolean equals(@Nullable Object other) {
      if (this == other) {
         return true;
      } else if (!(other instanceof ChatMessage)) {
         return false;
      } else {
         ChatMessage var2 = (ChatMessage)other;
         if (!Intrinsics.areEqual(this.id, var2.id)) {
            return false;
         } else if (!Intrinsics.areEqual(this.sender, var2.sender)) {
            return false;
         } else if (!Intrinsics.areEqual(this.text, var2.text)) {
            return false;
         } else {
            return Intrinsics.areEqual(this.timestamp, var2.timestamp);
         }
      }
   }
}
