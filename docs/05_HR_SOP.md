# Propozice: HR SOP (Standard Operating Procedures)

> **Authoring note:** §1 company profile is a vertical authoring example. Generated demo data uses the anchor tenant [ANCHOR_TENANT.md](ANCHOR_TENANT.md) (Meridian Pay a.s.), not VTM as a separate AlgOps tenant.

## 1. Company Profile — fiktivní firma

**Název:** Výrobní Technologie Morava a.s. (VTM)
**Sektor:** Strojírenská výroba — CNC obráběcí centra, automatizace výrobních linek, aftermarket servis
**Velikost:** ~310 zaměstnanců (175 výroba/servis, 55 engineering/R&D, 35 sales/marketing, 25 admin/finance, 12 HR, 8 management)
**Lokace:** HQ a hlavní výrobní závod Brno-Líšeň, servisní pobočka Praha, R&D centrum Olomouc
**Obrat:** ~1.2 mld CZK
**HR systémy:** SAP SuccessFactors (core HR od 2022, mzdy od 2023), Recruitee (ATS — od 2021), MS Teams, SharePoint (DMS — migrace z sdíleného disku, 70% dokončená), papírové osobní složky stále existují pro pre-2020 zaměstnance

### Historie a "geologické vrstvy"
- **2008:** Firma založena jako rodinný podnik (50 zaměstnanců). HR = 1 mzdová účetní + ředitel firmy dělá vše ostatní. Personalistika v Excelu, mzdy v Premiéře
- **2012–2015:** Růst na 150 zaměstnanců. Přijata první HR manažerka. Směrnice psané ve Wordu, sdílený disk. Benefity: stravenky + 5 sick days
- **2016:** Zákoník práce novela (home office zmínka). Firma ignoruje — "u nás se pracuje v závodě." Interní směrnice stále nemají čísla ani verze
- **2018:** Zákazník z automobilky vyžaduje IATF 16949 — nucená formalizace procesů. HR směrnice poprvé očíslovány (POL-HR-001 atd.), zavedeny záznamy o školeních
- **2019:** Akvizice R&D centra v Olomouci (+30 zaměstnanců, inženýři). Kulturní clash — Olomouc chce flexibilitu, Brno-výroba jede na směny. 2 odlišné pracovní řády
- **2020:** COVID — narychlo sepsaná Remote Work Policy (v1.0, 4 strany, pro kancelářské pozice). Výroba jede dál. 15% zaměstnanců na překážkách v práci. HR team naroste na 4 lidi
- **2021:** Implementace Recruitee (ATS). Onboarding checklist poprvé digitalizován. Ale 50% kroků stále vyžaduje papírový formulář. Fluktuace ve výrobě dosáhne 22% — reakce: zavedení referral programu
- **2022:** SAP SuccessFactors implementace — 14 měsíců trvající projekt, go-live v říjnu. Core HR modul. Ale: historická data (pre-2020) neúplně zmigrována. Leave management modul "Phase 2" — stále v Excelu
- **2023:** Mzdový modul SF go-live (nahrazuje Premiéru). Přechod na cafeteria systém (Benefity a.s.) místo stravenek — ale výrobní zaměstnanci odmítají, chtějí zpět stravenky. Kompromis: dual systém (cafeteria pro THP, stravenky pro výrobu)
- **2024:** Nový zákoník práce amendments (dohody DPP/DPČ, informační povinnost). HR musí aktualizovat 6 směrnic. 3 hotové, 3 "in progress" (= nezměněné). Fluktuace klesla na 14% (trh práce). 1 diskriminační stížnost — whistleblowing kanál existuje na papíře ale nikdo neví jak funguje. Remote Work Policy v2.0 stále platí jen pro kancelář, R&D Olomouc si udělal vlastní neoficiální pravidla.

