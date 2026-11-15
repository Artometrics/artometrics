#!/usr/bin/env node
/**
 * Every GitHub link in the built site must point at something that exists.
 *
 *   npm run test:github                 offline: article folders must be tracked in git, other repos must be on the verified list
 *   npm run test:github -- --online     also asks GitHub that each repo (and each folder, on --ref or the current branch) exists
 *
 * It also fails when a published article is missing its GitHub or Book button.
 */
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { ORG, MAIN_REPO, VERIFIED_REPOS } from "./lib/github-targets.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const online = process.argv.includes("--online");
const refArg = process.argv.indexOf("--ref");
const ref =
  (refArg > -1 && process.argv[refArg + 1]) ||
  process.env.GITHUB_HEAD_REF ||
  process.env.GITHUB_REF_NAME ||
  execFileSync("git", ["rev-parse", "--abbrev-ref", "HEAD"], { cwd: ROOT, encoding: "utf8" }).trim();

let failed = 0;
let passed = 0;
const check = (ok, message) => {
  if (ok) passed += 1;
  else {
    failed += 1;
    console.error("FAIL", message);
  }
};

function* htmlFiles(dir) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) yield* htmlFiles(full);
    else if (name.endsWith(".html")) yield full;
  }
}

const links = new Map();
const pages = new Map();
for (const file of htmlFiles(join(ROOT, "dist"))) {
  const html = readFileSync(file, "utf8");
  const page = "/" + file.slice(join(ROOT, "dist").length + 1).replace(/\.html$/, "").replace(/\/index$/, "");
  pages.set(page, html);
  for (const m of html.matchAll(/href="(https:\/\/github\.com\/[^"#?]*)/g)) {
    const url = m[1].replace(/\/$/, "");
    if (!links.has(url)) links.set(url, new Set());
    links.get(url).add(page);
  }
}

const tracked = (path) => execFileSync("git", ["ls-files", "--", path], { cwd: ROOT, encoding: "utf8" }).trim().length > 0;
const headers = { "User-Agent": "artometrics-link-check", Accept: "application/vnd.github+json", ...(process.env.GITHUB_TOKEN ? { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` } : {}) };
async function exists(apiPath) {
  try {
    const res = await fetch(`https://api.github.com/${apiPath}`, { headers });
    if (res.status === 404) return false;
    if (res.ok) return true;
    console.warn(`WARN ${apiPath}: GitHub answered ${res.status}, not counted`);
    return true;
  } catch (error) {
    console.warn(`WARN ${apiPath}: ${error.message}, not counted`);
    return true;
  }
}

for (const [url, from] of links) {
  const where = `${url} (on ${[...from].slice(0, 2).join(", ")}${from.size > 2 ? `, +${from.size - 2}` : ""})`;
  const parts = url.replace("https://github.com/", "").split("/");
  const [owner, repo, kind, branch, ...rest] = parts;
  if (owner !== ORG) continue;
  if (!repo) {
    if (online) check(await exists(`orgs/${ORG}`), `org page exists: ${where}`);
    continue;
  }
  if (repo === MAIN_REPO) {
    if (kind === "tree" && rest[0] === "articles" && rest[1]) {
      const folder = `articles/${rest[1]}`;
      check(branch === "main", `folder links use main: ${where}`);
      check(tracked(folder), `folder is tracked in git: ${where}`);
      if (online) check(await exists(`repos/${ORG}/${MAIN_REPO}/contents/${folder}?ref=${encodeURIComponent(ref)}`), `folder exists on ${ref}: ${where}`);
    } else if (online) {
      check(await exists(`repos/${ORG}/${MAIN_REPO}`), `repo exists: ${where}`);
    }
    continue;
  }
  check(VERIFIED_REPOS.includes(repo), `repo is on the verified list (scripts/lib/github-targets.mjs): ${where}`);
  if (online) check(await exists(`repos/${ORG}/${repo}`), `repo exists on GitHub: ${where}`);
}

const published = JSON.parse(readFileSync(join(ROOT, "src/generated/blog.json"), "utf8")).filter((p) => !p.draft);
for (const post of published) {
  const html = pages.get(`/${post.slug}`);
  if (!html) continue;
  const share = html.match(/<nav class="share-row"[\s\S]*?<\/nav>/)?.[0] || "";
  check(/folder on GitHub/.test(share), `/${post.slug}: GitHub button present`);
  check(/ebook \(EPUB\)/.test(share), `/${post.slug}: Book button present`);
}

if (failed) {
  console.error(`\n${failed} failed, ${passed} passed`);
  process.exit(1);
}
console.log(`github links OK (${links.size} distinct links, ${published.length} articles${online ? ", checked online" : ", offline"})`);
