import { useEffect, useRef } from "react";
import { Slot, usePathname } from "expo-router";
import { StatusBar } from "expo-status-bar";
import {
  NativeScrollEvent,
  NativeSyntheticEvent,
  Platform,
  ScrollView,
  View,
} from "react-native";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";
import { SiteHeader } from "@/components/SiteHeader";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteNavOverlay } from "@/components/SiteNavOverlay";
import { Analytics } from "@/components/Analytics";
import { ShoegazeBackground } from "@/components/ShoegazeBackground";
import { ChromeProvider, useChrome } from "@/lib/chrome";
import { LocaleProvider } from "@/lib/locale";
import { ThemeProvider, useTheme } from "@/lib/theme";
import { trackPageView } from "@/lib/analytics/ga";
import { getBlogPost } from "@/lib/content";

function SiteChrome() {
  const pathname = usePathname();
  const { setScrollY, setIsArticle } = useChrome();
  const { mode } = useTheme();
  const scrollRef = useRef<ScrollView>(null);
  const bareChrome =
    pathname === "/welcome" || pathname === "/welcome/" || pathname.startsWith("/welcome?");

  useEffect(() => {
    const slug = pathname.replace(/^\//, "").replace(/\/$/, "");
    const onArticle = Boolean(slug && !slug.includes("/") && getBlogPost(slug));
    setIsArticle(onArticle);
    setScrollY(0);
    scrollRef.current?.scrollTo({ y: 0, animated: false });
    if (Platform.OS === "web" && typeof window !== "undefined") {
      window.scrollTo(0, 0);
      document.documentElement.scrollTop = 0;
      document.body.scrollTop = 0;
      trackPageView(pathname, typeof document !== "undefined" ? document.title : pathname);
    }
  }, [pathname, setIsArticle, setScrollY]);

  const onScroll = (e: NativeSyntheticEvent<NativeScrollEvent>) => {
    setScrollY(e.nativeEvent.contentOffset.y);
  };

  return (
    <SafeAreaView
      className={bareChrome ? "flex-1 bg-black" : "flex-1"}
      edges={["top"]}
      style={bareChrome ? { backgroundColor: "#000000" } : { backgroundColor: "transparent" }}
    >
      <ShoegazeBackground />
      <StatusBar style={bareChrome || mode === "dark" ? "light" : "dark"} />
      <View
        className={bareChrome ? "relative flex-1 bg-black" : "relative flex-1"}
        style={bareChrome ? undefined : { backgroundColor: "transparent" }}
      >
        {bareChrome ? null : <SiteHeader />}
        <ScrollView
          ref={scrollRef}
          className="flex-1"
          contentContainerClassName={bareChrome ? "grow" : "grow pb-6"}
          onScroll={onScroll}
          scrollEventThrottle={32}
          keyboardShouldPersistTaps="handled"
          keyboardDismissMode="on-drag"
        >
          <Slot />
          {bareChrome ? null : <SiteFooter />}
        </ScrollView>
        {bareChrome ? null : <SiteNavOverlay />}
        <Analytics />
      </View>
    </SafeAreaView>
  );
}

export default function SiteLayout() {
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <LocaleProvider>
          <ChromeProvider>
            <SiteChrome />
          </ChromeProvider>
        </LocaleProvider>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
