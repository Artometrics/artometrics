import { useCallback, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  Text,
  TextInput,
  View,
} from "react-native";
import { useFocusEffect } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { PrimaryButton } from "@/components/PrimaryButton";
import { useTheme } from "@/lib/theme";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import { apiFetch } from "@/lib/supabase/client";

const NAV = [
  { href: "/tools/aftercare", label: "Home" },
  { href: "/tools/aftercare/journal", label: "Journal" },
  { href: "/tools/aftercare/tarot", label: "Tarot" },
  { href: "/tools/aftercare/track", label: "Track" },
  { href: "/tools/aftercare/tools", label: "Birth tools" },
];

const MOODS = [
  "tender",
  "clear",
  "heavy",
  "hopeful",
  "restless",
  "grateful",
] as const;

type Mood = (typeof MOODS)[number];

type JournalEntry = {
  id: string;
  title?: string | null;
  body: string;
  mood?: string | null;
  created_at?: string;
};

export default function AftercareJournalScreen() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [mood, setMood] = useState<Mood>("tender");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!user) return;
    try {
      const res = await apiFetch("aftercare-journal");
      const data = (await res.json().catch(() => ({}))) as {
        entries?: JournalEntry[];
        error?: string;
      };
      if (!res.ok) {
        setError(data.error || "Could not load journal entries.");
        return;
      }
      setError(null);
      setEntries(data.entries ?? []);
    } catch {
      setError("Could not load journal entries.");
    }
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
    if (!body.trim()) {
      setError("Write a few lines before saving.");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const res = await apiFetch("aftercare-journal", {
        method: "POST",
        body: JSON.stringify({
          title: title.trim() || undefined,
          body: body.trim(),
          mood,
        }),
      });
      const data = (await res.json().catch(() => ({}))) as {
        entry?: JournalEntry;
        error?: string;
      };
      if (!res.ok) {
        setError(data.error || "Could not save entry.");
        return;
      }
      setTitle("");
      setBody("");
      if (data.entry) {
        setEntries((prev) => [data.entry!, ...prev]);
      } else {
        await load();
      }
    } catch {
      setError("Could not save entry.");
    } finally {
      setSaving(false);
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
      <PageSeo
        title="Journal · Aftercare"
        description="Mood-tagged journal on Artometrics Aftercare."
        path="/tools/aftercare/journal"
      />
      <ToolsSubnav links={NAV} />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Aftercare</Text>
      <Text className="font-sans text-[36px] font-bold text-fg">Journal</Text>
      <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
        Name the feeling, then write what wants tending.
      </Text>

      <View className="mt-2 border border-border p-4 gap-2.5">
        <Text className="text-xs tracking-wide uppercase font-bold text-muted">Mood</Text>
        <View className="flex-row flex-wrap gap-2">
          {MOODS.map((m) => {
            const active = mood === m;
            return (
              <Pressable
                key={m}
                onPress={() => setMood(m)}
                className={[
                  "border px-3 py-2",
                  active ? "bg-fg border-fg" : "bg-transparent border-border",
                ].join(" ")}
              >
                <Text
                  className={[
                    "text-[13px] capitalize",
                    active ? "text-inverse" : "text-fg",
                  ].join(" ")}
                >
                  {m}
                </Text>
              </Pressable>
            );
          })}
        </View>

        <TextInput
          value={title}
          onChangeText={setTitle}
          placeholder="Title (optional)"
          placeholderTextColorClassName="text-subtle"
          className="border border-border px-3 py-2.5 font-sans text-base text-fg bg-bg-elevated"
        />
        <TextInput
          multiline
          value={body}
          onChangeText={setBody}
          placeholder="What softens, what stays…"
          placeholderTextColorClassName="text-subtle"
          className="border border-border p-3 min-h-[140px] font-sans text-base leading-[26px] text-fg bg-bg-elevated"
          style={{ textAlignVertical: "top" }}
        />
        {error ? <Text className="font-sans text-[15px] text-accent">{error}</Text> : null}
        <PrimaryButton
          label={saving ? "Saving…" : "Save entry"}
          onPress={onCreate}
          disabled={saving}
        />
      </View>

      <Text className="mt-4 text-xs tracking-wide uppercase font-bold text-muted">
        Recent entries
      </Text>
      {loading ? (
        <ActivityIndicator color={colors.accent} />
      ) : entries.length === 0 ? (
        <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
          No entries yet. Start with whatever is true today.
        </Text>
      ) : (
        <View className="gap-3 mt-1">
          {entries.map((entry) => (
            <View key={entry.id} className="border border-border p-3.5 gap-1.5">
              <View className="flex-row justify-between items-center">
                {entry.mood ? (
                  <Text className="text-xs tracking-wide uppercase font-bold text-accent">
                    {entry.mood}
                  </Text>
                ) : null}
                {entry.created_at ? (
                  <Text className="text-xs text-subtle">
                    {new Date(entry.created_at).toLocaleDateString()}
                  </Text>
                ) : null}
              </View>
              {entry.title ? (
                <Text className="font-sans text-lg font-bold text-fg">{entry.title}</Text>
              ) : null}
              <Text className="font-sans text-[15px] leading-6 text-muted">{entry.body}</Text>
            </View>
          ))}
        </View>
      )}
    </Wrapper>
  );
}
