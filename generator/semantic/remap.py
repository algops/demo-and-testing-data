"""Apply ANCHOR_TENANT vignette remap rules to generated text."""

from __future__ import annotations

import re

REMAP_RULES: list[tuple[str, str]] = [
    ("Finbee s.r.o.", "Meridian Pay a.s."),
    ("Finbee", "Meridian Pay"),
    ("ČEZ Energo Solutions a.s.", "Meridian Pay a.s."),
    ("ČEZ Energo", "Meridian Pay"),
    ("VTM a.s.", "Meridian Pay a.s."),
    ("VTM", "Meridian Pay"),
    ("Kovář & Partners (as tenant)", "Meridian Pay Legal"),
    ("Finanční Centrum (as tenant)", "Meridian Pay Finance"),
    ("legacy-order-monolith", "legacy-ledger-monolith"),
    ("legacy order monolith", "legacy-ledger-monolith"),
    ("LogiCorp", "LogiCorp"),
    ("Project Falcon", "Project Falcon"),
    ("Brno-Líšeň", "Brno"),
    ("Olomouc", "Brno"),
    ("user-auth-svc", "auth-service"),
    ("payment-gateway", "payment-gateway"),
    ("TechNova", "Meridian Pay"),
    ("RetailCo", "Partner Retail s.r.o."),
    ("BankCo", "Meridian Pay a.s."),
    ("StartupX", "PayFlow SK s.r.o."),
    ("Průmyslový holding a.s.", "LogiCorp a.s."),
    ("Průmyslový holding", "LogiCorp"),
]


def remap_text(text: str, domain: str | None = None) -> str:
    out = text
    for old, new in REMAP_RULES:
        out = out.replace(old, new)
    if domain == "it":
        out = re.sub(r"\buser-service\b", "auth-service", out)
    if domain == "hr":
        out = re.sub(r"\bManufacturing\b", "Engineering", out)
        out = re.sub(r"\bCNC Operator\b", "Software Engineer", out)
        out = re.sub(r"\bROL-MFG-", "ROL-ENG-", out)
    if domain == "esg":
        out = re.sub(r"\buhlí\b", "data centre energy", out, flags=re.IGNORECASE)
        out = re.sub(r"\bcoal\b", "fintech operations", out, flags=re.IGNORECASE)
    return out
