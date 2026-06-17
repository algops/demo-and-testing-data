#!/usr/bin/env python3
"""Generate all demo data artifacts from anchor tenant blueprints."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .catalogues import write_all_catalogues
from .derive import (
    derive_agents,
    derive_datapoints,
    derive_integrations,
    derive_knowledge_docs,
    derive_knowledge_folders,
    derive_object_types,
    derive_objects,
    derive_projects,
    derive_values,
)
from .domain_merge import merge_domain_slice
from .graph import build_relationship_graph
from .kb_content import write_kb_content
from .orchestration import (
    derive_activities,
    derive_datasets,
    derive_factors,
    derive_workflows,
)
from .util import BLUEPRINTS_ROOT, CANONICAL_ROOT, DOMAINS, NOW, checksum, load_yaml_simple
from .validate import validate


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _run_generation(domains: tuple[str, ...] | None) -> int:
    anchor = load_yaml_simple(BLUEPRINTS_ROOT / "anchor.yaml")
    min_docs = anchor.get("knowledge_base", {}).get("min_docs_per_domain", {})
    if isinstance(min_docs, dict):
        min_docs = {k: int(v) for k, v in min_docs.items()}

    active = domains or DOMAINS
    CANONICAL_ROOT.mkdir(parents=True, exist_ok=True)

    print("Phase 0: catalogues...")
    write_all_catalogues(min_docs, domains=active)

    print(f"Phase 1: relationships (domains={','.join(active)})...")
    state = build_relationship_graph(min_docs, domains=active)
    relationships = state.relationships
    write_json(CANONICAL_ROOT / "relationships.json", {"relationships": relationships})

    print("Phase 2: entities...")
    object_types = derive_object_types(state)
    datapoints = derive_datapoints(state)
    objects = derive_objects(state)
    values = derive_values(state)
    integrations = derive_integrations(state)
    agents = derive_agents(state)
    kb_folders = derive_knowledge_folders(state)
    kb_docs = derive_knowledge_docs(state)

    write_json(CANONICAL_ROOT / "object-types.json", {"object_types": object_types})
    write_json(CANONICAL_ROOT / "datapoints.json", {"datapoints": datapoints})
    write_json(CANONICAL_ROOT / "objects.json", {"objects": objects})
    write_json(CANONICAL_ROOT / "values.json", {"values": values})
    write_json(CANONICAL_ROOT / "integrations.json", {"integrations": integrations})
    write_json(CANONICAL_ROOT / "agents.json", {"agents": agents})
    write_json(CANONICAL_ROOT / "knowledge-folders.json", {"knowledge_folders": kb_folders})
    write_json(CANONICAL_ROOT / "knowledge-docs.json", {"knowledge_docs": kb_docs})
    write_json(CANONICAL_ROOT / "projects.json", derive_projects())

    print("Phase 2b: KB content...")
    write_kb_content(state, kb_docs)

    print("Phase 3–4: orchestration & warehouse...")
    workflows = derive_workflows()
    if domains:
        workflows = [w for w in workflows if w.get("domain_id") in active]
    activities = derive_activities(workflows, integrations)
    factors = derive_factors(activities)
    datasets = derive_datasets(objects, object_types, workflows)

    write_json(CANONICAL_ROOT / "workflows.json", {"workflows": workflows})
    write_json(CANONICAL_ROOT / "activities.json", {"activities": activities})
    write_json(CANONICAL_ROOT / "factors.json", {"factors": factors})

    for domain, records in datasets.items():
        write_json(CANONICAL_ROOT / "datasets" / domain / "datasets.json", {"datasets": records})

    if domains:
        print(f"Merging domain slice into canonical ({','.join(domains)})...")
        merge_domain_slice(domains)
        relationships = json.loads((CANONICAL_ROOT / "relationships.json").read_text())["relationships"]
        objects = json.loads((CANONICAL_ROOT / "objects.json").read_text())["objects"]
        object_types = json.loads((CANONICAL_ROOT / "object-types.json").read_text())["object_types"]
        kb_docs = json.loads((CANONICAL_ROOT / "knowledge-docs.json").read_text())["knowledge_docs"]
        values = json.loads((CANONICAL_ROOT / "values.json").read_text())["values"]
        datapoints = json.loads((CANONICAL_ROOT / "datapoints.json").read_text())["datapoints"]
        factors = json.loads((CANONICAL_ROOT / "factors.json").read_text())["factors"]

    print("Phase 6: validation...")
    report = validate(
        relationships, objects, object_types, kb_docs, datasets, min_docs, values, datapoints, factors
    )
    write_json(CANONICAL_ROOT / "validation_report.json", report)

    manifest = {
        "generated_at": NOW,
        "anchor_org": "org:anchor",
        "enabled_domains": list(active),
        "checksums": {
            "relationships": checksum(relationships),
            "objects": checksum(objects),
            "object_types": checksum(object_types),
        },
        "counts": {
            "relationships": len(relationships),
            "objects": len(objects),
            "object_types": len(object_types),
            "datapoints": len(datapoints),
            "values": len(values),
            "knowledge_docs": len(kb_docs),
            "workflows": len(workflows),
        },
    }
    write_json(CANONICAL_ROOT / "generation_manifest.json", manifest)

    print(f"Done. edges={len(relationships)} objects={len(objects)} docs={len(kb_docs)}")
    if not report["passed"]:
        print("VALIDATION ERRORS:", report["errors"], file=sys.stderr)
        return 1
    if report["warnings"]:
        print("Warnings:", report["warnings"])
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate demo data artifacts")
    parser.add_argument(
        "--domains",
        nargs="+",
        choices=list(DOMAINS),
        help="Regenerate only these domains and merge with legacy canonical",
    )
    args = parser.parse_args()
    domains = tuple(args.domains) if args.domains else None
    return _run_generation(domains)


if __name__ == "__main__":
    sys.exit(main())
