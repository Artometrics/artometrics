import { HomeMagazine } from "@/components/HomeMagazine";
import { PageSeo } from "@/components/PageSeo";
import { SeoJsonLd } from "@/components/SeoJsonLd";
import { getBlogPosts } from "@/lib/content";

const posts = getBlogPosts();

export default function HomeScreen() {
  return (
    <>
      <PageSeo
        title="Artometrics — data reports for creative industries"
        description="Investigative data stories on arts, sports, science, humanities, civics, and culture."
        path="/"
      />
      <SeoJsonLd
        data={[
          {
            "@context": "https://schema.org",
            "@type": "Organization",
            name: "Artometrics",
            url: "https://artometrics.com",
            logo: "https://artometrics.com/images/brand/chomsky-a.png",
            sameAs: ["https://github.com/Artometrics"],
          },
          {
            "@context": "https://schema.org",
            "@type": "WebSite",
            name: "Artometrics",
            url: "https://artometrics.com",
            potentialAction: {
              "@type": "SearchAction",
              target: "https://artometrics.com/search?q={search_term_string}",
              "query-input": "required name=search_term_string",
            },
          },
          {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            name: "Artometrics Reports",
            url: "https://artometrics.com/",
            hasPart: posts.slice(0, 12).map((post) => ({
              "@type": "Article",
              headline: post.title,
              url: `https://artometrics.com/${post.slug}`,
            })),
          },
        ]}
      />
      <HomeMagazine />
    </>
  );
}
