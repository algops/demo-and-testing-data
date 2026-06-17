"""Domain-aware attribute value pools for realistic demo data."""

from __future__ import annotations

import random
from datetime import date, timedelta
from typing import Any

from ..attribute_types import ValueScalar, coerce_for_type, get_data_type

CZ_LAWS = [
    "zákon č. 416/2009 Sb.",
    "zákon č. 563/1991 Sb.",
    "zákon č. 262/2006 Sb.",
    "zákon č. 110/2019 Sb.",
    "zákon č. 90/2012 Sb.",
]

ESG_STANDARDS = ["ESRS E1", "ESRS S1", "ESRS G1", "GRI 305", "GRI 401", "GHG Protocol", "SASB"]
IT_ECOSYSTEMS = ["npm", "Maven Central", "PyPI", "NuGet", "crates.io", "RubyGems"]
LICENSES = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "ISC", "MPL-2.0"]
AREA_OF_LAW = ["corporate", "employment", "data protection", "commercial", "litigation", "regulatory"]
GOVERNING_LAW = ["Czech law", "EU law", "Slovak law", "German law"]
CLIENTS = [
    "Meridian Pay a.s.",
    "Meridian Pay SK s.r.o.",
    "Anchor Payments GmbH",
    "Internal — Group Treasury",
]
COUNTERPARTIES = [
    "Kovář & Partners advokátní kancelář s.r.o.",
    "Deloitte CZ",
    "Finanční Centrum s.r.o.",
    "Benefity a.s.",
    "AWS EMEA",
]
DATA_SOURCES = {
    "esg": ["Sphera", "ERP/HR feeds", "Supplier portal", "Utility invoices"],
    "it": ["GitLab", "Datadog", "Confluence", "PagerDuty"],
    "legal": ["iManage", "SharePoint", "Beck-online"],
    "tax": ["Pohoda", "EPO", "SAP"],
    "hr": ["SAP SuccessFactors", "Recruitee", "SharePoint"],
}
DISCLOSURE_CODES = ["ESRS E1-6", "ESRS S1-14", "ESRS G1-1", "E1.5", "S1.1", "G1.3"]
CLOUD_PROVIDERS = ["AWS", "GCP", "Azure", "on-prem"]
FRAMEWORKS = ["NestJS", "Spring Boot", "React", "Next.js", "FastAPI", "Express"]
ENGINES = ["Node.js", "JVM", "Python", "Go", "Rust"]


def _date_str(rng: random.Random, year: int = 2024) -> str:
    start = date(year, 1, 1)
    return (start + timedelta(days=rng.randint(0, 364))).isoformat()


def _semver(rng: random.Random) -> str:
    return f"{rng.randint(1, 5)}.{rng.randint(0, 12)}.{rng.randint(0, 9)}"


def _description(domain: str, type_slug: str, display_name: str, attr: str) -> str:
    templates = {
        "esg": f"{display_name} supports CSRD evidence collection and ESRS alignment for Meridian Pay.",
        "it": f"{display_name} is part of the Meridian Pay engineering platform ({type_slug}).",
        "legal": f"{display_name} — legal record maintained under Czech counsel review.",
        "tax": f"{display_name} — tax filing and compliance context for Meridian Pay group.",
        "hr": f"{display_name} — HR policy and SOP reference for Meridian Pay employees.",
    }
    return templates.get(domain, f"{display_name} — {attr.replace('_', ' ')} for Meridian Pay operations.")


# Per-attribute generator callables: (attr, type_slug, domain, index, display_name, rng) -> ValueScalar
_ATTR_GENERATORS: dict[str, Any] = {}


def _register(attr: str, fn: Any) -> None:
    _ATTR_GENERATORS[attr] = fn


def _pool_choice(pool: list, rng: random.Random) -> str:
    return rng.choice(pool)


for _attr, _pool in [
    ("ecosystem", IT_ECOSYSTEMS),
    ("license", LICENSES),
    ("area_of_law", AREA_OF_LAW),
    ("governing_law", GOVERNING_LAW),
    ("standard", ESG_STANDARDS),
    ("standard_reference", ESG_STANDARDS),
    ("transposition_law", CZ_LAWS),
    ("cloud_provider", CLOUD_PROVIDERS),
    ("framework", FRAMEWORKS),
    ("engine", ENGINES),
    ("client", CLIENTS),
    ("counterparty", COUNTERPARTIES),
    ("target_company", CLIENTS),
    ("vendor", ["Deloitte CZ", "Kovář & Partners advokátní kancelář s.r.o.", "Finanční Centrum s.r.o."]),
]:
    _register(_attr, lambda a, ts, d, i, dn, rng, p=_pool: _pool_choice(p, rng))


