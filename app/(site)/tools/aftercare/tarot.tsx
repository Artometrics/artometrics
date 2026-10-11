import { useCallback, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  Text,
  TextInput,
  View,
} from "react-native";
import { Image } from "expo-image";
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

type SpreadType = "single" | "three";

type TarotCard = {
  cardId?: string;
  name: string;
  reversed?: boolean;
  position?: string;
  imageUrl?: string | null;
};

type TarotPull = {
  id: string;
  spread_type?: SpreadType | string;
  question?: string | null;
  interpretation?: string | null;
  cards?: TarotCard[];
  created_at?: string;
};

function resolveMediaUrl(url?: string | null) {
  if (!url) return null;
  if (/^https?:\/\//i.test(url)) return url;
  if (typeof window !== "undefined" && window.location?.origin) {
    return `${window.location.origin}${url.startsWith("/") ? "" : "/"}${url}`;
  }
  return url;
}

export default function AftercareTarotScreen() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const [spreadType, setSpreadType] = useState<SpreadType>("single");
  const [question, setQuestion] = useState("");
  const [pull, setPull] = useState<TarotPull | null>(null);
  const [history, setHistory] = useState<TarotPull[]>([]);
  const [loading, setLoading] = useState(true);
  const [pulling, setPulling] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadHistory = useCallback(async () => {
    if (!user) return;
    try {
      const res = await apiFetch("aftercare-tarot");
      const data = (await res.json().catch(() => ({}))) as {
        pulls?: TarotPull[];
        error?: string;
      };
      if (!res.ok) {
        setError(data.error || "Could not load pull history.");
        return;
      }
      setHistory(data.pulls ?? []);
      setError(null);
    } catch {
      setError("Could not load pull history.");
    }
  }, [user]);

  useFocusEffect(
    useCallback(() => {
      if (!ready || !user) return;
      let active = true;
      (async () => {
        try {
          setLoading(true);
          await loadHistory();
        } finally {
          if (active) setLoading(false);
        }
      })();
      return () => {
        active = false;
      };
    }, [loadHistory, ready, user]),
  );

  async function onPull() {
    setPulling(true);
    setError(null);
    try {
      const res = await apiFetch("aftercare-tarot", {
        method: "POST",
        body: JSON.stringify({
          spreadType,
          question: question.trim() || undefined,
          withArt: true,
        }),
      });
      const data = (await res.json().catch(() => ({}))) as {
        pull?: TarotPull;
        error?: string;
      };
      if (!res.ok) {
        setError(data.error || "Could not complete this pull.");
        return;
      }
      setPull(data.pull ?? null);
      await loadHistory();
    } catch {
      setError("Could not complete this pull.");
    } finally {
      setPulling(false);
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
        title="Tarot · Aftercare"
        description="Gentle tarot pulls on Artometrics Aftercare."
        path="/tools/aftercare/tarot"
      />
      <ToolsSubnav links={NAV} />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Aftercare</Text>
      <Text className="font-sans text-[36px] font-bold text-fg">Tarot</Text>
      <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
        Ask softly. Sit with what arrives.
      </Text>

      <View className="flex-row flex-wrap gap-2 mt-1">
        {(["single", "three"] as const).map((s) => {
          const active = spreadType === s;
          return (
            <Pressable
              key={s}
              onPress={() => setSpreadType(s)}
              className={[
                "border px-3 py-2",
                active ? "bg-fg border-fg" : "bg-transparent border-border",
              ].join(" ")}
            >
              <Text className={[active ? "text-inverse" : "text-fg", "text-[13px]"].join(" ")}>
                {s === "single" ? "Single card" : "Three-card"}
              </Text>
            </Pressable>
          );
        })}
      </View>

      <TextInput
        value={question}
        onChangeText={setQuestion}
        placeholder="Optional question"
        placeholderTextColorClassName="text-subtle"
        className="border border-border px-3 py-2.5 font-sans text-base text-fg bg-bg-elevated"
      />

      {error ? <Text className="font-sans text-[15px] text-accent">{error}</Text> : null}

      <PrimaryButton
        label={pulling ? "Pulling…" : "Pull cards"}
        onPress={onPull}
        disabled={pulling}
      />

      {pull ? (
        <View className="mt-2 border border-border p-4 gap-2.5">
          <Text className="text-xs tracking-wide uppercase font-bold text-muted">This pull</Text>
          {pull.question ? (
            <Text className="font-sans text-[17px] leading-[26px] text-fg">"{pull.question}"</Text>
          ) : null}
          <View className="flex-row flex-wrap gap-3">
            {(pull.cards ?? []).map((card, i) => {
              const art = resolveMediaUrl(card.imageUrl);
              return (
                <View key={`${card.cardId ?? card.name}-${i}`} className="border border-border p-2.5 w-[140px] gap-1.5">
                  {art ? (
                    <Image
                      source={{ uri: art }}
                      className="w-full aspect-[2/3] bg-base-200"
                      contentFit="cover"
                      transition={200}
                    />
                  ) : (
                    <View className="w-full aspect-[2/3] border border-border bg-bg-elevated items-center justify-center">
                      <Text className="text-subtle text-xs">No art</Text>
                    </View>
                  )}
                  {card.position ? (
                    <Text className="text-[11px] tracking-wide uppercase font-bold text-accent">
                      {card.position}
                    </Text>
                  ) : null}
                  <Text className="font-sans text-[15px] font-bold text-fg">
                    {card.name}
                    {card.reversed ? " (rev.)" : ""}
                  </Text>
                </View>
              );
            })}
          </View>
          {pull.interpretation ? (
            <Text className="font-sans text-base leading-[26px] text-muted">{pull.interpretation}</Text>
          ) : null}
        </View>
      ) : null}

      <Text className="mt-3 text-xs tracking-wide uppercase font-bold text-muted">History</Text>
      {loading ? (
        <ActivityIndicator color={colors.accent} />
      ) : history.length === 0 ? (
        <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
          No pulls yet. Start with a single card.
        </Text>
      ) : (
        <View className="gap-2.5">
          {history.map((h) => (
            <Pressable
              key={h.id}
              onPress={() => setPull(h)}
              className="border border-border p-3 gap-1"
            >
              <Text className="text-xs font-semibold text-accent">
                {h.spread_type === "three" ? "Three-card" : "Single"}
                {h.created_at ? ` · ${new Date(h.created_at).toLocaleDateString()}` : ""}
              </Text>
              <Text className="font-sans text-[15px] leading-[22px] text-fg" numberOfLines={2}>
                {h.question ||
                  (h.cards ?? []).map((c) => c.name).join(", ") ||
                  "Untitled pull"}
              </Text>
            </Pressable>
          ))}
        </View>
      )}
    </Wrapper>
  );
}
