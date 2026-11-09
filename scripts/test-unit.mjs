#!/usr/bin/env node
/**
 * Lightweight unit checks (no Jest) for Aftercare calculators / planets.
 */
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { formatHeaderDate } from "../lib/headerDateline.mjs";
import { buildSourcesCatalog, loadSourcesInputs } from "./lib/sources-catalog.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

function assert(cond, msg) {
  if (!cond) {
    console.error("FAIL:", msg);
    process.exit(1);
  }
}

function reduceNumerology(sum) {
  let n = sum;
  while (n > 9 && n !== 11 && n !== 22 && n !== 33) {
    n = [...String(n)].reduce((a, c) => a + Number(c), 0);
  }
  return n;
}

function lifePathNumber(isoDate) {
  const digits = isoDate.replace(/\D/g, "");
  if (digits.length < 8) return null;
  const sum = [...digits].reduce((a, c) => a + Number(c), 0);
  return reduceNumerology(sum);
}

const LETTER = {
  a: 1, b: 2, c: 3, d: 4, e: 5, f: 6, g: 7, h: 8, i: 9,
  j: 1, k: 2, l: 3, m: 4, n: 5, o: 6, p: 7, q: 8, r: 9,
  s: 1, t: 2, u: 3, v: 4, w: 5, x: 6, y: 7, z: 8,
};

function expressionNumber(name) {
  const letters = [...name.toLowerCase()].filter((ch) => LETTER[ch] != null);
  if (!letters.length) return null;
  return reduceNumerology(letters.reduce((a, ch) => a + LETTER[ch], 0));
}

assert(lifePathNumber("1990-06-15") != null, "life path computes");
assert(expressionNumber("Juliet Ramos") != null, "expression computes");
assert(existsSync(join(ROOT, "lib/aftercare/planets.ts")), "planets.ts present");
assert(existsSync(join(ROOT, "lib/aftercare/readings.ts")), "readings.ts present");
assert(existsSync(join(ROOT, "netlify/functions/places-search.ts")), "places-search present");
assert(existsSync(join(ROOT, "netlify/functions/sanity-sync.ts")), "sanity-sync present");
assert(existsSync(join(ROOT, "lib/sanity/client.ts")), "sanity client present");
assert(existsSync(join(ROOT, "sanity/sanity.config.ts")), "sanity studio config present");
assert(existsSync(join(ROOT, "sanity/sanity.cli.ts")), "sanity cli config present");
assert(existsSync(join(ROOT, "sanity/schemas/memberContribution.ts")), "memberContribution schema");

const contentLib = readFileSync(join(ROOT, "lib/content.ts"), "utf8");
assert(contentLib.includes('@/src/generated/blog.json'), "Expo content bridge uses src/generated");
assert(!contentLib.includes("sanity.io"), "Expo content bridge does not call Sanity CDN");

const planets = readFileSync(join(ROOT, "lib/aftercare/planets.ts"), "utf8");
assert(planets.includes("SAGITTARIUS SEASON"), "season titles present");
assert(planets.includes("celestialForSign"), "celestialForSign export");

assert(existsSync(join(ROOT, "lib/samples/types.ts")), "sample maker types present");
assert(existsSync(join(ROOT, "lib/palette/recommend.ts")), "palette recommend present");
assert(existsSync(join(ROOT, "app/(site)/tools/samples/index.tsx")), "samples route present");
assert(existsSync(join(ROOT, "app/(site)/tools/palette/analyze.tsx")), "palette analyze route present");
assert(existsSync(join(ROOT, "supabase/migrations/004_studio_generators.sql")), "generators migration present");

const colorsTs = readFileSync(join(ROOT, "constants/Colors.ts"), "utf8");
assert(colorsTs.includes('BrandStyle'), "brand style type present");
assert(colorsTs.includes("magazine"), "magazine brand tokens present");

const themeTs = readFileSync(join(ROOT, "lib/theme.tsx"), "utf8");
assert(themeTs.includes('const mode: ThemeMode = "dark"'), "site theme is locked dark");
assert(themeTs.includes("DEFAULT_BRAND_STYLE"), "magazine brand is the only applied brand");
const settingsTs = readFileSync(join(ROOT, "app/(site)/settings.tsx"), "utf8");
assert(!settingsTs.includes("Light mode"), "settings has no light-mode toggle");
assert(!settingsTs.includes("Swiss"), "settings has no swiss style toggle");
const layoutTs = readFileSync(join(ROOT, "app/(site)/_layout.tsx"), "utf8");
assert(layoutTs.includes("site-document-scroll"), "document scroll is enabled outside the reader");
assert(layoutTs.includes('className="site-document"'), "web pages opt into document scroll");

const issues = JSON.parse(readFileSync(join(ROOT, "magazine/issues.json"), "utf8"));
const blog = JSON.parse(readFileSync(join(ROOT, "src/generated/blog.json"), "utf8")).filter(
  (post) => !post.draft,
);
const issueSlugs = new Set(issues.map((issue) => issue.slug));
const blogSlugs = new Set(blog.map((post) => post.slug));
assert(issues.length === 103, `expected 103 magazine issues, got ${issues.length}`);
for (const slug of blogSlugs) assert(issueSlugs.has(slug), `magazine missing blog slug ${slug}`);
for (const slug of issueSlugs) assert(blogSlugs.has(slug), `blog missing magazine slug ${slug}`);
assert(issues.every((issue) => issue.sections || issue.custom), "every issue has sections or custom body");
assert(issues.every((issue) => Array.isArray(issue.src)), "every issue has a source list");

