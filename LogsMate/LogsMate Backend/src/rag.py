import torch
import logging
from FlagEmbedding import FlagReranker
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from rag_docs.android_docs import android_rag_docs
from rag_docs.hdfs_docs import hdfs_rag_docs
from rag_docs.healthApp_docs import healthapp_rag_docs
from src.config import CONFIG, ACTIVE_LOG_TYPE, SUB_CONFIG

device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Using device: {device}")

# Initialize the FlagReranker
reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={"device": device}
)

# Retrieve the chroma directory from the active config
chroma_directory = SUB_CONFIG.get("chroma_directory", "./default_chroma")
logging.info(f"Using Chroma directory: {chroma_directory}")

# Map of log types to their respective RAG documents
rag_docs_map = {
    "hdfs": hdfs_rag_docs,
    "android": android_rag_docs,
    "healthapp": healthapp_rag_docs
}

# Initialize with appropriate documents based on active log type
rag_docs = rag_docs_map.get(ACTIVE_LOG_TYPE, android_rag_docs)
logging.info(f"Using RAG documents for log type: {ACTIVE_LOG_TYPE}")

# Initialize the vector database using the directory from the config
vector_db = Chroma(
    embedding_function=embedding_model,
    persist_directory=chroma_directory
)

# Load documents if the vector store is empty
if len(vector_db.get()["ids"]) == 0:
    logging.info(f"Vector store is empty. Adding documents for {ACTIVE_LOG_TYPE}...")
    vector_db.add_documents(rag_docs)
else:
    logging.info(f"Vector store already contains {len(vector_db.get()['ids'])} documents.")
