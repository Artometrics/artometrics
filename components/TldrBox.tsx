import { Text, View } from "react-native";

export function TldrBox({
  tldr,
  keyPoints,
}: {
  tldr?: string | null;
  keyPoints?: string[] | null;
}) {
  const points = (keyPoints ?? []).filter(Boolean);
  if (!tldr && !points.length) return null;

  return (
    <View className="art-floating-box gap-3 px-5 py-6 my-4">
      <Text className="font-display text-[14px] uppercase tracking-[2px] text-accent">
        TL;DR
      </Text>
      {tldr ? (
        <Text className="font-sans text-[15px] leading-6 text-white">{tldr}</Text>
      ) : null}
      {points.length ? (
        <View className="mt-1 gap-3 border-t-2 border-white/20 pt-4">
          {points.map((point) => (
            <View key={point} className="flex-row items-start gap-3">
              <View className="mt-2 h-2 w-2 bg-accent" />
              <Text className="flex-1 font-mono text-[13px] leading-5 text-white/85">
                {point}
              </Text>
            </View>
          ))}
        </View>
      ) : null}
    </View>
  );
}
