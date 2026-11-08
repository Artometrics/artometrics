/** Page-engagement ranks. Counts come only from supplied rows. */

export const PERIODS = ["week", "month", "all"];

export const PERIOD_LABELS = {
  week: "This week",
  month: "This month",
  all: "All time",
};

export function nextPeriod(period) {
  const index = PERIODS.indexOf(period);
  return PERIODS[(index + 1) % PERIODS.length];
}

export function prevPeriod(period) {
  const index = PERIODS.indexOf(period);
  return PERIODS[(index - 1 + PERIODS.length) % PERIODS.length];
}

/** Rank 1 starts immediately. Each later rank waits another 80ms. */
export function staggerDelayMs(rank) {
  return Math.max(0, Number(rank) - 1) * 80;
}

function periodStartMs(period, now) {
  if (period === "all") return null;
  if (period === "week") return now.getTime() - 7 * 24 * 60 * 60 * 1000;
  return Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), 1);
}

/**
 * Highest engagedSessions first. Equal counts break to the newer pubDate.
 * Stories with no in-window count are left out. They are not treated as zero.
 */
export function rankDesk({ posts, rows, period, now, limit = 10 }) {
  const start = periodStartMs(period, now);
  const end = now.getTime();
  const totals = new Map();
  for (const row of rows || []) {
    const day = Date.parse(`${row.day}T00:00:00Z`);
    if (Number.isNaN(day)) continue;
    if (start != null && (day < start || day > end)) continue;
    const count = Number(row.engagedSessions);
    if (!Number.isFinite(count)) continue;
    totals.set(row.slug, (totals.get(row.slug) || 0) + count);
  }
  return (posts || [])
    .filter((post) => totals.has(post.slug))
    .map((post) => ({ ...post, engagedSessions: totals.get(post.slug) }))
    .sort((a, b) => {
      if (b.engagedSessions !== a.engagedSessions) return b.engagedSessions - a.engagedSessions;
      return new Date(b.pubDate).getTime() - new Date(a.pubDate).getTime();
    })
    .slice(0, limit)
    .map((post, index) => ({ ...post, rank: index + 1 }));
}

/** Banner lead for a period: highest count among desk leaders, newer pubDate wins a tie. */
export function pickLead(lists) {
  const tops = (lists || []).map((list) => list[0]).filter(Boolean);
  tops.sort((a, b) => {
    if (b.engagedSessions !== a.engagedSessions) return b.engagedSessions - a.engagedSessions;
    return new Date(b.pubDate).getTime() - new Date(a.pubDate).getTime();
  });
  return tops[0] || null;
}
