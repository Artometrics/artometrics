/** Header wordmarks. `white` is the default white-face extrude. */
export type WordmarkOption = {
  id: string;
  label: string;
  src: string;
};

export const WORDMARKS: WordmarkOption[] = [
  { id: "white", label: "White face", src: "/images/brand/wordmarks/wordmark-white.webp" },
  { id: "svg", label: "White vector", src: "/images/brand/wordmarks/wordmark-white.svg" },
  { id: "halftone", label: "Pink halftone", src: "/images/brand/wordmarks/wordmark-halftone.webp" },
  { id: "d01", label: "Dotted extrude", src: "/images/brand/wordmarks/wordmark-01-dotted-extrude.webp" },
  { id: "d02", label: "Dotted long shadow", src: "/images/brand/wordmarks/wordmark-02-dotted-long-shadow.webp" },
  { id: "d03", label: "Pink and blue bands", src: "/images/brand/wordmarks/wordmark-03-pink-blue-bands.webp" },
  { id: "d04", label: "Dot ring", src: "/images/brand/wordmarks/wordmark-04-dot-ring.webp" },
  { id: "d05", label: "Fade-in dots", src: "/images/brand/wordmarks/wordmark-05-dots-fade.webp" },
  { id: "d06", label: "Blue dots on pink", src: "/images/brand/wordmarks/wordmark-06-blue-on-pink.webp" },
  { id: "d07", label: "Blue lip", src: "/images/brand/wordmarks/wordmark-07-blue-lip.webp" },
  { id: "d08", label: "Riso misregister", src: "/images/brand/wordmarks/wordmark-08-riso.webp" },
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
