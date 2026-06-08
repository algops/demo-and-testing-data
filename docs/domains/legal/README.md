# Legal domain module

**`domain_id`:** `legal`  
**Anchor tenant:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)  
**Propozice (authoring):** [03_LEGAL.md](../../03_LEGAL.md) — §1 Kovář & Partners is an example only

## Module scope

**In-house legal team** at Meridian Pay — not a law-firm tenant. Matters, contracts, templates, legislation references. External counsel = org-layer `vendor` (Kovář & Partners).

## Reframe from propozice

| Propozice entity | Anchor meaning |
|------------------|----------------|
| Client | Counterparty (vendor, partner, customer, regulator) |
| Person (lawyer) | In-house counsel or `employee` bridge |
| Matter | Meridian Pay legal affair (e.g. Project Falcon / LogiCorp acquisition) |
| Koncipient workflows | Junior in-house lawyers + paralegals |

## Volume targets (MVP)

40–90 matters, 50–120 contracts, 15–30 counterparties, 8–10 legal areas.

## Org-bridge links

- `employee` → Matter (responsible_lawyer), Contract
- `vendor` (Kovář & Partners) → Matter (external_counsel overflow)
- iManage `system` → Legal integrations