const skinDefaults = JSON.parse(readFileSync(join(ROOT, "magazine/skin-defaults.json"), "utf8"));
assert(skinDefaults.length === 3, "three magazine skins");
assert(
  skinDefaults.map((skin) => skin.closing.name).join("|") === "The Fine Print|Back of the Box|End Credits",
  "closing box names",
);
const billboard = issues.find((issue) => issue.slug === "billboard");
assert(billboard && billboard.kp.some((point) => point.n === "1,195"), "billboard keeps the Oct 31 Hot 100 count");
assert(
  billboard.kp.some((point) => String(point.l).includes("Oct 31, 2026")),
  "billboard keeps the Oct 31 chart date",
);
const franchiseIssue = issues.find((issue) => issue.slug === "franchise");
assert(
  franchiseIssue.skins.map((skin) => skin.id).join(",") === "ledger,box,trade",
  "franchise keeps the shared skins",
);
assert(
  billboard.skins.map((skin) => skin.id).join(",") === "chart,sleeve,stream",
  "billboard skin order",
);
assert(
  billboard.skins.map((skin) => skin.closing.name).join("|") === "Chart Notes|Liner Notes|Track Info",
  "billboard closing names",
);
assert(billboard.skins[0].tokens.paper === "#F7F3EA" && billboard.skins[0].tokens.accent2 === "#E4002B", "chart tokens");
assert(billboard.skins[1].tokens.paper === "#FBF6EC" && billboard.skins[1].fonts.display === "Bungee", "sleeve tokens");
assert(billboard.skins[2].tokens.accent2 === "#12B886" && billboard.skins[2].fonts.figures === "JetBrains Mono", "stream tokens");
assert(billboard.title === "How Long Number-Ones Stay on Top", "billboard title unchanged");
assert(billboard.src.length === 4, "billboard keeps its four sources");
const streaming = issues.find((issue) => issue.slug === "streaming");
assert(
  streaming.skins.map((skin) => skin.id).join(",") === "shelf,guide,late",
  "streaming skin order",
);
assert(
  streaming.skins.map((skin) => skin.name).join("|") === "Top Shelf|Program Guide|Late Show",
  "streaming skin names",
);
assert(
  streaming.skins.map((skin) => skin.closing.name).join("|") === "Return Slip|Listings Key|After the Credits",
  "streaming closing names",
);
assert(streaming.skins[0].tokens.paper === "#F5F1E8" && streaming.skins[0].tokens.ink === "#15171C", "shelf paper and ink");
assert(streaming.skins[0].tokens.accent === "#0047FF" && streaming.skins[0].tokens.accent2 === "#D9480F", "shelf accents");
assert(streaming.skins[0].tokens.rule === "#CFC6B4", "shelf rule");
assert(
  streaming.skins[0].fonts.display === "Oswald" &&
    streaming.skins[0].fonts.body === "Source Serif 4" &&
    streaming.skins[0].fonts.figures === "IBM Plex Mono",
  "shelf fonts",
);
assert(streaming.skins[1].tokens.paper === "#FAF7F0" && streaming.skins[1].tokens.ink === "#111111", "guide paper and ink");
assert(streaming.skins[1].tokens.accent === "#0047FF" && streaming.skins[1].tokens.accent2 === "#2B8A3E", "guide accents");
assert(streaming.skins[1].tokens.rule === "#BDB6A6", "guide rule");
assert(
  streaming.skins[1].fonts.display === "Archivo" &&
    streaming.skins[1].fonts.body === "Source Serif 4" &&
    streaming.skins[1].fonts.figures === "Space Mono",
  "guide fonts",
);
assert(streaming.skins[2].tokens.paper === "#10131A" && streaming.skins[2].tokens.ink === "#E9ECF2", "late paper and ink");
assert(streaming.skins[2].tokens.accent === "#7FA2FF" && streaming.skins[2].tokens.accent2 === "#F2A900", "late accents");
assert(streaming.skins[2].tokens.rule === "#2A3040", "late rule");
assert(
  streaming.skins[2].fonts.display === "Space Grotesk" &&
    streaming.skins[2].fonts.body === "Inter" &&
    streaming.skins[2].fonts.figures === "JetBrains Mono",
  "late fonts",
);
assert(streaming.title === "Netflix's Top 10% of Titles Drew 68% of Viewing", "streaming title unchanged");
assert(streaming.src.length === 5, "streaming keeps its five sources");
assert(
  streaming.src.some((source) => String(source.text).includes("User-supplied or public streaming availability export")),
  "streaming keeps the availability src line",
);
const youtube = issues.find((issue) => issue.slug === "youtube");
assert(
  youtube.skins.map((skin) => skin.id).join(",") === "filing,gauge,onair",
  "youtube skin order",
);
assert(
  youtube.skins.map((skin) => skin.name).join("|") === "Filing|Living Room|On Air",
  "youtube skin names",
);
assert(
  youtube.skins.map((skin) => skin.closing.name).join("|") === "Notes to the Figures|Ratings Key|Show Notes",
  "youtube closing names",
);
assert(youtube.skins[0].tokens.paper === "#F8F7F2" && youtube.skins[0].tokens.ink === "#1A1D24", "filing paper and ink");
assert(youtube.skins[0].tokens.accent === "#0047FF" && youtube.skins[0].tokens.accent2 === "#B42318", "filing accents");
assert(youtube.skins[0].tokens.rule === "#C8C6BC", "filing rule");
assert(
  youtube.skins[0].fonts.display === "Archivo" &&
    youtube.skins[0].fonts.body === "Source Serif 4" &&
    youtube.skins[0].fonts.figures === "IBM Plex Mono",
  "filing fonts",
);
assert(youtube.skins[1].tokens.paper === "#F3F4F0" && youtube.skins[1].tokens.ink === "#121417", "gauge paper and ink");
assert(youtube.skins[1].tokens.accent === "#0047FF" && youtube.skins[1].tokens.accent2 === "#2F9E44", "gauge accents");
assert(youtube.skins[1].tokens.rule === "#C3C7BE", "gauge rule");
assert(
  youtube.skins[1].fonts.display === "Space Grotesk" &&
    youtube.skins[1].fonts.body === "Inter" &&
    youtube.skins[1].fonts.figures === "JetBrains Mono",
  "gauge fonts",
);
assert(youtube.skins[2].tokens.paper === "#14110F" && youtube.skins[2].tokens.ink === "#EFE9E1", "onair paper and ink");
assert(youtube.skins[2].tokens.accent === "#7FA2FF" && youtube.skins[2].tokens.accent2 === "#E8590C", "onair accents");
assert(youtube.skins[2].tokens.rule === "#2E2823", "onair rule");
assert(
  youtube.skins[2].fonts.display === "Oswald" &&
    youtube.skins[2].fonts.body === "Inter" &&
    youtube.skins[2].fonts.figures === "Space Mono",
  "onair fonts",
);
assert(youtube.title === "The Platform's $36B Engine and One Podcast's Borrowed Peak", "youtube title unchanged");
assert(youtube.src.length === 13, "youtube keeps its thirteen sources");
assert(
  youtube.src.some((source) => String(source.text).includes("YouTube ads disaggregation")),
  "youtube keeps the 10-K src line",
);
assert(
  youtube.src.some((source) => source.text === "Nielsen. Media Distributor Gauge, August 2026 (press release October 22, 2026)."),
  "youtube keeps the August 2026 src line",
);
assert(youtube.sections[1].h === "YouTube ads crossed $36B", "youtube section headings stay");
assert(
  youtube.sections[1].fig.src.endsWith("chart4_youtube_ads_revenue.png"),
  "youtube chart figure stays",
);
for (const skin of youtube.skins) {
  assert(contrastRatio(skin.tokens.ink, skin.tokens.paper) >= 4.5, `${skin.id} body contrast`);
  assert(contrastRatio(skin.tokens.accent, skin.tokens.paper) >= 4.5, `${skin.id} link contrast`);
}
assert(contrastRatio("#3A3A3A", "#F8F7F2") >= 4.5, "filing caption contrast");
assert(contrastRatio("#3A3A3A", "#F3F4F0") >= 4.5, "gauge caption contrast");
assert(contrastRatio("#C9C2B8", "#14110F") >= 4.5, "onair caption contrast");
assert(contrastRatio("#15171C", "#F6F3EC") >= 4.5, "onair chart mat text contrast");
assert(contrastRatio("#0047FF", "#F6F3EC") >= 4.5, "onair chart mat link contrast");
function channel(hex) {
  const n = parseInt(hex.slice(1), 16);
  const raw = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((value) => value / 255);
  const lin = raw.map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2];
}
function contrastRatio(a, b) {
  const hi = Math.max(channel(a), channel(b));
  const lo = Math.min(channel(a), channel(b));
  return (hi + 0.05) / (lo + 0.05);
}
for (const skin of streaming.skins) {
  assert(contrastRatio(skin.tokens.ink, skin.tokens.paper) >= 4.5, `${skin.id} body contrast`);
  assert(contrastRatio(skin.tokens.accent, skin.tokens.paper) >= 4.5, `${skin.id} link contrast`);
}
assert(contrastRatio("#3A3A3A", "#F5F1E8") >= 4.5, "shelf caption contrast");
assert(contrastRatio("#3A3A3A", "#FAF7F0") >= 4.5, "guide caption contrast");
assert(contrastRatio("#C5CAD3", "#10131A") >= 4.5, "late caption contrast");
assert(contrastRatio("#15171C", "#F6F3EC") >= 4.5, "late chart mat text contrast");
assert(contrastRatio("#0047FF", "#F6F3EC") >= 4.5, "late chart mat link contrast");
for (const issue of issues) {
  assert(Array.isArray(issue.skins) && issue.skins.length === 3, `${issue.slug} has three skins`);
  if (issue.slug === "billboard" || issue.slug === "streaming" || issue.slug === "youtube") continue;
  assert(
    issue.skins.map((skin) => skin.id).join(",") === "ledger,box,trade",
    `${issue.slug} skin order`,
  );
}
const skinSource = readFileSync(join(ROOT, "lib/magazine-skins.ts"), "utf8");
assert(skinSource.includes("artometrics-mag-skin:"), "skin choice is stored per issue");
assert(skinSource.includes("data-for"), "closing names switch with the skin");
assert(skinSource.includes("resolveSkinId"), "skin ids resolve before they are applied");
assert(skinSource.includes('new Set(["ledger", "box", "trade"])'), "retired billboard skins are named");
assert(skinSource.includes("Updated through: chart dated Oct 31, 2026"), "billboard chart date line");
assert(skinSource.includes("Artometrics Billboard report illustration."), "billboard hero credit");
assert(skinSource.includes("How Long Number-Ones Stay on Top"), "billboard title treatment keeps the headline");
assert(skinSource.includes('slug === "streaming"'), "streaming retires the shared skins");
assert(skinSource.includes('slug === "youtube"'), "youtube retires the shared skins");
assert(skinSource.includes("Updated through: Nielsen Gauge, August 2026 (press release October 22, 2026)"), "youtube updated line");
assert(skinSource.includes("The Platform's $36B Engine and One Podcast's Borrowed Peak"), "youtube title treatment keeps the headline");
assert(skinSource.includes("YouTube ads, FY2024"), "filing revenue row label");
assert(skinSource.includes("$36,147 million"), "filing revenue row total");
assert(skinSource.includes("of U.S. TV-screen time, August 2026 (Nielsen Gauge)"), "living room share label");
assert(skinSource.includes("ON AIR"), "on air lamp");
assert(skinSource.includes("the borrowed peak"), "on air peak label");
assert(skinSource.includes("Updated through: weeks ending June 28, 2026"), "streaming updated line");
assert(skinSource.includes("Netflix's Top 10% of Titles Drew 68% of Viewing"), "streaming title treatment keeps the headline");
assert(skinSource.includes("JAN–JUN 2026"), "program guide time slot");
assert(skinSource.includes("top 10% of titles"), "late show scrubber label");
const frame = readFileSync(join(ROOT, "components/MagazineFrame.web.tsx"), "utf8");
assert(frame.includes('data-skin'), "reader root carries data-skin");
assert(frame.includes("localStorage"), "picker remembers the skin");
const magJs = readFileSync(join(ROOT, "public/mag.js"), "utf8");
assert(magJs.includes("location.search"), "page turns keep ?skin=");
assert(magJs.includes("mag-page"), "magazine pages are discrete scroll containers");
assert(readFileSync(join(ROOT, "public/css/mag.css"), "utf8").includes(".mag-page"), "magazine page scroll css");
const skinCss = readFileSync(join(ROOT, "public/css/mag-skins.css"), "utf8");
assert(skinCss.includes('[data-skin="ledger"]'), "ledger skin css");
assert(skinCss.includes('[data-skin="box"]'), "box skin css");
assert(skinCss.includes('[data-skin="trade"]'), "trade skin css");
assert(skinCss.includes('[data-skin="chart"]'), "chart skin css");
assert(skinCss.includes('[data-skin="sleeve"]'), "sleeve skin css");
assert(skinCss.includes('[data-skin="stream"]'), "stream skin css");
assert(skinCss.includes('[data-skin="shelf"]'), "shelf skin css");
assert(skinCss.includes('[data-skin="guide"]'), "guide skin css");
assert(skinCss.includes('[data-skin="late"]'), "late skin css");
assert(skinCss.includes('[data-skin="filing"]'), "filing skin css");
assert(skinCss.includes('[data-skin="gauge"]'), "gauge skin css");
assert(skinCss.includes('[data-skin="onair"]'), "onair skin css");
assert(skinCss.includes("67.9%"), "late scrubber stops at 67.9%");
assert(skinCss.includes("15.8%"), "living room share bar stops at 15.8%");
assert(skinCss.includes("#F6F3EC"), "late charts sit on a light mat");
assert(!skinCss.includes("#E50914"), "skins do not use Netflix red");
assert(!skinCss.includes("#FF0000"), "skins do not use YouTube red");
assert(!/filter:\s*invert/.test(skinCss), "chart pngs are not inverted");
assert(skinCss.includes("prefers-reduced-motion"), "skins keep a reduced-motion path");
assert(frame.includes("resolveSkinId"), "reader uses the skin resolver");
assert(
  frame.includes('id === "shelf"') && frame.includes('id === "guide"') && frame.includes('id === "late"'),
  "picker draws the streaming skins",
);
assert(
  frame.includes('id === "filing"') && frame.includes('id === "gauge"') && frame.includes('id === "onair"'),
  "picker draws the youtube skins",
);
for (const font of ["archivo-latin.woff2", "bungee-latin.woff2", "space-grotesk-latin.woff2", "jetbrains-mono-latin.woff2"]) {
  const bytes = readFileSync(join(ROOT, "public/fonts/skins", font));
  assert(bytes.toString("ascii", 0, 4) === "wOF2", `${font} is a woff2`);
}
for (const plate of ["pacioli.jpg", "toy-shop.jpg", "belasco-box-office.jpg"]) {
  const bytes = readFileSync(join(ROOT, "public/images/skins", plate));
  assert(bytes[0] === 0xff && bytes[1] === 0xd8, `${plate} is a jpeg`);
}

