import type { SectionSlug } from "./sections";

export type DatasetPack = {
  id: string;
  title: string;
  section: SectionSlug;
  status: "planned" | "collecting" | "published";
  summary: string;
  primaryKeyword: string;
  relatedReports: string[];
  sources: { name: string; url: string }[];
  downloadPath?: string;
};

/** Dataset library catalog — start thin, grow packs. */
export const DATASET_PACKS: DatasetPack[] = [
  {
    id: "movies",
    title: "Movies pack",
    section: "arts",
    status: "planned",
    summary:
      "Title-level film economics and reception joins — studios, genres, ratings, box office where licensed. One schema, clear citations.",
    primaryKeyword: "movie industry data",
    relatedReports: ["blockbusters", "franchise"],
    sources: [{ name: "Arts reports", url: "/topics/arts" }],
  },
  {
    id: "streaming-catalogs",
    title: "Streaming catalogs pack",
    section: "arts",
    status: "collecting",
    summary:
      "Availability / library-shape tables for SVOD analysis. Powers the streaming brief.",
    primaryKeyword: "streaming catalog data",
    relatedReports: ["streaming", "anime"],
    sources: [{ name: "Content OS brief", url: "/resources" }],
  },
  {
    id: "sports-franchises",
    title: "Sports franchises pack",
    section: "sports",
    status: "planned",
    summary:
      "Franchise performance, dynasties, and market gravity — packaged CSVs behind Sports section reports.",
    primaryKeyword: "sports franchise data",
    relatedReports: [
      "yankees",
      "lakers",
      "cowboys",
    ],
    sources: [{ name: "Sports reports", url: "/topics/sports" }],
  },
  {
    id: "creative-exports",
    title: "Creative exports pack",
    section: "civics",
    status: "planned",
    summary: "Country and city geopolitics / export tables used in geo-economics reports.",
    primaryKeyword: "cultural exports data",
    relatedReports: ["geopolitics", "atlas"],
    sources: [{ name: "Civics reports", url: "/topics/civics" }],
  },
  {
    id: "gutenberg-reference",
    title: "Project Gutenberg reference pack",
    section: "humanities",
    status: "published",
    summary:
      "Open-reference catalog of ~250 English-language classics (title, authors, subjects, Gutenberg URLs). Built from Gutendex or the official Gutenberg CSV feed.",
    primaryKeyword: "project gutenberg catalog",
    relatedReports: ["gutenberg", "lcsh"],
    sources: [
      { name: "Project Gutenberg", url: "https://www.gutenberg.org/" },
      { name: "Gutendex", url: "https://gutendex.com/" },
    ],
    downloadPath: "/data/reference/gutenberg/catalog.json",
  },
  {
    id: "wikiart-reference",
    title: "WikiArt / Wikimedia reference pack",
    section: "arts",
    status: "published",
    summary:
      "Curated public-domain painting references with artist, title, year, style, and Wikimedia Commons image URLs. License notes per item — verify Commons file pages before reuse.",
    primaryKeyword: "public domain art catalog",
    relatedReports: [],
    sources: [
      {
        name: "Wikimedia Commons",
        url: "https://commons.wikimedia.org/",
      },
    ],
    downloadPath: "/data/reference/wikiart/catalog.json",
  },
];

export function getDatasetPack(id: string | undefined) {
  if (!id) return undefined;
  return DATASET_PACKS.find((p) => p.id === id);
}
