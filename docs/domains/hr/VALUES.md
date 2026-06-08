# HR — Values

Domain edge attributes with quantitative/temporal data materialize as `value` records.

| Edge type | Attributes → values |
|-----------|---------------------|
| GOVERNS | authority_level, exceptions, compliance_status |
| REQUIRED_FOR | mandatory, within_days_of_start, recertification_months |
| ELIGIBLE_FOR | condition, after_probation, band_minimum |
| BELONGS_TO | primary, location |
| REPORTS_TO | relationship_type |
| USES_SYSTEM | step, action, workaround |
| REQUIRES_DOCUMENT | mandatory, stage, format |
| COMPLIES_WITH | coverage_level, gaps |
| APPROVES | approval_level, delegation_allowed, escalation_to |
| INCLUDES_LEAVE | conditions, override_from_law |
| PART_OF_ONBOARDING | day_in_onboarding, sequence_order |
| SUPERSEDES | effective_date, reason |
| IN_BAND | typical_position_in_range |
| TRACKS_COMPLIANCE | evidence_type, audit_ready |
| RAISED_IN | alleged_violation |