### Reálný nepořádek
- **2 pracovní řády** — Brno (směnový provoz, 3 směny) a Olomouc (flexibilní, R&D) — formálně mají být sjednoceny od 2020, stále nejsou
- **Leave management v Excelu** — SF modul "Phase 2" odložen na neurčito, Excel "Dovolene_2024.xlsx" sdílený mezi 3 HR admin
- **Papírové osobní složky** — pre-2020 zaměstnanci (95 lidí) mají složky jen v papíru, neúplně naskenované
- **Dual benefit systém** — cafeteria (THP) + stravenky (výroba) — payroll nastavení je noční můra
- **Onboarding: 50% papír** — digitální checklist v Recruitee + papírový formulář pro IT setup, BOZP protokol, klíče
- **Whistleblowing kanál** — směrnice POL-HR-018 existuje od 2023, ale link na formulář nefunguje (IT nikdy nastavilo)
- **Školení BOZP** — evidence ve 3 systémech: papírový prezenční arch (výroba), Excel (admin), SF Learning (od 2024 pro nové zaměstnance)

---

## 2. Role a persony

| Role | Popis | Typické dotazy |
|------|-------|----------------|
| Zaměstnanec (výroba) | Operátor CNC, směnový provoz | "Kolik přesčasů mám letos a jak se proplácejí?" |
| Zaměstnanec (THP) | Kancelářský pracovník, admin/sales | "Můžu pracovat z domova v pátek? A jak to zadám?" |
| Zaměstnanec (R&D Olomouc) | Inženýr, vývoj | "Jaký je postup pro čerpání vzdělávacího budgetu na konferenci v zahraničí?" |
| Manažer (vedoucí výroby) | Řídí směnu, 45 direct reports | "Jak schválím dovolenou pro celou směnu najednou? Ten Excel je katastrofa." |
| HR Business Partner | Strategický HR pro engineering + sales | "Jaký je turnover rate v R&D a co s tím děláme?" |
| HR Admin / Personalista | Operativní HR, smlouvy, evidence | "Kde najdu vzor dodatku ke smlouvě pro změnu úvazku z DPČ na HPP?" |
| Payroll Specialist | Mzdy, odvody | "Jak nastavit cafeteria benefit pro zaměstnance, který přešel z výroby do THP?" |
| L&D Coordinator | Školení, development | "Kteří zaměstnanci mají propadlé BOZP školení?" |
| Nový zaměstnanec (onboarding) | První týden | "Kam mám donést podepsanou smlouvu a kde dostanu klíče?" |
| CFO / Finanční ředitel | Budget, headcount planning | "Jaký je cost-per-hire a jak se meziročně mění?" |
| Ředitel závodu | Celkový provoz Brno | "Máme dost lidí na noční směnu příští měsíc?" |

---

## 3. Klíčové procesy

### 3.1 Životní cyklus zaměstnance
1. Recruitment: hiring request (manažer) → schválení headcount (CFO) → inzerát (Recruitee) → screening → pohovory (2 kola: HR + hiring manager) → nabídka
2. Pre-boarding: smlouva (vzor v SharePointu, ale 3 verze existují) → lékařská prohlídka → IT request
3. Onboarding — Day 1: podpis dokumentů (stále papír), klíče/karta, IT setup, BOZP vstupní školení
4. Onboarding — Week 1: buddy assignment (THP) / mentor (výroba), systémy access, department intro
5. Onboarding — Month 1: GDPR e-learning (SF Learning), department-specific training
6. Probační doba: 30/60/90 day check-in (formulář v SharePointu, compliance ~60% — manažeři zapomínají)
7. Performance management: roční hodnocení (leden–únor), goal setting (březen), mid-year check (červenec — optional, utilization ~30%)
8. Development: IDP (Individual Development Plan) — template existuje, vyplněno u ~40% zaměstnanců
9. Compensation review: annual (duben), band adjustment, promotion
10. Offboarding: výpověď → 2M výpovědní doba → předání agendy → IT deactivation → exit interview (jen pro THP, výroba ne) → výstupní list

### 3.2 Absence management
1. Dovolená: žádost v Excelu "Dovolene_2024.xlsx" → schválení manažerem (email/ústně) → HR admin zapíše do SF
2. Nemocenská: zaměstnanec nahlásí manažerovi → HR admin zapíše → lékařské potvrzení do 3 dnů → karenční doba (nemocenská od 15. dne OSSZ)
3. Sick days: 3 dny/rok (THP), 5 dnů/rok (R&D Olomouc — vlastní pravidlo, nikde formálně), výroba nemá → nerovnost
4. Osobní volno: dle zákoníku práce (svatba 2 dny, pohřeb 1–3 dny, dárcovství krve 1 den, stěhování 1 den)
5. Rodičovská: mateřská (28 týdnů) → rodičovská (do 3–4 let) → návratový proces (re-onboarding light)
6. Home office: POL-HR-012 (THP a kanceláře, max 2 dny/týden), R&D Olomouc má neoficiální "4 dny HO" pravidlo
7. Přesčasy (výroba): evidence v docházkovém systému, schválení vedoucím směny, proplácení nebo náhradní volno

