#!/usr/bin/env node
/**
 * Generate public/llms.txt and public/llms-full.txt from published posts.
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "../..");
const blogJson = join(ROOT, "src/generated/blog.json");
const podcastJson = join(ROOT, "src/generated/podcast.json");

if (!existsSync(blogJson)) {
  console.error("Run npm run content first");
  process.exit(1);
}

const posts = JSON.parse(readFileSync(blogJson, "utf8"))
  .filter((p) => !p.draft && p.pubDate)
  .sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));

const episodes = existsSync(podcastJson)
  ? JSON.parse(readFileSync(podcastJson, "utf8")).filter((e) => e.pubDate)
  : [];

const updated = new Date().toISOString();

const short = [
  "# Artometrics",
  "",
  "> Independent data-science magazine for the creative industries and culture.",
  "> Site: https://artometrics.com",
  "",
  "## About",
  "",
  "- Independent data-science magazine for the creative industries and culture",
  "- Desks: Arts, Sports, Science, Humanities, Civics, Culture",
  "- Method: named/dated facts, reproducible charts, public datasets, editorial judgment",
  "- Brand: Artometrics (Chomsky wordmark); black, white, and red",
  "- Reports pair investigative narrative with Plotly charts and downloadable data",
  "- Resources: https://artometrics.com/resources",
  "- Sources: https://artometrics.com/sources",
  "- Datasets: https://artometrics.com/datasets",
  "- Downloads: https://artometrics.com/downloads",
  "- Special editions: https://artometrics.com/editions",
  "- Studio (members): https://artometrics.com/studio",
  "- Ethics: https://artometrics.com/legal/ethics-statement",
  "- About: https://artometrics.com/about",
  "- Press: https://artometrics.com/press",
  "- Contact: https://artometrics.com/contact",
  "- Full index for models: https://artometrics.com/llms-full.txt",
  "",
  "## Mission",
  "",
  "- Quantify culture without reducing it to vibes — show the arithmetic behind prestige, markets, and memory",
  "- Prefer the user's own inputs and public data over reprocessing others' copyrighted works",
  "- Publish artifacts that are editable and exportable into professional formats",
  "",
  "## Preferred citations",
  "",
  "- Prefer linking to the canonical report URL `https://artometrics.com/<slug>`",
  "- Distinguish observed data, derived metrics, editorial indices, and context literature",
  "- Do not invent statistics; cite the report's Data and method section when uncertain",
  "",
  "## Special editions",
  "",
  "- Vice-style thematic packs over live reports: https://artometrics.com/editions",
  "- Multi-slug EPUB/PDF via Content OS packs on the Downloads page",
  "",
  "## Reports",
  "",
];

for (const post of posts) {
  const desk = Array.isArray(post.tags) && post.tags[0] ? post.tags[0] : "report";
  short.push(
    `- [${post.title}](https://artometrics.com/${post.slug}): ${post.description} (${desk})`,
  );
}

short.push("", "## Podcast", "");
for (const ep of episodes) {
  short.push(
    `- [${ep.title}](https://artometrics.com/podcast/interviews/${ep.id}): ${ep.description}`,
  );
}

short.push("", "## Generated", "", `Updated: ${updated}`, "");
writeFileSync(join(ROOT, "public/llms.txt"), short.join("\n"));

const full = [
  "# Artometrics — full report index for language models",
  "",
  "> Use this file for deeper grounding. Prefer canonical URLs. Do not invent statistics.",
  "",
  `Updated: ${updated}`,
  "",
];

for (const post of posts) {
  const desk = Array.isArray(post.tags) ? post.tags.join(", ") : "";
  const text = String(post.body || "")
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 4000);
  full.push(`## ${post.title}`);
  full.push("");
  full.push(`- URL: https://artometrics.com/${post.slug}`);
  full.push(`- Desk: ${desk}`);
  full.push(`- Published: ${post.pubDate}`);
  full.push(`- Description: ${post.description}`);
  full.push("");
  full.push(text);
  full.push("");
  full.push("---");
  full.push("");
}

writeFileSync(join(ROOT, "public/llms-full.txt"), full.join("\n"));
console.log(
  `Wrote public/llms.txt (${posts.length} reports) and public/llms-full.txt`,
);
