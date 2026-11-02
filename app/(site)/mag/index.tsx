import { View } from "react-native";
import { MagazineFrame } from "@/components/MagazineFrame";
import { PageSeo } from "@/components/PageSeo";
import { SeoJsonLd } from "@/components/SeoJsonLd";
import { contentsJsonLd, magazineIssues, renderContentsBody } from "@/lib/magazine";
import skinDefaults from "@/magazine/skin-defaults.json";
import { withHouseSkin, type MagSkin } from "@/lib/magazine-skins";
import { House } from "@/constants/Colors";

const issues = magazineIssues();
const defaultSkins = withHouseSkin(skinDefaults as MagSkin[]);

export default function MagazineContentsScreen() {
  return (
    <View style={{ flex: 1, backgroundColor: House.groundDeep }}>
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
