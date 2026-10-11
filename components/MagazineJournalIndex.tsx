import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { BlogCard } from "@/components/BlogCard";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import { assetUrl } from "@/lib/assets";
import {
  deckLine,
  formatDate,
  sectionLabel,
  type BlogPost,
} from "@/lib/content";

function JournalLead({ post }: { post: BlogPost }) {
  const label = sectionLabel(post.tags, post.subject);
  const hero = assetUrl(post.heroImage);
  return (
    <View className="gap-6 border-b-2 border-fg pb-8">
      {label ? (
        <Text className="font-mono text-[11px] font-medium uppercase tracking-[0.14em] text-secondary">
          {label}
        </Text>
      ) : null}
      <View className="flex-col gap-5 md:flex-row md:items-stretch">
        <Link href={`/${post.slug}`} asChild>
          <Pressable
            accessibilityRole="link"
            className="min-w-0 md:w-[58%] md:flex-[3]"
          >
            {hero ? (
              <SiteCoverImage
                source={{ uri: hero }}
                wrapperClassName="w-full"
                wrapperStyle={{ aspectRatio: 16 / 10 }}
                transition={200}
                accessibilityLabel={post.title}
              />
            ) : (
              <View className="aspect-[16/10] w-full bg-bg-elevated" />
            )}
          </Pressable>
        </Link>
        <View className="min-w-0 justify-end gap-2 md:w-[42%] md:flex-[2]">
          <Text className="font-mono text-[11px] uppercase tracking-[0.12em] text-muted">
            {post.pubDate ? formatDate(post.pubDate) : ""}
          </Text>
          <Link href={`/${post.slug}`} asChild>
            <Pressable accessibilityRole="link">
              <Text className="font-sans text-[clamp(1.6rem,3vw,2.35rem)] font-bold leading-[1.08] tracking-[-0.02em] text-fg">
                {post.title}
              </Text>
            </Pressable>
          </Link>
          <Text className="font-sans text-[16px] leading-[1.45] text-muted">
            {deckLine(post.description, 28)}
          </Text>
        </View>
      </View>
    </View>
  );
}

export function MagazineJournalIndex({
  title,
  description,
  posts,
}: {
  title: string;
  description?: string;
  posts: BlogPost[];
}) {
  const [lead, ...rest] = posts;
  const grid = rest.slice(0, 9);
  const briefs = rest.slice(9);

  return (
    <View className="gap-8">
      <View className="gap-2 border-b-2 border-fg pb-6">
        <Text className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-accent">
          Reports
        </Text>
        <Text className="font-sans text-[clamp(2rem,4vw,2.75rem)] font-bold leading-[1.05] tracking-[-0.02em] text-fg">
          {title}
        </Text>
        {description ? (
          <Text className="max-w-[68ch] font-sans text-[17px] leading-[1.5] text-muted">
            {description}
          </Text>
        ) : null}
      </View>

      {lead ? <JournalLead post={lead} /> : null}

      {grid.length > 0 ? (
        <View className="gap-4 border-t-2 border-fg pt-8">
          <Text className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-muted">
            In this section
          </Text>
          <View className="flex-row flex-wrap gap-4">
            {grid.map((post) => (
              <View
                key={post.slug}
                className="min-w-[140px] flex-1 basis-[45%] md:basis-[30%]"
              >
                <BlogCard post={post} variant="stack" editorial />
              </View>
            ))}
          </View>
        </View>
      ) : null}

      {briefs.length > 0 ? (
        <View className="gap-3 border-t-2 border-fg pt-8">
          <Text className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-muted">
            More investigations
          </Text>
          {briefs.map((post) => (
            <BlogCard key={post.slug} post={post} variant="pick" editorial />
          ))}
        </View>
      ) : null}
    </View>
  );
}
