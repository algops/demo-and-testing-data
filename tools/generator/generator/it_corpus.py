"""Load and normalize IT source documentation from tools/docs/IT/."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from .util import DOCS_ROOT, load_yaml_simple

IT_DOCS_ROOT = DOCS_ROOT / "IT"
CONTENT_MAP_PATH = IT_DOCS_ROOT / "content_map.yaml"


def _normalize_path(rel: str) -> str:
    return unquote(rel).replace("\\", "/")


def _strip_noise(text: str) -> str:
    out = text
    out = re.sub(r"!\[[^\]]*\]\([^)]+\)", "[image omitted]", out)
    out = re.sub(r"!\[\]\([^)]+\)", "[image omitted]", out)
    out = re.sub(r"\[([^\]]+)\]\(https?://iguana\.wiki[^)]+\)", r"\1", out)
    out = re.sub(r"\[([^\]]+)\]\(\./[^)]+\)", r"\1", out)
    out = re.sub(r"\[([^\]]+)\]\(\.\./[^)]+\)", r"\1", out)
    out = re.sub(r"https?://iguana\.wiki[^\s)>]+", "", out)
    out = re.sub(r"https?://praguelabs\.getoutline\.com[^\s)>]+", "", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


@lru_cache(maxsize=1)
def load_content_map() -> dict[str, Any]:
    if CONTENT_MAP_PATH.is_file():
        return load_yaml_simple(CONTENT_MAP_PATH)
    return {}


def read_source(rel_path: str) -> str:
    path = IT_DOCS_ROOT / _normalize_path(rel_path)
    if not path.is_file():
        return f"(Source not found: {rel_path})"
    return _strip_noise(path.read_text(encoding="utf-8"))


def slot_key_from_doc(doc: dict[str, Any]) -> str | None:
    cp = doc.get("content_path", "")
    m = re.search(r"knowledgebase/it/(.+)\.md$", cp.replace("\\", "/"))
    if not m:
        return None
    return m.group(1).replace("/", "/")


def lookup_kb_body(doc: dict[str, Any]) -> str | None:
    rel = slot_key_from_doc(doc)
    if not rel:
        return None
    cmap = load_content_map()
    for entry in cmap.get("kb_docs", []):
        if entry.get("slot") == rel:
            return read_source(entry["source"])
    return None


def kb_title_for_doc(doc: dict[str, Any]) -> str | None:
    rel = slot_key_from_doc(doc)
    if not rel:
        return None
    for entry in load_content_map().get("kb_docs", []):
        if entry.get("slot") == rel:
            return entry.get("title")
    return None


def agent_excerpt(agent_slug: str, doc_kind: str) -> str:
    cmap = load_content_map()
    sources = cmap.get("agent_docs", {}).get(agent_slug, {}).get("sources", [])
    if not sources:
        return ""
    parts = [read_source(s) for s in sources[:2]]
    combined = "\n\n---\n\n".join(parts)
    if doc_kind == "system_prompt":
        return combined[:4000]
    if doc_kind == "agent_role":
        return combined[:2500]
    return combined[:1500]


@lru_cache(maxsize=1)
def warehouse_terms() -> dict[str, list[str]]:
    return load_content_map().get("warehouse_terms", {})


def header(doc: dict[str, Any]) -> str:
    kind = doc.get("doc_kind", "guideline")
    title = doc.get("title", "IT document")
    return f"# {title}\n\n> Typ: {kind} | Doména: it | Citlivost: internal\n\n"
