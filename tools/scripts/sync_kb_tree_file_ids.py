#!/usr/bin/env python3
"""Set knowledge-base/tree.json fileId to match existing knowledge-files/*.md stems."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TREE_PATH = ROOT / "knowledge-base" / "tree.json"
KB_FILES_DIR = ROOT / "knowledge-base" / "knowledge-files"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def node_prefix(node_id: str) -> str:
    if node_id.startswith("file-"):
        return node_id[len("file-") :]
    return node_id


def find_markdown_stem(prefix: str, md_files: list[Path]) -> str:
    matches = [p for p in md_files if p.stem.startswith(prefix)]
    if len(matches) != 1:
        names = [p.name for p in matches]
        raise SystemExit(
            f"Expected exactly one markdown for prefix {prefix!r}, found {len(matches)}: {names}"
        )
    return matches[0].stem


def sync_tree(nodes: list[dict[str, Any]], md_files: list[Path], dry_run: bool) -> int:
    updated = 0
    for node in nodes:
        children = node.get("children")
        if isinstance(children, list):
            updated += sync_tree(children, md_files, dry_run)

        if node.get("type") != "file":
            continue

        prefix = node_prefix(str(node.get("id", "")))
        new_file_id = find_markdown_stem(prefix, md_files)
        old_file_id = node.get("fileId")
        if old_file_id != new_file_id:
            if not dry_run:
                node["fileId"] = new_file_id
            updated += 1
            print(f"  {old_file_id} -> {new_file_id}")
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing tree.json")
    args = parser.parse_args()

    if not TREE_PATH.exists():
        raise SystemExit(f"Missing {TREE_PATH}")
    if not KB_FILES_DIR.exists():
        raise SystemExit(f"Missing {KB_FILES_DIR}")

    md_files = sorted(KB_FILES_DIR.glob("*.md"))
    payload = load_json(TREE_PATH)
    tree = payload.get("tree", [])
    if not isinstance(tree, list):
        raise SystemExit("tree.json must contain a tree array")

    print(f"{'Dry run: ' if args.dry_run else ''}Syncing fileId in {TREE_PATH}")
    updated = sync_tree(tree, md_files, args.dry_run)
    if not args.dry_run and updated:
        write_json(TREE_PATH, payload)

    print(f"Updated {updated} file node(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
