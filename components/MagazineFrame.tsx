import { ScrollView, Text, View } from "react-native";
import { Link } from "expo-router";

type Props = {
  pageKey: string;
  label: string;
  bodyHtml: string;
  skins?: { id: string; name: string }[];
};

function htmlToText(html: string) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/(p|h1|h2|h3|li|div|figure)>/gi, "\n")
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

/** Native fallback. The column page-flip runs on web (`MagazineFrame.web.tsx`). */
export function MagazineFrame({ label, bodyHtml }: Props) {
  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: "#ffffff" }}
      contentContainerStyle={{ paddingHorizontal: 22, paddingTop: 28, paddingBottom: 48 }}
    >
      <View style={{ flexDirection: "row", justifyContent: "space-between", marginBottom: 16 }}>
        <Link href="/">
          <Text style={{ color: "#0047FF", fontSize: 12, letterSpacing: 1.4, fontWeight: "700" }}>
            CONTENTS
          </Text>
        </Link>
        <Link href="/blog">
          <Text style={{ color: "#0047FF", fontSize: 12, letterSpacing: 1.4, fontWeight: "700" }}>
            SITE
          </Text>
        </Link>
      </View>
      <Text style={{ color: "#6b6b6b", fontSize: 12, letterSpacing: 1.6, marginBottom: 12 }}>
        {label.toUpperCase()}
      </Text>
      <Text style={{ color: "#111111", fontSize: 18, lineHeight: 28 }}>{htmlToText(bodyHtml)}</Text>
    </ScrollView>
  );
}
