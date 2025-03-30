import os
import time
import logging
import concurrent.futures
from tqdm import tqdm
import json
import os
from .config import print_config_info, CHUNK_SIZE
from .log_processor import chunk_log_file, retrieve_rag_context
from .hyperparameter import run_optuna_study
from .rag import reranker
from .llm_analysis import run_llm_analysis, generate_final_report

# Define default file name that can be overridden from outside
file_name = os.path.join("data", "logs", "Complete_Android_log (1).txt")

def main():
    print_config_info()
    
    # Create data/logs directory if it doesn't exist
    logs_dir = os.path.join("data", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Using the globally defined file_name
    global file_name
    
    if not os.path.exists(file_name):
        logging.error(f"Log file not found at: {file_name}")
        return
    logging.info(f"Reading log file from: {file_name}")

    try:
        # Chunk the log file
        log_chunks = chunk_log_file(file_name, chunk_size=CHUNK_SIZE, overlap_ratio=0.1)

        # Run hyperparameter tuning with Optuna
        study = run_optuna_study(log_chunks, reranker)
        best_multiplier = study.best_trial.params["reranker_multiplier"]
        logging.info(f"Optuna selected best reranker multiplier: {best_multiplier}")

        with open("best_params.json", "w") as f:
            json.dump(study.best_trial.params, f)
        logging.info("Best hyperparameters have been saved to best_params.json")

        # Retrieve RAG context for each log chunk
        rag_results = retrieve_rag_context(file_name, reranker)

        llm_results = []
        available_threads = os.cpu_count() or 1
        num_workers = min(available_threads, len(rag_results))
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_index = {executor.submit(run_llm_analysis, idx, result): idx for idx, result in enumerate(rag_results)}
            for future in tqdm(concurrent.futures.as_completed(future_to_index),
                               total=len(rag_results), desc="LLM Analysis"):
                idx, llm_response, mem = future.result()
                print(f"\n--- LLM Analysis for Log Chunk {idx+1} ---")
                print(llm_response)
                mem_data = mem.load_memory_variables({})
                print(f"\nChat History for Log Chunk {idx+1}:")
                for msg in mem_data["history"]:
                    print(msg.content)
                llm_results.append((idx, llm_response, mem))

        llm_results.sort(key=lambda x: x[0])

        structured_messages = []
        for idx, response, mem in llm_results:
            mem_data = mem.load_memory_variables({})
            for msg in mem_data["history"]:
                # Try to parse JSON from each message
                content = msg.content
                try:
                    # If it's valid JSON, keep it as is
                    json_obj = json.loads(content.strip().replace('```json', '').replace('```', '').strip())
                    structured_messages.append({
                        "chunk_index": idx,
                        "data": json_obj
                    })
                except json.JSONDecodeError:
                    # If not valid JSON, store as plain text with chunk index
                    structured_messages.append({
                        "chunk_index": idx,
                        "data": {"text": content}
                    })

        # Convert to well-formatted JSON string
        structured_data_json = json.dumps(structured_messages, indent=2)
        print("\n\n=== Structured Data for Final LLM ===\n")
        print(structured_data_json)
        
        # Generate final report using the structured data
        final_report_summary = generate_final_report(structured_messages)
        print("\nFinal Report Summary:")
        print(final_report_summary)
        return llm_results
    finally:
        # Cleanup reranker
        if hasattr(reranker, 'stop_self_pool'):
            try:
                reranker.stop_self_pool()
            except:
                pass
        if hasattr(reranker, 'close'):
            try:
                reranker.close()
            except:
                pass

if __name__ == '__main__':
    main()
