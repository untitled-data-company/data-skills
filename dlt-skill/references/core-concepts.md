# dlt Core Concepts

## What is dlt?

dlt is an open-source Python library that loads data from various data sources into well-structured datasets. It emphasizes being easy to use, flexible, and scalable while providing lightweight interfaces for data extraction, loading, inspection, and transformation.

## Core Components

### Sources
Sources extract data from multiple origins including REST APIs, SQL databases, cloud storage systems, and Python data structures. A source is a function decorated with `@dlt.source` that returns one or more resources.

**Key principles:**
- Sources should NOT extract data directly - leave that to resources
- Sources should yield or return resources
- Avoid heavy operations in source functions

### Resources
Resources are the actual data extraction units. They can be:
- Functions decorated with `@dlt.resource`
- Created dynamically using `dlt.resource()` as a function call
- Yielded from source functions

### Destinations
dlt supports various destinations including:
- **Data Warehouses**: BigQuery, Snowflake, Redshift, Databricks, Azure Synapse
- **Databases**: DuckDB, ClickHouse, Postgres, SQL Server
- **Data Lakes**: Delta, Iceberg, Athena/Glue
- **Vector Databases**: Weaviate, LanceDB, Qdrant
- **Storage**: S3, GCS, Azure Blob, filesystem
- **Custom**: Create custom destinations with `@dlt.destination` decorator

### Pipelines
A pipeline orchestrates the data movement process, connecting sources to destinations:

```python
pipeline = dlt.pipeline(
    pipeline_name='my_pipeline',
    destination='duckdb',
    dataset_name='my_data'
)
load_info = pipeline.run(my_source())
```

## Key Capabilities

### Schema Management
- Automatic schema inference
- Data type detection
- Data normalization
- Nested structure handling
- Schema evolution support

### Pipeline Automation
- Incremental loading
- Schema evolution
- Schema and data contracts
- Reduced maintenance overhead

### Data Access
- Python and SQL queries
- Transformations
- Pipeline inspection
- Visualization support

## Basic Workflow

1. Define data sources (verified, custom, or declarative)
2. Configure extraction parameters
3. Create pipeline instance specifying destination
4. Execute pipeline to load transformed data
5. Inspect and query loaded data

## Configuration

### Directory Structure
When you run `dlt init <source> <destination>`, it creates:
- Pipeline Python file
- `.dlt/` directory for configuration
- `requirements.txt` for dependencies

### Config and Secrets
- `.dlt/config.toml` - Non-sensitive configuration
- `.dlt/secrets.toml` - Sensitive credentials (never commit!)

Example secrets structure:
```toml
[sources]
api_secret_key = '<your-api-key>'

[destination.bigquery]
credentials = '<path-to-service-account.json>'
```

**Note**: DuckDB doesn't require credentials - just specify the file path in `.dlt/config.toml` or directly in the pipeline destination parameter.

Secret names correspond to argument names in source functions, enabling automatic credential injection.

## Write Dispositions

Control how data is written to destinations:

1. **replace** - Full load, overwrites existing data
2. **append** - Adds new data without modifying existing records
3. **merge** - Updates existing records using merge/primary keys (upserts)

## Data Inspection

After loading data:
```bash
dlt pipeline <pipeline_name> show
```

This opens the pipeline visualization/dashboard for debugging and inspection.
