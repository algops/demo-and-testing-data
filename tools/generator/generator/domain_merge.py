"""Merge domain-scoped generation output with frozen legacy canonical data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .util import CANONICAL_ROOT, LEGACY_ROOT

LIST_KEYS = {
    "relationships": "relationships",
    "object-types": "object_types",
    "datapoints": "datapoints",
    "objects": "objects",
    "values": "values",
    "integrations": "integrations",
    "agents": "agents",
    "knowledge-folders": "knowledge_folders",
    "knowledge-docs": "knowledge_docs",
    "workflows": "workflows",
    "activities": "activities",
    "factors": "factors",
}


def _load(path: Path, key: str) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return json.loads(path.read_text(encoding="utf-8")).get(key, [])


def _write(path: Path, key: str, items: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({key: items}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _ids_by_domain(items: list[dict], domain: str) -> set[str]:
    return {i["id"] for i in items if i.get("domain_id") == domain}


def _kb_folder_ids_for_domain(folders: list[dict], domain: str) -> set[str]:
    return {
        f["id"]
        for f in folders
        if f.get("domain_id") == domain or f.get("path", "").startswith(f"knowledgebase/{domain}/")
    }


def merge_domain_slice(target_domains: tuple[str, ...]) -> None:
    fresh = {key: _load(CANONICAL_ROOT / f"{stem}.json", key) for stem, key in LIST_KEYS.items()}
    legacy = {key: _load(LEGACY_ROOT / f"{stem}.json", key) for stem, key in LIST_KEYS.items()}

    merged: dict[str, list[dict[str, Any]]] = {}
    drop_ids: set[str] = set()

    for domain in target_domains:
        drop_ids |= _ids_by_domain(legacy["objects"], domain)
        drop_ids |= _ids_by_domain(fresh["objects"], domain)
        drop_ids |= _ids_by_domain(legacy["agents"], domain)
        drop_ids |= _ids_by_domain(legacy["integrations"], domain)
        drop_ids |= _ids_by_domain(legacy["knowledge_docs"], domain)
        drop_ids |= _kb_folder_ids_for_domain(legacy["knowledge_folders"], domain)

    def domain_filter(items: list[dict], domain_key: str = "domain_id") -> list[dict]:
        return [i for i in items if i.get(domain_key) not in target_domains]

    merged["objects"] = domain_filter(legacy["objects"])
    merged["objects"].extend([o for o in fresh["objects"] if o.get("domain_id") in target_domains])

    merged["object_types"] = domain_filter(legacy["object_types"])
    merged["object_types"].extend(
        [ot for ot in fresh["object_types"] if ot.get("domain_id") in target_domains]
    )

    merged["datapoints"] = domain_filter(legacy["datapoints"])
    merged["datapoints"].extend(
        [dp for dp in fresh["datapoints"] if dp.get("domain_id") in target_domains]
    )

    fresh_obj_ids = {o["id"] for o in fresh["objects"] if o.get("domain_id") in target_domains}
    merged["values"] = [v for v in legacy["values"] if v.get("object_id") not in drop_ids]
    merged["values"].extend(fresh["values"])

    for key in ("integrations", "agents", "knowledge_docs", "knowledge_folders"):
        merged[key] = domain_filter(legacy[key])
        merged[key].extend([e for e in fresh[key] if e.get("domain_id") in target_domains])

    for key in ("workflows", "activities", "factors"):
        merged[key] = domain_filter(legacy[key])
        merged[key].extend([e for e in fresh[key] if e.get("domain_id") in target_domains])

    fresh_entity_ids: set[str] = set()
    for key in ("objects", "agents", "integrations", "knowledge_docs", "knowledge_folders"):
        fresh_entity_ids |= {e["id"] for e in fresh[key] if e.get("domain_id") in target_domains}

    def keep_rel(rel: dict) -> bool:
        meta = rel.get("metadata") or {}
        if meta.get("domain_id") in target_domains:
            return False
        if rel.get("origin_id") in drop_ids or rel.get("destination_id") in drop_ids:
            return False
        return True

    merged["relationships"] = [r for r in legacy["relationships"] if keep_rel(r)]
    merged["relationships"].extend(fresh["relationships"])

    for stem, key in LIST_KEYS.items():
        _write(CANONICAL_ROOT / f"{stem}.json", key, merged[key])
