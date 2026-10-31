import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import { magazineImg, magazineIssue, magazineIssueHref, type MagIssue } from "@/lib/magazine";

type Props = {
  slug: string;
  compact?: boolean;
};

function MagazineEditionCardInner({ issue, compact }: { issue: MagIssue; compact?: boolean }) {
  const hero = magazineImg(issue.hero);
  const href = magazineIssueHref(issue.slug);

  return (
    <Link href={href} asChild>
      <Pressable
        accessibilityRole="link"
        accessibilityLabel={`Read the magazine edition: ${issue.title}`}
        className={[
          "overflow-hidden border-2 border-fg bg-bg-elevated",
          compact ? "flex-row items-stretch gap-0" : "gap-0",
        ].join(" ")}
        style={{ shadowColor: "#E60000", shadowOffset: { width: 4, height: 4 }, shadowOpacity: 1, shadowRadius: 0 }}
      >
        {hero ? (
          <SiteCoverImage
            source={{ uri: hero }}
            wrapperClassName={compact ? "w-[108px] shrink-0" : "w-full"}
            wrapperStyle={{ aspectRatio: compact ? 4 / 5 : 16 / 10 }}
            transition={200}
            accessibilityLabel=""
          />
        ) : null}
        <View className={compact ? "min-w-0 flex-1 justify-center gap-1.5 p-4" : "gap-2 p-4"}>
          <Text className="font-mono text-[10px] font-bold uppercase tracking-[0.16em] text-accent">
            Magazine edition
          </Text>
          <Text
            className="font-display text-[22px] leading-[1.05] text-fg"
            style={{ fontFamily: "Anton" }}
            numberOfLines={compact ? 3 : 4}
          >
            {issue.title}
          </Text>
          {!compact ? (
            <Text className="font-sans text-[14px] leading-snug text-muted" numberOfLines={2}>
              {issue.dek}
            </Text>
          ) : null}
          <Text className="font-mono text-[10px] font-semibold uppercase tracking-[0.14em] text-accent pt-1">
            Open page-flip reader →
          </Text>
        </View>
      </Pressable>
    </Link>
  );
}

/** End-of-article promo for the abbreviated page-flip issue when one exists. */
export function MagazineEditionCard({ slug, compact = true }: Props) {
  const issue = magazineIssue(slug);
  if (!issue) return null;
  return (
    <View className="gap-2 pt-2">
      <MagazineEditionCardInner issue={issue} compact={compact} />
    </View>
  );
}
