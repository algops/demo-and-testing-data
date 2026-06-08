# Domain modules & org layer

Demo data uses **one anchor tenant** ([ANCHOR_TENANT.md](../ANCHOR_TENANT.md)) with five enabled domain modules. This document defines org-layer object-types and the **org-bridge relationship matrix** (plan Part 1.3).

---

## Scoping model

| Field | Values | Scope |
|-------|--------|-------|
| `org_id` | `org:anchor` | Exactly one per demo corpus — AlgOps tenant boundary |
| `domain_id` | `esg`, `it`, `legal`, `tax`, `hr`, `shared` | Module tag on every entity |
| `enabled_domains` | all five on anchor org | Product upsell metadata |

**Edge tiers:**

1. **Domain-native** — both endpoints share the same `domain_id` (not `shared`). Must satisfy `docs/domains/{domain}/RELATIONSHIP_MATRIX.md`.
2. **Org-bridge** — one endpoint is org-layer (`domain_id: shared`), the other is domain-scoped. Must satisfy the matrix below.
3. **Forbidden** — domain-native type ↔ domain-native type with different `domain_id` (e.g. IT `Service` → Legal `Matter` without bridging via `person` or `system`).

---

## Org-layer object-types (`domain_id: shared`)

Documented once here; referenced by all domain catalogues. HR owns schema for `employee`; other domains reference via bridge edges.

| Slug | Czech label | Owner domain | Notes |
|------|-------------|--------------|-------|
| `organization` | Organizace | shared | Single anchor instance — Meridian Pay a.s. |
| `person` | Osoba | shared | Canonical identity; HR materializes employment attrs on `employee` |
| `employee` | Zaměstnanec | hr | `instance_of` person optional; HR datapoints authoritative |
| `department` | Oddělení | hr | Org chart units |
| `team` | Tým | it, hr | Engineering squads; legal practice areas may mirror as team |
| `system` | Systém | shared | GitLab, SuccessFactors, iManage — one record, multi-domain `syncs` |
| `vendor` | Dodavatel / partner | shared | External counsel, tax advisor, auditors |

Domain-specific object-types (Service, Matter, Metric, …) live in each `docs/domains/{domain}/OBJECT_TYPES.md`.

---

## Org-bridge relationship matrix

Legend: **A** = allowed, **O** = optional, **—** = forbidden.

Bridge edges use AlgOps `related_to` unless noted. All must also satisfy the global endpoint matrix (plan Part 1.1).

| org-layer (origin) | IT | Legal | Tax | HR | ESG |
|--------------------|----|-------|-----|----|-----|
| **person** → domain object | O → Incident (reporter) | A → Matter (responsible_lawyer) | O → Engagement (owner) | A → Employee | O → AuditFinding (owner) |
| **employee** → domain object | A → Incident, TechDebt | A → Matter, Contract | O → Engagement | A → Training, GrievanceCase | O → Policy (owner) |
| **department** → domain object | A → Team, Service (owner_dept) | A → LegalArea | O → Engagement | A → Process | O → MaterialTopic |
| **team** → domain object | A → Service | A → Matter | — | A → Role | — |
| **system** → domain object | A → Integration (1:1 link) | A → Integration | A → Integration | A → Integration | A → DataSource |
| **vendor** → domain object | O → Contract | A → Matter (external_counsel) | A → Engagement (advisory) | — | A → Supplier |
| **organization** → domain object | A → Service (org scope) | A → Matter | A → Engagement | A → Policy | A → Report |

| domain object (origin) | org-layer (destination) |
|------------------------|-------------------------|
| IT Integration → **system** | A (`related_to` "implements") |
| Legal Matter → **vendor** | O (external counsel) |
| Tax Engagement → **vendor** | O (external advisor) |
| HR Employee → **person** | A |
| ESG Supplier → **vendor** | O (when supplier is also contracted vendor) |

**Inverse:** Org-layer as destination follows the same allowance (symmetric `related_to`).

---

## Domain catalogue index

| `domain_id` | Folder | Propozice source | Module focus |
|-------------|--------|------------------|--------------|
| `esg` | [esg/](esg/) | [01_ESG_COMPLIANCE.md](../01_ESG_COMPLIANCE.md) | CSRD, taxonomy, suppliers |
| `it` | [it/](it/) | [02_IT_SW_DEVELOPMENT.md](../02_IT_SW_DEVELOPMENT.md) | Engineering, incidents, ADRs |
| `legal` | [legal/](legal/) | [03_LEGAL.md](../03_LEGAL.md) | In-house legal, contracts, matters |
| `tax` | [tax/](tax/) | [04_TAX_ACCOUNTING.md](../04_TAX_ACCOUNTING.md) | Group tax, filings, deadlines |
| `hr` | [hr/](hr/) | [05_HR_SOP.md](../05_HR_SOP.md) | SOPs, employees, training |

Each catalogue file must reference [ANCHOR_TENANT.md](../ANCHOR_TENANT.md) for naming and volume targets — not propozice §1 company names.

---

## Catalogue file set (per domain)

| File | Purpose |
|------|---------|
| `OBJECT_TYPES.md` | AlgOps slugs from propozice §4 |
| `OBJECTS.md` | Volumes & vignettes — anchor naming |
| `DATAPOINTS.md` | Fields from propozice `attributes[]` |
| `VALUES.md` | Warehouse materialization rules |
| `AGENTS.md` | Use-case agents (not job titles) |
| `INTEGRATIONS.md` | Sources, tools, destinations |
| `RELATIONSHIP_MATRIX.md` | Domain-native edges + AlgOps projection |
| `KB_MANIFEST.md` | Knowledge tab file list |

Authoring order: IT + HR first, then Legal + Tax, then ESG.
