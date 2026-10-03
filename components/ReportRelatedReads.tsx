import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import {
  deckLine,
  getRelatedPosts,
  sectionLabel,
  splitReportHeadline,
  type BlogPost,
} from "@/lib/content";

type Props = {
  slug: string;
  limit?: number;
};

export function ReportRelatedReads({ slug, limit = 4 }: Props) {
  const related = getRelatedPosts(slug, limit);
  if (related.length === 0) return null;

  return (
    <View className="gap-4 border-t border-border pt-4">
      <Text className="font-sans text-[10px] font-semibold uppercase tracking-[2.5px] text-accent">
        Read next
      </Text>
      <View className="gap-5">
        {related.map((post: BlogPost) => {
          const label = sectionLabel(post.tags, post.subject);
          const headline = splitReportHeadline(post.title);
          return (
            <Link key={post.slug} href={`/${post.slug}`} asChild>
              <Pressable className="gap-1">
                {label ? (
                  <Text className="font-sans text-[10px] font-bold uppercase tracking-[1.6px] text-accent">
                    {label}
                  </Text>
                ) : null}
                <Text className="font-serif text-[20px] font-semibold leading-[1.25] tracking-tight text-fg">
                  {headline ? (
                    <Text>
                      <Text className="text-secondary">{headline.slug}</Text>
                      {`: ${headline.subtitle}`}
                    </Text>
                  ) : (
                    post.title
                  )}
                </Text>
                <Text
                  className="font-sans text-[14px] font-bold leading-[22px] text-accent"
                  numberOfLines={2}
                >
                  {deckLine(post.description, 22)}
                </Text>
              </Pressable>
            </Link>
          );
        })}
      </View>
      <Link href="/blog">
        <Text className="font-sans text-[11px] uppercase tracking-[1.4px] text-muted">
          All reports →
        </Text>
      </Link>
    </View>
  );
}
