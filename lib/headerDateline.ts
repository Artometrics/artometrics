/** Masthead “today” strip. Pacific time, so a UTC server does not roll the date at 4pm PT. */
export function formatHeaderDate(now = new Date()): string {
  return now.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "America/Los_Angeles",
  });
}

/** Masthead dateline strip — `ARTOMETRICS · {date} · DATA REPORTS`. */
export function formatHeaderDateline(now = new Date()): string {
  return `ARTOMETRICS · ${formatHeaderDate(now)} · DATA REPORTS`;
}
