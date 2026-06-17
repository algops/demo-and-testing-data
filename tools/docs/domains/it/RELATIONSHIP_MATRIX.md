# IT — Relationship matrix

Domain-native edges from propozice §5, projected to AlgOps `related_to` (+ optional values).

| Domain edge | From → To | AlgOps projection |
|-------------|-----------|-------------------|
| AFFECTED | Incident → Service | object→object `related_to`; edge attrs → values |
| BLOCKS | TechDebt → TechDebt | object→object `related_to`; edge attrs → values |
| BUILT_BY | Pipeline → Service | object→object `related_to`; edge attrs → values |
| CAUSED_BY | Incident → TechDebt | object→object `related_to`; edge attrs → values |
| CONSUMES | Service → API | object→object `related_to`; edge attrs → values |
| CONTROLS | FeatureFlag → Service | object→object `related_to`; edge attrs → values |
| DECIDED_IN | Service → ADR | object→object `related_to`; edge attrs → values |
| DEPENDS_ON | Service → Service | object→object `related_to`; edge attrs → values |
| DEPLOYS_TO | Pipeline → Environment | object→object `related_to`; edge attrs → values |
| DOCUMENTED_IN | Runbook → Service | object→object `related_to`; edge attrs → values |
| EXPOSES | Service → API | object→object `related_to`; edge attrs → values |
| FOLLOWS | Team → Guideline | object→object `related_to`; edge attrs → values |
| HAS_DEPENDENCY | Service → Dependency | object→object `related_to`; edge attrs → values |
| LED_TO | Incident → ADR | object→object `related_to`; edge attrs → values |
| MONITORS | SLO → Service | object→object `related_to`; edge attrs → values |
| OWNED_BY | Service → Team | object→object `related_to`; edge attrs → values |
| RELATES_TO | TechDebt → Service | object→object `related_to`; edge attrs → values |
| USES_DATABASE | Service → Database | object→object `related_to`; edge attrs → values |

**Validation:** same `domain_id`; no cross-domain-native edges without org-bridge.
