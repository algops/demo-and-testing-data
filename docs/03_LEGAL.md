# Propozice: Legal (AI asistent pro advokátní kanceláře)

> **Authoring note:** §1 company profile is a vertical authoring example. Generated demo data uses the anchor tenant [ANCHOR_TENANT.md](ANCHOR_TENANT.md) — in-house legal at Meridian Pay; Kovář & Partners is an external vendor, not a tenant.

## 1. Company Profile — fiktivní kancelář

**Název:** Kovář & Partners, advokátní kancelář s.r.o.
**Typ:** Střední česká full-service advokátní kancelář
**Velikost:** 6 partnerů, 8 senior associates, 12 associates, 10 koncipientů, 5 paralegals, 4 back-office = ~45 lidí
**Zaměření:** Corporate/M&A, Banking & Finance, Employment, IP/IT & Data Protection, Real Estate, Litigation/Arbitration
**Klientela:** Mix — české střední firmy (výroba, IT, retail), nadnárodní korporace (CZ pobočky), municipality, startupy, private equity fondy
**Obrat:** ~180 mil CZK
**Systémy:** ASPI/Beck-online pro legislativu, iManage pro DMS, Clio pro matter management + billing, MS365

### Historie a "geologické vrstvy"
- **2015:** Kancelář založena odštěpením 3 partnerů z velké Big Law firmy. Převzali si klientelu, šablony, know-how (neformálně v hlavách)
- **2016–2018:** Růst, nabírání koncipientů. Šablony sdílené přes sdílený disk (chaos — 3 verze NDA šablony, nikdo neví která je aktuální)
- **2019:** Implementace iManage DMS, standardizace šablon (1. pokus — dokončen z 60%)
- **2020:** COVID — nucený přechod na remote, adoption MS Teams. Interní směrnice pro remote work narychlo sepsána
- **2021:** GDPR enforcement wave — kancelář urgentně aktualizuje NDA šablony, vytváří Data Processing Agreement template. 2 klienti žádají o GDPR compliance audit — kancelář zjišťuje, že vlastní compliance je děravá
- **2022:** Příchod nového IP/IT partnera, rozšíření o AI/tech law practice. Interní AI policy teprve v draftu
- **2023:** Implementace Clio (matter management + billing). Migrace dat z Excelu — historická data neúplná. Conflict check systém konečně elektronický
- **2024:** 2 koncipienti složili advokátní zkoušky a odešli (běžná fluktuace). Know-how v jejich hlavách z 50% nikde nezapsáno. 1 šablona SPA stále odkazuje na "starý ObZ" (před NOZ 2014). Billing guidelines existují ale 2 partneři je systematicky ignorují.

### Reálný nepořádek
- 3 verze NDA šablony (CZ v4.1, CZ v3.0 "pro rychlé dealy", EN v2.0 — nikdo neví, že v3.0 existuje)
- Conflict check: systém funguje od 2023, ale pre-2023 klienti nejsou úplně zmigrovaní
- 2 partneři mají vlastní "upravené" šablony, které nejsou v iManage
- Billing rates v Clio neodpovídají aktuálnímu ceníku (update zapomenut po Q1 rate increase)
- Internal guideline pro AML/KYC: verze 1.0 z roku 2017, novelizace AML zákona 2021 zapracována "ústně"

---

## 2. Role a persony

| Role | Popis | Typické dotazy |
|------|-------|----------------|
| Partner | Senior právník, business development, client relationship | "Jakou argumentaci jsme použili v kauze Novotný v. TechCorp u ÚS?" |
| Senior Associate | 5+ let praxe, vede menší matters samostatně | "Existuje precedent NS k limitaci odpovědnosti v SaaS smlouvách?" |
| Koncipient | Právník v přípravě (3 roky), research & drafting | "Jak formulovat smluvní pokutu podle naší M&A šablony? Kde najdu aktuální verzi?" |
| Paralegal | Due diligence review, document management | "Kolik dokumentů ještě zbývá v data roomu pro Project Falcon?" |
| Of Counsel | Externí expert (daňové právo), part-time | "Jaký je interní postup pro conflict check u nového klienta?" |
| Office Manager | Admin, fakturace, kancelářský provoz | "Jaké jsou hodinové sazby pro DD projekt — partner vs. koncipient?" |
| IT/KM Manager | Knowledge management, systémy | "Které šablony mají verzi starší než 2 roky?" |

