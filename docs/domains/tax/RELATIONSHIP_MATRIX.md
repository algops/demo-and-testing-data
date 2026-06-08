# TAX — Relationship matrix

Domain-native edges from propozice §5, projected to AlgOps `related_to` (+ optional values).

| Domain edge | From → To | AlgOps projection |
|-------------|-----------|-------------------|
| REQUIRES_FORM | TaxLaw → TaxForm | object→object `related_to`; edge attrs → values |
| DEFINES_RATE | TaxLaw → TaxRate | object→object `related_to`; edge attrs → values |
| MAPS_TO_ACCOUNT | AccountingStandard → Account | object→object `related_to`; edge attrs → values |
| INTERPRETS | TaxRuling → TaxLaw | object→object `related_to`; edge attrs → values |
| APPLIES_TO_CLIENT | TaxForm → LegalEntity | object→object `related_to`; edge attrs → values |
| HAS_ENGAGEMENT | LegalEntity → Engagement | object→object `related_to`; edge attrs → values |
| HAS_DEADLINE | Engagement → Deadline | object→object `related_to`; edge attrs → values |
| TAX_TREATMENT | Account → TaxLaw | object→object `related_to`; edge attrs → values |
| FOLLOWS_PROCEDURE | Engagement → InternalProcedure | object→object `related_to`; edge attrs → values |
| SUPERSEDES | TaxRuling → TaxRuling | object→object `related_to`; edge attrs → values |
| AMENDS | TaxLaw → TaxLaw | object→object `related_to`; edge attrs → values |
| USES_STANDARD | LegalEntity → AccountingStandard | object→object `related_to`; edge attrs → values |
| MODIFIES_RATE | TaxTreaty → TaxRate | object→object `related_to`; edge attrs → values |
| UNDER_CONTROL | LegalEntity → TaxControl | object→object `related_to`; edge attrs → values |
| RELATED_ENTITY | LegalEntity → LegalEntity | object→object `related_to`; edge attrs → values |

**Validation:** same `domain_id`; no cross-domain-native edges without org-bridge.
