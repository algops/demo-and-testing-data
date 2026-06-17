# IT — Object types

**Anchor:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)

| Slug | Propozice type | Attributes |
|------|----------------|------------|
| `adr` | ADR | author, category, date, id, linked_incidents, status, superseded_by, title |
| `api` | API | auth_method, base_url, breaking_changes, consumer_count, docs_url, name, protocol, rate_limit, status, version |
| `database` | Database | backup_policy, engine, hosting, name, owner_service, shared, size_gb, version |
| `dependency` | Dependency | current_version, cve_count, cve_critical, ecosystem, last_updated, latest_version, license, name |
| `environment` | Environment | access_control, auto_deploy, cloud_provider, name, region, type, url |
| `feature_flag` | FeatureFlag | created_date, description, name, owner, service, stale, status |
| `guideline` | Guideline | category, code, compliance_status, last_updated, owner, title, version |
| `incident` | Incident | detected_at, id, on_call_person, rca_status, resolved_at, root_cause_category, severity, status, title, ttd_minutes, ttr_minutes |
| `pipeline` | Pipeline | avg_duration_min, last_failure_reason, name, platform, stages, success_rate_pct, trigger, type |
| `runbook` | Runbook | author, last_updated, linked_alerts, service, status, title |
| `service` | Service | created_date, description, framework, language, last_deploy_date, lines_of_code, name, repo_url, status, team_owner, test_coverage_pct, tier, type |
| `slo` | SLO | current_value, error_budget_remaining_pct, metric, name, service, target, window |
| `team` | Team | domain, lead, member_count, name, on_call_schedule, slack_channel |
| `tech_debt` | TechDebt | blocked_by, category, created_date, estimated_effort_days, id, impact, priority, status, title |
