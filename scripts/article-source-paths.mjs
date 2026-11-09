/**
 * Canonical path map for the Drive archive worker.
 * Lists files that exist. Does not create, move, or invent paths.
 *
 *   node scripts/article-source-paths.mjs
 */
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const posts = JSON.parse(readFileSync(join(root, "src/generated/blog.json"), "utf8"));
const domains = new Set(["arts", "sports", "science", "humanities", "civics", "culture"]);
const skipDirs = new Set(["assets", "R", "tools", "styles"]);

function sectionOf(tags) {
  return (tags || []).find((tag) => domains.has(tag)) || "";
}
function subOf(tags) {
  return (tags || []).find((tag) => !domains.has(tag)) || "";
}
function walkFiles(dir) {
  if (!existsSync(dir) || !statSync(dir).isDirectory()) return [];
  const out = [];
  for (const name of readdirSync(dir)) {
    const abs = join(dir, name);
    const st = statSync(abs);
    if (st.isDirectory()) out.push(...walkFiles(abs));
    else if (st.isFile()) out.push(relative(root, abs));
  }
  return out.sort();
}
function existing(rel) {
  return existsSync(join(root, rel)) ? rel : "";
}

const rows = [];
const seen = new Set();
for (const post of posts) {
  if (post.draft || !post.pubDate || domains.has(post.slug) || seen.has(post.slug)) continue;
  seen.add(post.slug);
  const dirRel = `articles/${post.slug}`;
  const dirAbs = join(root, dirRel);
  const hasDir = existsSync(dirAbs) && statSync(dirAbs).isDirectory();
  const qmd = hasDir
    ? readdirSync(dirAbs)
        .filter((name) => name.endsWith(".qmd"))
        .map((name) => `${dirRel}/${name}`)
        .sort()
    : [];
  const publicDir = join(root, "public/images/content/articles", post.slug);
  const publicFiles = existsSync(publicDir)
    ? walkFiles(publicDir).filter((rel) => !rel.includes("/charts/"))
    : [];
  const projectImages = hasDir
    ? readdirSync(dirAbs)
        .filter((name) => /\.(png|webp|jpe?g)$/i.test(name))
        .map((name) => `${dirRel}/${name}`)
        .sort()
    : [];
  rows.push({
    slug: post.slug,
    title: post.title,
    topic: sectionOf(post.tags),
    subdomain: subOf(post.tags),
    url: `https://artometrics.com/${post.slug}`,
    articleDir: hasDir ? dirRel : "",
    qmd,
    quarto: hasDir ? existing(`${dirRel}/_quarto.yml`) : "",
    readme: hasDir ? existing(`${dirRel}/README.md`) : "",
    dataFiles: hasDir ? walkFiles(join(dirAbs, "data")) : [],
    chartsDir: hasDir && existsSync(join(dirAbs, "charts")) ? `${dirRel}/charts` : "",
    projectImages,
    publicFiles,
  });
}
rows.sort((a, b) => a.topic.localeCompare(b.topic) || a.slug.localeCompare(b.slug));

const blogSlugs = new Set(rows.map((row) => row.slug));
const extraFolders = readdirSync(join(root, "articles"))
  .filter((name) => !skipDirs.has(name) && !blogSlugs.has(name))
  .filter((name) => statSync(join(root, "articles", name)).isDirectory())
  .sort()
  .map((name) => {
    const dir = join(root, "articles", name);
    return {
      folder: `articles/${name}`,
      qmd: readdirSync(dir).filter((file) => file.endsWith(".qmd")).sort(),
    };
  });

const payload = {
  generatedFrom: "src/generated/blog.json and the articles/ and public/images/content/articles/ trees",
  purpose: "Drive archive map. Repo folders were not moved. Public URLs stay /images/content/articles/<slug>/.",
  contract: "Each published article keeps its current articles/<slug>/ folder. qmd and data paths are the files on disk. An empty list means that file is not in the repo. Do not invent a missing path.",
  canonicalCount: rows.length,
  withQmd: rows.filter((row) => row.qmd.length).length,
  withData: rows.filter((row) => row.dataFiles.length).length,
  withArticleDir: rows.filter((row) => row.articleDir).length,
  batch1TextFreeSlugs: rows.filter((row) => row.publicFiles.some((rel) => rel.endsWith("/square-plain.webp"))).map((row) => row.slug),
  articleFoldersNotInBlog: extraFolders,
  articles: rows,
};

const docs = join(root, "docs/report-assets");
mkdirSync(docs, { recursive: true });
writeFileSync(join(docs, "article-source-paths.json"), `${JSON.stringify(payload, null, 2)}\n`);

const header = [
  "slug",
  "title",
  "topic",
  "subdomain",
  "url",
  "article_dir",
  "qmd",
  "quarto",
  "readme",
  "data_files",
  "charts_dir",
  "project_images",
  "public_files",
];
const csv = [header.join(",")];
for (const row of rows) {
  const cells = [
    row.slug,
    row.title,
    row.topic,
    row.subdomain,
    row.url,
    row.articleDir,
    row.qmd.join(" | "),
    row.quarto,
    row.readme,
    row.dataFiles.join(" | "),
    row.chartsDir,
    row.projectImages.join(" | "),
    row.publicFiles.join(" | "),
  ].map((value) => `"${String(value).replaceAll('"', '""')}"`);
  csv.push(cells.join(","));
}
writeFileSync(join(docs, "article-source-paths.csv"), `${csv.join("\n")}\n`);

const artifact = "/opt/cursor/artifacts/article-source-paths";
mkdirSync(artifact, { recursive: true });
writeFileSync(join(artifact, "article-source-paths.json"), `${JSON.stringify(payload, null, 2)}\n`);
writeFileSync(join(artifact, "article-source-paths.csv"), `${csv.join("\n")}\n`);
console.log(
  `mapped ${rows.length}; qmd ${payload.withQmd}; data ${payload.withData}; dirs ${payload.withArticleDir}; extra folders ${extraFolders.length}`,
);