const htmlShell = readFileSync(join(ROOT, "app/+html.tsx"), "utf8");
assert(!htmlShell.includes("noindex"), "+html must not ship noindex");
assert(htmlShell.includes('content="index, follow"'), "+html asks crawlers to index");
const netlify = readFileSync(join(ROOT, "netlify.toml"), "utf8");
assert(!netlify.includes("noindex"), "netlify must not send noindex");
const firebase = readFileSync(join(ROOT, "firebase.json"), "utf8");
assert(!firebase.includes("noindex"), "firebase hosting must not send noindex");
const robots = readFileSync(join(ROOT, "public/robots.txt"), "utf8");
assert(!/Disallow:\s*\//.test(robots), "robots.txt must allow crawling");
assert(robots.includes("Sitemap: https://artometrics.com/sitemap.xml"), "robots points at sitemap");
assert(existsSync(join(ROOT, "public/sitemap.xml")), "sitemap.xml present");
assert(existsSync(join(ROOT, "public/llms.txt")), "llms.txt present");
assert(existsSync(join(ROOT, "public/rss.xml")), "rss.xml present");
assert(readFileSync(join(ROOT, "public/css/mag.css"), "utf8").includes("#0047ff"), "house blue");
assert(readFileSync(join(ROOT, "public/css/mag.css"), "utf8").includes("#0e1110"), "magazine ground is the dark house");
assert(readFileSync(join(ROOT, "public/css/mag.css"), "utf8").includes(".mag-page"), "magazine page scroll css stays");
const ebookCard = readFileSync(join(ROOT, "components/MagazineEditionCard.tsx"), "utf8");
assert(ebookCard.includes("Read as ebook"), "ebook entry is labeled Read as ebook");
assert(ebookCard.includes("magazineIssueHref"), "ebook entry opens the page-flip issue");
const home = readFileSync(join(ROOT, "site/pages/index.astro"), "utf8");
assert(!home.includes("home-c"), "home is not the narrow home column");
assert(!home.includes("desk-nav"), "home does not put the section strip back");
assert(home.includes("DeskHome"), "home is the desk-sections front page");
const deskHome = readFileSync(join(ROOT, "site/components/DeskHome.astro"), "utf8");
assert(deskHome.includes('"geopolitics"'), "the home banner includes the geopolitics report");
assert(!deskHome.includes("All reports"), "the All reports heading is gone from the front page");
assert(readFileSync(join(ROOT, "lib/site-nav.ts"), "utf8").includes('href: "/blog"'), "the report index stays in the menu");
assert(deskHome.includes('["dodgers", "padres", "celtics", "steam"]'), "Sports is four reports, with Steam last");
assert(deskHome.includes('["pixar", "anime", "franchise", "simpsons"]'), "Arts is four reports");
assert(deskHome.includes('["nuclear", "cetaceans", "readmitted", "wastewater"]'), "Science is four reports and skips Longevity");
assert(deskHome.includes('["wine", "coffee", "ramen", "pizza"]'), "Culture is four reports");
assert(!deskHome.includes('"longevity"'), "Longevity is not a homepage story");
assert(deskHome.includes('"atlas"'), "Atlas stays a homepage story");
const hosting = JSON.parse(readFileSync(join(ROOT, "firebase.json"), "utf8"));
const steal = hosting.hosting.redirects.filter((rule) => rule.source === "/atlas" || rule.source === "/atlas/**");
assert(steal.length === 0, "the Atlas article path is not sent to a topic");
assert(
  hosting.hosting.redirects.some((rule) => rule.source === "/culture" && rule.destination === "/topics/culture"),
  "the culture topic redirect stays",
);
assert(
  hosting.hosting.redirects.some((rule) => rule.source === "/desks/atlas" && rule.destination === "/topics/culture"),
  "the old desk path /desks/atlas still opens Culture",
);
assert(
  hosting.hosting.redirects.some((rule) => rule.source === "/national-export-identity-atlas" && rule.destination === "/atlas"),
  "the long Atlas alias still points at the article",
);
assert(
  hosting.hosting.redirects.some((rule) => rule.source === "/export-atlas" && rule.destination === "/atlas"),
  "the export-atlas alias still points at the article",
);
assert(!netlify.includes('from = "/atlas"\n'), "Netlify does not redirect the Atlas article to a topic");
assert(netlify.includes('from = "/desks/atlas"'), "Netlify still redirects the old desk path");
assert(readFileSync(join(ROOT, "src/content/blog/atlas.md"), "utf8").includes("slug: atlas"), "Atlas is a real article");
assert(deskHome.includes('["dodgers", "padres", "celtics", "steam"]'), "Sports keeps Dodgers, Padres, Celtics, and Steam");
assert(deskHome.includes("story-grid"), "stories below the banner are a square grid");
assert(!deskHome.includes("desk-rail"), "the story grid does not slide sideways");
assert(!deskHome.includes(">Week<"), "Week is not a homepage control");
assert(!deskHome.includes(">Month<"), "Month is not a homepage control");
assert(!deskHome.includes(">All time<"), "All time is not a homepage control");
assert(!deskHome.includes("data-front-view"), "period switches are gone");
assert(!deskHome.includes("Editorial selection"), "the editorial line is not on the page");
assert(deskHome.includes("story-tile"), "category stories use the square tiles");
assert(!deskHome.includes("desk-dial"), "the nine-shortcut grid is gone from the home page");
assert(!deskHome.includes("Home shortcuts"), "the phone shortcut nav is gone");
for (const label of ["Magazine", "Podcast", "Library", "Editions"]) {
  assert(!deskHome.includes(`label: "${label}"`), `${label} is not a home shortcut`);
}
assert(!deskHome.includes("OPTION 2"), "the mockup caption is not part of the page");
const deskCss = readFileSync(join(ROOT, "site/styles/site.css"), "utf8");
assert(!deskCss.includes("desk-dial"), "shortcut-grid styles are gone");
const reportPage = readFileSync(join(ROOT, "site/pages/[slug].astro"), "utf8");
assert(!reportPage.includes("Read as ebook"), "report pages do not show the ebook link");
assert(!reportPage.includes("report-hero"), "report pages do not render the hero figure");
assert(reportPage.includes('class="franchise-banner"'), "franchise article shows the wide banner once");
assert(reportPage.includes("/images/content/articles/franchise/cover.png"), "franchise article keeps the still cover");
assert(reportPage.includes('src="/videos/franchise-cover.mp4"'), "franchise article plays the approved cover video");
assert(reportPage.includes("muted") && reportPage.includes("playsinline") && reportPage.includes("loop"), "cover video is a silent inline loop");
assert(reportPage.includes('href="/mag/franchise"'), "magazine link stays separate from the video");
assert(!reportPage.includes('<a class="franchise-cover"'), "the cover video is not wrapped in the magazine link");
const bannerAt = reportPage.indexOf('class="franchise-banner"');
const titleAt = reportPage.indexOf("<h1>");
const articleBodyAt = reportPage.indexOf('class="artometrics-article-body"');
const coverAt = reportPage.indexOf('class="franchise-cover"');
assert(bannerAt >= 0 && titleAt > bannerAt, "banner precedes the article title");
assert(coverAt > articleBodyAt, "magazine cover follows the article body");
assert((reportPage.match(/<figure class="franchise-banner">/g) || []).length === 1, "banner appears once");
assert((reportPage.match(/<figure class="franchise-cover">/g) || []).length === 1, "cover appears once");
const previewCss = readFileSync(join(ROOT, "site/styles/preview.css"), "utf8");
assert(previewCss.includes("prefers-reduced-motion: reduce"), "reduced motion shows the still cover");
assert(
  readFileSync(join(ROOT, "src/content/blog/franchise.md"), "utf8").includes(
    "heroImage: /images/content/articles/franchise/banner.png",
  ),
  "franchise hero is the approved wide banner",
);
function sha256(file) {
  return createHash("sha256").update(readFileSync(file)).digest("hex");
}
assert(
  sha256(join(ROOT, "public/images/content/articles/franchise/banner.png")) ===
    "a9b0daafcc33fe8ccf77f3b1e62d3c07402823c4056240ca8702bda76030dbd0",
  "franchise banner bytes match the supplied PNG",
);
assert(
  sha256(join(ROOT, "public/images/content/articles/franchise/cover.png")) ===
    "db805d90be71dbfeb3962cc23feab879e7cc3f5317fc9fd28b847bceeb935386",
  "franchise cover bytes match the supplied PNG",
);
assert(
  sha256(join(ROOT, "public/videos/franchise-cover.mp4")) ===
    "d10f9d323d290a7e29e58b40a37defc57d7a12d1604e36b659207d4d7e68e731",
  "franchise cover video bytes match the supplied MP4",
);
assert(reportPage.includes("withStaticCharts"), "report pages keep the chart pipeline");
assert(reportPage.includes('post.slug === "longevity"'), "only longevity mounts the branded chart");
const header = readFileSync(join(ROOT, "site/components/Header.astro"), "utf8");
assert(header.includes("formatHeaderDate()"), "dateline is the date only");
assert(!header.includes("formatHeaderDateline"), "production header does not repeat the old dateline");
assert(!header.includes('class="desk-nav"'), "section buttons stay in the menu, not a second strip");
assert(header.includes('id="nav-search"'), "search stays inside the menu");
assert(!header.includes('aria-label="Search reports"'), "the header search icon is gone");
assert(header.includes("nav-catalogue"), "the menu can show catalogue covers");
assert(!header.includes("PDF not packed"), "missing PDFs are not labeled as packed");
assert(header.includes('anime: "/exports/anime.pdf"'), "anime catalogue links its PDF");
assert(header.includes('data-logo-form-choice="single"'), "the logo picker can show singles");
assert(header.includes(">Wordmarks<"), "the logo picker can show wordmarks");
assert(header.includes('["franchise", "Franchise"]'), "catalogue includes the Franchise cover");
assert(header.includes('["anime", "Anime"]'), "catalogue includes the Anime city-collage cover");
assert(header.includes("cover.webp"), "catalogue covers use the portrait role files");
assert(deskHome.includes("square-text.webp"), "story tiles use the square image that already includes its title");
assert(!deskHome.includes("reportKicker"), "tiles do not paint a second title over the square");
assert(readFileSync(join(ROOT, "site/components/BannerCarousel.astro"), "utf8").includes("banner-art.webp"), "banners use the banner-art files");
assert(deskHome.includes('["geopolitics", "franchise", "dodgers"]'), "the home banner is three reports from different desks");
assert(!readFileSync(join(ROOT, "site/styles/site.css"), "utf8").includes(".nav-overlay--keyboard .nav-catalogue { display: none; }"), "the cover shelf is not removed when the keyboard opens");
const magIndex = readFileSync(join(ROOT, "site/pages/mag/index.astro"), "utf8");
assert(magIndex.includes("layouts/Base.astro"), "magazine home uses the site chrome");
assert(!magIndex.includes("layouts/Mag.astro"), "magazine home is not the page-flip reader");
assert(magIndex.includes("/mag/${post.slug}"), "featured issues open the reader");
const topicPage = readFileSync(join(ROOT, "site/pages/topics/[channel].astro"), "utf8");
assert(topicPage.includes("BannerCarousel"), "category pages open with a banner carousel");
assert(topicPage.includes("DeskBoard"), "category pages use story columns");
assert(!topicPage.includes("ReportIndex"), "category pages are not the archive table");
assert(existsSync(join(ROOT, "public/images/content/articles/anime/hero.webp")), "the notebook Anime image is kept");
assert(existsSync(join(ROOT, "public/images/content/articles/anime/alternates/notebook-light-table.webp")), "the notebook Anime alternate is kept");
assert(readFileSync(join(ROOT, "firebase.json"), "utf8").includes("max-age=0, must-revalidate"), "HTML revalidates instead of staying fresh for an hour");
const assetManifest = readFileSync(join(ROOT, "docs/report-assets/manifest-all.csv"), "utf8");
assert(assetManifest.includes("UPSCALED"), "the asset manifest marks upscaled files");
assert(!/UPSCALED[^\n]*native hi-res/i.test(assetManifest), "upscaled assets are not described as native hi-res");
assert(deskHome.includes("story-tile"), "front page uses story cover buttons");
assert(!deskHome.includes("Hot"), "Hot is not a homepage control");
assert(!deskHome.includes("Trending"), "Trending is not a homepage control");
assert(header.includes('id="close-menu"'), "Close is in the menu");
assert(header.indexOf('id="close-menu"') < header.indexOf('id="nav-search"'), "Close comes before the search field");
assert(header.indexOf('id="nav-search"') < header.indexOf('id="nav-clear"'), "Clear comes after the search field");
assert(home.includes('footer="none"'), "the front page does not render the footer bumper");
assert(reportPage.includes('footer="article"'), "report pages keep their footer");
assert(header.includes('href="/about"'), "About stays in the menu");
assert(header.includes('href="/legal/ethics-statement"'), "Legal stays in the menu");
assert(header.includes('href="/sources"'), "Sources stays in the menu");
assert(header.includes('href="/rss.xml"'), "RSS stays in the menu");
const siteCss = readFileSync(join(ROOT, "site/styles/site.css"), "utf8");
assert(!/html\[data-theme="light"\] \.wordmark__plate\s*\{[^}]*background/.test(siteCss), "day mode does not put a black plate behind the wordmark");
assert(!siteCss.includes(".appearance__logos button {\n  height: 44px;\n  padding: 4px 6px;\n  border: 1px solid transparent;\n  background: #000;"), "wordmark choices are not painted on black squares");
const baseLayout = readFileSync(join(ROOT, "site/layouts/Base.astro"), "utf8");
assert(baseLayout.includes("monograms.halftone.night"), "default tab icon is the pink-purple single A");
assert(baseLayout.includes('id="mono-map"'), "tab icon follows the stored wordmark");
assert(!baseLayout.includes('href="/favicon.svg"'), "tab icon is not the black-backed svg");
assert(header.includes("appearance__mono"), "each wordmark shows its matching A");
assert(header.includes("paintIcon"), "choosing a wordmark updates the tab icon");
for (const id of ["white", "svg", "halftone", "d01", "d02", "d03", "d04", "d05", "d06", "d07", "d08"]) {
  assert(existsSync(join(ROOT, `public/images/brand/monograms/${id}-night-32.png`)), `${id} night A exists`);
  assert(existsSync(join(ROOT, `public/images/brand/monograms/${id}-day-32.png`)), `${id} day A exists`);
}
const wordmarks = readFileSync(join(ROOT, "lib/wordmarks.ts"), "utf8");
assert(wordmarks.includes('DEFAULT_WORDMARK_ID = "halftone"'), "the default mark is the pink-purple single A");
const logoReview = wordmarks.slice(wordmarks.indexOf("export const LOGO_REVIEW"));
assert(logoReview.includes('src: "/images/brand/wordmarks/wordmark-white.webp"'), "stripe review uses the diagonal pink/blue file");
assert(logoReview.includes('src: "/images/brand/wordmarks/wordmark-03-pink-blue-bands.webp"'), "halftone review uses the pink dotted file");
assert(!logoReview.includes("wordmark-halftone.webp"), "review does not use the misnamed halftone file");
assert(logoReview.includes('cover: "/images/brand/review/franchise-stripes.png"'), "stripe review points at the striped cover file");
assert(logoReview.includes('cover: "/images/brand/review/franchise-halftone.png"'), "halftone review points at the pink-halftone cover file");
assert(
  sha256(join(ROOT, "public/images/brand/review/franchise-stripes.png")) ===
    "e0402f0716c6f40d931c8acc00ceb659ae2fd58bd3417b3eb4871eadfef79712",
  "striped cover bytes match the supplied PNG",
);
assert(
  sha256(join(ROOT, "public/images/brand/review/franchise-halftone.png")) ===
    "279171ebcfd949c46068d54b8d0e9fc564194d05c1c9a2b921d060962a3c3d10",
  "pink halftone cover bytes match the supplied PNG",
);
assert(baseLayout.includes('data-logo-form="wordmark"'), "the header defaults to the full wordmark");
assert(header.includes("wordmark-halftone.webp"), "the default wordmark is the pink-purple Artometrics");
assert(baseLayout.includes("square-art.webp"), "search results can use report art without a baked title");
assert(baseLayout.includes('review ? "noindex, nofollow"'), "logo review routes stay out of the index");
const footer = readFileSync(join(ROOT, "site/components/Footer.astro"), "utf8");
assert(footer.includes("CONFIGURED_SOCIAL"), "footer can link the published GitHub URL");
assert(footer.includes("showSocial ? UNCONFIGURED_SOCIAL"), "unconfigured social labels stay off production");
assert(readFileSync(join(ROOT, "site/lib/plotly-bars.ts"), "utf8").includes('!== "75.6"'), "longevity chart guards the published Hong Kong value");
assert(existsSync(join(ROOT, "site/pages/design-preview/files.astro")), "filed-files preview exists");
assert(existsSync(join(ROOT, "site/pages/design-preview/citations.astro")), "citation preview exists");
assert(existsSync(join(ROOT, "site/pages/design-preview/reference.astro")), "reference preview exists");
assert(readFileSync(join(ROOT, "site/pages/datasets/index.astro"), "utf8").includes("DATASET_PACKS"), "live datasets page is unchanged in role");
assert(readFileSync(join(ROOT, "lib/headerDateline.mjs"), "utf8").includes('timeZone: "America/Los_Angeles"'), "masthead date uses Pacific time");
assert(readFileSync(join(ROOT, "lib/headerDateline.ts"), "utf8").includes('from "./headerDateline.mjs"'), "TypeScript dateline re-exports the tested module");
const beforePacific = formatHeaderDate(new Date("2026-11-07T07:30:00.000Z"));
const afterPacific = formatHeaderDate(new Date("2026-11-07T08:30:00.000Z"));
assert(beforePacific.includes("Fri") && beforePacific.includes("Nov 6"), `7:30 UTC is still Nov 6 in Los Angeles, got ${beforePacific}`);
assert(afterPacific.includes("Sat") && afterPacific.includes("Nov 7"), `8:30 UTC is Nov 7 in Los Angeles, got ${afterPacific}`);
assert(readFileSync(join(ROOT, "site/layouts/Preview.astro"), "utf8").includes('robots="noindex, nofollow"'), "catalog previews stay noindex");
assert(readFileSync(join(ROOT, "site/pages/design-preview/files.astro"), "utf8").includes("Filter reports"), "file filter names the records");
assert(readFileSync(join(ROOT, "site/lib/preview-catalog.ts"), "utf8").includes("120px-"), "reference thumbs use a Commons 120px size");
const reportScreen = readFileSync(join(ROOT, "app/(site)/[slug].tsx"), "utf8");
const ebookAt = reportScreen.indexOf("<MagazineEditionCard");
const bodyAt = reportScreen.indexOf("<ArticleBody");
assert(ebookAt > 0 && bodyAt > ebookAt, "ebook entry sits above the report body");
assert(!reportScreen.includes("view=magazine"), "articles have no magazine view toggle");
assert(!reportScreen.includes("MagazineFrame"), "articles render the report, not the page-flip");
assert(readFileSync(join(ROOT, "lib/magazine-skins.ts"), "utf8").includes('READER_PAPER = "#0e1110"'), "reader surface is dark");
assert(existsSync(join(ROOT, "public/mag.js")), "mag.js present");
assert(existsSync(join(ROOT, "public/logo.png")), "magazine logo present");

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    const stat = statSync(full);
    if (stat.isDirectory()) walk(full, out);
    else out.push({ full, size: stat.size });
  }
  return out;
}
const masters = walk(join(ROOT, "data/masters"));
const oversize = masters.filter((file) => file.size >= 50 * 1024 * 1024);
assert(oversize.length === 0, `master files over 50MB must stay out of git: ${oversize.map((f) => f.full).join(", ")}`);
assert(masters.some((file) => file.full.endsWith("artometrics_masters.sqlite")), "sqlite index present");
assert(masters.some((file) => file.full.includes("CHANGELOG_2026-10-29.md")), "changelog present");
assert(masters.some((file) => file.full.includes("dataset_inventory_2026-10-29.csv")), "inventory present");

