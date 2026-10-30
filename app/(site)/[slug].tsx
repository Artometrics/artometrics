import React, { useEffect } from "react";
import { Text, View } from "react-native";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import { useLocalSearchParams, Link } from "expo-router";
import { assetUrl } from "@/lib/assets";
import { Wrapper } from "@/components/Wrapper";
import { ArticleBody } from "@/components/ArticleBody";
import { ArticleActions } from "@/components/ArticleActions";
import { ArticleNarrationPlayer } from "@/components/ArticleNarrationPlayer";
import { ReportBreadcrumb } from "@/components/ReportBreadcrumb";
import { ReportRelatedReads } from "@/components/ReportRelatedReads";
import { ReportStatGrid } from "@/components/ReportStatGrid";
import { PageSeo } from "@/components/PageSeo";
import {
  deckLine,
  splitReportHeadline,
  formatAuthorName,
  formatDate,
  getBlogPost,
  getBlogPosts,
  sectionLabel,
} from "@/lib/content";
import { SECTION_META } from "@/data/sections";
import { SeoJsonLd } from "@/components/SeoJsonLd";
import { MagazineFrame } from "@/components/MagazineFrame";
import { paramString } from "@/lib/params";
import { trackEvent } from "@/lib/analytics/ga";
import {
  issueJsonLd,
  magazineImg,
  magazineIssue,
  magazineIssues,
  renderIssueBody,
} from "@/lib/magazine";
import { skinsForIssue } from "@/lib/magazine-skins";

function estimateMinutes(html: string) {
  const text = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  const words = text ? text.split(" ").length : 0;
  return Math.max(1, Math.round(words / 200));
}

export async function generateStaticParams() {
  const slugs = new Set<string>([
    ...getBlogPosts().map((post) => post.slug),
    ...magazineIssues().map((issue) => issue.slug),
  ]);
  return [...slugs].map((slug) => ({ slug }));
}

/** Full-article AI narrations (Gemini TTS, Kore). Runtimes are ffprobe durations floored to whole seconds. */
const NARRATION_META: Record<string, { runtimeSeconds: number; label: string }> = {
  anime: { runtimeSeconds: 1818, label: "Listen: narrated by AI voice (Kore), 30:18" },
  readmitted: { runtimeSeconds: 1145, label: "Listen: narrated by AI voice (Kore), 19:05" },
  franchise: { runtimeSeconds: 1451, label: "Listen: narrated by AI voice (Kore), 24:11" },
  youtube: { runtimeSeconds: 945, label: "Listen: narrated by AI voice (Kore), 15:45" },
};

