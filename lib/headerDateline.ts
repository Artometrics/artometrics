/** Date token shared by the production dateline and the preview strip. */
export function formatHeaderDate(now = new Date()): string {
  return now.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

/** Masthead dateline strip — `ARTOMETRICS · {date} · DATA REPORTS`. */
export function formatHeaderDateline(now = new Date()): string {
  return `ARTOMETRICS · ${formatHeaderDate(now)} · DATA REPORTS`;
}
