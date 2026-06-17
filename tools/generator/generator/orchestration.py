"""Phase 3–4: workflows, activities, factors, datasets."""

from __future__ import annotations

from typing import Any

from .util import BLUEPRINTS_ROOT, DOMAINS, NOW, ORG_ID, load_yaml_simple, make_id, slugify

WORKFLOW_SPECS = [
    ("it_kb_ingest", "it", "IT KB ingest", ["it_service_health"]),
    ("it_code_review", "it", "IT code review", ["it_service_health"]),
    ("it_incident_sync", "it", "IT incident sync", ["it_incident_log"]),
    ("legal_knowhow_index", "legal", "Legal know-how index", ["legal_matter_index", "legal_contract_index"]),
    ("esg_evidence_collect", "esg", "ESG evidence collect", ["esg_metric_facts", "esg_supplier_risk"]),
    ("tax_filing_ops", "tax", "Tax filing ops", ["tax_engagement_status", "tax_client_filings"]),
    ("hr_sop_sync", "hr", "HR SOP sync", ["hr_employee_sop_coverage", "hr_training_compliance"]),
]

DATASET_SPECS = [
    ("it_service_health", "it", "service", 35),
    ("it_incident_log", "it", "incident", 40),
    ("it_dependency_risk", "it", "dependency", 80),
    ("legal_matter_index", "legal", "matter", 50),
    ("legal_contract_index", "legal", "contract", 40),
    ("esg_metric_facts", "esg", "metric", 80),
    ("esg_supplier_risk", "esg", "supplier", 60),
    ("tax_engagement_status", "tax", "engagement", 50),
    ("tax_client_filings", "tax", "legal_entity", 40),
    ("hr_employee_sop_coverage", "hr", "employee", 50),
    ("hr_training_compliance", "hr", "training", 25),
]

_FACTOR_MAP: dict[str, Any] | None = None


def _load_factor_map() -> dict[str, Any]:
    global _FACTOR_MAP
    if _FACTOR_MAP is None:
        path = BLUEPRINTS_ROOT / "factor_datapoint_map.yaml"
        _FACTOR_MAP = load_yaml_simple(path) if path.is_file() else {}
    return _FACTOR_MAP


def _resolve_type_id(domain: str, type_slug: str) -> str:
    if type_slug == "employee" and domain == "hr":
        return make_id("object-type:shared:employee")
    return make_id(f"object-type:{domain}:{slugify(type_slug)}")


def _resolve_datapoint_id(domain: str, type_slug: str, datapoint: str) -> str:
    if type_slug == "employee" and domain == "hr":
        return make_id(f"datapoint:shared:employee:{datapoint}")
    return make_id(f"datapoint:{domain}:{slugify(type_slug)}:{datapoint}")


def derive_workflows() -> list[dict[str, Any]]:
    items = []
    for slug, domain, name, datasets in WORKFLOW_SPECS:
        items.append(
            {
                "id": make_id(f"workflow:{slug}"),
                "slug": slug,
                "name": name,
                "domain_id": domain,
                "owner_org_id": ORG_ID,
                "status": "active",
                "output_datasets": datasets,
                "created_at": NOW,
                "updated_at": NOW,
            }
        )
    return items


def derive_activities(workflows: list[dict], integrations: list[dict]) -> list[dict[str, Any]]:
    items = []
    for wf in workflows:
        domain = wf["domain_id"]
        domain_ints = [i for i in integrations if i["domain_id"] == domain]
        for idx, integ in enumerate(domain_ints[:2]):
            items.append(
                {
                    "id": make_id(f"activity:{wf['slug']}:{idx}"),
                    "name": f"{wf['name']} — krok {idx + 1}",
                    "workflow_id": wf["id"],
                    "workflow_slug": wf["slug"],
                    "step_index": idx,
                    "integration_id": integ["id"],
                    "domain_id": domain,
                    "owner_org_id": ORG_ID,
                    "status": "active",
                    "created_at": NOW,
                }
            )
    return items


def derive_factors(activities: list[dict]) -> list[dict[str, Any]]:
    factor_map = _load_factor_map()
    items = []
    for act in activities:
        wf_slug = act.get("workflow_slug", "")
        step = str(act.get("step_index", 0))
        wf_steps = factor_map.get(wf_slug, {})
        step_cfg = wf_steps.get(step, {})
        domain = act["domain_id"]

        for ftype in ("use-case", "guardrail"):
            cfg = step_cfg.get("guardrail" if ftype == "guardrail" else "use-case", {})
            object_type_id = ""
            datapoint_id = ""
            factor_type = cfg.get("factor_type", "boolean" if ftype == "guardrail" else "frequency")
            operator = cfg.get("operator")
            value = cfg.get("value")

            if cfg.get("object_type") and cfg.get("datapoint"):
                object_type_id = _resolve_type_id(domain, cfg["object_type"])
                datapoint_id = _resolve_datapoint_id(domain, cfg["object_type"], cfg["datapoint"])

            items.append(
                {
                    "id": make_id(f"factor:{act['id']}:{ftype}"),
                    "name": f"{act['name']} — {'použití' if ftype == 'use-case' else 'guardrail'}",
                    "type": ftype,
                    "activity_id": act["id"],
                    "domain_id": domain,
                    "object_type_id": object_type_id,
                    "datapoint_id": datapoint_id,
                    "factor_type": factor_type,
                    "operator": operator,
                    "value": value,
                    "locale": "cs-CZ",
                    "created_at": NOW,
                }
            )
    return items


def derive_datasets(
    state_objects: list[dict],
    object_types: list[dict],
    workflows: list[dict],
) -> dict[str, list[dict[str, Any]]]:
    ot_by_name = {ot["name"]: ot["id"] for ot in object_types}
    by_type: dict[str, list[str]] = {}
    for obj in state_objects:
        ot_id = obj.get("object_type_id")
        by_type.setdefault(ot_id, []).append(obj["id"])

    result: dict[str, list[dict[str, Any]]] = {}
    wf_by_slug = {w["slug"]: w for w in workflows}

    for slug, domain, type_name, min_rows in DATASET_SPECS:
        lookup_name = type_name
        if slug == "hr_employee_sop_coverage":
            lookup_name = "employee"
        ot_id = ot_by_name.get(lookup_name)
        pool = by_type.get(ot_id, []) if ot_id else []
        objs = list(pool)
        if pool and len(objs) < min_rows:
            while len(objs) < min_rows:
                objs.append(pool[len(objs) % len(pool)])
        objs = objs[:max(min_rows, len(pool))]
        wf = next((w for w in workflows if slug in w.get("output_datasets", [])), None)
        record = {
            "id": make_id(f"dataset:{slug}"),
            "name": slug,
            "org_id": ORG_ID,
            "domain": domain,
            "object_type_id": ot_id,
            "workflow_id": wf["id"] if wf else None,
            "objects": objs,
            "row_count": len(objs),
            "min_rows_target": min_rows,
            "generated_at": NOW,
        }
        result.setdefault(domain, []).append(record)
    return result
