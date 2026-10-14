import { ImageBackground } from "expo-image";
import { Pressable, Text, View } from "react-native";
import type { CoverKind } from "@/lib/twilda/novelcrafter/data";
import { Colors } from "@/constants/Colors";
import { assetUrl } from "@/lib/assets";

const COVER_LABEL: Record<CoverKind, string> = {
  gatsby: "Gatsby",
  trinity: "Trinity",
  cardinal: "Cardinal",
  apocrypha: "Apocrypha",
  artometrics: "Artometrics",
  psychonomics: "Psychonomics",
  plain: "Novel",
};

const COVER_BG: Record<CoverKind, string> = {
  gatsby: Colors.accent800,
  trinity: "#1e3a5f",
  cardinal: "#3d2b1f",
  apocrypha: "#2c1810",
  artometrics: "#E60000",
  psychonomics: "#1a1a1a",
  plain: "#2a2a2a",
};

/** Optional full-bleed jacket art for flagship manuscripts. */
const COVER_ART: Partial<Record<CoverKind, string>> = {
  artometrics: "/images/books/artometrics-culture-quantified.jpg",
  psychonomics: "/images/books/psychonomics-leader-profiles.jpg",
};

export function CoverTile({
  title,
  author,
  coverKind,
  updated,
  onPress,
}: {
  title: string;
  author?: string;
  coverKind: CoverKind;
  updated?: string;
  onPress: () => void;
}) {
  const art = COVER_ART[coverKind];
  const coverInner = (
    <>
      <Text className="mb-1.5 text-[11px] uppercase tracking-[1px] text-white/85">
        {COVER_LABEL[coverKind] ?? "Novel"}
      </Text>
      <Text className="font-serif text-lg font-bold leading-[22px] text-white" numberOfLines={3}>
        {title}
      </Text>
    </>
  );

  return (
    <Pressable onPress={onPress} className="mb-5 w-[47%] active:opacity-90">
      {art ? (
        <ImageBackground
          source={{ uri: assetUrl(art) }}
          className="aspect-[2/3] justify-end overflow-hidden p-3.5"
          contentFit="cover"
          transition={200}
        >
          <View className="-m-3.5 flex-1 justify-end bg-black/35 p-3.5">{coverInner}</View>
        </ImageBackground>
      ) : (
        <View
          className="aspect-[2/3] justify-end overflow-hidden p-3.5"
          style={{ backgroundColor: COVER_BG[coverKind] ?? COVER_BG.plain }}
        >
          {coverInner}
        </View>
      )}
      <View className="mt-2.5 gap-0.5">
        <Text className="font-serif text-[15px] text-fg" numberOfLines={2}>
          {title}
        </Text>
        {author ? (
          <Text className="text-[13px] text-muted" numberOfLines={1}>
            {author}
          </Text>
        ) : null}
        {updated ? (
          <Text className="text-[13px] text-subtle">{updated}</Text>
        ) : null}
      </View>
    </Pressable>
  );
}
