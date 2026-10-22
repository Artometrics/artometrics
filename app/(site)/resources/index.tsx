import { Linking, Text, View, Pressable } from "react-native";
import { Link } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";

const guides = [
  {
    title: "How to read an Artometrics report",
    body: "Start with the TL;DR and chart captions. Separate observed data, derived metrics, and editorial indices. Check limitations before quoting a number.",
  },
  {
    title: "Evidence labels",
    body: "Observed · Derived · Editorial index · Context literature — the four labels we use so artists and analysts can argue about the same claim.",
  },
  {
    title: "Mission & method",
    body: "Quantify culture without reducing it to vibes. Named/dated facts only. Prefer public datasets and the reader's own inputs. Publish editable exports.",
  },
];

const modelLinks = [
  { href: "/llms.txt", label: "/llms.txt" },
  { href: "/llms-full.txt", label: "/llms-full.txt" },
  { href: "/rss.xml", label: "/rss.xml" },
  { href: "/podcast.xml", label: "/podcast.xml" },
];

export default function ResourcesScreen() {
  return (
    <Wrapper className="gap-3.5 py-12">
      <PageSeo
        title="Resources"
        description="Guides and discovery files for Artometrics readers, journalists, and language models."
        path="/resources"
      />
      <Text className="text-[11px] tracking-[2.5px] uppercase font-semibold text-accent">
        Library
      </Text>
      <Text className="font-display text-[40px] text-fg">Resources</Text>
      <Text className="mb-2 max-w-[560px] text-base leading-6 text-muted">
        Guides for readers, analysts, and models — plus the dataset library and machine-readable
        indexes behind the reports.
      </Text>

      <View className="gap-3.5">
        {guides.map((g) => (
          <View key={g.title} className="gap-2 border-t-2 border-fg pt-3.5">
            <Text className="text-xl text-fg">{g.title}</Text>
            <Text className="text-[15px] leading-6 text-muted">{g.body}</Text>
          </View>
        ))}
        <View className="gap-2 border-t-2 border-fg pt-3.5">
          <Text className="text-xl text-fg">For language models</Text>
          <Text className="text-[15px] leading-6 text-muted">
            Prefer canonical report URLs. Do not invent statistics. Use these files for grounding:
          </Text>
          <View className="mt-1 flex-row flex-wrap gap-x-4 gap-y-2">
            {modelLinks.map((l) => (
              <Pressable key={l.href} onPress={() => Linking.openURL(l.href)}>
                <Text className="font-bold text-accent">{l.label}</Text>
              </Pressable>
            ))}
          </View>
        </View>
      </View>

      <View className="mt-4 flex-row flex-wrap gap-3">
        <Link href="/datasets" asChild>
          <Pressable className="bg-fg px-[18px] py-3">
            <Text className="text-xs font-bold uppercase tracking-[1.5px] text-inverse">
              Browse datasets
            </Text>
          </Pressable>
        </Link>
        <Link href="/downloads" asChild>
          <Pressable className="border border-border px-[18px] py-3">
            <Text className="text-xs font-bold uppercase tracking-[1.5px] text-fg">Downloads</Text>
          </Pressable>
        </Link>
        <Link href="/blog" asChild>
          <Pressable className="border border-border px-[18px] py-3">
            <Text className="text-xs font-bold uppercase tracking-[1.5px] text-fg">All reports</Text>
          </Pressable>
        </Link>
      </View>
    </Wrapper>
  );
}
