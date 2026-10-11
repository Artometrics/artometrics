import { Text, View, Pressable } from "react-native";
import { Link } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { SECTION_META, SECTION_SLUGS } from "@/data/sections";

export default function TopicsIndex() {
  return (
    <Wrapper variant="wide" className="gap-0 py-8 md:py-10">
      <PageSeo
        title="Sections"
        description="Browse Artometrics by section — sports, movies & TV, music, culture, and more."
        path="/topics"
      />
      <View className="gap-2 border-b-2 border-fg pb-6">
        <Text className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-accent">
          Desk fronts
        </Text>
        <Text className="font-sans text-[clamp(2rem,4vw,2.75rem)] font-bold leading-[1.05] tracking-[-0.02em] text-fg">
          Sections
        </Text>
        <Text className="max-w-[68ch] font-sans text-[17px] leading-[1.5] text-muted">
          Weekly investigation fronts by desk — the same grammar as the home page, sorted by beat.
        </Text>
      </View>
      <View className="mt-2 border-t-2 border-fg">
        {SECTION_SLUGS.map((slug) => (
          <Link key={slug} href={`/topics/${slug}` as `/topics/${string}`} asChild>
            <Pressable className="gap-1 border-b border-border py-5">
              <Text className="font-mono text-[10px] font-medium uppercase tracking-[0.14em] text-secondary">
                {slug}
              </Text>
              <Text className="font-sans text-2xl font-bold leading-tight text-fg">
                {SECTION_META[slug].title}
              </Text>
              <Text className="font-sans text-[15px] leading-[22px] text-muted">
                {SECTION_META[slug].description}
              </Text>
            </Pressable>
          </Link>
        ))}
      </View>
    </Wrapper>
  );
}
