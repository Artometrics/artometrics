/** Masthead dateline strip — `ARTOMETRICS · {date} · DATA REPORTS`. */
export function formatHeaderDateline(now = new Date()): string {
  const date = now.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  });
  return `ARTOMETRICS · ${date} · DATA REPORTS`;
}
