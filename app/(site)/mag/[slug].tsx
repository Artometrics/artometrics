import React, { useEffect } from "react";
import { Text, View } from "react-native";
import { Link, useLocalSearchParams } from "expo-router";
import { MagazineFrame } from "@/components/MagazineFrame";
import { PageSeo } from "@/components/PageSeo";
import { SeoJsonLd } from "@/components/SeoJsonLd";
import { Wrapper } from "@/components/Wrapper";
import { paramString } from "@/lib/params";
import { trackEvent } from "@/lib/analytics/ga";
import {
  issueJsonLd,
  magazineImg,
  magazineIssue,
  magazineIssues,
  magazineIssueHref,
  renderIssueBody,
} from "@/lib/magazine";
import { skinsForIssue } from "@/lib/magazine-skins";

export async function generateStaticParams() {
  return magazineIssues().map((issue) => ({ slug: issue.slug }));
}

export default function MagazineIssueScreen() {
  const params = useLocalSearchParams<{ slug: string | string[] }>();
  const slug = paramString(params.slug);
  const issue = magazineIssue(slug);

  useEffect(() => {
    if (!issue) return;
    trackEvent("magazine_view", { slug: issue.slug });
  }, [issue?.slug]);

  if (!issue) {
    return (
      <Wrapper variant="narrow" className="gap-3 pb-4 pt-10">
        <Text className="font-sans text-2xl text-fg">Magazine issue not found</Text>
        <Link href="/mag">
          <Text className="font-mono text-[11px] uppercase tracking-[2px] text-muted">
            ← Magazine contents
          </Text>
        </Link>
      </Wrapper>
    );
  }

  const image = magazineImg(issue.hero);
  const magPath = magazineIssueHref(issue.slug);

  return (
    <View style={{ flex: 1, backgroundColor: "#ffffff" }}>
      <PageSeo
        title={`${issue.title} — Artometrics Magazine`}
        description={issue.dek}
        path={magPath}
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
