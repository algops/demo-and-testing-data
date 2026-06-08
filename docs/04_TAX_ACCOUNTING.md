# Propozice: Tax & Accounting (Bookkeeping)

> **Authoring note:** §1 company profile is a vertical authoring example. Generated demo data uses the anchor tenant [ANCHOR_TENANT.md](ANCHOR_TENANT.md) — group corporate tax; Finanční Centrum is an external vendor, not a tenant.

## 1. Company Profile — fiktivní firma

**Název:** Finanční Centrum s.r.o. (daňově-účetní kancelář)
**Typ:** Střední CZ daňově-poradenská a účetní firma
**Velikost:** 3 partneři (daňoví poradci), 5 senior consultantů, 8 junior consultantů, 4 mzdové účetní, 3 back-office = ~23 lidí
**Klientela:** ~120 aktivních klientů — mix s.r.o. (65%), a.s. (15%), OSVČ (10%), p.o. (5%), zahraniční holdingové struktury (5%)
**Služby:** Vedení účetnictví, mzdová agenda, daňová přiznání (DPPO, DPFO, DPH), transfer pricing, daňové poradenství, audit support, due diligence
**Systémy:** Pohoda (účetnictví — 80% klientů), Money S3 (15% klientů), SAP (5% — velcí klienti), Helios (mzdová agenda), EPO (elektronické podání FÚ), datová schránka

### Historie a "geologické vrstvy"
- **2010:** Kancelář založena 2 daňovými poradci po odchodu z Big Four. Klientela: 20 malých s.r.o., vše v Excelu + Pohoda
- **2012–2015:** Růst na 60 klientů, první a.s. klient (audit required). Implementace Money S3 pro klienty, kteří na Pohoda nechtěli. Interní postupy: Word dokumenty na sdíleném disku
- **2016:** Kontrolní hlášení DPH zavedeno — chaos první 3 měsíce, 2 pokuty (5000 CZK) za pozdní podání. Vytvořen první interní checklist
- **2018:** Příchod 3. partnera (transfer pricing specialista). Rozšíření o mezinárodní daňové poradenství. První holdingový klient (CZ + LU + CY struktura)
- **2020:** COVID — odklad termínů, prominutí sankcí. 5 klientů přešlo na paušální daň. Remote work — sdílený disk → SharePoint migrace (z 60% dokončená)
- **2021:** Elektronické podání povinné. EPO integrace. AML povinnosti pro daňové poradce — narychlo vytvořený interní postup
- **2022:** Konsolidace klientů — 3 skupiny klientů (celkem 8 entit) vyžadují konsolidovanou závěrku. IFRS adopce u 2 klientů (dobrovolná pro CZ a.s. s ambicí IPO)
- **2023:** Implementace Helios pro mzdovou agendu (nahrazuje Excel). Změna DPH sazeb (15% → 12%) — nutné přenastavit všechny systémy. 1 klient pod daňovou kontrolou (DPH, období 2021–2022)
- **2024:** Nový zákon o účetnictví (transpozice CSRD) — nejasnosti ohledně dopadů na střední klienty. Transfer pricing dokumentace pro 4 klienty poprvé. Chybí interní postup pro TP — partner to dělá "z hlavy"

### Reálný nepořádek
- **Pohoda vs Money S3:** 2 systémy, žádná integrace, ruční přenosy pro konsolidaci
- **Účtový rozvrh:** každý klient má mírně jiný (historicky narostlé analytické účty), reconciliation hell
- **Deadline management:** v Excelu (sdílený spreadsheet "Termíny 2024.xlsx"), nikdo nezamyká, duplikáty
- **Archivace:** pre-2020 dokumenty v papíru (skříně ve skladu), 2020+ SharePoint (neúplné)
- **Transfer pricing:** partner dělá z hlavy, žádný šablonový proces, junior nemůže převzít
- **1 klient má FY = duben–březen** (irská matka), všechny ostatní kalendářní rok — systém to zvládá špatně

---

## 2. Role a persony

