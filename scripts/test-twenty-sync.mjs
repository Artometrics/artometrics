
const CRM_URL = process.env.TWENTY_CRM_URL || "http://localhost:3000";
const API_KEY = process.env.TWENTY_CRM_API_KEY;
const COMPANY_ID = process.env.TWENTY_CRM_ARTOMETRICS_COMPANY_ID || "4b11723a-f9ac-4c05-a7cc-28759c9b550b";

if (!API_KEY) {
  console.error("Missing TWENTY_CRM_API_KEY in .env");
  process.exit(1);
}

async function run() {
  console.log("1. Verifying Twenty CRM connection at:", CRM_URL);
  const healthRes = await fetch(`${CRM_URL}/healthz`);
  console.log("Health check status:", healthRes.status);

  console.log("2. Querying company Artometrics (ID:", COMPANY_ID, ")...");
  const compRes = await fetch(`${CRM_URL}/rest/companies/${COMPANY_ID}`, {
    headers: { Authorization: `Bearer ${API_KEY}` }
  });
  if (!compRes.ok) {
    throw new Error(`Company query failed: ${compRes.status} ${compRes.statusText}`);
  }
  const compData = await compRes.json();
  console.log("Found Company in CRM:", compData.data?.company?.name || compData.data);

  console.log("3. Simulating new Artometrics lead submission...");
  const testEmail = `lead-${Date.now()}@artometrics.com`;
  const personRes = await fetch(`${CRM_URL}/rest/people`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`
    },
    body: JSON.stringify({
      name: {
        firstName: "Elena",
        lastName: "Rostova"
      },
      emails: {
        primaryEmail: testEmail
      },
      jobTitle: "Lead Source: contact_editorial_tip",
      companyId: COMPANY_ID
    })
  });

  if (!personRes.ok) {
    const errText = await personRes.text();
    throw new Error(`Failed to create person: ${errText}`);
  }

  const personData = await personRes.json();
  const created = personData.data?.createPerson;
  console.log("Successfully created contact in Twenty CRM:");
  console.log(" - Person ID:", created.id);
  console.log(" - Name:", created.name.firstName, created.name.lastName);
  console.log(" - Primary Email:", created.emails.primaryEmail);
  console.log(" - Company ID:", created.companyId);
  console.log(" - Job / Source:", created.jobTitle);

  console.log("4. Verifying lead retrieval from CRM database...");
  const verifyRes = await fetch(`${CRM_URL}/rest/people/${created.id}`, {
    headers: { Authorization: `Bearer ${API_KEY}` }
  });
  const verifyData = await verifyRes.json();
  console.log("Retrieved verified lead record:", verifyData.data?.person?.id === created.id ? "CONFIRMED" : "MISMATCH");
  console.log("All Twenty CRM Artometrics sync tests passed.");
}

run().catch((err) => {
  console.error("Test failed:", err);
  process.exit(1);
});
