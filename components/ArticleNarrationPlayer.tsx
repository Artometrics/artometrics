import { useEffect, useState } from "react";
import { Pressable, Text, View } from "react-native";
import {
  setAudioModeAsync,
  useAudioPlayer,
  useAudioPlayerStatus,
} from "expo-audio";
import { assetUrl } from "@/lib/assets";

const RATES = [0.75, 1, 1.25, 1.5, 2] as const;

type Props = {
  audioSrc: string | null | undefined;
  title?: string;
  /** Known file length in seconds, shown before the player reports duration. */
  runtimeSeconds?: number;
};

function formatTime(seconds: number) {
  if (!Number.isFinite(seconds) || seconds < 0) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export function ArticleNarrationPlayer({ audioSrc, title, runtimeSeconds }: Props) {
  const uri = assetUrl(audioSrc);
  const player = useAudioPlayer(uri);
  const status = useAudioPlayerStatus(player);
  const [rate, setRate] = useState<(typeof RATES)[number]>(1);
  const [trackWidth, setTrackWidth] = useState(0);

  useEffect(() => {
    if (!uri) return;
    try {
      player.shouldCorrectPitch = true;
      player.setPlaybackRate(rate);
    } catch {
      try {
        player.playbackRate = rate;
      } catch {
        /* soft */
      }
    }
  }, [rate, uri, player]);

  if (!uri) return null;

  const duration = status.duration || runtimeSeconds || 0;
  const current = status.currentTime || 0;
  const progress = duration > 0 ? Math.min(1, current / duration) : 0;

  async function toggle() {
    if (status.playing) {
      try {
        player.pause();
      } catch {
        /* ignore */
      }
      return;
    }
    try {
      await setAudioModeAsync({
        playsInSilentMode: true,
        shouldPlayInBackground: false,
      });
    } catch {
      /* best-effort */
    }
    try {
      player.shouldCorrectPitch = true;
      player.setPlaybackRate(rate);
    } catch {
      try {
        player.playbackRate = rate;
      } catch {
        /* soft */
      }
    }
    try {
      player.play();
    } catch {
      /* not loaded yet */
    }
  }

  function seekToRatio(ratio: number) {
    if (!duration) return;
    const next = Math.max(0, Math.min(duration, ratio * duration));
    void player.seekTo(next);
  }

  return (
    <View
      className="mt-1 gap-3 border-2 border-border bg-black p-4"
      accessibilityLabel={title ? `Listen to ${title}` : "Listen to narration"}
    >
      <View className="flex-row flex-wrap items-center gap-3">
        <Pressable
          onPress={() => void toggle()}
          className="min-w-[100px] items-center bg-accent px-5 py-3"
          accessibilityRole="button"
          accessibilityLabel={status.playing ? "Pause narration" : "Play narration"}
        >
          <Text className="font-display text-[13px] uppercase tracking-[2px] text-white">
            {status.playing ? "Pause" : "Listen"}
          </Text>
        </Pressable>
        <View className="min-w-[100px] grow gap-0.5">
          <Text className="font-display text-[11px] uppercase tracking-[2px] text-accent">
            Narration
          </Text>
          <Text className="font-mono text-xs leading-4 text-white/70">
            {formatTime(current)} / {formatTime(duration)}
          </Text>
        </View>
        <View className="flex-row flex-wrap gap-1.5">
          {RATES.map((r) => {
            const active = rate === r;
            return (
              <Pressable
                key={r}
                onPress={() => setRate(r)}
                className={[
                  "min-w-10 items-center border-2 px-2 py-1.5",
                  active ? "border-white bg-white" : "border-white/30 bg-transparent",
                ].join(" ")}
                accessibilityRole="button"
                accessibilityLabel={`${r} times speed`}
                accessibilityState={{ selected: active }}
              >
                <Text
                  className={[
                    "font-mono text-xs font-bold",
                    active ? "text-black" : "text-white",
                  ].join(" ")}
                >
                  {r === 1 ? "1×" : `${r}×`}
                </Text>
              </Pressable>
            );
          })}
        </View>
      </View>

      <Pressable
        className="h-2 w-full overflow-hidden bg-white/20"
        onLayout={(e) => setTrackWidth(e.nativeEvent.layout.width)}
        onPress={(e) => {
          if (!trackWidth) return;
          seekToRatio(e.nativeEvent.locationX / trackWidth);
        }}
        accessibilityRole="adjustable"
        accessibilityLabel="Seek narration"
      >
        <View
          className="h-full bg-accent"
          style={{ width: `${progress * 100}%` }}
        />
      </Pressable>
    </View>
  );
}
