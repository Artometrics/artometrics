import { MagazineFrame } from "@/components/MagazineFrame";
import { PageSeo } from "@/components/PageSeo";
import { SeoJsonLd } from "@/components/SeoJsonLd";
import { contentsJsonLd, magazineIssues, renderContentsBody } from "@/lib/magazine";

const issues = magazineIssues();

export default function HomeScreen() {
  return (
    <>
      <PageSeo
        title="Artometrics Magazine"
        description="Data stories, five minutes each. Arts, sports, science, humanities, civics, and culture."
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
          contentsJsonLd(issues),
        ]}
      />
      <MagazineFrame pageKey="contents" label="Contents" bodyHtml={renderContentsBody(issues)} />
    </>
  );
}