---

## 3. Klíčové procesy

### 3.1 Matter lifecycle
1. Client intake: conflict check (Clio) → AML/KYC screening → engagement letter
2. Matter opening: assignment (lead partner + team), billing setup, DMS folder creation
3. Legal research: ASPI/Beck-online + internal precedent search (iManage)
4. Document drafting: template selection → customization → internal review (peer + partner)
5. Client review: track changes, negotiation rounds
6. Finalization: execution copies, apostille/superlegalization if needed
7. Filing: court submissions, OR zápisy, katastr
8. Billing: timesheet entry (Clio), monthly invoice, WIP review
9. Matter closure: final document set, archivace (iManage), retention period start
10. Post-matter: client satisfaction, lessons learned (rare — only for large M&A deals)

### 3.2 Knowledge management
1. Template lifecycle: draft → partner review → approval → versioning → periodic review (supposed to be annual, actual average 2.3 years)
2. Precedent tagging: when closing matter, tag key documents (legal opinion, SPA, court submission) by area + topic
3. Know-how sessions: monthly (planned), actual frequency ~6x/year. Notes in Confluence (inconsistent)
4. Legislative update tracking: partner assigns junior to monitor specific areas, ad-hoc email alerts
5. Internal memos: drafted when significant court decision or legislative change, distributed via email (not centralized)

### 3.3 Due diligence
1. Scope: legal, tax, employment, IP, real estate, environmental, regulatory
2. Document request list (DRL): template exists, customized per deal
3. Data room access: Intralinks or client-provided (Dropbox, SharePoint)
4. Review: paralegal first pass → associate detailed review → red flag escalation
5. DD report: section per area, traffic light rating (green/amber/red), management summary
6. Q&A log: tracked in Excel (not Clio — integration missing)
7. Supplementary DD: post-signing, pre-closing confirmatory

### 3.4 Compliance & internal governance
1. AML/KYC: client identification, beneficial ownership, PEP check, ongoing monitoring
2. Conflict of interest: Clio screening (post-2023), manual check for pre-2023 matters
3. GDPR: data processing records, DPA with vendors, breach notification procedure
4. Professional ethics: ČAK rules, confidentiality, advertising restrictions
5. Professional liability insurance: annual renewal, coverage review
6. Anti-corruption: internal policy exists (v1.0, 2016, never updated)

---

## 4. Knowledge Graph — Entity typy

