# Propozice: IT Software Development

> **Authoring note:** §1 company profile is a vertical authoring example. Generated demo data uses the anchor tenant [ANCHOR_TENANT.md](ANCHOR_TENANT.md) (Meridian Pay a.s.), not Finbee as a separate AlgOps tenant.

## 1. Company Profile — fiktivní firma

**Název:** Finbee s.r.o.
**Sektor:** Fintech — open banking platform pro SMB segment v CEE
**Produkt:** API-first platforma umožňující SMB firmám napojit bankovní účty, automatizovat fakturaci, cash flow predikce a platební workflow
**Velikost:** ~120 zaměstnanců, z toho ~75 engineering (6 týmů)
**Stack evoluce:**
- **2019:** Monolith v Java/Spring Boot, PostgreSQL, Jenkins CI, on-prem hosting (Hetzner)
- **2020:** První microservices (auth, payments) vyčleněny z monolithu, React frontend
- **2021:** Migrace na AWS (EKS), adopce Kubernetes, přechod Jenkins → GitHub Actions, ADR-001 schválení event-driven architektury (Kafka)
- **2022:** Go adopce pro high-throughput services (transaction-processor, webhook-dispatcher), DataDog monitoring, první SLO definice
- **2023:** gRPC pro inter-service komunikace (ADR-015), GraphQL gateway pro frontend, Terraform IaC. Incident INC-034 (payment timeout spike po Black Friday traffic) vedl k circuit breaker adopci (ADR-018)
- **2024:** Stále existuje `legacy-order-monolith` (Java, 180k LOC), který nikdo nechce přepsat. Jeden tým zkouší Rust pro card-tokenization-proxy. PHP admin panel z roku 2019 stále běží interně. 3 deprecated API verze (v1) stále konzumovány externími klienty.

### Technologický nepořádek (reálný stav)
- Naming inconsistence: některé services `-svc`, jiné `-service`, `legacy-order-monolith` bez suffixu
- 2 databáze sdílené mezi services (anti-pattern, v tech debt backlogu)
- Jeden tým (Data Engineering) používá Python/Airflow, zbytek TypeScript/Go/Java
- Jenkins instance stále běží pro legacy monolith (migration "in progress" 18 měsíců)
- 4 Confluence pages s "Getting Started" guides — 2 outdated, 1 partial, 1 current

---

## 2. Role a persony

| Role | Popis | Typické dotazy |
|------|-------|----------------|
| Software Developer | Píše a udržuje kód | "Jaký je náš pattern pro error handling v Go services?" |
| Tech Lead | Vede technická rozhodnutí týmu | "Jaké ADR se vztahují k naší event-driven architektuře?" |
| DevOps/Platform Engineer | Spravuje CI/CD, Kubernetes, IaC | "Proč deploy pipeline pro legacy-order-monolith trvá 45 minut?" |
| QA Engineer | Automatizované i manuální testování | "Jaké e2e testy pokrývají payment flow a jak často padají?" |
| Product Owner | Definuje requirements | "Které services ovlivní, když přidáme multi-currency support?" |
| Engineering Manager | Řídí tým, capacity planning | "Kolik tech debt days jsme alokovali v Q3 a na co?" |
| Solution Architect | Systémový design | "Jaký je blast radius výpadku Kafka clusteru?" |
| Junior Developer (onboarding) | Nový člen, první týden | "Jak rozběhnu lokální dev stack a kde je aktuální Getting Started guide?" |
| Security Engineer | AppSec, vulnerability management | "Které services mají kritické CVE v dependencies a nejsou patchnuté?" |

---

## 3. Klíčové procesy

### 3.1 Software Development Lifecycle
1. User story refinement (Product + Tech Lead, weekly)
2. Technical design doc pro features > 3 story points
3. Sprint planning (2-week sprints, Jira)
4. Development — feature branch, konvence: `feat/TICKET-123-description`
5. PR review — min. 2 approvals, 1 must be senior/lead, automated checks must pass
6. Automated testing: unit (>80% coverage target), integration, contract tests (Pact)
7. CI pipeline: lint → build → unit test → integration test → security scan (Snyk) → docker build
8. CD pipeline: auto-deploy to staging, manual approval for prod
9. Staging QA: automated e2e (Playwright) + manual exploratory for payment flows
10. Prod deployment: canary (5% → 25% → 100%), rollback on error rate >1%
11. Post-deploy: Datadog dashboard check, 30-min bake period, Slack notification to #releases

