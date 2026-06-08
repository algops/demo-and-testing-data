# Propozice: ESG Compliance

> **Authoring note:** §1 company profile is a vertical authoring example. Generated demo data uses the anchor tenant [ANCHOR_TENANT.md](ANCHOR_TENANT.md) (Meridian Pay a.s.), not this company as a separate AlgOps tenant.

## 1. Company Profile — fiktivní firma

**Název:** ČEZ Energo Solutions a.s. (fiktivní, inspirováno reálnými CZ energy/utility firmami)
**Sektor:** Energetika a utility — výroba elektřiny, distribuce, OZE projekty
**Velikost:** ~2 500 zaměstnanců, 8 dceřiných společností v CZ, SK, PL, DE
**Obrat:** ~12 mld CZK
**Proč ESG:** Spadá pod CSRD (large undertaking), musí reportovat od FY2024. Má diverzifikovaný energetický mix (uhlí, plyn, solární, větrné), tedy reálná environmentální dilemata. Dodavatelský řetězec zahrnuje těžbu, strojírenství, chemii — relevantní pro CSDDD.

### Historie ESG journey
- **2019:** První dobrovolný CSR report (GRI referenced)
- **2020:** Ustanovení ESG týmu (2 lidi), první carbon footprint kalkulace
- **2021:** Double materiality assessment (externí konzultant), identifikováno 12 materiálních témat
- **2022:** Přijetí Environmental Policy v1.0, začátek sběru Scope 1+2 dat, první supplier screening (top 50 dodavatelů)
- **2023:** CSRD gap analysis, nákup ESG software (Sphera), rozšíření na Scope 3 (kategorie 1, 3, 6), taxonomy eligibility assessment
- **2024:** První CSRD-compliant report, limited assurance od Deloitte, taxonomy alignment pro 4 aktivity, supplier assessment rozšířen na 180 dodavatelů. Ale: data quality pro Scope 3 stále slabá (kategorie 11, 12 chybí), 2 politiky mají expirovaný review date, 30% dodavatelů neodpovědělo na dotazník.

---

## 2. Role a persony

| Role | Popis | Typické dotazy |
|------|-------|----------------|
| ESG Manager | Odpovídá za ESG strategii a reporting, koordinuje sběr dat | "Které ESRS disclosure requirements ještě nemáme pokryté pro FY2024?" |
| Compliance Officer | Zajišťuje soulad s regulací, řeší výzvy od regulátora | "Splňujeme DNSH kritéria pro aktivitu 4.1 — jak to dokládáme?" |
| Sustainability Consultant (ext.) | Externí poradce na CSRD implementaci | "Jaký je gap mezi naším stávajícím GRI reportem a ESRS požadavky?" |
| ESG Data Analyst | Sbírá data z ERP, HR, dodavatelů | "Odkud táhneme data pro metriku E1-6 §44 a jaká je data quality?" |
| Procurement Manager | Řídí dodavatelský řetězec | "Kteří Tier 1 dodavatelé mají high-risk skóre a neprošli re-assessment?" |
| Auditor (ext.) | Ověřuje ESG data pro limited/reasonable assurance | "Kde najdu audit trail pro Scope 2 location-based kalkulaci?" |
| Board Member / CFO | Rozhoduje o ESG investicích | "Kolik nás bude stát dosáhnout 60% taxonomy alignment do 2026?" |
| Facility Manager | Spravuje budovy, energy management | "Jak reportovat spotřebu energie pro 3 pronajaté kanceláře?" |

---

## 3. Klíčové procesy

### 3.1 CSRD Reporting workflow
1. Regulatory scoping — jaké disclosure requirements se na nás vztahují (sector-agnostic + sector-specific ESRS)
2. Materiality assessment update (double materiality — impact + financial)
3. Data collection planning — mapování metrik na datové zdroje a ownery
4. Data gathering (Q1–Q3: průběžný sběr, Q4: finalizace)
5. Metriky kalkulace (GHG Protocol pro emise, vlastní metodika pro social KPIs)
6. Narrative drafting (politiky, targets, governance popis)
7. Internal review — ESG manager + CFO + Legal
8. External assurance engagement (limited → cíl reasonable do 2026)
9. Board approval
10. Publikace (výroční zpráva, standalone sustainability report, ESEF/xHTML)
11. Regulatory submission + Sbírka listin

