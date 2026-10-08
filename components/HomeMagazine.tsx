import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { BlogCard } from "@/components/BlogCard";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import { assetUrl } from "@/lib/assets";
import {
  deckLine,
  getBlogPosts,
  sectionLabel,
  type BlogPost,
} from "@/lib/content";

function HomeHeroImage({ post }: { post: BlogPost }) {
  const hero = assetUrl(post.heroImage);
  if (!hero) {
    return (
      <View
        className="w-full overflow-hidden bg-border"
        style={{ aspectRatio: 16 / 10 }}
      />
    );
  }
  return (
    <SiteCoverImage
      source={{ uri: hero }}
      wrapperClassName="w-full"
      wrapperStyle={{ aspectRatio: 16 / 10 }}
      transition={250}
      accessibilityLabel={post.title}
    />
  );
}

function HomeMainStory({ post }: { post: BlogPost }) {
  const label = sectionLabel(post.tags, post.subject);
  return (
    <View className="gap-4">
      {label ? (
        <Text className="font-sans text-[11px] font-semibold uppercase tracking-[2.2px] text-accent">
          {label}
        </Text>
      ) : null}
      <Link href={`/${post.slug}`} asChild>
        <Pressable accessibilityRole="link">
          <Text className="font-serif text-[30px] font-semibold leading-[1.1] tracking-tight text-fg md:text-[40px]">
            {post.title}
          </Text>
        </Pressable>
      </Link>
      <Text className="font-sans text-[15px] leading-[24px] text-muted">
        {deckLine(post.description, 40)}
      </Text>
      <Link href={`/${post.slug}`} asChild>
        <Pressable
          accessibilityRole="link"
          accessibilityLabel={post.title}
          className="w-full overflow-hidden border border-border"
        >
          <HomeHeroImage post={post} />
        </Pressable>
      </Link>
      <Link href={`/${post.slug}`} asChild>
        <Pressable accessibilityRole="link" className="self-start pt-1">
          <Text className="font-sans text-[12px] font-semibold uppercase tracking-[1.6px] text-accent">
            Read investigation ↗
          </Text>
        </Pressable>
      </Link>
    </View>
  );
}

function HomeSecondaryStory({ post }: { post: BlogPost }) {
  const label = sectionLabel(post.tags, post.subject);
  const hero = assetUrl(post.heroImage);
  return (
    <View className="gap-3 border-t border-border pt-8 mt-8">
      {label ? (
        <Text className="font-sans text-[11px] font-semibold uppercase tracking-[2.2px] text-accent">
          {label}
        </Text>
      ) : null}
      <Link href={`/${post.slug}`} asChild>
        <Pressable
          accessibilityRole="link"
          className="flex-row gap-4"
        >
          {hero ? (
            <SiteCoverImage
              source={{ uri: hero }}
              wrapperClassName="h-24 w-36 shrink-0 border border-border"
              transition={200}
              accessibilityLabel={post.title}
            />
          ) : null}
          <View className="min-w-0 flex-1 gap-1.5">
            <Text className="font-serif text-[21px] font-semibold leading-[1.2] tracking-tight text-fg md:text-[23px]">
              {post.title}
            </Text>
            <Text className="font-sans text-[13px] leading-[20px] text-muted">
              {deckLine(post.description, 28)}
            </Text>
          </View>
        </Pressable>
      </Link>
    </View>
  );
}

function HomeEditorsPicks({ posts }: { posts: BlogPost[] }) {
  if (!posts.length) return null;
  return (
    <View className="md:flex-[2] md:min-w-0 md:border-l md:border-border md:pl-6">
      <Text className="mb-2 font-sans text-[10px] font-bold uppercase tracking-[2px] text-muted">
        Editor&apos;s picks
      </Text>
      {posts.map((post) => (
        <BlogCard key={post.slug} post={post} variant="pick" editorial />
      ))}
    </View>
  );
}

function HomeTopStoriesGrid({ posts }: { posts: BlogPost[] }) {
  if (!posts.length) return null;
  return (
    <View className="gap-5 border-t border-border pt-8">
      <View className="items-center gap-2">
        <Text className="font-sans text-[10px] font-bold uppercase tracking-[3px] text-muted">
          Top stories
        </Text>
        <View className="h-px w-full max-w-md bg-border" />
      </View>
      <View className="flex-row flex-wrap gap-4">
        {posts.map((post) => (
          <View key={post.slug} className="min-w-[140px] flex-1 basis-[45%] md:basis-[22%]">
            <BlogCard post={post} variant="stack" editorial />
          </View>
        ))}
      </View>
    </View>
  );
}

/** FT-style front page — light, B&W, no promos. */
export function HomeMagazine() {
  const posts = getBlogPosts();
  const lead = posts[0];
  const secondary = posts[1];
  const picks = posts.slice(2, 7);
  const topStories = posts.slice(7, 15);

  if (!lead) {
    return (
      <Wrapper className="py-16">
        <Text className="font-serif text-xl text-fg">No reports yet.</Text>
      </Wrapper>
    );
  }

  return (
    <View className="bg-bg">
      <Wrapper className="gap-8 py-8 md:py-10">
        <View className="flex-col gap-10 md:flex-row md:items-start md:gap-8">
          <View className="gap-0 md:flex-[3] md:min-w-0">
            <HomeMainStory post={lead} />
            {secondary && secondary.slug !== lead.slug ? (
              <HomeSecondaryStory post={secondary} />
            ) : null}
          </View>
          <HomeEditorsPicks posts={picks} />
        </View>
        <HomeTopStoriesGrid posts={topStories} />
      </Wrapper>
    </View>
  );
}
