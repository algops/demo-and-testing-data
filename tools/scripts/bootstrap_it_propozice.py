#!/usr/bin/env python3
"""Bootstrap tools/docs/02_IT_SW_DEVELOPMENT.md from legacy IT schema."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "artifacts" / "legacy"
OUT = ROOT / "docs" / "02_IT_SW_DEVELOPMENT.md"

TYPE_LABELS = {
    "service": "Service",
    "api": "API",
    "database": "Database",
    "pipeline": "Pipeline",
    "team": "Team",
    "adr": "ADR",
    "guideline": "Guideline",
    "dependency": "Dependency",
    "environment": "Environment",
    "incident": "Incident",
    "tech_debt": "TechDebt",
    "slo": "SLO",
    "runbook": "Runbook",
    "feature_flag": "FeatureFlag",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_entity_types() -> list[dict]:
    ots = load_json(LEGACY / "object-types.json")["object_types"]
    dps = load_json(LEGACY / "datapoints.json")["datapoints"]
    objects = load_json(LEGACY / "objects.json")["objects"]

    it_ot_by_id = {ot["id"]: ot for ot in ots if ot.get("domain_id") == "it"}
    attrs_by_type: dict[str, list[str]] = defaultdict(list)
    for dp in dps:
        if dp.get("domain_id") != "it":
            continue
        name = dp["name"]
        if name.startswith("rel:"):
            continue
        ot_id = dp["object_type_id"]
        if ot_id in it_ot_by_id:
            attrs_by_type[it_ot_by_id[ot_id]["name"]].append(name)

    examples_by_type: dict[str, list[str]] = defaultdict(list)
    ot_id_to_name = {ot["id"]: ot["name"] for ot in it_ot_by_id.values()}
    for obj in objects:
        if obj.get("domain_id") != "it":
            continue
        tname = ot_id_to_name.get(obj["object_type_id"])
        if tname and len(examples_by_type[tname]) < 8:
            examples_by_type[tname].append(obj["name"])

    entity_types = []
    for slug in sorted(attrs_by_type.keys()):
        label = TYPE_LABELS.get(slug, slug.replace("_", " ").title())
        entity_types.append(
            {
                "type": label,
                "attributes": sorted(attrs_by_type[slug]),
                "examples": examples_by_type.get(slug, [f"{label} example"]),
            }
        )
    return entity_types


def build_relationship_types() -> list[dict]:
    rels = load_json(LEGACY / "relationships.json")["relationships"]
    objects = {o["id"]: o for o in load_json(LEGACY / "objects.json")["objects"]}
    ots = {ot["id"]: ot["name"] for ot in load_json(LEGACY / "object-types.json")["object_types"]}

    seen: set[tuple] = set()
    attrs_by_edge: dict[str, set[str]] = defaultdict(set)
    relationship_types: list[dict] = []

    for rel in rels:
        meta = rel.get("metadata") or {}
        if meta.get("domain_id") != "it" or not meta.get("domain_edge"):
            continue
        edge_type = meta["domain_edge"]
        for attr in (meta.get("edge_values") or {}).keys():
            attrs_by_edge[edge_type].add(attr)

        origin = objects.get(rel["origin_id"])
        dest = objects.get(rel["destination_id"])
        if not origin or not dest:
            continue
        from_type = TYPE_LABELS.get(ots.get(origin["object_type_id"], ""), ots.get(origin["object_type_id"], ""))
        to_type = TYPE_LABELS.get(ots.get(dest["object_type_id"], ""), ots.get(dest["object_type_id"], ""))
        if not from_type or not to_type:
            continue
        key = (edge_type, from_type, to_type)
        if key in seen:
            continue
        seen.add(key)
        relationship_types.append(
            {
                "type": edge_type,
                "from": from_type,
                "to": to_type,
                "attributes": sorted(attrs_by_edge.get(edge_type, set())),
            }
        )

    return sorted(relationship_types, key=lambda r: (r["type"], r["from"], r["to"]))


def main() -> None:
    entity_types = build_entity_types()
    relationship_types = build_relationship_types()
    payload_et = json.dumps({"entity_types": entity_types}, indent=2, ensure_ascii=False)
    payload_rt = json.dumps({"relationship_types": relationship_types}, indent=2, ensure_ascii=False)

    body = f"""# IT Software Development — Propozice (bootstrapped)

Authoring source for IT domain entity catalogues. Schema extracted from legacy canonical data.

## Entity types

```json
{payload_et}
```

## Relationship types

```json
{payload_rt}
```
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(body, encoding="utf-8")
    print(f"Wrote {OUT} ({len(entity_types)} types, {len(relationship_types)} rel types)")


if __name__ == "__main__":
    main()