```json
{
  "entity_types": [
    {
      "type": "Legislation",
      "attributes": ["name", "number", "type", "effective_date", "area_of_law", "status", "key_sections", "last_amendment"],
      "examples": ["zákon č. 89/2012 Sb., občanský zákoník (NOZ)", "zákon č. 90/2012 Sb., o obchodních korporacích (ZOK)", "zákon č. 262/2006 Sb., zákoník práce", "nařízení (EU) 2016/679 (GDPR)", "zákon č. 253/2008 Sb., o AML"]
    },
    {
      "type": "CourtDecision",
      "attributes": ["court", "case_number", "decision_date", "legal_area", "key_holding", "cited_legislation", "relevance_score", "internal_note"],
      "examples": ["NS 25 Cdo 1550/2020 (předsmluvní odpovědnost)", "ÚS II. ÚS 3/2003 (ochrana slabší strany)", "NS 23 Cdo 1061/2021 (SaaS smlouvy — novinka, relevantní pro IT practice)"]
    },
    {
      "type": "Contract",
      "attributes": ["title", "type", "matter_id", "client", "counterparty", "execution_date", "status", "value_czk", "governing_law", "template_used", "deviations_from_template", "language"],
      "examples": ["SPA – Project Falcon (Acquisition of LogiCorp, 450M CZK)", "NDA – Project Atlas (bilateral, CZ/EN)", "Service Agreement – TechNova maintenance (120k CZK/month)"]
    },
    {
      "type": "Template",
      "attributes": ["title", "code", "type", "version", "author", "last_updated", "language", "jurisdiction", "status", "known_issues"],
      "examples": ["TPL-NDA-CZ-v4.1 (current)", "TPL-NDA-CZ-v3.0 (unauthorized variant — partner Kovář's personal version)", "TPL-SPA-EN-v2.0 (still references pre-NOZ terminology in recitals — known issue)", "TPL-EMPL-CZ-v3.0 (current)"]
    },
    {
      "type": "LegalOpinion",
      "attributes": ["title", "id", "matter_id", "author", "date", "area_of_law", "confidentiality", "status", "cited_decisions_count", "cited_legislation_count"],
      "examples": ["LO-2024-015 Tax treatment of crypto staking rewards", "LO-2024-003 GDPR compliance of AI-powered HR screening tools", "LO-2023-042 Limitation of liability in SaaS contracts under CZ law"]
    },
    {
      "type": "Client",
      "attributes": ["name", "id", "type", "sector", "aml_status", "aml_last_check", "engagement_since", "key_contact", "conflict_check_complete", "revenue_tier"],
      "examples": ["Průmyslový holding a.s. (manufacturing, since 2015, Tier A)", "StartupX s.r.o. (IT/SaaS, since 2022, Tier C)", "Město Brno (municipality, since 2020, Tier B)", "Nordic Capital PE Fund (via London office, since 2023, Tier A)"]
    },
    {
      "type": "Matter",
      "attributes": ["id", "title", "type", "client_id", "lead_partner", "team_members", "status", "opened_date", "closed_date", "area_of_law", "fee_arrangement", "total_billed_czk", "wip_czk"],
      "examples": ["M-2024-0142 Acquisition of LogiCorp (Project Falcon)", "M-2024-0089 Employment dispute – Kovářová v. RetailCo (wrongful termination)", "M-2023-0201 GDPR compliance program for BankCo"]
    },
    {
      "type": "InternalGuideline",
      "attributes": ["title", "code", "category", "version", "approved_by", "effective_date", "next_review_date", "status"],
      "examples": ["IG-001 Conflict of Interest Policy v2.0 (current)", "IG-003 AML/KYC Procedure v1.0 (OUTDATED — 2017, needs update per 2021 AML amendment)", "IG-007 Billing Guidelines v1.1 (current but poorly enforced)", "IG-010 AI Use Policy v0.1 (DRAFT — since 2022)"]
    },
    {
      "type": "LegalArea",
      "attributes": ["name", "code", "parent_area", "team_lead", "headcount"],
      "examples": ["Corporate/M&A (LA-01, lead: JUDr. Kovář)", "Employment (LA-03, lead: Mgr. Horáková)", "IP/IT & Data Protection (LA-04, lead: Mgr. Černý — joined 2022)"]
    },
    {
      "type": "Person",
      "attributes": ["name", "role", "seniority", "legal_area", "bar_number", "joined_date", "hourly_rate_czk", "utilization_target_pct", "languages"],
      "examples": ["JUDr. Martin Kovář (Partner, M&A, bar #12345, 7500 CZK/h)", "Mgr. Eva Svobodová (Koncipient, IP/IT, bar #pending, 2800 CZK/h)"]
    },
    {
      "type": "DDProject",
      "attributes": ["id", "matter_id", "type", "target_company", "status", "total_documents", "reviewed_documents", "red_flags_count", "report_status"],
      "examples": ["DD-2024-003 Legal DD for Project Falcon (892 docs, 756 reviewed, 12 red flags, report DRAFT)"]
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
      "type": "CITES_LEGISLATION",
      "from": "LegalOpinion",
      "to": "Legislation",
      "attributes": ["section", "paragraph", "context"]
    },
    {
      "type": "CITES_DECISION",
      "from": "LegalOpinion",
      "to": "CourtDecision",
      "attributes": ["relevance", "supporting_or_distinguishing"]
    },
    {
      "type": "INTERPRETS",
      "from": "CourtDecision",
      "to": "Legislation",
      "attributes": ["interpreted_section", "interpretation_type"]
    },
    {
      "type": "OVERRULES",
      "from": "CourtDecision",
      "to": "CourtDecision",
      "attributes": ["scope", "partial"]
    },
    {
      "type": "GOVERNED_BY",
      "from": "Contract",
      "to": "Legislation",
      "attributes": ["specific_sections"]
    },
    {
      "type": "BASED_ON_TEMPLATE",
      "from": "Contract",
      "to": "Template",
      "attributes": ["deviation_level", "deviations_description"]
    },
    {
      "type": "BELONGS_TO_MATTER",
      "from": ["Contract", "LegalOpinion", "DDProject"],
      "to": "Matter",
      "attributes": ["document_role"]
    },
    {
      "type": "LED_BY",
      "from": "Matter",
      "to": "Person",
      "attributes": ["role_in_matter", "hours_billed"]
    },
    {
      "type": "FOR_CLIENT",
      "from": "Matter",
      "to": "Client",
      "attributes": ["engagement_type", "fee_arrangement"]
    },
    {
      "type": "SPECIALIZES_IN",
      "from": "Person",
      "to": "LegalArea",
      "attributes": ["expertise_level", "years_experience"]
    },
    {
      "type": "COVERS_AREA",
      "from": "Template",
      "to": "LegalArea",
      "attributes": ["primary"]
    },
    {
      "type": "AMENDS",
      "from": "Legislation",
      "to": "Legislation",
      "attributes": ["amendment_date", "affected_sections"]
    },
    {
      "type": "FOLLOWS_GUIDELINE",
      "from": "Matter",
      "to": "InternalGuideline",
      "attributes": ["compliance_status"]
    },
    {
      "type": "SIMILAR_TO",
      "from": "Matter",
      "to": "Matter",
      "attributes": ["similarity_basis", "reuse_potential"]
    }
  ]
}
```

