# Anchor Tenant — Meridian Pay a.s.

Single AlgOps customer for all demo data. Five domain modules (`it`, `legal`, `tax`, `hr`, `esg`) are enabled on this tenant. Propozice §1 company profiles (Finbee, Kovář & Partners, Finanční Centrum, VTM, ČEZ Energo) are **authoring examples only** — entity types, edges, and vignettes are remapped here.

---

## Identity


| Field                  | Value                                                                                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Legal name**         | Meridian Pay a.s.                                                                                                                                        |
| **Brand**              | Meridian Pay                                                                                                                                             |
| **Sector**             | Fintech — open banking & payment orchestration for SMB in CEE                                                                                            |
| **IČO**                | 09876543 (fictional)                                                                                                                                     |
| **HQ**                 | Praha 4, Karlín (office + leadership)                                                                                                                    |
| **Engineering hub**    | Brno (majority of product engineering)                                                                                                                   |
| **Employees**          | ~240 (155 product/engineering, 35 ops/risk/compliance, 25 G&A, 15 sales, 10 ESG/legal/tax shared services)                                               |
| **Revenue**            | ~890 mil CZK (FY2024)                                                                                                                                    |
| **Regulatory posture** | Czech National Bank payment-institution oversight; CSRD large-undertaking threshold approached via group consolidation rules — ESG reporting from FY2024 |


### `enabled_domains`

```yaml
enabled_domains: [esg, it, legal, tax, hr]
org_slug: anchor
org_id_seed: org:anchor
```

All generated entities carry `org_id: org:anchor`. Domain-scoped entities also carry `domain_id`. Org-layer shared entities use `domain_id: shared`.

---

## Org structure


| Unit                 | Location      | Headcount (approx) | Notes                                                           |
| -------------------- | ------------- | ------------------ | --------------------------------------------------------------- |
| Engineering          | Brno + remote | ~95                | 6 squads — payments, auth, ledger, integrations, platform, data |
| Product & Design     | Praha / Brno  | ~25                |                                                                 |
| Operations & SRE     | Brno          | ~20                | On-call, incident management                                    |
| Risk & Compliance    | Praha         | ~18                | Includes in-house legal (4) + compliance (6) + risk (8)         |
| Finance & Tax        | Praha         | ~12                | Corporate accounting; external tax advisor for TP/DPH peaks     |
| People (HR)          | Praha         | ~8                 | SuccessFactors admin, L&D, payroll liaison                      |
| ESG & Sustainability | Praha         | ~4                 | CSRD programme office (matrixed from Finance + Ops)             |
| Sales & CS           | Praha         | ~15                |                                                                 |
| G&A                  | Praha         | ~10                |                                                                 |


**Departments (org-layer):** Engineering, Product, Operations, Risk & Compliance, Finance, People, ESG, Sales, G&A.

---

## Systems map

One `system` object per row where noted — multiple domain integrations may `syncs` the same system.


| System                        | Primary domain | Role                                           |
| ----------------------------- | -------------- | ---------------------------------------------- |
| GitLab                        | IT             | Source of truth — services, MRs, pipelines     |
| GitHub (legacy mirror)        | IT             | External client API repos                      |
| Confluence                    | IT             | ADRs, runbooks, architecture                   |
| Slack                         | IT             | Engineering comms                              |
| Datadog                       | IT             | Metrics, incidents                             |
| PagerDuty                     | IT             | On-call routing                                |
| iManage                       | Legal          | Contract & matter DMS (in-house legal team)    |
| SharePoint                    | Legal, HR, Tax | Policies, templates, tax workpapers            |
| Beck-online / ASPI            | Legal          | Legislation research                           |
| SAP SuccessFactors            | HR             | Core HR, partial payroll                       |
| Recruitee                     | HR             | ATS                                            |
| Pohoda                        | Tax            | Group accounting (Meridian Pay + 1 subsidiary) |
| EPO / datová schránka         | Tax            | Tax filings                                    |
| Sphera                        | ESG            | ESRS data collection                           |
| ERP export (SF → spreadsheet) | ESG, HR        | Evidence packs for CSRD                        |


---

## External vendors (org-layer `vendor` objects)

Not separate tenants — referenced from Legal/Tax domains via org-bridge edges.


| Vendor                                     | Type             | Used by | Narrative source (propozice example)                                          |
| ------------------------------------------ | ---------------- | ------- | ----------------------------------------------------------------------------- |
| Kovář & Partners advokátní kancelář s.r.o. | External counsel | Legal   | [03_LEGAL.md](03_LEGAL.md) — M&A specialist support, overflow matters         |
| Finanční Centrum s.r.o.                    | Tax advisor      | Tax     | [04_TAX_ACCOUNTING.md](04_TAX_ACCOUNTING.md) — transfer pricing, DPH advisory |
| Deloitte CZ                                | Assurance        | ESG     | Limited assurance on CSRD report                                              |