### 3.3 Kompenzace a benefity
1. Mzdová struktura: 8 bandů (B1–B8), base + variabilní (výroba: úkolová mzda/směnové příplatky, THP: roční bonus 0–15%, management: 0–25%)
2. Benefity — univerzální: 5 týdnů dovolené (25 dnů), příspěvek na stravování (stravenky výroba / cafeteria THP), penzijní připojištění 800 CZK/m po zkušební době
3. Benefity — THP/mgmt: MultiSport card (50% employer), vzdělávací budget 25k CZK/rok (utilization 23% — nikdo nečerpá), 3 sick days, home office
4. Benefity — R&D: vzdělávací budget 40k CZK/rok, konferenční budget, 5 sick days (neformální)
5. Benefity — výroba: příplatek za směnnost (dle ZP), příplatek za přesčas 25%, vánoční prémie 1 měsíční plat (performance-based), jubilejní odměny
6. Referral program: 15k CZK za doporučení výrobního zaměstnance (po zkušební době), 25k CZK za inženýra
7. Služební auto: od B6 (manažer), služební telefon od B4

### 3.4 Compliance a policies
1. Zákoník práce (262/2006 Sb.) — základní rámec, novelizace 2023/2024
2. BOZP: školení vstupní + periodické (1x ročně výroba, 1x za 2 roky admin), evidence v 3 systémech (!)
3. PO (požární ochrana): školení 1x za 2 roky, evakuační plán
4. GDPR: interní směrnice POL-HR-015, souhlas se zpracováním OU v pracovní smlouvě, DPO (external)
5. Whistleblowing: POL-HR-018 (od 2023, zákon č. 171/2023 Sb.), formulář NEFUNGUJE
6. Anti-harassment / Code of Conduct: POL-HR-005 v2.0 (2020, update pending per 2024 novelizace)
7. Pracovní řád: 2 verze (Brno směnový, Olomouc flexibilní) — nesjednocené
8. Dress code: výroba = OOPP povinné, kancelář = smart casual (nepsané pravidlo)
9. IT security: POL-IT-003 (hesla, VPN, BYOD) — vlastní IT oddělení, ne HR

### 3.5 Školení a rozvoj
1. Povinná: BOZP vstupní (Day 1), BOZP periodické, PO, GDPR e-learning, řidiči referentských vozidel
2. Odborná (výroba): obsluha CNC strojů, svařování (certifikace dle ČSN EN ISO 9606), jeřábnický průkaz
3. Soft skills: leadership program (B5+, external provider), presentation skills (ad hoc)
4. Technická (R&D): CAD/CAM školení, specifické technologie
5. Jazyková: angličtina (firemní kurzy, 2x týdně, attendance ~55%)
6. Evidence: papírový arch (výroba do 2023), Excel (admin), SF Learning (od 2024 pro nové) — 3 systémy, žádný kompletní přehled

---

## 4. Knowledge Graph — Entity typy

