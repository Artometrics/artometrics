import { useCallback, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Pressable,
  RefreshControl,
  Text,
} from "react-native";
import { FlashList } from "@shopify/flash-list";
import { router, useFocusEffect } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { PrimaryButton } from "@/components/PrimaryButton";
import { useTheme } from "@/lib/theme";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import { getSupabase } from "@/lib/supabase/client";
import {
  createJournalEntry,
  formatJournalDate,
  listJournalEntries,
  type JournalEntry,
} from "@/lib/twilda/journal";

const NAV = [
  { href: "/tools/twilda", label: "Library" },
  { href: "/tools/twilda/journal", label: "Journal" },
  { href: "/tools/twilda/reference", label: "Reference" },
];

export default function TwildaJournalScreen() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const [entries, setEntries] = useState<
    Pick<JournalEntry, "id" | "title" | "body" | "created_at" | "updated_at">[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    if (!user) return;
    const supabase = getSupabase();
    if (!supabase) throw new Error("Supabase is not configured");
    setEntries(await listJournalEntries(supabase as never, user.id));
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
          if (active) Alert.alert("Journal error", e instanceof Error ? e.message : "Failed");
        } finally {
          if (active) setLoading(false);
        }
      })();
      return () => {
        active = false;
      };
    }, [load, ready, user]),
  );

  if (!ready) {
    return (
      <Wrapper className="gap-2.5 py-8">
        <Text className="text-muted">Loading…</Text>
      </Wrapper>
    );
  }

  return (
    <Wrapper className="gap-2.5 py-8">
      <PageSeo title="Twilda Journal" description="Private writing notes." path="/tools/twilda/journal" />
      <ToolsSubnav links={NAV} />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Twilda</Text>
      <Text className="font-sans text-[36px] font-bold text-fg">Journal</Text>
      <Text className="font-sans text-base leading-[26px] text-muted">
        Private notes — only you can see these.
      </Text>
      <PrimaryButton
        label="New entry"
        onPress={async () => {
          try {
            const entry = await createJournalEntry(getSupabase() as never, user!.id);
            router.push(`/tools/twilda/journal/${entry.id}`);
          } catch (e) {
            Alert.alert("Could not create entry", e instanceof Error ? e.message : "Error");
          }
        }}
      />
      {loading ? (
        <ActivityIndicator className="mt-8" color={colors.accent} />
      ) : (
        <FlashList
          data={entries}
          keyExtractor={(item) => item.id}
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
          ListEmptyComponent={
            <Text className="font-sans text-base leading-[26px] mt-5 text-muted">
              No entries yet.
            </Text>
          }
          renderItem={({ item }) => (
            <Pressable
              onPress={() => router.push(`/tools/twilda/journal/${item.id}`)}
              className="py-3.5 border-b border-border gap-1"
            >
              <Text className="font-sans text-lg text-fg">
                {item.title || "Untitled"}
              </Text>
              <Text className="text-muted text-[13px]">
                {formatJournalDate(item.updated_at)}
              </Text>
            </Pressable>
          )}
        />
      )}
    </Wrapper>
  );
}
