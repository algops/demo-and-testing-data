#!/usr/bin/env python3
"""Annotate demo-data runtime files with project_id aligned to UI projects."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
UI_PROJECTS = ROOT.parent / "ui" / "data" / "projects.json"
LEGACY_OBJECT_TYPES = ROOT / "tools" / "artifacts" / "legacy" / "object-types.json"
LEGACY_DATASETS_DIR = ROOT / "tools" / "artifacts" / "legacy" / "datasets"

DOMAINS = ("esg", "it", "legal", "tax", "hr")
DOMAIN_TO_PROJECT = {domain: f"org:anchor:{domain}" for domain in DOMAINS}
FILE_ID_DOMAIN_RE = re.compile(r"^kb-(esg|it|legal|tax|hr)-")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def project_id_for_domain(domain_id: str | None) -> str | None:
    if not domain_id or domain_id == "shared":
        return None
    return DOMAIN_TO_PROJECT.get(domain_id)


def validate_ui_projects() -> None:
    if not UI_PROJECTS.exists():
        print(f"WARN: UI projects file not found at {UI_PROJECTS}")
        return
    payload = load_json(UI_PROJECTS)
    projects = payload.get("projects", [])
    expected = {DOMAIN_TO_PROJECT[p["domain_id"]] for p in projects if p.get("domain_id") in DOMAINS}
    if expected != set(DOMAIN_TO_PROJECT.values()):
        raise SystemExit(f"UI project IDs mismatch. expected={set(DOMAIN_TO_PROJECT.values())} got={expected}")


def annotate_list_items(path: Path, list_key: str) -> int:
    payload = load_json(path)
    items = payload.get(list_key, [])
    updated = 0
    for item in items:
        domain_id = item.get("domain_id")
        project_id = project_id_for_domain(domain_id)
        if not project_id:
            raise SystemExit(f"Missing mappable domain_id in {path}: {item.get('id')}")
        if item.get("project_id") != project_id:
            item["project_id"] = project_id
            updated += 1
    write_json(path, payload)
    return len(items)


def load_legacy_dataset_by_object_type() -> dict[str, dict[str, Any]]:
    by_object_type: dict[str, dict[str, Any]] = {}
    if not LEGACY_DATASETS_DIR.exists():
        return by_object_type
    for catalog_path in sorted(LEGACY_DATASETS_DIR.glob("*/datasets.json")):
        for entry in load_json(catalog_path).get("datasets", []):
            object_type_id = entry.get("object_type_id")
            if object_type_id:
                by_object_type[object_type_id] = entry
    return by_object_type


def load_object_type_domains() -> dict[str, str]:
    if not LEGACY_OBJECT_TYPES.exists():
        return {}
    domains: dict[str, str] = {}
    for entry in load_json(LEGACY_OBJECT_TYPES).get("object_types", []):
        object_type_id = entry.get("id")
        domain_id = entry.get("domain_id")
        if object_type_id and domain_id:
            domains[object_type_id] = domain_id
    return domains


def derive_domain_from_rows(rows: list[dict[str, Any]]) -> str | None:
    domains = [row.get("domain_id") for row in rows if row.get("domain_id")]
    if not domains:
        return None
    counts = Counter(domains)
    non_shared = {domain: count for domain, count in counts.items() if domain != "shared"}
    if non_shared:
        return max(non_shared, key=non_shared.get)
    return "shared"


def rebuild_datasets_catalog() -> tuple[int, list[str]]:
    catalog_path = ROOT / "datasets" / "datasets.json"
    datasets_dir = ROOT / "datasets" / "datasets"
    current = load_json(catalog_path).get("datasets", [])
    legacy_by_object_type = load_legacy_dataset_by_object_type()
    object_type_domains = load_object_type_domains()

    rebuilt: list[dict[str, Any]] = []
    excluded: list[str] = []

    object_type_ids = sorted(
        {
            entry.get("objectTypeId") or entry.get("object_type_id")
            for entry in current
            if entry.get("objectTypeId") or entry.get("object_type_id")
        }
    )
    if not object_type_ids:
        object_type_ids = sorted(p.stem for p in datasets_dir.glob("*.json"))

    for object_type_id in object_type_ids:
        detail_path = datasets_dir / f"{object_type_id}.json"
        if not detail_path.exists():
            excluded.append(f"{object_type_id} (missing detail file)")
            continue

        detail = load_json(detail_path)
        rows = detail.get("data", []) if isinstance(detail.get("data"), list) else []
        legacy = legacy_by_object_type.get(object_type_id, {})

        domain = (
            derive_domain_from_rows(rows)
            or legacy.get("domain")
            or object_type_domains.get(object_type_id)
        )
        project_id = project_id_for_domain(domain)
        if not project_id:
            excluded.append(f"{object_type_id} (unmapped domain: {domain})")
            continue

        dataset_id = legacy.get("id") or object_type_id
        name = legacy.get("name") or detail.get("object_type_name") or object_type_id
        rebuilt.append(
            {
                "id": dataset_id,
                "name": name,
                "org_id": legacy.get("org_id", "org:anchor"),
                "domain": domain,
                "object_type_id": object_type_id,
                "workflow_id": legacy.get("workflow_id"),
                "objects": legacy.get("objects", []),
                "row_count": len(rows),
                "project_id": project_id,
            }
        )

    write_json(catalog_path, {"datasets": rebuilt})
    return len(rebuilt), excluded


def domain_from_file_id(file_id: str | None) -> str | None:
    if not file_id:
        return None
    match = FILE_ID_DOMAIN_RE.match(file_id)
    return match.group(1) if match else None


def annotate_tree_nodes(nodes: list[dict[str, Any]], domain_context: str | None = None) -> None:
    for node in nodes:
        node_type = node.get("type")
        node_name = node.get("name")

        if node_name in DOMAINS and node_type == "folder":
            domain_context = node_name
            node["project_id"] = DOMAIN_TO_PROJECT[node_name]
        elif domain_context:
            node["project_id"] = DOMAIN_TO_PROJECT[domain_context]

        if node_type == "file":
            file_domain = domain_from_file_id(node.get("fileId")) or domain_context
            if file_domain and file_domain in DOMAIN_TO_PROJECT:
                node["project_id"] = DOMAIN_TO_PROJECT[file_domain]

        children = node.get("children")
        if isinstance(children, list):
            annotate_tree_nodes(children, domain_context)


def annotate_knowledge_tree() -> tuple[int, int]:
    tree_path = ROOT / "knowledge" / "tree.json"
    payload = load_json(tree_path)
    tree = payload.get("tree", [])
    annotate_tree_nodes(tree)
    write_json(tree_path, payload)

    file_nodes = 0
    missing_project = 0

    def walk(nodes: list[dict[str, Any]]) -> None:
        nonlocal file_nodes, missing_project
        for node in nodes:
            if node.get("type") == "file":
                file_nodes += 1
                if not node.get("project_id"):
                    missing_project += 1
            children = node.get("children")
            if isinstance(children, list):
                walk(children)

    walk(tree)
    return file_nodes, missing_project


def validate() -> None:
    agents = load_json(ROOT / "agents" / "agents.json").get("agents", [])
    integrations = load_json(ROOT / "integrations" / "integrations.json").get("integrations", [])
    datasets = load_json(ROOT / "datasets" / "datasets.json").get("datasets", [])

    allowed = set(DOMAIN_TO_PROJECT.values())
    required_dataset_fields = {
        "id",
        "name",
        "org_id",
        "domain",
        "object_type_id",
        "objects",
        "row_count",
        "project_id",
    }

    for agent in agents:
        if agent.get("project_id") not in allowed:
            raise SystemExit(f"Invalid agent project_id: {agent.get('id')}")

    for integration in integrations:
        if integration.get("project_id") not in allowed:
            raise SystemExit(f"Invalid integration project_id: {integration.get('id')}")

    for dataset in datasets:
        missing = required_dataset_fields - set(dataset)
        if missing:
            raise SystemExit(f"Dataset missing fields {missing}: {dataset.get('id')}")
        if dataset.get("project_id") not in allowed:
            raise SystemExit(f"Invalid dataset project_id: {dataset.get('id')}")

    file_nodes, missing_project = annotate_knowledge_tree_validation_only()
    if missing_project:
        raise SystemExit(f"KB tree has {missing_project} file nodes without project_id")

    print("Validation OK")
    print(f"  agents: {len(agents)}")
    print(f"  integrations: {len(integrations)}")
    print(f"  datasets: {len(datasets)}")
    print(f"  kb file nodes: {file_nodes}")


def annotate_knowledge_tree_validation_only() -> tuple[int, int]:
    payload = load_json(ROOT / "knowledge" / "tree.json")
    tree = payload.get("tree", [])
    file_nodes = 0
    missing_project = 0

    def walk(nodes: list[dict[str, Any]]) -> None:
        nonlocal file_nodes, missing_project
        for node in nodes:
            if node.get("type") == "file":
                file_nodes += 1
                if not node.get("project_id"):
                    missing_project += 1
            children = node.get("children")
            if isinstance(children, list):
                walk(children)

    walk(tree)
    return file_nodes, missing_project


def main() -> int:
    validate_ui_projects()

    agents_count = annotate_list_items(ROOT / "agents" / "agents.json", "agents")
    integrations_count = annotate_list_items(
        ROOT / "integrations" / "integrations.json", "integrations"
    )
    datasets_count, excluded = rebuild_datasets_catalog()
    file_nodes, missing_project = annotate_knowledge_tree()

    print(f"Annotated agents: {agents_count}")
    print(f"Annotated integrations: {integrations_count}")
    print(f"Rebuilt datasets catalog: {datasets_count}")
    if excluded:
        print(f"Excluded datasets ({len(excluded)}):")
        for item in excluded:
            print(f"  - {item}")
    print(f"Annotated KB tree file nodes: {file_nodes} (missing project_id: {missing_project})")

    validate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