```json
{
  "entity_types": [
    {
      "type": "Policy",
      "attributes": ["title", "code", "category", "version", "effective_date", "next_review_date", "owner", "status", "applies_to", "known_issues", "language"],
      "examples": ["POL-HR-001 Pracovní řád Brno v3.0 (current, směnový provoz)", "POL-HR-001B Pracovní řád Olomouc v1.0 (current, flexibilní — should be merged with 001)", "POL-HR-012 Remote Work Policy v2.0 (current, THP only — R&D has unofficial rules)", "POL-HR-018 Whistleblowing v1.0 (current on paper, form link broken)", "POL-HR-005 Code of Conduct v2.0 (review overdue — 2024 amendment not incorporated)"]
    },
    {
      "type": "Process",
      "attributes": ["name", "code", "category", "owner", "sla_days", "approval_chain", "system", "digitalization_pct", "known_bottleneck"],
      "examples": ["PRO-HR-001 Leave Request (SLA 3 days, Excel-based, 0% digital in SF)", "PRO-HR-012 Onboarding Checklist (SLA 5 days, 50% digital, 50% paper)", "PRO-HR-025 Expense Reimbursement (SLA 10 days, SAP, fully digital)", "PRO-HR-030 Whistleblowing Report (SLA N/A, form link broken)"]
    },
    {
      "type": "Benefit",
      "attributes": ["name", "type", "provider", "monthly_value", "eligibility", "enrollment_period", "taxable", "utilization_pct", "applies_to", "status"],
      "examples": ["MultiSport card (wellness, 50% employer, THP only, after probation, utilization 68%)", "Vzdělávací budget 25k CZK/rok (development, THP, utilization 23% — nobody uses it)", "Stravenky 120 CZK/den (meal, výroba only, Sodexo, taxable partly)", "Cafeteria 2500 CZK/m (meal+wellness+culture, THP, Benefity a.s., since 2023)", "Vánoční prémie (bonus, výroba, performance-based, status: active)"]
    },
    {
      "type": "Role",
      "attributes": ["title", "code", "department", "level", "band", "reports_to", "headcount", "location", "shift_work"],
      "examples": ["CNC Operator (ROL-MFG-010, Manufacturing, L2, B3, reports to Shift Supervisor, HC 35, Brno, 3-shift)", "Software Engineer R&D (ROL-RND-005, R&D, L3, B5, reports to R&D Manager, HC 12, Olomouc, no shift)", "HR Business Partner (ROL-HR-003, HR, L4, B6, reports to HR Director, HC 2, Brno/remote, no shift)"]
    },
    {
      "type": "Department",
      "attributes": ["name", "code", "head", "headcount", "budget_center", "location", "interim_head"],
      "examples": ["Manufacturing (DEP-MFG, head: Ing. Procházka, HC 175, Brno)", "R&D (DEP-RND, head: Ing. Dvořák, HC 55, Olomouc)", "Sales (DEP-SAL, head: INTERIM — Mgr. Nováková since Sep 2024, HC 20, Brno+Praha)"]
    },
    {
      "type": "Training",
      "attributes": ["name", "code", "type", "mandatory", "frequency", "duration_hours", "provider", "certification", "evidence_system", "compliance_rate_pct"],
      "examples": ["BOZP vstupní školení (TRN-001, mandatory, once, 4h, internal, paper arch, 100%)", "BOZP periodické — výroba (TRN-002, mandatory, annual, 2h, internal, paper→Excel→SF, 92%)", "BOZP periodické — admin (TRN-003, mandatory, biennial, 1h, e-learning since 2024, SF Learning, 78%)", "Svařování ČSN EN ISO 9606 (TRN-015, mandatory for welders, 3-yearly, external, certification, paper, 100%)", "Leadership program (TRN-030, optional, annual, 40h, external provider, HR-managed, 45% invited attend)"]
    },
    {
      "type": "Document",
      "attributes": ["title", "code", "type", "template_available", "location", "format", "required_for", "retention_years", "status"],
      "examples": ["Pracovní smlouva vzor (DOC-HR-001, template, SharePoint, DOCX, hiring, 10 years — 3 versions exist)", "BOZP prezenční arch (DOC-HR-020, form, paper, PDF, training, 5 years, partially digitized)", "Exit checklist (DOC-HR-035, template, SharePoint, DOCX, offboarding, 3 years, current)", "Probační hodnocení formulář (DOC-HR-015, form, SharePoint, DOCX, probation, 3 years, compliance 60%)"]
    },
    {
      "type": "System",
      "attributes": ["name", "type", "vendor", "url", "admin_contact", "go_live_date", "module_status", "data_completeness"],
      "examples": ["SAP SuccessFactors (HRIS, core HR since Oct 2022, payroll since 2023, leave management NOT live)", "Recruitee (ATS, since 2021, fully operational)", "SharePoint (DMS, since 2020, 70% migration from shared drive)", "Excel Dovolene_2024.xlsx (leave tracking, ad-hoc, shared, no versioning, 3 HR admins edit simultaneously)"]
    },
    {
      "type": "LeaveType",
      "attributes": ["name", "code", "days_per_year", "carryover_allowed", "carryover_max_months", "approval_required", "documentation_needed", "applies_to", "system"],
      "examples": ["Annual leave 25 days (LV-001, carryover to June next year, all employees, Excel+SF)", "Sick days 3/year (LV-005, no carryover, THP only, no documentation, Excel)", "Sick days 5/year (LV-005B, no carryover, R&D Olomouc ONLY, informal — not in policy)", "Parental leave (LV-010, per zákoník práce, documentation from OSSZ, all, SF)"]
    },
    {
      "type": "LegalRequirement",
      "attributes": ["name", "law_reference", "requirement_type", "frequency", "deadline", "penalty", "responsible", "compliance_status"],
      "examples": ["Dovolená min. 4 týdny (§ 211 ZP, ongoing, N/A, N/A, compliant — firma dává 5)", "BOZP školení periodické (§ 103 ZP, annual/biennial, N/A, inspection fine up to 2M CZK, partially compliant — evidence fragmented)", "Informační povinnost DPP/DPČ (novelizace 2024, one-time update, 2024-07-01, N/A, 3 of 6 policies updated)"]
    },
    {
      "type": "CompensationBand",
      "attributes": ["band", "label", "min_base_czk", "max_base_czk", "variable_pct_max", "typical_roles", "auto_policy", "benefits_tier"],
      "examples": ["B1 (Entry, 28k–33k, 0%, trainee/intern)", "B3 (Skilled, 35k–48k, 5%, CNC operator/admin)", "B5 (Senior/Expert, 55k–75k, 10%, senior engineer/HRBP)", "B7 (Director, 90k–130k, 20%, plant director/CFO)", "B8 (C-level, 130k–180k, 25%, CEO)"]
    },
    {
      "type": "GrievanceCase",
      "attributes": ["id", "type", "filed_date", "filed_by_role", "status", "severity", "resolution", "days_to_resolve"],
      "examples": ["GR-2024-001 Discrimination complaint (filed Oct 2024, R&D engineer, open — investigation ongoing)", "GR-2023-005 Overtime dispute (filed Mar 2023, CNC operator, resolved — 45 days, adjusted payroll)"]
    },
    {
      "type": "PerformanceReview",
      "attributes": ["cycle", "status", "completion_rate_pct", "avg_rating", "applies_to", "system"],
      "examples": ["FY2024 Annual Review (completed Feb 2025, completion 73%, avg 3.4/5, THP+mgmt, SF — výroba excluded)", "FY2024 Mid-Year Check (completed Aug 2024, completion 31%, optional, only some teams)"]
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
      "type": "GOVERNS",
      "from": "Policy",
      "to": "Process",
      "attributes": ["authority_level", "exceptions", "compliance_status"]
    },
    {
      "type": "REQUIRED_FOR",
      "from": "Training",
      "to": "Role",
      "attributes": ["mandatory", "within_days_of_start", "recertification_months"]
    },
    {
      "type": "ELIGIBLE_FOR",
      "from": "Role",
      "to": "Benefit",
      "attributes": ["condition", "after_probation", "band_minimum"]
    },
    {
      "type": "BELONGS_TO",
      "from": "Role",
      "to": "Department",
      "attributes": ["primary", "location"]
    },
    {
      "type": "REPORTS_TO",
      "from": "Department",
      "to": "Department",
      "attributes": ["relationship_type"]
    },
    {
      "type": "USES_SYSTEM",
      "from": "Process",
      "to": "System",
      "attributes": ["step", "action", "workaround"]
    },
    {
      "type": "REQUIRES_DOCUMENT",
      "from": "Process",
      "to": "Document",
      "attributes": ["mandatory", "stage", "format"]
    },
    {
      "type": "COMPLIES_WITH",
      "from": "Policy",
      "to": "LegalRequirement",
      "attributes": ["coverage_level", "gaps"]
    },
    {
      "type": "APPROVES",
      "from": "Role",
      "to": "Process",
      "attributes": ["approval_level", "delegation_allowed", "escalation_to"]
    },
    {
      "type": "INCLUDES_LEAVE",
      "from": "Policy",
      "to": "LeaveType",
      "attributes": ["conditions", "override_from_law"]
    },
    {
      "type": "PART_OF_ONBOARDING",
      "from": "Training",
      "to": "Process",
      "attributes": ["day_in_onboarding", "sequence_order"]
    },
    {
      "type": "SUPERSEDES",
      "from": "Policy",
      "to": "Policy",
      "attributes": ["effective_date", "reason"]
    },
    {
      "type": "IN_BAND",
      "from": "Role",
      "to": "CompensationBand",
      "attributes": ["typical_position_in_range"]
    },
    {
      "type": "TRACKS_COMPLIANCE",
      "from": "Training",
      "to": "LegalRequirement",
      "attributes": ["evidence_type", "audit_ready"]
    },
    {
      "type": "RAISED_IN",
      "from": "GrievanceCase",
      "to": "Policy",
      "attributes": ["alleged_violation"]
    }
  ]
}
```

