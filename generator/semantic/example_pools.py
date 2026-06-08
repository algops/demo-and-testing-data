"""Parse propozice examples into realistic object instances."""

from __future__ import annotations

import re
from typing import Any

from ..attribute_types import ValueScalar, coerce_for_type, get_data_type
from .remap import remap_text
from .value_synth import generate


def _primary_label(example: str) -> tuple[str, str | None]:
    """Return display name and optional parenthetical hint."""
    m = re.match(r"^(.+?)(?:\s*\((.+)\))?\s*$", example.strip())
    if not m:
        return example.strip(), None
    return m.group(1).strip(), m.group(2)


def _parse_parenthetical(
    hint: str | None, attributes: list[str], type_slug: str, domain: str
) -> dict[str, ValueScalar]:
    if not hint:
        return {}
    out: dict[str, str] = {}
    parts = [p.strip() for p in re.split(r"[,;—–-]\s*(?=[A-Z])|,\s*", hint) if p.strip()]

    for part in parts:
        low = part.lower()
        if re.match(r"^tier\s*\d", low) or re.match(r"^tier\s+[0-3]", low):
            digit = re.search(r"\d", part)
            out["tier"] = int(digit.group()) if digit else 0
        elif "typescript" in low or "nestjs" in low or "java" in low or "go" in low or "rust" in low or "php" in low:
            out["language"] = part.split("/")[0] if "/" in part else part
            if "framework" not in attributes:
                pass
        elif low.startswith("p") and re.search(r"p[0-4]", low):
            out["severity"] = part
        elif "tco2e" in low or "m³" in low or "%" in part:
            out["unit"] = part.strip("()")
        elif low in ("eligible", "aligned", "not aligned", "assessment pending"):
            out["taxonomy_eligible"] = "not" not in low
            out["taxonomy_aligned"] = (
                "aligned" if low == "aligned" else ("not aligned" if "not" in low else "pending")
            )
        elif low.startswith("tier "):
            digit = re.search(r"\d", part)
            out["tier"] = int(digit.group()) if digit else 0
        elif re.match(r"^[a-z]{2}/[a-z]{2}$", low):
            out["country"] = part
        elif "high risk" in low or "low risk" in low:
            out["risk_score"] = "high" if "high" in low else "low"
        elif "current" in low or "outdated" in low or "draft" in low:
            out["status"] = part
        elif re.match(r"^v\d", low):
            out["version"] = part
        elif re.match(r"^\d+\.\d+", part):
            out["nace_code"] = part.split()[0]

    return out


def _expand_name(base: str, index: int, pool_size: int) -> str:
    if index < pool_size:
        return base
    suffixes = ["", " (Brno)", " (FY2024)", " v2", " — updated", f" #{index + 1}"]
    return base + suffixes[index % len(suffixes)]


def build_instance(
    example: str,
    attributes: list[str],
    type_slug: str,
    domain: str,
    index: int,
    pool_size: int,
    rng: Any,
) -> tuple[str, dict[str, ValueScalar]]:
    """Return (display_name, attr_values) for one object instance."""
    raw = remap_text(example, domain)
    primary, hint = _primary_label(raw)
    display = _expand_name(primary, index, pool_size)
    attrs: dict[str, ValueScalar] = _parse_parenthetical(hint, attributes, type_slug, domain)

    name_attr = next((a for a in attributes if a in ("name", "title")), attributes[0] if attributes else "name")
    attrs[name_attr] = display

    for attr in attributes:
        if attr not in attrs:
            attrs[attr] = generate(attr, type_slug, domain, index, display, rng)
        else:
            attrs[attr] = coerce_for_type(attrs[attr], get_data_type(domain, attr))

    return display, attrs
