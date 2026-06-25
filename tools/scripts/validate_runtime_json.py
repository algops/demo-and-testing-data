#!/usr/bin/env python3
"""Validate runtime JSON contract after trim (standalone; no generation tooling)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

PROJECTS_PATH = ROOT / "projects.json"
AGENTS_LIST_PATH = ROOT / "chat-agents" / "agents.json"
AGENTS_DIR = ROOT / "chat-agents" / "agents"
DATASETS_CATALOG_PATH = ROOT / "data-warehouse" / "datasets.json"
DATASETS_DIR = ROOT / "data-warehouse" / "datasets"
INTEGRATIONS_LIST_PATH = ROOT / "integrations" / "integrations.json"
INTEGRATIONS_DIR = ROOT / "integrations" / "integrations"
KB_TREE_PATH = ROOT / "knowledge-base" / "tree.json"
KB_FILES_DIR = ROOT / "knowledge-base" / "knowledge-files"
RELATIONSHIPS_DIR = ROOT / "overview" / "relationships"

PROJECT_FORBIDDEN = {"org_id", "parent_org_name"}
AGENT_LIST_FORBIDDEN = {"primary_use_case_cs", "org_id", "slug", "created_at", "updated_at"}
AGENT_DETAIL_FORBIDDEN = {"domain_id", "org_id"}
DATASET_CATALOG_FORBIDDEN = {"org_id", "workflow_id", "objects", "min_rows_target"}
DATASET_ROW_FORBIDDEN = {"object_type_id", "object_type_name", "created_at", "updated_at"}
INTEGRATION_LIST_FORBIDDEN = {"org_id", "created_at", "updated_at"}

EXPECTED_COUNTS = {
    "projects": 5,
    "agents": 23,
    "integrations": 27,
    "datasets": 63,
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def check_forbidden_keys(items: list[dict[str, Any]], forbidden: set[str], label: str) -> None:
    for item in items:
        found = forbidden & set(item)
        if found:
            fail(f"{label} still has forbidden keys {sorted(found)} (id={item.get('id')})")


def walk_tree_file_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    for node in nodes:
        if node.get("type") == "file":
            files.append(node)
        for child in node.get("children") or []:
            files.extend(walk_tree_file_nodes([child]))
    return files


def validate_phase1() -> None:
    projects = load_json(PROJECTS_PATH).get("projects", [])
    if len(projects) != EXPECTED_COUNTS["projects"]:
        fail(f"expected {EXPECTED_COUNTS['projects']} projects, got {len(projects)}")
    check_forbidden_keys(projects, PROJECT_FORBIDDEN, "projects.json")
    for project in projects:
        for key in ("id", "name", "domain_id"):
            if key not in project:
                fail(f"projects.json missing required key {key} on {project.get('id')}")

    agents = load_json(AGENTS_LIST_PATH).get("agents", [])
    if len(agents) != EXPECTED_COUNTS["agents"]:
        fail(f"expected {EXPECTED_COUNTS['agents']} agents, got {len(agents)}")
    check_forbidden_keys(agents, AGENT_LIST_FORBIDDEN, "chat-agents/agents.json")
    for agent in agents:
        if "project_id" not in agent:
            fail(f"agent missing project_id: {agent.get('id')}")

    agent_files = list(AGENTS_DIR.glob("*.json"))
    if len(agent_files) != EXPECTED_COUNTS["agents"]:
        fail(f"expected {EXPECTED_COUNTS['agents']} agent detail files, got {len(agent_files)}")
    for path in agent_files:
        detail = load_json(path)
        found = AGENT_DETAIL_FORBIDDEN & set(detail)
        if found:
            fail(f"{path.name} still has forbidden keys {sorted(found)}")
        if "setup" not in detail:
            fail(f"{path.name} missing setup")

    datasets = load_json(DATASETS_CATALOG_PATH).get("datasets", [])
    if len(datasets) != EXPECTED_COUNTS["datasets"]:
        fail(f"expected {EXPECTED_COUNTS['datasets']} datasets, got {len(datasets)}")
    check_forbidden_keys(datasets, DATASET_CATALOG_FORBIDDEN, "data-warehouse/datasets.json")
    for entry in datasets:
        for key in ("id", "name", "project_id", "domain", "object_type_id", "row_count"):
            if key not in entry:
                fail(f"dataset catalog missing {key}: {entry.get('id')}")

    for path in DATASETS_DIR.glob("*.json"):
        payload = load_json(path)
        if set(payload.keys()) != {"data"}:
            fail(f"{path.name} must be exactly {{\"data\": [...]}}, got keys {sorted(payload.keys())}")
        if not isinstance(payload.get("data"), list):
            fail(f"{path.name} data must be a list")

    integrations = load_json(INTEGRATIONS_LIST_PATH).get("integrations", [])
    if len(integrations) != EXPECTED_COUNTS["integrations"]:
        fail(f"expected {EXPECTED_COUNTS['integrations']} integrations, got {len(integrations)}")
    check_forbidden_keys(integrations, INTEGRATION_LIST_FORBIDDEN, "integrations/integrations.json")


def validate_phase2_optional() -> None:
    """Soft checks for linkage fixes when present."""
    if KB_TREE_PATH.exists():
        tree_payload = load_json(KB_TREE_PATH)
        tree = tree_payload.get("tree", tree_payload if isinstance(tree_payload, list) else [])
        file_nodes = walk_tree_file_nodes(tree if isinstance(tree, list) else [])
        for node in file_nodes:
            file_id = node.get("fileId")
            if not file_id:
                fail(f"KB tree file node missing fileId: {node.get('id')}")
            md_path = KB_FILES_DIR / f"{file_id}.md"
            if not md_path.exists():
                fail(f"KB fileId {file_id} has no markdown at {md_path}")

    if RELATIONSHIPS_DIR.exists():
        project_files = sorted(RELATIONSHIPS_DIR.glob("*.json"))
        if not project_files:
            fail("overview/relationships/ has no per-project JSON files")
        for path in project_files:
            rels = load_json(path).get("relationships", [])
            with_project = sum(
                1 for r in rels if (r.get("metadata") or {}).get("project_id")
            )
            domain_edges = sum(
                1
                for r in rels
                if r.get("relationship_kind") == "related_to"
                and (r.get("metadata") or {}).get("domain_edge")
            )
            if rels and domain_edges > 0 and with_project == 0:
                fail(f"{path.name} has domain edges but no metadata.project_id annotations")

    if INTEGRATIONS_LIST_PATH.exists() and INTEGRATIONS_DIR.exists():
        ids = {i["id"] for i in load_json(INTEGRATIONS_LIST_PATH).get("integrations", [])}
        detail_ids = {
            p.stem for p in INTEGRATIONS_DIR.glob("*.json") if p.name != "sources.json"
        }
        missing = ids - detail_ids
        if missing:
            fail(f"missing integration detail files: {sorted(missing)}")


def main() -> int:
    validate_phase1()
    validate_phase2_optional()
    print("Validation OK")
    print(f"  projects: {EXPECTED_COUNTS['projects']}")
    print(f"  agents: {EXPECTED_COUNTS['agents']}")
    print(f"  integrations: {EXPECTED_COUNTS['integrations']}")
    print(f"  datasets: {EXPECTED_COUNTS['datasets']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
