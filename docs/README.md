# Demo data documentation

## Anchor tenant model

All generated demo data represents **one AlgOps customer** with **five enabled domain modules**:

- [ANCHOR_TENANT.md](ANCHOR_TENANT.md) — Meridian Pay a.s. (tenant identity, systems, vendors, naming rules)
- [domains/README.md](domains/README.md) — org-layer types, org-bridge matrix, catalogue index

| `domain_id` | Catalogue | Propozice (authoring) |
|-------------|-----------|------------------------|
| `esg` | [domains/esg/](domains/esg/) | [01_ESG_COMPLIANCE.md](01_ESG_COMPLIANCE.md) |
| `it` | [domains/it/](domains/it/) | [02_IT_SW_DEVELOPMENT.md](02_IT_SW_DEVELOPMENT.md) |
| `legal` | [domains/legal/](domains/legal/) | [03_LEGAL.md](03_LEGAL.md) |
| `tax` | [domains/tax/](domains/tax/) | [04_TAX_ACCOUNTING.md](04_TAX_ACCOUNTING.md) |
| `hr` | [domains/hr/](domains/hr/) | [05_HR_SOP.md](05_HR_SOP.md) |

## Authoring note (propozice files)

**§1 company profiles in propozice files are vertical authoring examples only.** They provide realistic entity types, edges, processes, and vignettes for catalogue authors. Generated demo data always uses [ANCHOR_TENANT.md](ANCHOR_TENANT.md) — not Finbee, Kovář & Partners, Finanční Centrum, VTM, or ČEZ Energo as separate tenants.

## Implementation plan

See [.cursor/plans/mvp_demo-data_reset_48e8cbe4.plan.md](../.cursor/plans/mvp_demo-data_reset_48e8cbe4.plan.md) for generation pipeline, validation, and artifacts.
