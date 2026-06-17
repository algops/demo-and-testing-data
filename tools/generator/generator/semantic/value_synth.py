"""Synthesize attribute values when propozice examples do not cover all fields."""

from __future__ import annotations

import random
from datetime import date, timedelta

from ..attribute_types import ValueScalar, coerce_for_type, get_data_type
from .attribute_pools import generate_from_pools

STATUSES = ["active", "draft", "archived", "under_review", "expired"]
JURISDICTIONS = ["EU", "CZ", "SK", "DE", "international"]
DEPARTMENTS = ["Engineering", "Finance", "Legal", "People", "ESG", "Operations", "Risk & Compliance"]
LOCATIONS = ["Praha", "Brno", "Bratislava", "remote"]


def _date_str(rng: random.Random, year: int = 2024) -> str:
    start = date(year, 1, 1)
    offset = rng.randint(0, 364)
    return (start + timedelta(days=offset)).isoformat()


def _meaningful_fallback(
    attr: str,
    type_slug: str,
    domain: str,
    index: int,
    display_name: str,
    rng: random.Random,
    data_type: str,
) -> ValueScalar:
    """Last-resort value that avoids generic {attr}_{N} patterns."""
    label = attr.replace("_", " ")
    if data_type == "boolean":
        return rng.choice([True, False])
    if data_type == "number":
        return rng.randint(1, 100) + index % 50
    if data_type == "date":
        return _date_str(rng)
    prefixes = {
        "esg": "ESG",
        "it": "IT",
        "legal": "Legal",
        "tax": "Tax",
        "hr": "HR",
        "shared": "Org",
    }
    prefix = prefixes.get(domain, "MP")
    return f"{prefix} {label} — {display_name[:40]}"


def generate(
    attr: str,
    type_slug: str,
    domain: str,
    index: int,
    display_name: str,
    rng: random.Random,
) -> ValueScalar:
    data_type = get_data_type(domain, attr)
    pooled = generate_from_pools(attr, type_slug, domain, index, display_name, rng)
    if pooled is not None:
        return coerce_for_type(pooled, data_type)

    a = attr.lower()

    if a in ("name", "title"):
        return display_name
    if a == "id" or a.endswith("_id"):
        prefix = type_slug[:3].upper()
        return f"{prefix}-{index + 1:04d}"
    if a == "code":
        return f"{type_slug[:4].upper()}-{index + 1:03d}"
    if "date" in a or a.endswith("_at"):
        return _date_str(rng, 2023 + (index % 2))
    if a in ("status", "assessment_status", "adoption_status", "mitigation_status", "compliance_status"):
        return rng.choice(STATUSES)
    if a in ("jurisdiction", "country"):
        return rng.choice(JURISDICTIONS if a == "jurisdiction" else ["CZ", "SK", "DE", "US", "IN"])
    if a in ("unit",):
        return rng.choice(["tCO2e", "%", "CZK", "count", "hours", "ms", "days"])
    if a in ("type", "sector", "subcategory"):
        return rng.choice(["operational", "financial", "governance", "technical"])
    if a in ("frequency", "refresh_frequency", "filing_frequency"):
        return rng.choice(["monthly", "quarterly", "annual", "weekly", "daily"])
    if a in ("owner", "owner_department", "risk_owner", "author", "responsible", "responsible_person"):
        return rng.choice(DEPARTMENTS)
    if a in ("version",):
        return f"v{rng.randint(1, 4)}.{rng.randint(0, 9)}"
    if a in ("language", "languages"):
        return rng.choice(["cs", "en", "cs/en"])
    if a in ("email",):
        slug = display_name.lower().replace(" ", ".")
        return f"{slug}@meridianpay.cz"
    if a in ("phone",):
        return f"+420 {rng.randint(600, 799)} {rng.randint(100, 999)} {rng.randint(100, 999)}"
    if a in ("location",):
        return rng.choice(LOCATIONS)
    if a == "benefits_tier":
        return rng.choice(["bronze", "silver", "gold", "platinum"])
    if a in ("tier",):
        return rng.randint(0, 3)
    if a in ("severity", "impact_level"):
        return rng.choice(["low", "medium", "high", "critical"])
    if a in ("likelihood",):
        return rng.choice(["low", "medium", "high"])
    if a in ("risk_score",):
        return rng.choice(["low", "medium", "high"])
    if a in ("mandatory", "critical", "material", "quantitative", "binding"):
        return coerce_for_type(rng.choice(["yes", "no"]), "boolean")
    if a in ("abbreviation",):
        return display_name[:6].upper()
    if a in ("enforcement_body", "issuing_body", "issuing_authority", "authority"):
        return rng.choice(["EU Commission", "ČNB", "MF ČR", "ISO", "GRI"])
    if a in ("format",):
        return rng.choice(["PDF", "xHTML/ESEF", "Excel", "JSON"])
    if a in ("assurance_level",):
        return rng.choice(["none", "limited", "reasonable"])
    if a in ("assurance_provider",):
        return "Deloitte CZ"
    if a in ("nace_code",):
        return f"{rng.randint(1, 9)}.{rng.randint(1, 9)}"
    if a in ("spend_annual_czk", "revenue", "capex_share_pct", "opex_share_pct", "revenue_share_pct"):
        return rng.randint(100_000, 50_000_000)
    if a in ("fte",):
        return round(rng.uniform(0.5, 1.0), 1)
    if a in ("employment_type",):
        return rng.choice(["full-time", "part-time", "contractor"])
    if a in ("cost_center",):
        return f"CC-{rng.randint(100, 599)}"
    if a in ("role_title", "department"):
        return rng.choice(DEPARTMENTS)
    if a in ("manager_id",):
        return f"EMP-{rng.randint(1, 200):04d}"

    return coerce_for_type(
        _meaningful_fallback(attr, type_slug, domain, index, display_name, rng, data_type),
        data_type,
    )
