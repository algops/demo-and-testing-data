"""Audit datapoint value quality and type conformance."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any

from .attribute_types import get_data_type, validate_value_for_type

GENERIC_VALUE_RE = re.compile(r"^[a-z][a-z0-9_]*_\d+$")
TEMPLATE_DESC_RE = re.compile(r"\(Meridian Pay demo\)")


def audit_values(
    values: list[dict[str, Any]],
    datapoints: list[dict[str, Any]],
    factors: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    dp_by_id = {dp["id"]: dp for dp in datapoints}
    dp_name_by_id = {dp["id"]: dp["name"] for dp in datapoints}

    generic_by_attr: Counter[str] = Counter()
    generic_by_domain: Counter[str] = Counter()
    type_mismatches: list[dict[str, Any]] = []
    template_descriptions: list[dict[str, Any]] = []
    esg_category_leak: list[dict[str, Any]] = []
    factor_gaps: list[str] = []

    for v in values:
        dp_id = v.get("datapoint_id")
        if not dp_id or dp_id not in dp_by_id:
            continue
        dp = dp_by_id[dp_id]
        attr = dp["name"]
        domain = dp.get("domain_id", "unknown")
        val = v.get("value")
        data_type = dp.get("data_type") or get_data_type(domain, attr)

        if isinstance(val, str) and GENERIC_VALUE_RE.match(val):
            generic_by_attr[attr] += 1
            generic_by_domain[domain] += 1

        if isinstance(val, str) and TEMPLATE_DESC_RE.search(val):
            template_descriptions.append({"attr": attr, "value": val[:80]})

        if attr == "category" and domain not in ("esg", "shared") and val in ("E", "S", "G"):
            esg_category_leak.append({"domain": domain, "value": val})

        if not validate_value_for_type(val, data_type):
            type_mismatches.append(
                {
                    "attr": attr,
                    "domain": domain,
                    "expected": data_type,
                    "actual": type(val).__name__,
                    "value": val,
                }
            )

    if factors:
        for f in factors:
            if not f.get("datapoint_id"):
                factor_gaps.append(f.get("name", f.get("id", "unknown")))
            elif f.get("type") == "guardrail" and not f.get("value"):
                factor_gaps.append(f"guardrail missing value: {f.get('name')}")

    return {
        "generic_count": sum(generic_by_attr.values()),
        "generic_by_attr": dict(generic_by_attr.most_common(30)),
        "generic_by_domain": dict(generic_by_domain),
        "type_mismatch_count": len(type_mismatches),
        "type_mismatches": type_mismatches[:30],
        "template_description_count": len(template_descriptions),
        "template_descriptions": template_descriptions[:10],
        "esg_category_leak_count": len(esg_category_leak),
        "factor_gap_count": len(factor_gaps),
        "factor_gaps": factor_gaps[:20],
    }
