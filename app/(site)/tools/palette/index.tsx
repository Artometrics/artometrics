import { useCallback, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Platform,
  Pressable,
  Text,
  View,
} from "react-native";
import { router, useFocusEffect } from "expo-router";
import * as Clipboard from "expo-clipboard";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { ToolsAccent } from "@/components/tools/ToolsAccent";
import { PrimaryButton } from "@/components/PrimaryButton";
import { useTheme } from "@/lib/theme";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import {
  deletePalette,
  listPalettes,
  paletteToExportJson,
} from "@/lib/palette/storage";
import type { SavedPalette } from "@/lib/palette/types";
import { seasonById } from "@/lib/palette/types";

const NAV = [
  { href: "/tools/palette", label: "Saved" },
  { href: "/tools/palette/analyze", label: "Analyze" },
];

export default function PaletteHomeScreen() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const [items, setItems] = useState<SavedPalette[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!user) return;
    setItems(await listPalettes(user.id));
  }, [user]);

  useFocusEffect(
    useCallback(() => {
      if (!ready || !user) return;
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
    }, [load, ready, user]),
  );

  async function onExport(palette: SavedPalette) {
    const json = paletteToExportJson(palette);
    try {
      await Clipboard.setStringAsync(json);
      if (Platform.OS === "web" && typeof document !== "undefined") {
        const blob = new Blob([json], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${palette.title.replace(/\s+/g, "-").toLowerCase()}.json`;
        a.click();
        URL.revokeObjectURL(url);
      }
      Alert.alert("Exported", "Palette JSON copied / downloaded.");
    } catch {
      Alert.alert("Export failed", "Could not export palette.");
    }
  }

  if (!ready || !user) {
    return (
      <Wrapper variant="narrow" className="gap-2.5 py-8">
        <Text className="text-muted">Opening Color Kit…</Text>
      </Wrapper>
    );
  }

  return (
    <Wrapper className="gap-2.5 py-8">
      <PageSeo
        title="Color Kit"
        description="Save color palettes or get season recommendations from a selfie or photo."
        path="/tools/palette"
      />
      <ToolsSubnav links={NAV} />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Studio</Text>
      <Text className="font-sans text-[36px] font-bold text-fg">Color Kit</Text>
      <ToolsAccent />
      <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
        Analyze a photo for season + palette recommendations, then save looks to your profile.
      </Text>

      <PrimaryButton
        label="Analyze a photo"
        onPress={() => router.push("/tools/palette/analyze")}
        className="mt-3"
      />

      {loading ? (
        <ActivityIndicator className="mt-7" color={colors.accent} />
      ) : items.length === 0 ? (
        <View className="mt-5 border border-border bg-bg-elevated p-[22px] gap-2">
          <Text className="text-[22px] font-bold font-sans text-fg">No saved palettes</Text>
          <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
            Upload a selfie or photo to get your suggested season and swatches.
          </Text>
        </View>
      ) : (
        <View className="mt-4 gap-3">
          {items.map((pal) => {
            const season = pal.seasonId ? seasonById(pal.seasonId) : null;
            return (
              <View key={pal.id} className="border border-border p-4 gap-2">
                <Text className="text-xl font-bold font-sans text-fg">{pal.title}</Text>
                {season ? (
                  <Text className="text-[13px] leading-5 text-accent">
                    {season.name} — {season.tagline}
                  </Text>
                ) : null}
                <View className="flex-row flex-wrap gap-2 mt-1">
                  {pal.colors.map((c) => (
                    <View
                      key={c}
                      className="w-9 h-12 border border-border rounded-md"
                      style={{ backgroundColor: c }}
                    />
                  ))}
                </View>
                <View className="flex-row gap-4 mt-1.5">
                  <Pressable onPress={() => void onExport(pal)} hitSlop={8}>
                    <Text className="text-accent font-bold text-[13px]">Export</Text>
                  </Pressable>
                  <Pressable
                    onPress={() =>
                      Alert.alert("Delete palette?", pal.title, [
                        { text: "Cancel", style: "cancel" },
                        {
                          text: "Delete",
                          style: "destructive",
                          onPress: () => void deletePalette(user.id, pal.id).then(load),
                        },
                      ])
                    }
                    hitSlop={8}
                  >
                    <Text className="text-muted text-[13px]">Delete</Text>
                  </Pressable>
                </View>
              </View>
            );
          })}
        </View>
      )}
    </Wrapper>
  );
}
