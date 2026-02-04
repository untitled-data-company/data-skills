# Cloud Deployment with Dagster (Serverless)

Deploy a dlt-on-Dagster project to **Dagster Cloud** so it runs in production with managed infrastructure. Serverless means Dagster manages the infrastructure; hybrid is an alternative where you manage it (see Dagster docs).

## High-level flow

1. **Deploy via Git** — Connect your Dagster project to a Git repo (e.g. GitHub). This sets up GitHub Actions (or similar) for the deployment.
2. **Tests / build** — If the pipeline (e.g. tests, build) succeeds, the code location is updated in production.
3. **Run in production** — Assets appear in Dagster Cloud; materialize them from the UI or via schedules.

## Prerequisites

- Dagster Cloud account and organization.
- Project that runs locally (e.g. `dg dev`) with assets and definitions.
- Git repo for the project (often created from Dagster Cloud’s “Add code location” flow).

## Step 1: Environment variables in Dagster Cloud

Before or after adding the code location, set environment variables in the Dagster Cloud UI (Deployment → your location → Environment variables):

- Same names as in `.env`: e.g. `SOURCES__GITHUB__ACCESS_TOKEN`, `DESTINATION__BIGQUERY__CREDENTIALS`, etc.
- For BigQuery JSON credentials: paste the **raw JSON content only** (no outer quotes). In local `.env` you may use single quotes around the JSON; in Dagster Cloud use the JSON value alone.
- For optional incremental/backfill env vars, see [secrets-and-env.md](secrets-and-env.md).

## Step 2: Repo layout for Dagster Cloud

Typical layout after “Add code location”:

- Repo root contains config files: `dagster_cloud.yaml`, `pyproject.toml` (and optionally `setup.py` / `setup.cfg` if not using pyproject-only).
- Your **Dagster project** is the folder that has `definitions.py` (or the module that builds `Definitions`) **directly inside**. That folder is what you copy into the repo (replacing any default “quickstart” folders).

So:

- Clone the repo Dagster Cloud gives you.
- Remove any default example project folders (e.g. `quickstart_etl`).
- Remove `setup.py` / `setup.cfg` if you rely only on `pyproject.toml`.
- Copy your project folder (the one containing `definitions.py`) into the repo so that `definitions.py` lives at the path you will reference in config.

## Step 3: dagster_cloud.yaml

Point the location at your project’s module and package:

```yaml
locations:
  - location_name: my_dagster_project
    code_source:
      module_name: my_dagster_project
      package_name: my_dagster_project
```

Use the same `location_name` and module/package names that match your project (e.g. the folder that has `definitions.py` and is a Python package).

## Step 4: pyproject.toml

Ensure the project and Dagster code location are correctly declared:

- `[project]`: name, version, Python version, dependencies (e.g. `dagster`, `dagster-dlt`, `dlt[bigquery]` or your destination).
- `[tool.dagster.code_locations.<location_name>]`: `module_name` and `code_location` (or equivalent) set to your project package so Dagster Cloud can load `Definitions`.

Example (conceptual):

```toml
[project]
name = "my-dagster-project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["dagster", "dagster-dlt", "dlt[bigquery]"]

[tool.dagster.code_locations.my_dagster_project]
module_name = "my_dagster_project"
code_location = "my_dagster_project"
```

Naming must match `dagster_cloud.yaml` and the actual package on disk.

## Step 5: Push and materialize

1. Commit and push to the branch Dagster Cloud watches (e.g. `main`).
2. GitHub Actions (or the configured CI) runs; on success, the code location updates in Dagster Cloud.
3. In Dagster Cloud UI: open **Deployments** → your location → **Lineage** (or Assets). Your dlt assets should appear.
4. Materialize assets (all or a subset) from the UI; check runs and logs.

## Notes

- **Parallel runs:** If you use `multi_process_executor` and `max_concurrent`, Cloud may cap concurrency (e.g. trial limits); adjust `max_concurrent` if needed.
- **Secrets:** Prefer Dagster Cloud env vars/secrets over committing `.dlt/secrets.toml` or any credentials.
- **Hybrid:** For hybrid deployment, see [Dagster hybrid deployment](https://docs.dagster.io/hybrid) in the official docs.

## Reference

- [Dagster Cloud](https://docs.dagster.io/dagster-cloud)
- [Deploy with Dagster (dlt)](https://dlthub.com/docs/walkthroughs/deploy-a-pipeline/deploy-with-dagster)
