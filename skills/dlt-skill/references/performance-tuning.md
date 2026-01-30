# Performance Tuning in dlt

## Table of Contents
- [Overview](#overview)
- [Worker Configuration](#worker-configuration)
- [Buffer Management](#buffer-management)
- [File Rotation & Compression](#file-rotation--compression)
- [Extract Optimization Techniques](#extract-optimization-techniques)
- [Storage Management](#storage-management)
- [Configuration Scoping](#configuration-scoping)
- [Performance Best Practices](#performance-best-practices)
- [Common Optimization Scenarios](#common-optimization-scenarios)

## Overview

dlt pipelines have three main stages, each with configurable parallelism:
1. **Extract** - Fetch data from sources
2. **Normalize** - Process and prepare data
3. **Load** - Write to destination

## Worker Configuration

### Extract Stage
Uses thread pools for concurrent data extraction.

**Config (.dlt/config.toml):**
```toml
[extract]
workers = 5              # Thread pool workers (default: 5)
max_parallel_items = 20  # Async parallelism (default: 20)
```

**When to adjust:**
- Increase `workers` for I/O-bound operations (API calls)
- Increase `max_parallel_items` for async operations
- Monitor CPU usage to avoid over-threading

### Normalize Stage
Uses process pools for concurrent file processing.

**Config:**
```toml
[normalize]
workers = 3                    # Process pool workers (default: 3)
start_method = "spawn"         # Recommended for Linux with threading
```

**When to adjust:**
- Increase `workers` for CPU-intensive transformations
- Use `spawn` on Linux systems with threading issues
- Balance against available CPU cores

### Load Stage
Thread pool-based concurrent loading to destination.

**Config:**
```toml
[load]
workers = 50    # Concurrent load jobs (default: 20)
```

**When to adjust:**
- Increase for destinations that handle high concurrency well
- Decrease if hitting destination rate limits
- Monitor destination performance metrics

## Buffer Management

Control in-memory buffer sizes:

**Config:**
```toml
[data_writer]
buffer_max_items = 100    # Items in buffer (default: 5000)
```

**When to adjust:**
- Decrease for memory-constrained environments
- Increase for high-throughput pipelines with adequate memory

## File Rotation & Compression

Enable parallelization by rotating intermediary files:

**Config:**
```toml
[data_writer]
file_max_items = 100000     # Max items per file
file_max_bytes = 1000000    # Max bytes per file (1MB)

[normalize.data_writer]
disable_compression = true  # Disable for faster processing
```

**Important:** Default setting creates a single intermediary file. For millions of records, configure rotation to enable parallel processing.

**When to use:**
- Large datasets (millions+ records)
- Need parallel normalize/load stages
- Balance file count vs. file size

## Extract Optimization Techniques

### 1. Yield Pages Instead of Rows
```python
@dlt.resource
def optimized_resource():
    for page in paginate(url):
        yield page  # Yield entire page, not individual items
```

**Benefits:**
- Reduces pipeline iterations
- Better batching for downstream stages
- Lower overhead

### 2. Use Built-in HTTP Client
```python
from dlt.sources.helpers.rest_client import paginate

for page in paginate(url):
    yield page
```

**Benefits:**
- Optimized for dlt workflows
- Built-in retry logic
- Performance tuning included

### 3. Use orjson for JSON Parsing
dlt uses `orjson` by default for fast JSON parsing.

### 4. Switch to FIFO Mode for Debugging
```toml
[extract]
next_item_mode = "fifo"  # Sequential, deterministic extraction
```

Use only for debugging - reduces parallelism.

## Storage Management

### External Storage
For constrained environments, use external bucket storage:

```python
import os
os.environ["DLT_DATA_DIR"] = "/path/to/mounted/bucket"
```

### Monitoring
Enable graceful progress monitoring:

```bash
PROGRESS=log python pipeline.py
```

## Configuration Scoping

Apply settings at different levels:

**Global:**
```toml
[extract]
workers = 10
```

**Per-source:**
```toml
[sources.my_source.extract]
workers = 20
```

**Per-resource:**
```toml
[sources.my_source.resources.my_resource.extract]
workers = 5
```

## Performance Best Practices

1. **Start with defaults** - Profile first, optimize second
2. **Monitor resource usage** - Track CPU, memory, network I/O
3. **Optimize bottlenecks** - Focus on the slowest stage
4. **Test incrementally** - Change one setting at a time
5. **Balance parallelism** - More workers isn't always better
6. **Consider destination limits** - Respect rate limits and connection pools
7. **Use appropriate write disposition** - `append` is faster than `merge`
8. **Minimize data transformations** - Do heavy processing in source when possible
9. **Batch API calls** - Fetch data in pages/chunks
10. **Enable file rotation** - For large datasets requiring parallel processing

## Common Optimization Scenarios

### High-Volume API Extraction
```toml
[extract]
workers = 10
max_parallel_items = 50

[data_writer]
file_max_items = 50000
```

### CPU-Intensive Normalization
```toml
[normalize]
workers = 8
start_method = "spawn"
```

### Fast Destination Loading
```toml
[load]
workers = 100

[data_writer]
file_max_items = 100000
disable_compression = true
```

### Memory-Constrained Environment
```toml
[data_writer]
buffer_max_items = 1000

[extract]
workers = 2

[normalize]
workers = 1
```