| Role | Popis | Typické dotazy |
|------|-------|----------------|
| Daňový poradce (partner) | Vedení složitých případů, podepisování přiznání | "Jaký je daňový režim dividend z CY holdco do CZ? Máme k tomu interní memo?" |
| Senior consultant | Due diligence, přehledy, review | "Jak se liší DPPO přiznání pro klienta s IFRS vs české účetní standardy?" |
| Junior consultant | Příprava přiznání, sběr podkladů | "Jaká je správná sazba srážkové daně pro licenční poplatky do DE podle SZDZ?" |
| Mzdová účetní | Zpracování mezd, odvody, roční vyúčtování | "Jak se počítá solidární zvýšení daně a jaký je limit pro 2024?" |
| Client accountant | Vedení účetnictví, uzávěrky | "Na jaký účet zaúčtovat finanční leasing podle ČÚS vs IFRS 16?" |
| Klient (finanční ředitel) | Zadává data, ptá se na daňový dopad | "Kolik ušetříme, když přesuneme IP do NL struktury?" |
| Back-office / admin | Podání, archivace, datové schránky | "Bylo přiznání pro Průmyslový holding podáno včas? Kde najdu potvrzení?" |

---

## 3. Klíčové procesy

### 3.1 Daňové přiznání workflow
1. Engagement confirmation — scope, termín, odpovědná osoba
2. Sběr podkladů od klienta (termín: min. 3 týdny před deadline)
3. Účetní data check — obratová předvaha, kontrola s bankovními výpisy
4. Identifikace daňově neuznatelných nákladů (§ 25 ZDP) a odpočtů (§ 34, § 35)
5. Výpočet daňové povinnosti (zálohy, doplatky, přeplatky)
6. Příprava přiznání v EPO
7. 4-eye review (junior zpracuje, senior/partner zkontroluje)
8. Klient sign-off (email nebo datová schránka)
9. Podání na FÚ přes EPO/datovou schránku
10. Archivace (SharePoint + fyzicky) + deadline tracker update
11. Platba daně — hlídání termínu, upozornění klientovi

### 3.2 Měsíční účetní uzávěrka
1. Sběr dokladů od klienta (faktury, pokladna, banka, interní doklady)
2. Zaúčtování v Pohoda/Money S3
3. Bankovní reconciliation
4. Časové rozlišení kontrola
5. Kurzové přepočty (klienti s EUR/USD transakcemi)
6. DPH přiznání + kontrolní hlášení (25. den následujícího měsíce)
7. Kontrolní výstupy: obratová předvaha, DPH rekapitulace
8. Reporting klientovi (email s PDF, někteří klienti chtějí dashboard — Pohoda nemá)

### 3.3 Roční závěrka a audit support
1. Inventarizace pohledávek a závazků (konfirmace)
2. Opravné položky k pohledávkám (daňové vs účetní — § 8a ZOR)
3. Odpisy — daňové (§ 30–32 ZDP) vs účetní
4. Dohadné položky a rezervy
5. Odložená daň (IAS 12 pro IFRS klienty, ČÚS 003 pro ostatní)
6. Sestavení závěrky (rozvaha, VZZ, příloha, CF pro auditované)
7. Audit support — připrava PBC listu, response na queries
8. Výroční zpráva (pro a.s. a velké s.r.o.)
9. Sbírka listin — uložení do OR

### 3.4 Transfer pricing
1. Identifikace spřízněných osob a transakcí (§ 23 odst. 7 ZDP)
2. Funkční analýza (functions, assets, risks)
3. Výběr metody (CUP, TNMM, cost plus — vždy podle OECD TP Guidelines)
4. Benchmark study (Orbis database)
5. Dokumentace: Local file + Master file (mandatory od určité velikosti)
6. CbCR — Country-by-Country Reporting (pro skupiny >750M EUR)
7. Adjustments — pokud arm's length range nesedí
8. Monitoring a update (roční, ale reálně se dělá jednou za 3 roky)

---

## 4. Knowledge Graph — Entity typy

