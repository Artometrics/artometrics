import { Text, View } from "react-native";
import { Link } from "expo-router";
import {
  DOMAIN_META,
  SUBDOMAIN_META,
  primaryDomain,
  primarySubdomain,
  type DomainSlug,
  type SubdomainSlug,
} from "@/data/sections";

type Props = {
  tags: string[] | undefined;
};

export function ReportBreadcrumb({ tags }: Props) {
  if (!tags?.length) {
    return (
      <View className="flex-row flex-wrap items-center gap-x-1.5 gap-y-1">
        <Link href="/blog">
          <Text className="font-sans text-[13px] font-semibold uppercase tracking-[1.4px] text-accent md:text-sm">
            Reports
          </Text>
        </Link>
      </View>
    );
  }

  const domain = primaryDomain(tags) as DomainSlug;
  const sub = primarySubdomain(tags) as SubdomainSlug | null;
  const domainTitle = DOMAIN_META[domain]?.title ?? domain;
  const subTitle = sub && SUBDOMAIN_META[sub] ? SUBDOMAIN_META[sub].title : null;

  const crumbs: { label: string; href?: `/blog` | `/topics/${string}` }[] = [
    { label: "Reports", href: "/blog" },
    { label: domainTitle, href: `/topics/${domain}` },
  ];
  if (subTitle) {
    crumbs.push({
      label: subTitle,
      href: `/blog?subdomain=${sub}` as `/blog`,
    });
  }

  return (
    <View className="flex-row flex-wrap items-center gap-x-1.5 gap-y-1">
      {crumbs.map((crumb, i) => (
        <View key={`${crumb.label}-${i}`} className="flex-row items-center gap-1.5">
          {i > 0 ? (
            <Text className="font-sans text-[13px] text-subtle md:text-sm">·</Text>
          ) : null}
          {crumb.href ? (
            <Link href={crumb.href}>
              <Text className="font-sans text-[13px] font-semibold uppercase tracking-[1.4px] text-accent md:text-sm">
                {crumb.label}
              </Text>
            </Link>
          ) : (
            <Text className="font-sans text-[13px] font-semibold uppercase tracking-[1.4px] text-subtle md:text-sm">
              {crumb.label}
            </Text>
          )}
        </View>
      ))}
    </View>
  );
}
