/**
 * WSJ-style exhibit chrome for Quarto figures and static chart blocks.
 */

function exhibitSourceFromLive(live: HTMLElement): string | null {
  const raw =
    live.dataset.source?.trim() || live.getAttribute("data-source")?.trim();
  if (!raw) return null;
  return raw.replace(/^Data:\s*/i, "").trim();
}

function exhibitTitleFromFigure(figure: Element, live: HTMLElement | null): string {
  const cap = figure.querySelector("figcaption")?.textContent?.trim();
  if (cap) return cap;
  const aria = live?.getAttribute("aria-label")?.trim();
  if (aria) return aria;
  return "Chart";
}

function ensureExhibitHeader(figure: Element, index: number, title: string, source: string | null) {
  if (figure.querySelector(".art-exhibit__header")) return;

  const header = document.createElement("header");
  header.className = "art-exhibit__header";

  const label = document.createElement("p");
  label.className = "art-exhibit__label";
  label.textContent = `Exhibit ${index}`;

  const heading = document.createElement("h3");
  heading.className = "art-exhibit__title";
  heading.textContent = title;

  header.append(label, heading);

  if (source) {
    const sourceEl = document.createElement("p");
    sourceEl.className = "art-exhibit__source";
    sourceEl.textContent = `Source: ${source}`;
    header.appendChild(sourceEl);
  }

  figure.insertBefore(header, figure.firstChild);
  figure.classList.add("art-exhibit", "art-chart");
}

/** Number and label chart / Quarto figures under `root`. */
export function initArtExhibits(root: HTMLElement) {
  const figures = root.querySelectorAll<HTMLElement>(
    "figure.art-chart, figure:has(.art-chart-live)",
  );

  let index = 0;
  figures.forEach((figure) => {
    const live = figure.querySelector<HTMLElement>(".art-chart-live");
    if (!live && !figure.querySelector("img, svg, canvas")) return;
    index += 1;
    const title = exhibitTitleFromFigure(figure, live);
    const source = live ? exhibitSourceFromLive(live) : null;
    ensureExhibitHeader(figure, index, title, source);

    const cap = figure.querySelector("figcaption");
    if (cap && !cap.classList.contains("art-chart-caption--visible")) {
      cap.classList.add("art-chart-caption--visible", "art-exhibit__caption");
    }
  });
}
