import { useCallback, useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Text,
  TextInput,
  View,
} from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { PrimaryButton } from "@/components/PrimaryButton";
import { useTheme } from "@/lib/theme";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import { getSupabase } from "@/lib/supabase/client";
import { paramString } from "@/lib/params";
import {
  deleteJournalEntry,
  getJournalEntry,
  updateJournalEntry,
} from "@/lib/twilda/journal";

export function generateStaticParams() {
  return [];
}

const NAV = [
  { href: "/tools/twilda", label: "Library" },
  { href: "/tools/twilda/journal", label: "Journal" },
  { href: "/tools/twilda/reference", label: "Reference" },
];

export default function TwildaJournalEntryScreen() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const params = useLocalSearchParams<{ id?: string | string[] }>();
  const id = paramString(params.id);
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(true);
  const [saveState, setSaveState] = useState<"idle" | "saving" | "saved">("idle");
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const load = useCallback(async () => {
    if (!user || !id) return;
    const entry = await getJournalEntry(getSupabase() as never, user.id, id);
    if (!entry) throw new Error("Entry not found");
    setTitle(entry.title);
    setBody(entry.body);
  }, [user, id]);

  useEffect(() => {
    if (!ready || !user || !id) return;
    (async () => {
      try {
        setLoading(true);
        await load();
      } catch (e) {
        Alert.alert("Error", e instanceof Error ? e.message : "Failed");
        router.replace("/tools/twilda/journal");
      } finally {
        setLoading(false);
      }
    })();
  }, [ready, user, id, load]);

  function scheduleSave(nextTitle: string, nextBody: string) {
    setSaveState("saving");
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(async () => {
      if (!user || !id) return;
      try {
        await updateJournalEntry(getSupabase() as never, user.id, id, {
          title: nextTitle,
          body: nextBody,
        });
        setSaveState("saved");
      } catch {
        setSaveState("idle");
      }
    }, 700);
  }

  if (!ready || loading) {
    return (
      <Wrapper className="gap-2.5 py-7">
        <ActivityIndicator color={colors.accent} />
      </Wrapper>
    );
  }

  return (
    <Wrapper className="gap-2.5 py-7">
      <PageSeo title={title || "Journal"} path={`/tools/twilda/journal/${id}`} />
      <ToolsSubnav links={NAV} />
      <Text className="text-xs min-h-4 text-muted">
        {saveState === "saving" ? "Saving…" : saveState === "saved" ? "Saved" : " "}
      </Text>
      <TextInput
        value={title}
        onChangeText={(t) => {
          setTitle(t);
          scheduleSave(t, body);
        }}
        placeholder="Title"
        placeholderTextColorClassName="text-subtle"
        className="font-sans text-[28px] font-bold border-b border-border py-2 text-fg"
      />
      <TextInput
        multiline
        value={body}
        onChangeText={(t) => {
          setBody(t);
          scheduleSave(title, t);
        }}
        placeholder="Write…"
        placeholderTextColorClassName="text-subtle"
        className="border border-border min-h-[320px] p-3.5 font-sans text-[17px] leading-7 text-fg bg-bg-elevated"
        style={{ textAlignVertical: "top" }}
      />
      <View className="flex-row flex-wrap gap-3">
        <PrimaryButton
          label="Back"
          className="bg-fg"
          onPress={() => router.push("/tools/twilda/journal")}
        />
        <PrimaryButton
          label="Publish…"
          className="bg-muted"
          onPress={() =>
            router.push(
              `/studio/publish?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body.slice(0, 4000))}&source=twilda_journal&sourceId=${id}`,
            )
          }
        />
        <PrimaryButton
          label="Delete"
          className="bg-muted"
          onPress={() =>
            Alert.alert("Delete entry?", "This cannot be undone.", [
              { text: "Cancel", style: "cancel" },
              {
                text: "Delete",
                style: "destructive",
                onPress: async () => {
                  await deleteJournalEntry(getSupabase() as never, user!.id, id!);
                  router.replace("/tools/twilda/journal");
                },
              },
            ])
          }
        />
      </View>
    </Wrapper>
  );
}
