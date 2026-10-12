import { useLocalSearchParams } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { MagazineJournalIndex } from "@/components/MagazineJournalIndex";
import { getBlogPosts, primarySection, primarySubdomain } from "@/lib/content";
import { isSubdomainSlug, SECTION_META, SECTION_SLUGS, type SectionSlug } from "@/data/sections";
import { PageSeo } from "@/components/PageSeo";
import { paramString } from "@/lib/params";

export default function BlogIndex() {
  const params = useLocalSearchParams<{
    desk?: string | string[];
    section?: string | string[];
    subdomain?: string | string[];
  }>();
  const raw = paramString(params.section) || paramString(params.desk);
  const sectionFilter =
    raw && SECTION_SLUGS.includes(raw as SectionSlug) ? (raw as SectionSlug) : null;
  const rawSub = paramString(params.subdomain);
  const subdomainFilter = rawSub && isSubdomainSlug(rawSub) ? rawSub : null;
  const posts = getBlogPosts().filter((post) => {
    if (sectionFilter && primarySection(post.tags) !== sectionFilter) return false;
    if (subdomainFilter && primarySubdomain(post.tags) !== subdomainFilter) return false;
    return true;
  });

  const title = sectionFilter
    ? SECTION_META[sectionFilter].title
    : subdomainFilter
      ? subdomainFilter.replace(/-/g, " ")
      : "All investigations";

  const description = sectionFilter
    ? SECTION_META[sectionFilter].description
    : "Every Artometrics data report — cover stories, charts, and downloadable sources.";

  return (
    <Wrapper variant="wide" className="gap-0 py-8 md:py-10">
      <PageSeo
        title={sectionFilter ? title : "Reports"}
        description={description}
        path="/blog"
      />
      <MagazineJournalIndex title={title} description={description} posts={posts} />
    </Wrapper>
  );
}
