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
  deleteSamplePack,
  listSamplePacks,
  packToExportJson,
  saveSamplePack,
} from "@/lib/samples/storage";
import {
  DEFAULT_SYNTH,
  newPackId,
  type SamplePack,
} from "@/lib/samples/types";

const NAV = [
  { href: "/tools/samples", label: "Packs" },
  { href: "/tools/samples/record", label: "Record" },
];

export default function SamplesHomeScreen() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const [packs, setPacks] = useState<SamplePack[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!user) return;
    setPacks(await listSamplePacks(user.id));
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

  async function onCreate() {
    if (!user) return;
    const now = new Date().toISOString();
    const pack: SamplePack = {
      id: newPackId(),
      userId: user.id,
      title: `Sample pack ${new Date().toLocaleDateString()}`,
      sourceUri: null,
      durationSec: 0,
      synth: { ...DEFAULT_SYNTH },
      clips: [],
      createdAt: now,
      updatedAt: now,
    };
    await saveSamplePack(pack);
    router.push(`/tools/samples/${pack.id}`);
  }

  async function onExport(pack: SamplePack) {
    const json = packToExportJson(pack);
    try {
      await Clipboard.setStringAsync(json);
      Alert.alert("Exported", "Favorite clips JSON copied to clipboard.");
    } catch {
      if (Platform.OS === "web" && typeof document !== "undefined") {
        const blob = new Blob([json], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${pack.title.replace(/\s+/g, "-").toLowerCase()}.json`;
        a.click();
        URL.revokeObjectURL(url);
      } else {
        Alert.alert("Export failed", "Could not copy export JSON.");
      }
    }
  }

  if (!ready || !user) {
    return (
      <Wrapper variant="narrow" className="gap-2.5 py-8">
        <Text className="text-muted">Opening Sample Maker…</Text>
      </Wrapper>
    );
  }

  return (
    <Wrapper className="gap-2.5 py-8">
      <PageSeo
        title="Sample Maker"
        description="Record audio, shape it with synth settings, and save favorite clips to your profile."
        path="/tools/samples"
      />
      <ToolsSubnav links={NAV} />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Studio</Text>
      <Text className="font-sans text-[36px] font-bold text-fg">Sample Maker</Text>
      <ToolsAccent />
      <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
        Record a sound, tweak synth settings, mark favorite clips, and export the pack.
      </Text>

      <PrimaryButton label="New pack" onPress={onCreate} className="mt-3" />
      <Pressable onPress={() => router.push("/tools/samples/record")} className="mt-3">
        <Text className="text-accent font-bold">Quick record →</Text>
      </Pressable>

      {loading ? (
        <ActivityIndicator className="mt-7" color={colors.accent} />
      ) : packs.length === 0 ? (
        <View className="mt-5 border border-border bg-bg-elevated p-[22px] gap-2">
          <Text className="text-[22px] font-bold font-sans text-fg">No packs yet</Text>
          <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
            Start a recording and save clips you want to keep.
          </Text>
        </View>
      ) : (
        <View className="mt-4 gap-3">
          {packs.map((pack) => (
            <Pressable
              key={pack.id}
              onPress={() => router.push(`/tools/samples/${pack.id}`)}
              className="border border-border p-4 gap-1.5"
            >
              <Text className="text-xl font-bold font-sans text-fg">{pack.title}</Text>
              <Text className="text-xs tracking-wide text-subtle">
                {pack.clips.filter((c) => c.favorite).length} favorites ·{" "}
                {pack.synth.preset} · {new Date(pack.updatedAt).toLocaleDateString()}
              </Text>
              <View className="flex-row gap-4 mt-2">
                <Pressable
                  onPress={(e) => {
                    e.stopPropagation?.();
                    void onExport(pack);
                  }}
                  hitSlop={8}
                >
                  <Text className="text-accent font-bold text-[13px]">Export</Text>
                </Pressable>
                <Pressable
                  onPress={(e) => {
                    e.stopPropagation?.();
                    Alert.alert("Delete pack?", pack.title, [
                      { text: "Cancel", style: "cancel" },
                      {
                        text: "Delete",
                        style: "destructive",
                        onPress: () => void deleteSamplePack(user.id, pack.id).then(load),
                      },
                    ]);
                  }}
                  hitSlop={8}
                >
                  <Text className="text-muted text-[13px]">Delete</Text>
                </Pressable>
              </View>
            </Pressable>
          ))}
        </View>
      )}
    </Wrapper>
  );
}
