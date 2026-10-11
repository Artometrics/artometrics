import { useMemo, useState } from "react";
import { Alert, Pressable, Text, TextInput, View } from "react-native";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import {
  pinReference,
  searchReference,
  type ReferenceSource,
} from "@/lib/reference/catalog";

const NAV = [
  { href: "/tools/twilda", label: "Library" },
  { href: "/tools/twilda/journal", label: "Journal" },
  { href: "/tools/twilda/reference", label: "Reference" },
];

const FILTERS: { id: ReferenceSource | "all"; label: string }[] = [
  { id: "all", label: "All" },
  { id: "gutenberg", label: "Gutenberg" },
  { id: "wikiart", label: "WikiArt" },
  { id: "wikipedia", label: "Wikipedia" },
];

export default function TwildaReferenceScreen() {
  const { user, ready } = useRequireAuth();
  const [source, setSource] = useState<ReferenceSource | "all">("all");
  const [q, setQ] = useState("");
  const items = useMemo(() => searchReference(q, source).slice(0, 100), [q, source]);

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
        title="Twilda Reference"
        description="Pin public-domain sources into your research."
        path="/tools/twilda/reference"
      />
      <ToolsSubnav links={NAV} />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Twilda</Text>
      <Text className="font-sans text-[36px] font-bold text-fg">Reference</Text>
      <Text className="font-sans text-base leading-[26px] max-w-[640px] text-muted">
        Gutenberg, WikiArt/Wikimedia, and Wikipedia — pin items to your profile.
      </Text>

      <View className="flex-row flex-wrap gap-2">
        {FILTERS.map((f) => {
          const active = source === f.id;
          return (
            <Pressable
              key={f.id}
              onPress={() => setSource(f.id)}
              className={[
                "border px-3 py-2",
                active ? "bg-fg border-fg" : "bg-transparent border-border",
              ].join(" ")}
            >
              <Text className={[active ? "text-inverse" : "text-fg", "text-[13px]"].join(" ")}>
                {f.label}
              </Text>
            </Pressable>
          );
        })}
      </View>

      <TextInput
        value={q}
        onChangeText={setQ}
        placeholder="Search…"
        placeholderTextColorClassName="text-subtle"
        className="border border-border px-3 py-2.5 text-fg bg-bg-elevated"
      />

      <View className="mt-1">
        {items.map((item) => (
          <View
            key={`${item.source}-${item.id}`}
            className="py-3.5 border-b border-border gap-1"
          >
            <Text className="text-[11px] tracking-[1.2px] uppercase font-bold text-accent">
              {item.source}
            </Text>
            <Text className="font-sans text-lg text-fg">
              {item.title || item.label}
            </Text>
            <Text className="text-sm leading-5 text-muted" numberOfLines={2}>
              {[item.authors?.join(", "), item.artist, item.description, item.style]
                .filter(Boolean)
                .join(" · ")}
            </Text>
            <Pressable
              onPress={async () => {
                try {
                  await pinReference(user!.id, {
                    source: item.source,
                    external_id: String(item.id),
                    title: item.title || item.label || "Untitled",
                    url: item.url || item.downloadUrl,
                    payload: item as unknown as Record<string, unknown>,
                  });
                  Alert.alert("Pinned", "Saved to your reference pins.");
                } catch (e) {
                  Alert.alert("Pin failed", e instanceof Error ? e.message : "Error");
                }
              }}
            >
              <Text className="text-accent font-bold mt-1.5">Pin →</Text>
            </Pressable>
          </View>
        ))}
      </View>
    </Wrapper>
  );
}
