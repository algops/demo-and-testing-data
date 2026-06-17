#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UI_DATA="${UI_DATA:-$ROOT/../ui/data}"

cd "$ROOT"
python3 -m generator.main
python3 -m generator.publish_ui --target "$UI_DATA"
echo "Synced to $UI_DATA"
