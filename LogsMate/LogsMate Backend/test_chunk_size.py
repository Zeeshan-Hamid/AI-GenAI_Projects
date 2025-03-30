#!/usr/bin/env python3
"""
Test script to verify that the global chunk size configuration is working correctly.
"""

import os
import json
import logging
from src.config import CHUNK_SIZE, print_config_info
from src.log_processor import chunk_log_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_global_chunk_size():
    """Test that the global chunk size is being used correctly."""
    print_config_info()
    
    # Test default chunk size
    logger.info(f"Current global chunk size: {CHUNK_SIZE}")
    
    # Create a test log file
    test_log_path = os.path.join("data", "logs", "test_chunk_size.log")
    os.makedirs(os.path.dirname(test_log_path), exist_ok=True)
    
    # Create a test log with 100 lines
    with open(test_log_path, "w") as f:
        for i in range(1, 101):
            f.write(f"This is test log line {i}\n")
    
    # Test chunking with default size
    chunks = chunk_log_file(test_log_path)
    logger.info(f"Number of chunks with default size ({CHUNK_SIZE}): {len(chunks)}")
    
    # Test chunking with custom size
    custom_size = 500
    chunks = chunk_log_file(test_log_path, chunk_size=custom_size)
    logger.info(f"Number of chunks with custom size ({custom_size}): {len(chunks)}")
    
    # Test changing global size in config
    config_path = os.path.join("config", "config.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Save original value
    original_size = config.get("chunk_size", CHUNK_SIZE)
    
    try:
        # Change global size
        new_size = 10000
        config["chunk_size"] = new_size
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        # Reload config and test again
        logger.info("Changing global chunk size to 10000 and reloading configuration...")
        
        # We need to reload the config module
        import importlib
        import src.config
        importlib.reload(src.config)
        from src.config import CHUNK_SIZE as NEW_CHUNK_SIZE
        
        logger.info(f"Reloaded global chunk size: {NEW_CHUNK_SIZE}")
        
        # Test chunking with reloaded size
        from src.log_processor import chunk_log_file as reloaded_chunk_log_file
        chunks = reloaded_chunk_log_file(test_log_path)
        logger.info(f"Number of chunks with reloaded size ({NEW_CHUNK_SIZE}): {len(chunks)}")
        
    finally:
        # Restore original value
        config["chunk_size"] = original_size
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Restored original chunk size: {original_size}")
    
    logger.info("Chunk size test completed.")

if __name__ == "__main__":
    test_global_chunk_size() 