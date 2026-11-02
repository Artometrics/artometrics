/** Magazine taxonomy: 6 domains · 43 subdomains (final). */

export type DomainSlug =
  | "arts"
  | "sports"
  | "science"
  | "humanities"
  | "civics"
  | "culture";

export type SubdomainSlug =
  // Arts
  | "design"
  | "music"
  | "film"
  | "theater"
  | "architecture"
  | "fashion"
  | "language"
  // Sports
  | "football"
  | "basketball"
  | "baseball"
  | "soccer"
  | "hockey"
  | "golf"
  | "tennis"
  | "fighting"
  | "gaming"
  | "motorsports"
  // Science
  | "chemistry"
  | "physics"
  | "biology"
  | "astronomy"
  | "geology"
  | "math"
  | "medicine"
  | "engineering"
  | "tech"
  // Humanities
  | "history"
  | "philosophy"
  | "religion"
  | "psychology"
  | "sociology"
  | "anthropology"
  // Civics
  | "economics"
  | "business"
  | "politics"
  | "law"
  | "education"
  | "communication"
  // Culture
  | "travel"
  | "food"
  | "leisure"
  | "environment"
  | "wellness";

export const DOMAIN_META: Record<
  DomainSlug,
  {
    title: string;
    description: string;
    /** Short nav subtitle — one line, sentence or question. */
    navDescriptor: string;
    subdomains: SubdomainSlug[];
  }
> = {
  arts: {
    title: "Arts",
    navDescriptor: "What do film, music, and design reveal?",
    description: "Design, music, film, theater, architecture, fashion, and language.",
    subdomains: [
      "design",
      "music",
      "film",
      "theater",
      "architecture",
      "fashion",
      "language",
    ],
  },
  sports: {
    title: "Sports",
    navDescriptor: "What do leagues and fandom reward?",
    description: "Football, basketball, baseball, soccer, and the wider field of play.",
    subdomains: [
      "football",
      "basketball",
      "baseball",
      "soccer",
      "hockey",
      "golf",
      "tennis",
      "fighting",
      "gaming",
      "motorsports",
    ],
  },
  science: {
    title: "Science",
    navDescriptor: "What does the evidence show?",
    description: "Chemistry through tech — the measurable world.",
    subdomains: [
      "chemistry",
      "physics",
      "biology",
      "astronomy",
      "geology",
      "math",
      "medicine",
      "engineering",
      "tech",
    ],
  },
  humanities: {
    title: "Humanities",
    navDescriptor: "How do history and ideas shape us?",
    description: "History, philosophy, religion, and the study of people.",
    subdomains: [
      "history",
      "philosophy",
      "religion",
      "psychology",
      "sociology",
      "anthropology",
    ],
  },
  civics: {
    title: "Civics",
    navDescriptor: "Who sets the rules—and who pays?",
    description: "Economics, business, politics, law, education, and communication.",
    subdomains: [
      "economics",
      "business",
      "politics",
      "law",
      "education",
      "communication",
    ],
  },
  culture: {
    title: "Culture",
    navDescriptor: "How do we travel, eat, and live?",
    description: "Travel, food, leisure, environment, and wellness.",
    subdomains: ["travel", "food", "leisure", "environment", "wellness"],
  },
};

export const SUBDOMAIN_META: Record<
  SubdomainSlug,
  { title: string; domain: DomainSlug }
