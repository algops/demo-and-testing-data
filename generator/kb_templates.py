"""Domain-specific knowledge base document templates (Czech)."""

from __future__ import annotations

from .catalogues import DOMAIN_INTEGRATIONS, DOMAIN_KB_TITLES

ORG_NAME = "Meridian Pay a.s."
DISCLAIMER = "Vygenerováno pro demo účely"


def _integration_name(domain: str) -> str:
    specs = DOMAIN_INTEGRATIONS.get(domain, [])
    return specs[0]["name"] if specs else "interní systém"


def _header(title: str, domain: str, doc_kind: str, sensitivity: str) -> str:
    return f"""# {title}

> Organizace: **{ORG_NAME}** | Doména: **{domain}** | Typ: {doc_kind} | Citlivost: {sensitivity}

"""


def render_document(doc: dict) -> str:
    domain = doc["domain_id"]
    kind = doc.get("doc_kind", "guideline")
    title = doc["title"]
    sensitivity = doc.get("sensitivity", "internal")
    if kind in ("system_prompt", "agent_role", "agent_skill"):
        return _render_agent_document(doc)
    builders = {
        "policy": _policy,
        "guideline": _guideline,
        "runbook": _runbook,
        "sop": _sop,
        "adr": _adr,
        "template": _template,
        "faq": _faq,
    }
    body_fn = builders.get(kind, _guideline)
    return body_fn(title, domain, sensitivity)


def _kb_refs(domain: str, limit: int = 4) -> str:
    specs = DOMAIN_KB_TITLES.get(domain, [])[:limit]
    if not specs:
        return f"- `knowledgebase/{domain}/`"
    lines = []
    for s in specs:
        lines.append(f"- `{s['section']}/{s['sub']}` — {s['title']}")
    return "\n".join(lines)


def _render_agent_document(doc: dict) -> str:
    kind = doc.get("doc_kind", "system_prompt")
    builders = {
        "system_prompt": _system_prompt,
        "agent_role": _agent_role,
        "agent_skill": _agent_skill,
    }
    return builders[kind](doc)


def _system_prompt(doc: dict) -> str:
    domain = doc["domain_id"]
    name = doc.get("agent_name", doc["title"])
    use_case = doc.get("use_case", "")
    persona = doc.get("persona", "doménový asistent")
    audience = doc.get("audience", "zaměstnanci")
    guardrails = doc.get("guardrails", [])
    sections = doc.get("must_read_sections", [])
    integration = _integration_name(domain)
    sensitivity = doc.get("sensitivity", "internal")
    agent_slug = doc.get("agent_slug", "agent")
    guardrail_lines = "\n".join(f"- {g}" for g in guardrails) or "- Dodržuj interní politiky domény"
    section_lines = "\n".join(f"- `knowledgebase/{domain}/{s}`" for s in sections) or f"- `knowledgebase/{domain}/`"

    return _header(f"System prompt: {name}", domain, "system_prompt", sensitivity) + f"""## Role a mise

Jsi **{name}** — chat agent pro {ORG_NAME} v doméně `{domain}`.
**Persona:** {persona}
**Primární účel:** {use_case}
**Cílové publikum:** {audience}

## Rozsah znalostní báze

Čerpáš z dokumentů v KB pod cestami:
{section_lines}
- `knowledgebase/{domain}/agents/{agent_slug}/core/` — tvoje konfigurace (role, skill)

Autoritativní operativní data čti z integrace **{integration}**; KB popisuje interpretaci a postupy.

## Chování

1. Odpovídej stručně, v češtině, s odkazem na konkrétní KB dokument.
2. Pokud informace v KB chybí, řekni to explicitně a navrhni eskalaci.
3. U citlivých témat používej interní klasifikaci `{sensitivity}`.

## Guardrails

{guardrail_lines}

## Mimo rozsah / eskalace

- Právní, daňové nebo bezpečnostní závěry bez schváleného dokumentu → eskaluj na `#agents-{domain}` (supervisor Slack).
- Požadavky mimo doménu `{domain}` → přesměruj na příslušného doménového agenta.

## Související dokumenty v KB

{_kb_refs(domain)}
"""


