# LEGAL — Relationship matrix

Domain-native edges from propozice §5, projected to AlgOps `related_to` (+ optional values).

| Domain edge | From → To | AlgOps projection |
|-------------|-----------|-------------------|
| CITES_LEGISLATION | LegalOpinion → Legislation | object→object `related_to`; edge attrs → values |
| CITES_DECISION | LegalOpinion → CourtDecision | object→object `related_to`; edge attrs → values |
| INTERPRETS | CourtDecision → Legislation | object→object `related_to`; edge attrs → values |
| OVERRULES | CourtDecision → CourtDecision | object→object `related_to`; edge attrs → values |
| GOVERNED_BY | Contract → Legislation | object→object `related_to`; edge attrs → values |
| BASED_ON_TEMPLATE | Contract → Template | object→object `related_to`; edge attrs → values |
| BELONGS_TO_MATTER | ['Contract', 'LegalOpinion', 'DDProject'] → Matter | object→object `related_to`; edge attrs → values |
| LED_BY | Matter → Person | object→object `related_to`; edge attrs → values |
| FOR_CLIENT | Matter → Counterparty | object→object `related_to`; edge attrs → values |
| SPECIALIZES_IN | Person → LegalArea | object→object `related_to`; edge attrs → values |
| COVERS_AREA | Template → LegalArea | object→object `related_to`; edge attrs → values |
| AMENDS | Legislation → Legislation | object→object `related_to`; edge attrs → values |
| FOLLOWS_GUIDELINE | Matter → InternalGuideline | object→object `related_to`; edge attrs → values |
| SIMILAR_TO | Matter → Matter | object→object `related_to`; edge attrs → values |

**Validation:** same `domain_id`; no cross-domain-native edges without org-bridge.
