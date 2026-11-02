import type { SectionSlug } from "./sections";

export type EditionManifest = {
  id: string;
  title: string;
  dek: string;
  section: SectionSlug;
  heroImage?: string;
  articleSlugs: string[];
  /** Planned glue/meta articles (may not be live yet). */
  glueSlugs: string[];
  podcastIds?: string[];
  datasetIds?: string[];
  status: "planned" | "collecting" | "published";
};

/** Vice-style special editions — manifests over live reports + glue. */
export const EDITIONS: EditionManifest[] = [
  {
    id: "music",
    title: "The Music Issue",
    dek: "Charts, catalogs, and the dual books of fame — crash course for anyone who lives in the attention economy of sound.",
    section: "arts",
    heroImage: "/images/editions/music.jpg",
    status: "collecting",
    articleSlugs: [
      "billboard",
      "rankings",
      "fame",
      "albums",
      "beyonce",
      "lyrics",
      "broadway",
      "carols",
      "radio",
      "youtube",
    ],
    glueSlugs: ["narrative-economics-of-hits", "dual-books-of-fame"],
    datasetIds: ["gutenberg-reference"],
  },
  {
    id: "movies",
    title: "The Movie Issue",
    dek: "Franchise economics, streaming libraries, and when a star becomes expensive to protect.",
    section: "arts",
    heroImage: "/images/editions/movies.jpg",
    status: "collecting",
    articleSlugs: [
      "margins",
      "horror",
      "pixar",
      "franchise",
      "blockbusters",
      "streaming",
      "netflix",
      "catalog",
      "emmys",
      "oscars",
      "simpsons",
      "television",
    ],
    glueSlugs: ["poison", "protection"],
  },
  {
    id: "games",
    title: "The Games Issue",
    dek: "Steam, Pokémon, boards, and fandom as preference infrastructure.",
    section: "arts",
    heroImage: "/images/editions/games.jpg",
    status: "collecting",
    articleSlugs: [
      "steam",
      "slices",
      "pokemon",
      "games",
      "anime",
      "legos",
      "comics",
    ],
    glueSlugs: ["preference-infrastructure-fandom"],
  },
  {
    id: "food",
    title: "The Culinary Issue",
    dek: "Coffee, beer, wine, ramen, and the prestige economics of taste.",
    section: "culture",
    heroImage: "/images/editions/food.jpg",
    status: "collecting",
    articleSlugs: [
      "coffee",
      "breweries",
      "wine",
      "pizza",
      "ramen",
      "alcohol",
      "calories",
      "restaurants",
    ],
    glueSlugs: ["culinary-prestige-economics"],
  },
  {
    id: "sports",
    title: "The Sports Issue",
    dek: "Dynasties, markets, and institutional winning — teams as systems.",
    section: "sports",
    heroImage: "/images/editions/sports.jpg",
    status: "collecting",
    articleSlugs: [
      "dynasties",
      "yankees",
      "dodgers",
      "celtics",
      "lakers",
      "patriots",
      "warriors",
      "cowboys",
      "giants",
      "superbowl",
      "leagues",
      "fandom",
    ],
    glueSlugs: ["institutions"],
    datasetIds: ["sports-franchises"],
  },
  {
    id: "power",
    title: "The Power Issue",
    dek: "Leaders, silence, access brands, and the economics of when institutions stop protecting.",
    section: "civics",
    heroImage: "/images/editions/power.jpg",
    status: "collecting",
    articleSlugs: [
      "caesar",
      "beyonce",
      "ceos",
      "wealth",
      "trademarks",
      "prisons",
      "voters",
      "emperors",
    ],
    glueSlugs: [
      "protection",
      "playboy",
      "preference-falsification-explained",
      "silence-cascades",
      "access-mythologies",
    ],
  },
  {
    id: "science-art",
    title: "The Science of Art Issue",
    dek: "Canon, museums, heritage, and the historical bridge from artistic practice to scientific method.",
    section: "science",
    heroImage: "/images/editions/science-art.jpg",
    status: "collecting",
    articleSlugs: [
      "pantheon",
      "museums",
      "heritage",
      "gutenberg",
      "lcsh",
      "languages",
      "phds",
    ],
    glueSlugs: ["how-art-made-science"],
    datasetIds: ["gutenberg-reference"],
  },
  {
    id: "canon",
    title: "The Canon Issue",
    dek: "How lists become memory — Gutenberg, Pantheon, Rolling Stone, and literary fame.",
    section: "humanities",
    heroImage: "/images/editions/canon.jpg",
    status: "collecting",
    articleSlugs: [
      "gutenberg",
      "lcsh",
      "pantheon",
      "albums",
      "sherlock",
      "novels",
      "medium",
    ],
    glueSlugs: ["canon-formation-mechanics"],
  },
  {
    id: "geo",
    title: "The Atlas Issue",
    dek: "Soft power, rival cities, export identity — culture on a map.",
    section: "civics",
    heroImage: "/images/editions/geo.jpg",
    status: "collecting",
    articleSlugs: [
      "geopolitics",
      "exporters",
      "atlas",
      "metros",
      "rivalry",
      "bioeconomics",
      "parks",
      "sf",
    ],
    glueSlugs: [],
    datasetIds: ["creative-exports"],
  },
  {
    id: "platforms",
    title: "The Platform Issue",
    dek: "Netflix, Steam, YouTube dynasties, and attention as a factor market.",
    section: "arts",
    heroImage: "/images/editions/platforms.jpg",
    status: "collecting",
    articleSlugs: [
      "netflix",
      "catalog",
      "steam",
      "youtube",
      "streaming",
      "metrics",
      "medium",
    ],
    glueSlugs: ["attention-as-factor-market"],
    datasetIds: ["streaming-catalogs"],
  },
  {
    id: "identity",
    title: "The Identity Issue",
    dek: "Language, schools, regional identity — preference infrastructure made visible.",
    section: "culture",
    heroImage: "/images/editions/identity.jpg",
    status: "collecting",
    articleSlugs: [
      "schools",
      "languages",
      "fandom",
      "factbook",
      "diplomacy",
    ],
    glueSlugs: [],
  },
  {
    id: "money",
    title: "The Money Issue",
    dek: "Wages, tuition, prestige, and what creative labor actually pays.",
    section: "civics",
    heroImage: "/images/editions/money.jpg",
    status: "collecting",
    articleSlugs: [
      "wealth",
      "majors",
      "tuition",
      "phds",
      "mac",
      "ceos",
      "leagues",
    ],
    glueSlugs: [],
  },
  {
    id: "risk",
    title: "The Risk Issue",
    dek: "Airlines, storms, nuclear ledgers, hospitals — institutional risk as narrative and number.",
    section: "science",
    heroImage: "/images/editions/risk.jpg",
    status: "collecting",
    articleSlugs: [
      "airlines",
      "hurricanes",
      "nuclear",
      "plastic",
      "wastewater",
      "readmitted",
      "longevity",
      "exercise",
    ],
    glueSlugs: [],
  },
  {
    id: "psychonomics",
    title: "The Psychonomics Issue",
    dek: "OSS-style leader profiles — when one person’s psychology becomes infrastructure.",
    section: "humanities",
    heroImage: "/images/editions/psychonomics.jpg",
    status: "collecting",
    articleSlugs: [
      "caesar",
      "beyonce",
      "emperors",
      "ceos",
    ],
    glueSlugs: [
      "comparative-psychonomics-panel",
      "jackson",
      "protection",
    ],
  },
];

export function getEdition(id: string): EditionManifest | undefined {
  return EDITIONS.find((e) => e.id === id);
}

/** Slug → edition ids (many-to-many). */
export function buildEditionCrosswalk(): Record<string, string[]> {
  const map: Record<string, string[]> = {};
  for (const ed of EDITIONS) {
    for (const slug of [...ed.articleSlugs, ...ed.glueSlugs]) {
      if (!map[slug]) map[slug] = [];
      if (!map[slug].includes(ed.id)) map[slug].push(ed.id);
    }
  }
  return map;
}
