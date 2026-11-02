import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import { magazineImg, magazineIssue, magazineIssueHref } from "@/lib/magazine";

type Props = {
  slug: string;
};

/** Cover-thumbnail entry for the page-flip edition. Renders nothing when the slug has no issue. */
export function MagazineEditionCard({ slug }: Props) {
  const issue = magazineIssue(slug);
  if (!issue) return null;
  const hero = magazineImg(issue.hero);
  const href = magazineIssueHref(issue.slug);

  return (
    <Link href={href} asChild>
      <Pressable
        accessibilityRole="link"
        accessibilityLabel={`Read as ebook: ${issue.title}`}
        className="ebook-entry"
      >
        {hero ? (
          <SiteCoverImage
            source={{ uri: hero }}
            wrapperClassName="ebook-entry__cover"
            wrapperStyle={{ width: 84, height: 96 }}
            transition={200}
            accessibilityLabel=""
          />
        ) : (
          <View className="ebook-entry__cover" />
        )}
        <View className="ebook-entry__copy">
          <Text className="ebook-entry__kicker" style={{ fontFamily: "DM Mono" }}>
            Ebook
          </Text>
          <Text className="ebook-entry__title" style={{ fontFamily: "Anton" }}>
            Read as ebook
          </Text>
          <Text className="ebook-entry__meta" style={{ fontFamily: "DM Mono" }} numberOfLines={1}>
            {issue.kicker} · page-flip
          </Text>
        </View>
      </Pressable>
    </Link>
  );
}
