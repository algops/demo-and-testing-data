# IT domain module

**`domain_id`:** `it`  
**Anchor tenant:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md) — Meridian Pay a.s.  
**Propozice (authoring):** [02_IT_SW_DEVELOPMENT.md](../../02_IT_SW_DEVELOPMENT.md) — §1 Finbee is an example only

## Module scope

Engineering platform: services, APIs, incidents, tech debt, ADRs, runbooks. All objects carry `org_id: org:anchor` and `domain_id: it`.

## Volume targets (MVP)

See ANCHOR_TENANT § IT — 18–30 services, 25–45 APIs, 40–70 incidents, 80–180 dependencies.

## Org-bridge links

- `employee` → Incident (reporter), TechDebt (owner)
- `system` (GitLab, Confluence, Datadog) → IT integrations
- `department` Engineering → Service owner_dept

## Catalogue files

Fill from propozice §4–§6 using Meridian Pay naming (remap table in ANCHOR_TENANT).
