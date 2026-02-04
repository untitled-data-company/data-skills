# Changelog

All notable changes to the **data-skills** repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

When updating: compare with the repo since the last release (e.g. `git log v0.2.0..HEAD` or `git diff v0.2.0..HEAD`) and list changes per skill or area. Keep entries short and compact.

## [Unreleased]

_Nothing yet._

## [0.2.0] - 2026-02-04

### Added
- **dlt-dagster** skill: run dlt in Dagster (Component / Pythonic @dlt_assets, standard asset, external compute → dagster-integrations). Refs: component, pythonic, secrets-env, jobs-schedules, incremental-backfill-parallel, cloud-deployment, troubleshooting. Related: dlt-skill, dagster-integrations (install commands in SKILL).

### Changed
- **README:** Single generic install command; removed per-skill examples. Added dlt-dagster to table and repo structure.
- **CHANGELOG:** Repo-wide; removed per-skill version column from README.

## [0.1.0] - 2026-01-30

### Added
- **dlt-skill:** Data pipelines with dlt (verified sources, declarative REST, custom Python). Refs: core concepts, verified sources, REST API, custom sources, incremental loading, performance, troubleshooting. Templates and scripts (install_packages, open_dashboard).
- **Repo:** README, CHANGELOG. (Later: uv skill and skills/ layout added.)

[0.2.0]: https://github.com/untitled-data-company/data-skills/releases/tag/v0.2.0
[0.1.0]: https://github.com/untitled-data-company/data-skills/releases/tag/v0.1.0
