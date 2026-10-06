import React, { useEffect } from "react";
import { Pressable, Text, View } from "react-native";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import { useLocalSearchParams, Link } from "expo-router";
import { assetUrl } from "@/lib/assets";
import { Wrapper } from "@/components/Wrapper";
import { ArticleBody } from "@/components/ArticleBody";
import { ArticleActions } from "@/components/ArticleActions";
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
import { paramString } from "@/lib/params";
import { trackEvent } from "@/lib/analytics/ga";

function estimateMinutes(html: string) {
  const text = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  const words = text ? text.split(" ").length : 0;
  return Math.max(1, Math.round(words / 200));
}

export async function generateStaticParams() {
  return getBlogPosts().map((post) => ({ slug: post.slug }));
}

export default function ReportScreen() {
  const params = useLocalSearchParams<{ slug: string | string[] }>();
  const slug = paramString(params.slug);
  const post = getBlogPost(slug);

  useEffect(() => {
    if (!post) return;
    trackEvent("report_view", { slug: post.slug });
  }, [post?.slug]);

  if (!post) {
    return (
      <Wrapper variant="narrow" className="gap-3 pb-4 pt-10">
        <Text className="font-serif text-2xl text-fg">Report not found</Text>
        <Link href="/">
          <Text className="font-sans text-[11px] uppercase tracking-[2px] text-muted">
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

      <Wrapper variant="wide" className="gap-6 border-b border-border pb-8 pt-3 md:pt-4">
        <View className="flex-row flex-wrap items-center justify-between gap-x-3 gap-y-2">
          <View className="min-w-0 shrink">
            <ReportBreadcrumb tags={post.tags} />
          </View>
          <ArticleActions
            slug={post.slug}
            title={post.title}
            description={post.description}
            audioSrc={(post as { audioSrc?: string | null }).audioSrc}
            placement="header"
            variant="inline"
          />
        </View>
        <View className="flex-col gap-6 md:flex-row md:items-center md:gap-8">
          {hero ? (
            <View className="min-w-0 w-full shrink-0 md:w-1/2 md:flex-1">
              <SiteCoverImage
                source={{ uri: hero }}
                wrapperClassName="w-full overflow-hidden border border-border"
                wrapperStyle={{ aspectRatio: 16 / 10 }}
                transition={200}
                accessibilityLabel={post.title}
              />
            </View>
          ) : null}
          <View
            className={[
              "min-w-0 justify-center gap-3",
              hero ? "w-full md:w-1/2 md:flex-1" : "w-full",
            ].join(" ")}
          >
            <Text
              role="heading"
              aria-level={1}
              className="font-serif text-[28px] font-bold leading-[1.12] tracking-tight text-secondary sm:text-[32px] md:text-[36px] lg:text-[42px]"
            >
              {headline ? (
                <Text>
                  <Text className="text-accent">{headline.slug}</Text>
                  {`: ${headline.subtitle}`}
                </Text>
              ) : (
                post.title
              )}
            </Text>
            <Text className="font-serif text-lg font-bold leading-snug text-accent md:text-xl md:leading-relaxed">
              {deckLine(post.description, 12)}
            </Text>
            <Text className="font-sans text-[13px] font-bold uppercase tracking-[1.4px] text-fg md:text-sm">
              <Text className="text-accent">By </Text>
              {authorLabel}
              {post.pubDate ? ` · ${formatDate(post.pubDate)}` : ""} · {minutes} min
            </Text>
          </View>
        </View>
      </Wrapper>

      {post.keyPoints && post.keyPoints.length > 0 ? (
        <Wrapper variant="wide" className="pt-6 pb-2">
          <ReportStatGrid
            keyPoints={post.keyPoints}
            subject={post.subject}
            sourceLabel={post.subject ? `${post.subject} Analysis` : undefined}
          />
        </Wrapper>
      ) : null}

      <Wrapper variant="bleed" className="w-full min-w-0 max-w-[1600px] self-stretch gap-3 px-3 py-8 md:px-4">
        <ArticleBody html={post.body} />
        <ReportRelatedReads slug={post.slug} limit={4} />
      </Wrapper>
    </View>
  );
}
