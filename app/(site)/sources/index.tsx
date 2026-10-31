import { useEffect } from "react";
import { Platform, Text, View, Pressable } from "react-native";
import { Link, type Href } from "expo-router";
import Head from "expo-router/head";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { SeoJsonLd } from "@/components/SeoJsonLd";
import catalog from "@/src/generated/sources.json";

type Citation = { text: string; href: string | null };
type DatasetLink = { id: string; title: string; href: string };
type SourceEntry = {
  slug: string;
  title: string;
  kicker: string;
  href: string;
  updatedThrough: string;
  updatedThroughKind: "coverage" | "citation" | "unchecked" | "editorial";
  datasets: DatasetLink[];
  citations: Citation[];
  fixes?: SourceEntry[];
};
type SourceTopic = {
  id: string;
  title: string;
  description: string;
  href: string;
  issues: SourceEntry[];
};

const topics = catalog.topics as SourceTopic[];
const reportCount = topics.reduce((sum, topic) => sum + topic.issues.length, 0);
const SITE = "https://artometrics.com";

const DESCRIPTION =
  "Citations behind Artometrics reports, grouped by topic, with the date each file runs through.";

function citationLabel(citation: Citation) {
  return citation.text || citation.href || "Untitled citation";
}

function jumpToTopic(id: string) {
  if (Platform.OS !== "web" || typeof document === "undefined") return;
  requestAnimationFrame(() => {
    document.getElementById(id)?.scrollIntoView({ block: "start" });
  });
}

function CitationRow({ citation }: { citation: Citation }) {
  const label = citationLabel(citation);
  if (citation.href) {
    return (
      <Link
        href={citation.href as Href}
        target="_blank"
        rel="noreferrer"
        accessibilityHint="Opens the cited page"
      >
        <Text className="text-[15px] leading-6 text-accent underline decoration-transparent underline-offset-[3px] hover:decoration-current">
          {label}
        </Text>
      </Link>
    );
  }
  return (
    <View className="gap-1.5">
      <Text className="text-[15px] leading-6 text-fg">{label}</Text>
      <View className="self-start border border-border px-1.5 py-1">
        <Text className="font-mono text-[10px] uppercase tracking-[0.12em] text-fg">no link yet</Text>
      </View>
    </View>
  );
}

function DatasetLine({ datasets }: { datasets: DatasetLink[] }) {
  if (!datasets.length) return null;
  return (
    <Text className="text-[15px] leading-6 text-fg">
      Dataset{" "}
      {datasets.map((dataset, index) => (
        <Text key={dataset.id}>
          {index > 0 ? ", " : ""}
          <Link href={dataset.href as Href}>
            <Text className="font-bold text-accent">{dataset.title}</Text>
          </Link>
        </Text>
      ))}
    </Text>
  );
}

function IssueBlock({ issue, nested = false }: { issue: SourceEntry; nested?: boolean }) {
  return (
    <View className={nested ? "mt-4 gap-2 border-l border-border pl-4" : "gap-2 border-t border-border py-5"}>
      {nested ? (
        <Text className="font-mono text-[10px] uppercase tracking-[0.14em] text-fg">Data fix</Text>
      ) : issue.kicker ? (
        <Text className="font-mono text-[10px] uppercase tracking-[0.14em] text-accent">
          {issue.kicker}
        </Text>
      ) : null}
      <Link href={issue.href as Href}>
        <Text
          role="heading"
          aria-level={nested ? 4 : 3}
          className="font-sans text-[22px] font-bold leading-tight text-fg"
        >
          {issue.title}
        </Text>
      </Link>
      <Text className="font-mono text-[12px] leading-5 text-fg">{issue.updatedThrough}</Text>
      <DatasetLine datasets={issue.datasets} />
      <View className="mt-1 gap-3">
        {issue.citations.map((citation, index) => (
          <CitationRow key={`${issue.slug}-${index}`} citation={citation} />
        ))}
      </View>
      {(issue.fixes || []).map((fix) => (
        <IssueBlock key={fix.slug} issue={fix} nested />
      ))}
    </View>
  );
}

export default function SourcesScreen() {
  useEffect(() => {
    if (Platform.OS !== "web" || typeof window === "undefined") return;
    const id = window.location.hash.replace(/^#/, "");
    if (!id) return;
    const timer = setTimeout(() => jumpToTopic(id), 80);
    return () => clearTimeout(timer);
  }, []);

  return (
    <Wrapper className="sources-page gap-6 py-8 md:py-12">
      <PageSeo title="Sources" description={DESCRIPTION} path="/sources" />
      <SeoJsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "CollectionPage",
          name: "Sources",
          description: DESCRIPTION,
          url: `${SITE}/sources`,
          isPartOf: `${SITE}/resources`,
          hasPart: topics.map((topic) => ({
            "@type": "ItemList",
            name: topic.title,
            url: `${SITE}/sources#${topic.id}`,
            itemListElement: topic.issues.map((issue, index) => ({
              "@type": "ListItem",
              position: index + 1,
              name: issue.title,
              url: `${SITE}${issue.href}`,
            })),
          })),
        }}
      />
      <Head>
        <style>{`
          .sources-page ::selection { background: #0b5c56; color: #f3ead7; }
          .sources-page a:focus-visible { outline: 2px solid currentColor; outline-offset: 3px; }
          .sources-page [id] { scroll-margin-top: 7.5rem; }
        `}</style>
      </Head>

      <View className="max-w-[68ch] gap-3">
        <Text className="text-[11px] font-semibold uppercase tracking-[2.5px] text-accent">
          Library
        </Text>
        <Text
          role="heading"
          aria-level={1}
          className="font-display text-[clamp(2.5rem,10vw,3.5rem)] leading-[0.95] tracking-[-0.02em] text-fg"
        >
          Sources
        </Text>
        <Text className="font-sans text-base leading-6 text-muted">
          Citations for {reportCount} reports, grouped by topic. Updated through is the data
          coverage end when a source states one. Otherwise it is the latest citation date. If the
          file has neither, the line says not yet checked. Editorial indexes say so.
        </Text>
      </View>

      <View accessibilityLabel="Topics" className="flex-row flex-wrap gap-2">
        {topics.map((topic) => (
          <Link key={topic.id} href={`/sources#${topic.id}` as Href} asChild>
            <Pressable
              onPress={() => jumpToTopic(topic.id)}
              className="min-h-11 items-center justify-center border border-border px-3"
            >
              <Text className="font-mono text-[12px] uppercase tracking-[0.08em] text-fg">
                {topic.title}
              </Text>
            </Pressable>
          </Link>
        ))}
      </View>

      {topics.map((topic) => (
        <View key={topic.id} nativeID={topic.id} className="gap-1 border-t-2 border-fg pt-5">
          <Link href={topic.href as Href}>
            <Text
              role="heading"
              aria-level={2}
              className="font-display text-[clamp(1.75rem,6vw,2.25rem)] leading-none tracking-[-0.02em] text-fg"
            >
              {topic.title}
            </Text>
          </Link>
          <Text className="mb-2 max-w-[68ch] font-sans text-[15px] leading-6 text-muted">
            {topic.description}
          </Text>
          {topic.issues.map((issue) => (
            <IssueBlock key={issue.slug} issue={issue} />
          ))}
        </View>
      ))}
    </Wrapper>
  );
}
