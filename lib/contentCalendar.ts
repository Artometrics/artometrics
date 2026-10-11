/**
 * Friday release schedule — built from docs/content-os/content-calendar.csv via `npm run content`.
 */
import calendarData from "@/src/generated/content-calendar.json";

export type CalendarRow = {
  releaseFriday: string;
  slug: string;
  title: string;
  desk: string;
  subdomain: string;
};

function parseIsoDate(iso: string): Date {
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d));
}

/** Monday 00:00 UTC of the ISO week containing `date`. */
function weekStartMondayUtc(date: Date): Date {
  const d = new Date(date);
  const day = d.getUTCDay();
  const diff = day === 0 ? -6 : 1 - day;
  d.setUTCDate(d.getUTCDate() + diff);
  d.setUTCHours(0, 0, 0, 0);
  return d;
}

export function getContentCalendarRows(): CalendarRow[] {
  return calendarData as CalendarRow[];
}

/**
 * Up to `limit` investigations for the current issue week (Mon–Sun UTC),
 * preferring Friday releases in that window; fills from nearest upcoming if sparse.
 */
export function getThisWeekInvestigations(
  now = new Date(),
  limit = 3,
): CalendarRow[] {
  const rows = getContentCalendarRows();
  const weekStart = weekStartMondayUtc(now);
  const weekEnd = new Date(weekStart);
  weekEnd.setUTCDate(weekEnd.getUTCDate() + 7);

  const inWeek = rows.filter((row) => {
    const release = parseIsoDate(row.releaseFriday);
    return release >= weekStart && release < weekEnd;
  });

  const picked: CalendarRow[] = [];
  const seen = new Set<string>();
  for (const row of inWeek) {
    if (seen.has(row.slug)) continue;
    seen.add(row.slug);
    picked.push(row);
    if (picked.length >= limit) return picked;
  }

  const upcoming = rows
    .filter((row) => parseIsoDate(row.releaseFriday) >= weekStart)
    .sort(
      (a, b) =>
        parseIsoDate(a.releaseFriday).getTime() -
        parseIsoDate(b.releaseFriday).getTime(),
    );

  for (const row of upcoming) {
    if (seen.has(row.slug)) continue;
    seen.add(row.slug);
    picked.push(row);
    if (picked.length >= limit) break;
  }

  return picked;
}

export function formatIssueWeekLabel(now = new Date()): string {
  const start = weekStartMondayUtc(now);
  const end = new Date(start);
  end.setUTCDate(end.getUTCDate() + 6);
  const fmt = (d: Date) =>
    d.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      timeZone: "UTC",
    });
  return `Week of ${fmt(start)}–${fmt(end)}, ${start.getUTCFullYear()}`;
}
