/** Header wordmarks. `white` is the default white-face extrude. */
export type WordmarkOption = {
  id: string;
  label: string;
  src: string;
  /** Single A for a dark browser tab. White face kept. */
  monoNight: string;
  /** Single A for a light browser tab. Near-white face recoloured to ink. */
  monoDay: string;
  appleNight: string;
  appleDay: string;
};

function monogram(id: string) {
  return {
    monoNight: `/images/brand/monograms/${id}-night-32.png`,
    monoDay: `/images/brand/monograms/${id}-day-32.png`,
    appleNight: `/images/brand/monograms/${id}-night-180.png`,
    appleDay: `/images/brand/monograms/${id}-day-180.png`,
  };
}

export const WORDMARKS: WordmarkOption[] = [
  { id: "white", label: "White face", src: "/images/brand/wordmarks/wordmark-white.webp", ...monogram("white") },
  { id: "svg", label: "White vector", src: "/images/brand/wordmarks/wordmark-white.svg", ...monogram("svg") },
  { id: "halftone", label: "Pink halftone", src: "/images/brand/wordmarks/wordmark-halftone.webp", ...monogram("halftone") },
  { id: "d01", label: "Dotted extrude", src: "/images/brand/wordmarks/wordmark-01-dotted-extrude.webp", ...monogram("d01") },
  { id: "d02", label: "Dotted long shadow", src: "/images/brand/wordmarks/wordmark-02-dotted-long-shadow.webp", ...monogram("d02") },
  { id: "d03", label: "Pink and blue bands", src: "/images/brand/wordmarks/wordmark-03-pink-blue-bands.webp", ...monogram("d03") },
  { id: "d04", label: "Dot ring", src: "/images/brand/wordmarks/wordmark-04-dot-ring.webp", ...monogram("d04") },
  { id: "d05", label: "Fade-in dots", src: "/images/brand/wordmarks/wordmark-05-dots-fade.webp", ...monogram("d05") },
  { id: "d06", label: "Blue dots on pink", src: "/images/brand/wordmarks/wordmark-06-blue-on-pink.webp", ...monogram("d06") },
  { id: "d07", label: "Blue lip", src: "/images/brand/wordmarks/wordmark-07-blue-lip.webp", ...monogram("d07") },
  { id: "d08", label: "Riso misregister", src: "/images/brand/wordmarks/wordmark-08-riso.webp", ...monogram("d08") },
];

export const DEFAULT_WORDMARK_ID = "white";

/**
 * Review-only pair. Filenames do not describe the artwork.
 * Confirmed by looking at the pixels, not the names:
 * - stripes: wordmark-white.webp — long diagonal pink/blue extrusion, white face.
 * - halftone: wordmark-03-pink-blue-bands.webp — bright-pink dotted extrusion, blue accents.
 * wordmark-halftone.webp is a short blue-rim bevel. It is neither of these.
 * catalogId is the existing picker id that already points at that file.
 */
export const LOGO_REVIEW = {
  stripes: {
    id: "stripes",
    catalogId: "white",
    label: "Stripes",
    src: "/images/brand/wordmarks/wordmark-white.webp",
    file: "wordmark-white.webp",
    width: 600,
    height: 139,
    cover: "/images/brand/review/franchise-stripes.png",
    coverFile: "franchise-ebook-v5-logo-STRIPED-even-border-nowhite.png",
    coverWidth: 1600,
    coverHeight: 2133,
  },
  halftone: {
    id: "halftone",
    catalogId: "d03",
    label: "Pink halftone",
    src: "/images/brand/wordmarks/wordmark-03-pink-blue-bands.webp",
    file: "wordmark-03-pink-blue-bands.webp",
    width: 600,
    height: 140,
    cover: "/images/brand/review/franchise-halftone.png",
    coverFile: "franchise-ebook-v5-logo-PINK-HALFTONE-even-border-nowhite.png",
    coverWidth: 1600,
    coverHeight: 2133,
  },
} as const;

export type LogoReviewMark = keyof typeof LOGO_REVIEW;
