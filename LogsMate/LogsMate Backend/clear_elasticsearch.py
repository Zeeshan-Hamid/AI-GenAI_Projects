try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Elasticsearch configuration
ES_HOST = "http://localhost:9200"
INDEX_NAME = "logsmate_analysis"

def clear_elasticsearch_index():
    """
    Clear all documents from the Elasticsearch index without deleting the index itself
    """
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
            print(f"Failed to clear index. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Elasticsearch at {ES_HOST}")
        print("Make sure Elasticsearch is running and accessible")
        return False
    except Exception as e:
        print(f"Error clearing Elasticsearch index: {str(e)}")
        return False

def delete_index():
    """
    Delete the entire index and recreate it empty
    """
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
            print(f"Failed to delete index. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Elasticsearch at {ES_HOST}")
        print("Make sure Elasticsearch is running and accessible")
        return False
    except Exception as e:
        print(f"Error deleting Elasticsearch index: {str(e)}")
        return False

if __name__ == "__main__":
    print("Elasticsearch Database Management")
    print("1. Clear all documents (keep index structure)")
    print("2. Delete entire index")
    
    choice = input("Enter your choice (1/2): ")
    
    if choice == "1":
        print("Clearing all documents from Elasticsearch index...")
        success = clear_elasticsearch_index()
    elif choice == "2":
        print("Deleting entire Elasticsearch index...")
        success = delete_index()
    else:
        print("Invalid choice. Exiting.")
        exit(1)
    
    if success:
        print("Operation completed successfully")
    else:
        print("Operation failed") 