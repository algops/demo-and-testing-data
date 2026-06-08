"""Generate on-disk knowledge markdown files."""

from __future__ import annotations

from pathlib import Path

from .graph import GraphState
from .kb_templates import render_document
from .util import ROOT


def write_kb_content(state: GraphState, docs_meta: list[dict]) -> None:
    base = ROOT / "knowledge-content"
    for doc in docs_meta:
        rel = doc["content_path"].replace("knowledge-content/", "")
        path = base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        body = render_document(doc)
        path.write_text(body, encoding="utf-8")
