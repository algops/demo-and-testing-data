"""Datapoint attribute type registry and value format validation."""

from __future__ import annotations

import re
from typing import Any

from .util import SHARED, BLUEPRINTS_ROOT, load_yaml_simple

ValueScalar = str | int | float | bool

_REGISTRY: dict[str, Any] | None = None

# Attributes that are enums/strings despite containing "score"
_STRING_SCORE_ATTRS = frozenset({"risk_score"})

# Year fields stored as numbers
_YEAR_NUMBER_ATTRS = frozenset(
    {
        "baseline_year",
        "fiscal_year",
        "target_year",
        "assessment_year",
        "phase_in_year",
        "retention_years",
    }
)

# String year/period fields
_STRING_YEAR_ATTRS = frozenset({"reporting_period"})

_BOOLEAN_ATTRS = frozenset(
    {
        "mandatory",
        "mandatory_for_all",
        "subject_to_materiality",
        "quantitative",
        "binding",
        "assured",
        "on_time",
        "critical",
        "material",
        "auto_deploy",
        "auto_policy",
        "approval_required",
        "audit_required",
        "carryover_allowed",
        "conflict_check_complete",
        "contested",
        "electronic_only",
        "extension_possible",
        "sc_criteria_met",
        "sbti_validated",
        "shift_work",
        "stale",
        "taxable",
        "template_available",
        "determines_disclosure",
        "taxonomy_eligible",
    }
)

_STRING_ENUM_ATTRS = frozenset({"taxonomy_aligned"})

_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def _load_registry() -> dict[str, Any]:
    global _REGISTRY
    if _REGISTRY is None:
        path = BLUEPRINTS_ROOT / "attribute_types.yaml"
        _REGISTRY = load_yaml_simple(path) if path.is_file() else {}
    return _REGISTRY


def _lookup_explicit(domain: str, attr: str) -> str | None:
    reg = _load_registry()
    edge_attrs = reg.get("edge_attrs") or {}
    if attr.startswith("rel:") and attr in edge_attrs:
        entry = edge_attrs[attr]
        return entry.get("type") if isinstance(entry, dict) else entry
    for scope in (domain, SHARED, "global"):
        section = reg.get(scope) or {}
        if attr in section:
            entry = section[attr]
            return entry.get("type") if isinstance(entry, dict) else entry
    return None


def infer_data_type(attr: str) -> str:
    """Heuristic data_type when registry has no explicit entry."""
    a = attr.lower()
    bare = a.split(":")[-1] if ":" in a else a

    if bare in _STRING_ENUM_ATTRS:
        return "string"
    if bare in _BOOLEAN_ATTRS:
        return "boolean"
    if "date" in bare or bare.endswith("_at"):
        return "date"
    if bare in _STRING_YEAR_ATTRS:
        return "string"
    if bare in _YEAR_NUMBER_ATTRS or bare.endswith("_year"):
        return "number"
    if bare in _STRING_SCORE_ATTRS:
        return "string"
    if bare in ("benefits_tier", "rate_limit"):
        return "string"
    if (
        bare.endswith("_count")
        or bare.endswith("_czk")
        or bare.endswith("_pct")
        or bare.endswith("_minutes")
        or bare.endswith("_hours")
        or bare.endswith("_days")
        or bare.endswith("_gb")
        or "pct" in bare
        or "ratio" in bare
        or bare.endswith("_score")
        or bare.endswith("_amount")
        or bare in ("fte", "tier", "headcount", "datapoints_count", "lines_of_code", "number")
    ):
        return "number"
    return "string"


def get_data_type(domain: str, attr: str) -> str:
    explicit = _lookup_explicit(domain, attr)
    if explicit:
        return explicit
    return infer_data_type(attr)


def validate_value_for_type(value: Any, data_type: str) -> bool:
    if value is None or value == "":
        return False
    if data_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if data_type == "boolean":
        return isinstance(value, bool)
    if data_type == "date":
        return isinstance(value, str) and bool(_ISO_DATE_RE.match(value))
    return isinstance(value, str)


def coerce_for_type(value: ValueScalar, data_type: str) -> ValueScalar:
    """Normalize a synthesized value to match declared data_type."""
    if data_type == "boolean":
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("yes", "true", "1", "binding", "eligible", "aligned")
        return bool(value)
    if data_type == "number":
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
        if isinstance(value, str):
            try:
                return int(value) if "." not in value else float(value)
            except ValueError:
                return 0
        return 0
    if data_type == "date":
        if isinstance(value, str) and _ISO_DATE_RE.match(value):
            return value
        return "2024-06-01"
    return str(value)
