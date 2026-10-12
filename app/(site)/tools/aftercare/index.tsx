import { useCallback, useState } from "react";
import {
  ActivityIndicator,
  Platform,
  Pressable,
  Text,
  View,
  useWindowDimensions,
} from "react-native";
import { Image } from "expo-image";
import { router, useFocusEffect } from "expo-router";
import { ArrowRight, X } from "@/components/icons";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { StoryProgress } from "@/components/aftercare/StoryProgress";
import { StrategyMap } from "@/components/aftercare/StrategyMap";
import { PlanetPoster } from "@/components/aftercare/PlanetPoster";
import { CosmicChartCard } from "@/components/aftercare/CosmicChartCard";
import { useTheme } from "@/lib/theme";
import { useAuth } from "@/lib/auth";
import { apiFetch } from "@/lib/supabase/client";
import { assetUrl } from "@/lib/assets";
import { celestialForSign } from "@/lib/aftercare/planets";
import { sunSignFromDate } from "@/lib/aftercare/calculators";

/** Auth without forcing redirect — Stories home is browsable as a guest preview. */
function useAuthGate() {
  return useAuth();
}

const NAV = [
  { href: "/tools/aftercare", label: "Home" },
  { href: "/tools/aftercare/journal", label: "Journal" },
  { href: "/tools/aftercare/tarot", label: "Tarot" },
  { href: "/tools/aftercare/track", label: "Track" },
  { href: "/tools/aftercare/tools", label: "Birth tools" },
];

type SkyPayload = {
  skyNote?: string;
  moon?: { name?: string; illumination?: number };
  sunSign?: string | null;
  error?: string;
};

type ProfilePayload = {
  profile?: { display_name?: string | null; email?: string | null };
  email?: string | null;
  error?: string;
};

type SlideId = "open" | "poster" | "chart" | "strategies" | "checkin";

const SLIDES: SlideId[] = ["open", "poster", "chart", "strategies", "checkin"];