```json
{
  "entity_types": [
    {
      "type": "TaxLaw",
      "attributes": ["name", "number", "type", "area", "effective_date", "key_sections", "last_amendment", "status"],
      "examples": ["zákon č. 586/1992 Sb., o daních z příjmů (ZDP)", "zákon č. 235/2004 Sb., o DPH (ZDPH)", "zákon č. 563/1991 Sb., o účetnictví (ZÚ)", "zákon č. 16/1993 Sb., o dani silniční", "zákon č. 338/1992 Sb., o dani z nemovitých věcí"]
    },
    {
      "type": "AccountingStandard",
      "attributes": ["name", "code", "issuing_body", "scope", "version", "status"],
      "examples": ["ČÚS 001 – Účty a zásady účtování", "ČÚS 003 – Odložená daň", "ČÚS 013 – Dlouhodobý nehmotný a hmotný majetek", "IFRS 16 – Leases", "IAS 12 – Income Taxes"]
    },
    {
      "type": "TaxForm",
      "attributes": ["name", "form_number", "tax_type", "filing_frequency", "deadline_rule", "electronic_only", "system_used"],
      "examples": ["Přiznání k DPPO (25 5404, annual, EPO)", "Přiznání k DPH (25 5401, monthly/quarterly, EPO)", "Kontrolní hlášení (EPO, 25. den)", "Souhrnné hlášení (25. den, pokud intra-EU)", "Vyúčtování daně ze závislé činnosti (annual, 1.3.)"]
    },
    {
      "type": "Account",
      "attributes": ["number", "name", "class", "group", "type", "tax_relevance", "standard_reference"],
      "examples": ["022 – Hmotné movité věci (DHM)", "321 – Závazky z obchodních vztahů", "518 – Ostatní služby (daňově uznatelné s výjimkami)", "513 – Náklady na reprezentaci (daňově NEuznatelné — § 25/1/t ZDP)"]
    },
    {
      "type": "TaxRate",
      "attributes": ["type", "rate_pct", "applicable_to", "effective_from", "effective_to", "conditions", "law_reference"],
      "examples": ["DPPO 21% (§ 21/1 ZDP, od 2010)", "DPH základní 21%", "DPH snížená 12% (od 1.1.2024, dříve 15%)", "Srážková daň dividendy 15% (§ 36/2 ZDP)", "Srážková daň dividendy CZ→DE 5% (SZDZ čl. 10)"]
    },
    {
      "type": "Client",
      "attributes": ["name", "id", "ico", "dic", "legal_form", "sector", "size_category", "audit_required", "consolidation", "accounting_system", "fiscal_year", "ifrs", "engagement_since", "responsible_partner", "fee_monthly_czk"],
      "examples": ["Průmyslový holding a.s. (IČO 27654321, a.s., manufacturing, audit required, consolidation, Pohoda, FY=calendar)", "TechStart s.r.o. (IČO 08765432, s.r.o., IT, micro, Pohoda, paušální daň → zrušena 2024)", "Celtic Trade Ltd. (IČO 12345678, s.r.o., retail, FY=Apr–Mar, Money S3 — irská matka)"]
    },
    {
      "type": "Engagement",
      "attributes": ["id", "client_id", "type", "period", "status", "responsible_person", "fee_czk", "deadline", "filed_date", "notes"],
      "examples": ["ENG-2024-001 DPPO 2023 for Průmyslový holding (fee 45k, filed 28.6.2024 — s poradcem)", "ENG-2024-089 Vedení účetnictví Q1–Q4 2024 for TechStart (8k/month)", "ENG-2024-023 Transfer pricing Local File for Průmyslový holding (120k — first time, no template)"]
    },
    {
      "type": "InternalProcedure",
      "attributes": ["title", "code", "category", "version", "owner", "last_updated", "status", "known_gaps"],
      "examples": ["IP-001 DPH přiznání checklist v3.0 (current, aktualizováno po změně sazeb 2024)", "IP-003 Roční závěrka postup v2.0 (current, ale chybí IFRS specifika)", "IP-007 Transfer pricing dokumentace v0.0 (NEEXISTUJE — partner dělá z hlavy)", "IP-010 AML postup pro daňové poradce v1.0 (outdated — 2021)"]
    },
    {
      "type": "Deadline",
      "attributes": ["name", "type", "base_date_rule", "offset_days", "extension_possible", "extension_condition", "penalty_czk", "applies_to"],
      "examples": ["DPPO řádný (base: FY end + 3M, ext: +3M s poradcem, penalty: 0.05%/day up to 5%)", "DPH měsíční (25. den M+1, no extension, penalty: 0.05%/day)", "Kontrolní hlášení (25. den M+1, penalty: 1000 CZK za pozdní, 10k za followup)"]
    },
    {
      "type": "TaxRuling",
      "attributes": ["id", "topic", "issuing_authority", "date", "binding", "area", "superseded_by", "practical_impact"],
      "examples": ["KV/KDP 569/2022 – Daňový režim kryptoměn (GFŘ + KDP, binding for tax authority)", "Pokyn D-22 – Stanovení ceny obvyklé (GFŘ, guidance, critical for TP)", "Informace GFŘ k reverse charge ve stavebnictví (non-binding, practical)"]
    },
    {
      "type": "TaxTreaty",
      "attributes": ["countries", "treaty_number", "effective_date", "withholding_rates", "applicable_articles"],
      "examples": ["SZDZ CZ–DE (č. 18/1984 Sb., dividendy 5/15%, úroky 0%, licenční poplatky 5%)", "SZDZ CZ–CY (dividendy 0/5%, úroky 0%, LP 0/10%)", "SZDZ CZ–LU (dividendy 0/10%, úroky 0%, LP 0/10%)"]
    },
    {
      "type": "TaxControl",
      "attributes": ["id", "client_id", "tax_type", "period_under_review", "authority", "status", "findings_amount_czk", "contested"],
      "examples": ["TC-2024-001 DPH kontrola Průmyslový holding, období 2021–2022, FÚ Praha 4 (in progress, preliminary finding 850k CZK — firma kontestuje)"]
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
      "type": "REQUIRES_FORM",
      "from": "TaxLaw",
      "to": "TaxForm",
      "attributes": ["section_reference", "filing_condition"]
    },
    {
      "type": "DEFINES_RATE",
      "from": "TaxLaw",
      "to": "TaxRate",
      "attributes": ["section", "paragraph"]
    },
    {
      "type": "MAPS_TO_ACCOUNT",
      "from": "AccountingStandard",
      "to": "Account",
      "attributes": ["mapping_rule", "exceptions"]
    },
    {
      "type": "INTERPRETS",
      "from": "TaxRuling",
      "to": "TaxLaw",
      "attributes": ["interpreted_section", "practical_implication"]
    },
    {
      "type": "APPLIES_TO_CLIENT",
      "from": "TaxForm",
      "to": "Client",
      "attributes": ["applicable", "reason", "frequency"]
    },
    {
      "type": "HAS_ENGAGEMENT",
      "from": "Client",
      "to": "Engagement",
      "attributes": ["recurring", "start_date"]
    },
    {
      "type": "HAS_DEADLINE",
      "from": "Engagement",
      "to": "Deadline",
      "attributes": ["actual_deadline_date", "filed_date", "on_time"]
    },
    {
      "type": "TAX_TREATMENT",
      "from": "Account",
      "to": "TaxLaw",
      "attributes": ["deductible", "section_reference", "conditions", "common_mistakes"]
    },
    {
      "type": "FOLLOWS_PROCEDURE",
      "from": "Engagement",
      "to": "InternalProcedure",
      "attributes": ["mandatory", "compliance_status"]
    },
    {
      "type": "SUPERSEDES",
      "from": "TaxRuling",
      "to": "TaxRuling",
      "attributes": ["effective_date"]
    },
    {
      "type": "AMENDS",
      "from": "TaxLaw",
      "to": "TaxLaw",
      "attributes": ["amendment_number", "effective_date", "affected_sections"]
    },
    {
      "type": "USES_STANDARD",
      "from": "Client",
      "to": "AccountingStandard",
      "attributes": ["mandatory_or_voluntary", "since"]
    },
    {
      "type": "MODIFIES_RATE",
      "from": "TaxTreaty",
      "to": "TaxRate",
      "attributes": ["treaty_rate", "conditions", "applicable_article"]
    },
    {
      "type": "UNDER_CONTROL",
      "from": "Client",
      "to": "TaxControl",
      "attributes": ["risk_level"]
    },
    {
      "type": "RELATED_ENTITY",
      "from": "Client",
      "to": "Client",
      "attributes": ["relationship_type", "transfer_pricing_relevant"]
    }
  ]
}
```

