# IT — Values

Domain edge attributes with quantitative/temporal data materialize as `value` records.

| Edge type | Attributes → values |
|-----------|---------------------|
| AFFECTED | downtime_minutes, impact_level |
| BLOCKS | reason |
| BUILT_BY | artifact_type, stage_count |
| CAUSED_BY | contributing_factor |
| CONSUMES | fallback_strategy, usage_frequency, version_pinned |
| CONTROLS | rollout_pct |
| DECIDED_IN | relevance |
| DEPENDS_ON | circuit_breaker, criticality, protocol, sync_async |
| DEPLOYS_TO | approval_required, strategy |
| DOCUMENTED_IN | coverage |
| EXPOSES | endpoint_count, rate_limit |
| FOLLOWS | compliance_level, exceptions_noted |
| HAS_DEPENDENCY | pinned, scope, update_blocked_by |
| LED_TO | preventive_measure |
| MONITORS | alert_threshold |
| OWNED_BY | on_call, since |
| RELATES_TO | affected_component |
| USES_DATABASE | access_type, connection_pool_size, shared_violation |
