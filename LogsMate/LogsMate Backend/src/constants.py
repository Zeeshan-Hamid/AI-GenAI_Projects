import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Weights and multipliers for scoring
BM25_WEIGHT = 1.0
RERANKER_MULTIPLIER = 10.0
RERANKER_WEIGHT = 1.0
VECTOR_MULTIPLIER = 10.0
VECTOR_WEIGHT = 1.0
