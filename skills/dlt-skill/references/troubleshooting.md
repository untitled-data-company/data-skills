# Troubleshooting dlt Pipelines

## Table of Contents
- [Installation and Setup](#installation-and-setup)
- [Configuration and Secrets](#configuration-and-secrets)
- [Pipeline Execution](#pipeline-execution)
- [Incremental Loading](#incremental-loading)
- [REST API Source](#rest-api-source)
- [Performance Issues](#performance-issues)
- [Destination-Specific Issues](#destination-specific-issues)
- [Data Quality Issues](#data-quality-issues)
- [Debugging Techniques](#debugging-techniques)
- [Getting Help](#getting-help)
- [Error Message Reference](#error-message-reference)

## Common Issues and Solutions

### Installation and Setup

#### ModuleNotFoundError: No module named 'dlt'
```bash
# Install dlt
pip install dlt

# Install with specific destination support
pip install dlt[duckdb]
pip install dlt[bigquery]
pip install dlt[snowflake]
```

#### dlt init fails
```bash
# Ensure you're in a Python environment
python --version  # Should show Python 3.8+

# Update dlt to latest version
pip install --upgrade dlt

# Check available sources
dlt init --list-sources
```

### Configuration and Secrets

#### Credentials not found
**Problem**: `KeyError` or `ConfigFieldMissingException`

**Solution**:
1. Check `.dlt/secrets.toml` exists and has correct structure
2. Verify secret names match function parameters exactly
3. Ensure secrets are under correct section

```toml
# Correct structure
[sources.my_source]
api_key = "your-key"

# NOT
[my_source]  # Missing 'sources.' prefix
api_key = "your-key"
```

#### Secrets in wrong location
**Problem**: Secrets not being loaded

**Solution**:
- Secrets belong in `.dlt/secrets.toml` (never commit!)
- Config belongs in `.dlt/config.toml`
- Check file is in project root or `.dlt/` directory

### Pipeline Execution

#### Pipeline runs but loads no data
**Checklist**:
1. Resource function is actually yielding data: Add `print()` statements
2. Data selector is correct (for REST API source)
3. API authentication is working: Check API response
4. Resource is included in pipeline run

```python
# Debug: Print what's being yielded
@dlt.resource
def my_resource():
    data = fetch_data()
    print(f"Fetched {len(data)} items")  # Debug
    yield data

# Ensure resource is actually run
pipeline.run(source())  # Not just source
```

#### Schema inference issues
**Problem**: Incorrect data types or table structure

**Solution**:
```python
# Explicitly set hints
@dlt.resource(
    columns={"id": {"data_type": "bigint"}},
    primary_key="id"
)
def my_resource():
    yield data

# Or in table_schema
@dlt.resource(
    table_schema={
        "columns": {
            "created_at": {"data_type": "timestamp"},
            "amount": {"data_type": "decimal"}
        }
    }
)
```

#### Data type conversion errors
**Problem**: `ValueError` or destination-specific type errors

**Solution**:
- Check source data types match destination capabilities
- Convert data before yielding
- Use dlt data type hints

```python
from datetime import datetime

@dlt.resource
def my_resource():
    data = fetch_data()
    for item in data:
        # Convert string to datetime
        if isinstance(item['date'], str):
            item['date'] = datetime.fromisoformat(item['date'])
        yield item
```

### Incremental Loading

#### Incremental cursor not advancing
**Problem**: Pipeline reloads same data every run

**Checklist**:
1. Cursor field exists in data
2. Cursor field is monotonically increasing
3. Write disposition is correct (usually `merge`)
4. Primary key is set for merge operations

```python
# Correct incremental setup
@dlt.resource(
    write_disposition='merge',  # Required for incremental
    primary_key='id'            # Required for merge
)
def my_resource(
    updated_at=dlt.sources.incremental('updated_at', initial_value='2024-01-01T00:00:00Z')
):
    # Use cursor in API call
    data = fetch_data(since=updated_at.last_value)
    yield data
```

#### Incremental state reset needed
**Problem**: Need to reload all data

**Solution**:
```bash
# Drop state and reload
python pipeline.py --refresh drop_sources

# Or in code
pipeline.run(source(), refresh='drop_sources')
```

### REST API Source

#### Pipeline context conflicts with dlt.attach()

**Problem:** Using `dlt.attach()` inside a resource that runs within another pipeline causes `ContainerInjectableContextMangled` (or similar pipeline context) errors. The same can happen when opening a dlt-managed or pipeline-associated connection from inside a resource that is part of a different pipeline.

**Solution:** Read data **before** creating or running the pipeline, using direct database connections (no dlt context):

```python
import duckdb

def get_data_from_other_pipeline():
    """Read outside of dlt context to avoid conflicts."""
    conn = duckdb.connect("other_pipeline.duckdb", read_only=True)
    result = conn.execute("SELECT * FROM my_table").fetchall()
    conn.close()
    return result

# Then use the data in your pipeline
data = get_data_from_other_pipeline()
pipeline = dlt.pipeline(...)
pipeline.run(my_source(data))
```

Use this pattern when a REST API source is seeded from another pipeline’s database: load the seed data in a plain function with a direct DB connection, then pass that data into your seed resource so no `dlt.attach()` or pipeline context is used during extraction.

#### Authentication failing
**Checklist**:
1. Correct auth type for the API
2. Credentials in `.dlt/secrets.toml`
3. Token/key is valid and not expired
4. Auth is in correct location (header vs query)

```python
# Test credentials separately
import requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(url, headers=headers)
print(response.status_code)  # Should be 200
```

#### Pagination not working
**Problem**: Only getting first page of results

**Solutions**:
```python
# 1. Let dlt auto-detect (usually works)
"endpoint": "users"

# 2. Explicitly configure paginator
"endpoint": {
    "path": "users",
    "paginator": {
        "type": "page_number",
        "page_param": "page",
        "page_size": 100
    }
}

# 3. Check API response structure
# Add data_selector if data is nested
"endpoint": {
    "path": "users",
    "data_selector": "data.results"  # Adjust to your API
}
```

#### Parent-child resources not linking
**Problem**: Child resources not loading data

**Solution**:
```python
# Ensure parent has required fields
{
    "name": "parent",
    "endpoint": "parents",
    "primary_key": "id"  # Make sure this exists in data
},
{
    "name": "child",
    "endpoint": "parents/{id}/children",  # Use field from parent
    "include_from_parent": ["id"]         # Must match placeholder
}
```

### Performance Issues

#### Pipeline is slow
**Diagnosis**:
```bash
# Run with progress logging
PROGRESS=log python pipeline.py
```

**Solutions**:
1. **Increase parallelism**:
```toml
[extract]
workers = 10

[load]
workers = 50
```

2. **Enable file rotation** for large datasets:
```toml
[data_writer]
file_max_items = 100000
```

3. **Yield pages, not rows**:
```python
# Good
yield response.json()  # Entire page

# Bad
for item in response.json():
    yield item  # Individual items
```

#### Memory issues
**Problem**: `MemoryError` or system running out of RAM

**Solutions**:
```toml
# Reduce buffer size
[data_writer]
buffer_max_items = 1000

# Use external storage
[runtime]
data_dir = "/path/to/external/storage"
```

```python
# In code
import os
os.environ["DLT_DATA_DIR"] = "/mnt/external/storage"
```

### Destination-Specific Issues

#### BigQuery: 403 Forbidden
- Check credentials file path is correct
- Verify service account has necessary permissions
- Ensure project ID is correct

#### DuckDB: Database locked
- Close other connections to the database
- Use `read_only=False` in destination config
- Ensure no other processes are accessing the file

#### Snowflake: Connection timeout
- Check network connectivity
- Verify account identifier is correct
- Ensure credentials are valid

### Data Quality Issues

#### Duplicate records
**Causes**:
- Missing primary key
- Wrong write disposition
- Incremental cursor issues

**Solutions**:
```python
# Ensure primary key is set
@dlt.resource(
    write_disposition='merge',
    primary_key='id'  # Or composite: ['id', 'timestamp']
)

# Or deduplicate manually
@dlt.resource
def deduped_resource():
    data = fetch_data()
    seen = set()
    for item in data:
        if item['id'] not in seen:
            seen.add(item['id'])
            yield item
```

#### Missing fields
**Problem**: Expected fields not in destination

**Diagnosis**:
- Check source data actually contains the fields
- Verify data selector for REST API sources
- Check schema inference

**Solution**:
```python
# Validate data before yielding
@dlt.resource
def validated_resource():
    data = fetch_data()
    for item in data:
        # Ensure required fields exist
        assert 'id' in item, f"Missing id in {item}"
        assert 'name' in item, f"Missing name in {item}"
        yield item
```

### Debugging Techniques

#### Enable detailed logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run pipeline
pipeline.run(source())
```

#### Inspect pipeline state
```python
# Check pipeline info
print(pipeline.state)

# List tables
print(pipeline.default_schema.tables)

# Check last load info
load_info = pipeline.run(source())
print(load_info)
```

#### Use pipeline command
```bash
# Show pipeline info and open dashboard
dlt pipeline <pipeline_name> show

# View pipeline state
dlt pipeline <pipeline_name> info

# Trace last run
dlt pipeline <pipeline_name> trace
```

#### Test resources independently
```python
# Extract without loading
pipeline.extract(source())

# Normalize without loading
pipeline.normalize()

# Check extracted files
import os
print(os.listdir(pipeline.working_dir))
```

### Getting Help

When stuck:

1. **Check documentation**: https://dlthub.com/docs
2. **Search GitHub issues**: https://github.com/dlt-hub/dlt/issues
3. **Join Slack community**: https://dlthub.com/community
4. **Enable debug logging** and check error messages
5. **Create minimal reproducible example**
6. **Check dlt version**: `pip show dlt`

### Error Message Reference

| Error | Common Cause | Solution |
|-------|--------------|----------|
| `KeyError` in secrets | Missing or misnamed secret | Check `.dlt/secrets.toml` structure |
| `TableSchemaUpdateError` | Schema change conflict | Review schema evolution settings |
| `PipelineStepFailed` | Error in resource function | Check resource code and logs |
| `DestinationConnectionError` | Invalid destination config | Verify destination credentials |
| `ResourceExtractionError` | Error during data extraction | Add error handling in resource |
| `InvalidStepFunctionArguments` | Wrong function signature | Check decorator parameters |
