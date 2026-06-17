"""Materialize domain relationship edge attributes as value records."""

from __future__ import annotations

import random
from typing import Any, TYPE_CHECKING

from ..attribute_types import ValueScalar, coerce_for_type, get_data_type
from ..util import make_id

if TYPE_CHECKING:
    from ..graph import GraphState


def _edge_attr_type(attr: str, edge_type: str) -> str:
    return get_data_type("shared", f"rel:{edge_type}:{attr}")


EDGE_ATTR_GENERATORS: dict[str, Any] = {
    "mandatory": lambda rng: True if rng.random() > 0.3 else False,
    "phase_in_year": lambda rng: rng.randint(2024, 2026),
    "datapoint_id": lambda rng: f"DP-{rng.randint(100, 999)}",
    "quantitative": lambda rng: rng.random() > 0.4,
    "reference_type": lambda rng: rng.choice(["implements", "references", "supersedes"]),
    "binding": lambda rng: rng.choice(["binding", "voluntary"]),
    "calculation_method": lambda rng: rng.choice(["GHG Protocol", "market-based", "location-based", "activity-based"]),
    "coverage_pct": lambda rng: rng.randint(60, 98),
    "quality_assessment": lambda rng: rng.choice(["A", "B", "C"]),
    "coverage_level": lambda rng: rng.choice(["full", "partial", "minimal"]),
    "residual_risk_level": lambda rng: rng.choice(["low", "medium", "high"]),
    "control_type": lambda rng: rng.choice(["preventive", "detective", "corrective"]),
    "eligibility_status": lambda rng: rng.choice(["eligible", "not_eligible", "pending"]),
    "assessment_year": lambda rng: rng.randint(2023, 2025),
    "assessment_date": lambda rng: f"2024-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}",
    "score": lambda rng: rng.randint(1, 100),
    "method": lambda rng: rng.choice(["EcoVadis", "custom questionnaire", "SASB", "internal"]),
    "value": lambda rng: rng.randint(100, 50000),
    "period": lambda rng: rng.choice(["FY2024", "FY2023", "Q1 2024", "Q4 2024"]),
    "assured": lambda rng: rng.random() > 0.5,
    "page_reference": lambda rng: rng.randint(12, 180),
    "responsibility_type": lambda rng: rng.choice(["owner", "reviewer", "contributor"]),
    "data_quality_score": lambda rng: rng.randint(60, 95),
    "measurement_method": lambda rng: rng.choice(["direct", "estimated", "proxy"]),
    "finding_type": lambda rng: rng.choice(["observation", "deficiency", "non-compliance"]),
    "determines_disclosure": lambda rng: rng.random() > 0.35,
    "supply_category": lambda rng: rng.choice(["Tier 1", "Tier 2", "Tier 3"]),
    "criticality": lambda rng: rng.choice(["critical", "important", "standard"]),
    "relationship": lambda rng: rng.choice(["subordinate", "amends", "supplements"]),
    "impact_level": lambda rng: rng.choice(["low", "medium", "high", "critical"]),
    "downtime_minutes": lambda rng: rng.randint(0, 120),
    "dependency_type": lambda rng: rng.choice(["runtime", "build", "data"]),
    "version_constraint": lambda rng: rng.choice([">=1.0", "<2.0", "^4.18"]),
    "sla_target": lambda rng: rng.randint(95, 99),
    "on_time": lambda rng: rng.random() > 0.15,
    "filed_date": lambda rng: f"2024-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}",
    "actual_deadline_date": lambda rng: f"2024-{rng.randint(3,12):02d}-31",
    "stage_count": lambda rng: rng.randint(1, 5),
    "within_days_of_start": lambda rng: rng.randint(1, 90),
    "rate_pct": lambda rng: rng.randint(10, 99),
    "rate_limit": lambda rng: rng.choice(["100/min", "500/min", "1000/min", "unlimited"]),
    "fallback_strategy": lambda rng: rng.choice(["retry", "circuit-breaker", "failover", "cache"]),
    "strategy": lambda rng: rng.choice(["rolling", "blue-green", "canary", "recreate"]),
    "treaty_rate": lambda rng: rng.choice(["0%", "5%", "10%", "15%", "withholding"]),
}


def _generate_edge_attr(attr: str, edge_type: str, domain: str, rng: random.Random) -> ValueScalar:
    data_type = _edge_attr_type(attr, edge_type)
    gen = EDGE_ATTR_GENERATORS.get(attr)
    if gen:
        return coerce_for_type(gen(rng), data_type)
    if "date" in attr:
        return coerce_for_type(f"2024-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}", "date")
    if "pct" in attr or attr.endswith("_rate_pct") or attr.endswith("_count") or attr.endswith("_minutes"):
        return coerce_for_type(rng.randint(10, 99), "number")
    if attr in ("mandatory", "on_time", "assured", "determines_disclosure", "quantitative"):
        return coerce_for_type(rng.random() > 0.3, "boolean")
    return coerce_for_type(rng.choice(["low", "medium", "high"]), data_type)


def _type_key_from_oid(state: GraphState, oid: str) -> str | None:
    for tk, oids in state.objects_by_type.items():
        if oid in oids:
            return tk
    return None


def _ensure_edge_datapoint(
    state: GraphState,
    type_key: str,
    edge_type: str,
    attr: str,
    domain: str,
) -> str:
    dp_name = f"rel:{edge_type}:{attr}"
    dp_key = f"{type_key}:{dp_name}"
    if dp_key not in state.datapoint_ids:
        parts = type_key.split(":", 1)
        type_slug = parts[1] if len(parts) > 1 else type_key
        dom = parts[0]
        dp_id = make_id(f"datapoint:{dom}:{type_slug}:{dp_name}")
        state.datapoint_ids[dp_key] = dp_id
        ot_id = state.object_type_ids.get(type_key, "")
        if ot_id:
            state.add_rel("object-type", ot_id, "datapoint", dp_id, "defines_schema")
    return state.datapoint_ids[dp_key]


def _attach_value(
    state: GraphState,
    oid: str,
    dp_id: str,
    payload: ValueScalar,
    seed: str,
) -> None:
    val_id = make_id(f"value:{seed}")
    state.value_ids.append(val_id)
    state.value_payloads[val_id] = payload
    state.value_meta[val_id] = {"object_id": oid, "datapoint_id": dp_id}
    state.add_rel("object", oid, "value", val_id, "has_value")
    state.add_rel("datapoint", dp_id, "value", val_id, "value_of")


def materialize_edge_values(
    state: GraphState,
    origin_oid: str,
    rel_spec: dict[str, Any],
    domain: str,
    edge_index: int,
) -> dict[str, ValueScalar]:
    """Create edge_values dict and materialize as value records on origin object."""
    edge_type = rel_spec["type"]
    attrs = rel_spec.get("attributes", [])
    edge_values: dict[str, ValueScalar] = {}
    type_key = _type_key_from_oid(state, origin_oid)
    if not type_key:
        return edge_values

    for attr in attrs:
        payload = _generate_edge_attr(attr, edge_type, domain, state.rng)
        edge_values[attr] = payload
        dp_id = _ensure_edge_datapoint(state, type_key, edge_type, attr, domain)
        seed = f"edge:{domain}:{edge_type}:{origin_oid}:{attr}:{edge_index}"
        _attach_value(state, origin_oid, dp_id, payload, seed)

    return edge_values