export default function ReportScreen() {
  const params = useLocalSearchParams<{ slug: string | string[] }>();
  const slug = paramString(params.slug);
  const issue = magazineIssue(slug);
  const post = getBlogPost(slug);

  useEffect(() => {
    const viewed = issue?.slug || post?.slug;
    if (!viewed) return;
    trackEvent("report_view", { slug: viewed });
  }, [issue?.slug, post?.slug]);

  if (issue) {
    const image = magazineImg(issue.hero);
    return (
      <View style={{ flex: 1, backgroundColor: "#ffffff" }}>
        <PageSeo
          title={`${issue.title} — Artometrics`}
          description={issue.dek}
          path={`/${issue.slug}`}
          image={image || undefined}
          type="article"
        />
        <SeoJsonLd data={issueJsonLd(issue)} />
        <MagazineFrame
          pageKey={issue.slug}
          label={`Artometrics · ${issue.kicker}`}
          bodyHtml={renderIssueBody(issue)}
          skins={skinsForIssue(issue)}
        />
      </View>
    );
  }

  if (!post) {
    return (
      <Wrapper variant="narrow" className="gap-3 pb-4 pt-10">
        <Text className="font-sans text-2xl text-fg">Report not found</Text>
        <Link href="/">
          <Text className="font-mono text-[11px] uppercase tracking-[2px] text-muted">
            ← Contents
          </Text>
        </Link>
      </Wrapper>
    );
  }

  const section = post.tags?.[0];
  const label = sectionLabel(post.tags, post.subject);
  const hero = assetUrl(post.heroImage);
  const minutes = estimateMinutes(post.body);
  const authorLabel = post.author ? formatAuthorName(String(post.author)) : "Kyle McAuliffe";
  const faq = (post as { faq?: { question: string; answer: string }[] }).faq ?? [];
  const headline = splitReportHeadline(post.title);
  const audioSrc = (post as { audioSrc?: string | null }).audioSrc;

  const imageAbs = post.heroImage?.startsWith("http")
    ? post.heroImage
    : post.heroImage
      ? `https://artometrics.com${post.heroImage}`
      : "https://artometrics.com/images/brand/og-default.png";

  const jsonLd = [
    {
      "@context": "https://schema.org",
      "@type": "Article",
      headline: post.title,
      description: post.description,
      datePublished: post.pubDate,
      dateModified:
        (post as { updatedDate?: string }).updatedDate || post.pubDate,
      image: [imageAbs],
      author: { "@type": "Person", name: authorLabel },
      publisher: {
        "@type": "Organization",
        name: "Artometrics",
        url: "https://artometrics.com",
      },
      mainEntityOfPage: `https://artometrics.com/${post.slug}`,
      articleSection: label ?? (section ? SECTION_META[section as keyof typeof SECTION_META]?.title : "Articles"),
    },
    ...(faq.length
      ? [
          {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            mainEntity: faq.map((item) => ({
              "@type": "Question",
              name: item.question,
              acceptedAnswer: { "@type": "Answer", text: item.answer },
            })),
          },
        ]
      : []),
  ];

  return (
    <View className="bg-bg">
      <PageSeo
        title={post.title}
        description={post.description}
        path={`/${post.slug}`}
        image={post.heroImage || undefined}
        type="article"
      />
      <SeoJsonLd data={jsonLd} />

      <Wrapper variant="measure" className="gap-4 border-b border-border pb-6 pt-3 md:pt-5">
        <View className="flex-row flex-wrap items-center justify-between gap-x-3 gap-y-2">
          <View className="min-w-0 shrink">
            <ReportBreadcrumb tags={post.tags} />
          </View>
          <ArticleActions
            slug={post.slug}
            title={post.title}
            description={post.description}
            audioSrc={audioSrc}
            placement="header"
            variant="inline"
          />
        </View>

        {label ? (
          <Text className="house-kicker self-start" style={{ fontFamily: "DM Mono" }}>
            {label}
          </Text>
        ) : null}

        <Text
          role="heading"
          aria-level={1}
          className="font-display text-[clamp(2.4rem,5vw,4rem)] leading-[0.95] text-fg"
          style={{ fontFamily: "Anton" }}
        >
          {headline ? (
            <Text>
              <Text className="text-accent">{headline.slug}</Text>
              <Text className="text-fg">{`: ${headline.subtitle}`}</Text>
            </Text>
          ) : (
            post.title
          )}
        </Text>

        <Text className="font-sans text-lg font-medium leading-snug text-muted md:text-xl">
          {deckLine(post.description, 12)}
        </Text>
      </Wrapper>

      {hero ? (
        <Wrapper variant="bleed" className="w-full px-0">
          <SiteCoverImage
            source={{ uri: hero }}
            wrapperClassName="w-full overflow-hidden"
            wrapperStyle={{ aspectRatio: post.slug === "anime" ? 16 / 9 : 16 / 10 }}
            transition={200}
            accessibilityLabel={
              post.slug === "anime"
                ? "AI-generated illustration of an animator's lightbox and stacks of timing sheets on a darkened studio desk, with a single red pencil."
                : post.title
            }
          />
          {post.slug === "anime" ? (
            <Wrapper variant="measure" className="pt-2">
              <Text className="font-mono text-[11px] uppercase tracking-[0.1em] text-muted">
                Illustration: Artometrics (AI-generated)
              </Text>
            </Wrapper>
          ) : null}
        </Wrapper>
      ) : null}

      <Wrapper variant="measure" className="gap-4 border-b-2 border-fg py-5">
        {audioSrc ? (
          <ArticleNarrationPlayer
            audioSrc={audioSrc}
            title={post.title}
            runtimeSeconds={NARRATION_META[post.slug]?.runtimeSeconds}
            label={NARRATION_META[post.slug]?.label}
          />
        ) : null}
        <Text className="font-mono text-[12px] uppercase tracking-[0.12em] text-fg">
          <Text className="text-accent">By </Text>
          {authorLabel}
          {post.pubDate ? ` · ${formatDate(post.pubDate)}` : ""} · {minutes} min read
        </Text>
      </Wrapper>

      {post.keyPoints && post.keyPoints.length > 0 ? (
        <Wrapper variant="measure" className="pt-6 pb-2">
          <ReportStatGrid
            keyPoints={post.keyPoints}
            subject={post.subject}
            sourceLabel={post.subject ? `${post.subject} Analysis` : undefined}
          />
        </Wrapper>
      ) : null}

      <Wrapper variant="measure" className="w-full min-w-0 gap-3 py-8">
        <ArticleBody html={post.body} />
      </Wrapper>

      <Wrapper variant="measure" className="pb-10">
        <ReportRelatedReads slug={post.slug} limit={4} />
      </Wrapper>
    </View>
  );
}