### 3.2 Architecture Decision Records
1. Problem statement — kdo identifikoval, jaký je business/tech driver
2. RFC (Request for Comments) — lightweight design doc, 1-week comment period
3. ADR drafting — formální záznam rozhodnutí, varianty, trade-offs
4. Architecture board review (Tech Leads + CTO, biweekly)
5. Decision + documentation v Confluence (ADR-XXX)
6. Implementation tracking — linked Jira epics
7. Retrospective — po 6 měsících review, ADR status: `accepted` / `superseded` / `deprecated`

### 3.3 Incident Management
1. Alert fires (Datadog, PagerDuty → on-call)
2. Triage: P1 (revenue-impacting, <15min response), P2 (degraded, <30min), P3 (non-critical, <4h), P4 (cosmetic, next sprint)
3. Incident channel created (#inc-YYYY-MM-DD-title)
4. Incident commander assigned (on-call tech lead)
5. Investigation, mitigation, communication (stakeholder updates every 30min for P1)
6. Resolution + deploy fix
7. Post-mortem within 48h (blameless), published in Confluence
8. Action items → Jira tickets, tracked in weekly eng sync

### 3.4 Technical Debt Management
1. Anyone can file TD ticket (Jira label: `tech-debt`)
2. Monthly triage: Tech Leads categorize (security, performance, maintainability, deprecated-deps)
3. Impact scoring: blast radius × effort × risk
4. Sprint allocation: 20% capacity dedicated to tech debt (pol. target, actual ~12%)
5. Quarterly tech debt review with CTO (trends, KPIs)

### 3.5 On-Call & Observability
1. Weekly rotation per team, PagerDuty managed
2. Runbooks per service in Confluence (but 30% outdated)
3. SLOs defined per critical service (uptime, latency p99, error rate)
4. Error budget tracking monthly
5. Quarterly review of SLO breaches

---

## 4. Knowledge Graph — Entity typy

```json
{
  "entity_types": [
    {
      "type": "Service",
      "attributes": ["name", "type", "language", "framework", "team_owner", "status", "repo_url", "description", "created_date", "last_deploy_date", "test_coverage_pct", "lines_of_code", "tier"],
      "examples": ["user-auth-svc (TypeScript/NestJS, Tier 1)", "payment-gateway (Go, Tier 0 — critical)", "legacy-order-monolith (Java/Spring, Tier 2 — migration pending)", "card-tokenization-proxy (Rust, Tier 1 — experimental)", "php-admin-panel (PHP 7.4, Tier 3 — internal only, deprecated)"]
    },
    {
      "type": "API",
      "attributes": ["name", "version", "protocol", "base_url", "auth_method", "status", "docs_url", "consumer_count", "rate_limit", "breaking_changes"],
      "examples": ["Payments API v3 (REST, active)", "Payments API v1 (REST, deprecated — 12 external consumers still)", "Analytics API (GraphQL, active)", "Inter-service Auth (gRPC, internal)"]
    },
    {
      "type": "Database",
      "attributes": ["name", "engine", "version", "hosting", "size_gb", "backup_policy", "shared", "owner_service"],
      "examples": ["users-pg (PostgreSQL 15, RDS, 45GB, single-owner)", "orders-pg (PostgreSQL 14, RDS, 320GB, SHARED — tech debt)", "cache-redis (Redis 7, ElastiCache)", "search-es (Elasticsearch 8.11, self-managed on EKS)"]
    },
    {
      "type": "Pipeline",
      "attributes": ["name", "type", "trigger", "platform", "stages", "avg_duration_min", "success_rate_pct", "last_failure_reason"],
      "examples": ["payment-gateway-ci (GitHub Actions, PR trigger, 8min, 94%)", "legacy-monolith-ci (Jenkins, PR trigger, 43min, 78% — flaky tests)", "nightly-e2e (GitHub Actions, cron 2AM, 25min, 82%)"]
    },
    {
      "type": "Team",
      "attributes": ["name", "lead", "member_count", "domain", "slack_channel", "on_call_schedule"],
      "examples": ["Payments Squad (8 people, #team-payments)", "Platform/Infra (5 people, #team-platform)", "Growth (6 people, no on-call — no prod services)", "Data Engineering (4 people, Python shop)"]
    },
    {
      "type": "ADR",
      "attributes": ["id", "title", "status", "date", "author", "category", "superseded_by", "linked_incidents"],
      "examples": ["ADR-001 Adopt event-driven architecture (accepted, 2021)", "ADR-015 Use gRPC for inter-service communication (accepted, 2023)", "ADR-007 Use MongoDB for session storage (deprecated, superseded by ADR-022 — Redis)"]
    },
    {
      "type": "Guideline",
      "attributes": ["title", "code", "category", "version", "last_updated", "owner", "compliance_status"],
      "examples": ["API Design Standards v2.1 (current)", "Code Review Checklist v3.0 (current)", "Git Branching Strategy v1.0 (outdated — pre-monorepo, nobody follows)", "Security Coding Guidelines v2.0 (OWASP-based)"]
    },
    {
      "type": "Dependency",
      "attributes": ["name", "ecosystem", "current_version", "latest_version", "license", "cve_count", "cve_critical", "last_updated"],
      "examples": ["express@4.18.2 (npm, 0 CVE)", "lodash@4.17.19 (npm, 2 CVE — 1 critical, not updated)", "spring-boot@2.7.18 (maven, EOL — tech debt)", "kafka-go@0.4.47 (go, 0 CVE)"]
    },
    {
      "type": "Environment",
      "attributes": ["name", "type", "cloud_provider", "region", "url", "auto_deploy", "access_control"],
      "examples": ["dev (AWS eu-central-1, auto-deploy on merge to dev)", "staging (AWS eu-central-1, auto-deploy on merge to main)", "prod-eu (AWS eu-central-1, canary, manual approval)", "prod-us (AWS us-east-1, canary, manual approval)"]
    },
    {
      "type": "Incident",
      "attributes": ["id", "title", "severity", "status", "detected_at", "resolved_at", "ttd_minutes", "ttr_minutes", "rca_status", "root_cause_category", "on_call_person"],
      "examples": ["INC-034 Payment timeout spike (P1, Black Friday 2023, TTR 47min, root cause: connection pool exhaustion)", "INC-067 Auth service OOM (P2, 2024-03, TTR 12min, memory leak in JWT validation)", "INC-091 Nightly e2e pipeline broken 5 days (P4, flaky Playwright tests, nobody noticed)"]
    },
    {
      "type": "TechDebt",
      "attributes": ["id", "title", "category", "priority", "estimated_effort_days", "impact", "created_date", "status", "blocked_by"],
      "examples": ["TD-001 Decompose legacy-order-monolith (maintainability, P1, 120 days, blocked_by: TD-005)", "TD-012 Upgrade spring-boot from 2.7 to 3.x (deprecated-deps, P2, 15 days)", "TD-034 Eliminate shared orders-pg database (architecture, P2, 25 days)", "TD-045 Migrate Jenkins to GitHub Actions for monolith (tooling, P3, 8 days — 'in progress' 18 months)"]
    },
    {
      "type": "SLO",
      "attributes": ["name", "service", "metric", "target", "current_value", "error_budget_remaining_pct", "window"],
      "examples": ["payment-gateway availability 99.95% (current: 99.92%, error budget: 23%)", "auth-svc latency p99 < 200ms (current: 185ms, OK)", "legacy-monolith availability — no SLO defined (gap)"]
    },
    {
      "type": "Runbook",
      "attributes": ["title", "service", "last_updated", "author", "status", "linked_alerts"],
      "examples": ["payment-gateway: High Error Rate (updated 2024-06, current)", "auth-svc: OOM Recovery (updated 2023-01, OUTDATED)", "legacy-monolith: Manual Deploy Steps (updated 2022-08, OUTDATED)"]
    },
    {
      "type": "FeatureFlag",
      "attributes": ["name", "service", "status", "created_date", "owner", "description", "stale"],
      "examples": ["ff_multi_currency (payment-gateway, enabled 40% rollout)", "ff_new_onboarding_flow (frontend, disabled — experiment ended, flag not cleaned)", "ff_graphql_analytics (analytics-svc, fully enabled — can be removed, stale)"]
    }
  ]
}
```

---

## 5. Knowledge Graph — Vztahové typy (edges)

```json
{
  "relationship_types": [
    {
      "type": "DEPENDS_ON",
      "from": "Service",
      "to": "Service",
      "attributes": ["protocol", "sync_async", "criticality", "circuit_breaker"]
    },
    {
      "type": "EXPOSES",
      "from": "Service",
      "to": "API",
      "attributes": ["endpoint_count", "rate_limit"]
    },
    {
      "type": "CONSUMES",
      "from": "Service",
      "to": "API",
      "attributes": ["usage_frequency", "fallback_strategy", "version_pinned"]
    },
    {
      "type": "USES_DATABASE",
      "from": "Service",
      "to": "Database",
      "attributes": ["access_type", "connection_pool_size", "shared_violation"]
    },
    {
      "type": "OWNED_BY",
      "from": "Service",
      "to": "Team",
      "attributes": ["since", "on_call"]
    },
    {
      "type": "BUILT_BY",
      "from": "Pipeline",
      "to": "Service",
      "attributes": ["stage_count", "artifact_type"]
    },
    {
      "type": "DEPLOYS_TO",
      "from": "Pipeline",
      "to": "Environment",
      "attributes": ["strategy", "approval_required"]
    },
    {
      "type": "DECIDED_IN",
      "from": "Service",
      "to": "ADR",
      "attributes": ["relevance"]
    },
    {
      "type": "FOLLOWS",
      "from": "Team",
      "to": "Guideline",
      "attributes": ["compliance_level", "exceptions_noted"]
    },
    {
      "type": "HAS_DEPENDENCY",
      "from": "Service",
      "to": "Dependency",
      "attributes": ["scope", "pinned", "update_blocked_by"]
    },
    {
      "type": "AFFECTED",
      "from": "Incident",
      "to": "Service",
      "attributes": ["impact_level", "downtime_minutes"]
    },
    {
      "type": "CAUSED_BY",
      "from": "Incident",
      "to": "TechDebt",
      "attributes": ["contributing_factor"]
    },
    {
      "type": "LED_TO",
      "from": "Incident",
      "to": "ADR",
      "attributes": ["preventive_measure"]
    },
    {
      "type": "RELATES_TO",
      "from": "TechDebt",
      "to": "Service",
      "attributes": ["affected_component"]
    },
    {
      "type": "MONITORS",
      "from": "SLO",
      "to": "Service",
      "attributes": ["alert_threshold"]
    },
    {
      "type": "DOCUMENTED_IN",
      "from": "Runbook",
      "to": "Service",
      "attributes": ["coverage"]
    },
    {
      "type": "CONTROLS",
      "from": "FeatureFlag",
      "to": "Service",
      "attributes": ["rollout_pct"]
    },
    {
      "type": "BLOCKS",
      "from": "TechDebt",
      "to": "TechDebt",
      "attributes": ["reason"]
    }
  ]
}
```

---

## 6. Generovací pravidla

### 6.1 Objemové parametry
- Services: 18–35 (microservices + 1 monolith + 1 deprecated)
- APIs: 25–50 (including deprecated versions)
- Databases: 8–15
- Pipelines: 25–45
- Teams: 6–10
- ADR: 20–40 (including superseded/deprecated)
- Guidelines: 15–25
- Dependencies: 80–250
- Environments: 4–6
- Incidents: 40–90 (12 months history)
- Tech Debt: 25–55
- SLOs: 10–20 (not all services have them)
- Runbooks: 12–25 (some outdated)
- Feature Flags: 10–20 (some stale)

### 6.2 Pravidla hustoty vazeb
- Každá service → 2–6 service dependencies
- Každá service → 1–3 APIs exposed, 1–5 consumed
- Každá service → 1–2 databases (2 shared = tech debt)
- Každá service → 8–25 dependencies
- Každý tým → 2–5 services
- Každý incident → 1–3 affected services, 0–1 caused_by tech debt
- Celkový počet vazeb: 1000–3500

### 6.3 Konzistenční pravidla
- Service dependency graph: preferovaný DAG, 1–2 cykly explicitně označené jako tech debt
- API: v1 < v2 < v3, deprecated versions musí mít consumer_count > 0 (proto je nelze smazat)
- Pipeline success rate: legacy monolith < 85%, moderní services > 90%
- Pipeline duration: monolith 40–50min, microservices 5–15min
- Incident severity distribution: ~5% P1, ~15% P2, ~40% P3, ~40% P4
- Incident TTR distribution: P1 median 30–60min, P2 15–30min, P3 hours, P4 days
- SLO: critical services (Tier 0–1) mají SLO, Tier 2–3 nemají (gap)
- Runbook: 30% outdated (last_updated > 12 months ago)
- Feature flags: 20% stale (experiment ended, flag not removed)
- Test coverage: platforma >80%, monolith ~55%, PHP admin ~12%

### 6.4 Architektonická pravidla
- API gateway je entry point pro external APIs
- Kafka je event backbone — 5–8 services publish/consume events
- Shared databases explicitně označeny (tech debt TD-034)
- Each prod service MUST have pipeline (except PHP admin — manual deploy, tech debt)
- Tier 0 services (payment-gateway, auth) have stricter SLOs and on-call

---

## 7. Anti-patterns & Realism Rules

1. **`legacy-order-monolith`** — Java, 180k LOC, Jenkins CI (43min builds), 55% test coverage, owned by "everyone" (= nobody), no SLO, runbook outdated
2. **`php-admin-panel`** — PHP 7.4, no CI pipeline, manual deploy via SSH, test coverage 12%, deprecated but 15 internal users depend on it
3. **Shared database `orders-pg`** — used by legacy-monolith AND order-events-processor (shared_violation=true, tech debt)
4. **Deprecated API v1** still consumed by 12 external partners who refuse to migrate
5. **ADR-007 (MongoDB for sessions)** superseded by ADR-022 (Redis) but migration only 70% complete
6. **Guideline "Git Branching Strategy v1.0"** — nobody follows it since monorepo adoption, compliance_level: "none"
7. **Jenkins ↔ GitHub Actions** — two CI systems coexist, migration "in progress" since 2023
8. **Tech debt TD-001 (decompose monolith)** blocked by TD-005 (extract shared DB) blocked by TD-034 (define service boundaries) — chain
9. **Feature flag `ff_new_onboarding_flow`** disabled, experiment ended 6 months ago, nobody cleaned up
10. **Incident INC-091** — P4, nightly e2e broken for 5 days, nobody noticed because alerts went to wrong Slack channel

---

## 8. Narrative Vignettes

### Vignette 1: Black Friday Incident
November 2023. Marketing campaign drives 3x normal traffic. Payment-gateway connection pool to orders-pg exhausts at 16:42 CET (Friday). Datadog alert fires, PagerDuty pages on-call (Tomáš K.). TTD: 4 minutes. Investigation reveals shared database `orders-pg` is the bottleneck — legacy-monolith holds long transactions. Mitigation: increase pool size, add circuit breaker to payment-gateway. TTR: 47 minutes. Revenue impact: ~120k CZK in failed transactions. Post-mortem leads to ADR-018 (circuit breaker adoption) and escalates tech debt TD-034 (eliminate shared DB) to P1. Six months later, circuit breakers are in place but shared DB still exists.

### Vignette 2: The Immortal PHP Admin
php-admin-panel was "temporary" in 2019. Now 15 people in ops/finance use it daily for manual refunds, user lookups, and report exports. It has no CI, no tests, no monitoring. In March 2024, someone deployed a change via SSH that broke the refund flow for 2 days — nobody in engineering knew because there's no alerting. Tech debt ticket TD-052 exists but priority is P4 because "it's internal only."

### Vignette 3: The API v1 Zombie
Payments API v1 was deprecated in Q2 2023. API v3 has been stable for 9 months. But 12 external partners (B2B integrations) still use v1. Partnership team negotiated migration deadlines but 4 partners haven't responded. v1 has known issues (no pagination, inconsistent error codes) generating 5+ support tickets/month. There's a feature flag `ff_v1_deprecation_notice` that adds deprecation headers but it's been "coming soon" for 8 months.

---

## 9. Demo Scenarios

1. **"Jaké services závisí na payment-gateway a co se stane, když spadne?"** → Dependency graph traversal + SLO + affected teams
2. **"Kde máme security vulnerabilities v dependencies?"** → Dependency nodes s cve_critical > 0, propojené na services
3. **"Proč trvá build monolithu 45 minut?"** → Pipeline node + shared DB tech debt + Jenkins legacy
4. **"Kolik tech debt máme a co blokuje co?"** → Tech debt graph s BLOCKS edges
5. **"Které runbooks jsou outdated?"** → Runbook nodes s last_updated > 12M
6. **"Jaký je blast radius Kafka výpadku?"** → Services s DEPENDS_ON Kafka (event backbone)
7. **"Které API verze jsou deprecated ale stále používané?"** → API nodes s status=deprecated, consumer_count > 0
8. **"Jak probíhá onboarding nového vývojáře?"** → Guidelines, Getting Started docs (including outdated ones), dev environment setup

---

## 10. Vzorová JSON struktura

```json
{
  "nodes": [
    {
      "id": "svc_001",
      "type": "Service",
      "name": "payment-gateway",
      "type_detail": "microservice",
      "language": "Go",
      "framework": "stdlib + chi router",
      "team_owner": "team_payments",
      "status": "active",
      "repo_url": "github.com/finbee/payment-gateway",
      "description": "Core payment processing, bank API integration, transaction management",
      "created_date": "2020-06-15",
      "last_deploy_date": "2025-05-28",
      "test_coverage_pct": 87,
      "lines_of_code": 24500,
      "tier": 0
    },
    {
      "id": "svc_012",
      "type": "Service",
      "name": "legacy-order-monolith",
      "type_detail": "monolith",
      "language": "Java",
      "framework": "Spring Boot 2.7",
      "team_owner": null,
      "status": "active",
      "repo_url": "github.com/finbee/order-service",
      "description": "Legacy order management, billing, invoicing. Migration to microservices in progress since 2022.",
      "created_date": "2019-01-10",
      "last_deploy_date": "2025-05-15",
      "test_coverage_pct": 55,
      "lines_of_code": 182000,
      "tier": 2
    }
  ],
  "edges": [
    {
      "id": "edge_001",
      "type": "DEPENDS_ON",
      "from": "svc_001",
      "to": "svc_012",
      "protocol": "REST",
      "sync_async": "sync",
      "criticality": "high",
      "circuit_breaker": true
    },
    {
      "id": "edge_002",
      "type": "USES_DATABASE",
      "from": "svc_012",
      "to": "db_003",
      "access_type": "read_write",
      "connection_pool_size": 50,
      "shared_violation": true
    }
  ]
}
```

---

## 11. Zadání pro Claude Code

### Krok 1: Vygeneruj JSON schema
Vytvoř `swdev_schema.json` s rozšířenými entity typy (Service, API, Database, Pipeline, Team, ADR, Guideline, Dependency, Environment, Incident, TechDebt, SLO, Runbook, FeatureFlag). Zahrň enum hodnoty: tier (0–3), status, severity, protocol, ecosystem.

### Krok 2: Vygeneruj seed data
Vytvoř `swdev_seed_data.json` s:
- Kompletním service landscape pro Finbee (doménově specifické názvy — ne generic)
- Reálnými dependency jmény a verzemi (npm, go, maven, pip ecosystem)
- ADR timeline odpovídající company history (sekce 1)
- Incident seed data s reálnými root causes
- OWASP/CVE reference pro security findings

### Krok 3: Vygeneruj generovací script
Vytvoř `generate_swdev_data.py`, který:
- Generuje data PRO FIRMU Finbee — respektuje company profile a technology evolution
- Implementuje anti-patterns ze sekce 7 (legacy monolith, shared DB, zombie APIs, stale flags)
- Generuje realistickou incident historii (clustery po releasech, P1 rare but impactful)
- Vytváří tech debt dependency chain (TD → blocks → TD)
- SLO pouze pro Tier 0–1 services (gap pro ostatní)
- Parametrizovatelný: `--scale small/medium/large`
- Výstup: `swdev_knowledge_graph.json`

### Krok 4: Validace
- Service dependency DAG (cykly explicitně označené)
- Pipeline-environment consistency
- API version ordering + deprecated versions have consumers
- Incident timeline (detected < resolved, TTD + TTR realistic)
- Anti-patterns present (shared DB, deprecated API with consumers, outdated runbooks, stale flags)
- Demo scenario coverage — všech 8 otázek z sekce 9 musí být zodpověditelných
- Statistický report
