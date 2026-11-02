import { readdirSync, readFileSync, writeFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const astroRoot = path.resolve(here, "..");
const repoRoot = path.resolve(astroRoot, "..");
const dist = path.join(astroRoot, "dist");
const site = "https://artometrics.com";

function walk(dir, acc = []) {
  for (const name of readdirSync(dir)) {
    const full = path.join(dir, name);
    if (statSync(full).isDirectory()) walk(full, acc);
    else if (name.endsWith(".html")) acc.push(full);
  }
  return acc;
}

function toUrl(file) {
  const rel = path.relative(dist, file).split(path.sep).join("/");
  if (rel === "index.html") return "/";
  if (rel.endsWith("/index.html")) return `/${rel.slice(0, -"/index.html".length)}`;
  if (rel.endsWith(".html")) return `/${rel.slice(0, -".html".length)}`;
  return `/${rel}`;
}

const ASSET_PREFIXES = ["data/", "images/", "exports/", "img/", "audios/", "css/", "fonts/", "js/"];

function isPageFile(file) {
  const rel = path.relative(dist, file).split(path.sep).join("/");
  return !ASSET_PREFIXES.some((prefix) => rel.startsWith(prefix));
}

const pages = walk(dist)
  .filter(isPageFile)
  .map(toUrl)
  .filter((url) => url !== "/404")
  .sort();

const urls = [...pages];
for (const extra of ["/rss.xml", "/podcast.xml", "/llms.txt", "/llms-full.txt"]) {
  if (!urls.includes(extra)) urls.push(extra);
}

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map((loc) => `  <url><loc>${site}${loc === "/" ? "/" : loc}</loc></url>`)
  .join("\n")}
</urlset>
`;
writeFileSync(path.join(dist, "sitemap.xml"), sitemap);

const posts = JSON.parse(readFileSync(path.join(repoRoot, "src/generated/blog.json"), "utf8"))
  .filter((post) => post.pubDate && !post.draft)
  .sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));

function esc(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const rssItems = posts
  .map(
    (post) => `    <item>
      <title>${esc(post.title)}</title>
      <link>${site}/${post.slug}</link>
      <guid isPermaLink="true">${site}/${post.slug}</guid>
      <pubDate>${new Date(post.pubDate).toUTCString()}</pubDate>
      <description>${esc(post.description)}</description>
      ${(post.tags || []).map((tag) => `<category>${esc(tag)}</category>`).join("\n      ")}
    </item>`,
  )
  .join("\n");

const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Artometrics Reports</title>
    <link>${site}</link>
    <description>Data reports on culture, power, and the creative economy — Arts, Sports, Science, Humanities, Civics, Culture.</description>
    <language>en-us</language>
${rssItems}
  </channel>
</rss>
`;
writeFileSync(path.join(dist, "rss.xml"), rss);

const episodes = JSON.parse(readFileSync(path.join(repoRoot, "src/generated/podcast.json"), "utf8"));
const podcastItems = episodes
  .map((episode) => {
    const audio = episode.audioSrc ? `<enclosure url="${site}${episode.audioSrc}" type="audio/mpeg" />` : "";
    return `    <item>
      <title>${esc(episode.title)}</title>
      <link>${site}/podcast/interviews/${episode.id}</link>
      <guid isPermaLink="true">${site}/podcast/interviews/${episode.id}</guid>
      <pubDate>${new Date(episode.pubDate).toUTCString()}</pubDate>
      <description>${esc(episode.description)}</description>
      ${audio}
    </item>`;
  })
  .join("\n");
const podcast = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>Artometrics Podcast</title>
    <link>${site}/podcast</link>
    <description>Interviews from the Artometrics desk.</description>
    <language>en-us</language>
${podcastItems}
  </channel>
</rss>
`;
writeFileSync(path.join(dist, "podcast.xml"), podcast);

const robots = `User-agent: *
Allow: /

Sitemap: ${site}/sitemap.xml
`;
writeFileSync(path.join(dist, "robots.txt"), robots);
writeFileSync(path.join(dist, "route-manifest.json"), JSON.stringify({ count: pages.length, pages }, null, 2));
console.log(`finalize: ${pages.length} html routes, sitemap + rss + podcast`);
