import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import { assetUrl } from "@/lib/assets";
import {
  cardDeckLine,
  formatAuthorName,
  formatDate,
  sectionLabel,
  type BlogPost,
} from "@/lib/content";

export function BlogCard({
  post,
  variant = "row",
  editorial = false,
}: {
  post: BlogPost;
  variant?: "stack" | "row" | "cover" | "pick";
  /** Normal-case serif-style headlines (homepage FT grid). */
  editorial?: boolean;
}) {
  const label = sectionLabel(post.tags, post.subject);
  const hero = assetUrl(post.heroImage);
  const author = post.author
    ? formatAuthorName(String(post.author))
    : "Kyle McAuliffe";

  const titleClass =
    "font-display text-[22px] leading-[1.05] text-fg md:text-[26px]";

  if (variant === "pick") {
    return (
      <Link href={`/${post.slug}`} asChild>
        <Pressable
          accessibilityRole="link"
          accessibilityLabel={post.title}
          className="house-card mt-3 flex-row items-start gap-4 p-3"
          style={{
            backgroundColor: "#07070a",
            borderWidth: 1,
            borderColor: "#f4efe4",
            boxShadow: "4px 4px 0 #ff3d8a",
          }}
        >
          <View className="min-w-0 flex-1 gap-1.5">
            <Text className="house-card__issue" style={{ fontFamily: "DM Mono", color: "#b7d0cb" }}>
              {post.pubDate ? formatDate(post.pubDate) : label}
            </Text>
            <Text
              className="font-display text-[22px] leading-[1.02]"
              style={{ fontFamily: "Anton", color: "#f4efe4" }}
              numberOfLines={3}
            >
              {post.title}
            </Text>
            {label ? (
              <Text className="font-mono text-[10px] uppercase tracking-[1.4px]" style={{ color: "#8fb8b2" }}>
                {label}
              </Text>
            ) : null}
          </View>
          {hero ? (
            <SiteCoverImage
              source={{ uri: hero }}
              wrapperClassName="h-[72px] w-[72px] shrink-0 border border-border bg-border"
              transition={0}
              accessibilityLabel=""
            />
          ) : (
            <View
              accessibilityElementsHidden
              className="h-[72px] w-[72px] shrink-0 items-center justify-center bg-fg"
            >
              <Text className="font-mono text-[18px] font-bold text-[#E60000]">
                {(label || post.title).charAt(0).toUpperCase()}
              </Text>
            </View>
          )}
        </Pressable>
      </Link>
    );
  }

  if (variant === "cover") {
    return (
      <Link href={`/${post.slug}`} asChild>
        <Pressable className="relative min-h-[420px] w-full overflow-hidden border border-border bg-black">
          {hero ? (
            <SiteCoverImage
              source={{ uri: hero }}
              wrapperClassName="absolute inset-0"
              transition={200}
            />
          ) : null}
          <View className="absolute inset-0 bg-black/50" />
          <View className="absolute inset-0 justify-end gap-2 p-6">
            {label ? (
              <Text className="font-sans text-[11px] font-semibold uppercase tracking-[2px] text-accent">
                {label}
              </Text>
            ) : null}
            <Text
              className="font-display text-3xl leading-[0.95] text-white md:text-4xl"
              style={{ fontFamily: "Anton" }}
            >
              {post.title}
            </Text>
            <Text className="font-sans text-[12px] uppercase tracking-[1.4px] text-white/70">
              {author} · {formatDate(post.pubDate)}
            </Text>
          </View>
        </Pressable>
      </Link>
    );
  }

  if (variant === "stack") {
    const borderClass = "border border-border";
    const stackTitle =
      "font-display text-[22px] leading-[1.05] text-fg";
    return (
      <Link href={`/${post.slug}`} asChild>
        <Pressable className={`min-w-[140px] flex-1 gap-0 overflow-hidden ${borderClass} bg-header`}>
          {hero ? (
            <SiteCoverImage
              source={{ uri: hero }}
              wrapperClassName="w-full"
              wrapperStyle={{ aspectRatio: 1 }}
              transition={200}
              accessibilityLabel={post.title}
            />
          ) : (
            <View className="w-full overflow-hidden bg-border" style={{ aspectRatio: 1 }} />
          )}
          <View className="gap-2 p-4">
            {label ? (
              <Text className="font-sans text-[10px] font-semibold uppercase tracking-[1.8px] text-accent">
                {label}
              </Text>
            ) : null}
            <Text className={stackTitle} numberOfLines={4}>
              {post.title}
            </Text>
            <Text
              className="font-sans text-[13px] leading-[19px] text-muted"
              numberOfLines={2}
            >
              {cardDeckLine(post.description)}
            </Text>
          </View>
        </Pressable>
      </Link>
    );
  }

  return (
    <Link href={`/${post.slug}`} asChild>
      <Pressable className="flex-row items-stretch gap-0 border-b border-border">
        <View className="flex-1 justify-center gap-1.5 py-5 pr-4">
          {label ? (
            <Text className="font-sans text-[10px] font-semibold uppercase tracking-[1.8px] text-accent">
              {label}
            </Text>
          ) : null}
          <Text className="font-display text-[28px] leading-[1.02] text-fg" style={{ fontFamily: "Anton" }}>
            {post.title}
          </Text>
          <Text
            className="font-sans text-[14px] leading-[22px] text-muted"
            numberOfLines={2}
          >
            {cardDeckLine(post.description)}
          </Text>
          <Text className="mt-1 font-sans text-[11px] uppercase tracking-[1.4px] text-subtle">
            {formatDate(post.pubDate)}
          </Text>
        </View>
        {hero ? (
          <SiteCoverImage
            source={{ uri: hero }}
            wrapperClassName="h-[120px] w-[100px] shrink-0 border border-border"
            transition={200}
            accessibilityLabel={post.title}
          />
        ) : (
          <View className="h-[120px] w-[100px] bg-border" />
        )}
      </Pressable>
    </Link>
  );
}
