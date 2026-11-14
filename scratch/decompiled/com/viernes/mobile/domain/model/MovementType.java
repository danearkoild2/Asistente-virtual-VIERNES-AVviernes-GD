package com.viernes.mobile.domain.model;

import java.util.Iterator;
import kotlin.Metadata;
import kotlin.enums.EnumEntries;
import kotlin.enums.EnumEntriesKt;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import kotlin.text.StringsKt;
import org.jetbrains.annotations.NotNull;

@Metadata(
   mv = {1, 9, 0},
   k = 1,
   xi = 48,
   d1 = {"\u0000\u0012\n\u0002\u0018\u0002\n\u0002\u0010\u0010\n\u0000\n\u0002\u0010\u000e\n\u0002\b\n\b\u0086\u0081\u0002\u0018\u0000 \f2\b\u0012\u0004\u0012\u00020\u00000\u0001:\u0001\fB\u000f\b\u0002\u0012\u0006\u0010\u0002\u001a\u00020\u0003¢\u0006\u0002\u0010\u0004R\u0011\u0010\u0002\u001a\u00020\u0003¢\u0006\b\n\u0000\u001a\u0004\b\u0005\u0010\u0006j\u0002\b\u0007j\u0002\b\bj\u0002\b\tj\u0002\b\nj\u0002\b\u000b¨\u0006\r"},
   d2 = {"Lcom/viernes/mobile/domain/model/MovementType;", "", "value", "", "(Ljava/lang/String;ILjava/lang/String;)V", "getValue", "()Ljava/lang/String;", "INITIAL", "REFILL_ENTRY", "INTAKE_EXIT", "MANUAL_ADJUSTMENT", "DISCARD", "Companion", "app_debug"}
)
public enum MovementType {
   @NotNull
   public static final Companion Companion = new Companion((DefaultConstructorMarker)null);
   @NotNull
   private final String value;
   INITIAL("INITIAL"),
   REFILL_ENTRY("REFILL_ENTRY"),
   INTAKE_EXIT("INTAKE_EXIT"),
   MANUAL_ADJUSTMENT("MANUAL_ADJUSTMENT"),
   DISCARD("DISCARD");

   // $FF: synthetic field
   private static final EnumEntries $ENTRIES = EnumEntriesKt.enumEntries($VALUES);

   private MovementType(String value) {
      this.value = value;
   }

   @NotNull
   public final String getValue() {
      return this.value;
   }

   @NotNull
   public static EnumEntries<MovementType> getEntries() {
      return $ENTRIES;
   }

   // $FF: synthetic method
   private static final MovementType[] $values() {
      MovementType[] var0 = new MovementType[]{INITIAL, REFILL_ENTRY, INTAKE_EXIT, MANUAL_ADJUSTMENT, DISCARD};
      return var0;
   }

   @Metadata(
      mv = {1, 9, 0},
      k = 1,
      xi = 48,
      d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\b\u0086\u0003\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002J\u000e\u0010\u0003\u001a\u00020\u00042\u0006\u0010\u0005\u001a\u00020\u0006¨\u0006\u0007"},
      d2 = {"Lcom/viernes/mobile/domain/model/MovementType$Companion;", "", "()V", "from", "Lcom/viernes/mobile/domain/model/MovementType;", "value", "", "app_debug"}
   )
   @SourceDebugExtension({"SMAP\nEnums.kt\nKotlin\n*S Kotlin\n*F\n+ 1 Enums.kt\ncom/viernes/mobile/domain/model/MovementType$Companion\n+ 2 fake.kt\nkotlin/jvm/internal/FakeKt\n*L\n1#1,84:1\n1#2:85\n*E\n"})
   public static final class Companion {
      private Companion() {
      }

      @NotNull
      public final MovementType from(@NotNull String value) {
         Intrinsics.checkNotNullParameter(value, "value");
         Iterable var2 = (Iterable)MovementType.getEntries();
         Iterator var3 = var2.iterator();

         Object var10000;
         while(true) {
            if (var3.hasNext()) {
               Object var4 = var3.next();
               MovementType it = (MovementType)var4;
               int var6 = 0;
               if (!StringsKt.equals(it.getValue(), value, true)) {
                  continue;
               }

               var10000 = var4;
               break;
            }

            var10000 = null;
            break;
         }

         MovementType var7 = (MovementType)var10000;
         if (var7 == null) {
            var7 = MovementType.MANUAL_ADJUSTMENT;
         }

         return var7;
      }

      // $FF: synthetic method
      public Companion(DefaultConstructorMarker $constructor_marker) {
         this();
      }
   }
}
