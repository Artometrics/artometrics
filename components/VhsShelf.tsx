import { Platform, Pressable, Text, View, ScrollView } from "react-native";
import { Image } from "expo-image";
import { Link } from "expo-router";
import { assetUrl } from "@/lib/assets";
import type { EditionManifest } from "@/data/editions";
import { SECTION_META } from "@/data/sections";

const SPINE_PALETTE = ["#E60000", "#000000", "#FFFFFF", "#000000"] as const;

function spineColors(i: number) {
  const bg = SPINE_PALETTE[i % SPINE_PALETTE.length];
  const fg = bg === "#FFFFFF" ? "#000000" : "#FFFFFF";
  return { bg, fg };
}

/**
 * VHS box + spine shelf for editions / media archive.
 * Matches Artometrics Media & Books design reference.
 */
export function VhsShelf({ editions }: { editions: EditionManifest[] }) {
  const featured = editions.slice(0, 3);
  const spines = editions;

  return (
    <View className="w-full bg-[#0d0d0d] px-5 py-12 md:px-12">
      <View className="mb-11 flex-row flex-wrap items-baseline justify-between gap-3">
        <Text
          className="text-[34px] text-white"
          style={{ fontFamily: "Chomsky" }}
        >
          Artometrics Media
        </Text>
        <Text className="font-mono text-[13px] uppercase tracking-[0.06em] text-[#6E95FF]">
          The Archive — Vol. 01–{String(editions.length).padStart(2, "0")}
        </Text>
      </View>

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        className="mb-14"
        contentContainerStyle={{ gap: 20, paddingRight: 16 }}
      >
        {featured.map((ed, i) => {
          const hero = assetUrl(ed.heroImage);
          return (
            <Link key={ed.id} href={`/editions/${ed.id}`} asChild>
              <Pressable
                accessibilityRole="link"
                accessibilityLabel={ed.title}
                className="w-[220px] flex-none border-8 border-[#1a1a1a] bg-[#111] md:w-[260px]"
              >
                <View className="relative aspect-[3/4] overflow-hidden">
                  {hero ? (
                    <Image
                      source={{ uri: hero }}
                      alt=""
                      accessibilityIgnoresInvertColors
                      className="absolute inset-0 h-full w-full"
                      contentFit="cover"
                      transition={200}
                    />
                  ) : (
                    <View className="absolute inset-0 bg-base-800" />
                  )}
                  <View
                    className="absolute right-2.5 top-2.5 bg-accent px-2 py-1"
                    style={{ transform: [{ rotate: i % 2 ? "-3deg" : "4deg" }] }}
                  >
                    <Text className="font-mono text-[12px] font-bold text-white">
                      VOL. {String(i + 1).padStart(2, "0")}
                    </Text>
                  </View>
                  <View className="absolute bottom-0 left-0 right-0 bg-black px-3 py-2.5">
                    <Text
                      className="font-mono text-[16px] font-bold uppercase leading-[1.1] text-white"
                      numberOfLines={2}
                    >
                      {ed.title}
                    </Text>
                    <Text className="mt-1 font-mono text-[10px] text-[#a3a3a3]">
                      SP · {ed.articleSlugs.length} REPORTS · HI-FI
                    </Text>
                  </View>
                </View>
              </Pressable>
            </Link>
          );
        })}
      </ScrollView>

      <Text className="border-b border-[#262626] pb-3 font-mono text-[12px] uppercase tracking-[0.06em] text-[#A3A3A3]">
        Full collection
      </Text>

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        className="border border-t-0 border-[#262626] bg-[#161616]"
        contentContainerStyle={{ gap: 6, paddingHorizontal: 20, paddingVertical: 24 }}
      >
        {spines.map((ed, i) => {
          const { bg, fg } = spineColors(i);
          const label = `VOL. ${String(i + 1).padStart(2, "0")} — ${ed.title.toUpperCase()}`;
          return (
            <Link key={ed.id} href={`/editions/${ed.id}`} asChild>
              <Pressable
                accessibilityRole="link"
                accessibilityLabel={ed.title}
                className="h-[300px] w-14 flex-none items-center justify-center border-l-2 border-[#333] md:h-[340px]"
                style={{ backgroundColor: bg }}
              >
                <Text
                  className="font-mono text-[13px] font-bold tracking-[0.04em] md:text-[15px]"
                  style={{
                    color: fg,
                    ...(Platform.OS === "web"
                      ? ({
                          writingMode: "vertical-rl",
                          transform: "rotate(180deg)",
                        } as object)
                      : {
                          width: 20,
                          textAlign: "center",
                        }),
                  }}
                  numberOfLines={Platform.OS === "web" ? 1 : 12}
                >
                  {label}
                </Text>
              </Pressable>
            </Link>
          );
        })}
      </ScrollView>

      <Text className="mt-8 font-mono text-[11px] text-[#525252]">
        Play · Rewind · Artometrics Media Archive
        {editions[0]
          ? ` · ${SECTION_META[editions[0].section]?.title ?? "Editions"}`
          : ""}
      </Text>
    </View>
  );
}
