#!/usr/bin/env bash
set -euo pipefail

TOOLS="$(cd "$(dirname "$0")/../.." && pwd)"
GENERATOR="$TOOLS/generator"
UI_DATA="${UI_DATA:-$TOOLS/..}"
PYTHON="${PYTHON:-python3}"

cd "$GENERATOR"
"$PYTHON" -m generator.main
"$PYTHON" -m generator.publish_ui --target "$UI_DATA"
echo "Synced to $UI_DATA"