---

## 6. Generovací pravidla

### 6.1 Objemové parametry
- Politiky: 25–45 (HR, IT, Safety, General — including outdated/conflicting)
- Procesy: 30–60
- Benefity: 15–30 (including low-utilization, dual-system, zrušené)
- Role: 40–80 (across departments, banded)
- Oddělení: 8–15 (hierarchická, 3 lokace)
- Školení: 25–45 (mandatory + voluntary, with fragmented evidence)
- Dokumenty: 30–55 (templates, forms, checklists — some with multiple versions)
- Systémy: 8–12 (HRIS, ATS, payroll, DMS, legacy Excel)
- Typy absencí: 10–18 (including informal/inconsistent ones)
- Právní požadavky: 15–30
- Compensation bands: 8
- Grievance cases: 3–8
- Performance review cycles: 2–4

### 6.2 Pravidla hustoty vazeb
- Každá policy → 2–6 procesů
- Každý proces → 1–3 systémy, 1–4 dokumenty
- Každá role → 3–8 benefitů (band-dependent), 2–6 školení
- Každé oddělení → 4–15 rolí
- Každý proces → 1–3 approval role
- Každá policy → 1–4 legal requirements
- Celkový počet vazeb: 500–1800

### 6.3 Konzistenční pravidla
- Dovolená min. 20 dní zákonný + firma přidává 5 = 25
- Povinná školení: BOZP výroba = annual, admin = biennial, PO = biennial, GDPR = once + refresher
- Approval chain respektuje org hierarchii (ale manažer s 45 direct reports = bottleneck)
- Benefity po zkušební době: after_probation=true pro penzijko, MultiSport
- Mzdové pásmo musí korelovat s band (B1 < B2 < ... < B8)
- Policy verze inkrementální, ale unauthorized variants explicitně označeny
- Systémy pro leave management: Excel (current reality) ≠ SF (target, not live)
- Zákonné reference: § zákoníku práce (262/2006 Sb.) musí být správné
- Location-specific rules: Brno ≠ Olomouc (shift vs flex, sick days differ)

