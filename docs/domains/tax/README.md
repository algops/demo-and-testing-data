# Tax domain module

**`domain_id`:** `tax`  
**Anchor tenant:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)  
**Propozice (authoring):** [04_TAX_ACCOUNTING.md](../../04_TAX_ACCOUNTING.md) — §1 Finanční Centrum is an example only

## Module scope

**Corporate tax & group accounting** for Meridian Pay — not a multi-client tax firm. Legal entities: Meridian Pay a.s. (CZ) + Meridian Pay SK s.r.o. External advisor = org-layer `vendor` (Finanční Centrum s.r.o.).

## Reframe from propozice

| Propozice entity | Anchor meaning |
|------------------|----------------|
| Client | Legal entity / tax unit in group |
| Engagement | Annual tax cycle or advisory engagement |
| 120 clients | 2–3 group entities |
| Pohoda/Money S3 | Group accounting (mostly Pohoda) |

## Volume targets (MVP)

2–3 legal entities, 8–15 engagements, 20–40 accounts, entity-level deadlines.

## Org-bridge links

- `vendor` (Finanční Centrum) → Engagement (transfer pricing advisory)
- `employee` (Finance) → Engagement (owner)
- Pohoda `system` → Tax integrations
