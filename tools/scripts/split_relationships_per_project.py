#!/usr/bin/env python3
"""Split monolith relationships.json into per-project overview/relationships/{projectId}.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATOR_ROOT = ROOT / "tools" / "generator"
sys.path.insert(0, str(GENERATOR_ROOT))

from generator.overview_relationships import publish_overview_relationships_per_project  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Split relationships per project")
    parser.add_argument(
        "--source",
        type=Path,
        default=ROOT,
        help="Directory containing relationships.json and entity JSON files",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=ROOT,
        help="Output directory (default: same as source)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source = args.source.resolve()
    target = args.target.resolve()
    if not (source / "relationships.json").is_file():
        print(f"ERROR: relationships.json not found in {source}", file=sys.stderr)
        return 1

    counts = publish_overview_relationships_per_project(source, target, dry_run=args.dry_run)
    print(f"Wrote {len(counts)} project relationship files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