### 3.2 EU Taxonomy alignment
1. Screening ekonomických aktivit podle NACE kódů (revenue, CapEx, OpEx split)
2. Substantial contribution assessment per aktivita
3. DNSH assessment (6 environmental objectives)
4. Minimum safeguards check (OECD Guidelines, UNGPs, ILO)
5. Kalkulace alignment KPIs (% revenue, CapEx, OpEx)
6. Diskrepance řešení — aktivita eligible ale ne aligned, proč?
7. Year-over-year porovnání a target setting

### 3.3 Supply chain due diligence (CSDDD readiness)
1. Tier mapping — kdo jsou naši dodavatelé, kde sedí, co dodávají
2. Sector + geography risk scoring (SASB materiality map + country risk indices)
3. Distribuce ESG dotazníků (EcoVadis nebo custom)
4. Response tracking — kdo odpověděl, kdo ne (chase proces)
5. Scoring, kategorizace (green / amber / red)
6. Engagement s red-flagged dodavateli (corrective action plans)
7. Continuous monitoring (annual re-assessment, ad-hoc triggers)
8. Reporting dodavatelského řetězce v ESRS S2 a ESRS G1

### 3.4 Interní ESG governance
1. ESG Committee zasedání (kvartálně, zápisy)
2. Politiky lifecycle — drafting, approval, periodic review, update
3. Employee training (ESG awareness, specific role-based)
4. Incident / grievance management (whistleblowing ESG channel)
5. KPI dashboard (monthly update, quarterly board report)
6. Target tracking (science-based targets, diversity targets, governance goals)

---

## 4. Knowledge Graph — Entity typy

