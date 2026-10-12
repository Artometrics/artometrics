import { useCallback, useEffect, useState } from "react";
import { ActivityIndicator, Pressable, Text, View } from "react-native";
import { Link, router, useFocusEffect } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { PrimaryButton } from "@/components/PrimaryButton";
import { ToolsAccent } from "@/components/tools/ToolsAccent";
import { useTheme } from "@/lib/theme";
import { useAuth } from "@/lib/auth";
import { loadStudioContinue, type StudioContinue } from "@/lib/platform/studio";
import { useStudioStore } from "@/lib/studio/store";
import { formatUpdated } from "@/lib/twilda/service";

const TOOL_ROUTES: Record<string, "twilda" | "aftercare" | "samples" | "palette"> = {
  "/tools/twilda": "twilda",
  "/tools/aftercare": "aftercare",
  "/tools/samples": "samples",
  "/tools/palette": "palette",
};

function openTool(href: string) {
  const tool = TOOL_ROUTES[href];
  if (tool) useStudioStore.getState().setLastTool(tool);
  router.push(href as `/`);
}

export default function StudioHomeScreen() {
  const { colors } = useTheme();
  const { user, loading: authLoading } = useAuth();
  const [cont, setCont] = useState<StudioContinue | null>(null);
  const [loading, setLoading] = useState(true);
  const hydrateStudio = useStudioStore((s) => s.hydrate);

  useEffect(() => {
    hydrateStudio();
  }, [hydrateStudio]);

  useFocusEffect(
    useCallback(() => {
      if (authLoading) return;
      if (!user) {
        router.replace("/login?next=%2Fstudio");
        return;
      }
      let active = true;
      (async () => {
        try {
          setLoading(true);
          const data = await loadStudioContinue(user.id);
          if (active) setCont(data);
        } finally {
          if (active) setLoading(false);
        }
      })();
      return () => {
        active = false;
      };
    }, [user, authLoading]),
  );

  if (authLoading || !user) {
    return (
      <Wrapper variant="narrow" className="gap-3 py-10">
        <Text className="font-sans text-[17px] leading-7 text-muted">Opening Studio…</Text>
      </Wrapper>
    );
  }

  const empty = !cont?.novel && !cont?.journal && !cont?.aftercareNote;

  return (
    <Wrapper className="gap-3 py-10">
      <PageSeo
        title="Studio"
        description="Write, plan, record samples, and build color kits — your Artometrics workspace."
        path="/studio"
      />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Your workspace</Text>
      <Text className="font-sans text-[42px] font-bold text-fg">Studio</Text>
      <ToolsAccent />
      <Text className="font-sans text-[17px] leading-7 max-w-[560px] text-muted">
        One place to continue writing, check in, and publish when you are ready.
      </Text>

      {loading ? (
        <ActivityIndicator className="mt-8" color={colors.accent} />
      ) : empty ? (
        <View className="mt-5 border border-border bg-bg-elevated p-6 gap-2.5">
          <Text className="font-sans text-[26px] font-bold text-fg">Start with a blank page</Text>
          <Text className="font-sans text-[17px] leading-7 max-w-[560px] text-muted">
            Create a novel in Twilda, or open Aftercare for today's check-in. Your work stays private until
            you publish.
          </Text>
          <PrimaryButton
            label="New novel"
            onPress={() => openTool("/tools/twilda")}
            className="mt-2"
          />
          <Pressable onPress={() => openTool("/tools/aftercare")} className="mt-3">
            <Text className="text-accent font-bold">Open Aftercare →</Text>
          </Pressable>
        </View>
      ) : (
        <View className="mt-5 gap-2.5">
          <Text className="text-[11px] tracking-[1.4px] uppercase font-bold text-muted">Continue</Text>
          {cont?.novel ? (
            <Pressable
              onPress={() => router.push(`/tools/twilda/novels/${cont.novel!.id}`)}
              className="border border-border bg-bg-elevated p-4 gap-1"
            >
              <Text className="text-xs tracking-wide text-accent">Twilda · Novel</Text>
              <Text className="font-sans text-xl font-bold text-fg">{cont.novel.title}</Text>
              <Text className="text-xs tracking-wide text-subtle">
                {formatUpdated(cont.novel.last_opened_at ?? cont.novel.updated_at)}
              </Text>
            </Pressable>
          ) : null}
          {cont?.journal ? (
            <Pressable
              onPress={() => router.push(`/tools/twilda/journal/${cont.journal!.id}`)}
              className="border border-border bg-bg-elevated p-4 gap-1"
            >
              <Text className="text-xs tracking-wide text-accent">Twilda · Journal</Text>
              <Text className="font-sans text-xl font-bold text-fg">{cont.journal.title}</Text>
            </Pressable>
          ) : null}
          {cont?.aftercareNote ? (
            <Pressable
              onPress={() => router.push("/tools/aftercare/journal")}
              className="border border-border bg-bg-elevated p-4 gap-1"
            >
              <Text className="text-xs tracking-wide text-accent">Aftercare</Text>
              <Text className="font-sans text-xl font-bold text-fg">{cont.aftercareNote}</Text>
            </Pressable>
          ) : null}
        </View>
      )}

      <View className="flex-row flex-wrap gap-3 mt-2">
        <PrimaryButton label="Continue writing" onPress={() => openTool("/tools/twilda")} />
        <PrimaryButton
          label="Today's check-in"
          onPress={() => openTool("/tools/aftercare")}
          className="bg-muted"
        />
      </View>

      <View className="mt-5 gap-2.5">
        <Text className="text-[11px] tracking-[1.4px] uppercase font-bold text-muted">Spaces</Text>
        <View className="gap-3">
          {[
            {
              href: "/tools/twilda",
              title: "Twilda",
              body: "Novels, journal, storyboard, Codex.",
            },
            {
              href: "/tools/aftercare",
              title: "Aftercare",
              body: "Journal, tarot, mood, birth tools.",
            },
            {
              href: "/tools/samples",
              title: "Sample Maker",
              body: "Record, synth settings, favorite clips, export.",
            },
            {
              href: "/tools/palette",
              title: "Color Kit",
              body: "Save palettes or get season picks from a photo.",
            },
            {
              href: "/library/reference",
              title: "Reference",
              body: "Public-domain books, art, encyclopedia.",
            },
            {
              href: "/studio/publish",
              title: "Publish",
              body: "Share to your profile or submit to the magazine.",
            },
          ].map((item) => (
            <Link key={item.href} href={item.href as `/tools`} asChild>
              <Pressable
                className="border border-border p-[18px] gap-1.5"
                onPress={() => {
                  const tool = TOOL_ROUTES[item.href];
                  if (tool) useStudioStore.getState().setLastTool(tool);
                }}
              >
                <Text className="font-sans text-[22px] font-bold text-fg">{item.title}</Text>
                <Text className="font-sans text-[15px] leading-6 text-muted">{item.body}</Text>
              </Pressable>
            </Link>
          ))}
        </View>
      </View>
    </Wrapper>
  );
}
