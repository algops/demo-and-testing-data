"""Phase 2: derive endpoint entity JSON from graph state."""

from __future__ import annotations

from typing import Any

from .attribute_types import get_data_type
from .agent_specs import get_agent_slug
from .catalogues import DOMAIN_AGENTS, DOMAIN_INTEGRATIONS, _load_domain_spec
from .graph import GraphState, ORG_TYPES, SYSTEM_NAMES, VENDOR_NAMES, DEPT_NAMES
from .util import DOMAINS, NOW, ORG_ID, BLUEPRINTS_ROOT, SHARED, load_yaml_simple, make_id, project_id_for_domain, slugify


def _stamp_project_id(item: dict[str, Any], domain: str) -> dict[str, Any]:
    pid = project_id_for_domain(domain)
    if pid:
        item["project_id"] = pid
    return item


def derive_object_types(state: GraphState) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for key, oid in state.object_type_ids.items():
        if key.startswith("meta:"):
            continue
        domain, slug = key.split(":", 1) if ":" in key else (SHARED, key)
        items.append(
            _stamp_project_id(
                {
                    "id": oid,
                    "name": slug,
                    "description": f"Object type {slug}",
                    "org_id": ORG_ID,
                    "domain_id": domain,
                    "created_at": NOW,
                    "updated_at": NOW,
                    "deleted_at": None,
                },
                domain,
            )
        )
    return items


def derive_datapoints(state: GraphState) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for key, did in state.datapoint_ids.items():
        parts = key.split(":")
        domain, type_slug = parts[0], parts[1]
        attr = ":".join(parts[2:])
        ot_key = f"{domain}:{type_slug}"
        items.append(
            _stamp_project_id(
                {
                    "id": did,
                    "name": attr,
                    "key": attr,
                    "object_type_id": state.object_type_ids.get(ot_key, ""),
                    "org_id": ORG_ID,
                    "domain_id": domain,
                    "data_type": get_data_type(domain, attr),
                    "created_at": NOW,
                    "updated_at": NOW,
                },
                domain,
            )
        )
    return items


def derive_objects(state: GraphState) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for key, oid in state.object_ids.items():
        parts = key.split(":")
        if parts[0] == "shared":
            domain = SHARED
            slug = parts[-1]
            type_slug = parts[1]
        else:
            domain = parts[0]
            type_slug = parts[1]
            slug = parts[2] if len(parts) > 2 else "0000"
        name = state.object_names.get(key)
        if not name:
            name = slug.replace("-", " ").replace("_", " ").title()
            if type_slug == "organization":
                name = "Meridian Pay a.s."
        items.append(
            _stamp_project_id(
                {
                    "id": oid,
                    "name": name,
                    "object_type_id": state.object_type_ids.get(
                        f"{domain}:{type_slug}" if domain != SHARED else f"shared:{type_slug}"
                    ),
                    "org_id": ORG_ID,
                    "domain_id": domain,
                    "created_at": NOW,
                    "updated_at": NOW,
                    "deleted_at": None,
                },
                domain,
            )
        )
    return items


def derive_values(state: GraphState) -> list[dict[str, Any]]:
    object_domain: dict[str, str] = {}
    for key, oid in state.object_ids.items():
        domain = key.split(":", 1)[0]
        object_domain[oid] = domain

    items: list[dict[str, Any]] = []
    for val_id, payload in state.value_payloads.items():
        meta = state.value_meta.get(val_id, {})
        obj_id = meta.get("object_id", "")
        domain = object_domain.get(obj_id, SHARED)
        items.append(
            _stamp_project_id(
                {
                    "id": val_id,
                    "object_id": obj_id,
                    "datapoint_id": meta.get("datapoint_id"),
                    "value": payload,
                    "org_id": ORG_ID,
                    "created_at": NOW,
                    "updated_at": NOW,
                },
                domain,
            )
        )
    return items


