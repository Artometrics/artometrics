import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dist = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../dist");
const firebase = JSON.parse(readFileSync(path.resolve(dist, "../../firebase.json"), "utf8"));
const redirects = new Map();
for (const rule of firebase.hosting.redirects || []) {
  if (!rule.source.includes("*")) redirects.set(rule.source.replace(/\/$/, "") || "/", rule.destination);
}

function walk(dir, acc = []) {
  for (const name of readdirSync(dir)) {
    const full = path.join(dir, name);
    if (statSync(full).isDirectory()) walk(full, acc);
    else if (name.endsWith(".html")) acc.push(full);
  }
  return acc;
}

function fileFor(urlPath) {
  const clean = urlPath.split("#")[0].split("?")[0];
  if (!clean || clean.startsWith("mailto:") || clean.startsWith("tel:")) return null;
  let pathname = clean;
  if (pathname.startsWith("http")) {
    try {
      const u = new URL(pathname);
      if (u.hostname !== "artometrics.com" && u.hostname !== "www.artometrics.com") return null;
      pathname = u.pathname;
    } catch {
      return null;
    }
  }
  if (!pathname.startsWith("/")) return "skip-relative";
  pathname = pathname.replace(/\/$/, "") || "/";
  if (redirects.has(pathname)) return "redirect";
  const candidates = [];
  if (pathname === "/") candidates.push(path.join(dist, "index.html"));
  else {
    candidates.push(path.join(dist, pathname.slice(1), "index.html"));
    candidates.push(path.join(dist, `${pathname.slice(1)}.html`));
    const ext = path.extname(pathname);
    if (ext) candidates.push(path.join(dist, pathname.slice(1)));
  }
  return candidates.some((file) => existsSync(file)) ? "ok" : pathname;
}

const ASSET_PREFIXES = ["data/", "images/", "exports/", "img/", "audios/", "css/", "fonts/", "js/"];
const pages = walk(dist).filter((file) => {
  const rel = path.relative(dist, file).split(path.sep).join("/");
  return !ASSET_PREFIXES.some((prefix) => rel.startsWith(prefix));
});
const missing = [];
const hrefRe = /\b(?:href|src)="([^"]+)"/g;
for (const file of pages) {
  const html = readFileSync(file, "utf8");
  let match;
  while ((match = hrefRe.exec(html))) {
    const href = match[1];
    if (href.startsWith("#") || href.startsWith("data:") || href.startsWith("javascript:")) continue;
    const result = fileFor(href);
    if (result && result !== "ok" && result !== "redirect" && result !== "skip-relative") {
      missing.push(`${path.relative(dist, file)} -> ${href}`);
    }
  }
}

const manifest = JSON.parse(readFileSync(path.join(dist, "route-manifest.json"), "utf8"));
const posts = JSON.parse(readFileSync(path.resolve(dist, "../../src/generated/blog.json"), "utf8"));
const absentPosts = posts.filter((post) => !manifest.pages.includes(`/${post.slug}`)).map((post) => post.slug);

console.log(`pages ${manifest.count}`);
console.log(`broken internal links ${missing.length}`);
console.log(`reports missing a route ${absentPosts.length}`);
if (missing.length) console.log(missing.slice(0, 40).join("\n"));
if (absentPosts.length) console.log(absentPosts.join(", "));
if (missing.length || absentPosts.length) process.exit(1);
console.log("link check ok");
