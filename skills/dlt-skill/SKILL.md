---
name: dlt-skill
description: >
  Expert assistant for creating and maintaining dlt (data load tool) data pipelines.
  Use this skill when users want to create data ingestion pipelines from APIs, databases,
  or other sources; set up pipelines using dlt verified sources (Salesforce, GitHub, Stripe);
  build declarative REST API pipelines; write custom Python-based data extraction pipelines;
  configure dlt destinations (DuckDB, BigQuery, Snowflake); implement incremental loading
  strategies; optimize pipeline performance; debug or troubleshoot dlt pipelines; create
  or modify .dlt/config.toml and .dlt/secrets.toml files; or open the dlt pipeline dashboard
  for inspection. This skill acts as an expert data engineer providing best practices and guidance.
---

# dlt Pipeline Creator

## Overview

This skill helps create and maintain data pipelines using dlt (data load tool from dlthub.com). It provides expert guidance on pipeline architecture, configuration, and best practices for extracting data from various sources and loading it into destinations.

## Pipeline Type Decision Tree

When a user requests a dlt pipeline, determine which type to create:

```
START: User wants to create a dlt pipeline
│
├─→ Is there a dlt verified source available for this platform?
│   (Check: https://dlthub.com/docs/dlt-ecosystem/verified-sources)
│   │
│   YES → Use VERIFIED SOURCE approach
│   │     Examples: Salesforce, GitHub, Stripe, HubSpot, Slack
│   │     Action: Guide user through `dlt init <source> <destination>`
│   │
│   NO → Continue to next question
│
├─→ Is this a REST API with standard patterns?
│   (Standard auth, pagination, JSON responses)
│   │
│   YES → Use DECLARATIVE REST API approach
│   │     Examples: Pokemon API, simple REST APIs with clear endpoints
│   │     Action: Create config-based pipeline with rest_api_source
│   │
│   NO → Continue to next question
│
└─→ Does this require custom logic or Python packages?
    │
    YES → Use CUSTOM PYTHON approach
          Examples: Python packages (simple-salesforce), complex transformations,
                   non-standard APIs, custom data sources
          Action: Create custom source with @dlt.source and @dlt.resource decorators
```

## Core Workflow

### 1. Understand Requirements

Ask clarifying questions:
- **Source**: What is the data source? (API URL, platform name, database, etc.)
- **Source type**: Does this match a verified source, REST API, or require custom code?
- **Destination**: Where should data be loaded? (DuckDB, BigQuery, Snowflake, etc.)
- **Resources**: What specific data/endpoints are needed?
- **Incremental**: Should the pipeline load incrementally or do full refreshes?
- **Authentication**: What credentials are required?

### 2. Choose Pipeline Approach

Based on the decision tree above, select:
- **Verified Source** - Pre-built, tested connector
- **Declarative REST API** - Config-based REST API pipeline
- **Custom Python** - Full control with Python code

### 3. Initialize or Create Pipeline

#### Verified Source
```bash
dlt init <source_name> <destination_name>
```
Examples:
- `dlt init salesforce bigquery`
- `dlt init github duckdb`
- `dlt init stripe snowflake`

#### Declarative REST API or Custom Python
Use appropriate template from [assets/templates/](assets/templates/):
- `declarative_rest_pipeline.py` - For REST APIs
- `custom_python_pipeline.py` - For custom sources

### 4. Install Required Packages

Install dlt and destination-specific packages. The skill automatically detects the project's dependency manager (uv, pip, poetry, pipenv) or asks the user which to use.

**Use the helper script:**
```bash
python scripts/install_packages.py --destination <destination_name>
```

**Examples:**
```bash
# For BigQuery
python scripts/install_packages.py --destination bigquery

# For DuckDB (default, no extra dependencies needed)
python scripts/install_packages.py --destination duckdb

# For Snowflake
python scripts/install_packages.py --destination snowflake
```

**What gets installed:**
- `dlt[destination,workspace]` - dlt with destination-specific extras and dashboard support

