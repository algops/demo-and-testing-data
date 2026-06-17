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
python -m generator.main
```

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
