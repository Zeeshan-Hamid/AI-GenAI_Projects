import json
import requests
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Elasticsearch configuration
ES_HOST = "http://localhost:9200"
INDEX_NAME = "logsmate_analysis"

def save_analysis_to_elasticsearch(analysis_data, filename=None):
    """
    Save the analysis results to Elasticsearch for visualization in Grafana
    
    Args:
        analysis_data (str or dict): JSON string or dict containing the analysis results
        filename (str, optional): Name of the analyzed log file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Add debug logging to see what we're getting
        logger.info(f"Raw analysis data type: {type(analysis_data)}")
        
        # Handle different input types
        if isinstance(analysis_data, str):
            logger.info(f"Analysis data (first 200 chars): {analysis_data[:200]}...")
            
            # If it's a string, try to parse it as JSON
            try:
                # Handle case where the string might not be valid JSON
                analysis_data = json.loads(analysis_data.strip())
                logger.info("Successfully parsed JSON string")
            except json.JSONDecodeError as json_err:
                # Log more details about the parsing error
                logger.error(f"JSON parsing error: {str(json_err)}")
                logger.error(f"Problematic JSON string: {analysis_data[:500]}...")
                
                # Attempt to fix common JSON issues
                if not analysis_data.strip():
                    logger.warning("Empty JSON string received. Creating default structure.")
                    analysis_data = {
                        "narrative": "Error: No analysis data was generated",
                        "structured_data": {
                            "total_log_entries": 0,
                            "total_anomalies": 0,
                            "anomaly_summary": {
                                "INFO": {"count": 0, "percentage": "0%"},
                                "MEDIUM": {"count": 0, "percentage": "0%"},
                                "HIGH": {"count": 0, "percentage": "0%"},
                                "CRITICAL": {"count": 0, "percentage": "0%"}
                            },
                            "root_causes": ["Analysis error occurred"],
                            "system_health": "Unknown",
                            "actionable_insights": ["Retry the analysis"]
                        }
                    }
                else:
                    # If not a valid JSON, create a document with the raw text
                    logger.warning("Converting non-JSON string to document with raw text")
                    analysis_data = {
                        "narrative": analysis_data[:5000],  # Limit to 5000 chars
                        "structured_data": {
                            "total_log_entries": 0,
                            "total_anomalies": 0,
                            "anomaly_summary": {
                                "INFO": {"count": 0, "percentage": "0%"},
                                "MEDIUM": {"count": 0, "percentage": "0%"},
                                "HIGH": {"count": 0, "percentage": "0%"},
                                "CRITICAL": {"count": 0, "percentage": "0%"}
                            },
                            "root_causes": ["Data format error"],
                            "system_health": "Unknown",
                            "actionable_insights": ["Check LLM response format"]
                        }
                    }
        # Make sure we have a valid structure - even if analysis_data is already a dict
        elif isinstance(analysis_data, dict):
            # If it's a direct structure without narrative/structured_data
            if "narrative" not in analysis_data and "structured_data" not in analysis_data:
                # Check if this might be our API response format with final_summary
                if "final_summary" in analysis_data:
                    logger.info("Converting API response format to proper Elasticsearch format")
                    
                    # Try to extract the final_summary which should be our actual analysis
                    try:
                        # If final_summary is a JSON string
                        if isinstance(analysis_data["final_summary"], str):
                            try:
                                analysis_data = json.loads(analysis_data["final_summary"].strip())
                            except json.JSONDecodeError:
                                # If not valid JSON, use as raw narrative
                                analysis_data = {
                                    "narrative": analysis_data["final_summary"][:5000],
                                    "structured_data": {"system_health": "Unknown"}
                                }
                        else:
                            # If final_summary is already a dict
                            analysis_data = analysis_data["final_summary"]
                    except Exception as e:
                        logger.error(f"Error processing API response format: {str(e)}")
                        # Create a fallback structure
                        analysis_data = {
                            "narrative": str(analysis_data)[:5000],
                            "structured_data": {"system_health": "Unknown"}
                        }
                else:
                    # If it's some other dict format, wrap it in our expected structure
                    logger.info("Wrapping dict in standard format")
                    analysis_data = {
                        "narrative": str(analysis_data)[:5000],
                        "structured_data": {"system_health": "Unknown"}
                    }
        else:
            # Handle non-string, non-dict data (convert to string)
            logger.warning(f"Received non-string, non-dict data: {type(analysis_data)}")
            analysis_data = {
                "narrative": str(analysis_data)[:5000],
                "structured_data": {
                    "total_log_entries": 0,
                    "total_anomalies": 0,
                    "anomaly_summary": {
                        "INFO": {"count": 0, "percentage": "0%"},
                        "MEDIUM": {"count": 0, "percentage": "0%"},
                        "HIGH": {"count": 0, "percentage": "0%"},
                        "CRITICAL": {"count": 0, "percentage": "0%"}
                    },
                    "root_causes": ["Unexpected data type"],
                    "system_health": "Unknown",
                    "actionable_insights": ["Check API response format"]
                }
            }
        
        # Add timestamp and filename metadata
        document = {
            "timestamp": datetime.now().isoformat(),
            "log_filename": filename or "unknown_file.log",
            "analysis_result": analysis_data
        }
        
        logger.info(f"Final document structure: {json.dumps(document, indent=2)[:500]}...")
        
        # Check if the index exists, if not create it
        response = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        if response.status_code == 404:
            # Create the index with appropriate mappings
            create_index()
        
        # Post the document to Elasticsearch
        response = requests.post(
            f"{ES_HOST}/{INDEX_NAME}/_doc",
            headers={"Content-Type": "application/json"},
            json=document
        )
        
        if response.status_code in (200, 201):
            logger.info(f"Analysis saved to Elasticsearch successfully. Document ID: {response.json().get('_id')}")
            return True
        else:
            logger.error(f"Failed to save to Elasticsearch. Status code: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error saving analysis to Elasticsearch: {str(e)}")
        # Print stack trace for debugging
        import traceback
        logger.error(f"Stack trace: {traceback.format_exc()}")
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
            logger.info(f"Created Elasticsearch index '{INDEX_NAME}' successfully")
            return True
        else:
            logger.error(f"Failed to create index. Status code: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error creating Elasticsearch index: {str(e)}")
        return False

def get_all_analyses():
    """
    Retrieve all analysis results from Elasticsearch
    
    Returns:
        list: List of analysis documents
    """
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
            return [hit["_source"] for hit in results.get("hits", {}).get("hits", [])]
        else:
            logger.error(f"Failed to retrieve analyses. Status code: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error retrieving analyses from Elasticsearch: {str(e)}")
        return []

def add_sample_data():
    """
    Add sample analysis data to Elasticsearch for testing visualizations
    """
    sample_data = {
        "narrative": "The analysis of the provided log chunks revealed a total of 46 anomalies across 1599 log entries. The anomalies were categorized by their severity levels: INFO, MEDIUM, HIGH, and CRITICAL.\n\nAnomaly Ratios:\n- INFO: 15 anomalies, representing 32.61% of the total anomalies.\n- MEDIUM: 20 anomalies, representing 43.48% of the total anomalies.\n- HIGH: 6 anomalies, representing 13.04% of the total anomalies.\n- CRITICAL: 5 anomalies, representing 10.87% of the total anomalies.\n\nRoot Causes:\nSeveral potential root causes were identified for the anomalies:\n1. Security issues such as permission denials and data corruption.\n2. Performance issues including UI rendering problems and application not responding (ANR) events.\n3. Critical issues like native crashes and unexpected end-of-file (EOF) errors.\n\nSystem Health Assessment:\nThe overall system health is assessed as 'Degraded' due to the presence of multiple high and critical severity anomalies. The system's stability is compromised, indicating a need for immediate attention and remediation.\n\nActionable Insights:\n1. Conduct a thorough review of security policies and access controls to address permission issues.\n2. Investigate and resolve data corruption issues, particularly in SIM configuration.\n3. Address performance bottlenecks by optimizing UI rendering and managing resource contention.\n4. Prioritize fixing critical issues such as native crashes and EOF errors to enhance system stability.",
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
    
    return save_analysis_to_elasticsearch(sample_data, "sample_log.txt")

def clear_elasticsearch_index():
    """
    Clear all documents from the Elasticsearch index without deleting the index itself
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # First check if the index exists
        response = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        
        if response.status_code == 404:
            logger.info(f"Index '{INDEX_NAME}' does not exist. Nothing to clear.")
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
            logger.info(f"Successfully deleted {deleted_count} documents from '{INDEX_NAME}' index")
            return True
        else:
            logger.error(f"Failed to clear index. Status code: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error clearing Elasticsearch index: {str(e)}")
        return False

if __name__ == "__main__":
    # Test adding sample data
    add_sample_data()
    print("Sample data added to Elasticsearch") 