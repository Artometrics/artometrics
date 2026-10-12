import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Pressable,
  ScrollView,
  Text,
  TextInput,
  View,
} from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { StudioBreadcrumb } from "@/components/studio/StudioBreadcrumb";
import { StudioSelect } from "@/components/studio/StudioSelect";
import { PrimaryButton } from "@/components/PrimaryButton";
import { useTheme } from "@/lib/theme";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import { getSupabase } from "@/lib/supabase/client";
import { paramString } from "@/lib/params";
import {
  createChapter,
  createCodexEntry,
  createScene,
  deleteNovel,
  getNovelFull,
  updateNovelMetadata,
  updateSceneContent,
  type DbNovelFull,
} from "@/lib/twilda/service";
import {
  createStoryboardPanel,
  listStoryboardPanels,
  type StoryboardPanel,
} from "@/lib/twilda/storyboard";
import type { CoverKind } from "@/lib/twilda/novelcrafter/data";

/** Client-only workspace — no pre-rendered novel IDs at export time. */
export function generateStaticParams() {
  return [];
}

type Mode = "plan" | "write" | "board" | "codex" | "settings";

const MODES: { id: Mode; label: string }[] = [
  { id: "plan", label: "Plan" },
  { id: "write", label: "Write" },
  { id: "board", label: "Board" },
  { id: "codex", label: "Codex" },
  { id: "settings", label: "Settings" },
];

const COVER_OPTIONS: { value: CoverKind; label: string }[] = [
  { value: "gatsby", label: "Gatsby" },
  { value: "trinity", label: "Trinity" },
  { value: "cardinal", label: "Cardinal" },
  { value: "apocrypha", label: "Apocrypha" },
  { value: "artometrics", label: "Artometrics" },
  { value: "psychonomics", label: "Psychonomics" },
  { value: "plain", label: "Plain" },
];

const NAV = [
  { href: "/tools/twilda", label: "Library" },
  { href: "/tools/twilda/journal", label: "Journal" },
  { href: "/tools/twilda/reference", label: "Reference" },
];

function stripHtml(html: string): string {
  return html
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n\n")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .trim();
}

function toHtml(text: string): string {
  return text
    .split(/\n{2,}/)
    .map((p) => `<p>${p.replace(/\n/g, "<br/>")}</p>`)
    .join("");
}

function sb() {
  const client = getSupabase();
  if (!client) throw new Error("Supabase is not configured");
  return client as never;
}

