import { catalogCsv } from "../../lib/sources-pages";

export function GET() {
  return new Response(catalogCsv(), { headers: { "Content-Type": "text/csv; charset=utf-8" } });
}