export default function AftercareHomeScreen() {
  const { colors } = useTheme();
  const { width } = useWindowDimensions();
  const { user, loading: authLoading } = useAuthGate();
  const [skyNote, setSkyNote] = useState<string | null>(null);
  const [moonLabel, setMoonLabel] = useState<string | null>(null);
  const [displayName, setDisplayName] = useState<string | null>(null);
  const [sunSign, setSunSign] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [index, setIndex] = useState(0);

  const greetingName =
    displayName || user?.email?.split("@")[0] || user?.email || "friend";
  const storyW = Math.min(420, width - 32);
  const storyH = Math.min(740, Math.max(580, width * 1.6));
  const guest = !authLoading && !user;
  const celestial = celestialForSign(sunSign);

  const load = useCallback(async () => {
    if (!user) {
      setSkyNote(
        "A soft check-in day. Notice what wants tending — then pick one small ritual.",
      );
      setMoonLabel("Waxing Crescent");
      setSunSign("Sagittarius");
      setLoading(false);
      return;
    }
    setError(null);
    try {
      const [profileRes, skyRes] = await Promise.all([
        apiFetch("aftercare-profile"),
        apiFetch("aftercare-sky"),
      ]);

      if (profileRes.ok) {
        const data = (await profileRes.json()) as ProfilePayload & {
          profile?: { birth_date?: string | null };
        };
        setDisplayName(
          data.profile?.display_name?.trim() ||
            data.email?.split("@")[0] ||
            data.profile?.email?.split("@")[0] ||
            null,
        );
        if (data.profile?.birth_date) {
          setSunSign(sunSignFromDate(data.profile.birth_date));
        }
      } else {
        const data = (await profileRes.json().catch(() => ({}))) as ProfilePayload;
        setError(data.error || "Could not load profile.");
      }

      if (skyRes.ok) {
        const data = (await skyRes.json()) as SkyPayload;
        setSkyNote(data.skyNote ?? null);
        if (data.sunSign) setSunSign(data.sunSign);
        if (data.moon?.name) {
          const illum =
            typeof data.moon.illumination === "number"
              ? ` · ~${data.moon.illumination}% lit`
              : "";
          setMoonLabel(`${data.moon.name}${illum}`);
        }
      } else {
        const data = (await skyRes.json().catch(() => ({}))) as SkyPayload;
        setError((prev) => prev || data.error || "Could not load sky note.");
      }
    } catch {
      setError("Could not reach Aftercare. Try again shortly.");
    }
  }, [user]);

  useFocusEffect(
    useCallback(() => {
      if (authLoading) return;
      let active = true;
      (async () => {
        try {
          setLoading(true);
          await load();
        } finally {
          if (active) setLoading(false);
        }
      })();
      return () => {
        active = false;
      };
    }, [load, authLoading]),
  );

  function go(delta: number) {
    setIndex((i) => Math.max(0, Math.min(SLIDES.length - 1, i + delta)));
  }

  function goTool(href: string) {
    if (guest) {
      router.push(`/login?next=${encodeURIComponent(href)}`);
      return;
    }
    router.push(href as `/`);
  }

  if (authLoading) {
    return (
      <Wrapper className="gap-2.5 py-8 flex-1">
        <Text className="text-muted">Loading…</Text>
      </Wrapper>
    );
  }

  const slide = SLIDES[index];
  const heroBg =
    assetUrl("/images/brand/chomsky-a-white.png") ||
    assetUrl("/images/brand/chomsky-a-black.png");

  return (
    <Wrapper className="gap-2.5 py-8 flex-1">
      <PageSeo
        title="Aftercare"
        description="Journal, tarot, mood tracking, and birth tools on Artometrics."
        path="/tools/aftercare"
      />
      <ToolsSubnav links={NAV} />

      {loading ? (
        <ActivityIndicator className="mt-10" color={colors.accent} />
      ) : (
        <View className="rounded-[28px] overflow-hidden bg-[#0C0C0E] border border-white/10 relative self-center" style={{ width: storyW, height: storyH }}>
          {/* Atmospheric background */}
          <View className="absolute inset-0">
            <View
              className="absolute w-[280px] h-[280px] rounded-full opacity-55"
              style={{ top: "8%", left: "-10%", backgroundColor: "#6B4F3A" }}
            />
            <View
              className="absolute w-[280px] h-[280px] rounded-full opacity-55"
              style={{ top: "35%", right: "-16%", backgroundColor: "#3D5A6C", width: 220, height: 220 }}
            />
            <View
              className="absolute w-[280px] h-[280px] rounded-full opacity-55"
              style={{ bottom: "5%", left: "10%", backgroundColor: "#2A2A2E", width: 260, height: 260 }}
            />
            {heroBg ? (
              <Image
                source={{ uri: heroBg }}
                className="absolute w-[70%] h-[70%] top-[18%] left-[15%] opacity-[0.06]"
                contentFit="contain"
              />
            ) : null}
            <View className="absolute inset-0 bg-black/35" />
          </View>

          {/* Story chrome */}
          <View className="absolute top-0 left-0 right-0 z-[5] pt-3.5 px-3 gap-2.5">
            <StoryProgress count={SLIDES.length} index={index} />
            <View className="flex-row items-center justify-between">
              <View className="flex-row items-center gap-2">
                <View className="w-7 h-7 rounded-full border-[1.5px] border-white/85 items-center justify-center">
                  <View className="w-3 h-3 rounded-sm bg-white" />
                </View>
                <View>
                  <Text className="text-white text-[13px] font-bold">aftercare</Text>
                  <Text className="text-white/65 text-[11px]">{moonLabel || "Today"}</Text>
                </View>
              </View>
              <Pressable
                onPress={() => router.push("/studio")}
                hitSlop={10}
                accessibilityLabel="Close story"
              >
                <X size={22} color="#FFFFFF" />
              </Pressable>
            </View>
          </View>

          {/* Tap zones */}
          <View className="absolute inset-0 flex-row z-[2]" pointerEvents="box-none">
            <Pressable className="flex-1" onPress={() => go(-1)} />
            <Pressable className="flex-1" onPress={() => go(1)} />
          </View>

          {/* Slide content */}
          <View className="absolute left-5 right-5 top-[88px] bottom-12 z-[3] justify-between" pointerEvents="box-none">
            {error ? <Text className="font-sans text-[15px] text-accent">{error}</Text> : null}

            {slide === "open" ? (
              <>
                <Text className="text-white/88 font-sans text-sm leading-5 max-w-[220px]">
                  Soft rituals for the creative life — {greetingName}.
                </Text>
                <Text className="font-wordmark text-white text-[56px] leading-[58px] text-center self-center my-auto">CHECK{"\n"}IN</Text>
                <View className="gap-1.5 flex-row flex-wrap justify-between items-end">
                  <Text className="text-white text-[15px] font-extrabold tracking-wide flex-[0.4]">{"Today's sky"}</Text>
                  <Text className="text-white/72 text-xs leading-[17px] flex-[0.52] text-right" numberOfLines={4}>
                    {skyNote ||
                      "Add a birth date in Birth tools for a more personal note."}
                  </Text>
                </View>
              </>
            ) : null}

            {slide === "poster" ? (
              <View className="flex-1 justify-center" pointerEvents="none">
                <PlanetPoster
                  seasonTitle={celestial.seasonTitle}
                  seasonLine={celestial.seasonLine}
                  planet={celestial.planet}
                  dateLabel={moonLabel || "Tonight"}
                  compact
                />
              </View>
            ) : null}

            {slide === "chart" ? (
              <View className="flex-1 justify-center" pointerEvents="box-none">
                <CosmicChartCard
                  eyebrow={
                    skyNote ||
                    `${celestial.planet.id} frames this check-in — reflective, not predictive.`
                  }
                  planet={celestial.planet}
                  profileLabel={greetingName}
                  onContinue={() => go(1)}
                />
              </View>
            ) : null}

            {slide === "strategies" ? (
              <View
                className="mt-6 rounded-[22px] p-4 bg-white/14 border border-white/22 gap-2" style={Platform.OS === "web" ? ({ backdropFilter: "blur(18px)" } as object) : undefined}
                pointerEvents="auto"
              >
                <View className="flex-row items-center gap-2.5">
                  <View className="flex-row flex-wrap w-[22px] gap-0.5">
                    <View className="w-[7px] h-[7px] rounded bg-white" />
                    <View className="w-[7px] h-[7px] rounded bg-white" />
                    <View className="w-[7px] h-[7px] rounded bg-white opacity-50" />
                    <View className="w-[7px] h-[7px] rounded bg-white opacity-35" />
                  </View>
                  <Text className="text-white font-wordmark text-[28px]">Strategies.</Text>
                </View>
                <StrategyMap />
                <Text className="text-white/75 text-xs leading-[17px] text-center mt-1">
                  Combine strategies to create a comfortable plan.
                </Text>
              </View>
            ) : null}

            {slide === "checkin" ? (
              <>
                <Text className="text-white/88 font-sans text-sm leading-5 max-w-[220px]">
                  {guest
                    ? "Sign in to save rituals. Preview the doors below."
                    : "Pick a door. Stay as long as you need."}
                </Text>
                <Text className="font-wordmark text-white text-[56px] leading-[58px] text-center self-center my-auto">BEGIN</Text>
                <View className="gap-2.5 mt-3" pointerEvents="auto">
                  {[
                    ["/tools/aftercare/journal", "Open journal"],
                    ["/tools/aftercare/tarot", "Pull cards"],
                    ["/tools/aftercare/tools", "Birth tools"],
                  ].map(([href, label]) => (
                    <Pressable
                      key={href}
                      onPress={() => goTool(href)}
                      className="flex-row items-center justify-between bg-white px-4 py-3.5 rounded-full"
                    >
                      <Text className="text-[#0A0A0A] text-sm font-bold">{label}</Text>
                      <ArrowRight size={16} color="#0A0A0A" />
                    </Pressable>
                  ))}
                </View>
              </>
            ) : null}
          </View>

          <View className="absolute bottom-3.5 left-0 right-0 items-center z-[4]">
            <Text className="text-white/45 text-[11px] tracking-wide">
              Tap edges to move · {index + 1}/{SLIDES.length}
            </Text>
          </View>
        </View>
      )}
    </Wrapper>
  );
}

