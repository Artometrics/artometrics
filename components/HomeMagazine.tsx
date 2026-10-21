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
  getComingInvestigations,
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
      transition={0}
      priority="high"
      accessibilityLabel={post.title}
    />
  );
}

function HomeMainStory({ post }: { post: BlogPost }) {
  const label = sectionLabel(post.tags, post.subject);
  const dateline = post.pubDate ? formatDate(post.pubDate) : null;
  return (
    <View className="house-hero">
      <View className="house-hero__drift" accessibilityElementsHidden />
      <View className="house-hero__benday" accessibilityElementsHidden />
      <View className="house-hero__line" accessibilityElementsHidden />
      <View className="house-hero__copy flex-col gap-4 md:flex-row md:items-end">
        <View className="min-w-0 flex-1 gap-3">
          {label ? (
            <Text className="house-kicker" style={{ fontFamily: "DM Mono" }}>
              {label}
            </Text>
          ) : null}
          {dateline ? (
            <Text
              className="font-mono text-[11px] uppercase tracking-[0.12em]"
              style={{ color: "#b7d0cb" }}
            >
              {dateline}
            </Text>
          ) : null}
          <Link href={`/${post.slug}`} asChild>
            <Pressable accessibilityRole="link">
              <Text
                className="home-lead-headline house-display text-[clamp(2.4rem,5vw,4.25rem)]"
                style={{ fontFamily: "Anton", color: "#f3ead7" }}
              >
                {post.title}
              </Text>
            </Pressable>
          </Link>
          <Text className="font-sans text-[17px] leading-[1.45]" style={{ color: "#f4f7f6" }}>
            {deckLine(post.description, 36)}
          </Text>
          <Link href={`/${post.slug}`} asChild>
            <Pressable accessibilityRole="link" className="self-start pt-1">
              <Text
                className="font-mono text-[11px] font-medium uppercase tracking-[0.14em]"
                style={{ color: "#7fded6" }}
              >
                Read investigation →
              </Text>
            </Pressable>
          </Link>
        </View>
        <Link href={`/${post.slug}`} asChild>
          <Pressable
            accessibilityRole="link"
            accessibilityLabel={post.title}
            className="w-[148px] shrink-0"
          >
            <HomeHeroImage post={post} aspectRatio={4 / 5} />
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
          <Text
            className="font-display text-[26px] leading-[1.05] text-fg md:text-[30px]"
            style={{ fontFamily: "Anton" }}
          >
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
  const thisWeek = getThisWeekInvestigations(undefined, 3);
  const coming = getComingInvestigations(undefined, 3);
  if (!thisWeek.length && !coming.length) return null;

  const renderRow = (
    row: { slug: string; title: string; releaseFriday: string },
    dateLabel: string,
  ) => {
    const post = getBlogPost(row.slug);
    const title = post?.title ?? row.title;
    return (
      <Link key={`${dateLabel}-${row.slug}`} href={`/${row.slug}`} asChild>
        <Pressable
          accessibilityRole="link"
          className="flex-row items-baseline justify-between gap-3 border-b border-border py-2"
        >
          <Text className="min-w-0 flex-1 font-sans text-[15px] font-semibold leading-snug text-fg">
            {title}
          </Text>
          <Text className="shrink-0 font-mono text-[10px] uppercase tracking-[0.1em] text-muted">
            {dateLabel}
          </Text>
        </Pressable>
      </Link>
    );
  };

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
      {thisWeek.length > 0 ? (
        <View className="gap-1">
          {thisWeek.map((row) =>
            renderRow(row, formatDate(row.releaseFriday)),
          )}
        </View>
      ) : (
        <Text className="font-sans text-[14px] text-muted">
          No Friday release in this window — see coming investigations below.
        </Text>
      )}
      {coming.length > 0 ? (
        <View className="gap-2 border-t border-border pt-4">
          <Text className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-muted">
            Coming
          </Text>
          {coming.map((row) =>
            renderRow(row, formatDate(row.releaseFriday)),
          )}
        </View>
      ) : null}
    </View>
  );
}

function HomeEditorsPicks({ posts }: { posts: BlogPost[] }) {
  if (!posts.length) return null;
  return (
    <View className="md:flex-[2] md:min-w-0 md:border-l md:border-border md:pl-6">
      <View className="mb-1 flex-row items-baseline justify-between border-b-2 border-fg pb-2">
        <Text
          accessibilityRole="header"
          className="font-mono text-[11px] font-bold uppercase tracking-[0.16em] text-fg"
        >
          Editor&apos;s picks
        </Text>
        <Link href="/blog" asChild>
          <Pressable accessibilityRole="link" accessibilityLabel="See all reports">
            <Text className="font-mono text-[10px] font-semibold uppercase tracking-[0.14em] text-accent">
              See all →
            </Text>
          </Pressable>
        </Link>
      </View>
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
