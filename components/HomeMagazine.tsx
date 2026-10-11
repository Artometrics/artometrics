import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { BlogCard } from "@/components/BlogCard";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import { assetUrl } from "@/lib/assets";
import {
  deckLine,
  formatDate,
  getBlogPost,
  getBlogPosts,
  sectionLabel,
  type BlogPost,
} from "@/lib/content";
import {
  formatIssueWeekLabel,
  getThisWeekInvestigations,
} from "@/lib/contentCalendar";

function HomeHeroImage({
  post,
  aspectRatio = 4 / 5,
}: {
  post: BlogPost;
  aspectRatio?: number;
}) {
  const hero = assetUrl(post.heroImage);
  if (!hero) {
    return (
      <View
        className="w-full overflow-hidden bg-bg-elevated"
        style={{ aspectRatio }}
      />
    );
  }
  return (
    <SiteCoverImage
      source={{ uri: hero }}
      wrapperClassName="w-full"
      wrapperStyle={{ aspectRatio }}
      transition={250}
      accessibilityLabel={post.title}
    />
  );
}

function HomeMainStory({ post }: { post: BlogPost }) {
  const label = sectionLabel(post.tags, post.subject);
  const dateline = post.pubDate ? formatDate(post.pubDate) : null;
  return (
    <View className="flex-col gap-6 md:flex-row md:items-stretch md:gap-8">
      <Link href={`/${post.slug}`} asChild>
        <Pressable
          accessibilityRole="link"
          accessibilityLabel={post.title}
          className="min-w-0 md:w-[62%] md:flex-[3]"
        >
          <HomeHeroImage post={post} aspectRatio={16 / 10} />
        </Pressable>
      </Link>
      <View className="min-w-0 justify-end gap-3 md:w-[38%] md:flex-[2] md:py-2">
        {label ? (
          <Text className="font-mono text-[11px] font-medium uppercase tracking-[0.14em] text-secondary">
            {label}
          </Text>
        ) : null}
        {dateline ? (
          <Text className="font-mono text-[11px] uppercase tracking-[0.12em] text-muted">
            {dateline}
          </Text>
        ) : null}
        <Link href={`/${post.slug}`} asChild>
          <Pressable accessibilityRole="link">
            <Text
              className="font-sans text-[clamp(28px,4vw,48px)] font-bold leading-[1.05] tracking-[-0.02em] text-fg"
            >
              {post.title}
            </Text>
          </Pressable>
        </Link>
        <Text className="font-sans text-[17px] leading-[1.45] text-muted">
          {deckLine(post.description, 36)}
        </Text>
        <Link href={`/${post.slug}`} asChild>
          <Pressable accessibilityRole="link" className="self-start pt-1">
            <Text className="font-mono text-[11px] font-medium uppercase tracking-[0.14em] text-accent">
              Read investigation →
            </Text>
          </Pressable>
        </Link>
      </View>
    </View>
  );
}

function HomeSecondaryStory({ post }: { post: BlogPost }) {
  const label = sectionLabel(post.tags, post.subject);
  return (
    <View className="gap-2 border-t-2 border-fg pt-6">
      {label ? (
        <Text className="font-mono text-[10px] font-medium uppercase tracking-[0.14em] text-muted">
          {label}
        </Text>
      ) : null}
      <Link href={`/${post.slug}`} asChild>
        <Pressable accessibilityRole="link" className="gap-1">
          <Text className="font-sans text-[20px] font-semibold leading-[1.2] tracking-tight text-fg md:text-[22px]">
            {post.title}
          </Text>
          <Text className="font-sans text-[14px] leading-[1.4] text-muted">
            {deckLine(post.description, 22)}
          </Text>
        </Pressable>
      </Link>
    </View>
  );
}

function HomeThisWeekRow() {
  const rows = getThisWeekInvestigations(undefined, 3);
  if (!rows.length) return null;
  return (
    <View className="gap-4 border-t-2 border-fg pt-8">
      <View className="gap-1">
        <Text className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-accent">
          This week
        </Text>
        <Text className="font-mono text-[11px] uppercase tracking-[0.1em] text-muted">
          {formatIssueWeekLabel()}
        </Text>
      </View>
      <View className="gap-3">
        {rows.map((row) => {
          const post = getBlogPost(row.slug);
          const title = post?.title ?? row.title;
          const release = formatDate(row.releaseFriday);
          return (
            <Link key={row.slug} href={`/${row.slug}`} asChild>
              <Pressable
                accessibilityRole="link"
                className="flex-row items-baseline justify-between gap-3 border-b border-border py-2"
              >
                <Text className="min-w-0 flex-1 font-sans text-[15px] font-semibold leading-snug text-fg">
                  {title}
                </Text>
                <Text className="shrink-0 font-mono text-[10px] uppercase tracking-[0.1em] text-secondary">
                  {release}
                </Text>
              </Pressable>
            </Link>
          );
        })}
      </View>
    </View>
  );
}

function HomeEditorsPicks({ posts }: { posts: BlogPost[] }) {
  if (!posts.length) return null;
  return (
    <View className="md:flex-[2] md:min-w-0 md:border-l md:border-border md:pl-6">
      <Text className="mb-3 font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-muted">
        Editor&apos;s picks
      </Text>
      {posts.map((post) => (
        <BlogCard key={post.slug} post={post} variant="pick" editorial />
      ))}
    </View>
  );
}

function HomeBriefsList({ posts }: { posts: BlogPost[] }) {
  if (!posts.length) return null;
  return (
    <View className="gap-4 border-t-2 border-fg pt-8">
      <Text className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-muted">
        Briefs
      </Text>
      <View className="gap-1">
        {posts.map((post) => (
          <HomeSecondaryStory key={post.slug} post={post} />
        ))}
      </View>
    </View>
  );
}

/** Magazine front page — asymmetric lead, section rules, issue row. */
export function HomeMagazine() {
  const posts = getBlogPosts();
  const lead = posts[0];
  const secondary = posts[1];
  const moreBriefs = posts.slice(2, 5);
  const picks = posts.slice(5, 10);

  if (!lead) {
    return (
      <Wrapper className="py-16">
        <Text className="font-sans text-xl text-fg">No reports yet.</Text>
      </Wrapper>
    );
  }

  return (
    <View className="bg-bg">
      <Wrapper className="gap-0 py-8 md:py-12">
        <View className="flex-col gap-10 md:flex-row md:items-start md:gap-8">
          <View className="gap-8 md:flex-[3] md:min-w-0">
            <HomeMainStory post={lead} />
            {secondary && secondary.slug !== lead.slug ? (
              <HomeSecondaryStory post={secondary} />
            ) : null}
          </View>
          <HomeEditorsPicks posts={picks} />
        </View>

        <HomeThisWeekRow />

        <HomeBriefsList posts={moreBriefs} />
      </Wrapper>
    </View>
  );
}
