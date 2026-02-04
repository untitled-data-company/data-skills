# Jobs and Schedules for dlt Assets in Dagster

After defining dlt assets (Component or Pythonic), you can materialize them via **jobs** and run those jobs on a **schedule**.

## Asset jobs

Define a job that selects your dlt assets (by name, group, or tags), then run it from the UI or via the API.

**Pythonic example:**

```python
from dagster import define_asset_job, Definitions

dagster_github_assets_job = define_asset_job(
    name="dagster_github_assets_job",
    selection=[dagster_github_assets],
)

defs = Definitions(
    assets=[dagster_github_assets],
    jobs=[dagster_github_assets_job],
    resources={"dlt": DagsterDltResource()},
)
```

For Component-defined assets, reference the same assets in a job (e.g. by group or asset key) in your codebase’s `Definitions` or in the same component system your project uses.

## Schedules

Attach a schedule to the job so it runs on a cron (or other schedule type):

```python
from dagster import ScheduleDefinition

dagster_github_assets_schedule = ScheduleDefinition(
    job=dagster_github_assets_job,
    cron_schedule="0 0 * * *",  # daily at midnight
)

defs = Definitions(
    assets=[dagster_github_assets],
    jobs=[dagster_github_assets_job],
    schedules=[dagster_github_assets_schedule],
    resources={"dlt": DagsterDltResource()},
)
```

## Multiple dlt asset groups

To run different dlt pipelines on different schedules, define separate jobs and schedules:

```python
github_job = define_asset_job(name="github_ingest", selection=[github_assets])
stripe_job = define_asset_job(name="stripe_ingest", selection=[stripe_assets])

defs = Definitions(
    assets=[github_assets, stripe_assets],
    jobs=[github_job, stripe_job],
    schedules=[
        ScheduleDefinition(job=github_job, cron_schedule="0 */6 * * *"),
        ScheduleDefinition(job=stripe_job, cron_schedule="0 2 * * *"),
    ],
    resources={"dlt": DagsterDltResource()},
)
```

## Reference

- [Dagster jobs](https://docs.dagster.io/concepts/ops-jobs-graphs/jobs)
- [Dagster schedules](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules)
