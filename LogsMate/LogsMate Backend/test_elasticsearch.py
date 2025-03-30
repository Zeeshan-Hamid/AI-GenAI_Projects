import requests
import json
from datetime import datetime

# Elasticsearch configuration
ES_HOST = "http://localhost:9200"
INDEX_NAME = "logsmate_analysis"

def create_index():
    """Create the Elasticsearch index with proper mappings for the analysis data"""
    mapping = {
        "mappings": {
            "properties": {
                "timestamp": {"type": "date"},
                "log_filename": {"type": "keyword"},
                "analysis_result": {
                    "properties": {
                        "narrative": {"type": "text"},
                        "structured_data": {
                            "properties": {
                                "total_log_entries": {"type": "integer"},
                                "total_anomalies": {"type": "integer"},
                                "anomaly_summary": {
                                    "properties": {
                                        "INFO": {
                                            "properties": {
                                                "count": {"type": "integer"},
                                                "percentage": {"type": "keyword"}
                                            }
                                        },
                                        "MEDIUM": {
                                            "properties": {
                                                "count": {"type": "integer"},
                                                "percentage": {"type": "keyword"}
                                            }
                                        },
                                        "HIGH": {
                                            "properties": {
                                                "count": {"type": "integer"},
                                                "percentage": {"type": "keyword"}
                                            }
                                        },
                                        "CRITICAL": {
                                            "properties": {
                                                "count": {"type": "integer"},
                                                "percentage": {"type": "keyword"}
                                            }
                                        }
                                    }
                                },
                                "system_health": {"type": "keyword"},
                                "root_causes": {"type": "text"},
                                "actionable_insights": {"type": "text"}
                            }
                        }
                    }
                }
            }
        }
    }
    
    try:
        # Check if index exists
        response = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        if response.status_code == 404:
            # Create index
            response = requests.put(
                f"{ES_HOST}/{INDEX_NAME}",
                headers={"Content-Type": "application/json"},
                json=mapping
            )
            
            if response.status_code in (200, 201):
                print(f"Created Elasticsearch index '{INDEX_NAME}' successfully")
            else:
                print(f"Failed to create index. Status code: {response.status_code}, Response: {response.text}")
        else:
            print(f"Index '{INDEX_NAME}' already exists")
            
    except Exception as e:
        print(f"Error creating Elasticsearch index: {str(e)}")

def add_sample_data():
    """Add sample analysis data to Elasticsearch for testing visualizations"""
    sample_data = {
        "narrative": "The analysis of the provided log chunks revealed a total of 46 anomalies across 1599 log entries. The anomalies were categorized by their severity levels: INFO, MEDIUM, HIGH, and CRITICAL.",
        "structured_data": {
            "total_log_entries": 1599,
            "total_anomalies": 46,
            "anomaly_summary": {
                "INFO": {"count": 15, "percentage": "32.61%"},
                "MEDIUM": {"count": 20, "percentage": "43.48%"},
                "HIGH": {"count": 6, "percentage": "13.04%"},
                "CRITICAL": {"count": 5, "percentage": "10.87%"}
            },
            "root_causes": [
                "Security issues such as permission denials and data corruption.",
                "Performance issues including UI rendering problems and application not responding (ANR) events.",
                "Critical issues like native crashes and unexpected end-of-file (EOF) errors."
            ],
            "system_health": "Degraded",
            "actionable_insights": [
                "Conduct a thorough review of security policies and access controls to address permission issues.",
                "Investigate and resolve data corruption issues, particularly in SIM configuration.",
                "Address performance bottlenecks by optimizing UI rendering and managing resource contention.",
                "Prioritize fixing critical issues such as native crashes and EOF errors to enhance system stability."
            ]
        }
    }
    
    # Add timestamp and filename metadata
    document = {
        "timestamp": datetime.now().isoformat(),
        "log_filename": "sample_log.txt",
        "analysis_result": sample_data
    }
    
    try:
        # Ensure index exists
        create_index()
        
        # Post the document to Elasticsearch
        response = requests.post(
            f"{ES_HOST}/{INDEX_NAME}/_doc",
            headers={"Content-Type": "application/json"},
            json=document
        )
        
        if response.status_code in (200, 201):
            doc_id = response.json().get('_id')
            print(f"Sample data added to Elasticsearch successfully. Document ID: {doc_id}")
            return True
        else:
            print(f"Failed to save to Elasticsearch. Status code: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error saving analysis to Elasticsearch: {str(e)}")
        return False

def test_elasticsearch_connection():
    """Test basic Elasticsearch connectivity"""
    try:
        response = requests.get(f"{ES_HOST}")
        if response.status_code == 200:
            print("Successfully connected to Elasticsearch")
            print(f"Elasticsearch info: {response.json()}")
            return True
        else:
            print(f"Failed to connect to Elasticsearch. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Elasticsearch connection...")
    if test_elasticsearch_connection():
        print("\nAdding sample data to Elasticsearch...")
        add_sample_data()
        
        print("\nVerifying data in Elasticsearch...")
        try:
            response = requests.get(
                f"{ES_HOST}/{INDEX_NAME}/_search",
                headers={"Content-Type": "application/json"},
                json={
                    "query": {"match_all": {}},
                    "size": 10
                }
            )
            
            if response.status_code == 200:
                results = response.json()
                hits = results.get("hits", {}).get("hits", [])
                print(f"Found {len(hits)} documents in Elasticsearch")
                for hit in hits:
                    print(f"Document ID: {hit['_id']}")
                    print(f"Log Filename: {hit['_source']['log_filename']}")
                    print(f"Timestamp: {hit['_source']['timestamp']}")
                    print("---")
            else:
                print(f"Failed to query Elasticsearch. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error querying Elasticsearch: {str(e)}")
    else:
        print("Elasticsearch connection failed. Please ensure Elasticsearch is running at", ES_HOST) 