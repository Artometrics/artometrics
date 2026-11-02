import { useEffect, useState } from "react";
import { Platform, Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { trackPageView } from "@/lib/analytics/ga";

const KEY = "artometrics-cookie-pref";

const overlayPosition = (
  Platform.OS === "web" ? { position: "fixed" } : { position: "absolute" }
) as { position: "absolute" };

export function CookieBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (Platform.OS !== "web" || typeof localStorage === "undefined") return;
    if (!localStorage.getItem(KEY)) setVisible(true);
  }, []);

  if (!visible) return null;

  function accept() {
    try {
      localStorage.setItem(KEY, "accepted");
    } catch {
      /* ignore */
    }
    setVisible(false);
    if (Platform.OS === "web" && typeof window !== "undefined") {
      window.dispatchEvent(new Event("artometrics-consent"));
      trackPageView(window.location.pathname, document.title);
    }
  }

  return (
    <View
      className="left-3 right-3 bottom-3 z-[1500] self-center max-w-[480px] gap-3 border border-border bg-bg-elevated p-3.5"
      style={overlayPosition as object}
    >
      <Text className="text-[13px] leading-5 font-serif text-fg">
        We use essential cookies for membership and optional analytics when configured.{" "}
        <Link href="/legal/cookies">
          <Text className="underline text-accent">Cookie policy</Text>
        </Link>
      </Text>
      <Pressable onPress={accept} className="self-start bg-fg px-4 py-2">
        <Text className="text-xs font-bold tracking-wide text-inverse">OK</Text>
      </Pressable>
    </View>
  );
}
