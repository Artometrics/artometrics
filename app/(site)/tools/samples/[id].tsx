import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Alert,
  Platform,
  Pressable,
  Text,
  TextInput,
  View,
} from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import {
  RecordingPresets,
  setAudioModeAsync,
  useAudioPlayer,
  useAudioRecorder,
  useAudioRecorderState,
  requestRecordingPermissionsAsync,
} from "expo-audio";
import * as Clipboard from "expo-clipboard";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { PrimaryButton } from "@/components/PrimaryButton";
import { useTheme } from "@/lib/theme";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import { paramString } from "@/lib/params";
import {
  getSamplePack,
  packToExportJson,
  saveSamplePack,
} from "@/lib/samples/storage";
import {
  DEFAULT_SYNTH,
  applyPreset,
  newClipId,
  type SampleClip,
  type SamplePack,
  type SynthSettings,
} from "@/lib/samples/types";

const NAV = [
  { href: "/tools/samples", label: "Packs" },
  { href: "/tools/samples/record", label: "Record" },
];

export default function SamplePackScreen() {
  const params = useLocalSearchParams<{ id: string | string[] }>();
  const id = paramString(params.id);
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const [pack, setPack] = useState<SamplePack | null>(null);
  const [busy, setBusy] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  const recorderState = useAudioRecorderState(recorder, 200);
  const player = useAudioPlayer(pack?.sourceUri ?? null);

  useEffect(() => {
    void setAudioModeAsync({
      playsInSilentMode: true,
      allowsRecording: true,
    });
  }, []);

  const load = useCallback(async () => {
    if (!user || !id) return;
    const existing = await getSamplePack(user.id, id);
    if (existing) {
      setPack(existing);
      return;
    }
    // Soft-create if opened via stale link
    const now = new Date().toISOString();
    const created: SamplePack = {
      id,
      userId: user.id,
      title: "Untitled pack",
      sourceUri: null,
      durationSec: 0,
      synth: { ...DEFAULT_SYNTH },
      clips: [],
      createdAt: now,
      updatedAt: now,
    };
    await saveSamplePack(created);
    setPack(created);
  }, [user, id]);

  useEffect(() => {
    if (ready && user) void load();
  }, [ready, user, load]);

  const synth = pack?.synth ?? DEFAULT_SYNTH;

  async function persist(next: SamplePack) {
    setPack(next);
    await saveSamplePack(next);
  }

  async function startRec() {
    setStatusMsg(null);
    const perm = await requestRecordingPermissionsAsync();
    if (!perm.granted) {
      Alert.alert("Microphone needed", "Allow microphone access to record samples.");
      return;
    }
    try {
      setBusy(true);
      await recorder.prepareToRecordAsync();
      recorder.record();
      setStatusMsg("Recording…");
    } catch (e) {
      Alert.alert("Record error", e instanceof Error ? e.message : "Failed to start");
    } finally {
      setBusy(false);
    }
  }

  async function stopRec() {
    if (!pack || !user) return;
    try {
      setBusy(true);
      await recorder.stop();
      const uri = recorder.uri;
      const duration = recorderState.durationMillis
        ? recorderState.durationMillis / 1000
        : 0;
      if (!uri) {
        setStatusMsg("No recording captured.");
        return;
      }
      await persist({
        ...pack,
        sourceUri: uri,
        durationSec: duration,
      });
      try {
        player.replace(uri);
      } catch {
        /* soft */
      }
      setStatusMsg("Recording saved. Adjust synth, then mark favorite clips.");
    } catch (e) {
      Alert.alert("Stop error", e instanceof Error ? e.message : "Failed to stop");
    } finally {
      setBusy(false);
    }
  }

  function setSynth(patch: Partial<SynthSettings>) {
    if (!pack) return;
    void persist({ ...pack, synth: { ...pack.synth, ...patch } });
  }

  function usePreset(preset: SynthSettings["preset"]) {
    if (!pack) return;
    void persist({ ...pack, synth: applyPreset(preset) });
  }

  function addClipFromSource(favorite = true) {
    if (!pack?.sourceUri) {
      Alert.alert("Record first", "Capture audio before creating a clip.");
      return;
    }
    const end = Math.max(0.5, pack.durationSec || 3);
    const clip: SampleClip = {
      id: newClipId(),
      label: `Clip ${pack.clips.length + 1}`,
      uri: pack.sourceUri,
      startSec: 0,
      endSec: end,
      favorite,
      createdAt: new Date().toISOString(),
    };
    void persist({ ...pack, clips: [...pack.clips, clip] });
  }

  function toggleFavorite(clipId: string) {
    if (!pack) return;
    void persist({
      ...pack,
      clips: pack.clips.map((c) =>
        c.id === clipId ? { ...c, favorite: !c.favorite } : c,
      ),
    });
  }

  async function exportPack() {
    if (!pack) return;
    const json = packToExportJson(pack);
    await Clipboard.setStringAsync(json);
    if (Platform.OS === "web" && typeof document !== "undefined") {
      const blob = new Blob([json], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${pack.title.replace(/\s+/g, "-").toLowerCase()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }
    setStatusMsg("Exported favorites JSON.");
  }

  const recording = recorderState.isRecording;
  const presets = useMemo(
    () => ["clean", "lofi", "bright", "warm"] as SynthSettings["preset"][],
    [],
  );

  if (!ready || !user || !pack) {
    return (
      <Wrapper variant="narrow" className="gap-2.5 py-8 flex-1">
        <Text className="text-muted">Loading pack…</Text>
      </Wrapper>
    );
  }

  return (
    <Wrapper className="gap-2.5 py-8 flex-1">
      <PageSeo
        title={pack.title}
        description="Shape your recording with synth settings and save favorite clips."
        path={`/tools/samples/${pack.id}`}
      />
      <ToolsSubnav links={NAV} />
      <TextInput
        value={pack.title}
        onChangeText={(title) => void persist({ ...pack, title })}
        className="text-[28px] font-bold border-b border-border py-1.5 text-fg"
      />
      <Text className="font-sans text-base leading-[26px] max-w-[560px] text-muted">
        Record → synth → favorite clips → export.
      </Text>

      <View className="border border-border p-4 gap-3">
        <Text className="text-[11px] tracking-[1.4px] uppercase font-bold text-muted">Transport</Text>
        <View className="flex-row flex-wrap gap-2.5 items-center">
          <PrimaryButton
            label={recording ? "Recording…" : "Record"}
            onPress={() => void startRec()}
            disabled={busy || recording}
            className={recording ? "" : "bg-fg"}
          />
          <PrimaryButton
            label="Stop"
            onPress={() => void stopRec()}
            disabled={!recording}
            className="bg-muted"
          />
          <PrimaryButton
            label={player.playing ? "Pause" : "Play"}
            onPress={() => {
              if (!pack.sourceUri) return;
              if (player.playing) player.pause();
              else {
                try {
                  player.playbackRate = synth.pitch;
                  player.volume = synth.gain;
                } catch {
                  /* soft */
                }
                player.play();
              }
            }}
            disabled={!pack.sourceUri}
          />
        </View>
        {statusMsg ? <Text className="text-[13px] text-accent">{statusMsg}</Text> : null}
        {pack.sourceUri ? (
          <Text className="text-[13px] text-subtle" numberOfLines={1}>
            Source ready · ~{pack.durationSec.toFixed(1)}s
          </Text>
        ) : null}
      </View>

      <View className="border border-border p-4 gap-3">
        <Text className="text-[11px] tracking-[1.4px] uppercase font-bold text-muted">Synth</Text>
        <View className="flex-row flex-wrap gap-2">
          {presets.map((p) => (
            <Pressable
              key={p}
              onPress={() => usePreset(p)}
              className={[
                "border border-border px-3 py-2",
                synth.preset === p ? "bg-fg border-fg" : "bg-bg-elevated border-border",
              ].join(" ")}
            >
              <Text
                className={[
                  "text-[13px] font-semibold capitalize",
                  synth.preset === p ? "text-inverse" : "text-fg",
                ].join(" ")}
              >
                {p}
              </Text>
            </Pressable>
          ))}
        </View>
        <SliderRow
          label={`Pitch ${synth.pitch.toFixed(2)}`}
          value={synth.pitch}
          min={0.5}
          max={2}
          onChange={(pitch) => setSynth({ pitch, preset: "clean" })}
          colors={colors}
        />
        <SliderRow
          label={`Gain ${synth.gain.toFixed(2)}`}
          value={synth.gain}
          min={0}
          max={1}
          onChange={(gain) => setSynth({ gain })}
          colors={colors}
        />
        <SliderRow
          label={`Filter ${Math.round(synth.filterHz)} Hz`}
          value={synth.filterHz}
          min={200}
          max={12000}
          onChange={(filterHz) => setSynth({ filterHz })}
          colors={colors}
        />
        <SliderRow
          label={`Drive ${synth.drive.toFixed(2)}`}
          value={synth.drive}
          min={0}
          max={1}
          onChange={(drive) => setSynth({ drive })}
          colors={colors}
        />
      </View>

      <View className="border border-border p-4 gap-3">
        <Text className="text-[11px] tracking-[1.4px] uppercase font-bold text-muted">Clips</Text>
        <PrimaryButton label="Add clip from recording" onPress={() => addClipFromSource(true)} />
        {pack.clips.length === 0 ? (
          <Text className="text-[13px] text-subtle">
            No clips yet. Add favorites to build your sample pack.
          </Text>
        ) : (
          pack.clips.map((clip) => (
            <Pressable
              key={clip.id}
              onPress={() => toggleFavorite(clip.id)}
              className="flex-row items-center gap-3 border border-border p-3"
            >
              <View className="flex-1">
                <Text className="text-fg font-semibold">{clip.label}</Text>
                <Text className="text-[13px] text-subtle">
                  {clip.startSec.toFixed(1)}s – {clip.endSec.toFixed(1)}s
                </Text>
              </View>
              <Text className={clip.favorite ? "text-accent" : "text-muted"}>
                {clip.favorite ? "★ Favorite" : "☆"}
              </Text>
            </Pressable>
          ))
        )}
      </View>

      <View className="flex-row flex-wrap gap-2.5 items-center">
        <PrimaryButton label="Export favorites" onPress={() => void exportPack()} />
        <Pressable onPress={() => router.push("/tools/samples")}>
          <Text className="text-accent font-bold">All packs →</Text>
        </Pressable>
      </View>
    </Wrapper>
  );
}

function SliderRow({
  label,
  value,
  min,
  max,
  onChange,
  colors,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  onChange: (v: number) => void;
  colors: { text: string; textMuted: string; border: string; accent: string };
}) {
  // Simple stepper buttons — no extra slider dependency
  const step = (max - min) / 20;
  return (
    <View className="flex-row items-center gap-2">
      <Text className="text-muted text-[13px] flex-1">{label}</Text>
      <Pressable
        onPress={() => onChange(Math.max(min, value - step))}
        className="w-9 h-9 items-center justify-center border border-border"
      >
        <Text className="text-fg">−</Text>
      </Pressable>
      <Pressable
        onPress={() => onChange(Math.min(max, value + step))}
        className="w-9 h-9 items-center justify-center border border-border"
      >
        <Text className="text-fg">+</Text>
      </Pressable>
    </View>
  );
}

export async function generateStaticParams() {
  return [{ id: "demo" }];
}

