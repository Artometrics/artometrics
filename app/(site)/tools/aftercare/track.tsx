import { useCallback, useMemo, useState } from "react";
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

type TrackingLog = {
  id: string;
  type?: string;
  value?: number | null;
  notes?: string | null;
  label?: string | null;
  logged_on?: string;
  created_at?: string;
};

export default function AftercareTrackScreen() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const [mood, setMood] = useState(3);
  const [note, setNote] = useState("");
  const [logs, setLogs] = useState<TrackingLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const recentMoods = useMemo(
    () =>
      logs
        .filter((l) => l.type === "mood" && typeof l.value === "number")
        .slice(0, 14),
    [logs],
  );

  const maxBar = 5;

  const load = useCallback(async () => {
    if (!user) return;
    try {
      const res = await apiFetch("aftercare-tracking?type=mood");
      const data = (await res.json().catch(() => ({}))) as {
        logs?: TrackingLog[];
        error?: string;
      };
      if (!res.ok) {
        setError(data.error || "Could not load tracking logs.");
        return;
      }
      setLogs(data.logs ?? []);
      setError(null);
    } catch {
      setError("Could not load tracking logs.");
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

  async function onSave() {
    setSaving(true);
    setError(null);
    try {
      const res = await apiFetch("aftercare-tracking", {
        method: "POST",
        body: JSON.stringify({
          type: "mood",
          value: mood,
          notes: note.trim() || undefined,
          label: `Mood ${mood}`,
        }),
      });
      const data = (await res.json().catch(() => ({}))) as {
        log?: TrackingLog;
        error?: string;
      };
      if (!res.ok) {
        setError(data.error || "Could not save mood.");
        return;
      }
      setNote("");
      if (data.log) {
        setLogs((prev) => [data.log!, ...prev]);
      } else {
        await load();
      }
    } catch {
      setError("Could not save mood.");
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
        title="Track · Aftercare"
        description="Mood tracking on Artometrics Aftercare."
        path="/tools/aftercare/track"
      />
      <ToolsSubnav links={NAV} />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Aftercare</Text>
      <Text className="font-sans text-[36px] font-bold text-fg">Track</Text>
      <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
        Log mood from 1 (heavy) to 5 (light). A short note is enough.
      </Text>

      <View className="mt-2 border border-border p-4 gap-2.5">
        <Text className="text-xs tracking-wide uppercase font-bold text-muted">Mood</Text>
        <View className="flex-row gap-2">
          {[1, 2, 3, 4, 5].map((n) => {
            const active = mood === n;
            return (
              <Pressable
                key={n}
                onPress={() => setMood(n)}
                className={[
                  "border w-11 h-11 items-center justify-center",
                  active ? "bg-fg border-fg" : "bg-transparent border-border",
                ].join(" ")}
              >
                <Text
                  className={[
                    "font-bold text-[15px]",
                    active ? "text-inverse" : "text-fg",
                  ].join(" ")}
                >
                  {n}
                </Text>
              </Pressable>
            );
          })}
        </View>
        <TextInput
          multiline
          value={note}
          onChangeText={setNote}
          placeholder="Optional note"
          placeholderTextColorClassName="text-subtle"
          className="border border-border p-3 min-h-[88px] font-sans text-base leading-6 text-fg bg-bg-elevated"
          style={{ textAlignVertical: "top" }}
        />
        {error ? <Text className="font-sans text-[15px] text-accent">{error}</Text> : null}
        <PrimaryButton
          label={saving ? "Saving…" : "Log mood"}
          onPress={onSave}
          disabled={saving}
        />
      </View>

      <Text className="mt-3 text-xs tracking-wide uppercase font-bold text-muted">Recent</Text>
      {loading ? (
        <ActivityIndicator color={colors.accent} />
      ) : recentMoods.length === 0 ? (
        <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
          No mood logs yet.
        </Text>
      ) : (
        <>
          <View className="flex-row items-end gap-1.5 min-h-[88px] py-2">
            {[...recentMoods].reverse().map((log) => {
              const v = Number(log.value) || 0;
              const height = Math.max(8, (v / maxBar) * 72);
              return (
                <View key={log.id} className="items-center gap-1 flex-1 max-w-7">
                  <View className="w-full min-h-2 bg-accent" style={{ height }} />
                  <Text className="text-[10px] text-subtle">{v}</Text>
                </View>
              );
            })}
          </View>
          <View className="gap-2">
            {recentMoods.map((log) => (
              <View key={`row-${log.id}`} className="border border-border p-3 flex-row gap-3 items-start">
                <Text className="font-sans text-lg font-bold min-w-10 text-fg">{log.value}/5</Text>
                <View className="flex-1 gap-0.5">
                  <Text className="text-xs text-subtle">
                    {log.logged_on ||
                      (log.created_at ? new Date(log.created_at).toLocaleDateString() : "")}
                  </Text>
                  {log.notes ? (
                    <Text className="font-sans text-[15px] leading-[22px] text-muted">{log.notes}</Text>
                  ) : null}
                </View>
              </View>
            ))}
          </View>
        </>
      )}
    </Wrapper>
  );
}
