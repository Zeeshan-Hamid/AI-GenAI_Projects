import requests
import json
import time
import subprocess
import sys
import os
import signal
from datetime import datetime

# API and Elasticsearch configuration
API_HOST = "http://localhost:8080"
ES_HOST = "http://localhost:9200"
INDEX_NAME = "logsmate_analysis"

def test_elasticsearch_connection():
    """Test basic Elasticsearch connectivity"""
    try:
        response = requests.get(f"{ES_HOST}")
        if response.status_code == 200:
            print("✅ Successfully connected to Elasticsearch")
            return True
        else:
            print(f"❌ Failed to connect to Elasticsearch. Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to Elasticsearch at {ES_HOST}")
        print("   Make sure Elasticsearch is running and accessible")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Elasticsearch: {str(e)}")
        return False

def check_elasticsearch_data():
    """Check if data exists in Elasticsearch"""
    try:
        response = requests.get(
            f"{ES_HOST}/{INDEX_NAME}/_search",
            headers={"Content-Type": "application/json"},
            json={
                "query": {"match_all": {}},
                "sort": [{"timestamp": {"order": "desc"}}],
                "size": 10
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
                
                # Show analysis info if available
                if "analysis_result" in source:
                    if "structured_data" in source["analysis_result"]:
                        sd = source["analysis_result"]["structured_data"]
                        if "system_health" in sd:
                            print(f"System Health: {sd['system_health']}")
                        if "total_anomalies" in sd:
                            print(f"Total Anomalies: {sd['total_anomalies']}")
            
            return True
        else:
            print(f"❌ Failed to query Elasticsearch. Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to Elasticsearch at {ES_HOST}")
        return False
    except Exception as e:
        print(f"❌ Error querying Elasticsearch: {str(e)}")
        return False

def test_api_analyze_endpoint():
    """Test the /analyze/{filename} API endpoint"""
    print("\n🔍 Testing the API analyze endpoint")
    
    # First, list available log files
    try:
        response = requests.get(f"{API_HOST}/logs/")
        if response.status_code != 200:
            print(f"❌ Failed to get list of logs. Status code: {response.status_code}")
            return False
        
        log_files = response.json()
        if not log_files:
            print("❌ No log files found. Please upload a log file first.")
            return False
        
        # Use the first log file for testing
        test_file = log_files[0]
        print(f"📄 Using log file for testing: {test_file}")
        
        # Count existing documents in Elasticsearch before test
        es_response = requests.get(
            f"{ES_HOST}/{INDEX_NAME}/_count",
            headers={"Content-Type": "application/json"}
        )
        initial_count = 0
        if es_response.status_code == 200:
            initial_count = es_response.json().get("count", 0)
            print(f"📊 Initial document count in Elasticsearch: {initial_count}")
        
        # Call the analyze endpoint
        print(f"⏳ Analyzing log file: {test_file} (this may take a while)...")
        start_time = time.time()
        response = requests.post(f"{API_HOST}/analyze/{test_file}")
        elapsed_time = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ Analysis failed. Status code: {response.status_code}")
            print(f"Error: {response.text}")
            return False
        
        print(f"✅ Analysis completed in {elapsed_time:.2f} seconds")
        
        # Wait a moment for Elasticsearch to index the data
        print("⏳ Waiting for Elasticsearch to index the data...")
        time.sleep(2)
        
        # Check if a new document was added to Elasticsearch
        es_response = requests.get(
            f"{ES_HOST}/{INDEX_NAME}/_count",
            headers={"Content-Type": "application/json"}
        )
        if es_response.status_code == 200:
            new_count = es_response.json().get("count", 0)
            print(f"📊 New document count in Elasticsearch: {new_count}")
            
            if new_count > initial_count:
                print("✅ Analysis was successfully saved to Elasticsearch")
                return True
            else:
                print("❌ No new documents were added to Elasticsearch")
                return False
        else:
            print(f"❌ Failed to get document count from Elasticsearch. Status code: {es_response.status_code}")
            return False
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to API at {API_HOST}")
        print("   Make sure the API server is running")
        return False
    except Exception as e:
        print(f"❌ Error testing analyze endpoint: {str(e)}")
        return False

def start_api_server():
    """Start the API server in a subprocess"""
    try:
        print("🚀 Starting API server...")
        process = subprocess.Popen([sys.executable, "-m", "src.api"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Test if server is running
        try:
            response = requests.get(f"{API_HOST}/")
            if response.status_code == 200:
                print("✅ API server is running")
                return process
            else:
                print(f"❌ API server returned unexpected status: {response.status_code}")
                process.kill()
                return None
        except requests.exceptions.ConnectionError:
            print(f"❌ Could not connect to API at {API_HOST}")
            process.kill()
            return None
    except Exception as e:
        print(f"❌ Error starting API server: {str(e)}")
        return None

def stop_api_server(process):
    """Stop the API server subprocess"""
    if process:
        print("🛑 Stopping API server...")
        try:
            if os.name == 'nt':  # Windows
                process.kill()
            else:  # Linux/Mac
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except:
            process.kill()
        
        print("✅ API server stopped")

def upload_sample_log():
    """Upload a sample log file for testing"""
    # Create a simple sample log file if none exists
    log_dir = os.path.join("data", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    sample_file_path = os.path.join(log_dir, "sample_test.log")
    if not os.path.exists(sample_file_path):
        print("📝 Creating sample log file for testing...")
        with open(sample_file_path, "w") as f:
            f.write("2023-06-01 12:00:00 INFO [main] Starting application\n")
            f.write("2023-06-01 12:00:01 DEBUG [config] Loading configuration\n")
            f.write("2023-06-01 12:00:02 WARNING [auth] Failed login attempt from 192.168.1.100\n")
            f.write("2023-06-01 12:00:03 ERROR [database] Connection timeout\n")
            f.write("2023-06-01 12:00:04 INFO [main] Retrying database connection\n")
            f.write("2023-06-01 12:00:05 INFO [main] Connected to database\n")
            f.write("2023-06-01 12:00:06 DEBUG [user] User profile loaded\n")
            f.write("2023-06-01 12:00:07 INFO [main] Application ready\n")
        print(f"✅ Created sample log file: {sample_file_path}")
    else:
        print(f"✅ Sample log file already exists: {sample_file_path}")

def run_complete_test():
    """Run a complete test of the API and Elasticsearch integration"""
    print("\n" + "="*60)
    print(" TESTING API & ELASTICSEARCH INTEGRATION ".center(60, "="))
    print("="*60 + "\n")
    
    # Step 1: Check Elasticsearch connection
    print("\n📋 STEP 1: Checking Elasticsearch connection")
    if not test_elasticsearch_connection():
        print("\n❌ TEST FAILED: Could not connect to Elasticsearch")
        return
    
    # Step 2: Create sample log file
    print("\n📋 STEP 2: Preparing sample log file")
    upload_sample_log()
    
    # Step 3: Start API server
    print("\n📋 STEP 3: Starting API server")
    api_process = start_api_server()
    if not api_process:
        print("\n❌ TEST FAILED: Could not start API server")
        return
    
    try:
        # Step 4: Test the analyze endpoint
        print("\n📋 STEP 4: Testing analyze endpoint")
        api_test_success = test_api_analyze_endpoint()
        
        # Step 5: Check the data in Elasticsearch
        print("\n📋 STEP 5: Checking data in Elasticsearch")
        es_data_success = check_elasticsearch_data()
        
        # Final result
        print("\n" + "="*60)
        if api_test_success and es_data_success:
            print("✅ TEST PASSED: API successfully saves analysis to Elasticsearch")
        else:
            print("❌ TEST FAILED: Issues detected during testing")
        print("="*60 + "\n")
    
    finally:
        # Always stop the API server
        stop_api_server(api_process)

if __name__ == "__main__":
    run_complete_test() 