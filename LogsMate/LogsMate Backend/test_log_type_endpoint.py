import requests
import time
import os
import json

# API configuration
API_HOST = "http://localhost:8080"
TEST_LOG_TYPES = ["android", "hdfs", "healthapp"]

def ensure_sample_logs_exist():
    """Create sample log files for each log type if they don't exist"""
    log_dir = os.path.join("data", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Create one sample file for each log type
    files_created = False
    
    # Android sample log
    android_file = os.path.join(log_dir, "android_sample.log")
    if not os.path.exists(android_file):
        with open(android_file, "w") as f:
            f.write("06-15 12:34:56.789 E/AndroidRuntime: FATAL EXCEPTION: main\n")
            f.write("06-15 12:34:56.789 E/AndroidRuntime: Process: com.example.app, PID: 12345\n")
            f.write("06-15 12:34:56.789 E/AndroidRuntime: java.lang.NullPointerException: Attempt to invoke virtual method\n")
            f.write("06-15 12:34:56.790 E/AndroidRuntime:   at com.example.app.MainActivity.onCreate(MainActivity.java:25)\n")
            f.write("06-15 12:34:56.790 I/Process: Sending signal. PID: 12345 SIG: 9\n")
        print(f"Created Android sample log: {android_file}")
        files_created = True
    
    # HDFS sample log
    hdfs_file = os.path.join(log_dir, "hdfs_sample.log")
    if not os.path.exists(hdfs_file):
        with open(hdfs_file, "w") as f:
            f.write("2023-06-15 12:34:56 INFO dfs.DataNode: Receiving block blk_123456789\n")
            f.write("2023-06-15 12:34:57 INFO dfs.DataNode: Received block blk_123456789 of size 67108864\n")
            f.write("2023-06-15 12:34:58 ERROR dfs.DataNode: Checksum failed for block blk_123456789\n")
            f.write("2023-06-15 12:34:59 WARN dfs.DataNode: Block blk_123456789 received with invalid checksum\n")
            f.write("2023-06-15 12:35:00 INFO dfs.DataNode: Deleting block blk_123456789\n")
        print(f"Created HDFS sample log: {hdfs_file}")
        files_created = True
    
    # Health app sample log
    health_file = os.path.join(log_dir, "healthapp_sample.log")
    if not os.path.exists(health_file):
        with open(health_file, "w") as f:
            f.write("20230615-12:34:56:789 [INFO] HealthApp: Starting health monitoring service\n")
            f.write("20230615-12:34:57:123 [INFO] SensorManager: Heart rate sensor initialized\n")
            f.write("20230615-12:34:58:456 [ERROR] SensorManager: Failed to read data from blood pressure sensor\n")
            f.write("20230615-12:34:59:789 [WARN] DataProcessor: Abnormal heart rate detected: 150 BPM\n")
            f.write("20230615-12:35:00:123 [INFO] HealthApp: Alert sent to user for abnormal heart rate\n")
        print(f"Created Health App sample log: {health_file}")
        files_created = True
    
    if not files_created:
        print("All sample log files already exist")
    
    # Return the file names for each log type
    return {
        "android": "android_sample.log",
        "hdfs": "hdfs_sample.log",
        "healthapp": "healthapp_sample.log"
    }

def test_api_server_running():
    """Test if the API server is running"""
    try:
        response = requests.get(f"{API_HOST}")
        if response.status_code == 200:
            print(f"✅ API server is running at {API_HOST}")
            return True
        else:
            print(f"❌ API server returned unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to API at {API_HOST}")
        print("Please start the API server with: python -m src.api")
        return False
    except Exception as e:
        print(f"❌ Error connecting to API: {str(e)}")
        return False

def test_log_type_endpoint(log_type, log_file):
    """Test the analyze endpoint with a specific log type"""
    print(f"\n📝 Testing log type: {log_type}")
    
    try:
        # Call the analyze endpoint with the form data
        url = f"{API_HOST}/analyze/{log_file}"
        form_data = {"log_type": log_type}
        
        print(f"📤 Sending request to: {url}")
        print(f"📤 With form data: {form_data}")
        
        response = requests.post(url, data=form_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis succeeded for {log_type}")
            print(f"📊 Response log_type: {result.get('log_type', 'Not specified')}")
            print(f"📂 Analyzed file: {result.get('filename', 'Unknown')}")
            print(f"📝 Message: {result.get('message', 'No message')}")
            
            # Check if final summary exists and is too long
            if "final_summary" in result:
                summary_len = len(str(result["final_summary"]))
                print(f"📜 Final summary length: {summary_len} characters")
            
            return True
        else:
            print(f"❌ Analysis failed. Status code: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing endpoint: {str(e)}")
        return False

def run_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print(" TESTING LOG TYPE CONFIG IN ANALYZE ENDPOINT ".center(60, "="))
    print("="*60 + "\n")
    
    # Step 1: Check API server
    if not test_api_server_running():
        print("\n❌ Please start the API server and try again")
        return
    
    # Step 2: Create sample log files
    print("\n📋 STEP 1: Creating sample log files")
    sample_files = ensure_sample_logs_exist()
    
    # Step 3: Test each log type
    print("\n📋 STEP 2: Testing each log type")
    results = {}
    
    for log_type in TEST_LOG_TYPES:
        log_file = sample_files[log_type]
        test_result = test_log_type_endpoint(log_type, log_file)
        results[log_type] = test_result
        time.sleep(1)  # Brief pause between tests
    
    # Step 4: Print summary
    print("\n" + "="*60)
    print(" TEST RESULTS SUMMARY ".center(60, "="))
    print("="*60)
    
    for log_type, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{log_type.ljust(15)}: {status}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    run_tests() 