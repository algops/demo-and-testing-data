#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"

echo "==> Bootstrap IT propozice (if needed)"
python3 "$ROOT/scripts/bootstrap_it_propozice.py"

echo "==> Generate IT domain slice"
cd "$ROOT/generator"
python3 -m generator.main --domains it

echo "==> Publish to runtime (repo root)"
python3 -m generator.publish_runtime --target "$REPO_ROOT" --domains it

echo "==> Validate runtime contract"
python3 "$ROOT/scripts/validate_runtime_json.py"

echo "Done."