def derive_integrations(state: GraphState) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for key, iid in state.integration_ids.items():
        domain, slug = key.split(":", 1)
        spec = next((s for s in DOMAIN_INTEGRATIONS[domain] if slugify(s["name"]) == slug), None)
        items.append(
            _stamp_project_id(
                {
                    "id": iid,
                    "name": spec["name"] if spec else slug,
                    "integration_role": spec["role"] if spec else "source",
                    "org_id": ORG_ID,
                    "domain_id": domain,
                    "status": "active",
                    "created_at": NOW,
                    "updated_at": NOW,
                },
                domain,
            )
        )
    return items


def derive_agents(state: GraphState) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for domain in DOMAINS:
        for i, spec in enumerate(DOMAIN_AGENTS[domain]):
            slug = get_agent_slug(spec)
            aid = make_id(f"agent:{domain}:{slug}")
            items.append(
                _stamp_project_id(
                    {
                        "id": aid,
                        "name": spec["name"],
                        "slug": slug,
                        "description": spec["use_case"],
                        "org_id": ORG_ID,
                        "domain_id": domain,
                        "primary_use_case_cs": spec["use_case"],
                        "status": "active" if i == 0 else "draft",
                        "created_at": NOW,
                        "updated_at": NOW,
                    },
                    domain,
                )
            )
    return items


def derive_knowledge_folders(state: GraphState) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path, fid in state.kb_folder_ids.items():
        domain = path.split("/")[1] if "/" in path and path != "knowledgebase" else SHARED
        folder_domain = domain if domain in DOMAINS else SHARED
        items.append(
            _stamp_project_id(
                {
                    "id": fid,
                    "path": path,
                    "name": path.split("/")[-1],
                    "org_id": ORG_ID,
                    "domain_id": folder_domain,
                    "created_at": NOW,
                },
                folder_domain,
            )
        )
    return items


def derive_projects() -> dict[str, Any]:
    anchor = load_yaml_simple(BLUEPRINTS_ROOT / "anchor.yaml")
    org = anchor.get("org", {})
    org_id = org.get("org_id_seed", ORG_ID)
    parent_name = org.get("legal_name", "Meridian Pay a.s.")
    project_specs = anchor.get("projects", [])
    if not project_specs:
        project_specs = [{"domain_id": d, "name": d.upper(), "logo": "Building2", "plan": "Enterprise"} for d in DOMAINS]
    projects = []
    for spec in project_specs:
        domain = spec["domain_id"]
        projects.append(
            {
                "id": make_id(f"project:{domain}"),
                "name": spec.get("name", domain.upper()),
                "domain_id": domain,
                "org_id": org_id,
                "parent_org_name": parent_name,
                "logo": spec.get("logo", "Building2"),
                "plan": spec.get("plan", "Enterprise"),
            }
        )
    return {
        "projects": projects,
        "user": {
            "name": "Eva Nováková",
            "email": "eva.novakova@meridianpay.cz",
            "avatar": "/avatars/eva.jpg",
        },
    }


def derive_knowledge_docs(state: GraphState) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for key, did in state.kb_doc_ids.items():
        domain = key.split(":", 1)[0]
        meta = state.kb_doc_meta.get(key, {})
        rel_path = meta.get("rel_path", f"core/doc-{key.split(':', 1)[1]}.md")
        title = meta.get("title", rel_path)
        doc_record: dict[str, Any] = _stamp_project_id(
            {
                "id": did,
                "title": title,
                "doc_kind": meta.get("doc_kind", "guideline"),
                "language": "cs",
                "sensitivity": "internal",
                "org_id": ORG_ID,
                "domain_id": domain,
                "content_path": f"knowledge-content/knowledgebase/{domain}/{rel_path}",
                "token_count": 800,
                "version": "1.0",
                "created_at": NOW,
                "updated_at": NOW,
            },
            domain,
        )
        for field in (
            "agent_slug",
            "agent_name",
            "use_case",
            "persona",
            "audience",
            "guardrails",
            "demo_questions",
            "must_read_sections",
            "operates_on",
        ):
            if field in meta:
                doc_record[field] = meta[field]
        items.append(doc_record)
    return items
