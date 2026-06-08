# ESG — Relationship matrix

Domain-native edges from propozice §5, projected to AlgOps `related_to` (+ optional values).

| Domain edge | From → To | AlgOps projection |
|-------------|-----------|-------------------|
| REQUIRES_DISCLOSURE | Regulation → DisclosureRequirement | object→object `related_to`; edge attrs → values |
| CONTAINS_METRIC | DisclosureRequirement → Metric | object→object `related_to`; edge attrs → values |
| REFERENCES_STANDARD | Regulation → Standard | object→object `related_to`; edge attrs → values |
| MEASURED_FROM | Metric → DataSource | object→object `related_to`; edge attrs → values |
| ADDRESSES_TOPIC | Policy → MaterialTopic | object→object `related_to`; edge attrs → values |
| MITIGATES | Policy → Risk | object→object `related_to`; edge attrs → values |
| APPLIES_TO | Regulation → EconomicActivity | object→object `related_to`; edge attrs → values |
| ASSESSED_FOR | Supplier → Risk | object→object `related_to`; edge attrs → values |
| REPORTED_IN | Metric → Report | object→object `related_to`; edge attrs → values |
| OWNS | DataSource → Metric | object→object `related_to`; edge attrs → values |
| TRACKS_TARGET | Target → Metric | object→object `related_to`; edge attrs → values |
| RAISED_ON | AuditFinding → Metric | object→object `related_to`; edge attrs → values |
| MATERIAL_FOR | MaterialTopic → Standard | object→object `related_to`; edge attrs → values |
| SUPPLIES_TO | Supplier → EconomicActivity | object→object `related_to`; edge attrs → values |
| HAS_SUBREGULATION | Regulation → Regulation | object→object `related_to`; edge attrs → values |

**Validation:** same `domain_id`; no cross-domain-native edges without org-bridge.
