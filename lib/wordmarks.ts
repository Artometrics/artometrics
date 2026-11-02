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
