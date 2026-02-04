# Troubleshooting dlt on Dagster

**Contents:** [Wrong venv](#wrong-venv) · [Import errors](#import-errors) · [defs.yaml / loads paths](#defsyaml--loads-paths) · [Credentials not found](#credentials-not-found)

## Wrong venv

**Symptom:** Dagster or dlt commands fail, or `dagster-dlt` not found after install.

**Fix:** Use the **Dagster project venv** (e.g. `.venv` created by `uvx create-dagster project` or `create-dagster project`), not a separate dlt-only venv. Activate it before running `dg dev` or materializing assets. Install both Dagster and dlt in that venv: `uv add dagster-dlt` (and destination extras if needed, e.g. `dlt[bigquery]`).

## Import errors

**Symptom:** `ModuleNotFoundError` when loading assets or definitions (e.g. custom dlt source or pipeline not found).

**Fix:** Ensure the dlt pipeline script (or package that defines the source) is on the Python path. For Pythonic setup, keep the dlt pipeline module in the same package or directory as your assets (e.g. `defs/assets.py` and `defs/github_pipeline.py` in the same folder). For Component setup, the scaffold puts `loads.py` under `defs/<name>/`; use relative imports (e.g. `from .github import ...`) or install the project as a package so that `defs` is a package.

## defs.yaml / loads paths

**Symptom:** Component not loading assets, or "could not resolve" source/pipeline.

**Fix:** In `defs.yaml`, `source` and `pipeline` must be **dotted Python identifiers** relative to the component module. Example: if the component is `defs/my_ingest/` and in `loads.py` you have `my_source = ...` and `my_pipeline = ...`, use `source: .loads.my_source` and `pipeline: .loads.my_pipeline`. The leading `.` is the component module; `loads` is the `loads.py` submodule. Run from the project root where Dagster loads definitions (e.g. `my-project/src`).

## Credentials not found

**Symptom:** dlt fails with missing credentials for source or destination.

**Fix:** When running under Dagster, use **environment variables** (see [secrets-and-env.md](secrets-and-env.md)). Ensure the same env vars are set in the process that runs Dagster (e.g. `dg dev` loads `.env` from the project root; Dagster Cloud uses the deployment’s environment variables). Names must match dlt’s convention: `SOURCES__<NAME>__<KEY>`, `DESTINATION__<NAME>__CREDENTIALS__<KEY>`, etc. No `.dlt/secrets.toml` is required if all credentials are in env.
