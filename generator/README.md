# Demo data generator

Relationship-first pipeline for the Meridian Pay anchor tenant (five domain modules).

## Run

```bash
pip install -r requirements.txt
python -m generator.main
python -m generator.publish_ui --target ../ui/data
```

Or one shot: `./scripts/sync-to-ui-data.sh`

## Outputs (repo root)

- `relationships.json`, `object-types.json`, `objects.json`, `datapoints.json`, `values.json`
- `agents.json`, `integrations.json`, `knowledge-folders.json`, `knowledge-docs.json`
- `knowledge-content/knowledgebase/{domain}/**`
- `workflows.json`, `activities.json`, `factors.json`
- `datasets/{domain}/datasets.json`
- `validation_report.json`, `generation_manifest.json`

## Inputs

- `docs/ANCHOR_TENANT.md`, `docs/0*_*.md` (propozice)
- `docs/domains/{domain}/*.md` (generated/updated in Phase 0)
- `blueprints/anchor.yaml`, `blueprints/domains/*.yaml`
