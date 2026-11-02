import { Text } from "react-native";
import { Link } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";

export default function MethodologyScreen() {
  return (
    <Wrapper variant="narrow" className="gap-3.5 py-12">
      <PageSeo
        title="Methodology"
        description="How Artometrics separates observed data, derived metrics, and editorial judgment, and where the sources live."
        path="/methodology"
      />
      <Text className="text-xs font-bold uppercase tracking-[1.8px] text-accent">Method</Text>
      <Text role="heading" aria-level={1} className="font-display text-[34px] leading-10 text-fg">
        Methodology and source library
      </Text>
      <Text className="font-serif text-base leading-7 text-muted">
        Reports name the dataset, the date it was pulled, and the cleaning choices that change a
        number. Observed facts, derived metrics, and editorial indices are labeled separately so a
        reader can argue with the claim without guessing which kind of sentence it is.
      </Text>
      <Text className="font-serif text-base leading-7 text-muted">
        Charts and tables are built from public sources or from files the reader supplies. Each
        report lists those sources in its back matter. The grouped citation catalog is on the{" "}
        <Link href="/sources">
          <Text className="text-accent underline">sources</Text>
        </Link>{" "}
        page. Editorial standards are in the{" "}
        <Link href="/legal/ethics-statement">
          <Text className="text-accent underline">ethics statement</Text>
        </Link>
        .
      </Text>
      <Text className="font-serif text-base leading-7 text-muted">
        Exports (HTML, PDF, EPUB, CSV) are the record. If a figure and the prose disagree, the
        figure&apos;s source note wins until a correction is published.
      </Text>
    </Wrapper>
  );
}
