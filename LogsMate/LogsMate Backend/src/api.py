import os
import shutil
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import importlib
from datetime import datetime

app = FastAPI(title="LogsMate API", 
              description="API for uploading and analyzing log files",
              version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure logs directory exists
LOGS_DIR = os.path.join("data", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Status tracking for analysis jobs
analysis_status = {}

@app.get("/")
async def root():
    return {"message": "Welcome to LogsMate API"}

@app.post("/upload/", response_model=dict)
async def upload_log_file(file: UploadFile = File(...)):
    """
    Upload a log file (.log or .txt)
    """
    # Validate file extension
    if not (file.filename.endswith('.log') or file.filename.endswith('.txt')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only .log and .txt files are supported."
        )
    
    # Save the file
    file_path = os.path.join(LOGS_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    finally:
        file.file.close()
    
    return {
        "filename": file.filename,
        "message": f"File {file.filename} uploaded successfully",
        "file_path": file_path
    }

@app.get("/logs/", response_model=List[str])
async def list_logs():
    """
    List all available log files
    """
    try:
        files = [f for f in os.listdir(LOGS_DIR) 
                if os.path.isfile(os.path.join(LOGS_DIR, f)) and 
                (f.endswith('.log') or f.endswith('.txt'))]
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing log files: {str(e)}")

@app.post("/analyze/{filename}")
async def analyze_log(filename: str, log_type: Optional[str] = Form(None)):
    """
    Run analysis on a specific log file and return the results.
    The final analysis will be stored in Elasticsearch for visualization.
    
    Parameters:
    - filename: Name of the log file to analyze
    - log_type: Optional form parameter to specify the log type (hdfs, android, or healthapp)
    """
    file_path = os.path.join(LOGS_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    
    if not (filename.endswith('.log') or filename.endswith('.txt')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only .log and .txt files are supported."
        )
    
    # Import logging at the top level
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Validate and set log type if provided
    if log_type:
        if log_type not in ["hdfs", "android", "healthapp"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid log_type: {log_type}. Must be one of: hdfs, android, or healthapp."
            )
        
        # Update the active log type in config
        try:
            # Import config module
            config_module = importlib.import_module("src.config")
            
            # Import json module to update the config file
            import json
            
            # Path to config file
            config_file_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
            
            # Load the current config
            with open(config_file_path, "r") as f:
                config_data = json.load(f)
            
            # Update the active log type
            config_data["active_log_type"] = log_type
            
            # Save the updated config
            with open(config_file_path, "w") as f:
                json.dump(config_data, f, indent=2)
            
            # Reload the config in memory
            config_module.CONFIG = config_module.load_config()
            config_module.ACTIVE_LOG_TYPE = config_module.CONFIG.get("active_log_type", "hdfs")
            config_module.SUB_CONFIG = config_module.CONFIG.get(config_module.ACTIVE_LOG_TYPE, {})
            config_module.ERROR_CODE_BONUS = config_module.SUB_CONFIG.get("error_code_bonus", {})
            config_module.LOG_STRUCTURE = config_module.SUB_CONFIG.get("log_structure", {})
            config_module.RAG_FILE = config_module.SUB_CONFIG.get("rag_file", f"rag_{config_module.ACTIVE_LOG_TYPE}.json")
            
            # Also update RAG settings since they're loaded at module import time
            rag_module = importlib.import_module("src.rag")
            
            # Set the appropriate RAG docs based on the log type
            if log_type == "hdfs":
                rag_module.rag_docs = rag_module.hdfs_rag_docs
                logger.info("Using HDFS RAG documents")
            elif log_type == "android":
                rag_module.rag_docs = rag_module.android_rag_docs
                logger.info("Using Android RAG documents")
            elif log_type == "healthapp":
                rag_module.rag_docs = rag_module.healthapp_rag_docs
                logger.info("Using HealthApp RAG documents")
            
            # Update the Chroma directory from the new config
            chroma_directory = config_module.SUB_CONFIG.get("chroma_directory", "./default_chroma")
            
            # Reinitialize the vector database with the new directory
            rag_module.vector_db = rag_module.Chroma(
                embedding_function=rag_module.embedding_model,
                persist_directory=chroma_directory
            )
            
            logger.info(f"Successfully updated active log type to: {log_type}")
            logger.info(f"Chroma directory set to: {chroma_directory}")
            
        except Exception as config_error:
            logger.error(f"Error updating config with log_type {log_type}: {config_error}")
            raise HTTPException(
                status_code=500,
                detail=f"Error updating configuration: {str(config_error)}"
            )
    
    try:
        # Import main module dynamically
        main_module = importlib.import_module("src.main")
        
        # Set the file path in main module
        main_module.file_name = file_path
        
        # Run analysis synchronously (this will block until complete)
        logger.info(f"Starting analysis for {filename}")
        llm_results = await asyncio.to_thread(main_module.main)
        logger.info(f"Analysis computation completed for {filename}")
        
        # Initialize default response
        response_data = {
            "filename": filename,
            "message": "Analysis completed but no results were produced",
            "final_summary": "No analysis results available"
        }
        
        # Process analysis results
        if llm_results and isinstance(llm_results, list):
            # Sort results by index to ensure correct order
            llm_results.sort(key=lambda x: x[0])
            
            # Extract all history from memory
            combined_history = []
            for _, _, mem in llm_results:
                mem_data = mem.load_memory_variables({})
                combined_history.extend(mem_data["history"])
            
            # Import the generate_final_report function and get final summary
            llm_analysis_module = importlib.import_module("src.llm_analysis")
            final_report_summary = llm_analysis_module.generate_final_report(combined_history)
            
            # Update response with actual data
            response_data = {
                "filename": filename,
                "message": "Analysis completed successfully",
                "final_summary": final_report_summary,
                "log_type": log_type or importlib.import_module("src.config").ACTIVE_LOG_TYPE
            }
        
        # Save to Elasticsearch - this happens ALWAYS, even if analysis had issues
        try:
            # Import visualization module
            visualization_module = importlib.import_module("src.visualization")
            
            # Save final report to Elasticsearch - saving the API response itself
            # This ensures we always save something to Elasticsearch
            es_save_result = visualization_module.save_analysis_to_elasticsearch(
                response_data["final_summary"],
                filename
            )
            
            if es_save_result:
                logger.info(f"Successfully saved analysis for {filename} to Elasticsearch")
            else:
                logger.warning(f"Save to Elasticsearch returned False for {filename}")
                
        except Exception as viz_error:
            logger.error(f"Error saving to Elasticsearch: {str(viz_error)}")
            import traceback
            logger.error(f"Elasticsearch error traceback: {traceback.format_exc()}")
            # Continue with the API response even if Elasticsearch storage fails
        
        # Always return the response
        return response_data
        
    except Exception as e:
        logger.error(f"Error during analysis of {filename}: {str(e)}")
        import traceback
        logger.error(f"Analysis error traceback: {traceback.format_exc()}")
        
        # Try to save error information to Elasticsearch
        try:
            # Create an error report
            error_report = {
                "narrative": f"Error during analysis: {str(e)}",
                "structured_data": {
                    "total_log_entries": 0,
                    "total_anomalies": 0,
                    "anomaly_summary": {
                        "INFO": {"count": 0, "percentage": "0%"},
                        "MEDIUM": {"count": 0, "percentage": "0%"},
                        "HIGH": {"count": 0, "percentage": "0%"},
                        "CRITICAL": {"count": 0, "percentage": "0%"}
                    },
                    "root_causes": ["Analysis engine error"],
                    "system_health": "Error",
                    "actionable_insights": ["Check server logs for details"]
                }
            }
            
            # Import visualization module
            visualization_module = importlib.import_module("src.visualization")
            
            # Save error report to Elasticsearch
            visualization_module.save_analysis_to_elasticsearch(error_report, filename)
            logger.info(f"Saved error report for {filename} to Elasticsearch")
            
        except Exception as es_error:
            logger.error(f"Failed to save error report to Elasticsearch: {str(es_error)}")
        
        # Re-raise the original exception for API error response
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")

@app.get("/status/{filename}", response_model=dict)
async def check_status(filename: str):
    """
    Check the status of an analysis job
    """
    if filename not in analysis_status:
        return {"status": "not_started"}
    
    return {
        "status": analysis_status[filename]
    }

@app.get("/recent-uploads/")
async def recent_uploads():
    """
    Get list of recently uploaded log files with their details
    """
    try:
        files = []
        for filename in os.listdir(LOGS_DIR):
            if filename.endswith(('.log', '.txt')):
                file_path = os.path.join(LOGS_DIR, filename)
                file_stats = os.stat(file_path)
                files.append({
                    "filename": filename,
                    "size_bytes": file_stats.st_size,
                    "upload_time": datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                })
        
        # Sort files by upload time, most recent first
        files.sort(key=lambda x: x["upload_time"], reverse=True)
        
        return {
            "files": files,
            "total_count": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing recent uploads: {str(e)}")

@app.get("/analyses/")
async def list_analyses():
    """
    Get all analysis results stored in Elasticsearch for visualization
    """
    try:
        visualization_module = importlib.import_module("src.visualization")
        analyses = visualization_module.get_all_analyses()
        return {
            "analyses": analyses,
            "total_count": len(analyses)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving analyses: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8080, reload=True) 