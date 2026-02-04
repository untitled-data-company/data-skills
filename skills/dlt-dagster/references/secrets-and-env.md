# Secrets and Environment Variables for dlt in Dagster

dlt reads credentials from [configuration and secrets](https://dlthub.com/docs/general-usage/credentials/configuration). When running under Dagster, use **environment variables** so the same deployment config drives both Dagster and dlt.

## Why environment variables

- One place to configure secrets (Dagster deployment env or secrets backend).
- No need to ship `.dlt/secrets.toml` in production.
- dlt natively supports env vars with the same naming as in TOML.

## Naming convention

dlt maps TOML keys to env vars: sections and keys are uppercased and joined with double underscores.

Pattern: `SOURCES__<SOURCE_NAME>__<KEY>` and `DESTINATION__<DESTINATION_NAME>__CREDENTIALS__<KEY>`.

Examples:

| TOML (secrets.toml)              | Environment variable                          |
|----------------------------------|-----------------------------------------------|
| `[sources.github]` / `access_token` | `SOURCES__GITHUB__ACCESS_TOKEN`              |
| `[destination.snowflake.credentials]` / `database` | `DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE` |
| same / `password`                 | `DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD` |
| same / `username`                | `DESTINATION__SNOWFLAKE__CREDENTIALS__USERNAME` |
| same / `warehouse`               | `DESTINATION__SNOWFLAKE__CREDENTIALS__WAREHOUSE` |
| same / `role`                    | `DESTINATION__SNOWFLAKE__CREDENTIALS__ROLE`   |
| same / `host`                    | `DESTINATION__SNOWFLAKE__CREDENTIALS__HOST`   |

For BigQuery, DuckDB, etc., use the same pattern: `DESTINATION__<NAME>__CREDENTIALS__...` (or the keys documented for that destination).

## BigQuery: single env var with full JSON

Instead of separate env vars for `project_id`, `private_key`, `client_email`, you can set one variable to the **entire JSON** credentials object:

- **Env var name:** `DESTINATION__BIGQUERY__CREDENTIALS`
- **Value:** The full JSON (e.g. service account key). In a local `.env` file use single quotes around the JSON so the inner double quotes don’t break parsing; in Dagster Cloud / UI, paste the raw JSON content only (no outer quotes).

## Optional: incremental and backfill env vars

If you drive incremental or backfill from env (see [incremental-backfill-parallel.md](incremental-backfill-parallel.md)), add vars such as:

- `ISSUES_INITIAL_VALUE` — initial cursor for incremental (e.g. issues).
- `FORKS_INITIAL_VALUE`, `FORKS_END_VALUE` — for optional backfill; leave unset to skip backfill.

## Where to set them

- **Local:** `.env` in the project root or export in the shell; ensure Dagster (e.g. `dg dev`) loads that env.
- **Dagster Cloud / production:** Use the deployment’s environment variables or secrets management; Dagster and dlt will both read from the process env.

## Optional: keep .dlt for local dev

You can still use `.dlt/secrets.toml` locally; do not commit it and add `.dlt/secrets.toml` to `.gitignore`. In production, rely on env vars only.

## Reference

- [dlt credentials and configuration](https://dlthub.com/docs/general-usage/credentials/configuration)
