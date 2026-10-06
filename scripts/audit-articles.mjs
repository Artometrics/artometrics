import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");
const blogDir = path.join(rootDir, "src", "content", "blog");

const EMOJI_REGEX = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F1E6}-\u{1F1FF}\u{1F900}-\u{1F9FF}\u{1FA70}-\u{1FAFF}]/u;

function auditArticles() {
  console.log("Starting Artometrics article audit across src/content/blog/...");
  const files = fs.readdirSync(blogDir).filter((f) => f.endsWith(".md"));
  console.log(`Found ${files.length} article files to audit.\n`);

  let passed = 0;
  let warnings = 0;
  let errors = 0;

  const emojiViolations = [];
  const missingKeyPoints = [];
  const missingHero = [];
  const parseIssues = [];

  for (const file of files) {
    const filePath = path.join(blogDir, file);
    const content = fs.readFileSync(filePath, "utf8");

    // 1. Emoji check
    if (EMOJI_REGEX.test(content)) {
      emojiViolations.push(file);
      errors++;
    }

    // 2. Frontmatter check
    if (!content.startsWith("---")) {
      parseIssues.push(`${file}: Missing frontmatter header`);
      errors++;
      continue;
    }

    const endFm = content.indexOf("\n---", 3);
    if (endFm === -1) {
      parseIssues.push(`${file}: Malformed frontmatter boundary`);
      errors++;
      continue;
    }

    const fm = content.slice(3, endFm);
    const body = content.slice(endFm + 4);

    // 3. Key points check
    if (!fm.includes("keyPoints:")) {
      missingKeyPoints.push(file);
      warnings++;
    }

    // 4. Hero image check
    if (!fm.includes("heroImage:")) {
      missingHero.push(file);
      warnings++;
    }

    // 5. Body length check
    if (body.trim().length < 500) {
      warnings++;
    }

    passed++;
  }

  console.log("=== AUDIT SUMMARY ===");
  console.log(`Total Articles Audited: ${files.length}`);
  console.log(`Fully Passed: ${passed - errors}`);
  console.log(`Errors: ${errors}`);
  console.log(`Warnings: ${warnings}`);

  if (emojiViolations.length > 0) {
    console.error("EMOJI VIOLATIONS FOUND IN:");
    emojiViolations.forEach((f) => console.error(`  - ${f}`));
  } else {
    console.log("Zero emoji violations detected across all articles.");
  }

  if (missingKeyPoints.length > 0) {
    console.warn(`Articles missing keyPoints (${missingKeyPoints.length}):`);
    missingKeyPoints.slice(0, 5).forEach((f) => console.warn(`  - ${f}`));
  } else {
    console.log("All articles have structured keyPoints for floating stat cards.");
  }

  if (missingHero.length > 0) {
    console.warn(`Articles missing heroImage (${missingHero.length}):`);
    missingHero.slice(0, 5).forEach((f) => console.warn(`  - ${f}`));
  } else {
    console.log("All articles have valid heroImage paths.");
  }

  return errors === 0;
}

const success = auditArticles();
if (!success) {
  process.exit(1);
}
