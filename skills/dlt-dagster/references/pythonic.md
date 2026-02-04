# dlt on Dagster — Pythonic Approach

Use the **@dlt_assets** decorator and **DagsterDltResource** when your Dagster definitions live entirely in Python (no component YAML).

**Contents:** [Prerequisites](#prerequisites) · [1. Create a dlt source and pipeline](#1-create-a-dlt-source-and-pipeline) · [2. Define DagsterDltResource](#2-define-dagsterdltresource) · [3. Define @dlt_assets](#3-define-dlt_assets) · [4. Multiple dlt asset groups](#4-multiple-dlt-asset-groups) · [5. Customize asset specs (DagsterDltTranslator)](#5-customize-asset-specs-dagsterdlttranslator) · [6. Downstream assets](#6-downstream-assets)

## Prerequisites

- Dagster project with a `Definitions` object (e.g. in `definitions.py` or per-asset modules).
- `dagster-dlt` installed: `uv add dagster-dlt` or `pip install dagster-dlt`.
- Use the **Dagster project venv** (e.g. `.venv` from `uvx create-dagster project` or `create-dagster project`), not a separate dlt-only venv, so Dagster and dlt share the same environment.
- If you import a custom dlt pipeline script (e.g. your GitHub source), keep that script in the same package or path as your assets so the import resolves (e.g. `defs/assets.py` and `defs/github_pipeline.py` in the same folder).

## 1. Create a dlt source and pipeline

Your dlt code can live in the same repo (e.g. `dlt_sources/` or next to your assets). Use verified sources, REST config, or custom `@dlt.source` / `@dlt.resource`. Example with verified GitHub:

```python
from dlt_sources.github import github_reactions
import dlt

# Source instance (with any parameters your source needs)
source = github_reactions("dagster-io", "dagster", max_items=250)

# Pipeline
pipeline = dlt.pipeline(
    pipeline_name="github_issues",
    dataset_name="github",
    destination="snowflake",
    progress="log",
)
```

## 2. Define DagsterDltResource

Create a single shared resource and pass it into `Definitions`:

```python
from dagster_dlt import DagsterDltResource

dlt_resource = DagsterDltResource()
```

## 3. Define @dlt_assets

Use the `@dlt_assets` decorator with your source and pipeline; inject `DagsterDltResource` and call `run`:

```python
from dagster import AssetExecutionContext, Definitions
from dagster_dlt import DagsterDltResource, dlt_assets

@dlt_assets(
    dlt_source=github_reactions("dagster-io", "dagster", max_items=250),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="github_issues",
        dataset_name="github",
        destination="snowflake",
        progress="log",
    ),
    name="github",
    group_name="github",
)
def dagster_github_assets(context: AssetExecutionContext, dlt_resource: DagsterDltResource):
    yield from dlt_resource.run(context=context)

defs = Definitions(
    assets=[dagster_github_assets],
    resources={"dlt": DagsterDltResource()},
)
```

## 4. Multiple dlt asset groups

Define multiple `@dlt_assets` with different sources/pipelines and group names:

```python
@dlt_assets(dlt_source=..., dlt_pipeline=..., name="github", group_name="github")
def github_assets(context, dlt_resource): ...

@dlt_assets(dlt_source=..., dlt_pipeline=..., name="stripe", group_name="stripe")
def stripe_assets(context, dlt_resource): ...

defs = Definitions(
    assets=[github_assets, stripe_assets],
    resources={"dlt": DagsterDltResource()},
)
```

## 5. Customize asset specs (DagsterDltTranslator)

To change asset keys, group names, or metadata, pass a custom translator:

```python
from dagster_dlt import DagsterDltTranslator
from dagster_dlt.translator import DltResourceTranslatorData
from dagster import AssetSpec, AssetKey

class CustomTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data: DltResourceTranslatorData) -> AssetSpec:
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(key=AssetKey(data.resource.name))

@dlt_assets(..., dagster_dlt_translator=CustomTranslator())
def my_assets(context, dlt_resource): ...
```

## 6. Downstream assets

Use asset keys from the translator to declare dependencies:

```python
from dagster import asset

# Get key for a specific dlt resource if needed (see Dagster docs for full pattern)
@asset(deps=[AssetKey("github")])  # or the concrete asset key for a resource
def downstream_from_github(): ...
```

## Reference

- [Dagster & dlt (Pythonic)](https://docs.dagster.io/integrations/libraries/dlt/dlt-pythonic)
- [dagster-dlt API](https://docs.dagster.io/api/libraries/dagster-dlt)