### 6.4 Organizační pravidla
- Org struktura: CEO → 4 directors (Manufacturing, R&D, Sales, Finance/Admin) → managers → ICs
- HR reports to Finance/Admin director
- Each department has head (but Sales head is interim since Sep 2024)
- Manufacturing has 3 shift supervisors + 1 plant director
- R&D has flat structure (1 manager, all others L3–L5 ICs)
- Max direct reports: 45 (Shift Supervisor — bottleneck, known issue)

---

## 7. Anti-patterns & Realism Rules

1. **2 pracovní řády nesjednocené** — POL-HR-001 (Brno, směny) a POL-HR-001B (Olomouc, flex). Formálně mají být 1 dokument od 2020.
2. **Leave management v Excelu** — SF modul odložen, Excel sdílený bez zamykání, 3 HR admins editují současně
3. **Sick days nerovnost** — THP 3 dny, R&D Olomouc 5 dnů (neoficiální), výroba 0 — nikde formálně nezdokumentováno
4. **Whistleblowing formulář nefunguje** — POL-HR-018 existuje, ale odkaz na online formulář vede na 404
5. **Školení evidence ve 3 systémech** — papír + Excel + SF Learning, žádný kompletní přehled, audit risk
6. **Vzdělávací budget 23% utilization** — benefit existuje ale zaměstnanci nevědí jak čerpat (proces nepopsán)
7. **3 verze pracovní smlouvy** — DOC-HR-001 v3.0 (current), v2.1 (pre-2024 novelizace, stále v SharePointu), v1.0 (papír, pre-2020)
8. **Sales dept interim head od září 2024** — žádný formální succession plan
9. **Onboarding 50% papír** — digitální checklist existuje ale IT setup form, BOZP protokol, klíče = papír
10. **Code of Conduct v2.0 review overdue** — next_review_date: 2024-01-15, dnes je 2025+, 2024 ZP novelizace nezapracována