---

## 6. Generovací pravidla

### 6.1 Objemové parametry
- Daňové zákony: 20–35
- Účetní standardy: 25–45 (ČÚS + IFRS/IAS)
- Daňové formuláře: 15–25
- Účtový rozvrh: 120–250 (syntetické účty + klíčové analytické)
- Daňové sazby: 25–45 (včetně historických změn a treaty rates)
- Klienti: 40–120 (s realistickým long-tail)
- Engagementy: 100–350
- Interní postupy: 15–25 (včetně chybějících a outdated)
- Deadlines: 30–50
- Tax rulings: 15–25
- Tax treaties: 8–15 (klíčové SZDZ)
- Tax controls: 2–5

### 6.2 Pravidla hustoty vazeb
- Každý zákon → 2–5 formulářů
- Každý formulář → 1–3 deadlines
- Každý účetní standard → 5–20 účtů
- Každý klient → 3–8 engagementů
- Každý engagement → 1–2 interní postupy
- Každý klient → 4–10 applicable forms
- Každá SZDZ → modifikuje 3–5 domestic sazeb
- Celkový počet vazeb: 600–2500

### 6.3 Konzistenční pravidla
- Čísla zákonů musí odpovídat Sb.
- Účtový rozvrh: třídy 0–9, správné skupiny
- DPH sazby: 21% base, 12% reduced (od 1.1.2024, předtím 15%), 0% exempt
- DPPO: 21% od 2010
- IČO: 8 číslic, DIČ: "CZ" + IČO
- Klient s audit_required=true → musí mít audit engagement
- IFRS klienti → musí být a.s. nebo s ambicí IPO
- Klient s FY ≠ calendar → deadline offsety přepočítány
- Treaty rates ≤ domestic rates
- Engagement filed_date ≤ deadline (s výjimkami — late filing = realism)

