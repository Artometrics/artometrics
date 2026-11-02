import { ReactNode } from "react";
import { ScrollView, View, Text, Pressable, Platform } from "react-native";
import { Link } from "expo-router";
import { Wrapper } from "@/components/Wrapper";

export function CarouselRail({
  title,
  href,
  children,
  itemGap = 16,
}: {
  title: string;
  href?: string;
  children: ReactNode;
  itemGap?: number;
}) {
  return (
    <View className="mb-9">
      <Wrapper
        variant="magazine"
        className="flex-row items-baseline justify-between mb-3.5 gap-3"
      >
        <Text className="font-display text-[28px] tracking-[0.5px] uppercase text-fg">
          {title}
        </Text>
        {href ? (
          <Link href={href as `/topics/${string}`} asChild>
            <Pressable hitSlop={8}>
              <Text className="text-xs font-bold tracking-[0.6px] uppercase text-muted">
                View all
              </Text>
            </Pressable>
          </Link>
        ) : null}
      </Wrapper>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        nestedScrollEnabled
        decelerationRate="fast"
        contentContainerStyle={[
          {
            flexDirection: "row",
            alignItems: "stretch",
            paddingBottom: 4,
            gap: itemGap,
            paddingHorizontal: 20,
          },
          Platform.OS === "web" ? ({ scrollSnapType: "x mandatory" } as object) : null,
        ]}
        className="site-hscroll w-full"
      >
        {children}
      </ScrollView>
    </View>
  );
}
