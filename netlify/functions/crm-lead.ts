import { corsPreflight, json } from "../lib/shared";

interface LeadPayload {
  email: string;
  name?: string;
  firstName?: string;
  lastName?: string;
  message?: string;
  source?: string;
  phone?: string;
}

const DEFAULT_TWENTY_URL = "http://localhost:3000";

export default async (request: Request) => {
  if (request.method === "OPTIONS") return corsPreflight();

  if (request.method !== "POST") {
    return json({ error: "Method not allowed" }, 405);
  }

  let body: LeadPayload;
  try {
    body = (await request.json()) as LeadPayload;
  } catch {
    return json({ error: "Invalid JSON body" }, 400);
  }

  const email = body.email?.trim().toLowerCase();
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ error: "Valid email address is required" }, 400);
  }

  const crmUrl = process.env.TWENTY_CRM_URL || DEFAULT_TWENTY_URL;
  const apiKey = process.env.TWENTY_CRM_API_KEY;

  if (!apiKey) {
    return json(
      { error: "Twenty CRM API key not configured on server", ok: false },
      500,
    );
  }

  // Parse names
  let firstName = body.firstName?.trim();
  let lastName = body.lastName?.trim();
  if (!firstName && !lastName && body.name?.trim()) {
    const parts = body.name.trim().split(/\s+/);
    firstName = parts[0];
    lastName = parts.slice(1).join(" ") || "Lead";
  }

  if (!firstName && !lastName) {
    firstName = email.split("@")[0];
    lastName = "Subscriber";
  }

  const companyId =
    process.env.TWENTY_CRM_ARTOMETRICS_COMPANY_ID ||
    "4b11723a-f9ac-4c05-a7cc-28759c9b550b";

  try {
    const personPayload = {
      name: {
        firstName: firstName || "Subscriber",
        lastName: lastName || "Artometrics",
      },
      emails: {
        primaryEmail: email,
      },
      jobTitle: body.source
        ? `Lead Source: ${body.source}`
        : "Artometrics Subscriber",
      ...(body.phone
        ? {
            phones: {
              primaryPhoneNumber: body.phone,
            },
          }
        : {}),
      ...(companyId ? { companyId } : {}),
    };

    const res = await fetch(`${crmUrl}/rest/people`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(personPayload),
    });

    if (!res.ok) {
      const errText = await res.text();
      return json(
        {
          error: `Twenty CRM API error: ${res.statusText}`,
          details: errText,
          ok: false,
        },
        502,
      );
    }

    const resData = (await res.json()) as {
      data?: { createPerson?: { id?: string } };
    };
    const personId = resData.data?.createPerson?.id;

    return json({
      ok: true,
      personId,
      companyId,
      message: "Lead successfully recorded in Twenty CRM under Artometrics",
    });
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    return json({ error: msg, ok: false }, 500);
  }
};