---

## Domain module stories (under this tenant)

### IT (`domain_id: it`)

Meridian Pay engineering platform — microservices on AWS/EKS, legacy Java monolith, agentic-development readiness. Content sourced from [02_IT_SW_DEVELOPMENT.md](02_IT_SW_DEVELOPMENT.md) §2–§9; Finbee naming → Meridian Pay naming.

**Volume band (MVP):** 18–30 services, 25–45 APIs, 40–70 incidents, 80–180 dependencies.

### HR (`domain_id: hr`)

Meridian Pay employees, SOPs, benefits, onboarding. Content from [05_HR_SOP.md](05_HR_SOP.md); VTM manufacturing scale → ~240-employee fintech (single Praha HQ + Brno hub, no factory floor).

**Volume band (MVP):** 30–45 policies, 35–55 processes, 180–240 employees, 8–12 departments.

### Legal (`domain_id: legal`)

**In-house legal team** (4 lawyers + 2 paralegals) — not a law firm tenant. Matters = Meridian Pay affairs (vendor contracts, licensing, employment disputes, M&A support). External counsel = Kovář & Partners `vendor`. Content from [03_LEGAL.md](03_LEGAL.md); "Client" entities → **counterparties** (vendors, partners, regulators).

**Volume band (MVP):** 40–90 matters, 50–120 contracts, 15–30 counterparties, 8–10 legal areas.

### Tax (`domain_id: tax`)

**Corporate tax & accounting** for Meridian Pay a.s. + subsidiary **Meridian Pay SK s.r.o.** (Bratislava ops). Not a multi-client tax firm. "Client" in propozice → **legal entity / tax unit**. External advisor = Finanční Centrum `vendor`. Content from [04_TAX_ACCOUNTING.md](04_TAX_ACCOUNTING.md).

**Volume band (MVP):** 2–3 legal entities, 8–15 engagements (annual cycles), 20–40 accounts, deadlines per entity.

### ESG (`domain_id: esg`)

Meridian Pay CSRD journey — payment-sector material topics (financial inclusion, fraud, energy of data centres, supplier due diligence). Content from [01_ESG_COMPLIANCE.md](01_ESG_COMPLIANCE.md); ČEZ utility scale → mid-size fintech supplier base (~80–120 suppliers screened).

**Volume band (MVP):** 80–120 metrics, 15–25 policies, 60–90 suppliers, 8–12 reports.

---

## Vignette & naming remap rules

When transcribing propozice §6–§8 vignettes into catalogues and generators:


| Propozice reference                   | Anchor remap                                                               |
| ------------------------------------- | -------------------------------------------------------------------------- |
| Finbee s.r.o.                         | Meridian Pay a.s.                                                          |
| Kovář & Partners (as tenant)          | In-house Legal team; Kovář = external `vendor` for Project Falcon overflow |
| Finanční Centrum (as tenant)          | Finance team + Finanční Centrum `vendor` for TP                            |
| VTM a.s.                              | Meridian Pay (HR domain only)                                              |
| ČEZ Energo Solutions                  | Meridian Pay (ESG domain only)                                             |
| Project Falcon / LogiCorp acquisition | Meridian Pay acquisition of LogiCorp — matter M-2024-0142                  |
| `legacy-order-monolith`               | `legacy-ledger-monolith` (Java, Meridian Pay)                              |
| Brno-Líšeň / Olomouc plants           | Brno engineering hub / Praha HQ (no manufacturing sites)                   |
| 120 tax clients                       | 2–3 group legal entities                                                   |
| 2 500 employees (ESG)                 | ~240 employees; CSRD via size + consolidation criteria                     |


**Slug prefix:** `{org}:{domain}:{entity}:{slug}` e.g. `org:anchor:it:service:payment-gateway`.

**Org-layer slug prefix:** `org:anchor:shared:{entity}:{slug}` e.g. `org:anchor:shared:person:eva-novakova`.

---

## KPI narrative (sales demo)

Values on anchor `organization` object (see IT domain `VALUES.md`):

- Engineering: deployment frequency, incident MTTR, tech-debt ratio
- HR: time-to-answer SOP queries, onboarding checklist completion
- Legal: template find time, matter response SLA
- Tax: filing on-time rate, open deadline count
- ESG: ESRS coverage %, supplier response rate

---

## Related docs

- [docs/README.md](README.md) — index
- [docs/domains/README.md](domains/README.md) — org-layer types, bridge matrix
- Propozice (authoring): [01_ESG_COMPLIANCE.md](01_ESG_COMPLIANCE.md) … [05_HR_SOP.md](05_HR_SOP.md)

