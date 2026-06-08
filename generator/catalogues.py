"""Generate domain catalogue markdown files from propozice."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .attribute_types import get_data_type
from .util import ROOT, DOMAINS, load_json_block, slugify

DOMAIN_PROPOZICE = {
    "esg": "01_ESG_COMPLIANCE.md",
    "it": "02_IT_SW_DEVELOPMENT.md",
    "legal": "03_LEGAL.md",
    "tax": "04_TAX_ACCOUNTING.md",
    "hr": "05_HR_SOP.md",
}

DOMAIN_AGENTS: dict[str, list[dict[str, str]]] = {
    "it": [
        {"name": "Agentic engineering KB builder", "use_case": "Budování znalostní báze z GitLab a Confluence"},
        {"name": "Automated code review copilot", "use_case": "Automatizované code review a Snyk nálezy"},
        {"name": "Incident/runbook assistant", "use_case": "Asistence při incidentech a runboocích"},
        {"name": "Architecture & ADR Q&A", "use_case": "Dotazy na ADR a architekturu"},
        {"name": "PM/tech comms assistant", "use_case": "Shrnutí technických rozhodnutí do Slacku"},
    ],
    "legal": [
        {"name": "In-house know-how copilot", "use_case": "Interní právní know-how"},
        {"name": "Contract/template finder", "use_case": "Vyhledávání smluv a šablon"},
        {"name": "DD progress assistant", "use_case": "Sledování due diligence"},
        {"name": "Conflict-check helper", "use_case": "Kontrola střetu zájmů"},
        {"name": "Legislative update summarizer", "use_case": "Shrnutí legislativních změn"},
    ],
    "esg": [
        {"name": "CSRD gap & disclosure copilot", "use_case": "Mezery v CSRD disclosure"},
        {"name": "Taxonomy alignment explainer", "use_case": "Vysvětlení EU taxonomie"},
        {"name": "Supplier risk assistant", "use_case": "Riziko dodavatelů"},
        {"name": "Audit-finding remediation guide", "use_case": "Náprava auditních nálezů"},
    ],
    "tax": [
        {"name": "Filing deadline tracker", "use_case": "Sledování termínů podání"},
        {"name": "Account tax-treatment Q&A", "use_case": "Daňové zacházení s účty"},
        {"name": "TP documentation assistant", "use_case": "Transfer pricing dokumentace"},
        {"name": "DPH/sazba change explainer", "use_case": "Změny sazeb DPH"},
    ],
    "hr": [
        {"name": "SOP & policy copilot", "use_case": "Odpovědi na HR SOP a politiky"},
        {"name": "Leave/absence navigator", "use_case": "Navigace dovolené a absence"},
        {"name": "Onboarding checklist assistant", "use_case": "Onboarding checklisty"},
        {"name": "Training compliance reporter", "use_case": "BOZP a školení compliance"},
        {"name": "Benefits eligibility guide", "use_case": "Nárok na benefity"},
    ],
}

DOMAIN_INTEGRATIONS: dict[str, list[dict[str, str]]] = {
    "it": [
        {"name": "GitLab", "role": "source"},
        {"name": "Confluence", "role": "source"},
        {"name": "Slack", "role": "source"},
        {"name": "Datadog", "role": "source"},
        {"name": "LLM gateway", "role": "tool"},
        {"name": "Snyk", "role": "tool"},
        {"name": "Engineering metrics warehouse", "role": "destination"},
    ],
    "legal": [
        {"name": "iManage", "role": "source"},
        {"name": "SharePoint", "role": "source"},
        {"name": "Beck-online", "role": "source"},
        {"name": "OCR redaction LLM", "role": "tool"},
        {"name": "Contracts/matter index", "role": "destination"},
    ],
    "esg": [
        {"name": "Sphera", "role": "source"},
        {"name": "ERP/HR feeds", "role": "source"},
        {"name": "Supplier portal", "role": "source"},
        {"name": "ESRS mapping assistant", "role": "tool"},
        {"name": "Readiness scores export", "role": "destination"},
    ],
    "tax": [
        {"name": "Pohoda", "role": "source"},
        {"name": "EPO", "role": "source"},
        {"name": "Datová schránka", "role": "source"},
        {"name": "Tax calc validators", "role": "tool"},
        {"name": "Filing status export", "role": "destination"},
    ],
    "hr": [
        {"name": "SAP SuccessFactors", "role": "source"},
        {"name": "Recruitee", "role": "source"},
        {"name": "SharePoint HR", "role": "source"},
        {"name": "LLM HR assistant", "role": "tool"},
        {"name": "HR SOP answers dataset", "role": "destination"},
    ],
}

TYPE_REFRAME = {
    "legal": {"Client": "Counterparty"},
    "tax": {"Client": "LegalEntity"},
}


def _load_domain_spec(domain: str) -> tuple[list[dict], list[dict]]:
    path = ROOT / "docs" / DOMAIN_PROPOZICE[domain]
    block = load_json_block(path, "entity_types")
    types = block.get("entity_types", [])
    rel_block = load_json_block(path, "relationship_types")
    rels = rel_block.get("relationship_types", [])
    reframe = TYPE_REFRAME.get(domain, {})
    for t in types:
        if t["type"] in reframe:
            t["type"] = reframe[t["type"]]
    for r in rels:
        for key in ("from", "to"):
            val = r[key]
            if isinstance(val, list):
                r[key] = [reframe.get(v, v) for v in val]
            elif val in reframe:
                r[key] = reframe[val]
    return types, rels


def write_object_types(domain: str, types: list[dict], out: Path) -> None:
    lines = [
        f"# {domain.upper()} — Object types",
        "",
        "**Anchor:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)",
        "",
        "| Slug | Propozice type | Attributes |",
        "|------|----------------|------------|",
    ]
    for t in types:
        slug = slugify(t["type"])
        attrs = ", ".join(t.get("attributes", []))
        lines.append(f"| `{slug}` | {t['type']} | {attrs} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_datapoints(domain: str, types: list[dict], out: Path) -> None:
    lines = [
        f"# {domain.upper()} — Datapoints",
        "",
        "Fields from propozice `attributes[]`; edge via `defines_schema`.",
        "",
    ]
    for t in types:
        slug = slugify(t["type"])
        lines.append(f"## `{slug}`")
        for attr in t.get("attributes", []):
            dtype = get_data_type(domain, attr)
            lines.append(f"- `{attr}` — {dtype}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def write_values(domain: str, rels: list[dict], out: Path) -> None:
    lines = [
        f"# {domain.upper()} — Values",
        "",
        "Domain edge attributes with quantitative/temporal data materialize as `value` records.",
        "",
        "| Edge type | Attributes → values |",
        "|-----------|---------------------|",
    ]
    for r in rels:
        attrs = ", ".join(r.get("attributes", []))
        lines.append(f"| {r['type']} | {attrs} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_agents(domain: str, out: Path) -> None:
    lines = [
        f"# {domain.upper()} — Agents (use-case based)",
        "",
        "| Agent | Primary use-case (cs) |",
        "|-------|----------------------|",
    ]
    for a in DOMAIN_AGENTS[domain]:
        lines.append(f"| {a['name']} | {a['use_case']} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_integrations(domain: str, out: Path) -> None:
    lines = [
        f"# {domain.upper()} — Integrations",
        "",
        "| Name | Role |",
        "|------|------|",
    ]
    for i in DOMAIN_INTEGRATIONS[domain]:
        lines.append(f"| {i['name']} | {i['role']} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_relationship_matrix(domain: str, rels: list[dict], out: Path) -> None:
    lines = [
        f"# {domain.upper()} — Relationship matrix",
        "",
        "Domain-native edges from propozice §5, projected to AlgOps `related_to` (+ optional values).",
        "",
        "| Domain edge | From → To | AlgOps projection |",
        "|-------------|-----------|-------------------|",
    ]
    for r in rels:
        lines.append(
            f"| {r['type']} | {r['from']} → {r['to']} | object→object `related_to`; edge attrs → values |"
        )
    lines.extend(
        [
            "",
            "**Validation:** same `domain_id`; no cross-domain-native edges without org-bridge.",
        ]
    )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


DOMAIN_KB_TITLES: dict[str, list[dict[str, str]]] = {
    "esg": [
        {"kind": "policy", "section": "compliance", "sub": "core", "title": "Politika životního prostředí Meridian Pay"},
        {"kind": "guideline", "section": "compliance", "sub": "core", "title": "Příručka CSRD a ESRS pro FY2024"},
        {"kind": "runbook", "section": "operations", "sub": "core", "title": "Runbook sběru emisních dat Scope 1–3"},
        {"kind": "sop", "section": "operations", "sub": "core", "title": "SOP: Double materiality assessment"},
        {"kind": "template", "section": "templates", "sub": "core", "title": "Šablona ESG dotazníku pro dodavatele"},
        {"kind": "faq", "section": "engineering", "sub": "core", "title": "FAQ: EU Taxonomy a DNSH kritéria"},
        {"kind": "policy", "section": "compliance", "sub": "archive", "title": "Politika udržitelného financování v1"},
        {"kind": "runbook", "section": "operations", "sub": "drafts", "title": "Runbook: CSDDD due diligence dodavatelů"},
        {"kind": "guideline", "section": "compliance", "sub": "drafts", "title": "Metodika výpočtu taxonomy alignment KPI"},
        {"kind": "adr", "section": "engineering", "sub": "core", "title": "ADR: Architektura ESG datové platformy"},
    ],
    "it": [
        {"kind": "adr", "section": "engineering", "sub": "core", "title": "ADR-001: Mikroservisní architektura platební brány"},
        {"kind": "runbook", "section": "operations", "sub": "core", "title": "Runbook incident response P1/P2"},
        {"kind": "sop", "section": "operations", "sub": "core", "title": "SOP: Code review a merge do main"},
        {"kind": "policy", "section": "compliance", "sub": "core", "title": "Politika bezpečnosti vývoje (Secure SDLC)"},
        {"kind": "guideline", "section": "engineering", "sub": "core", "title": "Příručka observability — Datadog a SLO"},
        {"kind": "template", "section": "templates", "sub": "core", "title": "Šablona RFC pro změny infrastruktury"},
        {"kind": "faq", "section": "engineering", "sub": "drafts", "title": "FAQ: GitLab CI/CD a release train"},
        {"kind": "runbook", "section": "operations", "sub": "archive", "title": "Runbook: Rollback produkčního release"},
        {"kind": "adr", "section": "engineering", "sub": "archive", "title": "ADR-012: Event-driven integrace s core banking"},
        {"kind": "sop", "section": "operations", "sub": "drafts", "title": "SOP: On-call rotace a eskalace"},
        {"kind": "guideline", "section": "compliance", "sub": "core", "title": "Příručka Snyk a dependency scanning"},
        {"kind": "policy", "section": "compliance", "sub": "drafts", "title": "Politika přístupu k produkčním systémům"},
    ],
    "legal": [
        {"kind": "policy", "section": "compliance", "sub": "core", "title": "Politika compliance a whistleblowingu"},
        {"kind": "template", "section": "templates", "sub": "core", "title": "Šablona NDA — standardní ujednání"},
        {"kind": "sop", "section": "operations", "sub": "core", "title": "SOP: Conflict check před novým mandatem"},
        {"kind": "guideline", "section": "compliance", "sub": "core", "title": "Příručka GDPR pro smluvní vztahy"},
        {"kind": "runbook", "section": "operations", "sub": "core", "title": "Runbook: Due diligence — fáze a checklist"},
        {"kind": "faq", "section": "templates", "sub": "core", "title": "FAQ: iManage a správa spisů"},
        {"kind": "template", "section": "templates", "sub": "archive", "title": "Šablona smlouvy o dílo — IT služby"},
        {"kind": "policy", "section": "compliance", "sub": "archive", "title": "Politika schvalování smluv nad 500 tis. Kč"},
        {"kind": "guideline", "section": "compliance", "sub": "drafts", "title": "Přehled legislativních změn Q1 2025"},
        {"kind": "runbook", "section": "operations", "sub": "drafts", "title": "Runbook: Redakce citlivých údajů ve spisech"},
    ],
    "tax": [
        {"kind": "guideline", "section": "compliance", "sub": "core", "title": "Příručka DPH pro finanční transakce"},
        {"kind": "sop", "section": "operations", "sub": "core", "title": "SOP: Měsíční DPH kontrola a podání"},
        {"kind": "runbook", "section": "operations", "sub": "core", "title": "Runbook: Roční daň z příjmů PO"},
        {"kind": "template", "section": "templates", "sub": "core", "title": "Šablona transfer pricing dokumentace"},
        {"kind": "faq", "section": "compliance", "sub": "core", "title": "FAQ: Elektronické podání přes EPO"},
        {"kind": "policy", "section": "compliance", "sub": "core", "title": "Politika daňového řízení a archivace"},
        {"kind": "guideline", "section": "compliance", "sub": "archive", "title": "Metodika účtování leasingu dle ČÚS"},
        {"kind": "runbook", "section": "operations", "sub": "drafts", "title": "Runbook: Kontrola od finanční správy"},
        {"kind": "sop", "section": "operations", "sub": "archive", "title": "SOP: Zpracování záloh na daň z příjmů"},
        {"kind": "template", "section": "templates", "sub": "drafts", "title": "Šablona potvrzení pro zahraniční zdanění"},
    ],
    "hr": [
        {"kind": "policy", "section": "compliance", "sub": "core", "title": "Politika pracovněprávních vztahů"},
        {"kind": "sop", "section": "operations", "sub": "core", "title": "SOP: Nástup nového zaměstnance"},
        {"kind": "runbook", "section": "operations", "sub": "core", "title": "Runbook: Řízení absence a dovolené"},
        {"kind": "template", "section": "templates", "sub": "core", "title": "Šablona pracovní smlouvy — HQ"},
        {"kind": "faq", "section": "operations", "sub": "core", "title": "FAQ: Benefity a sick days"},
        {"kind": "guideline", "section": "compliance", "sub": "core", "title": "Příručka BOZP a povinná školení"},
        {"kind": "policy", "section": "compliance", "sub": "archive", "title": "Politika home office v1"},
        {"kind": "sop", "section": "operations", "sub": "drafts", "title": "SOP: Offboarding a předání přístupů"},
        {"kind": "runbook", "section": "operations", "sub": "archive", "title": "Runbook: Roční hodnocení výkonu"},
        {"kind": "template", "section": "templates", "sub": "drafts", "title": "Šablona interního přesunu"},
    ],
}


def get_kb_doc_specs(domain: str, min_docs: int) -> list[dict[str, str]]:
    specs = DOMAIN_KB_TITLES.get(domain, [])
    if len(specs) >= min_docs:
        return specs[:min_docs]
    kinds = ["policy", "guideline", "runbook", "sop", "template", "faq", "adr"]
    out = list(specs)
    for i in range(len(out), min_docs):
        kind = kinds[i % len(kinds)]
        section = ["engineering", "compliance", "operations", "templates"][i % 4]
        sub = ["core", "archive", "drafts"][i % 3]
        out.append(
            {
                "kind": kind,
                "section": section,
                "sub": sub,
                "title": f"{domain.upper()} — {kind} {i + 1}",
            }
        )
    return out


def write_kb_manifest(domain: str, min_docs: int, out: Path) -> None:
    lines = [
        f"# {domain.upper()} — KB manifest",
        "",
        f"Paths under `knowledgebase/{domain}/`. Minimum docs: **{min_docs}**.",
        "",
        "| path | doc_kind | title_cs | sensitivity | source_integration |",
        "|------|----------|----------|-------------|-------------------|",
    ]
    for i, spec in enumerate(get_kb_doc_specs(domain, min_docs)):
        path = f"{spec['section']}/{spec['sub']}/{spec['kind']}-{i + 1:03d}.md"
        lines.append(
            f"| `{path}` | {spec['kind']} | {spec['title']} | internal | {DOMAIN_INTEGRATIONS[domain][0]['name']} |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_catalogues(min_docs: dict[str, int]) -> None:
    for domain in DOMAINS:
        types, rels = _load_domain_spec(domain)
        base = ROOT / "docs" / "domains" / domain
        base.mkdir(parents=True, exist_ok=True)
        write_object_types(domain, types, base / "OBJECT_TYPES.md")
        write_datapoints(domain, types, base / "DATAPOINTS.md")
        write_values(domain, rels, base / "VALUES.md")
        write_agents(domain, base / "AGENTS.md")
        write_integrations(domain, base / "INTEGRATIONS.md")
        write_relationship_matrix(domain, rels, base / "RELATIONSHIP_MATRIX.md")
        write_kb_manifest(domain, min_docs.get(domain, 25), base / "KB_MANIFEST.md")
