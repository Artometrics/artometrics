import { View } from "react-native";
import { MagazineFrame } from "@/components/MagazineFrame";
import { PageSeo } from "@/components/PageSeo";
import { SeoJsonLd } from "@/components/SeoJsonLd";
import { contentsJsonLd, magazineIssues, renderContentsBody } from "@/lib/magazine";
import skinDefaults from "@/magazine/skin-defaults.json";
import type { MagSkin } from "@/lib/magazine-skins";

const issues = magazineIssues();
const defaultSkins = skinDefaults as MagSkin[];

export default function MagazineContentsScreen() {
  return (
    <View style={{ flex: 1, backgroundColor: "#0e1110" }}>
      <PageSeo
        title="Artometrics Magazine — page-flip edition"
        description="Five-minute data stories in the October 2026 page-flip reader. Choose a skin and swipe through the issue."
        path="/mag"
      />
      <SeoJsonLd data={contentsJsonLd(issues)} />
      <MagazineFrame
        pageKey="contents"
        label="Contents"
        bodyHtml={renderContentsBody(issues)}
        skins={defaultSkins}
      />
    </View>
  );
}