> = {
  design: { title: "Design", domain: "arts" },
  music: { title: "Music", domain: "arts" },
  film: { title: "Film", domain: "arts" },
  theater: { title: "Theater", domain: "arts" },
  architecture: { title: "Architecture", domain: "arts" },
  fashion: { title: "Fashion", domain: "arts" },
  language: { title: "Language", domain: "arts" },
  football: { title: "Football", domain: "sports" },
  basketball: { title: "Basketball", domain: "sports" },
  baseball: { title: "Baseball", domain: "sports" },
  soccer: { title: "Soccer", domain: "sports" },
  hockey: { title: "Hockey", domain: "sports" },
  golf: { title: "Golf", domain: "sports" },
  tennis: { title: "Tennis", domain: "sports" },
  fighting: { title: "Fighting", domain: "sports" },
  gaming: { title: "Gaming", domain: "sports" },
  motorsports: { title: "Motorsports", domain: "sports" },
  chemistry: { title: "Chemistry", domain: "science" },
  physics: { title: "Physics", domain: "science" },
  biology: { title: "Biology", domain: "science" },
  astronomy: { title: "Astronomy", domain: "science" },
  geology: { title: "Geology", domain: "science" },
  math: { title: "Math", domain: "science" },
  medicine: { title: "Medicine", domain: "science" },
  engineering: { title: "Engineering", domain: "science" },
  tech: { title: "Tech", domain: "science" },
  history: { title: "History", domain: "humanities" },
  philosophy: { title: "Philosophy", domain: "humanities" },
  religion: { title: "Religion", domain: "humanities" },
  psychology: { title: "Psychology", domain: "humanities" },
  sociology: { title: "Sociology", domain: "humanities" },
  anthropology: { title: "Anthropology", domain: "humanities" },
  economics: { title: "Economics", domain: "civics" },
  business: { title: "Business", domain: "civics" },
  politics: { title: "Politics", domain: "civics" },
  law: { title: "Law", domain: "civics" },
  education: { title: "Education", domain: "civics" },
  communication: { title: "Communication", domain: "civics" },
  travel: { title: "Travel", domain: "culture" },
  food: { title: "Food", domain: "culture" },
  leisure: { title: "Leisure", domain: "culture" },
  environment: { title: "Environment", domain: "culture" },
  wellness: { title: "Wellness", domain: "culture" },
};

export const DOMAIN_SLUGS = Object.keys(DOMAIN_META) as DomainSlug[];
export const SUBDOMAIN_SLUGS = Object.keys(SUBDOMAIN_META) as SubdomainSlug[];

/** Nav / topics use domains (alias kept for existing imports). */
export const SECTION_META = Object.fromEntries(
  DOMAIN_SLUGS.map((slug) => [
    slug,
    { title: DOMAIN_META[slug].title, description: DOMAIN_META[slug].description },
  ]),
) as Record<DomainSlug, { title: string; description: string }>;

export type SectionSlug = DomainSlug;
export const SECTION_SLUGS = DOMAIN_SLUGS;

/** @deprecated Use SECTION_META / DOMAIN_META */
export const CHANNEL_META = SECTION_META;
export type ChannelSlug = SectionSlug;
export const CHANNEL_SLUGS = SECTION_SLUGS;

/** Legacy magazine sections → new domain. */
export const LEGACY_SECTION_TO_DOMAIN: Record<string, DomainSlug> = {
  sports: "sports",
  "movies-tv": "arts",
  music: "arts",
  culture: "culture",
  galleries: "arts",
  "cities-travel": "culture",
  games: "sports",
  business: "civics",
  books: "arts",
  tech: "science",
  // old desks
  atlas: "culture",
  history: "humanities",
  persona: "humanities",
  power: "civics",
};

/** @deprecated desk → domain */
export const LEGACY_DESK_TO_SECTION: Record<string, DomainSlug> = {
  culture: "culture",
  atlas: "culture",
  history: "humanities",
  persona: "humanities",
  power: "civics",
};

export function isDomainSlug(value: string): value is DomainSlug {
  return value in DOMAIN_META;
}

export function isSubdomainSlug(value: string): value is SubdomainSlug {
  return value in SUBDOMAIN_META;
}

export function primaryDomain(tags: string[] = []): DomainSlug {
  for (const t of tags) {
    if (isDomainSlug(t)) return t;
    if (isSubdomainSlug(t)) return SUBDOMAIN_META[t].domain;
  }
  for (const t of tags) {
    const mapped = LEGACY_SECTION_TO_DOMAIN[t];
    if (mapped) return mapped;
  }
  return "culture";
}