```json
{
  "entity_types": [
    {
      "type": "Regulation",
      "attributes": ["name", "abbreviation", "jurisdiction", "effective_date", "scope", "enforcement_body", "status", "transposition_law"],
      "examples": ["CSRD (Directive 2022/2464)", "EU Taxonomy Regulation (2020/852)", "SFDR (2019/2088)", "CSDDD (2024/1760)", "Czech transposition zákon o účetnictví novela"]
    },
    {
      "type": "Standard",
      "attributes": ["name", "code", "issuing_body", "version", "category", "mandatory", "adoption_status"],
      "examples": ["ESRS E1 – Climate Change", "ESRS S1 – Own Workforce", "ESRS G1 – Business Conduct", "GRI 305 – Emissions (voluntary reference)", "TCFD Recommendations (phasing out)"]
    },
    {
      "type": "DisclosureRequirement",
      "attributes": ["code", "standard", "title", "mandatory_for_all", "subject_to_materiality", "datapoints_count"],
      "examples": ["E1-6 Gross Scope 1,2,3 GHG emissions", "S1-6 Characteristics of employees", "G1-3 Prevention and detection of corruption"]
    },
    {
      "type": "Metric",
      "attributes": ["name", "unit", "category", "disclosure_requirement", "data_source", "frequency", "data_quality_score", "methodology"],
      "examples": ["Scope 1 GHG emissions (tCO2e)", "Gender pay gap (%)", "Board independence ratio (%)", "Water withdrawal (m³)"]
    },
    {
      "type": "Policy",
      "attributes": ["title", "code", "version", "owner_department", "approval_date", "next_review_date", "status", "scope", "related_esrs"],
      "examples": ["ENV-POL-001 Environmental Policy v3.2", "SOC-POL-003 Diversity & Inclusion Policy v2.0 (review overdue)", "GOV-POL-001 Anti-corruption Policy v4.0"]
    },
    {
      "type": "Report",
      "attributes": ["title", "type", "reporting_period", "status", "author", "assurance_level", "assurance_provider", "publication_date", "format"],
      "examples": ["Sustainability Report FY2024 (CSRD-compliant, limited assurance)", "Taxonomy Disclosure FY2023 (first year, no assurance)", "Voluntary CSR Report 2019–2022 (GRI referenced)"]
    },
    {
      "type": "EconomicActivity",
      "attributes": ["nace_code", "name", "taxonomy_eligible", "taxonomy_aligned", "revenue_share_pct", "capex_share_pct", "opex_share_pct", "sc_criteria_met", "dnsh_status"],
      "examples": ["4.1 Electricity from solar PV (eligible, aligned)", "4.3 Electricity from wind (eligible, aligned)", "4.29 Electricity from fossil gas (eligible, NOT aligned — DNSH fail)", "7.7 Acquisition of non-residential buildings (eligible, assessment pending)"]
    },
    {
      "type": "Supplier",
      "attributes": ["name", "id", "tier", "country", "sector", "risk_score", "last_assessment_date", "assessment_status", "spend_annual_czk", "critical"],
      "examples": ["Siemens Energy s.r.o. (Tier 1, DE/CZ, low risk)", "Důl Paskov Mining a.s. (Tier 1, CZ, HIGH risk — coal)", "No Name Chemicals Ltd. (Tier 2, IN, risk unknown — no response)"]
    },
    {
      "type": "Risk",
      "attributes": ["name", "category", "subcategory", "severity", "likelihood", "mitigation_status", "risk_owner", "last_reviewed"],
      "examples": ["Carbon tax exposure CZ (E, high severity, medium likelihood)", "Forced labor in cobalt supply chain (S, high, low — but reputational)", "Board diversity non-compliance (G, medium, high)"]
    },
    {
      "type": "Target",
      "attributes": ["name", "category", "baseline_year", "baseline_value", "target_year", "target_value", "current_value", "status", "sbti_validated"],
      "examples": ["Scope 1+2 reduction 42% by 2030 (SBTi validated)", "30% women in senior management by 2027", "Zero coal revenue by 2028"]
    },
    {
      "type": "DataSource",
      "attributes": ["name", "type", "system", "owner_department", "refresh_frequency", "data_quality_rating", "coverage_pct", "known_gaps"],
      "examples": ["SAP ERP – energy invoices (monthly, quality A, 95% coverage)", "HR system – headcount & diversity (quarterly, quality B, missing contractors)", "Supplier portal – ESG questionnaires (annual, quality C, 70% response rate)"]
    },
    {
      "type": "MaterialTopic",
      "attributes": ["name", "category", "impact_score", "financial_score", "material", "stakeholder_relevance"],
      "examples": ["Climate change mitigation (E, impact 9/10, financial 8/10, material=yes)", "Employee health & safety (S, 7/10, 5/10, material=yes)", "Tax transparency (G, 4/10, 3/10, material=no)"]
    },
    {
      "type": "AuditFinding",
      "attributes": ["id", "type", "severity", "metric_affected", "description", "status", "remediation_deadline"],
      "examples": ["AF-2024-003 Scope 2 market-based calculation missing REC certificates (major)", "AF-2024-007 Supplier risk scoring methodology not documented (minor)"]
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
      "type": "REQUIRES_DISCLOSURE",
      "from": "Regulation",
      "to": "DisclosureRequirement",
      "attributes": ["mandatory", "phase_in_year"]
    },
    {
      "type": "CONTAINS_METRIC",
      "from": "DisclosureRequirement",
      "to": "Metric",
      "attributes": ["datapoint_id", "quantitative"]
    },
    {
      "type": "REFERENCES_STANDARD",
      "from": "Regulation",
      "to": "Standard",
      "attributes": ["reference_type", "binding"]
    },
    {
      "type": "MEASURED_FROM",
      "from": "Metric",
      "to": "DataSource",
      "attributes": ["calculation_method", "coverage_pct", "quality_assessment"]
    },
    {
      "type": "ADDRESSES_TOPIC",
      "from": "Policy",
      "to": "MaterialTopic",
      "attributes": ["coverage_level"]
    },
    {
      "type": "MITIGATES",
      "from": "Policy",
      "to": "Risk",
      "attributes": ["residual_risk_level", "control_type"]
    },
    {
      "type": "APPLIES_TO",
      "from": "Regulation",
      "to": "EconomicActivity",
      "attributes": ["eligibility_status", "assessment_year"]
    },
    {
      "type": "ASSESSED_FOR",
      "from": "Supplier",
      "to": "Risk",
      "attributes": ["assessment_date", "score", "method"]
    },
    {
      "type": "REPORTED_IN",
      "from": "Metric",
      "to": "Report",
      "attributes": ["value", "period", "assured", "page_reference"]
    },
    {
      "type": "OWNS",
      "from": "DataSource",
      "to": "Metric",
      "attributes": ["responsibility_type", "data_quality_score"]
    },
    {
      "type": "TRACKS_TARGET",
      "from": "Target",
      "to": "Metric",
      "attributes": ["measurement_method"]
    },
    {
      "type": "RAISED_ON",
      "from": "AuditFinding",
      "to": "Metric",
      "attributes": ["finding_type"]
    },
    {
      "type": "MATERIAL_FOR",
      "from": "MaterialTopic",
      "to": "Standard",
      "attributes": ["determines_disclosure"]
    },
    {
      "type": "SUPPLIES_TO",
      "from": "Supplier",
      "to": "EconomicActivity",
      "attributes": ["supply_category", "criticality"]
    },
    {
      "type": "HAS_SUBREGULATION",
      "from": "Regulation",
      "to": "Regulation",
      "attributes": ["relationship"]
    }
  ]
}
```

