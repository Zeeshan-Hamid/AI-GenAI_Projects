# WikiWise: A Semantic Search Engine for Wikipedia Movie Plots 🎥

WikiWise is a semantic search system that enhances how users interact with large text datasets. Using advanced Natural Language Processing (NLP) techniques, WikiWise bridges the gap between traditional keyword searches and contextual understanding, providing more relevant and meaningful results. This project focuses on movie plot summaries from Wikipedia, creating an efficient and user-friendly semantic search engine.

## Features 🚀
- **Semantic Search**: Context-aware retrieval using state-of-the-art language models.
- **Multiple Embedding Techniques**: Includes models like BERT, SBERT, BGE-3, and Snowflake.
- **Efficient Retrieval**: Integration with FAISS (Facebook AI Similarity Search) for fast and scalable vector search.
- **Fine-Tuned Model**: SBERT fine-tuned on synthetic queries for enhanced accuracy.
- **User-Friendly Deployment**: Backend built with FASTAPI and frontend developed using React for smooth interaction.

---

## Project Workflow 🛠️

### 1. **Data Collection and Preprocessing**
- Dataset: 34,800 Wikipedia movie plot articles.
- Preprocessing:
  - Text cleaning (lowercase, punctuation removal).
  - Stopword removal and tokenization.
  - Filtering articles to fit model constraints (≤ 512 tokens).

### 2. **Embedding Generation**
- Models used:
  - **BERT**: Contextual understanding of words.
  - **BGE-3**: Optimized for semantic textual search.
  - **Snowflake**: High-dimensional embeddings.
  - **SBERT**: Sentence-level embeddings for semantic understanding.

### 3. **Efficient Search with FAISS**
- Indexed SBERT embeddings using FAISS for fast similarity searches.
- FAISS accelerated the retrieval process with approximate nearest neighbor (ANN) search.

### 4. **Fine-Tuning SBERT**
- Synthetic queries generated using **T5** to simulate user inputs.
- SBERT fine-tuned on query-plot pairs using **Multiple Negative Ranking Loss**.
- Improved query understanding and retrieval accuracy.

### 5. **Deployment**
- Backend: **FASTAPI** for query processing and model inference.
- Frontend: **React** for an interactive and intuitive user interface.
- Models loaded using **pickle** for runtime efficiency.

---

## Results 📊

### Performance Metrics:
- Fine-tuned SBERT with FAISS achieved the best results:
  - **Query Accuracy**: 86% (correctly matched 180 out of 209 queries).
  - **Precision for Malignant Queries**: 94%.
- Improved retrieval speed and contextual relevance compared to baseline models.

### Model Comparison:
| **Model**               | **Accuracy** | **Matched Queries** |
|--------------------------|--------------|----------------------|
| BERT                    | 31%          | ~65                 |
| BGE                     | 40%          | ~85                 |
| Snowflake               | 38%          | ~80                 |
| SBERT                   | 53%          | ~110                |
| SBERT with FAISS        | 60%          | ~125                |
| Fine-tuned SBERT + FAISS| 86%          | ~180                |

---