---

## 6. Generovací pravidla

### 6.1 Objemové parametry
- Legislativa: 40–80
- Judikáty: 120–300
- Smlouvy: 60–200
- Šablony: 25–50 (including unauthorized/outdated variants)
- Právní stanoviska: 40–100
- Klienti: 25–60
- Matters: 60–180
- Interní směrnice: 15–25
- Právní oblasti: 8–12 (hierarchické)
- Osoby: 35–50
- DD Projekty: 5–15

### 6.2 Pravidla hustoty vazeb
- Každý judikát → 1–5 citací legislativy
- Každé právní stanovisko → 3–12 citací (legislativa + judikáty)
- Každá smlouva → 1–3 legislativní odkazy, 0–1 šablona
- Každý matter → 2–10 dokumentů
- Každý klient → 1–8 matters
- Každá osoba → 1–3 právní oblasti, 3–15 matters
- Celkový počet vazeb: 800–3000

### 6.3 Konzistenční pravidla
- Spisové značky: NS format "XX Cdo XXXX/YYYY", ÚS "I./II./III./IV. ÚS XXXX/YY", NSS "X Afs/As/Azs XXXX/YYYY"
- Čísla zákonů: "č. XX/YYYY Sb." nebo "nařízení (EU) YYYY/XXXX"
- Judikáty nemohou citovat pozdější legislativu
- Partner nemůže být koncipient na stejném matteru
- AML status "cleared" vyžadován před matter opening (ale pre-2023 matters mohou mít "legacy_unchecked")
- Hourly rates: Partner 6000–8000, Senior 4500–5500, Associate 3500–4500, Koncipient 2500–3200
- Template versions inkrementální, unauthorized variants explicitně označeny
- Closed matters musí mít total_billed ≥ 0, open matters mohou mít WIP

