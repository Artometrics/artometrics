export const TOOL_PAGES: Record<string, { title: string; body: string }> = {
  aftercare: {
    title: "Aftercare",
    body: "A private notebook for the night after: notes, tarot spreads, tracking, and small tools. Entries live on the member profile.",
  },
  "aftercare/journal": {
    title: "Aftercare journal",
    body: "Journal entries are stored for the signed-in member. This page keeps the URL.",
  },
  "aftercare/tarot": {
    title: "Aftercare tarot",
    body: "Spreads run in the signed-in tool. The static page does not deal a deck.",
  },
  "aftercare/tools": {
    title: "Aftercare tools",
    body: "The tool drawer inside Aftercare. Open it from the member app.",
  },
  "aftercare/track": {
    title: "Aftercare track",
    body: "Tracking history stays on the member profile.",
  },
  palette: {
    title: "Color Kit",
    body: "Build a palette from your own image. Analysis runs in the signed-in tool so uploads are not sent through this static host.",
  },
  "palette/analyze": {
    title: "Analyze a palette",
    body: "Upload and analysis stay in the member tool.",
  },
  samples: {
    title: "Sample Maker",
    body: "Record a sample from your own input. Takes are stored for the signed-in member.",
  },
  "samples/record": {
    title: "Record a sample",
    body: "The recorder needs the member session and is not bundled in the static site.",
  },
  twilda: {
    title: "Twilda",
    body: "Novels and a journal on the shared profile. Drafts are private to the member.",
  },
  "twilda/journal": {
    title: "Twilda journal",
    body: "Journal index for the signed-in writer.",
  },
  "twilda/reference": {
    title: "Twilda reference",
    body: "Reference shelf used while drafting. The public reference catalog is on the library.",
  },
};
