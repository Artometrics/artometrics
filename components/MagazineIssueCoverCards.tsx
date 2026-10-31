import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { SiteCoverImage } from "@/components/SiteCoverImage";
import {
  magazineContentsHref,
  magazineImg,
  magazineIssue,
  magazineIssueHref,
} from "@/lib/magazine";

export type MagazineCoverCard = {
  id: string;
  title: string;
  subtitle: string;
  href: string;
  /** Magazine hero path under /img… or site path */
  coverSrc: string;
  accent?: string;
};

const FEATURED_SKIN_SLUGS = ["billboard", "streaming", "youtube"] as const;

/** Cover cards for Lab log — default skins + specialty issue packs. */
export function buildMagazineCoverCards(): MagazineCoverCard[] {
  const franchise = magazineIssue("franchise");
  const franchiseHero = franchise ? magazineImg(franchise.hero) : "/logo.png";

  const cards: MagazineCoverCard[] = [
    {
      id: "october-edition",
      title: "October 2026",
      subtitle: "103 five-minute issues · swipe the full TOC",
      href: magazineContentsHref(),
      coverSrc: franchiseHero,
    },
    {
      id: "data-minimal",
      title: "Data Minimal",
      subtitle: "Ledger skin · serif audit columns",
      href: magazineContentsHref("ledger"),
      coverSrc: franchiseHero,
      accent: "#0047FF",
    },
    {
      id: "glossy-editorial",
      title: "Glossy Editorial",
      subtitle: "Back of the Box · packaging loud type",
      href: magazineContentsHref("box"),
      coverSrc: franchiseHero,
      accent: "#FFCC00",
    },
    {
      id: "indie-zine",
      title: "Indie Zine",
      subtitle: "Trade Paper · marquee credits",
      href: magazineContentsHref("trade"),
      coverSrc: franchiseHero,
      accent: "#8A8A8A",
    },
  ];

  for (const slug of FEATURED_SKIN_SLUGS) {
    const issue = magazineIssue(slug);
    if (!issue) continue;
    const skinHint =
      slug === "billboard"
        ? "Chart · Sleeve · Stream skins"
        : slug === "streaming"
          ? "Top Shelf · Program Guide · Late Show"
          : "Filing · Living Room · On Air";
    cards.push({
      id: `pack-${slug}`,
      title: issue.title,
      subtitle: `${issue.kicker} · ${skinHint}`,
      href: magazineIssueHref(slug),
      coverSrc: magazineImg(issue.hero),
    });
  }

  return cards;
}

export function MagazineIssueCoverCards({ cards }: { cards: MagazineCoverCard[] }) {
  return (
    <View className="flex-row flex-wrap gap-3">
      {cards.map((card) => (
        <Link key={card.id} href={card.href} asChild>
          <Pressable
            accessibilityRole="link"
            accessibilityLabel={`Open magazine: ${card.title}`}
            className="w-full min-w-0 max-w-full sm:max-w-[calc(50%-6px)]"
          >
            <View
              className="overflow-hidden border-2 border-fg bg-bg-elevated"
              style={{
                shadowColor: "#E60000",
                shadowOffset: { width: 3, height: 3 },
                shadowOpacity: 1,
                shadowRadius: 0,
              }}
            >
              <SiteCoverImage
                source={{ uri: card.coverSrc }}
                wrapperClassName="w-full"
                wrapperStyle={{ aspectRatio: 3 / 4 }}
                transition={200}
                accessibilityLabel={card.title}
              />
              <View className="gap-1 border-t-2 border-fg p-3">
                {card.accent ? (
                  <View className="h-1 w-10 rounded-full" style={{ backgroundColor: card.accent }} />
                ) : (
                  <Text className="font-mono text-[9px] font-bold uppercase tracking-[0.14em] text-accent">
                    Page-flip
                  </Text>
                )}
                <Text
                  className="font-display text-[18px] leading-tight text-fg"
                  style={{ fontFamily: "Anton" }}
                  numberOfLines={3}
                >
                  {card.title}
                </Text>
                <Text className="font-sans text-[13px] leading-snug text-muted" numberOfLines={2}>
                  {card.subtitle}
                </Text>
              </View>
            </View>
          </Pressable>
        </Link>
      ))}
    </View>
  );
}
