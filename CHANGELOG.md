# Changelog

All notable changes to the **data-skills** repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_Nothing yet._

## [0.2.0] - 2026-02-04

### Added
- **dlt-dagster** skill: run dlt pipelines in Dagster (Component or Pythonic @dlt_assets, standard Dagster asset, external compute via dagster-integrations). References: component, pythonic, secrets-env, jobs-schedules, incremental-backfill-parallel, cloud-deployment, troubleshooting. Related skills: dlt-skill, dagster-integrations with install commands.

### Changed
- README: single generic installation command; removed per-skill install examples. Added dlt-dagster to Available Skills and repository structure.

## [0.1.0] - 2026-01-30

### Added
- Initial release of dlt-skill
- Support for three pipeline types:
  - Verified Sources (pre-built connectors)
  - Declarative REST API (config-based)
  - Custom Python (full control)
- Comprehensive reference documentation:
  - Core concepts
  - Verified sources guide
  - REST API source configuration
  - Custom sources with decorators
  - Incremental loading strategies
  - Performance tuning guide
  - Troubleshooting guide
- Pipeline templates for all three approaches
- Automatic package installation with dependency manager detection (uv, pip, poetry, pipenv)
- Helper scripts:
  - `install_packages.py` - Auto-detect and install dependencies
  - `open_dashboard.py` - Open dlt pipeline dashboard
- Configuration templates:
  - `.dlt/config.toml` - Non-sensitive configuration
  - `.dlt/secrets.toml` - Comprehensive credential examples for all destinations
  - `.gitignore` - Prevent committing secrets

### Features
- Expert data engineering guidance and best practices
- Decision tree for choosing pipeline approach
- Step-by-step workflow (10 steps from requirements to inspection)
- DuckDB-specific guidance (no credentials needed)
- Support for all major dlt destinations:
  - Data Warehouses: BigQuery, Snowflake, Redshift, Databricks, Synapse
  - Databases: DuckDB, ClickHouse, Postgres, SQL Server
  - Data Lakes: Delta, Iceberg, Athena
  - Vector DBs: Weaviate, LanceDB, Qdrant
  - Cloud Storage: S3, GCS, Azure Blob
- Complete authentication examples for all destinations
- Performance optimization strategies
- Incremental loading patterns

[0.2.0]: https://github.com/untitled-data-company/data-skills/releases/tag/v0.2.0
[0.1.0]: https://github.com/untitled-data-company/data-skills/releases/tag/v0.1.0
