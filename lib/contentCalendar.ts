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

export type IssueWeekItem = CalendarRow & {
  kind: "this-week" | "coming";
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

/** Friday releases with `releaseFriday` in the current Mon–Sun UTC window only. */
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

  return inWeek.slice(0, limit);
}

/** Next scheduled releases after the current issue week (for “Coming”). */
export function getComingInvestigations(
  now = new Date(),
  limit = 3,
): CalendarRow[] {
  const rows = getContentCalendarRows();
  const weekStart = weekStartMondayUtc(now);
  const weekEnd = new Date(weekStart);
  weekEnd.setUTCDate(weekEnd.getUTCDate() + 7);

  return rows
    .filter((row) => parseIsoDate(row.releaseFriday) >= weekEnd)
    .sort(
      (a, b) =>
        parseIsoDate(a.releaseFriday).getTime() -
        parseIsoDate(b.releaseFriday).getTime(),
    )
    .slice(0, limit);
}

/** This week + coming rows for the home issue band (no backfill across sections). */
export function getIssueWeekBand(
  now = new Date(),
  thisWeekLimit = 3,
  comingLimit = 3,
): IssueWeekItem[] {
  const thisWeek = getThisWeekInvestigations(now, thisWeekLimit).map((row) => ({
    ...row,
    kind: "this-week" as const,
  }));
  const coming = getComingInvestigations(now, comingLimit).map((row) => ({
    ...row,
    kind: "coming" as const,
  }));
  return [...thisWeek, ...coming];
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