**Manual installation** (if preferred):
```bash
# Using pip (for BigQuery destination)
pip install "dlt[bigquery,workspace]"

# Using uv (for BigQuery destination)
uv add "dlt[bigquery,workspace]"

# Using poetry (for BigQuery destination)
poetry add "dlt[bigquery,workspace]"

# For DuckDB (workspace only, duckdb is included by default)
pip install "dlt[workspace]"
uv add "dlt[workspace]"
poetry add "dlt[workspace]"
```

**Important**: The `workspace` extra is **required** for `dlt pipeline <name> show` and dashboard functionality. Always include it in your installation.

**Note**: DuckDB support is included by default in dlt, so only the `workspace` extra is needed for DuckDB destinations.

### 5. Configure Credentials

Create or update `.dlt/secrets.toml`:

**Structure:**
```toml
[sources.<source_name>]
# Source credentials here

[destination.<destination_name>]
# Destination credentials here
```

Use the template: [assets/templates/.dlt/secrets.toml](assets/templates/.dlt/secrets.toml)

**Important**: Remind user to add `.dlt/secrets.toml` to `.gitignore`!

**Note for DuckDB**: DuckDB doesn't require credentials in secrets.toml. Just specify the database file path in the pipeline or config.toml.

### 6. Configure Pipeline Settings

Create or update `.dlt/config.toml` for non-sensitive settings:

```toml
[sources.<source_name>]
base_url = "https://api.example.com"
timeout = 30

[destination.<destination_name>]
location = "US"
```

Use the template: [assets/templates/.dlt/config.toml](assets/templates/.dlt/config.toml)

### 7. Implement Pipeline Logic

Flesh out the pipeline code based on requirements:

**For Verified Sources**:
- Customize resource selection with `.with_resources()`
- Configure incremental loading with `.apply_hints()`
- See: [references/verified-sources.md](references/verified-sources.md)

**For Declarative REST API**:
- Define client configuration (base_url, auth)
- Configure resources and endpoints
- Set up pagination and incremental loading
- See: [references/rest-api-source.md](references/rest-api-source.md)

**For Custom Python**:
- Implement `@dlt.source` and `@dlt.resource` functions
- Use generators and yield patterns
- Configure write dispositions and primary keys
- See: [references/custom-sources.md](references/custom-sources.md)

### 8. Configure Incremental Loading (If Needed)

For pipelines that should load only new/changed data:
- Identify cursor field (timestamp, ID)
- Set write disposition to `merge`
- Define primary key for deduplication
- Configure incremental parameters

See: [references/incremental-loading.md](references/incremental-loading.md)

### 9. Test and Run Pipeline

```python
python <pipeline_file>.py
```

Check for errors and verify data is loaded correctly.

### 10. Inspect Results

**Prerequisite**: Ensure `dlt[workspace]` is installed (included by default when using `install_packages.py`).

Open the dlt dashboard to inspect loaded data:
```bash
dlt pipeline <pipeline_name> show
```

Or use the helper script:
```bash
python scripts/open_dashboard.py <pipeline_name>
```

## Pipeline Patterns

### Pattern 1: Verified Source - Select Specific Resources

```python
from salesforce import salesforce_source

source = salesforce_source()
pipeline = dlt.pipeline(
    pipeline_name='salesforce_pipeline',
    destination='bigquery',
    dataset_name='salesforce_data'
)

# Load only specific Salesforce objects
pipeline.run(source.with_resources("Account", "Opportunity", "Contact"))
```

### Pattern 2: Declarative REST API - Simple Endpoints

```python
from dlt.sources.rest_api import rest_api_source

config = {
    "client": {
        "base_url": "https://pokeapi.co/api/v2/",
    },
    "resources": [
        "pokemon",
        {
            "name": "pokemon_details",
            "endpoint": "pokemon/{name}",
            "write_disposition": "merge",
            "primary_key": "id"
        }
    ]
}

pipeline = dlt.pipeline(
    pipeline_name="pokemon",
    destination="duckdb",
    dataset_name="pokemon_data"
)
pipeline.run(rest_api_source(config))
```

