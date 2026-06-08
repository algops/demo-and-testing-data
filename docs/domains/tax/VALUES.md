# TAX — Values

Domain edge attributes with quantitative/temporal data materialize as `value` records.

| Edge type | Attributes → values |
|-----------|---------------------|
| REQUIRES_FORM | section_reference, filing_condition |
| DEFINES_RATE | section, paragraph |
| MAPS_TO_ACCOUNT | mapping_rule, exceptions |
| INTERPRETS | interpreted_section, practical_implication |
| APPLIES_TO_CLIENT | applicable, reason, frequency |
| HAS_ENGAGEMENT | recurring, start_date |
| HAS_DEADLINE | actual_deadline_date, filed_date, on_time |
| TAX_TREATMENT | deductible, section_reference, conditions, common_mistakes |
| FOLLOWS_PROCEDURE | mandatory, compliance_status |
| SUPERSEDES | effective_date |
| AMENDS | amendment_number, effective_date, affected_sections |
| USES_STANDARD | mandatory_or_voluntary, since |
| MODIFIES_RATE | treaty_rate, conditions, applicable_article |
| UNDER_CONTROL | risk_level |
| RELATED_ENTITY | relationship_type, transfer_pricing_relevant |
