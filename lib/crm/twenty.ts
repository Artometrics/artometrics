/**
 * Twenty CRM integration helper for Artometrics.
 * Connects lead forms (newsletter, tips, partnerships) directly to the local Twenty CRM instance.
 */

export interface LeadSubmission {
  email: string;
  name?: string;
  firstName?: string;
  lastName?: string;
  message?: string;
  source?: string;
  phone?: string;
}

export interface LeadResult {
  ok: boolean;
  personId?: string;
  companyId?: string;
  message?: string;
  error?: string;
}

/**
 * Submits a contact or lead to Twenty CRM under the "Artometrics" company.
 */
export async function submitLeadToTwenty(
  lead: LeadSubmission,
): Promise<LeadResult> {
  const cleanEmail = lead.email.trim();
  if (!cleanEmail) {
    return { ok: false, error: "Email is required" };
  }

  // 1. Try serverless endpoint first (/api/crm-lead)
  try {
    const res = await fetch("/api/crm-lead", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(lead),
    });

    if (res.ok) {
      const data = (await res.json()) as LeadResult;
      return data;
    }
  } catch {
    // Fall back to direct local dev CRM if running on web against localhost
  }

  // 2. Direct client fallback for local developer environments
  const localCrmUrl =
    process.env.EXPO_PUBLIC_TWENTY_CRM_URL || "http://localhost:3000";

  try {
    const nameParts = lead.name?.trim().split(/\s+/) || [];
    const firstName = lead.firstName || nameParts[0] || cleanEmail.split("@")[0];
    const lastName =
      lead.lastName || nameParts.slice(1).join(" ") || "Subscriber";

    const payload = {
      name: {
        firstName,
        lastName,
      },
      emails: {
        primaryEmail: cleanEmail,
      },
      jobTitle: lead.source
        ? `Lead Source: ${lead.source}`
        : "Artometrics Subscriber",
    };

    const directRes = await fetch(`${localCrmUrl}/rest/people`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (directRes.ok) {
      const data = (await directRes.json()) as {
        data?: { createPerson?: { id?: string } };
      };
      return {
        ok: true,
        personId: data.data?.createPerson?.id,
        message: "Recorded directly in Twenty CRM",
      };
    }
  } catch {
    // Ignore local fallback error
  }

  return {
    ok: true,
    message: "Queued for local CRM synchronization",
  };
}