def _agent_role(doc: dict) -> str:
    domain = doc["domain_id"]
    name = doc.get("agent_name", doc["title"])
    audience = doc.get("audience", "zaměstnanci")
    use_case = doc.get("use_case", "")
    sensitivity = doc.get("sensitivity", "internal")
    integration = _integration_name(domain)

    return _header(f"Role: {name}", domain, "agent_role", sensitivity) + f"""## Odpovědnosti

| Oblast | Popis |
|--------|-------|
| Primární use-case | {use_case} |
| Publikum | {audience} |
| Doména | `{domain}` @ {ORG_NAME} |
| Zdroj dat | {integration} + schválená KB |

## Matice oprávnění

| Smí | Nesmí |
|-----|-------|
| Vysvětlovat schválené SOP, politiky a runbooky z KB | Vydávat závazná právní/daňová stanoviska |
| Navrhovat další kroky dle dokumentovaných postupů | Měnit produkční systémy nebo data |
| Citovat cesty v `knowledgebase/{domain}/` | Šířit osobní údaje mimo účel dotazu |
| Eskalovat na supervizora `#agents-{domain}` | Obcházet guardrails definované v system promptu |

## Handoff pravidla

- **Supervisor:** Slack `#agents-{domain}` — steering, schválení výjimek
- **Domain owner:** `#domain-{domain}` — chyby v dokumentaci (ticket `KB-FIX`)
- **Lidský expert:** při nejistotě nebo vysokém dopadu na zákazníka/regulátora

## Compliance

Agent je řízen dokumenty v `knowledgebase/{domain}/agents/` a musí být v souladu s platnými politikami v `compliance/core/`.
Revize role: minimálně při změně use-case nebo guardrails.
"""


def _agent_skill(doc: dict) -> str:
    domain = doc["domain_id"]
    name = doc.get("agent_name", doc["title"])
    guardrails = doc.get("guardrails", [])
    demo_questions = doc.get("demo_questions", [])
    sections = doc.get("must_read_sections", [])
    sensitivity = doc.get("sensitivity", "internal")
    integration = _integration_name(domain)
    tools = [i["name"] for i in DOMAIN_INTEGRATIONS.get(domain, []) if i["role"] == "tool"]
    tool_name = tools[0] if tools else "doménový nástroj"
    guardrail_lines = "\n".join(f"- {g}" for g in guardrails) or "- Viz system prompt"
    section_lines = "\n".join(f"- Prohledej `knowledgebase/{domain}/{s}`" for s in sections)
    qa_lines = ""
    for q in demo_questions:
        qa_lines += f"\n**Q:** {q}\n**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.\n"

    return _header(f"Skill: {name}", domain, "agent_skill", sensitivity) + f"""## Workflow odpovědi

1. **Porozumění** — identifikuj záměr dotazu a dotčené KB sekce.
2. **Vyhledání** — prohledej:
{section_lines}
3. **Validace** — ověř proti {integration} pokud jde o stav systému/recordů.
4. **Odpověď** — struktura: shrnutí → citace KB cesty → doporučený krok.
5. **Eskalace** — pokud chybí podklad, otevři handoff na supervizora.

## Použití nástrojů

- **{tool_name}** — doplňkové akce dle oprávnění v chat-agent setup (execute_tool).
- Integrační data nikdy nepřepisují schválený text politik v KB.

## Formát citace

```
[KB: knowledgebase/{domain}/<section>/<sub>/<soubor>.md | verze core]
```

## Guardrails (operativní)

{guardrail_lines}

## Příklady interakcí
{qa_lines}

## Kontrolní seznam kvality

- [ ] Odpověď má alespoň jednu KB citaci
- [ ] Guardrails dodrženy
- [ ] Žádné vymyšlené metriky nebo termíny
- [ ] Eskalace nabídnuta pokud data chybí
"""


def _policy(title: str, domain: str, sensitivity: str) -> str:
    integration = _integration_name(domain)
    return _header(title, domain, "policy", sensitivity) + f"""## Účel a rozsah

Tato politika stanovuje závazná pravidla pro oblast **{title.lower()}** v rámci {ORG_NAME}. Platí pro všechny zaměstnance, dodavatele s přístupem k interním systémům a vedení společnosti.

## Odpovědnosti

| Role | Odpovědnost |
|------|-------------|
| Vedení společnosti | Schválení politiky, alokace zdrojů |
| Domain owner ({domain}) | Aktualizace, compliance monitoring |
| Line managers | Zajištění dodržování v týmech |
| Interní audit | Nezávislá kontrola každých 12 měsíců |

## Klíčová ustanovení

1. Všechny procesy v doméně {domain} musí být dokumentovány a verzovány v znalostní bázi pod `knowledgebase/{domain}/`.
2. Data z integrace **{integration}** jsou považována za autoritativní zdroj pro operativní rozhodování.
3. Odchylky od politiky vyžadují písemnou výjimku schválenou domain ownerem a záznam v registru rizik.
4. Porušení politiky může vést k disciplinárnímu řízení dle interních předpisů {ORG_NAME}.

## Životní cyklus dokumentu

- **Návrh:** domain owner + právní/compliance (dle domény)
- **Review:** minimálně jednou ročně nebo při změně regulace
- **Schválení:** člen představenstva pro politiku úrovně 1
- **Distribuce:** publikace v KB, notifikace přes Slack #compliance

## Související dokumenty

- Runbooky a SOP v `knowledgebase/{domain}/operations/`
- Integrační dokumentace k systému {integration}
- Registr rizik {ORG_NAME} (interní)

## Revize

| Verze | Datum | Autor | Změna |
|-------|-------|-------|-------|
| 1.0 | 2025-03-01 | Domain owner {domain} | První vydání |
"""