### 6.4 Klientské profily (distribuce)
- Micro (OSVČ, malé s.r.o.): 40% — jen DPPO/DPFO, DPH, jednoduché účetnictví
- Malé (s.r.o., 5–50 zaměstnanců): 35% — účetnictví + mzdy + DPH + DPPO
- Střední (a.s., konsolidace): 15% — vše + audit + transfer pricing
- Velké/mezinárodní: 10% — vše + IFRS + TP dokumentace + treaty structuring

---

## 7. Anti-patterns & Realism Rules

1. **Transfer pricing postup neexistuje** — IP-007 má verzi "v0.0", partner to dělá z hlavy
2. **Deadline tracker je Excel** — sdílený, nezamykatelný, 3 duplicitní záznamy za Q2 2024
3. **Klient s nestandardním FY** — Celtic Trade (Apr–Mar), vše se musí offsetovat, systém to řeší špatně
4. **2 účetní systémy bez integrace** — Pohoda a Money S3, ruční přenosy pro konsolidaci
5. **AML postup outdated** — v1.0 z 2021, novela AML zákona 2023 nezapracována
6. **Účtový rozvrh chaos** — 3 klienti mají "historické" analytické účty, které neodpovídají žádnému standardu
7. **1 klient pod daňovou kontrolou** — DPH 2021–2022, finding 850k CZK, firm kontestuje
8. **1 engagement filed late** — kontrolní hlášení podáno 27. místo 25. (pokuta 1000 CZK)
9. **SZDZ pro CY** — klient přes Kypr, treaty rate 0% dividendy, ale beneficial ownership test sporný
10. **Paušální daň → zrušena 2024** — 2 klienti museli přejít zpět na standardní režim, přechodný chaos

---

## 8. Narrative Vignettes

### Vignette 1: DPH kontrola a chybějící podklady
Průmyslový holding a.s. je pod DPH kontrolou za období 2021–2022. FÚ Praha 4 požaduje doložení reverse charge transakcí ve stavebnictví (§ 92e ZDPH). Klient v 2021 používal starší verzi Pohody, exporty jsou neúplné. Accounting team stráví 3 dny rekonstrukcí dat z papírových faktur. Preliminary finding: 850k CZK doměřené DPH. Partner kontestuje — argumentuje, že reverse charge byl aplikován správně, chybí jen formální náležitosti. Engagement ENG-2024-TC-001 nemá interní postup (IP pro daňové kontroly neexistuje).

### Vignette 2: Transfer pricing z hlavy
Partner Novotný dělá TP dokumentaci pro Průmyslový holding (CZ matka + PL + SK dcery). Local File pro 2023 je jeho 4. TP engagement celkem. Dělá to sám, nemá šablonu, benchmark study dělá manuálně v Orbis. Junior Petra by se to měla naučit, ale partner "nemá čas ji zaučit." Když Petra dostane TP dotaz od jiného klienta, nemá kam sáhnout — žádný interní memo, žádný precedent v DMS. Fee: 120k CZK, ale partner na to stráví 60 hodin (= efektivní sazba 2000 CZK/h vs jeho rate 5500 CZK/h).

### Vignette 3: Změna DPH sazeb 2024
1. ledna 2024 se mění snížená sazba z 15% na 12% a ruší se druhá snížená sazba 10%. Accounting team musí přenastavit sazby v Pohoda (80 klientů) a Money S3 (18 klientů) = 98 individuálních úprav. Checklist IP-001 je aktualizován (v2.0 → v3.0). Ale 3 klienti v Money S3 mají špatné nastavení ještě v březnu — zachyceno až při DPH přiznání za Q1. Opravná přiznání za leden a únor.

