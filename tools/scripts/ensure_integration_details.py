#!/usr/bin/env python3
"""Create missing integrations/integrations/{id}.json detail files from list entries."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INTEGRATIONS_LIST_PATH = ROOT / "integrations" / "integrations.json"
INTEGRATIONS_DIR = ROOT / "integrations" / "integrations"

EMPTY_SETUP: dict[str, Any] = {
    "customization_permissions": {"factor_creation": "creator_only"},
    "load_balancing": {"concurrency": 10, "timeout": 30},
    "processing_options": {"input_processing": "ignore"},
    "run_request": {
        "mappings": {
            "request": {
                "run_setup": {"path": [], "mapping_status": "remaining"},
                "run_id": {"path": [], "mapping_status": "remaining"},
                "webhook_url": {"path": [], "mapping_status": "remaining"},
            },
            "response": {
                "status": {"path": [], "mapping_status": "remaining"},
            },
        },
        "request_template": {"url": "", "method": "POST", "headers": {}, "body": {}},
        "response_examples": [],
        "factor_variables": {},
    },
    "status_request": {
        "mappings": {
            "request": {"run_external_id": {"path": [], "mapping_status": "remaining"}},
            "response": {"status": {"path": [], "mapping_status": "remaining"}},
        },
        "request_template": {"url": "", "method": "GET", "headers": {}, "body": {}},
        "response_examples": [],
    },
    "delivery_request": {
        "mappings": {"request": {}, "response": {}},
        "request_template": {"url": "", "method": "GET", "headers": {}, "body": {}},
        "response_examples": [],
        "response_mappings": {},
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_detail(entry: dict[str, Any]) -> dict[str, Any]:
    domain = entry.get("domain_id", "")
    name = entry.get("name", "Integration")
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    role = entry.get("integration_role", "destination")
    return {
        "id": entry["id"],
        "name": name,
        "description": f"{name} — integrace domény {domain} pro Meridian Pay a.s.",
        "source_type": "Integration",
        "delivery_type": "Endpoint",
        "max_concurrent_runs": 10,
        "timeout": 30,
        "average_run_duration": 0,
        "created_at": now,
        "updated_at": now,
        "status": entry.get("status", "active"),
        "owner_org_id": "org:anchor",
        "owner_org_name": "Meridian Pay a.s.",
        "domain_id": domain,
        "integration_role": role,
        "last_used_at": now,
        "total_runs": 0,
        "successful_runs": 0,
        "failed_runs": 0,
        "success_rate": 0.0,
        "activities_count": 0,
        "workflows_count": 0,
        "use_cases_count": 0,
        "guardrails_count": 0,
        "setup": json.loads(json.dumps(EMPTY_SETUP)),
    }


def main() -> int:
    integrations = load_json(INTEGRATIONS_LIST_PATH).get("integrations", [])
    existing = {
        p.stem for p in INTEGRATIONS_DIR.glob("*.json") if p.name != "sources.json"
    }
    created = 0
    for entry in integrations:
        integration_id = entry.get("id")
        if not integration_id or integration_id in existing:
            continue
        path = INTEGRATIONS_DIR / f"{integration_id}.json"
        write_json(path, build_detail(entry))
        print(f"  created {path.name} ({entry.get('name')})")
        created += 1

    print(f"Created {created} integration detail file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
