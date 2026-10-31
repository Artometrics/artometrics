import { Link } from "expo-router";
import { Text, View } from "react-native";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { magazineEditionHref } from "@/lib/magazine";

const steps = ["🔎 Find data", "🧪 Audit", "🗄️ SQL", "📊 Charts", "✍️ Story"];
const issues = [
  { href: magazineEditionHref("", "ledger"), label: "📄 Data Minimal" },
  { href: magazineEditionHref("", "box"), label: "📄 Glossy Editorial" },
  { href: magazineEditionHref("", "trade"), label: "📄 Indie Zine" },
];
const log = [
  ["2026-10-23", "Lab log + magazine PDFs"],
  ["2026-10-21", "Style Lab house style"],
  ["2026-10-14", "Editor's picks redesign, a11y"],
  ["2026-10-12", "Franchise Kore narration; Anime clean ledger + charts"],
];

export default function LabLogScreen() {
  return (
    <Wrapper variant="narrow" className="gap-3 py-12">
      <PageSeo title="Lab log" description="How Artometrics is made, plus a dated log." path="/lab-log" />
      <Text className="text-xs font-bold uppercase tracking-[1.8px] text-accent">Lab log</Text>
      <Text role="heading" aria-level={1} className="font-display text-[36px] text-fg">How it's made</Text>
      <View className="flex-row flex-wrap gap-2">
        {steps.map((s) => (
          <Text key={s} className="rounded-full border border-accent px-3 py-1 font-serif text-base text-fg">{s}</Text>
        ))}
      </View>
      <Text className="mt-3 font-serif text-[22px] font-bold text-fg">🛠️ Tools</Text>
      <Text className="font-serif text-base leading-[26px] text-muted">
        Expo · Plotly · R · DuckDB · Quarto · Gemini TTS · Firebase
      </Text>
      <Text className="mt-3 font-serif text-[22px] font-bold text-fg">📰 Issues</Text>
      <View className="gap-2">
        {issues.map((a) => (
          <Link key={a.href} href={a.href}>
            <Text className="font-serif text-base text-accent">{a.label}</Text>
          </Link>
        ))}
      </View>
      <Text className="mt-3 font-serif text-[22px] font-bold text-fg">🗓️ Log</Text>
      <View className="gap-1">
        {log.map(([d, t]) => (
          <Text key={d} className="font-serif text-base text-muted"><Text className="font-bold text-fg">{d}</Text>  {t}</Text>
        ))}
      </View>
    </Wrapper>
  );
}