### Pattern 3: Custom Python - Using Python Package

```python
import dlt
from simple_salesforce import Salesforce

@dlt.source
def salesforce_custom(username=dlt.secrets.value, password=dlt.secrets.value):
    sf = Salesforce(username=username, password=password)

    @dlt.resource(write_disposition='merge', primary_key='Id')
    def accounts():
        records = sf.query_all("SELECT Id, Name FROM Account")
        yield records['records']

    return accounts

pipeline = dlt.pipeline(
    pipeline_name='salesforce_custom',
    destination='duckdb',
    dataset_name='salesforce'
)
pipeline.run(salesforce_custom())
```

### Pattern 4: Incremental Loading with REST API

```python
config = {
    "client": {
        "base_url": "https://api.github.com/repos/dlt-hub/dlt/",
        "auth": {"token": dlt.secrets["github_token"]}
    },
    "resources": [
        {
            "name": "issues",
            "endpoint": {
                "path": "issues",
                "params": {
                    "state": "all",
                    "since": "{incremental.start_value}"
                }
            },
            "incremental": {
                "cursor_path": "updated_at",
                "initial_value": "2024-01-01T00:00:00Z"
            },
            "write_disposition": "merge",
            "primary_key": "id"
        }
    ]
}
```

## Best Practices as an Expert Data Engineer

### 1. Security
- **Never hardcode credentials** - Always use `.dlt/secrets.toml`
- **Add secrets to .gitignore** - Provide `.gitignore` template
- **Use environment-specific configs** - Separate dev/prod configurations

### 2. Data Quality
- **Set primary keys** - Essential for merge operations and deduplication
- **Use appropriate write dispositions**:
  - `append` for immutable event data
  - `merge` for stateful data that changes
  - `replace` for full snapshots
- **Validate data** - Check for required fields before yielding

### 3. Performance
- **Yield pages, not individual items** - Reduces pipeline overhead
- **Configure parallelism** - Adjust workers for extract/normalize/load stages
- **Enable file rotation** - For large datasets (millions+ records)
- **Use incremental loading** - Reduce data transfer and API calls

See: [references/performance-tuning.md](references/performance-tuning.md)

### 4. Maintainability
- **Document pipeline purpose** - Add docstrings to sources and resources
- **Use descriptive names** - Clear pipeline, resource, and table names
- **Follow dlt patterns** - Use decorators and generators correctly
- **Handle errors gracefully** - Add try-except blocks for API calls

### 5. Incremental Loading Strategy
- **Choose the right cursor** - Timestamps usually better than IDs
- **Handle late data** - Use lag windows when needed
- **Test incremental logic** - Verify no data is missed or duplicated
- **Plan for full refreshes** - Document how to reset state

### 6. API Considerations
- **Respect rate limits** - Add delays or reduce parallelism if needed
- **Handle pagination correctly** - Test with multiple pages
- **Implement retries** - For transient failures
- **Monitor API changes** - APIs evolve, pipelines need updates

## Common Challenges and Solutions

### Challenge: Complex API Authentication

**Solution**: For declarative REST API:
```python
# OAuth2
"auth": {
    "type": "oauth2_client_credentials",
    "client_id": dlt.secrets["client_id"],
    "client_secret": dlt.secrets["client_secret"],
    "access_token_url": "https://auth.example.com/oauth/token"
}
```

For custom Python, implement auth in requests:
```python
from dlt.sources.helpers.rest_client import paginate
from dlt.sources.helpers.rest_client.auth import OAuth2ClientCredentials

auth = OAuth2ClientCredentials(
    client_id=dlt.secrets["client_id"],
    client_secret=dlt.secrets["client_secret"],
    access_token_url="https://auth.example.com/oauth/token"
)

for page in paginate(url, auth=auth):
    yield page
```

