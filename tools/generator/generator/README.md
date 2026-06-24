# Demo data generator

Relationship-first pipeline for the Meridian Pay anchor tenant (five domain modules).

## Layout

- `ROOT` = `tools/` (docs, blueprints under `tools/docs/`)
- Canonical output = `tools/artifacts/canonical/`
- Legacy merge source = `tools/artifacts/legacy/`
- Runtime publish target = demo-data repo root

## Run (full)

```bash
pip install -r requirements.txt
cd tools/generator && python3 -m generator.main
python3 -m generator.publish_ui --target ../..
```

Or one shot from repo root: `./tools/scripts/scripts/sync-to-ui-data.sh`

## Project IDs

Each domain project uses a stable UUID from `make_id("project:{domain_id}")` (see `generator/util.py`). Example: `esg` → `478c1584-69c0-5545-9f34-33d311b96d71`. All domain-scoped entities and relationship `metadata.project_id` values use these IDs.

## Phase order

```
catalogues → graph → derive (+ project_id) → kb_content → orchestration (+ project_id)
→ validate → publish_ui
```

## Published UI layout (`publish_ui --target <ui/data>`)

Flat layout at repo root: `integrations.json` + `integrations/{id}.json`, `agents.json` + `agents/{id}.json`, `datasets/datasets.json`, `knowledge-base/tree.json` + `knowledge-base/files/`. Legacy `sources/` and `chat-agents/` require `--legacy`.

## Run (IT domain only)

```bash
./tools/scripts/regenerate_it_domain.sh
```

Or manually:

```bash
python3 tools/scripts/bootstrap_it_propozice.py
cd tools/generator && python3 -m generator.main --domains it
python3 -m generator.publish_runtime --target ../.. --domains it
python3 tools/scripts/validate_runtime_json.py
```

## Outputs (canonical)

- `tools/artifacts/canonical/relationships.json`, `object-types.json`, `objects.json`, …
- `tools/artifacts/canonical/knowledge-content/knowledgebase/{domain}/**`
- `validation_report.json`, `generation_manifest.json`

## Inputs

- `tools/docs/ANCHOR_TENANT.md`, `tools/docs/0*_*.md` (propozice)
- `tools/docs/IT/` — IT source corpus (`content_map.yaml`)
- `tools/docs/domains/{domain}/*.md` (generated catalogues)
- `tools/docs/blueprints/anchor.yaml`, `tools/docs/blueprints/domains/*.yaml`
