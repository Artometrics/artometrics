export type ToolKind =
  | "hub"
  | "journal"
  | "tarot"
  | "calm"
  | "track"
  | "palette"
  | "samples"
  | "drafts"
  | "reference";

export interface ToolPage {
  title: string;
  body: string;
  kind: ToolKind;
  /** localStorage namespace for tools that keep data on the device. */
  store?: string;
  parent?: string;
}

/**
 * Studio tools run in the browser. Nothing is uploaded and nobody has to sign in;
 * whatever you make stays on this device until you export it.
 */
export const TOOL_PAGES: Record<string, ToolPage> = {
  aftercare: {
    title: "Aftercare",
    body: "A private notebook for the night after: notes, tarot spreads, tracking, and small calming tools. Everything stays on this device.",
    kind: "hub",
  },
  "aftercare/journal": {
    title: "Aftercare journal",
    body: "Write it down while it is still loud. Entries are saved in this browser and can be exported any time.",
    kind: "journal",
    store: "aftercare-journal",
    parent: "aftercare",
  },
  "aftercare/tarot": {
    title: "Aftercare tarot",
    body: "Draw one card or a three-card spread from a full 78-card deck. Save a reading to your journal if it lands.",
    kind: "tarot",
    parent: "aftercare",
  },
  "aftercare/tools": {
    title: "Aftercare tools",
    body: "A breathing pacer and a five-senses grounding checklist for when the evening is too much.",
    kind: "calm",
    parent: "aftercare",
  },
  "aftercare/track": {
    title: "Aftercare track",
    body: "A thirty-second daily check-in: mood, energy, sleep. Watch the pattern build over time, then export it as CSV.",
    kind: "track",
    store: "aftercare-track",
    parent: "aftercare",
  },
  palette: {
    title: "Color Kit",
    body: "Pull a palette from your own image. The picture is analysed in your browser and never uploaded.",
    kind: "palette",
  },
  "palette/analyze": {
    title: "Analyze a palette",
    body: "Drop an image, pick how many colors, and export the kit as CSS, JSON, or an SVG swatch strip.",
    kind: "palette",
    parent: "palette",
  },
  samples: {
    title: "Sample Maker",
    body: "Record a sound with your microphone or load your own audio file, shape it, and export a WAV. It all happens in your browser.",
    kind: "samples",
  },
  "samples/record": {
    title: "Record a sample",
    body: "Hit record, make a sound, trim and shape the take, then export it as a WAV file.",
    kind: "samples",
    parent: "samples",
  },
  twilda: {
    title: "Twilda",
    body: "A drafting desk for novels and long pieces. Drafts autosave in this browser; export Markdown or text when you are ready.",
    kind: "drafts",
    store: "twilda-drafts",
  },
  "twilda/journal": {
    title: "Twilda journal",
    body: "A writer's journal beside the drafts. Entries stay on this device and export any time.",
    kind: "journal",
    store: "twilda-journal",
    parent: "twilda",
  },
  "twilda/reference": {
    title: "Twilda reference",
    body: "Keep a reference shelf of quotes, links, and notes while drafting. The public reference catalog lives in the library.",
    kind: "reference",
    store: "twilda-reference",
    parent: "twilda",
  },
};