---

## 8. Narrative Vignettes

### Vignette 1: BOZP audit a fragmentovaná evidence
V březnu 2025 přijde inspektorát práce na kontrolu BOZP. Požadují kompletní přehled všech školení za posledních 3 roky. HR zjistí, že: výroba (175 lidí) má papírové prezenční archy v šanonech (2022–2023) a Excel (2024). Admin (60 lidí) má Excel (2022–2023) a SF Learning (2024). R&D Olomouc (55 lidí) má vlastní Excel, který nikdo z Brna neviděl. Po 2 dnech ručního skládání dat chybí záznamy pro 12 zaměstnanců — buď nebyli školeni, nebo se záznamy ztratily. Inspektorát napíše 3 zjištění, pokuta 50k CZK.

### Vignette 2: Dovolená Excel katastrofa
Červenec 2024. Vedoucí směny B (45 direct reports) chce schválit dovolenou pro 8 operátorů najednou. Otevře Excel "Dovolene_2024.xlsx" a zjistí, že HR admin Jana právě edituje stejný soubor. Konflikt verzí — Jana uložila svou verzi, vedoucí přepsal 3 řádky. Navíc: 2 operátoři mají v Excelu špatný zůstatek (chybí záznamy z dubna, kdy je zadávala Petra, která od té doby odešla na mateřskou). Výsledek: 1 operátor čerpá dovolenou, kterou nemá, zjistí se to až při měsíční uzávěrce. Payroll korekce v srpnu.

### Vignette 3: Diskriminační stížnost a nefunkční whistleblowing
V říjnu 2024 R&D inženýrka podá stížnost na diskriminaci (odlišné zacházení při povýšení). Zkusí použít whistleblowing formulář dle POL-HR-018 — odkaz vede na 404. Nakonec pošle email HR ředitelce. Ta zjistí, že: POL-HR-018 existuje od 2023 (zákon 171/2023 Sb.), formulář mělo nastavit IT, nikdy to neproběhlo. Navíc: Code of Conduct (POL-HR-005 v2.0 z 2020) nezmiňuje gender-based diskriminaci explicitně — je "in progress" od ledna 2024. Case GR-2024-001 otevřen, ale postup řešení není jasný — interní směrnice odkazuje na "etickou komisi", která nikdy nebyla ustavena.

---

## 9. Demo Scenarios

1. **"Kolik dní dovolené mi zbývá?"** → LeaveType + evidence v Excelu + vysvětlení proč to není v SF
2. **"Jaká školení musím absolvovat jako nový CNC operátor?"** → Role → REQUIRED_FOR → Training (BOZP, PO, strojní školení, GDPR)
3. **"Kde najdu postup pro práci z domova?"** → Policy POL-HR-012 (THP) + upozornění že R&D Olomouc má neoficiální pravidla
4. **"Kteří zaměstnanci mají propadlé BOZP?"** → Training compliance report — ale data ve 3 systémech
5. **"Jak čerpat vzdělávací budget?"** → Benefit node s utilization 23% + absence procesu v knowledge base
6. **"Jaký je turnover rate v R&D?"** → Personální data + historický trend + comparison s výrobou
7. **"Máme whistleblowing kanál?"** → POL-HR-018 existuje ALE formulář nefunguje (known issue)
8. **"Jak se liší pravidla pro Brno a Olomouc?"** → 2 pracovní řády, rozdílné sick days, remote work policy vs reality

---

## 10. Vzorová JSON struktura

