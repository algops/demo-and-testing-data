"""Publish canonical demo data to UI legacy layout (ui/data submodule)."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from .util import NOW, ROOT

ANCHOR_ORG_NAME = "Meridian Pay a.s."
ANCHOR_ORG_ID = "org:anchor"

INTEGRATION_URLS: dict[str, str] = {
    "gitlab": "https://gitlab.meridianpay.cz/api/v4",
    "confluence": "https://confluence.meridianpay.cz/rest/api",
    "slack": "https://slack.com/api",
    "datadog": "https://api.datadoghq.eu/api/v1",
    "sphera": "https://api.sphera.com/v1/esg",
    "pohoda": "https://api.pohoda.cz/v1",
    "epo": "https://adisrws.mfcr.cz/epo",
    "imanage": "https://imanage.meridianpay.cz/api",
    "sharepoint": "https://meridianpay.sharepoint.com/_api",
    "sap": "https://api.successfactors.eu/odata/v2",
    "recruitee": "https://api.recruitee.com/c",
}

DOMAIN_OBJECT_TYPE = {
    "esg": "metric",
    "it": "service",
    "legal": "matter",
    "tax": "engagement",
    "hr": "employee",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any, dry_run: bool) -> None:
    if dry_run:
        print(f"  [dry-run] would write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def publish_object_types(
    source: Path, target: Path, dry_run: bool
) -> tuple[list[dict], dict[str, str]]:
    object_types = load_json(source / "object-types.json")["object_types"]
    objects = load_json(source / "objects.json")["objects"]
    datapoints = load_json(source / "datapoints.json")["datapoints"]
    values = load_json(source / "values.json")["values"]

    obj_count: dict[str, int] = defaultdict(int)
    for obj in objects:
        obj_count[obj["object_type_id"]] += 1

    schema_dp_ids_by_type: dict[str, set[str]] = defaultdict(set)
    for dp in datapoints:
        if not dp["name"].startswith("rel:"):
            schema_dp_ids_by_type[dp["object_type_id"]].add(dp["id"])

    values_by_object: dict[str, set[str]] = defaultdict(set)
    for val in values:
        values_by_object[val["object_id"]].add(val.get("datapoint_id", ""))

    name_by_id = {ot["id"]: ot["name"] for ot in object_types}
    enriched = []
    for ot in object_types:
        oid = ot["id"]
        count = obj_count.get(oid, 0)
        schema_dps = schema_dp_ids_by_type.get(oid, set())
        dps = len(schema_dps)
        complete = 0
        for obj in objects:
            if obj["object_type_id"] != oid:
                continue
            filled = values_by_object.get(obj["id"], set()) & schema_dps
            if schema_dps and filled == schema_dps:
                complete += 1
        incomplete = max(0, count - complete)
        success_rate = (complete / count) if count else 0.0
        enriched.append(
            {
                **ot,
                "object_count": count,
                "datapoint_count": dps,
                "value_count": sum(
                    1
                    for obj in objects
                    if obj["object_type_id"] == oid
                    for _ in values_by_object.get(obj["id"], set())
                ),
                "coverage_total_objects": count,
                "coverage_complete_objects": complete,
                "coverage_incomplete_objects": incomplete,
                "coverage_success_rate": round(success_rate, 4),
                "latest_value_updated_at": ot.get("updated_at", NOW),
            }
        )
        meta_path = target / "object-types" / f"{oid}.json"
        write_json(meta_path, {**ot, "object_count": count, "datapoint_count": dps}, dry_run)

    write_json(target / "object-types" / "object-types.json", {"object_types": enriched}, dry_run)
    write_json(target / "object-types.json", {"object_types": enriched}, dry_run)
    return enriched, name_by_id


def publish_datasets(
    source: Path,
    target: Path,
    object_types: list[dict],
    name_by_id: dict[str, str],
    dry_run: bool,
) -> None:
    objects = load_json(source / "objects.json")["objects"]
    values = load_json(source / "values.json")["values"]
    datapoints = load_json(source / "datapoints.json")["datapoints"]

    dp_by_id = {dp["id"]: dp for dp in datapoints}
    values_by_object: dict[str, dict[str, Any]] = defaultdict(dict)
    for val in values:
        dp = dp_by_id.get(val.get("datapoint_id"))
        if dp:
            values_by_object[val["object_id"]][dp["name"]] = val.get("value", "")

    by_type: dict[str, list[dict]] = defaultdict(list)
    for obj in objects:
        by_type[obj["object_type_id"]].append(obj)

    datasets_dir = target / "datasets"
    if not dry_run:
        datasets_dir.mkdir(parents=True, exist_ok=True)

    for ot in object_types:
        oid = ot["id"]
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
        payload = {
            "object_type_id": oid,
            "object_type_name": type_name,
            "created_at": ot.get("created_at", NOW),
            "updated_at": ot.get("updated_at", NOW),
            "data": rows,
        }
        write_json(datasets_dir / f"{oid}.json", payload, dry_run)


def publish_workflows_and_activities(source: Path, target: Path, dry_run: bool) -> None:
    workflows = load_json(source / "workflows.json")["workflows"]
    activities = load_json(source / "activities.json")["activities"]

    acts_by_wf: dict[str, list[dict]] = defaultdict(list)
    for act in activities:
        acts_by_wf[act["workflow_id"]].append(act)

    ui_workflows = []
    for i, wf in enumerate(workflows):
        wf_acts = acts_by_wf.get(wf["id"], [])
        ui_wf = {
            **wf,
            "description": wf.get("description") or f"Workflow {wf.get('slug', wf['name'])} pro doménu {wf.get('domain_id', '')}",
            "verification_status": True,
            "owner_org_name": ANCHOR_ORG_NAME,
            "last_used_at": wf.get("updated_at", NOW),
            "total_executions": 20 + i * 5,
            "successful_executions": 18 + i * 4,
            "failed_executions": 2 + i,
            "success_rate": round(0.85 + (i % 3) * 0.04, 3),
            "activities_count": len(wf_acts),
            "phases_count": max(1, len(wf_acts)),
            "average_duration": 120.5 + i * 30,
        }
        ui_workflows.append(ui_wf)

        setup_data: dict[str, Any] = {}
        prev_key: str | None = None
        for j, act in enumerate(wf_acts):
            key = re.sub(r"[^a-z0-9_]+", "_", act["name"].lower())[:40] or f"step_{j}"
            entry: dict[str, Any] = {
                "id": act["id"],
                "type": "activity",
                "setup": {"config": {"phase": j + 1, "domain_id": act.get("domain_id")}},
                "destination": {},
            }
            if prev_key:
                setup_data[prev_key]["destination"] = {"activity": {"id": [act["id"]]}}
            setup_data[key] = entry
            prev_key = key

        detail = {
            **ui_wf,
            "setup": {"data": setup_data},
        }
        write_json(target / "workflows" / f"{wf['id']}.json", detail, dry_run)

    write_json(target / "workflows" / "workflows.json", {"workflows": ui_workflows}, dry_run)

    ui_activities = []
    for i, act in enumerate(activities):
        wf = next((w for w in workflows if w["id"] == act["workflow_id"]), None)
        domain = act.get("domain_id", "")
        obj_type = DOMAIN_OBJECT_TYPE.get(domain, "organization")
        ui_act = {
            **act,
            "description": act.get("description") or f"Aktivita workflow {wf['name'] if wf else ''}",
            "type": "source" if i % 2 == 0 else "enrich",
            "object_type": obj_type,
            "verification_status": True,
            "owner_org_name": ANCHOR_ORG_NAME,
            "updated_at": act.get("created_at", NOW),
            "last_used_at": act.get("created_at", NOW),
            "total_requests": 100 + i * 37,
            "successful_requests": 90 + i * 33,
            "failed_requests": 10 + i * 4,
            "success_rate": round(0.88 + (i % 4) * 0.02, 4),
            "workflows_count": 1,
            "average_duration": 35.0 + i * 5,
            "sources_count": 1,
            "factors_count": 2,
        }
        ui_activities.append(ui_act)

        act_detail = {
            "id": act["id"],
            "name": act["name"],
            "description": ui_act["description"],
            "type": ui_act["type"],
            "object_type": obj_type,
            "status": act.get("status", "active"),
            "verification_status": True,
            "setup": {
                "data": {
                    "integration_step": {
                        "id": act.get("integration_id"),
                        "type": "source",
                        "destination": {},
                    }
                }
            },
            "runtime_stats": {
                "total_requests": ui_act["total_requests"],
                "successful_requests": ui_act["successful_requests"],
                "failed_requests": ui_act["failed_requests"],
                "success_rate": ui_act["success_rate"],
                "average_duration": ui_act["average_duration"],
                "last_used_at": ui_act["last_used_at"],
            },
            "metadata": {
                "owner_org_id": act.get("owner_org_id", "org:anchor"),
                "owner_org_name": ANCHOR_ORG_NAME,
                "created_at": act.get("created_at", NOW),
                "updated_at": ui_act["updated_at"],
                "workflows": (
                    [{"id": wf["id"], "name": wf["name"]}] if wf else []
                ),
            },
        }
        write_json(target / "activities" / f"{act['id']}.json", act_detail, dry_run)

    write_json(target / "activities" / "activities.json", {"activities": ui_activities}, dry_run)


def publish_factors(
    source: Path,
    target: Path,
    object_types: list[dict],
    dry_run: bool,
) -> None:
    factors = load_json(source / "factors.json")["factors"]
    datapoints = load_json(source / "datapoints.json")["datapoints"]

    type_by_domain = {}
    dp_by_domain: dict[str, str] = {}
    for ot in object_types:
        domain = ot.get("domain_id")
        if domain and domain not in type_by_domain:
            type_by_domain[domain] = ot["id"]
    for dp in datapoints:
        domain = dp.get("domain_id")
        if domain and domain not in dp_by_domain:
            dp_by_domain[domain] = dp["id"]

    ui_factors = []
    for f in factors:
        domain = f.get("domain_id", "shared")
        ui_factors.append(
            {
                "id": f["id"],
                "name": f["name"],
                "description": f.get("description") or f["name"],
                "type": f["type"],
                "factor_type": f.get("factor_type") or ("boolean" if f["type"] == "guardrail" else "frequency"),
                "object_type_id": f.get("object_type_id") or type_by_domain.get(domain) or object_types[0]["id"],
                "datapoint_id": f.get("datapoint_id") or dp_by_domain.get(domain) or datapoints[0]["id"],
                "operator": f.get("operator") if f.get("operator") is not None else ("regex" if f["type"] == "guardrail" else None),
                "value": f.get("value"),
                "setup": {},
                "created_at": f.get("created_at", NOW),
                "updated_at": f.get("created_at", NOW),
                "deleted_at": None,
                "stackable": False,
                "activity_id": f.get("activity_id"),
                "domain_id": domain,
                "locale": f.get("locale", "cs-CZ"),
            }
        )
    write_json(target / "factors.json", {"factors": ui_factors}, dry_run)


def _folder_children(folders: list[dict], parent_path: str) -> list[dict]:
    prefix = parent_path + "/"
    depth = parent_path.count("/")
    return sorted(
        [f for f in folders if f["path"].startswith(prefix) and f["path"].count("/") == depth + 1],
        key=lambda x: x["name"],
    )


def _doc_parent_folder(doc: dict) -> str:
    cp = doc.get("content_path", "").replace("knowledge-content/", "")
    parts = Path(cp).parts
    if "doc" in parts:
        idx = parts.index("doc")
        return "/".join(parts[:idx])
    return "/".join(parts[:-1]) if len(parts) > 1 else "knowledgebase"


def _docs_in_folder(docs: list[dict], folder_path: str) -> list[dict]:
    if folder_path == "knowledgebase":
        return []
    return [d for d in docs if _doc_parent_folder(d) == folder_path]


def _build_folder_node(
    folder: dict,
    folders: list[dict],
    docs: list[dict],
    doc_file_ids: dict[str, str],
) -> dict:
    path = folder["path"]
    children: list[dict] = []
    for child_folder in _folder_children(folders, path):
        children.append(_build_folder_node(child_folder, folders, docs, doc_file_ids))
    for doc in _docs_in_folder(docs, path):
        file_id = doc_file_ids[doc["id"]]
        filename = doc["title"][:60].replace(" ", "-").lower() + ".md"
        children.append(
            {
                "id": f"file-{doc['id'][:8]}",
                "name": filename,
                "type": "file",
                "fileId": file_id,
            }
        )
    return {
        "id": f"folder-{folder['id'][:8]}",
        "name": folder["name"],
        "type": "folder",
        "children": children,
    }


def publish_knowledge_base(source: Path, target: Path, dry_run: bool) -> None:
    folders = load_json(source / "knowledge-folders.json")["knowledge_folders"]
    docs = load_json(source / "knowledge-docs.json")["knowledge_docs"]

    doc_file_ids: dict[str, str] = {}
    for i, doc in enumerate(docs):
        domain = doc.get("domain_id", "shared")
        doc_file_ids[doc["id"]] = f"kb-{domain}-{i + 1:03d}"

    roots = [f for f in folders if f["path"] == "knowledgebase"]
    tree = []
    for root in roots:
        tree.append(_build_folder_node(root, folders, docs, doc_file_ids))

    write_json(target / "knowledge-base" / "tree.json", {"tree": tree}, dry_run)

    files_dir = target / "knowledge-base" / "files"
    if not dry_run:
        files_dir.mkdir(parents=True, exist_ok=True)

    for doc in docs:
        file_id = doc_file_ids[doc["id"]]
        content_path = source / doc.get("content_path", "")
        content = ""
        if content_path.is_file():
            content = content_path.read_text(encoding="utf-8")
        else:
            alt = source / "knowledge-content" / doc.get("content_path", "").replace("knowledge-content/", "")
            if alt.is_file():
                content = alt.read_text(encoding="utf-8")
            else:
                content = f"# {doc['title']}\n\n(Dokument vygenerován pro demo.)\n"

        payload = {
            "id": file_id,
            "title": doc["title"],
            "versions": [
                {
                    "id": "v1",
                    "label": "Published",
                    "createdAt": doc.get("created_at", NOW),
                    "content": content,
                }
            ],
        }
        write_json(files_dir / f"{file_id}.json", payload, dry_run)


def _integration_url(name: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "", name.lower())
    for pattern, url in INTEGRATION_URLS.items():
        if pattern in key:
            return url
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"https://api.meridianpay.cz/integrations/{slug}"


def _default_source_setup(name: str, delivery_type: str = "Endpoint") -> dict[str, Any]:
    return {
        "customization_permissions": {"factor_creation": "creator_only"},
        "load_balancing": {"concurrency": 10, "timeout": 30},
        "processing_options": {"input_processing": "ignore"},
        "run_request": {
            "mappings": {
                "request": {
                    "run_setup": {"path": ["body"], "mapping_status": "mapped"},
                    "run_id": {"path": ["id"], "mapping_status": "mapped"},
                },
                "response": {"status": {"path": ["status"], "mapping_status": "mapped"}},
            },
            "request_template": {
                "url": _integration_url(name),
                "method": "POST",
                "headers": {"Authorization": "Bearer <<$auth_key>>", "Content-Type": "application/json"},
                "body": {"query": "<<$run_setup>>"},
            },
            "response_examples": [],
            "factor_variables": {},
        },
        "status_request": {
            "mappings": {"request": {}, "response": {"status": {"path": ["status"], "mapping_status": "mapped"}}},
            "request_template": {"url": _integration_url(name), "method": "GET", "headers": {}, "body": {}},
            "response_examples": [],
        },
        "delivery_request": {
            "mappings": {"request": {}, "response": {}},
            "request_template": {"url": _integration_url(name), "method": "GET", "headers": {}, "body": {}},
            "response_examples": [],
            "response_mappings": {},
        },
    }


def publish_sources(source: Path, target: Path, dry_run: bool) -> None:
    integrations = load_json(source / "integrations.json")["integrations"]
    sources_dir = target / "sources"
    if not dry_run and sources_dir.exists():
        for old in sources_dir.glob("*.json"):
            if old.name not in ("sources.json", "source-template.json"):
                old.unlink()

    ui_sources = []
    for i, integration in enumerate(integrations):
        role = integration.get("integration_role", "source")
        if role == "destination":
            continue
        iid = integration["id"]
        name = integration["name"]
        domain = integration.get("domain_id", "shared")
        list_entry = {
            "id": iid,
            "name": name,
            "description": f"{name} — integrace domény {domain} pro {ANCHOR_ORG_NAME}",
            "source_type": "Integration",
            "delivery_type": "Endpoint",
            "max_concurrent_runs": 10,
            "timeout": 30,
            "average_run_duration": 35 + (i % 5) * 5,
            "created_at": integration.get("created_at", NOW),
            "updated_at": integration.get("updated_at", NOW),
            "status": integration.get("status", "active"),
            "owner_org_id": ANCHOR_ORG_ID,
            "owner_org_name": ANCHOR_ORG_NAME,
            "domain_id": domain,
            "integration_role": role,
            "last_used_at": integration.get("updated_at", NOW),
            "total_runs": 50 + i * 11,
            "successful_runs": 45 + i * 10,
            "failed_runs": 5 + i,
            "success_rate": round(0.88 + (i % 4) * 0.02, 3),
            "activities_count": 1 if role == "source" else 0,
            "workflows_count": 1 if role == "source" else 0,
            "use_cases_count": 1 if role == "tool" else 0,
            "guardrails_count": 1 if role == "tool" else 0,
        }
        ui_sources.append(list_entry)
        detail = {
            **list_entry,
            "setup": _default_source_setup(name),
        }
        write_json(sources_dir / f"{iid}.json", detail, dry_run)

    write_json(sources_dir / "sources.json", {"sources": ui_sources}, dry_run)


def publish_chat_agents(source: Path, target: Path, dry_run: bool) -> None:
    agents = load_json(source / "agents.json")["agents"]
    integrations = load_json(source / "integrations.json")["integrations"]
    agents_dir = target / "chat-agents"
    if not dry_run and agents_dir.exists():
        for old in agents_dir.glob("*.json"):
            if old.name != "chat-agents.json":
                old.unlink()

    tools_by_domain: dict[str, list[str]] = {}
    sources_by_domain: dict[str, list[str]] = {}
    for integ in integrations:
        domain = integ.get("domain_id", "shared")
        role = integ.get("integration_role", "source")
        if role == "tool":
            tools_by_domain.setdefault(domain, []).append(integ["id"])
        elif role == "source":
            sources_by_domain.setdefault(domain, []).append(integ["id"])

    list_items = []
    for agent in agents:
        domain = agent.get("domain_id", "shared")
        file_id = agent["id"]
        tree_path = f"/knowledgebase/{domain}"
        tool_ids = tools_by_domain.get(domain, [])
        source_ids = sources_by_domain.get(domain, [])
        detail = {
            "id": file_id,
            "name": agent["name"],
            "description": agent.get("description") or agent.get("primary_use_case_cs", ""),
            "status": agent.get("status", "draft"),
            "domain_id": domain,
            "org_id": agent.get("org_id", ANCHOR_ORG_ID),
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
                    "grants": [
                        {"treePath": tree_path, "scope": "folder", "includeDescendants": True},
                    ],
                    "skillsPath": f"/skills/{domain}",
                    "skillFilePaths": [],
                },
                "data_warehouse_access": {"objectTypeIds": []},
                "realtime_data_access": {
                    "grants": [
                        {
                            "sourceId": sid,
                            "label": "Realtime feed",
                            "streamKey": "events",
                        }
                        for sid in source_ids[:2]
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
                        for tid in tool_ids[:1]
                    ],
                },
            },
        }
        write_json(agents_dir / f"{file_id}.json", detail, dry_run)
        list_items.append(
            {
                "id": agent["id"],
                "name": agent["name"],
                "description": detail["description"],
                "status": agent.get("status", "draft"),
                "domain_id": domain,
            }
        )

    write_json(agents_dir / "chat-agents.json", {"chat_agents": list_items}, dry_run)


def copy_canonical(source: Path, target: Path, dry_run: bool) -> None:
    names = [
        "relationships.json",
        "objects.json",
        "agents.json",
        "integrations.json",
        "values.json",
        "generation_manifest.json",
        "validation_report.json",
        "projects.json",
        "datapoints.json",
        "knowledge-docs.json",
        "knowledge-folders.json",
    ]
    for name in names:
        src = source / name
        if not src.is_file():
            continue
        if dry_run:
            print(f"  [dry-run] would copy {name}")
        else:
            shutil.copy2(src, target / name)

    kb_src = source / "knowledge-content"
    kb_dst = target / "knowledge-content"
    if kb_src.is_dir():
        if dry_run:
            print("  [dry-run] would copy knowledge-content/")
        else:
            if kb_dst.exists():
                shutil.rmtree(kb_dst)
            shutil.copytree(kb_src, kb_dst)


def publish(target: Path, dry_run: bool = False) -> dict[str, Any]:
    source = ROOT
    print(f"Publishing from {source} -> {target}")
    object_types, name_by_id = publish_object_types(source, target, dry_run)
    publish_datasets(source, target, object_types, name_by_id, dry_run)
    publish_workflows_and_activities(source, target, dry_run)
    publish_factors(source, target, object_types, dry_run)
    publish_knowledge_base(source, target, dry_run)
    publish_sources(source, target, dry_run)
    publish_chat_agents(source, target, dry_run)
    copy_canonical(source, target, dry_run)
    stats = {
        "object_types": len(object_types),
        "workflows": len(load_json(source / "workflows.json")["workflows"]),
        "activities": len(load_json(source / "activities.json")["activities"]),
        "knowledge_docs": len(load_json(source / "knowledge-docs.json")["knowledge_docs"]),
    }
    print(f"Published: {stats}")
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish demo data to UI layout")
    parser.add_argument("--target", required=True, help="Path to ui/data directory")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"Target not found: {target}", file=sys.stderr)
        return 1
    publish(target, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
