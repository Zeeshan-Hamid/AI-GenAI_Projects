import json
import os

def load_config(config_file=None):
    if config_file is None:
        config_file = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
    with open(config_file, "r") as f:
        config = json.load(f)
    return config

CONFIG = load_config()
ACTIVE_LOG_TYPE = CONFIG.get("active_log_type", "hdfs")
SUB_CONFIG = CONFIG.get(ACTIVE_LOG_TYPE, {})
ERROR_CODE_BONUS = SUB_CONFIG.get("error_code_bonus", {})
LOG_STRUCTURE = SUB_CONFIG.get("log_structure", {})
RAG_FILE = SUB_CONFIG.get("rag_file", f"rag_{ACTIVE_LOG_TYPE}.json")
CHUNK_SIZE = CONFIG.get("chunk_size", 15000)  # Default to 15000 if not specified

def print_config_info():
    print(f"Active log type: {ACTIVE_LOG_TYPE}")
    print(f"Using rag file: {RAG_FILE}")
    print(f"Log structure: {LOG_STRUCTURE}")
    print(f"Error code bonuses: {ERROR_CODE_BONUS}")
    print(f"Chunk size: {CHUNK_SIZE}")
