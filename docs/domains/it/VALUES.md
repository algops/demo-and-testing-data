# IT — Values

Domain edge attributes with quantitative/temporal data materialize as `value` records.

| Edge type | Attributes → values |
|-----------|---------------------|
| DEPENDS_ON | protocol, sync_async, criticality, circuit_breaker |
| EXPOSES | endpoint_count, rate_limit |
| CONSUMES | usage_frequency, fallback_strategy, version_pinned |
| USES_DATABASE | access_type, connection_pool_size, shared_violation |
| OWNED_BY | since, on_call |
| BUILT_BY | stage_count, artifact_type |
| DEPLOYS_TO | strategy, approval_required |
| DECIDED_IN | relevance |
| FOLLOWS | compliance_level, exceptions_noted |
| HAS_DEPENDENCY | scope, pinned, update_blocked_by |
| AFFECTED | impact_level, downtime_minutes |
| CAUSED_BY | contributing_factor |
| LED_TO | preventive_measure |
| RELATES_TO | affected_component |
| MONITORS | alert_threshold |
| DOCUMENTED_IN | coverage |
| CONTROLS | rollout_pct |
| BLOCKS | reason |
