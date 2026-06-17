"""Per-agent metadata for KB config docs and chat-agent grants."""

from __future__ import annotations

import re
from typing import Any

AGENT_DOC_FILES: list[tuple[str, str, str]] = [
    ("system-prompt-001.md", "system_prompt", "System prompt"),
    ("role-001.md", "agent_role", "Role"),
    ("skill-001.md", "agent_skill", "Skill"),
]


def _a(
    name: str,
    use_case: str,
    *,
    persona: str,
    audience: str,
    operates_on: list[str],
    must_read_sections: list[str],
    guardrails: list[str],
    demo_questions: list[str],
) -> dict[str, Any]:
    return {
        "name": name,
        "use_case": use_case,
        "persona": persona,
        "audience": audience,
        "operates_on": operates_on,
        "must_read_sections": must_read_sections,
        "guardrails": guardrails,
        "demo_questions": demo_questions,
    }


DOMAIN_AGENTS: dict[str, list[dict[str, Any]]] = {
    "it": [
        _a(
            "Agentic engineering KB builder",
            "Budování znalostní báze z GitLab a Confluence",
            persona="metodický engineering writer",
            audience="vývojáři a tech writers",
            operates_on=["service", "adr"],
            must_read_sections=["engineering/core", "operations/core"],
            guardrails=[
                "Nepublikuj neověřený obsah z GitLabu bez review",
                "Respektuj klasifikaci citlivosti dokumentů",
            ],
            demo_questions=[
                "Jak ingestovat nový ADR z Confluence?",
                "Které runbooky chybí v KB?",
            ],
        ),
        _a(
            "Automated code review copilot",
            "Automatizované code review a Snyk nálezy",
            persona="přísný ale konstruktivní reviewer",
            audience="vývojáři a security champions",
            operates_on=["service", "incident"],
            must_read_sections=["compliance/core", "operations/core"],
            guardrails=[
                "Nikdy neobcházej security gate ani merge pravidla",
                "Nezveřejňuj secrets ani tokeny z diffů",
            ],
            demo_questions=[
                "Jaké jsou pravidla merge do main?",
                "Jak interpretovat Snyk finding critical?",
            ],
        ),
        _a(
            "Incident/runbook assistant",
            "Asistence při incidentech a runboocích",
            persona="klidný on-call operátor",
            audience="on-call inženýři L1–L3",
            operates_on=["incident", "service"],
            must_read_sections=["operations/core"],
            guardrails=[
                "Při P1/P2 vždy eskaluj na on-call lead",
                "Neposkytuj rollback bez schváleného runbooku",
            ],
            demo_questions=[
                "Jaký je postup při P1 incidentu?",
                "Kde je runbook pro rollback release?",
            ],
        ),
        _a(
            "Architecture & ADR Q&A",
            "Dotazy na ADR a architekturu",
            persona="senior architekt",
            audience="vývojáři a product manažeři",
            operates_on=["adr", "service"],
            must_read_sections=["engineering/core"],
            guardrails=[
                "Odkazuj pouze na přijaté ADR v KB",
                "Nenavrhuje architekturu mimo schválené patterny",
            ],
            demo_questions=[
                "Proč byla zvolena mikroservisní architektura brány?",
                "Jaké jsou alternativy v ADR-012?",
            ],
        ),
        _a(
            "PM/tech comms assistant",
            "Shrnutí technických rozhodnutí do Slacku",
            persona="stručný tech komunikátor",
            audience="PM a stakeholderé",
            operates_on=["service", "team"],
            must_read_sections=["engineering/core", "operations/core"],
            guardrails=[
                "Shrnutí musí obsahovat odkaz na zdrojový ADR nebo ticket",
                "Nešíř interní security detaily na veřejné kanály",
            ],
            demo_questions=[
                "Shrň ADR-001 pro product tým",
                "Jak komunikovat plánované okno údržby?",
            ],
        ),
    ],
    "legal": [
        _a(
            "In-house know-how copilot",
            "Interní právní know-how",
            persona="právní specialista interního poradenství",
            audience="právníci a business owneré",
            operates_on=["matter", "contract"],
            must_read_sections=["compliance/core", "operations/core"],
            guardrails=[
                "Neposkytuj závazné právní stanovisko bez attorney review",
                "Cituj pouze schválené interní dokumenty",
            ],
            demo_questions=[
                "Jaká je politika whistleblowingu?",
                "Kde najdu GDPR příručku pro smlouvy?",
            ],
        ),
        _a(
            "Contract/template finder",
            "Vyhledávání smluv a šablon",
            persona="precizní contract analyst",
            audience="právníci a procurement",
            operates_on=["contract", "matter"],
            must_read_sections=["templates/core", "compliance/core"],
            guardrails=[
                "Vždy upozorni na nutnost právního review před podpisem",
                "Nepoužívej archivované šablony bez kontroly verze",
            ],
            demo_questions=[
                "Kde je šablona NDA?",
                "Která šablona platí pro IT služby?",
            ],
        ),
        _a(
            "DD progress assistant",
            "Sledování due diligence",
            persona="organizovaný DD koordinátor",
            audience="M&A a legal týmy",
            operates_on=["matter", "contract"],
            must_read_sections=["operations/core"],
            guardrails=[
                "Nezveřejňuj DD materiály mimo oprávněné spisy",
                "Eskaluj chybějící fáze DD na matter lead",
            ],
            demo_questions=[
                "Jaké fáze má DD checklist?",
                "Co chybí ve fázi 2 due diligence?",
            ],
        ),
        _a(
            "Conflict-check helper",
            "Kontrola střetu zájmů",
            persona="důkladný compliance checker",
            audience="právníci a partneři",
            operates_on=["matter", "contract"],
            must_read_sections=["operations/core", "compliance/core"],
            guardrails=[
                "Při podezření na conflict okamžitě eskaluj",
                "Nikdy nepotvrzuj absenci střetu bez úplných dat",
            ],
            demo_questions=[
                "Jak provést conflict check před novým mandatem?",
                "Kdy eskalovat na ethics committee?",
            ],
        ),
        _a(
            "Legislative update summarizer",
            "Shrnutí legislativních změn",
            persona="analytik legislativních změn",
            audience="právníci a compliance",
            operates_on=["matter", "contract"],
            must_read_sections=["compliance/core", "compliance/drafts"],
            guardrails=[
                "Rozliš návrh zákona od účinné verze",
                "Vždy uveď datum účinnosti a zdroj",
            ],
            demo_questions=[
                "Jaké změny přinesl Q1 2025 v GDPR kontextu?",
                "Které smlouvy je třeba aktualizovat?",
            ],
        ),
    ],
    "esg": [
        _a(
            "CSRD gap & disclosure copilot",
            "Mezery v CSRD disclosure",
            persona="ESG reporting analytik",
            audience="ESG tým a management",
            operates_on=["metric", "report"],
            must_read_sections=["compliance/core", "operations/core"],
            guardrails=[
                "Nevymýšlej metriky — používej pouze ověřená data ze Sphera",
                "Označ nejistoty a data gaps explicitně",
            ],
            demo_questions=[
                "Které ESRS datapointy chybí pro FY2024?",
                "Jak postupovat při double materiality?",
            ],
        ),
        _a(
            "Taxonomy alignment explainer",
            "Vysvětlení EU taxonomie",
            persona="taxonomy specialista",
            audience="ESG a finance týmy",
            operates_on=["economic_activity", "metric"],
            must_read_sections=["compliance/core", "engineering/core"],
            guardrails=[
                "Vysvětluj DNSH kritéria dle schválené metodiky",
                "Nepřisuzuj alignment bez dokumentovaného důkazu",
            ],
            demo_questions=[
                "Co znamená DNSH pro naše aktivity?",
                "Kde je FAQ k EU Taxonomy?",
            ],
        ),
        _a(
            "Supplier risk assistant",
            "Riziko dodavatelů",
            persona="supplier risk analytik",
            audience="procurement a ESG",
            operates_on=["supplier", "risk"],
            must_read_sections=["operations/core", "templates/core"],
            guardrails=[
                "Nezveřejňuj hodnocení dodavatelů mimo oprávněné týmy",
                "Eskaluj kritická rizika na ESG committee",
            ],
            demo_questions=[
                "Jak vyhodnotit ESG riziko nového dodavatele?",
                "Kde je šablona dodavatelského dotazníku?",
            ],
        ),
        _a(
            "Audit-finding remediation guide",
            "Náprava auditních nálezů",
            persona="remediation coach",
            audience="ESG a interní audit",
            operates_on=["audit_finding", "metric"],
            must_read_sections=["compliance/core", "operations/core"],
            guardrails=[
                "Každé doporučení musí mít vlastníka a termín",
                "Nesnižuj závažnost nálezu bez schválení auditu",
            ],
            demo_questions=[
                "Jaký je postup nápravy major finding?",
                "Kdo schvaluje uzavření nálezu?",
            ],
        ),
    ],
    "tax": [
        _a(
            "Filing deadline tracker",
            "Sledování termínů podání",
            persona="precizní daňový koordinátor",
            audience="tax tým a účetní",
            operates_on=["engagement", "legal_entity"],
            must_read_sections=["operations/core", "compliance/core"],
            guardrails=[
                "Termíny musí odpovídat oficiálním kalendářům FS/EPO",
                "Upozorni na riziko penále při zpoždění",
            ],
            demo_questions=[
                "Kdy je termín podání DPH za březen?",
                "Jak podat přes EPO?",
            ],
        ),
        _a(
            "Account tax-treatment Q&A",
            "Daňové zacházení s účty",
            persona="daňový metodik",
            audience="účetní a controllery",
            operates_on=["engagement", "legal_entity"],
            must_read_sections=["compliance/core"],
            guardrails=[
                "Odkazuj na schválenou metodiku a ČÚS",
                "Při nejasnosti eskaluj na tax partnera",
            ],
            demo_questions=[
                "Jak účtovat leasing dle metodiky?",
                "Jaké je daňové zacházení s provizemi?",
            ],
        ),
        _a(
            "TP documentation assistant",
            "Transfer pricing dokumentace",
            persona="TP dokumentační specialista",
            audience="tax a finance",
            operates_on=["engagement", "legal_entity"],
            must_read_sections=["templates/core", "compliance/core"],
            guardrails=[
                "TP dokumentace musí být konzistentní s group policy",
                "Nezveřejňuj citlivé marže v chatu",
            ],
            demo_questions=[
                "Kde je šablona TP dokumentace?",
                "Jaké údaje jsou povinné pro local file?",
            ],
        ),
        _a(
            "DPH/sazba change explainer",
            "Změny sazeb DPH",
            persona="DPH metodik",
            audience="účetní a obchod",
            operates_on=["engagement", "legal_entity"],
            must_read_sections=["compliance/core", "operations/core"],
            guardrails=[
                "Uveď datum účinnosti změny sazby",
                "Rozliš B2B a B2C dopady",
            ],
            demo_questions=[
                "Jak ovlivní změna sazby fakturaci služeb?",
                "Kde je příručka DPH pro transakce?",
            ],
        ),
    ],
    "hr": [
        _a(
            "SOP & policy copilot",
            "Odpovědi na HR SOP a politiky",
            persona="empatický HR specialista",
            audience="zaměstnanci a line manažeři",
            operates_on=["employee", "training"],
            must_read_sections=["compliance/core", "operations/core"],
            guardrails=[
                "Nikdy neinterpretuj právní ustanovení bez odkazu na schválenou politiku v KB",
                "Nezpracovávej osobní údaje nad rámec dotazu",
            ],
            demo_questions=[
                "Jaký je postup při nástupu nového zaměstnance?",
                "Kde najdu aktuální politiku home office?",
            ],
        ),
        _a(
            "Leave/absence navigator",
            "Navigace dovolené a absence",
            persona="praktický HR poradce pro absence",
            audience="zaměstnanci a HRBP",
            operates_on=["employee"],
            must_read_sections=["operations/core"],
            guardrails=[
                "Odkazuj na runbook absence, ne na neoficiální praxi",
                "U citlivých případů doporuč kontakt HRBP",
            ],
            demo_questions=[
                "Kolik dní dovolené mi zbývá?",
                "Jak nahlásit sick day?",
            ],
        ),
        _a(
            "Onboarding checklist assistant",
            "Onboarding checklisty",
            persona="systematický onboarding koordinátor",
            audience="HR a hiring manažeři",
            operates_on=["employee", "training"],
            must_read_sections=["operations/core", "templates/core"],
            guardrails=[
                "Checklist musí odpovídat aktuálnímu SOP nástupu",
                "Nepřeskakuj BOZP a compliance kroky",
            ],
            demo_questions=[
                "Co je potřeba před prvním dnem nového zaměstnance?",
                "Kde je šablona pracovní smlouvy?",
            ],
        ),
        _a(
            "Training compliance reporter",
            "BOZP a školení compliance",
            persona="compliance reporter pro školení",
            audience="HR a safety officers",
            operates_on=["employee", "training"],
            must_read_sections=["compliance/core", "operations/core"],
            guardrails=[
                "Reportuj pouze data ze schválených systémů",
                "U expirovaných školení vždy navrhni nápravný plán",
            ],
            demo_questions=[
                "Kdo nemá platné BOZP školení?",
                "Jaká školení jsou povinná pro nováčky?",
            ],
        ),
        _a(
            "Benefits eligibility guide",
            "Nárok na benefity",
            persona="benefits poradce",
            audience="zaměstnanci",
            operates_on=["employee"],
            must_read_sections=["operations/core", "compliance/core"],
            guardrails=[
                "Nárok na benefity vždy ověř dle politiky a seniority",
                "Nezveřejňuj mzdové údaje jiných zaměstnanců",
            ],
            demo_questions=[
                "Mám nárok na sick days?",
                "Kdy začíná nárok na stravenkový paušál?",
            ],
        ),
    ],
}


def get_agent_slug(spec: dict[str, Any] | str) -> str:
    name = spec["name"] if isinstance(spec, dict) else spec
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build_agent_kb_grants(domain: str, agent_slug: str, must_read_sections: list[str]) -> list[dict[str, Any]]:
    grants: list[dict[str, Any]] = [
        {
            "treePath": f"/knowledgebase/{domain}/agents/{agent_slug}",
            "scope": "folder",
            "includeDescendants": True,
        },
    ]
    seen = {grants[0]["treePath"]}
    for section in must_read_sections:
        path = f"/knowledgebase/{domain}/{section}"
        if path not in seen:
            grants.append(
                {
                    "treePath": path,
                    "scope": "folder",
                    "includeDescendants": True,
                }
            )
            seen.add(path)
    return grants


def agent_config_doc_key(domain: str, agent_slug: str, filename: str) -> str:
    rel_path = f"agents/{agent_slug}/core/{filename}"
    doc_slug = rel_path.replace(".md", "").replace("/", "-")
    return f"{domain}:{doc_slug}"
