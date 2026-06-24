#!/usr/bin/env python3
"""Annotate overview/relationships.json with metadata.project_id from metadata.domain_id."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RELATIONSHIPS_PATH = ROOT / "overview" / "relationships.json"

DOMAIN_TO_PROJECT = {
    "esg": "org:anchor:esg",
    "it": "org:anchor:it",
    "legal": "org:anchor:legal",
    "tax": "org:anchor:tax",
    "hr": "org:anchor:hr",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    payload = load_json(RELATIONSHIPS_PATH)
    relationships = payload.get("relationships", [])
    updated = 0
    skipped = 0

    for edge in relationships:
        metadata = edge.setdefault("metadata", {})
        domain_id = metadata.get("domain_id")
        project_id = DOMAIN_TO_PROJECT.get(domain_id) if isinstance(domain_id, str) else None
        if not project_id:
            skipped += 1
            continue
        if metadata.get("project_id") != project_id:
            metadata["project_id"] = project_id
            updated += 1

    print(f"Relationships: {len(relationships)} total")
    print(f"  updated project_id: {updated}")
    print(f"  skipped (no mappable domain_id): {skipped}")

    if not args.dry_run and updated:
        write_json(RELATIONSHIPS_PATH, payload)
    elif args.dry_run:
        print("Dry run — no file written")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
