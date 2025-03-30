import os
import requests
import json
from datetime import datetime

# Elasticsearch configuration
ES_HOST = "http://localhost:9200"
INDEX_NAME = "logsmate_analysis"

def clear_elasticsearch_index():
    """Clear all documents from the Elasticsearch index without deleting the index"""
    try:
        # First check if the index exists
        response = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        
        if response.status_code == 404:
            print(f"Index '{INDEX_NAME}' does not exist. Nothing to clear.")
            return True
            
        # Delete all documents using the delete by query API
        delete_query = {
            "query": {
                "match_all": {}
            }
        }
        
        response = requests.post(
            f"{ES_HOST}/{INDEX_NAME}/_delete_by_query",
            headers={"Content-Type": "application/json"},
            json=delete_query
        )
        
        if response.status_code in (200, 201):
            deleted_count = response.json().get('deleted', 0)
            print(f"Successfully deleted {deleted_count} documents from '{INDEX_NAME}' index")
            return True
        else:
            print(f"Failed to clear index. Status code: {response.status_code}, Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Elasticsearch at {ES_HOST}")
        print("Make sure Elasticsearch is running and accessible")
        return False
    except Exception as e:
        print(f"Error clearing Elasticsearch index: {str(e)}")
        return False

def delete_index():
    """Delete the entire Elasticsearch index"""
    try:
        # Check if index exists
        response = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        
        if response.status_code == 404:
            print(f"Index '{INDEX_NAME}' does not exist. Nothing to delete.")
            return True
            
        # Delete the index
        response = requests.delete(f"{ES_HOST}/{INDEX_NAME}")
        
        if response.status_code in (200, 201):
            print(f"Successfully deleted index '{INDEX_NAME}'")
            return True
        else:
            print(f"Failed to delete index. Status code: {response.status_code}, Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Elasticsearch at {ES_HOST}")
        print("Make sure Elasticsearch is running and accessible")
        return False
    except Exception as e:
        print(f"Error deleting Elasticsearch index: {str(e)}")
        return False

def add_sample_data():
    """Add sample analysis data to Elasticsearch for testing visualizations"""
    sample_data = {
        "narrative": "This is a sample analysis generated for testing. It shows a total of 46 anomalies across 1599 log entries with different severity levels.",
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
                "Performance issues including UI rendering problems and application not responding events.",
                "Critical issues like native crashes and unexpected end-of-file errors."
            ],
            "system_health": "Degraded",
            "actionable_insights": [
                "Review security policies and access controls to address permission issues.",
                "Investigate and resolve data corruption issues in configuration.",
                "Address performance bottlenecks in UI rendering and resource management.",
                "Prioritize fixes for critical issues to enhance system stability."
            ]
        }
    }
    
    # Add timestamp and filename metadata
    document = {
        "timestamp": datetime.now().isoformat(),
        "log_filename": "sample_log.txt",
        "analysis_result": sample_data
    }
    
    # Create index if it doesn't exist
    try:
        # Check if the index exists
        response = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        if response.status_code == 404:
            # Create the index with appropriate mappings
            create_index()
    except Exception as e:
        print(f"Error checking index: {str(e)}")
        return False
    
    # Post the document to Elasticsearch
    try:
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
            
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Elasticsearch at {ES_HOST}")
        print("Make sure Elasticsearch is running and accessible")
        return False
    except Exception as e:
        print(f"Error saving sample data to Elasticsearch: {str(e)}")
        return False

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
        response = requests.put(
            f"{ES_HOST}/{INDEX_NAME}",
            headers={"Content-Type": "application/json"},
            json=mapping
        )
        
        if response.status_code in (200, 201):
            print(f"Created Elasticsearch index '{INDEX_NAME}' successfully")
            return True
        else:
            print(f"Failed to create index. Status code: {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Elasticsearch at {ES_HOST}")
        print("Make sure Elasticsearch is running and accessible")
        return False
    except Exception as e:
        print(f"Error creating Elasticsearch index: {str(e)}")
        return False

def list_documents():
    """List all documents in the Elasticsearch index"""
    try:
        response = requests.get(
            f"{ES_HOST}/{INDEX_NAME}/_search",
            headers={"Content-Type": "application/json"},
            json={
                "query": {"match_all": {}},
                "sort": [{"timestamp": {"order": "desc"}}],
                "size": 100
            }
        )
        
        if response.status_code == 200:
            results = response.json()
            hits = results.get("hits", {}).get("hits", [])
            print(f"Found {len(hits)} documents in Elasticsearch")
            
            for i, hit in enumerate(hits, 1):
                source = hit["_source"]
                print(f"\n--- Document {i} ---")
                print(f"ID: {hit['_id']}")
                print(f"Log Filename: {source['log_filename']}")
                print(f"Timestamp: {source['timestamp']}")
                
                # Get structured data if available
                structured_data = source.get("analysis_result", {}).get("structured_data", {})
                if structured_data:
                    print(f"Total Log Entries: {structured_data.get('total_log_entries', 'N/A')}")
                    print(f"Total Anomalies: {structured_data.get('total_anomalies', 'N/A')}")
                    print(f"System Health: {structured_data.get('system_health', 'N/A')}")
            
            return True
        else:
            print(f"Failed to query Elasticsearch. Status code: {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Elasticsearch at {ES_HOST}")
        print("Make sure Elasticsearch is running and accessible")
        return False
    except Exception as e:
        print(f"Error querying Elasticsearch: {str(e)}")
        return False

def main_menu():
    """Display main menu and handle user choices"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*60)
    print("LogsMate Elasticsearch Data Management".center(60))
    print("="*60 + "\n")
    
    print("1. Clear all documents (keep index structure)")
    print("2. Delete entire index")
    print("3. Add sample data for testing")
    print("4. List all documents")
    print("5. Check Elasticsearch connection")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-5): ")
    
    if choice == "1":
        print("\nClearing all documents from Elasticsearch index...")
        success = clear_elasticsearch_index()
    elif choice == "2":
        print("\nDeleting entire Elasticsearch index...")
        confirmation = input("Are you sure you want to delete the entire index? (y/n): ")
        if confirmation.lower() == 'y':
            success = delete_index()
        else:
            print("Operation cancelled.")
            return
    elif choice == "3":
        print("\nAdding sample data to Elasticsearch...")
        success = add_sample_data()
    elif choice == "4":
        print("\nListing all documents in Elasticsearch...")
        success = list_documents()
    elif choice == "5":
        print("\nChecking Elasticsearch connection...")
        try:
            response = requests.get(ES_HOST)
            if response.status_code == 200:
                print("Successfully connected to Elasticsearch")
                print(f"Elasticsearch info: {json.dumps(response.json(), indent=2)}")
                success = True
            else:
                print(f"Failed to connect to Elasticsearch. Status code: {response.status_code}")
                success = False
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to Elasticsearch at {ES_HOST}")
            print("Make sure Elasticsearch is running and accessible")
            success = False
        except Exception as e:
            print(f"Error connecting to Elasticsearch: {str(e)}")
            success = False
    elif choice == "0":
        print("\nExiting...")
        exit(0)
    else:
        print("\nInvalid choice. Please try again.")
        input("\nPress Enter to continue...")
        main_menu()
        return
    
    if success:
        print("\nOperation completed successfully")
    else:
        print("\nOperation failed")
    
    input("\nPress Enter to continue...")
    main_menu()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}") 