def _guideline(title: str, domain: str, sensitivity: str) -> str:
    integration = _integration_name(domain)
    return _header(title, domain, "guideline", sensitivity) + f"""## Kontext

{ORG_NAME} provozuje platební a fintech služby v regulovaném prostředí. Tato příručka vysvětluje, jak interpretovat požadavky v oblasti **{title}** a jak je promítnout do praxe domény `{domain}`.

## Regulační a interní rámec

- Soulad s českou a EU legislativou relevantní pro doménu {domain}
- Propojení na datové zdroje v **{integration}** a související systémy
- Mapování požadavků na object types a datapointy v AlgOps katalogu

## Postup implementace

1. **Identifikace rozsahu** — určete dotčené týmy, systémy a procesy.
2. **Gap analýza** — porovnejte stávající stav s požadavky příručky.
3. **Akční plán** — vlastník, termín, měřitelný výstup.
4. **Validace** — kontrola vzorkem záznamů z {integration}.
5. **Reporting** — kvartální status pro ESG/compliance výbor (dle domény).

## Metriky úspěchu

- Pokrytí dokumentovaných procesů ≥ 90 %
- Počet otevřených gapů s překročeným SLA ≤ 3
- Úspěšnost auditních kontrol bez major finding

## Časté chyby

- Spoléhání na neoficiální Excel místo schválené KB verze
- Neaktuální reference na zrušené interní postupy
- Chybějící vazba na zdrojová data v integraci

## Kontakt

Domain owner `{domain}` — slack:#domain-{domain}
"""


def _runbook(title: str, domain: str, sensitivity: str) -> str:
    integration = _integration_name(domain)
    return _header(title, domain, "runbook", sensitivity) + f"""## Přehled

Runbook popisuje operativní postup: **{title}**. Používejte při incidentech, plánovaných oknech i ad-hoc eskalacích v doméně {domain}.

## Předpoklady

- Přístup do **{integration}** a souvisejících systémů
- Role: operátor L2+ nebo on-call engineer
- Aktuální kontakty v PagerDuty / Slack `#oncall-{domain}`

## Kroky

### 1. Detekce a klasifikace

- Ověřte alert nebo ticket v monitoringu.
- Přiřaďte závažnost P1–P4 dle dopadu na zákazníky {ORG_NAME}.

### 2. Stabilizace

- Izolujte dotčenou službu nebo datový tok.
- Zdokumentujte čas začátku incidentu (UTC).

### 3. Diagnostika

- Zkontrolujte logy a poslední deploye v integraci {integration}.
- Porovnejte s posledním známým dobrým stavem (baseline dataset).

### 4. Náprava

- Aplikujte schválený rollback nebo hotfix dle SOP.
- Po obnově služby spusťte smoke testy.

### 5. Uzavření

- Aktualizujte ticket, přidejte timeline.
- Do 48 hodin post-mortem pro P1/P2.

## Eskalace

| Úroveň | Kontakt | Podmínka |
|--------|---------|----------|
| L1 | Service desk | První reakce |
| L2 | Domain on-call | P3+, neznámá příčina |
| L3 | Architekt / vendor | P1/P2, data loss risk |

## Přílohy

- Odkaz na dashboard v {integration}
- Checklist pro handover mezi směnami
"""


