# IT Software Development — Propozice (bootstrapped)

Authoring source for IT domain entity catalogues. Schema extracted from legacy canonical data.

## Entity types

```json
{
  "entity_types": [
    {
      "type": "ADR",
      "attributes": [
        "author",
        "category",
        "date",
        "id",
        "linked_incidents",
        "status",
        "superseded_by",
        "title"
      ],
      "examples": [
        "ADR-001 Adopt event-driven architecture",
        "ADR-015 Use gRPC for inter-service communication",
        "ADR-007 Use MongoDB for session storage",
        "ADR-001 Adopt event-driven architecture v2",
        "ADR-015 Use gRPC for inter-service communication — updated",
        "ADR-007 Use MongoDB for session storage #6",
        "ADR-001 Adopt event-driven architecture",
        "ADR-015 Use gRPC for inter-service communication (Brno)"
      ]
    },
    {
      "type": "API",
      "attributes": [
        "auth_method",
        "base_url",
        "breaking_changes",
        "consumer_count",
        "docs_url",
        "name",
        "protocol",
        "rate_limit",
        "status",
        "version"
      ],
      "examples": [
        "Payments API v3",
        "Payments API v1",
        "Analytics API",
        "Inter-service Auth",
        "Payments API v3 — updated",
        "Payments API v1 #6",
        "Analytics API",
        "Inter-service Auth (Brno)"
      ]
    },
    {
      "type": "Database",
      "attributes": [
        "backup_policy",
        "engine",
        "hosting",
        "name",
        "owner_service",
        "shared",
        "size_gb",
        "version"
      ],
      "examples": [
        "users-pg",
        "orders-pg",
        "cache-redis",
        "search-es",
        "users-pg — updated",
        "orders-pg #6",
        "cache-redis",
        "search-es (Brno)"
      ]
    },
    {
      "type": "Dependency",
      "attributes": [
        "current_version",
        "cve_count",
        "cve_critical",
        "ecosystem",
        "last_updated",
        "latest_version",
        "license",
        "name"
      ],
      "examples": [
        "express@4.18.2",
        "lodash@4.17.19",
        "spring-boot@2.7.18",
        "kafka-go@0.4.47",
        "express@4.18.2 — updated",
        "lodash@4.17.19 #6",
        "spring-boot@2.7.18",
        "kafka-go@0.4.47 (Brno)"
      ]
    },
    {
      "type": "Environment",
      "attributes": [
        "access_control",
        "auto_deploy",
        "cloud_provider",
        "name",
        "region",
        "type",
        "url"
      ],
      "examples": [
        "dev",
        "staging",
        "prod-eu",
        "prod-us",
        "dev — updated"
      ]
    },
    {
      "type": "FeatureFlag",
      "attributes": [
        "created_date",
        "description",
        "name",
        "owner",
        "service",
        "stale",
        "status"
      ],
      "examples": [
        "ff_multi_currency",
        "ff_new_onboarding_flow",
        "ff_graphql_analytics",
        "ff_multi_currency v2",
        "ff_new_onboarding_flow — updated",
        "ff_graphql_analytics #6",
        "ff_multi_currency",
        "ff_new_onboarding_flow (Brno)"
      ]
    },
    {
      "type": "Guideline",
      "attributes": [
        "category",
        "code",
        "compliance_status",
        "last_updated",
        "owner",
        "title",
        "version"
      ],
      "examples": [
        "API Design Standards v2.1",
        "Code Review Checklist v3.0",
        "Git Branching Strategy v1.0",
        "Security Coding Guidelines v2.0",
        "API Design Standards v2.1 — updated",
        "Code Review Checklist v3.0 #6",
        "Git Branching Strategy v1.0",
        "Security Coding Guidelines v2.0 (Brno)"
      ]
    },
    {
      "type": "Incident",
      "attributes": [
        "detected_at",
        "id",
        "on_call_person",
        "rca_status",
        "resolved_at",
        "root_cause_category",
        "severity",
        "status",
        "title",
        "ttd_minutes",
        "ttr_minutes"
      ],
      "examples": [
        "INC-034 Payment timeout spike",
        "INC-067 Auth service OOM",
        "INC-091 Nightly e2e pipeline broken 5 days",
        "INC-034 Payment timeout spike v2",
        "INC-067 Auth service OOM — updated",
        "INC-091 Nightly e2e pipeline broken 5 days #6",
        "INC-034 Payment timeout spike",
        "INC-067 Auth service OOM (Brno)"
      ]
    },
    {
      "type": "Pipeline",
      "attributes": [
        "avg_duration_min",
        "last_failure_reason",
        "name",
        "platform",
        "stages",
        "success_rate_pct",
        "trigger",
        "type"
      ],
      "examples": [
        "payment-gateway-ci",
        "legacy-monolith-ci",
        "nightly-e2e",
        "payment-gateway-ci v2",
        "legacy-monolith-ci — updated",
        "nightly-e2e #6",
        "payment-gateway-ci",
        "legacy-monolith-ci (Brno)"
      ]
    },
    {
      "type": "Runbook",
      "attributes": [
        "author",
        "last_updated",
        "linked_alerts",
        "service",
        "status",
        "title"
      ],
      "examples": [
        "payment-gateway: High Error Rate",
        "auth-svc: OOM Recovery",
        "legacy-monolith: Manual Deploy Steps",
        "payment-gateway: High Error Rate v2",
        "auth-svc: OOM Recovery — updated",
        "legacy-monolith: Manual Deploy Steps #6",
        "payment-gateway: High Error Rate",
        "auth-svc: OOM Recovery (Brno)"
      ]
    },
    {
      "type": "Service",
      "attributes": [
        "created_date",
        "description",
        "framework",
        "language",
        "last_deploy_date",
        "lines_of_code",
        "name",
        "repo_url",
        "status",
        "team_owner",
        "test_coverage_pct",
        "tier",
        "type"
      ],
      "examples": [
        "auth-service",
        "payment-gateway",
        "legacy-ledger-monolith",
        "card-tokenization-proxy",
        "php-admin-panel",
        "auth-service #6",
        "payment-gateway",
        "legacy-ledger-monolith (Brno)"
      ]
    },
    {
      "type": "SLO",
      "attributes": [
        "current_value",
        "error_budget_remaining_pct",
        "metric",
        "name",
        "service",
        "target",
        "window"
      ],
      "examples": [
        "payment-gateway availability 99.95%",
        "auth-svc latency p99 < 200ms",
        "legacy-monolith availability — no SLO defined",
        "payment-gateway availability 99.95% v2",
        "auth-svc latency p99 < 200ms — updated",
        "legacy-monolith availability — no SLO defined #6",
        "payment-gateway availability 99.95%",
        "auth-svc latency p99 < 200ms (Brno)"
      ]
    },
    {
      "type": "Team",
      "attributes": [
        "domain",
        "lead",
        "member_count",
        "name",
        "on_call_schedule",
        "slack_channel"
      ],
      "examples": [
        "Payments Squad",
        "Platform/Infra",
        "Growth",
        "Data Engineering",
        "Payments Squad — updated",
        "Platform/Infra #6",
        "Growth",
        "Data Engineering (Brno)"
      ]
    },
    {
      "type": "TechDebt",
      "attributes": [
        "blocked_by",
        "category",
        "created_date",
        "estimated_effort_days",
        "id",
        "impact",
        "priority",
        "status",
        "title"
      ],
      "examples": [
        "TD-001 Decompose legacy-ledger-monolith",
        "TD-012 Upgrade spring-boot from 2.7 to 3.x",
        "TD-034 Eliminate shared orders-pg database",
        "TD-045 Migrate Jenkins to GitHub Actions for monolith",
        "TD-001 Decompose legacy-ledger-monolith — updated",
        "TD-012 Upgrade spring-boot from 2.7 to 3.x #6",
        "TD-034 Eliminate shared orders-pg database",
        "TD-045 Migrate Jenkins to GitHub Actions for monolith (Brno)"
      ]
    }
  ]
}
```

