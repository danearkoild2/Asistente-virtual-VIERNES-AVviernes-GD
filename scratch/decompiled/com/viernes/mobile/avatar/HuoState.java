package com.viernes.mobile.avatar;

import kotlin.Metadata;
import kotlin.enums.EnumEntries;
import kotlin.enums.EnumEntriesKt;
import org.jetbrains.annotations.NotNull;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000\f\n\u0002\u0018\u0002\n\u0002\u0010\u0010\n\u0002\b\u0007\b\u0086\u0081\u0002\u0018\u00002\b\u0012\u0004\u0012\u00020\u00000\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002j\u0002\b\u0003j\u0002\b\u0004j\u0002\b\u0005j\u0002\b\u0006j\u0002\b\u0007¨\u0006\b"},
   d2 = {"Lcom/viernes/mobile/avatar/HuoState;", "", "(Ljava/lang/String;I)V", "IDLE", "LISTENING", "THINKING", "SPEAKING", "ALERT", "app_debug"}
)
public enum HuoState {
   IDLE,
   LISTENING,
   THINKING,
   SPEAKING,
   ALERT;

   // $FF: synthetic field
   private static final EnumEntries $ENTRIES = EnumEntriesKt.enumEntries($VALUES);

   private HuoState() {
   }

   @NotNull
   public static EnumEntries<HuoState> getEntries() {
      return $ENTRIES;
   }

   // $FF: synthetic method
   private static final HuoState[] $values() {
      HuoState[] var0 = new HuoState[]{IDLE, LISTENING, THINKING, SPEAKING, ALERT};
      return var0;
   }
}