---

## 6. Generovací pravidla

### 6.1 Objemové parametry
- Regulace: 15–25
- Standardy: 30–50 (ESRS sekce + GRI + TCFD + SASB)
- Disclosure Requirements: 80–120 (mapované z ESRS)
- Metriky: 100–200
- Politiky: 20–40
- Reporty: 8–15 (across FY2019–FY2024, ukazující evoluci)
- Ekonomické aktivity: 10–25
- Dodavatelé: 80–250 (Tier 1–3, s realistickým long-tail)
- Rizika: 30–60
- Targety: 10–20
- Datové zdroje: 15–30
- Materiální témata: 15–25 (z toho ~12 material)
- Audit findings: 8–15

### 6.2 Pravidla hustoty vazeb
- Každý disclosure requirement → 1–5 metrik
- Každá metrika → 1–3 datové zdroje
- Každý dodavatel → 2–5 rizik
- Každý report → 20–60 metrik
- Každý target → 1–2 metriky
- Celkový počet vazeb: 800–2500

### 6.3 Konzistenční pravidla
- Scope 1/2/3 emise v tCO2e, konzistentní s GHG Protocol kategorizací
- Taxonomy alignment % ≤ eligibility %
- Policy dates < report dates (ale některé policies mají expired review — realism)
- ESRS references musí odpovídat reálným ESRS Set 1 kódům
- Assurance: FY2019–2022 = none, FY2023 = none, FY2024 = limited
- Targets musí mít baseline < target year, current_value konzistentní s trajectory
- Audit findings musí odkazovat na metriky, které reálně existují v grafu
- Supplier risk score musí korelovat se sektorem a geografií

### 6.4 Temporální pravidla
- Reports: FY2019 (GRI basic) → FY2024 (CSRD full) — viditelná maturita
- Policy versions: inkrementální, některé s propadem (review overdue)
- Supplier assessments: rozložené přes 18M, s 20–30% non-respondents
- Regulace effective dates: reálné (CSRD 2024, Taxonomy 2020/2022, CSDDD 2026)
- Targets: baseline typicky FY2020 nebo FY2022

---

## 7. Anti-patterns & Realism Rules

Claude Code MUSÍ záměrně generovat tyto „nedokonalosti":

