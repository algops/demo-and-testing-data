"""Split canonical relationships into per-project overview files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .util import DOMAINS, project_id_for_domain

ORG_WIDE_KINDS = frozenset(
    {
        "root_folder",
        "contains_folder",
        "contains_doc",
        "defines_schema",
        "has_instance",
        "instance_of",
        "has_value",
        "value_of",
        "scoped_to",
        "reads",
        "syncs",
        "uses_tool",
    }
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any, dry_run: bool = False) -> None:
    if dry_run:
        print(f"  [dry-run] would write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def is_org_wide(rel: dict[str, Any]) -> bool:
    kind = rel.get("relationship_kind") or ""
    if kind in ORG_WIDE_KINDS:
        return True
    if kind == "related_to":
        meta = rel.get("metadata") or {}
        if isinstance(meta.get("bridge"), str) and not meta.get("domain_edge"):
            return True
    return False


def is_domain_rel(
    rel: dict[str, Any],
    project_id: str,
    domain_id: str,
    entity_domain_by_id: dict[str, str | None],
) -> bool:
    if rel.get("relationship_kind") != "related_to":
        return False
    meta = rel.get("metadata") or {}
    if meta.get("project_id") == project_id:
        return True
    if domain_id and meta.get("domain_id") == domain_id:
        return True
    if meta.get("domain_edge"):
        origin_domain = entity_domain_by_id.get(rel.get("origin_id", ""))
        dest_domain = entity_domain_by_id.get(rel.get("destination_id", ""))
        if origin_domain == domain_id or dest_domain == domain_id:
            return True
        return False
    return False


def _entities_with_domain(data_root: Path) -> dict[str, str | None]:
    domain_by_id: dict[str, str | None] = {}

    def ingest(items: list[dict[str, Any]], key: str = "domain_id") -> None:
        for item in items:
            eid = item.get("id")
            if eid:
                domain_by_id[eid] = item.get(key)

    for name, list_key in (
        ("objects.json", "objects"),
        ("object-types.json", "object_types"),
        ("datapoints.json", "datapoints"),
        ("agents.json", "agents"),
        ("integrations.json", "integrations"),
    ):
        path = data_root / name
        if path.is_file():
            ingest(load_json(path).get(list_key, []))

    return domain_by_id


def filter_edges_for_project(
    relationships: list[dict[str, Any]],
    project_id: str,
    domain_id: str,
    entity_domain_by_id: dict[str, str | None],
) -> list[dict[str, Any]]:
    return [
        rel
        for rel in relationships
        if is_org_wide(rel)
        or is_domain_rel(rel, project_id, domain_id, entity_domain_by_id)
    ]


def publish_overview_relationships_per_project(
    source: Path,
    target: Path,
    dry_run: bool = False,
    domain_filter: tuple[str, ...] | None = None,
) -> dict[str, int]:
    """Write overview/relationships/{projectId}.json for each project."""
    rel_path = source / "relationships.json"
    if not rel_path.is_file():
        print(f"  skip overview relationships: missing {rel_path}")
        return {}

    relationships = load_json(rel_path).get("relationships", [])
    projects_path = target / "projects.json"
    if not projects_path.is_file():
        projects_path = source / "projects.json"
    projects = load_json(projects_path).get("projects", [])

    entity_domain_by_id = _entities_with_domain(source)
    if target != source:
        entity_domain_by_id.update(_entities_with_domain(target))

    out_dir = target / "overview" / "relationships"
    counts: dict[str, int] = {}

    for project in projects:
        domain_id = project.get("domain_id")
        project_id = project.get("id")
        if not project_id or not domain_id:
            continue
        if domain_filter and domain_id not in domain_filter:
            continue

        edges = filter_edges_for_project(
            relationships, project_id, domain_id, entity_domain_by_id
        )
        out_path = out_dir / f"{project_id}.json"
        write_json(out_path, {"relationships": edges}, dry_run)
        counts[project_id] = len(edges)
        print(f"  overview relationships {domain_id}: {len(edges)} edges -> {out_path.name}")

    return counts
