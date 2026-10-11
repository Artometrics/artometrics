import { useMemo, useState } from "react";
import {
  Alert,
  Pressable,
  Text,
  TextInput,
  View,
} from "react-native";
import { Image } from "expo-image";
import { router } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { PrimaryButton } from "@/components/PrimaryButton";
import { PaletteSkiaStrip } from "@/components/PaletteSkiaStrip";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import { extractDominantColors } from "@/lib/palette/extract";
import { recommendFromHexes } from "@/lib/palette/recommend";
import { savePalette } from "@/lib/palette/storage";
import { newPaletteId, type SavedPalette } from "@/lib/palette/types";
import { pickImage } from "@/lib/pickers";

const NAV = [
  { href: "/tools/palette", label: "Saved" },
  { href: "/tools/palette/analyze", label: "Analyze" },
];

export default function PaletteAnalyzeScreen() {
  const { user, ready } = useRequireAuth();
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [hexes, setHexes] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [title, setTitle] = useState("My palette");
  const [tab, setTab] = useState<"editorial" | "drape" | "palette">("editorial");

  const result = useMemo(
    () => (hexes.length ? recommendFromHexes(hexes) : null),
    [hexes],
  );

  async function onPickImage() {
    const picked = await pickImage();
    if (!picked) return;
    setImageUri(picked.uri);
    setBusy(true);
    try {
      const extracted = await extractDominantColors(picked.uri, 6);
      setHexes(extracted);
      setTitle("From photo");
    } catch (e) {
      Alert.alert(
        "Analyze error",
        e instanceof Error ? e.message : "Could not read colors",
      );
    } finally {
      setBusy(false);
    }
  }

  async function onSave() {
    if (!user || !result) return;
    const now = new Date().toISOString();
    const palette: SavedPalette = {
      id: newPaletteId(),
      userId: user.id,
      title: title.trim() || result.season.name,
      seasonId: result.season.id,
      colors: result.season.palette,
      undertone: result.traits.undertone,
      depth: result.traits.depth,
      clarity: result.traits.clarity,
      sourceImageUri: imageUri,
      notes: result.season.tagline,
      createdAt: now,
      updatedAt: now,
    };
    await savePalette(palette);
    Alert.alert("Saved", "Palette saved to your Color Kit.");
    router.push("/tools/palette");
  }

  if (!ready || !user) {
    return (
      <Wrapper variant="narrow" className="gap-2.5 py-8 flex-1">
        <Text className="text-muted">Loading…</Text>
      </Wrapper>
    );
  }

  return (
    <Wrapper className="gap-2.5 py-8 flex-1">
      <PageSeo
        title="Analyze colors"
        description="Get season and palette recommendations from a selfie or photo."
        path="/tools/palette/analyze"
      />
      <ToolsSubnav links={NAV} />
      <Text className="font-sans text-[36px] font-bold text-fg">
        One selfie. Your season.
      </Text>
      <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
        Upload a photo for a suggested season, undertone read, and wearable palette.
      </Text>

      <PrimaryButton label="Upload photo" onPress={() => void onPickImage()} />
      {busy ? (
        <Text className="text-muted">Reading colors…</Text>
      ) : null}

      {result ? (
        <View className="border border-border p-5 gap-3 mt-2 bg-bg-elevated">
          <View className="flex-row justify-between items-center">
            <Text className="text-[13px] text-muted">Your suggested season</Text>
            <Text className="text-[11px] tracking-[2px] font-bold text-subtle">ARTOMETRICS</Text>
          </View>

          <Text className="text-[32px] font-bold font-sans text-fg">
            {result.season.name}
          </Text>
          <Text className="text-[15px] -mt-1 text-muted">
            {result.season.tagline}
          </Text>

          {imageUri ? (
            <View className="flex-row items-center justify-center gap-3 my-2">
              <View className="gap-2">
                {result.season.palette.slice(0, 3).map((c) => (
                  <View
                    key={c}
                    className="w-7 h-10 rounded-lg border border-border"
                    style={{ backgroundColor: c }}
                  />
                ))}
              </View>
              <Image source={{ uri: imageUri }} className="w-40 h-[200px] rounded-2xl" contentFit="cover" transition={200} />
              {tab === "drape" ? (
                <View className="gap-2">
                  {result.season.avoid.slice(0, 4).map((c) => (
                    <View
                      key={c}
                      className="w-7 h-10 rounded-lg border border-border"
                      style={{ backgroundColor: c, opacity: 0.55 }}
                    />
                  ))}
                </View>
              ) : (
                <View style={{ width: 28 }} />
              )}
            </View>
          ) : null}

          <View className="flex-row flex-wrap gap-2">
            {(
              [
                ["UNDERTONE", result.traits.undertone],
                ["DEPTH", result.traits.depth],
                ["CLARITY", result.traits.clarity],
              ] as const
            ).map(([k, v]) => (
              <View key={k} className="border border-border rounded-full px-3 py-2 min-w-[100px] bg-bg">
                <Text className="text-[10px] tracking-wide font-bold text-subtle">{k}</Text>
                <Text className="text-sm font-semibold mt-0.5 text-fg">
                  {v.charAt(0).toUpperCase() + v.slice(1)}
                </Text>
              </View>
            ))}
          </View>

          <View className="flex-row gap-2 mt-1">
            {(["editorial", "drape", "palette"] as const).map((t) => (
              <Pressable
                key={t}
                onPress={() => setTab(t)}
                className={[
                  "border border-border rounded-full px-3.5 py-2",
                  tab === t ? "bg-fg border-fg" : "bg-bg border-border",
                ].join(" ")}
              >
                <Text
                  className={[
                    "text-[13px] font-semibold capitalize",
                    tab === t ? "text-inverse" : "text-fg",
                  ].join(" ")}
                >
                  {t}
                </Text>
              </Pressable>
            ))}
          </View>

          {tab === "palette" || tab === "editorial" ? (
            <View className="gap-2">
              <View className="flex-row flex-wrap gap-2">
                {(tab === "palette" ? result.season.palette : hexes).map((c) => (
                  <View key={c} className="items-center gap-1">
                    <View
                      className="w-12 h-12 border border-border rounded-lg"
                      style={{ backgroundColor: c }}
                    />
                    <Text className="text-subtle text-[10px]">{c}</Text>
                  </View>
                ))}
              </View>
              <PaletteSkiaStrip
                colors={tab === "palette" ? result.season.palette : hexes}
                className="rounded-lg border border-border"
              />
            </View>
          ) : (
            <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
              Your colors, left. Colors to avoid, right.
            </Text>
          )}

          {tab === "editorial" ? (
            <View style={{ gap: 8, marginTop: 8 }}>
              <Text className="text-[11px] tracking-[1.4px] uppercase font-bold text-muted">Colors to avoid</Text>
              <View className="flex-row flex-wrap gap-2">
                {result.season.avoid.map((c) => (
                  <View
                    key={c}
                    className="w-12 h-12 border border-border rounded-lg"
                    style={{ backgroundColor: c }}
                  />
                ))}
              </View>
            </View>
          ) : null}

          <TextInput
            value={title}
            onChangeText={setTitle}
            placeholder="Palette title"
            placeholderTextColorClassName="text-subtle"
            className="text-[28px] font-bold border-b border-border py-1.5 text-fg"
          />
          <PrimaryButton label="Save to profile" onPress={() => void onSave()} />
        </View>
      ) : (
        <Text className="font-sans text-base leading-[26px] max-w-[560px] text-subtle">
          Tip: natural daylight selfies work best. No filter, face in frame.
        </Text>
      )}
    </Wrapper>
  );
}