1. **2–3 politiky s `next_review_date` v minulosti** (expired review, nikdo nezrevidoval)
2. **20–30% dodavatelů s `assessment_status: "no_response"`** nebo `risk_score: null`
3. **Scope 3 metriky s `data_quality_score: "C"` nebo `"D"`** — category 11, 12 chybí úplně
4. **1 ekonomická aktivita `taxonomy_eligible: true` ale `taxonomy_aligned: false`** s reálným důvodem (DNSH fail na climate adaptation)
5. **1 audit finding statusu `"open"` s prošlým `remediation_deadline`**
6. **Starší reporty (FY2019–2022) s `assurance_level: "none"` a menším počtem metrik** — viditelná evoluce
7. **2 metriky s `methodology: "estimated"` místo `"calculated"`**
8. **1 target s `status: "off_track"` a current_value horší než trajectory**
9. **Duplikátní datový zdroj** (HR systém poskytuje data do 2 metrik s různou quality)
10. **1 disclosure requirement s `coverage: "partial"` v reportu** — firma ví, že nesplňuje plně

---

## 8. Narrative Vignettes (vzory pro Claude Code)

### Vignette 1: Scope 3 data gap
Firma reportuje Scope 3 emise, ale jen pro kategorie 1 (purchased goods), 3 (fuel & energy) a 6 (business travel). Kategorie 11 (use of sold products) a 12 (end-of-life) chybí, protože energetická firma prodává elektřinu — metodicky sporné, zda to počítat. ESG manager to řeší s konzultantem, v reportu je disclosure s vysvětlením "not material / methodology under development". Audit finding AF-2024-005 na to upozorňuje jako minor observation.

### Vignette 2: Dodavatel-problém
Důl Paskov Mining dodává uhlí pro jednu z thermal power plants. ESG assessment ukazuje high risk (fossil fuel, CZ báňský sektor). Firma má target "zero coal revenue by 2028" → aktivita 4.29 (fossil gas) je taxonomy eligible ale NOT aligned (DNSH fail). V supply chain due diligence je tento dodavatel "red flagged", corrective action plan = postupný phase-out. Ale stále 15% revenue jde z uhelných aktivit.

### Vignette 3: Policy review overdue
Diversity & Inclusion Policy v2.0 byla schválena v lednu 2022 s review cycle "biennial". Je červen 2025 a nikdo ji nezrevidoval — `next_review_date: "2024-01-15"` je v minulosti. Mezitím se změnily ESRS S1 požadavky na disclosure o diverzitě. Audit finding AF-2024-008 (minor) to zachytil.

---

## 9. Demo Scenarios (acceptance test)

Na demu musí vygenerovaný knowledge graf umět odpovědět na tyto otázky:

1. **"Které ESRS disclosure requirements ještě nemáme pokryté?"** → Graf musí ukázat DR s `coverage: "none"` nebo `"partial"` propojené na regulaci.
2. **"Jaká je naše taxonomy alignment a proč nejsme na 100%?"** → Ekonomické aktivity s eligible=true, aligned=false + důvod (DNSH fail).
3. **"Kteří dodavatelé jsou high-risk a neprošli assessment?"** → Filtr na `risk_score >= 7` AND `assessment_status != "completed"`.
4. **"Jaký je trend našich Scope 1+2 emisí?"** → Metrika reportovaná across FY2020–FY2024 s hodnotami v edges REPORTED_IN.
5. **"Máme nějaké otevřené audit findings?"** → AF s `status: "open"`.
6. **"Které politiky potřebují revizi?"** → Policies s `next_review_date < today`.
7. **"Jaká je kvalita našich ESG dat?"** → Data sources s quality ratings, metriky s estimated methodology.
8. **"Jsme on-track s SBTi targety?"** → Targets s trajectory vs current_value.

---

## 10. Vzorová JSON struktura

