import { useCallback, useMemo, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  Text,
  TextInput,
  View,
} from "react-native";
import { useFocusEffect } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { ToolsSubnav } from "@/components/tools/ToolsSubnav";
import { StudioBreadcrumb } from "@/components/studio/StudioBreadcrumb";
import { StudioDateField, StudioTimeField } from "@/components/studio/StudioDateField";
import { StudioPlaceField } from "@/components/studio/StudioPlaceField";
import { StudioSelect } from "@/components/studio/StudioSelect";
import { PrimaryButton } from "@/components/PrimaryButton";
import { useTheme } from "@/lib/theme";
import { useRequireAuth } from "@/lib/tools/requireAuth";
import { apiFetch } from "@/lib/supabase/client";
import { listTimezones } from "@/lib/studio/timezones";
import {
  ageFromBirthDate,
  birthdayInsight,
  lifePathNumber,
  moonPhaseApprox,
  nameNumbers,
  nextBirthday,
  sunSignFromDate,
} from "@/lib/aftercare/calculators";
import {
  expressionReading,
  lifePathReading,
  personalityReading,
  soulUrgeReading,
  sunSignReading,
  type NumberReading,
  type SunReading,
} from "@/lib/aftercare/readings";
import { celestialForSign } from "@/lib/aftercare/planets";
import { PlanetPoster } from "@/components/aftercare/PlanetPoster";
import { CosmicChartCard } from "@/components/aftercare/CosmicChartCard";

const NAV = [
  { href: "/tools/aftercare", label: "Home" },
  { href: "/tools/aftercare/journal", label: "Journal" },
  { href: "/tools/aftercare/tarot", label: "Tarot" },
  { href: "/tools/aftercare/track", label: "Track" },
  { href: "/tools/aftercare/tools", label: "Birth tools" },
];

type Profile = {
  display_name?: string | null;
  birth_date?: string | null;
  birth_time?: string | null;
  birth_place?: string | null;
  timezone?: string | null;
};