### 6.4 Doménově specifická pravidla
- M&A matters: SPA + NDA + DD project + legal opinions + shareholder agreements
- Employment matters: employment contract review, termination opinion, court submissions
- IP matters: license agreements, trademark applications, cease & desist, NDA
- Real Estate: purchase agreements, lease agreements, due diligence (katastr, OR)
- Each legal area must have ≥1 partner + ≥2 juniors
- High-value matters (>50M CZK) must have partner + senior associate lead

---

## 7. Anti-patterns & Realism Rules

1. **3 verze NDA šablony** — v4.1 je aktuální, v3.0 je "Kovářova verze" (unauthorized), EN v2.0 je outdated
2. **SPA template stále odkazuje na "starý ObZ"** v recitals (known issue, nikdo neopravil)
3. **AML/KYC guideline v1.0 z 2017** — novelizace AML zákona 2021 zapracována jen ústně
4. **AI Use Policy v0.1** — draft od 2022, nikdy neschválena, ale 3 koncipienti už ChatGPT používají
5. **Billing rates v Clio nesedí** — Q1 2025 rate increase nezapracován do systému
6. **2 odešlí koncipienti** — 50% jejich know-how nikde nezapsáno, matters přeassignovány ale poznámky chybí
7. **DD Q&A log v Excelu** — nesyncovaný s Clio, duplikátní záznamy
8. **Conflict check pre-2023** — historičtí klienti nekompletně zmigrovaní do Clio
9. **Know-how sessions** — plánované měsíčně, reálně 6x ročně, zápisy inconsistentní
10. **1 matter s `fee_arrangement: "success_fee"` ale tracking je manuální** — žádný systém to neumí

---

## 8. Narrative Vignettes

### Vignette 1: Šablona-chaos při urgentním dealu
Klient Nordic Capital potřebuje NDA pro Project Falcon do 2 hodin. Koncipientka Eva stáhne z iManage TPL-NDA-CZ-v3.0 (Kovářovu neoficiální verzi — kratší, bez GDPR klauzule). Partner Kovář to schválí, protože "pro rychlý deal stačí." O 3 týdny později při DD protistrany zjistí, že NDA nemá GDPR article 28 reference — musí se re-executovat. Čas navíc: 4 hodiny. Klient nefakturován (partner rozhodl). V DMS jsou teď 2 verze NDA pro stejný deal.

### Vignette 2: Ztracené know-how po odchodu koncipienta
Koncipient Marek pracoval 2.5 roku primárně na employment matters. Složil advokátní zkoušky a odešel do korporátu. Jeho 15 matters přeassignováno na novou koncipientku Kláru. Problém: Marek měl v hlavě precedentní argumentaci z kauzy "Kovářová v. RetailCo" (NS rozhodnutí z 2023), kterou nikde nezapsal. Klára dostane podobný případ a stráví 8 hodin researching something Marek znal zpaměti. Legal opinion LO-2023-042 existuje ale je tagován jen "employment" — chybí tag "limitation of liability" a "SaaS" (crossover s IP/IT).

### Vignette 3: AML compliance gap
Při kontrole ČAK v říjnu 2024 se ukáže, že klient "Města Brno" (municipality) nemá kompletní AML screening — v 2020 se municipality považovaly za low-risk a screenoval se jen statutární zástupce. Od novelizace 2021 je vyžadován screening beneficial ownership i u veřejných zakázek. Kancelář má AML guideline v1.0 z 2017 — novelizace "ústně sdělena" ale nikdo ji formálně nezapracoval. Finding: 8 municipal klientů nemá aktuální AML screening.

---

## 9. Demo Scenarios