def generate_from_pools(
    attr: str,
    type_slug: str,
    domain: str,
    index: int,
    display_name: str,
    rng: random.Random,
) -> ValueScalar | None:
    """Return a typed value from pools/generators, or None to defer to value_synth."""
    if domain == "it":
        from ..it_corpus import warehouse_terms

        terms = warehouse_terms()
        if attr == "name" and type_slug == "service":
            pool = terms.get("services", [])
            if pool:
                return pool[index % len(pool)]
        if attr == "name" and type_slug == "pipeline":
            pool = terms.get("pipelines", [])
            if pool:
                return pool[index % len(pool)]
        if attr in ("title", "name") and type_slug == "incident":
            pool = terms.get("incidents", [])
            if pool:
                return f"INC-{index + 1:03d} {pool[index % len(pool)]}"
        if attr == "title" and type_slug == "tech_debt":
            pool = terms.get("tech_debt", [])
            if pool:
                return f"TD-{index + 1:03d} {pool[index % len(pool)]}"
        if attr == "name" and type_slug == "team":
            pool = terms.get("teams", [])
            if pool:
                return pool[index % len(pool)]

    if attr in _ATTR_GENERATORS:
        raw = _ATTR_GENERATORS[attr](attr, type_slug, domain, index, display_name, rng)
        return coerce_for_type(raw, get_data_type(domain, attr))

    data_type = get_data_type(domain, attr)
    a = attr.lower()

    if a in ("current_version", "latest_version"):
        return _semver(rng)
    if a == "mandatory_for_all":
        return rng.choice([True, False])
    if a == "datapoints_count":
        return rng.randint(8, 120)
    if a in ("cve_count",):
        return rng.randint(0, 12)
    if a in ("cve_critical",):
        return rng.randint(0, 3)
    if a == "value_czk":
        return rng.randint(50_000, 5_000_000)
    if a.endswith("_czk") or a.endswith("_amount_czk"):
        return rng.randint(10_000, 2_000_000)
    if a.endswith("_count") or a == "headcount" or a == "member_count":
        return rng.randint(1, 200)
    if a.endswith("_pct") or a.endswith("_score") and a != "risk_score":
        return rng.randint(5, 98)
    if a.endswith("_minutes") or a.endswith("_hours") or a.endswith("_days"):
        return rng.randint(1, 180)
    if a.endswith("_year") and a not in ("reporting_period",):
        return rng.randint(2020, 2026)
    if "date" in a or a.endswith("_at"):
        return _date_str(rng, 2023 + (index % 2))
    if a == "data_source":
        return rng.choice(DATA_SOURCES.get(domain, ["Internal system"]))
    if a == "disclosure_requirement":
        return rng.choice(DISCLOSURE_CODES)
    if a == "system" or a == "system_used":
        return rng.choice(["GitLab", "SAP SuccessFactors", "Pohoda", "Sphera", "iManage"])
    if a == "applies_to":
        return rng.choice(["all employees", "engineering", "management", "EU entities"])
    if a == "template_used":
        return rng.choice(["MSA v3.2", "NDA standard", "DPA template", "SOW template"])
    if a in ("description", "scope", "methodology", "known_issues", "known_gaps"):
        return _description(domain, type_slug, display_name, attr)
    if a == "accounting_system":
        return rng.choice(["Pohoda", "SAP", "Oracle NetSuite"])
    if a == "approval_chain":
        return rng.choice(["Legal → CFO", "HR → People Ops", "Engineering → CTO", "Compliance → Board"])
    if a == "legal_area" or a == "parent_area":
        return rng.choice(AREA_OF_LAW)
    if a == "service":
        if domain == "it":
            from ..it_corpus import warehouse_terms

            pool = warehouse_terms().get("services", [])
            if pool:
                return pool[index % len(pool)]
        return rng.choice(["payments-api", "ledger-service", "auth-gateway", "notification-hub"])
    if a == "topic":
        return rng.choice(["climate", "workforce", "governance", "biodiversity", "supply chain"])
    if a == "metric":
        return rng.choice(["Scope 1 emissions", "Employee turnover", "Water consumption"])
    if a == "platform":
        if domain == "it":
            return rng.choice(["GitLab CI", "GitLab Runner", "Kubernetes", "release-it"])
    if a == "protocol":
        return rng.choice(["HTTPS", "gRPC", "AMQP", "WebSocket"])
    if a == "provider":
        return rng.choice(["AWS", "Cloudflare", "Auth0", "SendGrid"])
    if a == "region":
        return rng.choice(["eu-central-1", "eu-west-1", "CZ", "SK"])
    if a == "hosting":
        return rng.choice(["AWS", "on-prem", "hybrid"])
    if a == "domain":
        return domain if domain != "shared" else rng.choice(["it", "hr", "legal", "esg", "tax"])
    if a == "url" or a == "base_url" or a == "repo_url" or a == "docs_url":
        slug = type_slug.replace("_", "-")
        return f"https://{slug}.meridianpay.cz/{index + 1}"
    if a == "law_reference":
        return rng.choice(CZ_LAWS)
    if a == "cited_legislation":
        return rng.choice(["§ 262/2006 Sb.", "§ 110/2019 Sb.", "GDPR Art. 6"])
    if a == "court":
        return rng.choice(["Městský soud v Praze", "Krajský soud v Brně", "OS Brno"])
    if a == "trigger":
        return rng.choice(["manual", "scheduled", "webhook", "threshold"])
    if a == "resolution":
        return rng.choice(["resolved", "mitigated", "accepted", "open"])
    if a == "root_cause_category":
        return rng.choice(["config", "dependency", "capacity", "human error"])
    if a == "blocked_by":
        return rng.choice(["security review", "dependency upgrade", "QA sign-off", "none"])
    if a == "breaking_changes":
        return rng.choice(["none", "API v2", "schema migration", "auth change"])
    if a == "access_control":
        return rng.choice(["RBAC", "ABAC", "OAuth2 scopes", "mTLS"])
    if a == "auth_method":
        return rng.choice(["OAuth2", "SAML", "API key", "mTLS"])
    if a == "backup_policy":
        return rng.choice(["daily", "hourly", "continuous", "weekly"])
    if a == "category":
        if domain == "esg":
            return rng.choice(["E", "S", "G"])
        return rng.choice(["operational", "financial", "governance", "technical", "compliance"])

    return None