## Relationship types

```json
{
  "relationship_types": [
    {
      "type": "AFFECTED",
      "from": "Incident",
      "to": "Service",
      "attributes": [
        "downtime_minutes",
        "impact_level"
      ]
    },
    {
      "type": "BLOCKS",
      "from": "TechDebt",
      "to": "TechDebt",
      "attributes": [
        "reason"
      ]
    },
    {
      "type": "BUILT_BY",
      "from": "Pipeline",
      "to": "Service",
      "attributes": [
        "artifact_type",
        "stage_count"
      ]
    },
    {
      "type": "CAUSED_BY",
      "from": "Incident",
      "to": "TechDebt",
      "attributes": [
        "contributing_factor"
      ]
    },
    {
      "type": "CONSUMES",
      "from": "Service",
      "to": "API",
      "attributes": [
        "fallback_strategy",
        "usage_frequency",
        "version_pinned"
      ]
    },
    {
      "type": "CONTROLS",
      "from": "FeatureFlag",
      "to": "Service",
      "attributes": [
        "rollout_pct"
      ]
    },
    {
      "type": "DECIDED_IN",
      "from": "Service",
      "to": "ADR",
      "attributes": [
        "relevance"
      ]
    },
    {
      "type": "DEPENDS_ON",
      "from": "Service",
      "to": "Service",
      "attributes": [
        "circuit_breaker",
        "criticality",
        "protocol",
        "sync_async"
      ]
    },
    {
      "type": "DEPLOYS_TO",
      "from": "Pipeline",
      "to": "Environment",
      "attributes": [
        "approval_required",
        "strategy"
      ]
    },
    {
      "type": "DOCUMENTED_IN",
      "from": "Runbook",
      "to": "Service",
      "attributes": [
        "coverage"
      ]
    },
    {
      "type": "EXPOSES",
      "from": "Service",
      "to": "API",
      "attributes": [
        "endpoint_count",
        "rate_limit"
      ]
    },
    {
      "type": "FOLLOWS",
      "from": "Team",
      "to": "Guideline",
      "attributes": [
        "compliance_level",
        "exceptions_noted"
      ]
    },
    {
      "type": "HAS_DEPENDENCY",
      "from": "Service",
      "to": "Dependency",
      "attributes": [
        "pinned",
        "scope",
        "update_blocked_by"
      ]
    },
    {
      "type": "LED_TO",
      "from": "Incident",
      "to": "ADR",
      "attributes": [
        "preventive_measure"
      ]
    },
    {
      "type": "MONITORS",
      "from": "SLO",
      "to": "Service",
      "attributes": [
        "alert_threshold"
      ]
    },
    {
      "type": "OWNED_BY",
      "from": "Service",
      "to": "Team",
      "attributes": [
        "on_call",
        "since"
      ]
    },
    {
      "type": "RELATES_TO",
      "from": "TechDebt",
      "to": "Service",
      "attributes": [
        "affected_component"
      ]
    },
    {
      "type": "USES_DATABASE",
      "from": "Service",
      "to": "Database",
      "attributes": [
        "access_type",
        "connection_pool_size",
        "shared_violation"
      ]
    }
  ]
}
```
