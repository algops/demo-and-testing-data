# Tax — Objects (volume & naming)

**Anchor:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md) — `org_id: org:anchor`, `domain_id: tax`.  
**Semantic source:** [04_TAX_ACCOUNTING.md](../../04_TAX_ACCOUNTING.md) §6–§8 (group tax, not tax-firm tenant).

## Reframe

- **Client** → **LegalEntity** / tax unit (Meridian Pay a.s., Meridian Pay SK s.r.o.)
- External advisor → org-layer `vendor:financni-centrum`

## Volume targets (MVP)

| Object-type | Target count | Notes |
|-------------|--------------|-------|
| LegalEntity (Client) | 2–3 | CZ parent + SK subsidiary |
| Engagement | 8–15 | Annual cycles + TP project |
| TaxControl | 3–8 | |
| Account | 20–40 | Group chart |
| Deadline | per entity × form types | |
| TaxLaw, TaxForm, TaxRate | reference density per propozice §6 scaled | |

## Naming

Engagements named for Meridian Pay entities, not Finanční Centrum client list.
