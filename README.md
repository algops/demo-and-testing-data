# Demo and Testing Data

Relationship-first demo corpus for **one anchor tenant** — Meridian Pay a.s. — with five enabled domain modules (`esg`, `it`, `legal`, `tax`, `hr`).

## Regenerate

```bash
pip install -r requirements.txt
python -m generator.main
```

See [generator/README.md](generator/README.md) for pipeline phases and artifacts.

## Documentation (authoring)

- [docs/ANCHOR_TENANT.md](docs/ANCHOR_TENANT.md) — tenant identity, systems, vendors
- [docs/domains/README.md](docs/domains/README.md) — org-layer types, bridge matrix
- [docs/domains/{domain}/](docs/domains/) — per-domain catalogues
- Propozice: [docs/01_ESG_COMPLIANCE.md](docs/01_ESG_COMPLIANCE.md) … [05_HR_SOP.md](docs/05_HR_SOP.md)
- [blueprints/](blueprints/) — generation blueprints

## Generated artifacts

`relationships.json`, `object-types.json`, `objects.json`, `datapoints.json`, `values.json`, `agents.json`, `integrations.json`, `knowledge-*.json`, `knowledge-content/`, `workflows.json`, `activities.json`, `factors.json`, `datasets/`, `validation_report.json`, `generation_manifest.json`

## Integration

Git submodule in UI at `data/` (branch `demo-dev`).
