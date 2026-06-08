# HR — Relationship matrix

Domain-native edges from propozice §5, projected to AlgOps `related_to` (+ optional values).

| Domain edge | From → To | AlgOps projection |
|-------------|-----------|-------------------|
| GOVERNS | Policy → Process | object→object `related_to`; edge attrs → values |
| REQUIRED_FOR | Training → Role | object→object `related_to`; edge attrs → values |
| ELIGIBLE_FOR | Role → Benefit | object→object `related_to`; edge attrs → values |
| BELONGS_TO | Role → Department | object→object `related_to`; edge attrs → values |
| REPORTS_TO | Department → Department | object→object `related_to`; edge attrs → values |
| USES_SYSTEM | Process → System | object→object `related_to`; edge attrs → values |
| REQUIRES_DOCUMENT | Process → Document | object→object `related_to`; edge attrs → values |
| COMPLIES_WITH | Policy → LegalRequirement | object→object `related_to`; edge attrs → values |
| APPROVES | Role → Process | object→object `related_to`; edge attrs → values |
| INCLUDES_LEAVE | Policy → LeaveType | object→object `related_to`; edge attrs → values |
| PART_OF_ONBOARDING | Training → Process | object→object `related_to`; edge attrs → values |
| SUPERSEDES | Policy → Policy | object→object `related_to`; edge attrs → values |
| IN_BAND | Role → CompensationBand | object→object `related_to`; edge attrs → values |
| TRACKS_COMPLIANCE | Training → LegalRequirement | object→object `related_to`; edge attrs → values |
| RAISED_IN | GrievanceCase → Policy | object→object `related_to`; edge attrs → values |

**Validation:** same `domain_id`; no cross-domain-native edges without org-bridge.
