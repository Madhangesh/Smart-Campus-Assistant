import faiss
import numpy as np

def build_faiss_index(embeddings):
    if embeddings.ndim != 2 or embeddings.shape[0] == 0:
        raise ValueError("No valid embeddings found. Check PDF content.")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype("float32"))
    return index

def search_index(index, query_embedding, k=5):
    return index.search(query_embedding.astype("float32"), k)
