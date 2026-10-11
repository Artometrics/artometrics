import { useCallback, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Pressable,
  RefreshControl,
  Text,
  View,
} from "react-native";
import { FlashList } from "@shopify/flash-list";
import { router, useFocusEffect } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { CoverTile } from "@/components/twilda/CoverTile";
import { PrimaryButton } from "@/components/PrimaryButton";
import { useTheme } from "@/lib/theme";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import { getSupabase } from "@/lib/supabase/client";
import {
  createNovel,
  formatUpdated,
  listNovels,
  type DbNovelSummary,
} from "@/lib/twilda/service";

const NAV = [
  { href: "/tools/twilda", label: "Library" },
  { href: "/tools/twilda/journal", label: "Journal" },
  { href: "/tools/twilda/reference", label: "Reference" },
];

export default function TwildaLibraryScreen() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const [novels, setNovels] = useState<DbNovelSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    if (!user) return;
    const supabase = getSupabase();
    if (!supabase) throw new Error("Supabase is not configured");
    const { ensureStarterNovels } = await import("@/lib/twilda/starters");
    await ensureStarterNovels(supabase as never, user.id);
    const rows = await listNovels(supabase as never, user.id);
    setNovels(rows);
  }, [user]);

  useFocusEffect(
    useCallback(() => {
      if (!ready || !user) return;
      let active = true;
      (async () => {
        try {
          setLoading(true);
          await load();
        } catch (e) {
          if (active) {
            Alert.alert("Library error", e instanceof Error ? e.message : "Failed to load");
          }
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
    try {
      const supabase = getSupabase();
      if (!supabase) throw new Error("Supabase is not configured");
      const id = await createNovel(supabase as never, user.id);
      router.push(`/tools/twilda/novels/${id}`);
    } catch (e) {
      Alert.alert("Could not create novel", e instanceof Error ? e.message : "Unknown error");
    }
  }

  if (!ready) {
    return (
      <Wrapper className="gap-2.5 py-8">
        <Text className="text-muted">Loading…</Text>
      </Wrapper>
    );
  }

  return (
    <Wrapper className="gap-2.5 py-8">
      <PageSeo title="Twilda" description="Story workspace on Artometrics." path="/tools/twilda" />
      <ToolsSubnav links={NAV} />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Twilda</Text>
      <Text className="font-sans text-[36px] font-bold text-fg">Library</Text>
      <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
        Plan, write, storyboard, and keep your Codex in one place.
      </Text>
      <PrimaryButton label="New novel" onPress={onCreate} />

      {loading ? (
        <ActivityIndicator className="mt-10" color={colors.accent} />
      ) : novels.length === 0 ? (
        <Text className="font-sans text-base leading-[26px] max-w-[560px] mt-6 text-muted">
          No novels yet. Create a blank novel or wait for starters to seed.
        </Text>
      ) : (
        <FlashList
          data={novels}
          keyExtractor={(item) => item.id}
          numColumns={2}
          contentContainerClassName="pt-4 pb-6"
          scrollEnabled={false}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={async () => {
                setRefreshing(true);
                try {
                  await load();
                } finally {
                  setRefreshing(false);
                }
              }}
            />
          }
          ListHeaderComponent={
            <Text className="text-xs mb-3 uppercase tracking-wide text-muted">
              {novels.length} {novels.length === 1 ? "novel" : "novels"}
            </Text>
          }
          renderItem={({ item }) => (
            <CoverTile
              title={item.title}
              author={item.author}
              coverKind={item.cover_kind}
              updated={formatUpdated(item.last_opened_at ?? item.updated_at)}
              onPress={() => router.push(`/tools/twilda/novels/${item.id}`)}
            />
          )}
        />
      )}

      <Pressable onPress={() => router.push("/tools/twilda/reference")} className="mt-2">
        <Text className="text-accent font-bold">Browse reference library →</Text>
      </Pressable>
    </Wrapper>
  );
}