def _sop(title: str, domain: str, sensitivity: str) -> str:
    return _header(title, domain, "sop", sensitivity) + f"""## Standardní operační postup

**{title}** — závazný postup pro zaměstnance {ORG_NAME} v doméně `{domain}`.

## Rozsah

Platí pro všechny týmy podílející se na procesu. Výjimky pouze po schválení domain ownerem.

## Kroky

1. **Příprava** — ověřte oprávnění, šablony a aktuální verzi dokumentace v KB.
2. **Provedení** — postupujte podle checklistu; každý krok zaznamenejte v ticketu.
3. **Kontrola kvality** — nezávislý reviewer u transakcí nad prahem 100 000 Kč (nebo dle domény).
4. **Archivace** — uložte výstupy do `knowledgebase/{domain}/operations/archive/`.

## Checklist

- [ ] Vstupní data validována
- [ ] Schválení druhým členem týmu (four-eyes)
- [ ] Výstup uložen v autoritativním systému
- [ ] Notifikace stakeholderům odeslána

## Metriky

- SLA zpracování dle typu požadavku
- Počet vrácení k doplnění ≤ 5 % měsíčně

## Revize

Revize SOP minimálně každých 6 měsíců nebo po změně regulace.
"""


def _adr(title: str, domain: str, sensitivity: str) -> str:
    return _header(title, domain, "adr", sensitivity) + f"""## Status

Přijato — platí pro {ORG_NAME}, doména `{domain}`.

## Kontext

{ORG_NAME} potřebuje škálovatelnou a auditovatelnou architekturu v oblasti popsané dokumentem **{title}**. Tým zvažoval více alternativ s ohledem na regulaci, latenci a provozní náklady.

## Rozhodnutí

Zvolený přístup kombinuje:

- Event-driven integraci mezi core službami
- Centrální observability a SLO monitoring
- Oddělení čtení/zápisu pro reportingové workloady

## Důsledky

### Pozitivní

- Lepší traceability pro audit a incident review
- Snazší onboarding nových týmů díky jasné hranici služeb

### Negativní

- Vyšší počáteční investice do infrastruktury
- Potřeba školení pro distributed tracing

## Alternativy zvažované

1. Monolitický modul — rychlejší start, horší škálování
2. Čistě batch ETL — nižší náklady, nedostatečná latence pro platby

## Dodržování

Architecture board review každých 12 měsíců. Změny vyžadují nové ADR.
"""


def _template(title: str, domain: str, sensitivity: str) -> str:
    return _header(title, domain, "template", sensitivity) + f"""## Šablona

**{title}** — použijte pro standardizované dokumenty v {ORG_NAME}.

```
Dokument č.: [MP-{domain.upper()}-____]
Verze: 1.0
Datum účinnosti: [DD.MM.RRRR]
Strany smluvních stran:
  1. {ORG_NAME}, IČO: [●●●●●●●●], sídlo Praha
  2. [Název druhé strany], IČO: [________]

Předmět:
[Stručný popis předmětu smlouvy / procesu / formuláře]

Doba trvání:
Od [datum] do [datum / neurčito]

Platební podmínky:
[Splatnost, měna CZK/EUR, způsob úhrady]

Ochrana dat:
Strany se zavazují zpracovávat osobní údaje dle GDPR a interních politik {ORG_NAME}.

Podpisy:
_______________________          _______________________
za {ORG_NAME}                    za druhou stranu
```

## Pokyny k vyplnění

- Povinná pole označená [hranatými závorkami]
- Právní review povinné před podpisem u smluv nad 500 000 Kč
- Archivace podepsané verze v `knowledgebase/{domain}/templates/archive/`
"""


def _faq(title: str, domain: str, sensitivity: str) -> str:
    integration = _integration_name(domain)
    return _header(title, domain, "faq", sensitivity) + f"""## Často kladené dotazy

### Kdo je vlastník procesu v doméně {domain}?

Domain owner jmenuje představenstvo {ORG_NAME}. Kontaktujte `#domain-{domain}` na Slacku.

### Kde najdu autoritativní data?

Primární zdroj je integrace **{integration}**. KB dokumenty popisují interpretaci, nenahrazují systémová data.

### Jak často se dokumenty aktualizují?

Politiky a SOP minimálně ročně; runbooky po každém větším incidentu; FAQ průběžně dle dotazů z chat agentů.

### Jak nahlásit chybu v dokumentaci?

Vytvořte ticket typu `KB-FIX` s odkazem na cestu v `knowledgebase/{domain}/`.

### Mohu použít starší verzi šablony?

Ne — vždy používejte verzi označenou jako **core** nebo poslední schválenou v archive.

### Jak souvisí tento FAQ s chat agenty?

Doménoví agenti čerpají z tohoto FAQ a propojených runbooků pro odpovědi zaměstnancům {ORG_NAME}.
"""
