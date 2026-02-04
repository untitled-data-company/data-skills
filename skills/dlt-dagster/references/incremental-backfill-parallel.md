# Incremental Loading, Backfilling, and Parallelization

Use dynamic config (env vars + `apply_hints`) for incremental and backfill, and one-asset-per-resource with a multi-process executor for parallel runs.

**Contents:** [Dynamic incremental loading](#dynamic-incremental-loading) · [Dynamic backfilling](#dynamic-backfilling) · [Parallelization (one asset per resource)](#parallelization-one-asset-per-resource) · [Summary](#summary)

## Dynamic incremental loading

Avoid hardcoding `initial_value` in the dlt source. Override at runtime with **apply_hints** and environment variables.

1. In your assets (or loads) code, after creating the source, call `source.<resource_name>.apply_hints(...)`.
2. Use `dlt.sources.incremental("cursor_path", initial_value=os.getenv("MY_INITIAL_VALUE", "1970-01-01T00:00:00Z"))` for the incremental config.
3. Set the env var (e.g. `ISSUES_INITIAL_VALUE`) in `.env` or Dagster Cloud; change it without editing code.

Example (Pythonic):

```python
import os
import dlt
from dagster_dlt import DagsterDltResource, dlt_assets

source = github_source()  # your dlt source
# Override incremental for "issues" from env
source.issues.apply_hints(
    incremental=dlt.sources.incremental(
        "updated_at",
        initial_value=os.getenv("ISSUES_INITIAL_VALUE", "1970-01-01T00:00:00Z"),
    ),
)

@dlt_assets(dlt_source=source, dlt_pipeline=pipeline, ...)
def dagster_github_assets(context, dlt_resource: DagsterDltResource):
    yield from dlt_resource.run(context=context)
```

## Dynamic backfilling

Backfill is a time-window load (initial_value + end_value, row_order). Make it optional so it only runs when you set env vars.

1. Use `apply_hints` with `incremental=dlt.sources.incremental(..., initial_value=..., end_value=..., row_order="ASC")`.
2. Read initial_value and end_value from env (e.g. `FORKS_INITIAL_VALUE`, `FORKS_END_VALUE`) with empty string default.
3. Only call `apply_hints` for the backfill resource when both env vars are set (e.g. `if os.getenv("FORKS_INITIAL_VALUE") and os.getenv("FORKS_END_VALUE"): source.forks.apply_hints(...)`).

Example:

```python
forks_initial = os.getenv("FORKS_INITIAL_VALUE", "")
forks_end = os.getenv("FORKS_END_VALUE", "")
if forks_initial and forks_end:
    source.forks.apply_hints(
        incremental=dlt.sources.incremental(
            "cursor_path",
            initial_value=forks_initial,
            end_value=forks_end,
            row_order="ASC",
        ),
    )
```

Result: normal runs use only incremental; backfill runs when you set the two env vars.

## Parallelization (one asset per resource)

To run multiple dlt resources **concurrently** instead of sequentially:

1. **One Dagster asset per dlt resource** — Use a factory that, for each resource name, returns a `@dlt_assets`-decorated function with:
   - **Source:** `source.with_resources(resource_name)` so only that resource is loaded.
   - **Pipeline:** a pipeline with a **unique name** per resource (e.g. `pipeline_name + "_" + resource_name`). Different pipeline names keep dlt state separate and avoid interference.
2. **Register all assets** — Build a list, e.g. `parallel_assets = [make_resource_asset(r) for r in resource_names]`, and pass that list to `Definitions(assets=parallel_assets)`.
3. **Enable parallel execution** — In `define_asset_job`, set `executor_def=multi_process_executor` and `config={"max_concurrent": N}` (e.g. N = number of resources).

Example factory (Pythonic):

```python
from dagster import define_asset_job, Definitions
from dagster.executors import multi_process_executor

def make_resource_asset(resource_name: str):
    @dlt_assets(
        dlt_source=source.with_resources(resource_name),
        dlt_pipeline=dlt.pipeline(
            pipeline_name=f"github_issues_{resource_name}",
            dataset_name="github",
            destination="bigquery",
            progress="log",
        ),
        name=f"github_{resource_name}",
        group_name="github",
    )
    def asset_fn(context, dlt_resource: DagsterDltResource):
        yield from dlt_resource.run(context=context)
    return asset_fn

resource_names = ["issues", "pull_requests", "repos", "forks", "stargazers"]
parallel_assets = [make_resource_asset(r) for r in resource_names]

github_job = define_asset_job(
    name="github_job",
    selection=parallel_assets,
    executor_def=multi_process_executor,
    config={"max_concurrent": 5},
)

defs = Definitions(
    assets=parallel_assets,
    jobs=[github_job],
    resources={"dlt": DagsterDltResource()},
)
```

In the Dagster UI, materializing the job will run the dlt resources in parallel (up to `max_concurrent`).

## Summary

- **Incremental:** Use env vars for `initial_value` and override with `apply_hints` so you can change the cursor without editing code.
- **Backfill:** Use env vars for initial/end and only apply hints when both are set; leave unset for normal incremental runs.
- **Parallel:** One asset per resource, `source.with_resources(name)`, unique pipeline name per resource, and `multi_process_executor` with `max_concurrent`.