See: [references/rest-api-source.md](references/rest-api-source.md) for more auth patterns

### Challenge: Custom Pagination Logic

**Solution**: Use custom Python for non-standard pagination:
```python
@dlt.resource
def custom_paginated_resource():
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}")
        data = response.json()

        if not data:  # No more data
            break

        yield data
        page += 1
```

### Challenge: Nested/Complex Data Structures

**Solution**: Control table nesting:
```python
@dlt.source(max_table_nesting=2)  # Limit nested table depth
def my_source():
    return my_resource()
```

Or flatten data manually before yielding.

### Challenge: Performance with Large Datasets

**Solution**: See [references/performance-tuning.md](references/performance-tuning.md)

Key optimizations:
- Increase worker counts
- Enable file rotation
- Yield pages instead of rows
- Use appropriate buffer sizes

## Reference Documentation

This skill includes comprehensive reference documentation:

- **[core-concepts.md](references/core-concepts.md)** - dlt fundamentals, sources, resources, destinations
- **[verified-sources.md](references/verified-sources.md)** - Using pre-built verified sources
- **[rest-api-source.md](references/rest-api-source.md)** - Declarative REST API configuration
- **[custom-sources.md](references/custom-sources.md)** - Creating custom Python sources
- **[incremental-loading.md](references/incremental-loading.md)** - Incremental loading strategies
- **[performance-tuning.md](references/performance-tuning.md)** - Performance optimization
- **[troubleshooting.md](references/troubleshooting.md)** - Common issues and solutions

Read these files when needed for detailed information on specific topics.

## Templates and Scripts

### Templates (assets/templates/)

- **[custom_python_pipeline.py](assets/templates/custom_python_pipeline.py)** - Custom Python pipeline skeleton
- **[verified_source_pipeline.py](assets/templates/verified_source_pipeline.py)** - Verified source pipeline skeleton
- **[declarative_rest_pipeline.py](assets/templates/declarative_rest_pipeline.py)** - Declarative REST API pipeline skeleton
- **[.dlt/config.toml](assets/templates/.dlt/config.toml)** - Configuration file template
- **[.dlt/secrets.toml](assets/templates/.dlt/secrets.toml)** - Secrets file template
- **[.gitignore](assets/templates/.gitignore)** - Git ignore template for dlt projects

### Scripts (scripts/)

- **[install_packages.py](scripts/install_packages.py)** - Automatically install dlt packages with dependency manager detection (includes `workspace` extra by default)
- **[open_dashboard.py](scripts/open_dashboard.py)** - Helper to open dlt pipeline dashboard (requires `dlt[workspace]`)

## Workflow Example: Creating a Pokemon API Pipeline

**User request**: "Create a pipeline ingesting data from https://pokeapi.co/api/v2/pokemon/ and https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

**Step-by-step:**

1. **Analyze**: REST API with standard patterns → Use declarative approach
2. **Destination**: Ask user (assume DuckDB for this example)
3. **Create pipeline** using declarative REST template
4. **Configure**:
   ```python
   config = {
       "client": {"base_url": "https://pokeapi.co/api/v2/"},
       "resources": [
           {
               "name": "pokemon_list",
               "endpoint": "pokemon",
               "write_disposition": "replace"
           },
           {
               "name": "pokemon_details",
               "endpoint": "pokemon/{name}",
               "write_disposition": "merge",
               "primary_key": "id",
               "include_from_parent": ["name"]
           }
       ]
   }
   ```
5. **No secrets needed** (public API)
6. **Create pipeline code** with config
7. **Test**: Run pipeline
8. **Inspect**: Open dashboard to verify data

## Key Reminders
- **Always ask about destination** - Don't assume
- **Security first** - Never commit secrets; use `.dlt/secrets.toml` and provide `.gitignore`
- **Start simple** - Use verified sources when available; test incrementally
- **Read references** - Load detailed docs only when needed