```json
{
  "nodes": [
    {
      "id": "pol_001",
      "type": "Policy",
      "title": "Pracovní řád — závod Brno",
      "code": "POL-HR-001",
      "category": "HR",
      "version": "3.0",
      "effective_date": "2023-01-01",
      "next_review_date": "2025-01-01",
      "owner": "HR Director",
      "status": "current",
      "applies_to": "Manufacturing + Admin Brno",
      "known_issues": "Should be merged with POL-HR-001B (Olomouc) per 2020 decision. Still not done.",
      "language": "CZ"
    },
    {
      "id": "pro_001",
      "type": "Process",
      "name": "Leave Request",
      "code": "PRO-HR-001",
      "category": "Absence Management",
      "owner": "HR Operations",
      "sla_days": 3,
      "approval_chain": ["Direct Manager"],
      "system": "Excel Dovolene_2024.xlsx",
      "digitalization_pct": 0,
      "known_bottleneck": "Shared Excel, no locking, 3 concurrent editors, SF Leave module not live"
    },
    {
      "id": "ben_003",
      "type": "Benefit",
      "name": "Vzdělávací budget",
      "type_detail": "development",
      "provider": "internal",
      "monthly_value": null,
      "annual_value_czk": 25000,
      "eligibility": "THP, after probation, B4+",
      "enrollment_period": "continuous",
      "taxable": false,
      "utilization_pct": 23,
      "applies_to": "THP",
      "status": "active"
    },
    {
      "id": "trn_002",
      "type": "Training",
      "name": "BOZP periodické — výroba",
      "code": "TRN-002",
      "type_detail": "mandatory",
      "mandatory": true,
      "frequency": "annual",
      "duration_hours": 2,
      "provider": "internal (BOZP technik)",
      "certification": false,
      "evidence_system": "paper→Excel→SF (fragmented)",
      "compliance_rate_pct": 92
    }
  ],
  "edges": [
    {
      "id": "edge_001",
      "type": "GOVERNS",
      "from": "pol_001",
      "to": "pro_001",
      "authority_level": "mandatory",
      "exceptions": "R&D Olomouc follows POL-HR-001B with different leave rules",
      "compliance_status": "partial"
    },
    {
      "id": "edge_010",
      "type": "REQUIRED_FOR",
      "from": "trn_002",
      "to": "rol_010",
      "mandatory": true,
      "within_days_of_start": 1,
      "recertification_months": 12
    }
  ]
}
```

---

## 11. Zadání pro Claude Code

### Krok 1: Vygeneruj JSON schema
Vytvoř `hr_schema.json` s rozšířenými entity typy (včetně CompensationBand, GrievanceCase, PerformanceReview). Enum hodnoty: band (B1–B8), status, frequency, category, location (Brno/Olomouc/Praha).

### Krok 2: Vygeneruj seed data
Vytvoř `hr_seed_data.json` s:
- Organizační strukturou VTM a.s. (3 lokace, departments, leadership)
- Reálnými CZ benefity (MultiSport, Sodexo/Edenred, cafeteria Benefity a.s., penzijko)
- Reálnými zákoník práce referencemi (§ 211 dovolená, § 103 BOZP, § 191 nemocenská, § 52 výpověď)
- Realistickými mzdovými pásmy pro CZ strojírenství
- Reálnými HR systémy (SAP SF, Recruitee)
- Školení s certifikacemi (svařování ČSN EN ISO 9606, jeřábnický průkaz dle ČSN ISO 12480)

### Krok 3: Vygeneruj generovací script
Vytvoř `generate_hr_data.py`, který:
- Generuje data PRO FIRMU VTM a.s. — 3 lokace, směnový provoz + office + R&D
- Implementuje anti-patterns (Excel leave, fragmented training evidence, dual benefit system, broken whistleblowing, 2 pracovní řády)
- Org chart s realistickými bottlenecky (45 direct reports, interim head)
- Benefit eligibility rules per band × location × department
- Parametrizovatelný: `--scale small/medium/large` (150/310/500 zaměstnanců)
- Výstup: `hr_knowledge_graph.json`

### Krok 4: Validace
- Org chart completeness (každé oddělení má head nebo interim, reports_to chain konzistentní)
- Benefit eligibility × band konzistence
- Training compliance: povinná školení pro relevantní role exist
- Evidence system fragmentation zachycena (3 systémy, žádný kompletní)
- Anti-patterns present (broken whistleblowing, Excel leave, dual benefit system)
- Location-specific rules konzistentní (Brno ≠ Olomouc)
- Demo scenario coverage
- Statistický report
