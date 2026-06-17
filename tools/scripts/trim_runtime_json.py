#!/usr/bin/env python3
"""Strip unused attributes from runtime JSON contract files (UI audit). Idempotent."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

PROJECTS_PATH = ROOT / "projects.json"
AGENTS_LIST_PATH = ROOT / "chat-agents" / "agents.json"
AGENTS_DIR = ROOT / "chat-agents" / "agents"
DATASETS_CATALOG_PATH = ROOT / "data-warehouse" / "datasets.json"
DATASETS_DIR = ROOT / "data-warehouse" / "datasets"
INTEGRATIONS_LIST_PATH = ROOT / "integrations" / "integrations.json"

PROJECT_KEYS_TO_REMOVE = ("org_id", "parent_org_name")
AGENT_LIST_KEYS_TO_REMOVE = (
    "primary_use_case_cs",
    "org_id",
    "slug",
    "created_at",
    "updated_at",
)
AGENT_DETAIL_KEYS_TO_REMOVE = ("domain_id", "org_id")
DATASET_CATALOG_KEYS_TO_REMOVE = ("org_id", "workflow_id", "objects", "min_rows_target")
DATASET_ROW_KEYS_TO_REMOVE = ("object_type_id", "object_type_name", "created_at", "updated_at")
INTEGRATION_LIST_KEYS_TO_REMOVE = ("org_id", "created_at", "updated_at")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def remove_keys(obj: dict[str, Any], keys: tuple[str, ...]) -> int:
    removed = 0
    for key in keys:
        if key in obj:
            del obj[key]
            removed += 1
    return removed


def trim_projects() -> int:
    payload = load_json(PROJECTS_PATH)
    changes = 0
    for project in payload.get("projects", []):
        changes += remove_keys(project, PROJECT_KEYS_TO_REMOVE)
    write_json(PROJECTS_PATH, payload)
    return changes


def trim_agents_list() -> int:
    payload = load_json(AGENTS_LIST_PATH)
    changes = 0
    for agent in payload.get("agents", []):
        changes += remove_keys(agent, AGENT_LIST_KEYS_TO_REMOVE)
    write_json(AGENTS_LIST_PATH, payload)
    return changes


def trim_agent_details() -> int:
    changes = 0
    for path in sorted(AGENTS_DIR.glob("*.json")):
        payload = load_json(path)
        delta = remove_keys(payload, AGENT_DETAIL_KEYS_TO_REMOVE)
        if delta:
            write_json(path, payload)
            changes += delta
    return changes


def trim_datasets_catalog() -> int:
    payload = load_json(DATASETS_CATALOG_PATH)
    changes = 0
    for entry in payload.get("datasets", []):
        changes += remove_keys(entry, DATASET_CATALOG_KEYS_TO_REMOVE)
    write_json(DATASETS_CATALOG_PATH, payload)
    return changes


def trim_dataset_rows() -> int:
    changes = 0
    for path in sorted(DATASETS_DIR.glob("*.json")):
        payload = load_json(path)
        rows = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(rows, list):
            if isinstance(payload, list):
                rows = payload
            else:
                continue
        normalized = {"data": rows}
        if payload != normalized:
            write_json(path, normalized)
            changes += 1
    return changes


def trim_integrations_list() -> int:
    payload = load_json(INTEGRATIONS_LIST_PATH)
    changes = 0
    for entry in payload.get("integrations", []):
        changes += remove_keys(entry, INTEGRATION_LIST_KEYS_TO_REMOVE)
    write_json(INTEGRATIONS_LIST_PATH, payload)
    return changes


def main() -> int:
    print(f"Trimming runtime JSON under {ROOT}")
    print(f"  projects.json: {trim_projects()} keys removed")
    print(f"  chat-agents/agents.json: {trim_agents_list()} keys removed")
    print(f"  chat-agents/agents/*.json: {trim_agent_details()} keys removed")
    print(f"  data-warehouse/datasets.json: {trim_datasets_catalog()} keys removed")
    print(f"  data-warehouse/datasets/*.json: {trim_dataset_rows()} files normalized")
    print(f"  integrations/integrations.json: {trim_integrations_list()} keys removed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