export default function AftercareBirthToolsScreen() {
  const { colors } = useTheme();
  const { user, ready } = useRequireAuth();
  const [displayName, setDisplayName] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [birthTime, setBirthTime] = useState("");
  const [birthPlace, setBirthPlace] = useState("");
  const [timezone, setTimezone] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedMsg, setSavedMsg] = useState<string | null>(null);
  const [openReading, setOpenReading] = useState<string | null>("lifePath");

  const tzOptions = useMemo(
    () => listTimezones().map((tz) => ({ value: tz, label: tz.replace(/_/g, " ") })),
    [],
  );

  const validDate = /^\d{4}-\d{2}-\d{2}$/.test(birthDate.trim());
  const insight = useMemo(
    () => (validDate ? birthdayInsight(birthDate.trim()) : null),
    [birthDate, validDate],
  );
  const sunSign = useMemo(
    () => (validDate ? sunSignFromDate(birthDate.trim()) : null),
    [birthDate, validDate],
  );
  const lifePath = useMemo(
    () => (validDate ? lifePathNumber(birthDate.trim()) : null),
    [birthDate, validDate],
  );
  const nextBday = useMemo(
    () => (validDate ? nextBirthday(birthDate.trim()) : null),
    [birthDate, validDate],
  );
  const age = useMemo(
    () => (validDate ? ageFromBirthDate(birthDate.trim()) : null),
    [birthDate, validDate],
  );
  const moon = useMemo(() => moonPhaseApprox(), []);
  const names = useMemo(() => nameNumbers(displayName), [displayName]);

  const readings = useMemo(() => {
    const cards: {
      id: string;
      badge: string;
      reading: NumberReading | SunReading | null;
      kind: "number" | "sun";
    }[] = [
      {
        id: "lifePath",
        badge: lifePath != null ? `Life Path ${lifePath}` : "Life Path",
        reading: lifePathReading(lifePath),
        kind: "number",
      },
      {
        id: "sun",
        badge: sunSign ? `Sun · ${sunSign}` : "Sun sign",
        reading: sunSignReading(sunSign),
        kind: "sun",
      },
      {
        id: "expression",
        badge:
          names.expression != null ? `Expression ${names.expression}` : "Expression",
        reading: expressionReading(names.expression),
        kind: "number",
      },
      {
        id: "soulUrge",
        badge: names.soulUrge != null ? `Soul Urge ${names.soulUrge}` : "Soul Urge",
        reading: soulUrgeReading(names.soulUrge),
        kind: "number",
      },
      {
        id: "personality",
        badge:
          names.personality != null
            ? `Personality ${names.personality}`
            : "Personality",
        reading: personalityReading(names.personality),
        kind: "number",
      },
    ];
    return cards;
  }, [lifePath, sunSign, names]);

  const load = useCallback(async () => {
    if (!user) return;
    try {
      const res = await apiFetch("aftercare-profile");
      const data = (await res.json().catch(() => ({}))) as {
        profile?: Profile;
        error?: string;
      };
      if (!res.ok) {
        setError(data.error || "Could not load birth profile.");
        return;
      }
      const p = data.profile;
      setDisplayName(p?.display_name ?? "");
      setBirthDate(p?.birth_date ?? "");
      setBirthTime(p?.birth_time ?? "");
      setBirthPlace(p?.birth_place ?? "");
      setTimezone(p?.timezone ?? "");
      setError(null);
    } catch {
      setError("Could not load birth profile.");
    }
  }, [user]);

  useFocusEffect(
    useCallback(() => {
      if (!ready || !user) return;
      let active = true;
      (async () => {
        try {
          setLoading(true);
          await load();
        } finally {
          if (active) setLoading(false);
        }
      })();
      return () => {
        active = false;
      };
    }, [load, ready, user]),
  );

  async function onSave() {
    setSaving(true);
    setError(null);
    setSavedMsg(null);
    try {
      const res = await apiFetch("aftercare-profile", {
        method: "PUT",
        body: JSON.stringify({
          displayName: displayName.trim() || undefined,
          birthDate: birthDate.trim() || undefined,
          birthTime: birthTime.trim() || undefined,
          birthPlace: birthPlace.trim() || undefined,
          timezone: timezone.trim() || undefined,
        }),
      });
      const data = (await res.json().catch(() => ({}))) as {
        profile?: Profile;
        error?: string;
      };
      if (!res.ok) {
        setError(data.error || "Could not save profile.");
        return;
      }
      if (data.profile) {
        setDisplayName(data.profile.display_name ?? "");
        setBirthDate(data.profile.birth_date ?? "");
        setBirthTime(data.profile.birth_time ?? "");
        setBirthPlace(data.profile.birth_place ?? "");
        setTimezone(data.profile.timezone ?? "");
      }
      setSavedMsg("Profile saved.");
    } catch {
      setError("Could not save profile.");
    } finally {
      setSaving(false);
    }
  }

  if (!ready) {
    return (
      <Wrapper className="gap-2.5 py-8 flex-1">
        <Text className="text-muted">Loading…</Text>
      </Wrapper>
    );
  }

  const badgeParts = [
    names.expression != null ? `Expression ${names.expression}` : null,
    names.soulUrge != null ? `Soul Urge ${names.soulUrge}` : null,
    lifePath != null ? `Life Path ${lifePath}` : null,
  ].filter(Boolean);

  return (
    <Wrapper className="gap-2.5 py-8 flex-1">
      <PageSeo
        title="Birth tools · Aftercare"
        description="Birth profile and reflective calculators on Artometrics Aftercare."
        path="/tools/aftercare/tools"
      />
      <ToolsSubnav links={NAV} />
      <StudioBreadcrumb
        items={[
          { label: "Studio", href: "/studio" },
          { label: "Aftercare", href: "/tools/aftercare" },
          { label: "Birth tools" },
        ]}
      />
      <Text className="font-sans text-[36px] font-bold text-fg">Birth tools</Text>
      <Text className="font-sans text-base leading-[26px] max-w-[640px] text-muted">
        Name numbers, life path, and sun notes — reflective tools, not science, medical, or
        financial advice.
      </Text>

      {loading ? (
        <ActivityIndicator color={colors.accent} style={{ marginTop: 16 }} />
      ) : (
        <>
          <View className="mt-2 gap-5 flex-row flex-wrap items-start">
            <View className="border border-border rounded-sm p-[18px] gap-3 bg-bg-elevated z-20 flex-grow flex-[1] min-w-[320px] max-w-[420px]">
              <Text className="text-xs tracking-wide uppercase font-bold text-muted">
                Profile
              </Text>
              <View style={{ gap: 6 }}>
                <Text className="text-xs tracking-wide uppercase font-bold text-muted">
                  Display name
                </Text>
                <TextInput
                  value={displayName}
                  onChangeText={setDisplayName}
                  placeholder="Name for numerology"
                  placeholderTextColorClassName="text-subtle"
                  className="border border-border rounded-sm min-h-11 px-3 py-2.5 text-base text-fg bg-bg"
                />
              </View>
              {badgeParts.length ? (
                <Text className="text-sm text-accent">
                  {badgeParts.join(" · ")}
                </Text>
              ) : null}

              <StudioDateField
                label="Birth date"
                value={birthDate}
                onChange={setBirthDate}
              />
              <StudioTimeField
                label="Birth time"
                value={birthTime}
                onChange={setBirthTime}
              />
              <StudioPlaceField
                label="Birth place"
                value={birthPlace}
                onChange={setBirthPlace}
                onTimezoneSuggest={(tz) => setTimezone(tz)}
              />
              <StudioSelect
                label="Timezone"
                value={timezone}
                options={tzOptions}
                onChange={setTimezone}
                placeholder="Select timezone…"
                searchable
              />

              {error ? (
                <Text className="font-sans text-[15px] text-accent">{error}</Text>
              ) : null}
              {savedMsg ? (
                <Text className="text-sm text-muted">{savedMsg}</Text>
              ) : null}
              <PrimaryButton
                label={saving ? "Saving…" : "Save profile"}
                onPress={onSave}
                disabled={saving}
              />
            </View>

            <View className="flex-grow flex-[1] min-w-[280px] gap-3">
              <View className="border border-border p-3.5 gap-1.5 bg-bg-elevated">
                <Text className="text-xs tracking-wide uppercase font-bold text-muted">Today</Text>
                <Text className="font-sans text-base text-fg">
                  {age != null ? `Age ${age}` : "Add a birth date"}
                  {nextBday
                    ? ` · Next birthday in ${nextBday.daysUntil} day${nextBday.daysUntil === 1 ? "" : "s"}`
                    : ""}
                </Text>
                <Text className="text-xs text-subtle">
                  Moon: {moon.name}
                  {typeof moon.illumination === "number" ? ` · ~${moon.illumination}% lit` : ""}
                  {insight?.note ? ` · ${sunSign ?? "—"} season` : ""}
                </Text>
              </View>

              {validDate ? (
                <View style={{ gap: 14 }}>
                  {(() => {
                    const c = celestialForSign(sunSign);
                    return (
                      <>
                        <PlanetPoster
                          seasonTitle={c.seasonTitle}
                          seasonLine={c.seasonLine}
                          planet={c.planet}
                          dateLabel={
                            nextBday
                              ? `Next birthday · ${nextBday.daysUntil}d`
                              : undefined
                          }
                          compact
                        />
                        <CosmicChartCard
                          eyebrow={
                            insight?.note ||
                            `Life path ${lifePath ?? "—"} · reflective chart card`
                          }
                          planet={c.planet}
                          profileLabel={displayName || "You"}
                        />
                      </>
                    );
                  })()}
                </View>
              ) : null}

              <Text className="text-xs tracking-wide uppercase font-bold text-muted">
                Reading deck
              </Text>
              {!displayName.trim() && !validDate ? (
                <Text className="text-sm text-muted">
                  Enter a display name and birth date to unlock Expression, Soul Urge, Life Path,
                  and sun readings.
                </Text>
              ) : null}

              {readings.map((card) => {
                if (!card.reading) return null;
                const open = openReading === card.id;
                return (
                  <View
                    key={card.id}
                    className="border border-border p-3.5 gap-2 bg-bg-elevated"
                  >
                    <Pressable
                      onPress={() => setOpenReading(open ? null : card.id)}
                      className="flex-row justify-between items-center gap-2"
                    >
                      <Text className="text-xs tracking-wide uppercase font-bold text-accent">
                        {card.badge}
                      </Text>
                      <Text className="font-sans text-lg font-bold flex-1 text-fg">
                        {"title" in card.reading
                          ? card.reading.title
                          : `${(card.reading as SunReading).sign} · ${(card.reading as SunReading).element} / ${(card.reading as SunReading).modality}`}
                      </Text>
                      <Text className="text-subtle text-lg">
                        {open ? "−" : "+"}
                      </Text>
                    </Pressable>
                    {open ? (
                      <View className="gap-2 pt-1">
                        {"keywords" in card.reading ? (
                          <Text className="text-sm text-muted">
                            {(card.reading as NumberReading).keywords.join(" · ")}
                          </Text>
                        ) : null}
                        <Text className="font-sans text-[15px] leading-6 text-fg">
                          {card.reading.essay}
                        </Text>
                        <Text className="text-sm italic text-muted">
                          {"seasonPrompt" in card.reading
                            ? (card.reading as NumberReading).seasonPrompt
                            : (card.reading as SunReading).seasonNote}
                        </Text>
                      </View>
                    ) : null}
                  </View>
                );
              })}

              <Text className="text-xs leading-5 text-subtle">
                Reflective tools for creative self-inquiry. Not science, astrology-as-fact, medical,
                or financial advice.
              </Text>
            </View>
          </View>
        </>
      )}
    </Wrapper>
  );
}

