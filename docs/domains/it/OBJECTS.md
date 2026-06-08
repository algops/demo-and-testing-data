# IT — Objects (volume & naming)

**Anchor:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md) — all instances `org_id: org:anchor`, `domain_id: it`.  
**Semantic source:** [02_IT_SW_DEVELOPMENT.md](../../02_IT_SW_DEVELOPMENT.md) §6–§8 (Finbee → Meridian Pay per remap table).

## Volume targets (MVP)

| Object-type | Target count | Notes |
|-------------|--------------|-------|
| Service | 18–30 | Include `legacy-ledger-monolith` |
| API | 25–45 | |
| Database | 8–12 | Shared-DB anti-pattern on 2 DBs |
| Pipeline | 25–40 | |
| Environment | 4–6 | |
| Team | 6–10 | Engineering squads |
| Incident | 40–70 | |
| TechDebt | 25–45 | |
| Dependency | 80–180 | |
| ADR, Runbook, Guideline | mix objects + knowledge-docs | per KB_MANIFEST |

## Naming

Use Meridian Pay service names from propozice patterns — domain-specific slugs, not generic `user-service`.
