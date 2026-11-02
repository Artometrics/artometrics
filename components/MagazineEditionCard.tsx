import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import { magazineImg, magazineIssue, magazineIssueHref, type MagIssue } from "@/lib/magazine";

type Props = {
  slug: string;
};

function EbookCard({ issue }: { issue: MagIssue }) {
  const hero = magazineImg(issue.hero);
  const href = magazineIssueHref(issue.slug);

  return (
    <Link href={href} asChild>
      <Pressable
        accessibilityRole="link"
        accessibilityLabel={`Read as ebook: ${issue.title}`}
        className="flex-row items-stretch overflow-hidden border border-[#f4efe4] bg-[#07070a]"
        style={{ boxShadow: "4px 4px 0 #ff3d8a" }}
      >
        {hero ? (
          <SiteCoverImage
            source={{ uri: hero }}
            wrapperClassName="w-[72px] shrink-0 bg-[#111]"
            wrapperStyle={{ aspectRatio: 4 / 5 }}
            transition={200}
            accessibilityLabel=""
          />
        ) : (
          <View className="w-[72px] shrink-0 bg-[#111]" style={{ aspectRatio: 4 / 5 }} />
        )}
        <View className="min-w-0 flex-1 justify-center gap-1 px-3 py-2.5">
          <Text
            className="font-display text-[22px] leading-[1.05] text-[#f3ead7]"
            style={{ fontFamily: "Anton" }}
            numberOfLines={2}
          >
            Read as ebook
          </Text>
          <Text
            className="font-mono text-[10px] font-medium uppercase tracking-[0.14em]"
            style={{ color: "#7fded6" }}
            numberOfLines={1}
          >
            {issue.kicker} · page-flip edition
          </Text>
        </View>
      </Pressable>
    </Link>
  );
}

/** Top-of-article entry for the page-flip edition. Hidden when the report has no issue. */
export function MagazineEditionCard({ slug }: Props) {
  const issue = magazineIssue(slug);
  if (!issue) return null;
  return <EbookCard issue={issue} />;
}
