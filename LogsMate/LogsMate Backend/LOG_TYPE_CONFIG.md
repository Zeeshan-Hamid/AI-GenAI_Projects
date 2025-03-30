# LogsMate Log Type Configuration

This document explains how to use the log type configuration feature in LogsMate. This feature allows you to specify which log type (hdfs, android, or healthapp) to use when analyzing log files.

## Overview

The LogsMate system supports different types of log files, each with its own configuration for:

1. **Chroma Vector Store** - Each log type uses a separate Chroma DB directory for storing vector embeddings
2. **RAG Documents** - Different reference documents are used for each log type
3. **Log Structure** - Different parsing rules and field names for each log type
4. **Error Codes** - Different error codes and bonuses are applied based on log type

## Supported Log Types

The system currently supports the following log types:

1. **hdfs** - For Hadoop Distributed File System logs
2. **android** - For Android application and system logs
3. **healthapp** - For health application logs

## Using the API with Log Type Configuration

### Analyze Endpoint with Log Type Parameter

The `/analyze/{filename}` endpoint now accepts a form parameter called `log_type` that allows you to specify which configuration to use:

```bash
curl -X POST "http://localhost:8080/analyze/your-log-file.log" \
     -F "log_type=android"
```

Supported values for `log_type` are:
- `hdfs`
- `android`
- `healthapp`

### How It Works

When you provide a `log_type` parameter:

1. The API updates the active log type in the configuration
2. It reloads the configuration settings in memory
3. It updates the RAG documents and Chroma database directory according to the specified log type
4. It then analyzes the log file using the selected configuration

### Examples

#### Analyzing HDFS Logs

```bash
curl -X POST "http://localhost:8080/analyze/hdfs_server.log" \
     -F "log_type=hdfs"
```

#### Analyzing Android Logs

```bash
curl -X POST "http://localhost:8080/analyze/app_crash.log" \
     -F "log_type=android"
```

#### Analyzing Health App Logs

```bash
curl -X POST "http://localhost:8080/analyze/health_metrics.log" \
     -F "log_type=healthapp"
```

## Testing the Feature

A test script is provided to verify that the log type configuration works properly:

```bash
python test_log_type_endpoint.py
```

This script:
1. Creates sample log files for each log type if they don't exist
2. Tests the API with each log type
3. Displays a summary of the results

## Technical Details

### Configuration Structure

The configuration for each log type is defined in `config/config.json`:

```json
{
  "active_log_type": "hdfs",
  "hdfs": {
    "log_type": "hdfs",
    "error_code_bonus": { ... },
    "log_structure": { ... },
    "critical_errors": [ ... ],
    "rag_file": "rag_hdfs.json",
    "chroma_directory": "./hdfs_chroma"
  },
  "android": {
    ...
  },
  "healthapp": {
    ...
  }
}
```

### RAG Document Selection

Each log type has its own set of RAG documents defined in:
- `rag_docs/hdfs_docs.py`
- `rag_docs/android_docs.py`
- `rag_docs/healthApp_docs.py`

The system automatically selects the appropriate documents based on the active log type.

### Vector Store Management

Each log type uses a separate Chroma DB directory specified in its configuration:
- HDFS: `./hdfs_chroma`
- Android: `./android_chroma`
- Health App: `./health_app_chroma`

This ensures that each log type maintains its own separate vector store.

## Troubleshooting

### API Errors

If you receive a `400 Bad Request` error, ensure that:
- The `log_type` parameter is one of: `hdfs`, `android`, or `healthapp`

If you receive a `500 Internal Server Error`, check:
- The server logs for details about the error
- Ensure the configuration file is correctly formatted
- Verify that the specified Chroma directory exists and is writable 