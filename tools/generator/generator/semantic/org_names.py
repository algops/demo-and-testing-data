"""Czech org-layer names and employment attributes."""

from __future__ import annotations

import random
from typing import Any

ORG_PERSON_ATTRS = ["first_name", "last_name", "email", "phone", "location"]

ORG_EMPLOYEE_ATTRS = [
    "employee_id",
    "hire_date",
    "employment_type",
    "department",
    "role_title",
    "manager_id",
    "status",
    "fte",
    "cost_center",
]

ORG_TEAM_NAMES = [
    "Payments Squad",
    "Auth & Identity",
    "Ledger Platform",
    "Integrations",
    "Platform/Infra",
    "Data Engineering",
    "Risk & Compliance",
    "Legal Practice",
    "ESG Programme",
    "Finance Ops",
    "People Ops",
    "Growth",
    "Customer Success",
    "Product Design",
    "SRE On-call",
    "Security",
]

ORG_KPI_ATTRS = [
    "deployment_frequency",
    "incident_mttr_minutes",
    "tech_debt_ratio_pct",
    "sop_query_response_hours",
    "onboarding_completion_pct",
    "template_find_time_minutes",
    "filing_on_time_pct",
    "open_deadline_count",
    "esrs_coverage_pct",
    "supplier_response_rate_pct",
]

FIRST_NAMES = [
    "Eva", "Martin", "Jana", "Tomáš", "Petra", "Pavel", "Lucie", "Jakub",
    "Kateřina", "Michal", "Veronika", "David", "Alena", "Filip", "Markéta",
    "Ondřej", "Barbora", "Lukáš", "Tereza", "Adam", "Kristýna", "Jiří",
    "Michaela", "Vojtěch", "Lenka", "Marek", "Simona", "Radek", "Hana",
    "Daniel",
]

LAST_NAMES = [
    "Nováková", "Procházka", "Svobodová", "Dvořák", "Černý", "Horáková",
    "Kučera", "Veselý", "Krejčí", "Benešová", "Fiala", "Pokorná", "Král",
    "Jelínková", "Růžička", "Bartoš", "Němcová", "Urban", "Šimek", "Vlčková",
    "Kolář", "Machová", "Štěpánek", "Rychlá", "Holub", "Sedláčková",
    "Moravec", "Bláhová", "Hájek", "Kříž",
]

DEPARTMENTS = [
    "Engineering", "Product", "Operations", "Risk & Compliance",
    "Finance", "People", "ESG", "Sales", "G&A", "Legal",
]

ROLE_TITLES = [
    "Software Engineer", "Senior Engineer", "Engineering Manager",
    "Product Manager", "Compliance Analyst", "Legal Counsel",
    "HR Business Partner", "ESG Analyst", "Tax Specialist",
    "Accountant", "SRE", "Data Engineer", "QA Engineer",
]


def _pick_name(index: int, rng: random.Random) -> tuple[str, str]:
    fn = FIRST_NAMES[index % len(FIRST_NAMES)]
    ln = LAST_NAMES[(index * 7 + 3) % len(LAST_NAMES)]
    if index > len(FIRST_NAMES) * len(LAST_NAMES):
        ln = f"{ln} {(index // 30) + 1}"
    return fn, ln


def generate_person_attrs(index: int, rng: random.Random) -> dict[str, str]:
    fn, ln = _pick_name(index, rng)
    email_slug = f"{fn.lower()}.{ln.lower().replace(' ', '')}"
    email_slug = (
        email_slug.replace("á", "a").replace("č", "c").replace("ě", "e")
        .replace("í", "i").replace("ň", "n").replace("ó", "o")
        .replace("ř", "r").replace("š", "s").replace("ť", "t")
        .replace("ú", "u").replace("ů", "u").replace("ý", "y")
        .replace("ž", "z")
    )
    return {
        "first_name": fn,
        "last_name": ln,
        "email": f"{email_slug}@meridianpay.cz",
        "phone": f"+420 {600 + (index % 100)} {100 + (index % 800):03d} {100 + (index % 900):03d}",
        "location": rng.choice(["Praha", "Brno", "remote", "Bratislava"]),
    }


def generate_employee_attrs(
    index: int,
    person_attrs: dict[str, str],
    rng: random.Random,
) -> dict[str, str | int | float]:
    year = 2018 + (index % 7)
    month = 1 + (index % 12)
    day = 1 + (index % 28)
    dept = DEPARTMENTS[index % len(DEPARTMENTS)]
    return {
        "employee_id": f"EMP-{index + 1:04d}",
        "hire_date": f"{year}-{month:02d}-{day:02d}",
        "employment_type": rng.choice(["full-time", "part-time", "contractor"]),
        "department": dept,
        "role_title": ROLE_TITLES[index % len(ROLE_TITLES)],
        "manager_id": f"EMP-{max(1, (index % 20) + 1):04d}",
        "status": rng.choice(["active", "active", "active", "on_leave", "terminated"]),
        "fte": round(rng.choice([1.0, 1.0, 0.8, 0.5]), 1),
        "cost_center": f"CC-{100 + (index % 500)}",
    }


def generate_team_attrs(team_name: str, index: int, rng: random.Random) -> dict[str, str | int]:
    return {
        "name": team_name,
        "slug": team_name.lower().replace(" ", "-").replace("/", "-"),
        "domain": rng.choice(["it", "hr", "legal", "esg", "tax", "shared"]),
        "headcount": rng.randint(4, 12),
        "location": rng.choice(["Brno", "Praha", "remote"]),
        "channel": f"#team-{team_name.split()[0].lower()}",
    }


def generate_org_kpi_values(rng: random.Random) -> dict[str, str | int]:
    return {
        "deployment_frequency": f"{rng.randint(2, 15)}/week",
        "incident_mttr_minutes": rng.randint(8, 45),
        "tech_debt_ratio_pct": rng.randint(12, 28),
        "sop_query_response_hours": rng.randint(1, 8),
        "onboarding_completion_pct": rng.randint(78, 96),
        "template_find_time_minutes": rng.randint(3, 25),
        "filing_on_time_pct": rng.randint(85, 100),
        "open_deadline_count": rng.randint(0, 5),
        "esrs_coverage_pct": rng.randint(72, 94),
        "supplier_response_rate_pct": rng.randint(55, 85),
    }


ORG_TEAM_ATTRS = ["name", "slug", "domain", "headcount", "location", "channel"]