const sourcesRoute = readFileSync(join(ROOT, "app/(site)/sources/index.tsx"), "utf8");
assert(sourcesRoute.includes("no link yet"), "unlinked citations are tagged");
assert(sourcesRoute.includes('path="/sources"'), "sources page sets a canonical path");
const resources = readFileSync(join(ROOT, "app/(site)/resources/index.tsx"), "utf8");
assert(resources.includes('href="/sources"'), "resources links to sources");
const sitemapScript = readFileSync(join(ROOT, "scripts/content-os/generate-sitemap.mjs"), "utf8");
assert(sitemapScript.includes('"/sources"'), "sitemap generator lists /sources");
assert(readFileSync(join(ROOT, "public/llms.txt"), "utf8").includes("https://artometrics.com/sources"), "llms.txt lists sources");
assert(readFileSync(join(ROOT, "docs/sources-page.md"), "utf8").includes("# Decided"), "decided note recorded");

const { issues: sourceIssues, packs } = loadSourcesInputs(ROOT);
const freshSources = buildSourcesCatalog(sourceIssues, packs);
const committedSources = JSON.parse(readFileSync(join(ROOT, "src/generated/sources.json"), "utf8"));
assert(
  JSON.stringify(freshSources) === JSON.stringify(committedSources),
  "src/generated/sources.json is stale — run npm run sources",
);
assert(freshSources.orphanFixes.length === 0, "every data fix has a parent issue");
assert(freshSources.topics.map((topic) => topic.id).join(",") === "arts,sports,science,humanities,civics,culture", "topics follow the site order");
const listed = freshSources.topics.flatMap((topic) => topic.issues);
assert(listed.length === 100, `expected 100 parent reports, got ${listed.length}`);
assert(listed.every((issue) => !issue.slug.endsWith("-data-fix")), "data fixes are not top-level rows");
const anime = listed.find((issue) => issue.slug === "anime");
assert(anime && anime.updatedThrough === "Updated through October 11, 2026", "anime uses the snapshot coverage end");
assert(anime.fixes.length === 1 && anime.fixes[0].slug === "anime-data-fix", "anime data fix sits under anime");
assert(anime.datasets.some((pack) => pack.id === "streaming-catalogs"), "anime links its dataset pack");
const padres = listed.find((issue) => issue.slug === "padres");
assert(padres && padres.fixes.some((fix) => fix.slug === "padres-data-fix"), "padres data fix sits under padres");
const franchise = listed.find((issue) => issue.slug === "franchise");
assert(franchise && franchise.datasets.some((pack) => pack.id === "movies"), "franchise links the movies pack");
assert(franchise.fixes.some((fix) => fix.slug === "franchise-data-fix"), "franchise data fix sits under franchise");
const coffee = listed.find((issue) => issue.slug === "coffee");
assert(coffee && coffee.datasets.length === 0, "reports without a pack do not invent a dataset link");
const albums = listed.find((issue) => issue.slug === "albums");
assert(albums && albums.updatedThroughKind === "unchecked", "albums says not yet checked");
const pantheon = listed.find((issue) => issue.slug === "pantheon");
assert(pantheon && pantheon.updatedThrough === "Updated through: editorial index", "pantheon says it is an editorial index");
const geopolitics = listed.find((issue) => issue.slug === "geopolitics");
assert(geopolitics && geopolitics.updatedThroughKind === "editorial", "geopolitics says it is an editorial index");
const gutenberg = listed.find((issue) => issue.slug === "gutenberg");
assert(gutenberg && gutenberg.datasets.some((pack) => pack.id === "gutenberg-reference"), "gutenberg links its pack");
let sawUnlinked = false;
for (const issue of listed) {
  for (const citation of issue.citations) {
    assert(citation.href === null || /^https?:\/\//i.test(citation.href), `${issue.slug} citation href`);
    if (citation.href === null) sawUnlinked = true;
  }
  for (const fix of issue.fixes) {
    for (const citation of fix.citations) {
      assert(citation.href === null || /^https?:\/\//i.test(citation.href), `${fix.slug} citation href`);
    }
  }
}
assert(sawUnlinked, "at least one citation is unlinked");
const catalogText = JSON.stringify(freshSources);
assert(!/sk_live|api_key|BEGIN (RSA |OPENSSH )?PRIVATE/i.test(catalogText), "sources catalog has no secrets");

const funFacts = JSON.parse(readFileSync(join(ROOT, "lib/nav-fun-facts.json"), "utf8"));
assert(funFacts.length >= 40 && funFacts.length <= 60, `fun facts should be 40–60, got ${funFacts.length}`);
const factHrefs = new Map();
for (const topic of committedSources.topics) {
  for (const issue of topic.issues) {
    factHrefs.set(
      issue.slug,
      new Set((issue.citations || []).map((citation) => citation.href).filter(Boolean)),
    );
  }
}
const factTexts = new Set();
for (const fact of funFacts) {
  assert(fact.text && /[.!?]$/.test(fact.text), `fact needs a sentence: ${fact.slug}`);
  assert(fact.text.length <= 180, `fact is too long: ${fact.slug}`);
  assert(!factTexts.has(fact.text), `duplicate fact: ${fact.text}`);
  factTexts.add(fact.text);
  const articlePath = join(ROOT, "src/content/blog", `${fact.slug}.md`);
  assert(existsSync(articlePath), `fact report missing: ${fact.slug}`);
  const article = readFileSync(articlePath, "utf8");
  assert(article.includes(fact.anchor), `fact anchor missing in ${fact.slug}: ${fact.anchor}`);
  const cited = factHrefs.get(fact.slug);
  assert(
    (cited && cited.has(fact.sourceHref)) || article.includes(fact.sourceHref),
    `fact source is not cited by ${fact.slug}`,
  );
}
assert(readFileSync(join(ROOT, "lib/nav-fun-fact.ts"), "utf8").includes("Math.random"), "facts rotate randomly");

console.log("unit OK");
