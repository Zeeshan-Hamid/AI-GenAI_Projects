import requests
import json
from datetime import datetime
import time

# Elasticsearch configuration
ES_HOST = "http://localhost:9200"
INDEX_NAME = "logsmate_analysis"

def test_es_connection():
    """Test the connection to Elasticsearch"""
    try:
        print("Testing Elasticsearch connection...")
        response = requests.get(ES_HOST)
        if response.status_code == 200:
            print("✅ Connected to Elasticsearch successfully")
            print(f"Elasticsearch version: {response.json().get('version', {}).get('number', 'Unknown')}")
            return True
        else:
            print(f"❌ Failed to connect to Elasticsearch. Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Elasticsearch is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Elasticsearch: {str(e)}")
        return False

def clear_es_index():
    """Attempt to clear the Elasticsearch index"""
    try:
        print(f"\nAttempting to clear index '{INDEX_NAME}'...")
        
        # First check if the index exists
        head_response = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        if head_response.status_code == 404:
            print(f"❌ Index '{INDEX_NAME}' does not exist. Nothing to clear.")
            return False
        
        # Try to clear all documents using DELETE BY QUERY API
        delete_query = {
            "query": {
                "match_all": {}
            }
        }
        
        # Use DELETE BY QUERY endpoint
        response = requests.post(
            f"{ES_HOST}/{INDEX_NAME}/_delete_by_query",
            headers={"Content-Type": "application/json"},
            json=delete_query
        )
        
        if response.status_code in (200, 201):
            deleted_count = response.json().get('deleted', 0)
            print(f"✅ Successfully deleted {deleted_count} documents from '{INDEX_NAME}'")
            
            # Refresh index to make changes visible immediately
            refresh_response = requests.post(f"{ES_HOST}/{INDEX_NAME}/_refresh")
            if refresh_response.status_code in (200, 201):
                print("✅ Index refreshed successfully")
            else:
                print(f"⚠️ Index refresh failed: {refresh_response.status_code}")
                
            return True
        else:
            print(f"❌ Failed to clear index. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Elasticsearch is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error clearing Elasticsearch index: {str(e)}")
        return False

def add_test_document():
    """Add a test document to Elasticsearch"""
    try:
        print(f"\nAdding test document to '{INDEX_NAME}'...")
        
        # Create a test document
        test_doc = {
            "timestamp": datetime.now().isoformat(),
            "log_filename": "test_doc.log",
            "analysis_result": {
                "narrative": "This is a test document added at " + datetime.now().isoformat(),
                "structured_data": {
                    "total_log_entries": 100,
                    "total_anomalies": 5,
                    "anomaly_summary": {
                        "INFO": {"count": 2, "percentage": "40%"},
                        "MEDIUM": {"count": 2, "percentage": "40%"},
                        "HIGH": {"count": 1, "percentage": "20%"},
                        "CRITICAL": {"count": 0, "percentage": "0%"}
                    },
                    "root_causes": ["Test root cause"],
                    "system_health": "Stable",
                    "actionable_insights": ["Test insight"]
                }
            }
        }
        
        # Check if the index exists, if not create it
        head_response = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        if head_response.status_code == 404:
            print(f"Index '{INDEX_NAME}' does not exist. Creating it...")
            
            # Create index with basic mapping
            mapping = {
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "log_filename": {"type": "keyword"},
                        "analysis_result": {
                            "properties": {
                                "narrative": {"type": "text"},
                                "structured_data": {"type": "object"}
                            }
                        }
                    }
                }
            }
            
            create_response = requests.put(
                f"{ES_HOST}/{INDEX_NAME}",
                headers={"Content-Type": "application/json"},
                json=mapping
            )
            
            if create_response.status_code not in (200, 201):
                print(f"❌ Failed to create index. Status code: {create_response.status_code}")
                print(f"Response: {create_response.text}")
                return False
            
            print(f"✅ Index '{INDEX_NAME}' created successfully")
        
        # Add the document
        response = requests.post(
            f"{ES_HOST}/{INDEX_NAME}/_doc",
            headers={"Content-Type": "application/json"},
            json=test_doc
        )
        
        if response.status_code in (200, 201):
            doc_id = response.json().get('_id')
            print(f"✅ Test document added successfully. Document ID: {doc_id}")
            
            # Refresh index to make document immediately visible
            refresh_response = requests.post(f"{ES_HOST}/{INDEX_NAME}/_refresh")
            if refresh_response.status_code in (200, 201):
                print("✅ Index refreshed successfully")
            else:
                print(f"⚠️ Index refresh failed: {refresh_response.status_code}")
                
            return True
        else:
            print(f"❌ Failed to add document. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Elasticsearch is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error adding test document: {str(e)}")
        return False

def count_documents():
    """Count documents in the index"""
    try:
        print(f"\nCounting documents in '{INDEX_NAME}'...")
        
        # Check if the index exists
        head_response = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        if head_response.status_code == 404:
            print(f"❌ Index '{INDEX_NAME}' does not exist.")
            return 0
        
        # Count documents
        response = requests.get(
            f"{ES_HOST}/{INDEX_NAME}/_count",
            headers={"Content-Type": "application/json"},
            json={"query": {"match_all": {}}}
        )
        
        if response.status_code == 200:
            count = response.json().get('count', 0)
            print(f"✅ Found {count} documents in '{INDEX_NAME}'")
            return count
        else:
            print(f"❌ Failed to count documents. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return 0
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Elasticsearch is not running or not accessible")
        return 0
    except Exception as e:
        print(f"❌ Error counting documents: {str(e)}")
        return 0

def run_tests():
    """Run all tests in sequence"""
    print("=" * 60)
    print("ELASTICSEARCH OPERATIONS TEST")
    print("=" * 60)
    
    # Test 1: Check connection
    if not test_es_connection():
        print("\n❌ Test failed: Could not connect to Elasticsearch")
        return
    
    # Test 2: Count existing documents
    initial_count = count_documents()
    
    # Test 3: Add a test document
    if not add_test_document():
        print("\n❌ Test failed: Could not add test document")
    else:
        # Verify document was added
        time.sleep(1)  # Wait for indexing
        new_count = count_documents()
        if new_count > initial_count:
            print("✅ Document count increased, confirming document was added")
        else:
            print("❌ Document count did not increase, document may not have been added")
    
    # Test 4: Clear the index
    if not clear_es_index():
        print("\n❌ Test failed: Could not clear Elasticsearch index")
    else:
        # Verify documents were cleared
        time.sleep(1)  # Wait for indexing
        final_count = count_documents()
        if final_count == 0:
            print("✅ All documents were cleared successfully")
        else:
            print(f"⚠️ Not all documents were cleared. {final_count} documents remain")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_tests() 