export function primarySubdomain(tags: string[] = []): SubdomainSlug | null {
  for (const t of tags) {
    if (isSubdomainSlug(t)) return t;
  }
  return null;
}

/** @deprecated Use primaryDomain */
export function primarySection(tags: string[] = []): DomainSlug {
  return primaryDomain(tags);
}

export function inferSection(
  slug: string,
  title: string,
  tags: string[] = [],
): DomainSlug {
  return inferTaxonomy(slug, title, tags).domain;
}

export function inferTaxonomy(
  slug: string,
  title: string,
  tags: string[] = [],
): { domain: DomainSlug; subdomain: SubdomainSlug } {
  for (const t of tags) {
    if (isSubdomainSlug(t)) {
      return { domain: SUBDOMAIN_META[t].domain, subdomain: t };
    }
  }
  for (const t of tags) {
    if (isDomainSlug(t)) {
      // domain only — pick first subdomain as soft default
      return { domain: t, subdomain: DOMAIN_META[t].subdomains[0] };
    }
  }

  const hay = `${slug} ${title} ${tags.join(" ")}`.toLowerCase();
  const rules: [RegExp, DomainSlug, SubdomainSlug][] = [
    [/\b(yankees|dodgers|padres|giant|mlb|baseball)\b/, "sports", "baseball"],
    [/\b(celtics|lakers|warrior|nba|basketball)\b/, "sports", "basketball"],
    [/\b(cowboys|patriots|nfl|super.?bowl|football)\b/, "sports", "football"],
    [/\b(soccer|premier.?league|fifa)\b/, "sports", "soccer"],
    [/\b(steam|pokemon|video.?game|gaming|board.?games|lego)\b/, "sports", "gaming"],
    [/\b(anime|film|movie|oscar|emmy|horror|franchise|disney|cinema|netflix|pixar|simpsons|streaming|imdb|tv)\b/, "arts", "film"],
    [/\b(broadway|musical|theater|theatre)\b/, "arts", "theater"],
    [/\b(music|grammy|spotify|album|song|billboard|radio|rolling.?stone|musicbrainz|beyonce|taylor)\b/, "arts", "music"],
    [/\b(lcsh|sherlock|novel|book|holmes|language|glottolog)\b/, "arts", "language"],
    [/\b(museum|heritage|gallery|architecture)\b/, "arts", "architecture"],
    [/\b(comic|design)\b/, "arts", "design"],
    [/\b(readmit|hospital|life.?expect|medicine|phd)\b/, "science", "medicine"],
    [/\b(cetacean|whale|biology)\b/, "science", "biology"],
    [/\b(nuclear|physics)\b/, "science", "physics"],
    [/\b(wastewater|engineering|hydro)\b/, "science", "engineering"],
    [/\b(web.?page|medium|tech|software)\b/, "science", "tech"],
    [/\b(caesar|emperor|roman|imperial|pantheon|history)\b/, "humanities", "history"],
    [/\b(incarceration|law|legal)\b/, "civics", "law"],
    [/\b(voter|vote|un.?vote|politics|california.?vs.?texas)\b/, "civics", "politics"],
    [/\b(tuition|college|school|education|phd)\b/, "civics", "education"],
    [/\b(ceo|business|export|wealth|big.?mac|economics|gdp)\b/, "civics", "economics"],
    [/\b(youtube|h3|super.?bowl.?ad|communication|medium)\b/, "civics", "communication"],
    [/\b(pizza|ramen|wine|beer|coffee|food|calorie|alcohol)\b/, "culture", "food"],
    [/\b(exercise|wellness)\b/, "culture", "wellness"],
    [/\b(plastic|hurricane|environment|climate)\b/, "culture", "environment"],
    [/\b(airline|biketown|park|travel|city|cities|urban|restaurant|san.?francisco|new.?york)\b/, "culture", "travel"],
    [/\b(leisure|comic)\b/, "culture", "leisure"],
  ];
  for (const [re, domain, subdomain] of rules) {
    if (re.test(hay)) return { domain, subdomain };
  }
  return { domain: "culture", subdomain: "leisure" };
}