export default function TwildaNovelWorkspace() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const params = useLocalSearchParams<{ id?: string | string[] }>();
  const id = paramString(params.id);
  const [novel, setNovel] = useState<DbNovelFull | null>(null);
  const [mode, setMode] = useState<Mode>("write");
  const [loading, setLoading] = useState(true);
  const [activeSceneId, setActiveSceneId] = useState<string | null>(null);
  const [sceneText, setSceneText] = useState("");
  const [panels, setPanels] = useState<StoryboardPanel[]>([]);
  const [saveState, setSaveState] = useState<"idle" | "saving" | "saved">("idle");
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [synopsis, setSynopsis] = useState("");
  const [series, setSeries] = useState("");
  const [coverKind, setCoverKind] = useState<CoverKind>("plain");
  const saveTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const load = useCallback(async () => {
    if (!user || !id) return;
    const data = await getNovelFull(sb(), user.id, id);
    setNovel(data);
    if (data) {
      setTitle(data.title);
      setAuthor(data.author);
      setSynopsis(data.synopsis);
      setSeries(data.series_name ?? "");
      setCoverKind(data.cover_kind);
      const firstScene = data.chapters[0]?.scenes[0];
      if (firstScene && !activeSceneId) {
        setActiveSceneId(firstScene.id);
        setSceneText(stripHtml(firstScene.content || ""));
      }
      const board = await listStoryboardPanels(sb(), user.id, id, data.active_draft_id);
      setPanels(board);
    }
  }, [user, id, activeSceneId]);

  useEffect(() => {
    if (!ready || !user || !id) return;
    let active = true;
    (async () => {
      try {
        setLoading(true);
        await load();
      } catch (e) {
        if (active) Alert.alert("Workspace error", e instanceof Error ? e.message : "Failed");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready, user, id]);

  const activeScene = useMemo(() => {
    if (!novel || !activeSceneId) return null;
    for (const ch of novel.chapters) {
      const scene = ch.scenes.find((s) => s.id === activeSceneId);
      if (scene) return { chapter: ch, scene };
    }
    return null;
  }, [novel, activeSceneId]);

  const chapterOptions = useMemo(() => {
    if (!novel) return [];
    return novel.chapters.map((ch, i) => ({
      value: ch.id,
      label: ch.title || `Chapter ${i + 1}`,
    }));
  }, [novel]);

  const activeChapterId = activeScene?.chapter.id ?? chapterOptions[0]?.value ?? "";

  const sceneOptions = useMemo(() => {
    if (!novel || !activeChapterId) return [];
    const ch = novel.chapters.find((c) => c.id === activeChapterId);
    if (!ch) return [];
    return ch.scenes.map((sc, i) => ({
      value: sc.id,
      label: sc.title || `Scene ${i + 1}`,
    }));
  }, [novel, activeChapterId]);

  const chapterIndex = useMemo(() => {
    if (!novel || !activeScene) return 0;
    return novel.chapters.findIndex((c) => c.id === activeScene.chapter.id) + 1;
  }, [novel, activeScene]);

  const sceneIndex = useMemo(() => {
    if (!activeScene) return 0;
    return activeScene.chapter.scenes.findIndex((s) => s.id === activeScene.scene.id) + 1;
  }, [activeScene]);

  function selectChapter(chapterId: string) {
    if (!novel) return;
    const ch = novel.chapters.find((c) => c.id === chapterId);
    const first = ch?.scenes[0];
    if (first) {
      setActiveSceneId(first.id);
      setSceneText(stripHtml(first.content || ""));
    }
  }

  function selectScene(sceneId: string) {
    if (!novel) return;
    for (const ch of novel.chapters) {
      const scene = ch.scenes.find((s) => s.id === sceneId);
      if (scene) {
        setActiveSceneId(scene.id);
        setSceneText(stripHtml(scene.content || ""));
        return;
      }
    }
  }

  function onSceneChange(text: string) {
    setSceneText(text);
    setSaveState("saving");
    if (saveTimer.current) clearTimeout(saveTimer.current);
    saveTimer.current = setTimeout(async () => {
      if (!user || !activeSceneId) return;
      try {
        await updateSceneContent(sb(), user.id, activeSceneId, toHtml(text));
        setSaveState("saved");
      } catch {
        setSaveState("idle");
      }
    }, 700);
  }

  const modeLabel = MODES.find((m) => m.id === mode)?.label ?? "Write";

  if (!ready || loading) {
    return (
      <Wrapper className="gap-2.5 py-8 flex-1">
        <ActivityIndicator color={colors.accent} />
      </Wrapper>
    );
  }

  if (!novel) {
    return (
      <Wrapper className="gap-2.5 py-8 flex-1">
        <Text className="text-fg">Novel not found.</Text>
        <PrimaryButton label="Back to library" onPress={() => router.push("/tools/twilda")} />
      </Wrapper>
    );
  }

  const panelClassName = "border border-border rounded-sm p-4 gap-2 bg-bg-elevated";

  return (
    <Wrapper className="gap-2.5 py-8 flex-1">
      <PageSeo title={novel.title} description="Twilda workspace" path={`/tools/twilda/novels/${id}`} />
      <ToolsSubnav links={NAV} />
      <StudioBreadcrumb
        items={[
          { label: "Studio", href: "/studio" },
          { label: "Twilda", href: "/tools/twilda" },
          { label: novel.title, href: `/tools/twilda/novels/${id}` },
          { label: modeLabel },
          ...(mode === "write" && activeScene
            ? [{ label: `Chapter ${chapterIndex} · Scene ${sceneIndex}` }]
            : []),
        ]}
      />
      <View className="flex-row flex-wrap items-baseline justify-between gap-2">
        <Text className="font-sans text-[36px] font-bold text-fg">{novel.title}</Text>
        <Text className="text-xs min-h-4 text-muted">
          {saveState === "saving" ? "Saving…" : saveState === "saved" ? "Saved" : " "}
        </Text>
      </View>

      <View className="flex-row flex-wrap border border-border rounded-sm p-0.5 gap-0.5 my-1.5 self-start bg-bg">
        {MODES.map((m) => {
          const active = mode === m.id;
          return (
            <Pressable
              key={m.id}
              onPress={() => setMode(m.id)}
              className={["px-3.5 py-2 rounded-sm", active ? "bg-fg" : "bg-transparent"].join(" ")}
            >
              <Text
                className={[
                  "text-[13px] tracking-wide",
                  active ? "text-inverse font-bold" : "text-muted font-medium",
                ].join(" ")}
              >
                {m.label}
              </Text>
            </Pressable>
          );
        })}
      </View>

      <ScrollView contentContainerStyle={{ gap: 12, paddingBottom: 48 }}>
        {mode === "plan" ? (
          <View className={panelClassName} style={{ gap: 12 }}>
            {novel.chapters.map((ch) => (
              <View key={ch.id} className="border border-border p-3.5 gap-1.5">
                <Text className="font-sans text-lg font-bold text-fg">{ch.title}</Text>
                {ch.scenes.map((sc) => (
                  <Pressable
                    key={sc.id}
                    onPress={() => {
                      setActiveSceneId(sc.id);
                      setSceneText(stripHtml(sc.content || ""));
                      setMode("write");
                    }}
                  >
                    <Text className="text-accent py-1.5">
                      {sc.title || "Scene"} →
                    </Text>
                  </Pressable>
                ))}
                <Pressable onPress={() => createScene(sb(), user!.id, ch.id).then(load)}>
                  <Text className="text-muted">+ Scene</Text>
                </Pressable>
              </View>
            ))}
            <PrimaryButton
              label="Add chapter"
              onPress={() => createChapter(sb(), user!.id, id!).then(load)}
            />
          </View>
        ) : null}

        {mode === "write" ? (
          <View className={panelClassName} style={{ gap: 12, zIndex: 8 }}>
            <View className="flex-row flex-wrap gap-3">
              <View style={{ flex: 1, minWidth: 140, zIndex: 12 }}>
                <StudioSelect
                  label="Chapter"
                  value={activeChapterId}
                  options={chapterOptions}
                  onChange={selectChapter}
                  placeholder="Chapter…"
                />
              </View>
              <View style={{ flex: 1, minWidth: 140, zIndex: 11 }}>
                <StudioSelect
                  label="Scene"
                  value={activeSceneId ?? ""}
                  options={sceneOptions}
                  onChange={selectScene}
                  placeholder="Scene…"
                />
              </View>
            </View>
            <TextInput
              multiline
              value={sceneText}
              onChangeText={onSceneChange}
              placeholder="Write this scene…"
              placeholderTextColorClassName="text-subtle"
              className="border border-border rounded-sm min-h-[200px] p-3.5 font-sans text-base leading-7 text-fg bg-bg"
              style={{ textAlignVertical: "top" }}
            />
          </View>
        ) : null}

        {mode === "board" ? (
          <View className={panelClassName} style={{ gap: 12 }}>
            {panels.map((p) => (
              <View key={p.id} className="border border-border p-3.5 gap-1.5">
                <Text className="font-sans text-lg font-bold text-fg">
                  Panel {p.sort_order + 1}
                </Text>
                <Text className="text-muted">{p.caption || "No caption"}</Text>
                <Text className="text-subtle">{p.prompt || "No prompt"}</Text>
              </View>
            ))}
            <PrimaryButton
              label="Add panel"
              onPress={async () => {
                await createStoryboardPanel(sb(), user!.id, id!, novel.active_draft_id);
                setPanels(await listStoryboardPanels(sb(), user!.id, id!, novel.active_draft_id));
              }}
            />
          </View>
        ) : null}

        {mode === "codex" ? (
          <View className={panelClassName} style={{ gap: 12 }}>
            {novel.codex.map((entry) => (
              <View key={entry.id} className="border border-border p-3.5 gap-1.5">
                <Text className="text-[11px] tracking-[1.2px] uppercase font-bold text-accent">{entry.type}</Text>
                <Text className="font-sans text-lg font-bold text-fg">{entry.name}</Text>
                <Text className="text-muted">{entry.summary}</Text>
              </View>
            ))}
            <PrimaryButton
              label="Add character"
              onPress={() =>
                createCodexEntry(sb(), user!.id, id!, {
                  type: "character",
                  name: "New character",
                  summary: "",
                  description: "",
                }).then(load)
              }
            />
          </View>
        ) : null}

        {mode === "settings" ? (
          <View className={panelClassName} style={{ gap: 12, zIndex: 8 }}>
            {(
              [
                ["Title", title, setTitle],
                ["Author", author, setAuthor],
                ["Series", series, setSeries],
              ] as const
            ).map(([label, value, set]) => (
              <View key={label} style={{ gap: 6 }}>
                <Text className="text-xs tracking-wide uppercase font-bold text-muted">{label}</Text>
                <TextInput
                  value={value}
                  onChangeText={set}
                  className="border border-border rounded-sm min-h-11 px-3 py-2.5 text-base text-fg bg-bg"
                />
              </View>
            ))}
            <StudioSelect
              label="Cover"
              value={coverKind}
              options={COVER_OPTIONS}
              onChange={(v) => setCoverKind(v as CoverKind)}
            />
            <View style={{ gap: 6 }}>
              <Text className="text-xs tracking-wide uppercase font-bold text-muted">Synopsis</Text>
              <TextInput
                multiline
                value={synopsis}
                onChangeText={setSynopsis}
                className="border border-border rounded-sm min-h-[120px] p-3.5 font-sans text-base leading-7 text-fg bg-bg"
                style={{ textAlignVertical: "top" }}
              />
            </View>
            <PrimaryButton
              label="Save settings"
              onPress={async () => {
                await updateNovelMetadata(sb(), user!.id, id!, {
                  title,
                  author,
                  synopsis,
                  series_name: series.trim() || null,
                  cover_kind: coverKind,
                });
                await load();
                Alert.alert("Saved", "Novel settings updated.");
              }}
            />
            <View className="border-t border-border mt-4 pt-4 gap-2">
              <Text className="text-xs tracking-wide uppercase font-bold text-muted">Danger zone</Text>
              <PrimaryButton
                label="Delete novel"
                className="bg-muted"
                onPress={() =>
                  Alert.alert("Delete novel?", "This cannot be undone.", [
                    { text: "Cancel", style: "cancel" },
                    {
                      text: "Delete",
                      style: "destructive",
                      onPress: async () => {
                        await deleteNovel(sb(), user!.id, id!);
                        router.replace("/tools/twilda");
                      },
                    },
                  ])
                }
              />
            </View>
          </View>
        ) : null}
      </ScrollView>
    </Wrapper>
  );
}

