#!/usr/bin/env node
/**
 * Lightweight unit checks (no Jest) for Aftercare calculators / planets.
 */
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

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
assert(themeTs.includes("artometrics-brand-style"), "brand style persistence key");
assert(themeTs.includes("toggleBrandStyle"), "brand style toggle");

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
for (const issue of issues) {
  assert(Array.isArray(issue.skins) && issue.skins.length === 3, `${issue.slug} has three skins`);
  assert(
    issue.skins.map((skin) => skin.id).join(",") === "ledger,box,trade",
    `${issue.slug} skin order`,
  );
}
const skinSource = readFileSync(join(ROOT, "lib/magazine-skins.ts"), "utf8");
assert(skinSource.includes("artometrics-mag-skin:"), "skin choice is stored per issue");
assert(skinSource.includes("data-for"), "closing names switch with the skin");
const frame = readFileSync(join(ROOT, "components/MagazineFrame.web.tsx"), "utf8");
assert(frame.includes('data-skin'), "reader root carries data-skin");
assert(frame.includes("localStorage"), "picker remembers the skin");
const magJs = readFileSync(join(ROOT, "public/mag.js"), "utf8");
assert(magJs.includes("location.search"), "page turns keep ?skin=");
assert(readFileSync(join(ROOT, "public/css/mag-skins.css"), "utf8").includes('[data-skin="ledger"]'), "ledger skin css");
assert(readFileSync(join(ROOT, "public/css/mag-skins.css"), "utf8").includes('[data-skin="box"]'), "box skin css");
assert(readFileSync(join(ROOT, "public/css/mag-skins.css"), "utf8").includes('[data-skin="trade"]'), "trade skin css");
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

console.log("unit OK");
