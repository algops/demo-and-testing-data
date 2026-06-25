"""Publish canonical demo data to demo-data repo root runtime layout."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from .agent_specs import DOMAIN_AGENTS, build_agent_kb_grants, get_agent_slug
from .overview_relationships import publish_overview_relationships_per_project
from .publish_ui import _default_source_setup, _resolve_object_type_ids
from .util import CANONICAL_ROOT, DOMAINS, REPO_ROOT, project_id_for_domain, slugify


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any, dry_run: bool = False) -> None:
    if dry_run:
        print(f"  [dry-run] would write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, dry_run: bool = False) -> None:
    if dry_run:
        print(f"  [dry-run] would write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _domain_filter(items: list[dict], domains: tuple[str, ...], key: str = "domain_id") -> list[dict]:
    return [i for i in items if i.get(key) in domains]


def publish_kb_files(source: Path, target: Path, domains: tuple[str, ...], dry_run: bool) -> int:
    docs = load_json(source / "knowledge-docs.json")["knowledge_docs"]
    kb_root = source / "knowledge-content"
    files_dir = target / "knowledge-base" / "knowledge-files"
    count = 0
    for doc in docs:
        if doc.get("domain_id") not in domains:
            continue
        file_id = doc["id"]
        content_path = kb_root / doc.get("content_path", "").replace("knowledge-content/", "")
        content = ""
        if content_path.is_file():
            content = content_path.read_text(encoding="utf-8")
        write_text(files_dir / f"{file_id}.md", content, dry_run)
        count += 1
    return count


def _slug_filename(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return f"{s}.md" if s else "document.md"


def _patch_tree_titles(nodes: list[dict], title_by_file_id: dict[str, str]) -> None:
    for node in nodes:
        if node.get("type") == "file":
            fid = node.get("fileId")
            if fid and fid in title_by_file_id:
                node["name"] = _slug_filename(title_by_file_id[fid])
        for child in node.get("children") or []:
            _patch_tree_titles([child], title_by_file_id)


def publish_kb_tree(source: Path, target: Path, domains: tuple[str, ...], dry_run: bool) -> None:
    tree_path = target / "knowledge-base" / "tree.json"
    if not tree_path.is_file():
        return
    payload = load_json(tree_path)
    tree = payload.get("tree", [])
    docs = load_json(source / "knowledge-docs.json")["knowledge_docs"]
    title_by_id = {d["id"]: d["title"] for d in docs if d.get("domain_id") in domains}

    def walk(nodes: list[dict]) -> None:
        for node in nodes:
            if node.get("name") in domains and node.get("type") == "folder":
                _patch_tree_titles(node.get("children") or [], title_by_id)
            for child in node.get("children") or []:
                walk([child])

    walk(tree)
    write_json(tree_path, payload, dry_run)


def publish_datasets_runtime(
    source: Path, target: Path, domains: tuple[str, ...], dry_run: bool
) -> int:
    objects = load_json(source / "objects.json")["objects"]
    values = load_json(source / "values.json")["values"]
    datapoints = load_json(source / "datapoints.json")["datapoints"]
    object_types = load_json(source / "object-types.json")["object_types"]

    catalog_path = target / "data-warehouse" / "datasets.json"
    catalog = load_json(catalog_path).get("datasets", [])
    domain_catalog = [e for e in catalog if e.get("domain") in domains]

    dp_by_id = {dp["id"]: dp for dp in datapoints}
    ot_by_id = {ot["id"]: ot for ot in object_types}
    values_by_object: dict[str, dict[str, Any]] = defaultdict(dict)
    for val in values:
        dp = dp_by_id.get(val.get("datapoint_id"))
        if dp:
            values_by_object[val["object_id"]][dp["name"]] = val.get("value", "")

    by_type: dict[str, list[dict]] = defaultdict(list)
    for obj in objects:
        if obj.get("domain_id") in domains:
            by_type[obj["object_type_id"]].append(obj)

    count = 0
    for entry in domain_catalog:
        oid = entry["object_type_id"]
        ot = ot_by_id.get(oid)
        if not ot:
            continue
        type_name = ot["name"]
        rows = []
        for obj in by_type.get(oid, []):
            field_values = values_by_object.get(obj["id"], {})
            rows.append(
                {
                    type_name: obj["name"],
                    "id": obj["id"],
                    "domain_id": obj.get("domain_id"),
                    "data": field_values,
                }
            )
        if not rows:
            continue
        write_json(target / "data-warehouse" / "datasets" / f"{oid}.json", {"data": rows}, dry_run)
        count += 1
    return count


def publish_agents_runtime(source: Path, target: Path, domains: tuple[str, ...], dry_run: bool) -> int:
    agents = load_json(source / "agents.json")["agents"]
    integrations = load_json(source / "integrations.json")["integrations"]
    object_types = load_json(source / "object-types.json")["object_types"]
    list_path = target / "chat-agents" / "agents.json"
    list_payload = load_json(list_path)
    list_by_id = {a["id"]: a for a in list_payload.get("agents", [])}

    tools_by_domain: dict[str, list[str]] = {}
    sources_by_domain: dict[str, list[str]] = {}
    for integ in integrations:
        domain = integ.get("domain_id", "shared")
        role = integ.get("integration_role", "source")
        if role == "tool":
            tools_by_domain.setdefault(domain, []).append(integ["id"])
        elif role == "source":
            sources_by_domain.setdefault(domain, []).append(integ["id"])

    count = 0
    for agent in agents:
        domain = agent.get("domain_id")
        if domain not in domains:
            continue
        file_id = agent["id"]
        agent_slug = agent.get("slug") or slugify(agent["name"])
        agent_spec = next(
            (s for s in DOMAIN_AGENTS.get(domain, []) if get_agent_slug(s) == agent_slug),
            {},
        )
        kb_grants = build_agent_kb_grants(
            domain, agent_slug, agent_spec.get("must_read_sections", [])
        )
        object_type_ids = _resolve_object_type_ids(
            object_types, domain, agent_spec.get("operates_on", [])
        )
        list_item = list_by_id.get(file_id, {})
        detail = {
            "id": file_id,
            "name": agent["name"],
            "description": agent.get("description") or agent.get("primary_use_case_cs", ""),
            "status": agent.get("status", list_item.get("status", "draft")),
            "setup": {
                "accessibility": {
                    "primary": {"type": "web_widget", "enabled": True, "bidirectional": True, "label": "Web widget"},
                    "supervisor": {
                        "type": "slack",
                        "enabled": agent.get("status") == "active",
                        "bidirectional": True,
                        "canSteer": True,
                        "label": f"#agents-{domain}",
                    },
                },
                "knowledge_base_access": {
                    "grants": kb_grants,
                    "skillsPath": f"/knowledgebase/{domain}/agents/{agent_slug}",
                    "skillFilePaths": [],
                },
                "data_warehouse_access": {"objectTypeIds": object_type_ids},
                "realtime_data_access": {
                    "grants": [
                        {"sourceId": sid, "label": "Realtime feed", "streamKey": "events"}
                        for sid in sources_by_domain.get(domain, [])[:2]
                    ],
                },
                "actions_access": {
                    "grants": [
                        {
                            "sourceId": tid,
                            "actionKey": "execute_tool",
                            "label": "Tool action",
                            "description": f"Execute via {tid}",
                            "permission": "execute",
                        }
                        for tid in tools_by_domain.get(domain, [])[:1]
                    ],
                },
            },
        }
        write_json(target / "chat-agents" / "agents" / f"{file_id}.json", detail, dry_run)
        if file_id in list_by_id:
            list_by_id[file_id]["description"] = detail["description"]
            list_by_id[file_id]["status"] = detail["status"]
        count += 1

    list_payload["agents"] = list(list_by_id.values())
    write_json(list_path, list_payload, dry_run)
    return count


def publish_integrations_runtime(
    source: Path, target: Path, domains: tuple[str, ...], dry_run: bool
) -> int:
    integrations = load_json(source / "integrations.json")["integrations"]
    count = 0
    for integration in integrations:
        domain = integration.get("domain_id")
        if domain not in domains:
            continue
        iid = integration["id"]
        name = integration["name"]
        detail_path = target / "integrations" / "integrations" / f"{iid}.json"
        existing = load_json(detail_path) if detail_path.is_file() else {}
        list_entry = {
            "id": iid,
            "name": name,
            "integration_role": integration.get("integration_role", "source"),
            "domain_id": domain,
            "status": integration.get("status", "active"),
            "project_id": project_id_for_domain(domain) or "",
        }
        detail = {
            **list_entry,
            "description": f"{name} — integrace domény {domain}",
            "setup": existing.get("setup") or _default_source_setup(name),
        }
        write_json(detail_path, detail, dry_run)
        count += 1
    return count


def publish_relationships_runtime(
    source: Path, target: Path, domains: tuple[str, ...], dry_run: bool
) -> int:
    counts = publish_overview_relationships_per_project(
        source, target, dry_run=dry_run, domain_filter=domains
    )
    return sum(counts.values())


def publish(target: Path, domains: tuple[str, ...], dry_run: bool = False) -> dict[str, int]:
    source = CANONICAL_ROOT
    print(f"Publishing runtime {domains} from {source} -> {target}")
    stats = {
        "kb_files": publish_kb_files(source, target, domains, dry_run),
        "datasets": publish_datasets_runtime(source, target, domains, dry_run),
        "agents": publish_agents_runtime(source, target, domains, dry_run),
        "integrations": publish_integrations_runtime(source, target, domains, dry_run),
        "relationships": publish_relationships_runtime(source, target, domains, dry_run),
    }
    publish_kb_tree(source, target, domains, dry_run)
    print(f"Published: {stats}")
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish demo data to repo root runtime layout")
    parser.add_argument("--target", type=Path, default=REPO_ROOT, help="Repo root (default: demo-data)")
    parser.add_argument(
        "--domains",
        nargs="+",
        choices=list(DOMAINS),
        default=["it"],
        help="Domains to publish",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.is_dir():
        print(f"Target not found: {target}", file=sys.stderr)
        return 1
    publish(target, tuple(args.domains), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
