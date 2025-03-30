import os
from langchain.text_splitter import TokenTextSplitter
from rank_bm25 import BM25Okapi
import statistics
import logging

from src.rag import rag_docs, vector_db
from src.config import LOG_STRUCTURE, CHUNK_SIZE
from src.utils import apply_severity_bonus, apply_error_type_bonus, compute_metadata_bonus

# Prepare BM25 scorer with the RAG documents
rag_corpus = [doc.page_content for doc in rag_docs]
tokenized_corpus = [doc.split() for doc in rag_corpus]
bm25 = BM25Okapi(tokenized_corpus)

def chunk_log_file(file_path, chunk_size=CHUNK_SIZE, overlap_ratio=0.1):
    with open(file_path, "r") as f:
        text = f.read()
    chunk_overlap_tokens = int(chunk_size * overlap_ratio)
    token_text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap_tokens)
    splits = token_text_splitter.split_text(text)
    final_chunks = []
    for idx, split in enumerate(splits):
        final_chunks.append((f"chunk_{idx+1}", split))
    return final_chunks

def process_chunk(key, chunk, reranker,
                  BM25_WEIGHT=1.0, RERANKER_MULTIPLIER=10.0,
                  RERANKER_WEIGHT=1.0, VECTOR_MULTIPLIER=10.0,
                  VECTOR_WEIGHT=1.0):
    query_tokens = chunk.split()
    bm25_scores = bm25.get_scores(query_tokens)
    vector_results = vector_db.similarity_search_with_score(chunk, k=len(rag_docs))
    vector_scores_map = {doc.page_content: 1 / (1 + score) for doc, score in vector_results}
    candidates = []
    chunk_lower = chunk.lower()
    for doc, bm25_score in zip(rag_docs, bm25_scores):
        metadata = doc.metadata
        error_type = metadata.get(LOG_STRUCTURE.get("error_field", "error_type"), "Unknown")
        severity = metadata.get(LOG_STRUCTURE.get("severity_field", "severity"), "low")
        node_id = metadata.get(LOG_STRUCTURE.get("node_field", "node_id"), "Unknown")
        patterns = [p.strip().lower() for p in metadata.get("patterns", "").split(",") if p.strip()]
        bonus = sum(5 for pattern in patterns if pattern in chunk_lower)
        bm25_component = bm25_score + bonus
        
        score_result = reranker.compute_score([chunk, doc.page_content], normalize=True)
        if isinstance(score_result, list):
            score_result = score_result[0] if score_result else 0.0
        rerank_score = float(score_result)
        rerank_component = rerank_score * RERANKER_MULTIPLIER
        
        vector_similarity = vector_scores_map.get(doc.page_content, 0)
        vector_component = vector_similarity * VECTOR_MULTIPLIER
        
        combined_score = (
            BM25_WEIGHT * bm25_component +
            RERANKER_WEIGHT * rerank_component +
            VECTOR_WEIGHT * vector_component
        )
        combined_score = apply_severity_bonus(combined_score, severity)
        combined_score = apply_error_type_bonus(combined_score, error_type)
        combined_score += compute_metadata_bonus(doc)
        candidates.append((doc, combined_score, bm25_component, rerank_component, vector_component))
    
    scores = [c[1] for c in candidates]
    if scores:
        mean_score = statistics.mean(scores)
        stdev_score = statistics.stdev(scores) if len(scores) > 1 else 0
        dynamic_threshold = max(mean_score + 0.5 * stdev_score, 25)
    else:
        dynamic_threshold = 25

    filtered = [
        {
            "description": doc.metadata.get("description", "N/A"),
            "error_type": doc.metadata.get("error_type", "N/A"),
            "severity": doc.metadata.get("severity", "N/A"),
            "resolution": doc.metadata.get("resolution", "N/A"),
            "combined_score": combined_score,
            "bm25_component": bm25_component,
            "reranker_component": rerank_component,
            "vector_component": vector_component
        }
        for doc, combined_score, bm25_component, rerank_component, vector_component in candidates
        if combined_score >= dynamic_threshold
    ]
    if not filtered and candidates:
        best = max(candidates, key=lambda x: x[1])
        filtered = [{
            "description": best[0].metadata.get("description", "N/A"),
            "error_type": best[0].metadata.get("error_type", "N/A"),
            "severity": best[0].metadata.get("severity", "N/A"),
            "resolution": best[0].metadata.get("resolution", "N/A"),
            "combined_score": best[1],
            "bm25_component": best[2],
            "reranker_component": best[3],
            "vector_component": best[4]
        }]
    filtered.sort(key=lambda x: x["combined_score"], reverse=True)
    return {
        "chunk_key": key,
        "log_chunk": chunk,
        "matches": filtered
    } if filtered else None

def retrieve_rag_context(file_path, reranker, chunk_size=CHUNK_SIZE, overlap_ratio=0.1):
    log_chunks = chunk_log_file(file_path, chunk_size=chunk_size, overlap_ratio=overlap_ratio)
    results = []
    for key, chunk in log_chunks:
        try:
            result = process_chunk(key, chunk, reranker)
            if result is not None:
                results.append(result)
        except Exception as e:
            logging.error(f"Error processing chunk ({key}): {e}")
    return results