1. **"Najdi mi relevantní judikaturu NS k limitaci odpovědnosti v SaaS smlouvách"** → Court decisions s legal_area IP/IT + key_holding matching + cited legislation (§ 2913 NOZ)
2. **"Kde najdu aktuální NDA šablonu?"** → Template nodes — musí ukázat v4.1 jako current A varovat před v3.0
3. **"Jaké matters máme otevřené pro klienta Nordic Capital?"** → Client → Matter traversal + status + WIP
4. **"Kteří koncipienti mají volnou kapacitu tento měsíc?"** → Person nodes (koncipient) + hours_billed vs utilization_target
5. **"Které interní směrnice potřebují update?"** → InternalGuideline s next_review_date v minulosti NEBO status OUTDATED
6. **"Jakou argumentaci jsme použili v podobném případu?"** → SIMILAR_TO edges mezi matters + linked legal opinions
7. **"Máme conflict of interest u nového klienta?"** → Client/Matter traversal + counterparty matching
8. **"Kolik DD dokumentů zbývá zkontrolovat v Project Falcon?"** → DDProject node: total vs reviewed

---

## 10. Vzorová JSON struktura

```json
{
  "nodes": [
    {
      "id": "leg_001",
      "type": "Legislation",
      "name": "Občanský zákoník",
      "number": "89/2012 Sb.",
      "type_detail": "zákon",
      "effective_date": "2014-01-01",
      "area_of_law": "Civil Law",
      "status": "in_force",
      "key_sections": ["§ 1724–1788 Smlouvy obecně", "§ 2913 Náhrada škody", "§ 1729 Předsmluvní odpovědnost"],
      "last_amendment": "115/2025 Sb."
    },
    {
      "id": "tpl_003",
      "type": "Template",
      "title": "NDA Template CZ",
      "code": "TPL-NDA-CZ",
      "type_detail": "NDA",
      "version": "3.0",
      "author": "JUDr. Kovář",
      "last_updated": "2021-06-15",
      "language": "CZ",
      "jurisdiction": "CZ",
      "status": "unauthorized_variant",
      "known_issues": "Missing GDPR Article 28 reference, not approved by KM committee"
    }
  ],
  "edges": [
    {
      "id": "edge_001",
      "type": "BASED_ON_TEMPLATE",
      "from": "con_015",
      "to": "tpl_003",
      "deviation_level": "minor",
      "deviations_description": "Added arbitration clause per client request"
    }
  ]
}
```

---

## 11. Zadání pro Claude Code

### Krok 1: Vygeneruj JSON schema
Vytvoř `legal_schema.json` — entity typy (sekce 4), relationship typy (sekce 5). Speciální validace: spisové značky (regex per court), čísla zákonů, ECLI identifikátory, hourly rate ranges per seniority.

### Krok 2: Vygeneruj seed data
Vytvoř `legal_seed_data.json` s:
- Reálnými CZ zákony (NOZ, ZOK, ZP, OSŘ, TZ, zákon o advokacii, AML zákon, GDPR)
- Reálnými formáty spisových značek (NS, ÚS, NSS, krajské soudy)
- Kancelář Kovář & Partners profile (osoby, seniority, rate cards)
- Template naming convention + known issues seed
- Fiktivní ale realistické client names (CZ firmy)

### Krok 3: Vygeneruj generovací script
Vytvoř `generate_legal_data.py`, který:
- Generuje data PRO KANCELÁŘ Kovář & Partners
- Implementuje anti-patterns (template chaos, AML gap, lost know-how)
- Vytváří konzistentní citační síť (judikáty ↔ legislativa), respektuje temporální logiku
- Generuje matter portfolio s realistickým billing (seniority × hours × rate)
- DD projekty s progress tracking (reviewed/total documents)
- Parametrizovatelný: `--scale small/medium/large`
- Výstup: `legal_knowledge_graph.json`

### Krok 4: Validace
- Spisové značky format validation
- Temporální konzistence citací (judikát nemůže citovat pozdější zákon)
- Seniority-rate consistency
- Template version ordering + unauthorized variants flagged
- Anti-patterns present (outdated AML, template chaos, lost know-how gaps)
- Demo scenario coverage
- Statistický report
