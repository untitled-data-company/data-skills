# dlt on Dagster — Component Approach

Use the **DltLoadCollectionComponent** when you have (or want) a components-ready Dagster project and prefer YAML-defined defs plus a small `loads.py`.

## Prerequisites

- Dagster project created with `uvx create-dagster project` (or migrated to components).
- `dagster-dlt` installed: `uv add dagster-dlt`.

## 1. Scaffold a dlt component

From the project root (e.g. `my-project/src`):

```bash
dg scaffold defs dagster_dlt.DltLoadCollectionComponent <component_name> [--source <dlt_source>] [--destination <dlt_destination>]
```

Examples:

- `dg scaffold defs dagster_dlt.DltLoadCollectionComponent github_snowflake_ingest --source github --destination snowflake`
- `dg scaffold defs dagster_dlt.DltLoadCollectionComponent my_ingest` (no source/destination; you fill in loads.py manually)

This creates under `defs/<component_name>/`:

- `loads.py` — skeleton dlt source and pipeline
- `defs.yaml` — component definition pointing at those objects

## 2. Edit loads.py

Replace the scaffold with your real dlt source and pipeline. Sources can be:

- Verified: `from github import github_stargazers` then `github_stargazers("org", "repo")`
- Custom: `@dlt.source` / `@dlt.resource` in the same file or imported

Keep at least:

- A variable holding the **source** (e.g. `my_load_source = my_source()`).
- A variable holding the **pipeline** (e.g. `my_load_pipeline = dlt.pipeline(...)`).

Example:

```python
import dlt
from .github import github_stargazers

dlthub_stargazers_source = github_stargazers("dlt-hub", "dlt")
dlthub_stargazers_pipeline = dlt.pipeline(
    pipeline_name="github_stargazers",
    destination="snowflake",
    dataset_name="dlthub_stargazers",
)
```

## 3. Edit defs.yaml

Point the component at the source and pipeline in `loads.py` using dotted Python identifiers relative to the component module:

```yaml
type: dagster_dlt.DltLoadCollectionComponent
attributes:
  loads:
    - source: .loads.dlthub_stargazers_source
      pipeline: .loads.dlthub_stargazers_pipeline
```

You can add multiple `source`/`pipeline` pairs under `loads`.

## 4. Customize assets (translation)

Use `translation` to set group name, description, or metadata for the emitted assets:

```yaml
attributes:
  loads: [ ... ]
  translation:
    group_name: github_data
    description: "Load stargazers from dlt-hub/dlt"
    metadata:
      resource_name: "{{ resource.name }}"
      pipeline_name: "{{ pipeline.pipeline_name }}"
```

`resource` and `pipeline` are in scope for Jinja-style expressions.

## 5. Verify

- `dg list defs` — lists definitions and the assets produced by the load(s).
- `dg dev` — start the UI and materialize the dlt assets from the Assets view.

## Reference

- [Dagster & dlt (Component)](https://docs.dagster.io/integrations/libraries/dlt)
- dlt verified sources: https://dlthub.com/docs/dlt-ecosystem/verified-sources
