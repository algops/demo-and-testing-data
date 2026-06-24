"""Shared utilities for demo data generation."""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
REPO_ROOT = ROOT.parent
CANONICAL_ROOT = ROOT / "artifacts" / "canonical"
LEGACY_ROOT = ROOT / "artifacts" / "legacy"
DOCS_ROOT = ROOT / "docs"
BLUEPRINTS_ROOT = DOCS_ROOT / "blueprints"
NAMESPACE = uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
ORG_ID = "org:anchor"
DOMAINS = ("esg", "it", "legal", "tax", "hr")
SHARED = "shared"
NOW = datetime(2025, 6, 1, 12, 0, 0, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def make_id(seed: str) -> str:
    return str(uuid.uuid5(NAMESPACE, seed))


def project_id_for_domain(domain_id: str | None) -> str | None:
    if domain_id and domain_id in DOMAINS:
        return make_id(f"project:{domain_id}")
    return None


def slugify(name: str) -> str:
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return s.lower().replace(" ", "_").replace("-", "_")


def parse_range(value: str | int) -> int:
    if isinstance(value, int):
        return value
    if "-" in str(value):
        lo, hi = str(value).split("-", 1)
        return (int(lo) + int(hi)) // 2
    return int(value)


def load_json_block(md_path: Path, key: str) -> dict[str, Any]:
    text = md_path.read_text(encoding="utf-8")
    marker = f'"{key}"'
    start = text.find(marker)
    if start == -1:
        return {key: []}
    brace = text.rfind("{", 0, start)
    if brace == -1:
        brace = text.find("{", start)
    depth = 0
    in_string = False
    escape = False
    for i in range(brace, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[brace : i + 1])
                except json.JSONDecodeError:
                    return {key: []}
    return {key: []}


def load_yaml_simple(path: Path) -> dict[str, Any]:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def checksum(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]
