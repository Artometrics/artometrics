import { SOURCE_ENTRIES } from "../../lib/sources-pages";

export function GET() {
  const body = SOURCE_ENTRIES.map((entry) => ({
    slug: entry.slug,
    title: entry.title,
    desk: entry.topic.title,
    updatedThrough: entry.updatedThrough,
    report: `https://artometrics.com${entry.href}`,
    sources: `https://artometrics.com/sources/${entry.slug}`,
    citations: entry.issue.citations,
  }));
  return new Response(JSON.stringify(body, null, 2), { headers: { "Content-Type": "application/json; charset=utf-8" } });
}