---

## 9. Demo Scenarios

1. **"Jaký je deadline pro DPPO pro klienta Průmyslový holding?"** → Engagement → Deadline (s poradcem = 1.7.)
2. **"Je účet 513 daňově uznatelný?"** → Account node → TAX_TREATMENT → § 25/1/t ZDP = NE
3. **"Jaká je srážková daň na dividendy do Německa?"** → Domestic rate 15% MODIFIES_BY treaty rate 5% (SZDZ CZ–DE)
4. **"Kteří klienti potřebují konsolidovanou závěrku?"** → Client nodes s consolidation=true
5. **"Máme interní postup pro transfer pricing?"** → InternalProcedure IP-007 v0.0 = neexistuje
6. **"Kolik engagementů je po deadline?"** → Engagements s filed_date > deadline = late
7. **"Který klient je pod daňovou kontrolou?"** → TaxControl entity propojená na klienta
8. **"Jak se změnily DPH sazby v 2024?"** → TaxRate nodes s effective_from/to ukazující transition

---

## 10. Vzorová JSON struktura

```json
{
  "nodes": [
    {
      "id": "law_001",
      "type": "TaxLaw",
      "name": "Zákon o daních z příjmů",
      "number": "586/1992 Sb.",
      "type_detail": "zákon",
      "area": "Income Tax",
      "effective_date": "1993-01-01",
      "key_sections": ["§ 17 Poplatník", "§ 21 Sazba daně", "§ 23/7 Transfer pricing", "§ 24 Výdaje uznatelné", "§ 25 Výdaje neuznatelné"],
      "last_amendment": "163/2024 Sb.",
      "status": "in_force"
    },
    {
      "id": "cli_005",
      "type": "Client",
      "name": "Celtic Trade Ltd.",
      "ico": "12345678",
      "dic": "CZ12345678",
      "legal_form": "s.r.o.",
      "sector": "Retail",
      "size_category": "small",
      "audit_required": false,
      "consolidation": false,
      "accounting_system": "Money S3",
      "fiscal_year": "April–March",
      "ifrs": false,
      "engagement_since": "2019-04-01",
      "responsible_partner": "per_002",
      "fee_monthly_czk": 12000
    }
  ],
  "edges": [
    {
      "id": "edge_001",
      "type": "HAS_DEADLINE",
      "from": "eng_005",
      "to": "dl_003",
      "actual_deadline_date": "2024-07-01",
      "filed_date": "2024-06-28",
      "on_time": true
    }
  ]
}
```

---

## 11. Zadání pro Claude Code

### Krok 1: Vygeneruj JSON schema
Vytvoř `tax_schema.json` s rozšířenými entity typy (včetně TaxTreaty, TaxControl, rozšířený Client). Validace: IČO (8 číslic), DIČ (CZ prefix), účtové třídy (0–9), čísla zákonů.

### Krok 2: Vygeneruj seed data
Vytvoř `tax_seed_data.json` s:
- Reálnými CZ daňovými zákony + klíčovými novelami
- Účtový rozvrh dle ČÚS (klíčové syntetické účty všech tříd)
- Reálnými daňovými sazbami včetně historických změn (DPH 2024 transition)
- Reálnými SZDZ (DE, SK, PL, CY, LU, NL, UK, US) s withholding rates
- Reálnými termíny a penalizacemi
- Reálnými čísly formulářů MF
- Finanční Centrum s.r.o. profil (osoby, fee structure)

### Krok 3: Vygeneruj generovací script
Vytvoř `generate_tax_data.py`, který:
- Generuje data PRO KANCELÁŘ Finanční Centrum (klientské portfolio, engagement calendar)
- Implementuje anti-patterns (missing TP procedure, Excel deadlines, late filing, tax control)
- Klientské profily dle distribuce v sekci 6.4
- Treaty-modified rates konzistentní s SZDZ
- Parametrizovatelný: `--scale small/medium/large`
- Výstup: `tax_knowledge_graph.json`

### Krok 4: Validace
- Účtový rozvrh completeness
- Deadline konzistence (klient s nestandardním FY správně offsetován)
- Treaty rate ≤ domestic rate
- Anti-patterns present
- Demo scenario coverage
- Statistický report
