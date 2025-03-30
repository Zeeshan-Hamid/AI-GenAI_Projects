# Setting up Grafana for LogsMate Visualizations

This guide will help you set up Grafana to visualize the log analysis data from LogsMate.

## Prerequisites

- Elasticsearch running on http://localhost:9200/
- Grafana installed and running (typically on http://localhost:3000/)

## Step 1: Add Elasticsearch as a Data Source in Grafana

1. Open Grafana in your browser (http://localhost:3000/)
2. Log in (default credentials are admin/admin)
3. Go to Configuration > Data Sources
4. Click "Add data source"
5. Select "Elasticsearch"
6. Configure the data source:
   - Name: LogsMate
   - URL: http://localhost:9200
   - Access: Browser
   - Index name: logsmate_analysis
   - Time field name: timestamp
   - Version: Select the version matching your Elasticsearch (8.x)
7. Click "Save & Test" to verify the connection

## Step 2: Create a Dashboard

1. In Grafana, go to "Dashboards" > "New" > "New Dashboard"
2. Click "Add visualization"
3. Select the "LogsMate" data source you just created

## Step 3: Add Anomaly Severity Pie Chart

1. Click "Add panel"
2. Select "Pie Chart"
3. In the Query tab:
   - Configure the query:
   ```
   {
     "query": {
       "bool": {
         "must": [
           {"match_all": {}}
         ]
       }
     },
     "aggs": {
       "severity_counts": {
         "nested": {
           "path": "analysis_result.structured_data.anomaly_summary"
         },
         "aggs": {
           "info_count": {
             "sum": {
               "field": "analysis_result.structured_data.anomaly_summary.INFO.count"
             }
           },
           "medium_count": {
             "sum": {
               "field": "analysis_result.structured_data.anomaly_summary.MEDIUM.count"
             }
           },
           "high_count": {
             "sum": {
               "field": "analysis_result.structured_data.anomaly_summary.HIGH.count"
             }
           },
           "critical_count": {
             "sum": {
               "field": "analysis_result.structured_data.anomaly_summary.CRITICAL.count"
             }
           }
         }
       }
     },
     "size": 0
   }
   ```
4. Under Visualization settings:
   - Title: "Anomaly Severity Distribution"
   - Set appropriate colors for each severity (e.g., INFO=blue, MEDIUM=yellow, HIGH=orange, CRITICAL=red)

## Step 4: Add System Health Gauge

1. Click "Add panel"
2. Select "Gauge"
3. In the Query tab:
   - Configure a Lucene query to get the system health status
   - Use a value mapping to convert status text to numeric values

## Step 5: Add Table of Anomalies Summary

1. Click "Add panel"
2. Select "Table"
3. Configure a query to display:
   - Total log entries
   - Total anomalies
   - System health status

## Step 6: Add Anomaly Metrics

1. Add a "Stat" panel for total anomalies
2. Add a "Stat" panel for each severity level

## Step 7: Save Your Dashboard

1. Click the save icon in the top right corner
2. Name your dashboard "LogsMate Analysis Dashboard"
3. Click "Save"

## Troubleshooting

- If no data appears, make sure:
  - The Elasticsearch service is running
  - You've added sample data (using `python -m src.visualization`)
  - The index mapping is correct
  - The time range in Grafana includes the timestamp of your data

## Advanced Visualizations

For more advanced visualizations:

1. **Time Series** - If you analyze multiple log files over time, you can track anomalies over time
2. **Heatmaps** - Visualize concentration of anomalies by severity
3. **Text Panels** - Display the narrative parts of your analysis
4. **Annotations** - Mark important events or when specific analyses were performed 