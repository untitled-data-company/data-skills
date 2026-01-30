# Incremental Loading in dlt

## Table of Contents
- [Overview](#overview)
- [Write Dispositions](#write-dispositions)
- [Choosing the Right Strategy](#choosing-the-right-strategy)
- [Cursor-Based Incremental Loading](#cursor-based-incremental-loading)
- [Merge Strategies](#merge-strategies)
- [Advanced Techniques](#advanced-techniques)
- [Best Practices](#best-practices)

## Overview

Incremental loading transfers only new or modified data rather than reprocessing existing records. This reduces latency and operational costs while requiring careful state management.

## Write Dispositions

### 1. Replace (Full Load)
```python
@dlt.resource(write_disposition='replace')
def my_resource():
    yield data
```
- Completely overwrites destination dataset with current source data
- Use when you need a fresh snapshot every time
- No state tracking required

### 2. Append
```python
@dlt.resource(write_disposition='append')
def my_resource():
    yield data
```
- Adds new data without modifying existing records
- Best for stateless data (events, logs)
- Simple and efficient for immutable data

### 3. Merge
```python
@dlt.resource(
    write_disposition='merge',
    primary_key='id'
)
def my_resource():
    yield data
```
- Updates existing records using merge keys or primary keys
- Enables upserts and deduplication
- Use for stateful data that changes over time

## Choosing the Right Strategy

**Ask: Is your data stateful or stateless?**

- **Stateless data** (unchanging events) → Use `append`
- **Stateful data** (user profiles, evolving records) → Use `merge` or SCD2

**For stateful data, ask: Do you need change history?**

- **No history needed** → Use `merge` with incremental extraction
- **History needed** → Use SCD2 (Slowly Changing Dimensions Type-2)

## Cursor-Based Incremental Loading

Track changes via timestamp or ID fields:

```python
@dlt.resource(
    write_disposition='merge',
    primary_key='id'
)
def incremental_resource(
    updated_at=dlt.sources.incremental('updated_at', initial_value='2024-01-01T00:00:00Z')
):
    # Fetch data modified after the last cursor value
    url = f"https://api.example.com/data?updated_since={updated_at.last_value}"
    response = requests.get(url)
    yield response.json()
```

Key parameters:
- `cursor_path` - Field to track (e.g., 'updated_at', 'id')
- `initial_value` - Starting point for first run
- `last_value` - Last processed value (maintained by dlt)

## Merge Strategies

### Delete-Insert
Replaces records matching the merge key.

### SCD2 (Slowly Changing Dimensions Type-2)
Preserves historical changes by versioning records.

### Upsert
Updates existing records, inserts new ones.

## Advanced Techniques

### Lag/Attribution Windows
Refresh data within specific timeframes to handle late-arriving data:

```python
@dlt.resource(
    write_disposition='merge',
    primary_key='id'
)
def resource_with_lag(
    updated_at=dlt.sources.incremental(
        'updated_at',
        initial_value='2024-01-01T00:00:00Z',
        lag=timedelta(days=2)  # Re-fetch last 2 days
    )
):
    yield data
```

### Full Refresh

Force complete data reload when needed:

```python
# Reset incremental state
pipeline.run(source(), refresh='drop_sources')
```

For merge operations, this deletes destination data and reloads fresh content.

## Best Practices

1. **Choose appropriate cursor fields**: Use monotonically increasing fields (timestamps, IDs)
2. **Handle timezone consistency**: Ensure cursor timestamps are in UTC
3. **Consider data latency**: Use lag windows for systems with delayed updates
4. **Test incremental logic**: Verify that incremental runs don't miss or duplicate data
5. **Monitor state**: Check dlt's state to ensure cursors advance correctly
6. **Handle deletions**: Merge doesn't detect deletions by default - consider soft deletes or periodic full refreshes