```json
{
  "nodes": [
    {
      "id": "reg_001",
      "type": "Regulation",
      "name": "Corporate Sustainability Reporting Directive",
      "abbreviation": "CSRD",
      "jurisdiction": "EU",
      "effective_date": "2024-01-01",
      "scope": "Large undertakings, listed SMEs (phased)",
      "enforcement_body": "National competent authorities",
      "status": "in_force",
      "transposition_law": "Novela zákona o účetnictví 2024"
    },
    {
      "id": "dr_012",
      "type": "DisclosureRequirement",
      "code": "E1-6",
      "standard": "ESRS E1",
      "title": "Gross Scopes 1, 2, 3 and Total GHG emissions",
      "mandatory_for_all": true,
      "subject_to_materiality": false,
      "datapoints_count": 18
    },
    {
      "id": "met_001",
      "type": "Metric",
      "name": "Scope 1 GHG emissions",
      "unit": "tCO2e",
      "category": "Environmental",
      "disclosure_requirement": "E1-6",
      "data_source": "ds_001",
      "frequency": "annual",
      "data_quality_score": "B",
      "methodology": "calculated"
    },
    {
      "id": "sup_042",
      "type": "Supplier",
      "name": "Důl Paskov Mining a.s.",
      "tier": 1,
      "country": "CZ",
      "sector": "Coal mining",
      "risk_score": 9.2,
      "last_assessment_date": "2024-03-15",
      "assessment_status": "completed",
      "spend_annual_czk": 280000000,
      "critical": true
    }
  ],
  "edges": [
    {
      "id": "edge_001",
      "type": "REQUIRES_DISCLOSURE",
      "from": "reg_001",
      "to": "dr_012",
      "mandatory": true,
      "phase_in_year": null
    },
    {
      "id": "edge_002",
      "type": "CONTAINS_METRIC",
      "from": "dr_012",
      "to": "met_001",
      "datapoint_id": "E1-6.44a",
      "quantitative": true
    },
    {
      "id": "edge_050",
      "type": "REPORTED_IN",
      "from": "met_001",
      "to": "rep_005",
      "value": 145230,
      "period": "FY2024",
      "assured": true,
      "page_reference": "p. 47"
    }
  ]
}
```

---

## 11. Zadání pro Claude Code

### Krok 1: Vygeneruj JSON schema
Vytvoř `esg_schema.json` definující všechny entity typy (sekce 4) a relationship typy (sekce 5). Zahrň validační pravidla: povinné atributy, enum hodnoty, formátové constrainty. Schema musí reflektovat nový entity typ `DisclosureRequirement`, `Target`, `MaterialTopic`, `AuditFinding`.

### Krok 2: Vygeneruj seed data
Vytvoř `esg_seed_data.json` s:
- Reálnými ESRS Set 1 disclosure requirements (E1–E5, S1–S4, G1) s kódy a titulky
- Reálnými EU regulacemi s effective dates
- Reálnými NACE kódy pro energetiku (sekce D — electricity)
- Taxonomy screening criteria pro vybrané aktivity
- Reálnými GHG Protocol scope/category definicemi
- Seed pro company profile (sekce 1)

### Krok 3: Vygeneruj generovací script
Vytvoř `generate_esg_data.py`, který:
- Generuje data PRO KONKRÉTNÍ FIRMU z Company Profile (energetika/utility)
- Respektuje historickou timeline (FY2019–FY2024 evoluce)
- Implementuje anti-patterns ze sekce 7 (expired policies, data gaps, non-respondent suppliers)
- Vytváří realistickou supply chain (Tier 1 = key industrial suppliers, Tier 2–3 = long tail)
- Generuje audit findings propojené na reálné metriky
- Parametrizovatelný: `--scale small/medium/large`
- Výstup: `esg_knowledge_graph.json`

### Krok 4: Validace
- Referenční integrita (žádné dangling edges)
- ESRS kódy odpovídají reálným disclosure requirements
- Taxonomy alignment ≤ eligibility per aktivita
- Temporal consistency (baseline year < target year, policy date < report date)
- Anti-patterns present (min. 2 expired policies, min. 15% non-respondent suppliers, min. 1 off-track target)
- Demo scenario coverage — ověření, že graf odpovídá na všech 8 otázek ze sekce 9
- Statistický report (počty, hustota, data quality distribution)
