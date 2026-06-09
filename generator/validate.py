"""Phase 6: validation gate."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import json

from .agent_specs import DOMAIN_AGENTS, build_agent_kb_grants, get_agent_slug
from .attribute_types import get_data_type, validate_value_for_type
from .audit_values import GENERIC_VALUE_RE, TEMPLATE_DESC_RE, audit_values
from .util import DOMAINS, ROOT

AGENT_CONFIG_KINDS = {"system_prompt", "agent_role", "agent_skill"}

FORBIDDEN = {
    ("object-type", "agent"),
    ("object-type", "value"),
    ("datapoint", "object"),
    ("value", "agent"),
    ("value", "knowledge-doc"),
    ("value", "knowledge-folder"),
    ("knowledge-doc", "knowledge-folder"),
    ("agent", "object-type"),
    ("integration", "agent"),
}

KB_SEMANTIC_KINDS = {"contains_folder", "contains_doc", "root_folder", "scoped_to", "reads", "syncs", "uses_tool"}
DEMO_DISCLAIMER = "Vygenerováno pro demo účely"
MIN_TOKEN_COUNT = 400
GENERIC_NAME_RE = re.compile(r"^\d{4}$")
GENERIC_ORG_RE = re.compile(r"^(Person|Employee) \d{4}$")


def validate(
    relationships: list[dict],
    objects: list[dict],
    object_types: list[dict],
    knowledge_docs: list[dict],
    datasets: dict[str, list[dict]],
    min_docs: dict[str, int],
    values: list[dict] | None = None,
    datapoints: list[dict] | None = None,
    factors: list[dict] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in relationships:
        pair = (rel["origin_type"], rel["destination_type"])
        if pair in FORBIDDEN:
            errors.append(f"Forbidden edge: {pair} kind={rel.get('relationship_kind')}")

    if len([o for o in objects if o.get("name") == "Meridian Pay a.s."]) != 1:
        errors.append("Expected exactly one anchor organization object")

    for o in objects:
        if not o.get("org_id"):
            errors.append(f"Missing org_id on object {o['id']}")
        if not o.get("domain_id"):
            errors.append(f"Missing domain_id on object {o['id']}")
        name = o.get("name", "")
        if GENERIC_NAME_RE.match(name) or GENERIC_ORG_RE.match(name):
            errors.append(f"Generic object name: {name} ({o['id']})")

    if values is not None:
        for v in values:
            if v.get("value") == "demo":
                errors.append(f"Placeholder value on object {v.get('object_id')}")
            val = v.get("value")
            if val is None or val == "":
                errors.append(f"Empty value on object {v.get('object_id')}")
            if isinstance(val, str) and GENERIC_VALUE_RE.match(val):
                errors.append(f"Generic fallback value: {val}")
            if isinstance(val, str) and TEMPLATE_DESC_RE.search(val):
                warnings.append(f"Template description value: {val[:60]}")

    if values is not None and datapoints is not None:
        schema_dps_by_type: dict[str, set[str]] = defaultdict(set)
        for dp in datapoints:
            if not dp["name"].startswith("rel:"):
                schema_dps_by_type[dp["object_type_id"]].add(dp["id"])

        values_by_object: dict[str, set[str]] = defaultdict(set)
        dp_id_to_type: dict[str, str] = {dp["id"]: dp["object_type_id"] for dp in datapoints}
        for v in values:
            dp_id = v.get("datapoint_id")
            if dp_id and dp_id in dp_id_to_type:
                dp_name = next((d["name"] for d in datapoints if d["id"] == dp_id), "")
                if not dp_name.startswith("rel:"):
                    values_by_object[v["object_id"]].add(dp_id)

        dp_by_id = {dp["id"]: dp for dp in datapoints}
        for v in values:
            dp_id = v.get("datapoint_id")
            if not dp_id or dp_id not in dp_by_id:
                continue
            dp = dp_by_id[dp_id]
            data_type = dp.get("data_type") or get_data_type(dp.get("domain_id", ""), dp["name"])
            if not validate_value_for_type(v.get("value"), data_type):
                errors.append(
                    f"Type mismatch on {dp['name']}: expected {data_type}, got {v.get('value')!r}"
                )

        for o in objects:
            ot_id = o.get("object_type_id", "")
            expected = schema_dps_by_type.get(ot_id, set())
            if not expected:
                continue
            actual = values_by_object.get(o["id"], set())
            if actual != expected:
                missing = len(expected - actual)
                if missing:
                    errors.append(
                        f"Incomplete schema values on {o.get('name')}: missing {missing} datapoints"
                    )

    for rel in relationships:
        if rel.get("relationship_kind") != "related_to":
            continue
        meta = rel.get("metadata") or {}
        if meta.get("domain_edge") and not meta.get("edge_values"):
            errors.append(f"Missing edge_values on {meta.get('domain_edge')}")

    domain_edge_counts: dict[str, int] = defaultdict(int)
    for rel in relationships:
        meta = rel.get("metadata") or {}
        if rel.get("relationship_kind") == "related_to" and meta.get("domain_edge"):
            domain_edge_counts[meta.get("domain_id", "unknown")] += 1
    for domain in DOMAINS:
        count = domain_edge_counts.get(domain, 0)
        if count < 4:
            errors.append(f"Domain {domain}: expected domain_edge relationships, found {count}")

    edge_count = len(relationships)
    if edge_count < 2500:
        warnings.append(f"Edge count {edge_count} below target 2500")

    kb_edge_count = sum(1 for r in relationships if r.get("relationship_kind") in KB_SEMANTIC_KINDS)
    if kb_edge_count < 50:
        errors.append(f"Expected KB/agent/integration semantic edges, found {kb_edge_count}")

    expected_agent_docs = sum(len(DOMAIN_AGENTS[d]) for d in DOMAINS) * 3
    agent_config_docs = [d for d in knowledge_docs if d.get("doc_kind") in AGENT_CONFIG_KINDS]
    if len(agent_config_docs) != expected_agent_docs:
        errors.append(
            f"Expected {expected_agent_docs} agent config docs, found {len(agent_config_docs)}"
        )

    for domain, minimum in min_docs.items():
        count = len(
            [
                d
                for d in knowledge_docs
                if d.get("domain_id") == domain and d.get("doc_kind") not in AGENT_CONFIG_KINDS
            ]
        )
        if count < minimum:
            errors.append(f"KB ops docs for {domain}: {count} < {minimum}")

    folders_path = ROOT / "knowledge-folders.json"
    if folders_path.is_file():
        folder_paths = {
            "/" + f["path"] for f in json.loads(folders_path.read_text(encoding="utf-8"))["knowledge_folders"]
        }
        for domain in DOMAINS:
            for spec in DOMAIN_AGENTS[domain]:
                slug = get_agent_slug(spec)
                for grant in build_agent_kb_grants(domain, slug, spec.get("must_read_sections", [])):
                    if grant["treePath"] not in folder_paths:
                        errors.append(f"KB grant path missing from folders: {grant['treePath']}")

    agent_reads = [
        r
        for r in relationships
        if r.get("origin_type") == "agent"
        and r.get("relationship_kind") == "reads"
        and r.get("destination_type") == "knowledge-doc"
    ]
    config_doc_ids = {d["id"] for d in agent_config_docs}
    reads_config = [r for r in agent_reads if r["destination_id"] in config_doc_ids]
    if len(reads_config) < expected_agent_docs:
        errors.append(
            f"Expected agent reads edges to config docs >= {expected_agent_docs}, found {len(reads_config)}"
        )

    for doc in knowledge_docs:
        if doc.get("token_count", 0) < MIN_TOKEN_COUNT:
            warnings.append(f"Low token_count on doc {doc.get('title')}")
        content_path = doc.get("content_path", "")
        if content_path:
            path = ROOT / content_path.replace("knowledge-content/", "knowledge-content/")
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                if DEMO_DISCLAIMER in text:
                    errors.append(f"Demo disclaimer found in {content_path}")

    projects_path = ROOT / "projects.json"
    if projects_path.is_file():
        projects_data = json.loads(projects_path.read_text(encoding="utf-8"))
        projects = projects_data.get("projects", [])
        if len(projects) != 5:
            errors.append(f"Expected 5 projects, found {len(projects)}")
        domain_ids = {p.get("domain_id") for p in projects}
        if domain_ids != set(DOMAINS):
            errors.append(f"Project domain_ids mismatch: {domain_ids}")

    for slug in (
        "it_service_health",
        "it_incident_log",
        "legal_matter_index",
        "esg_metric_facts",
        "tax_engagement_status",
        "hr_employee_sop_coverage",
    ):
        found = any(ds["name"] == slug for domain_ds in datasets.values() for ds in domain_ds)
        if not found:
            errors.append(f"Missing dataset {slug}")

    value_audit: dict[str, Any] = {}
    if values is not None and datapoints is not None:
        value_audit = audit_values(values, datapoints, factors)

    return {
        "passed": len(errors) == 0,
        "errors": errors[:50],
        "error_count": len(errors),
        "warnings": warnings,
        "edge_count": edge_count,
        "kb_edge_count": kb_edge_count,
        "object_count": len(objects),
        "object_type_count": len(object_types),
        "knowledge_doc_count": len(knowledge_docs),
        "value_audit": value_audit,
    }
