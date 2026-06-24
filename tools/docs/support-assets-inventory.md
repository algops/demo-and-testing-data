# Support Assets Inventory

This inventory tracks files and folders in `demo-and-testing-data` that are not required by the runtime API contract and were moved under `tools/`.

## Runtime Contract (repo root)

| Path | Purpose |
| --- | --- |
| `projects.json` | Project list (`{ "projects": [...], "user": {...} }`) |
| `overview/relationships.json` | Overview relationships graph (`metadata.project_id` per domain) |
| `knowledge-base/tree.json` | Knowledge base folder tree (`fileId` = `knowledge-files/{fileId}.md` stem) |
| `knowledge-base/knowledge-files/{fileId}.md` | Knowledge base markdown files |
| `data-warehouse/datasets.json` | Dataset catalog |
| `data-warehouse/datasets/{objectTypeId}.json` | Dataset rows (`{ "data": [...] }` only) |
| `chat-agents/agents.json` | Agents list (`{ "agents": [...] }`) |
| `chat-agents/agents/{id}.json` | Agent detail (`id`, `name`, `description`, `status`, `setup`) |
| `integrations/integrations.json` | Integrations list (`{ "integrations": [...] }`) |
| `integrations/integrations/{id}.json` | Integration detail |

## Runtime cleanup scripts (`tools/scripts/`)

| Script | Purpose |
| --- | --- |
| `trim_runtime_json.py` | Phase 1: strip unused attributes from runtime JSON |
| `validate_runtime_json.py` | Validate trimmed contract + linkage fixes |
| `sync_kb_tree_file_ids.py` | Phase 2a: align `tree.json` `fileId` with existing `.md` stems |
| `annotate_relationships_project_id.py` | Phase 2b: add `metadata.project_id` from `domain_id` |
| `ensure_integration_details.py` | Phase 2c: create missing integration detail JSON files |

## Generation and tooling assets

| Current path (before cleanup) | Classification | Reason | New target path |
| --- | --- | --- | --- |
| `generator/` | support-only | Demo data generation pipeline code | `tools/generator/generator/` |
| `scripts/` | support-only | Utility shell scripts for generation/sync workflows | `tools/scripts/scripts/` |
| `blueprints/` | support-only | Authoring blueprints used to synthesize demo data | `tools/docs/blueprints/` |
| `populate_all_sources.py` | support-only | Source population helper script | `tools/scripts/populate_all_sources.py` |
| `populate_sources_factors.py` | support-only | Factor/source generation helper script | `tools/scripts/populate_sources_factors.py` |
| `update_all_sources.py` | support-only | Source update helper script | `tools/scripts/update_all_sources.py` |
| `update_factors.py` | support-only | Factor update helper script | `tools/scripts/update_factors.py` |
| `requirements.txt` | support-only | Python deps used for generation pipeline only | `tools/generator/requirements.txt` |
| `generation_manifest.json` | support-only | Generation run metadata artifact | `tools/artifacts/generation_manifest.json` |
| `validation_report.json` | support-only | Generation validation artifact | `tools/artifacts/validation_report.json` |

## Legacy pre-contract assets

These were used during demo data generation or older UI contracts and are archived under `tools/artifacts/legacy/`.

| Current path (before cleanup) | Classification | Reason | New target path |
| --- | --- | --- | --- |
| `activities/` | support-only | Legacy activity detail payloads | `tools/artifacts/legacy/activities/` |
| `activities.json` | support-only | Legacy activity list | `tools/artifacts/legacy/activities.json` |
| `agents.json` | support-only | Canonical agent list used to build runtime contract | `tools/artifacts/legacy/agents.json` |
| `chat-agents/` (flat layout) | support-only | Legacy chat agent detail files and `chat-agents.json` | `tools/artifacts/legacy/chat-agents/` |
| `dashboard-full.json` | support-only | Legacy dashboard payload | `tools/artifacts/legacy/dashboard-full.json` |
| `datapoints.json` | support-only | Canonical datapoint graph input | `tools/artifacts/legacy/datapoints.json` |
| `datasets/` | support-only | Legacy dataset detail and domain catalogs | `tools/artifacts/legacy/datasets/` |
| `factors.json` | support-only | Legacy factor definitions | `tools/artifacts/legacy/factors.json` |
| `integrations.json` | support-only | Canonical integration list used to build runtime contract | `tools/artifacts/legacy/integrations.json` |
| `knowledge-base/files/` | support-only | Legacy knowledge file JSON stubs | `tools/artifacts/legacy/knowledge-base/` |
| `knowledge-content/` | support-only | Source markdown tree used to generate knowledge files | `tools/artifacts/legacy/knowledge-content/` |
| `knowledge-docs.json` | support-only | Knowledge doc index used during generation | `tools/artifacts/legacy/knowledge-docs.json` |
| `knowledge-folders.json` | support-only | Knowledge folder index used during generation | `tools/artifacts/legacy/knowledge-folders.json` |
| `object-types/` | support-only | Legacy object type detail payloads | `tools/artifacts/legacy/object-types/` |
| `object-types.json` | support-only | Legacy object type list | `tools/artifacts/legacy/object-types.json` |
| `objects.json` | support-only | Canonical object graph input | `tools/artifacts/legacy/objects.json` |
| `overview.json` | support-only | Legacy overview payload | `tools/artifacts/legacy/overview.json` |
| `projects.json` | support-only | Legacy projects payload | `projects.json` |
| `relationships.json` | support-only | Canonical relationships graph input | `tools/artifacts/legacy/relationships.json` |
| `sources/` | support-only | Legacy integration/source detail payloads | `tools/artifacts/legacy/sources/` |
| `targets.json` | support-only | Legacy targets payload | `tools/artifacts/legacy/targets.json` |
| `values.json` | support-only | Canonical values graph input | `tools/artifacts/legacy/values.json` |
| `workflows/` | support-only | Legacy workflow detail payloads | `tools/artifacts/legacy/workflows/` |
| `workflows.json` | support-only | Legacy workflow list | `tools/artifacts/legacy/workflows.json` |

## Project scoping

Runtime list/tree payloads are scoped by `project_id`, aligned with UI project IDs from `ui/data/projects.json`:

| `domain_id` | `project_id` |
| --- | --- |
| `esg` | `org:anchor:esg` |
| `it` | `org:anchor:it` |
| `legal` | `org:anchor:legal` |
| `tax` | `org:anchor:tax` |
| `hr` | `org:anchor:hr` |

Annotated runtime files:

- `chat-agents/agents.json` (23 agents)
- `integrations/integrations.json` (27 integrations)
- `data-warehouse/datasets.json` (63 project-scoped catalog entries)
- `knowledge-base/tree.json` (121 file nodes with `project_id`)

Regenerate scoping with:

```bash
python3 tools/scripts/annotate_project_scope.py
```

Dataset catalog exclusions (16 object types) are intentional for `shared`/unmapped domains and are reported by the script.

## Notes

- Runtime contract files live at the repository root (no intermediate `data/` folder).
- Local clutter artifacts (for example `.DS_Store`, `__pycache__`, `.pyc`, `.cursor/plans`) were intentionally left untouched.
- KB markdown filenames (`knowledge-files/{docId}.md`) may still differ from tree `fileId` values (`kb-{domain}-###`); that is a separate follow-up from project scoping.
