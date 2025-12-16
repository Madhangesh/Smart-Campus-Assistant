import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks):
    texts = [c["content"] for c in chunks if c["content"].strip()]

    if len(texts) == 0:
        return np.empty((0, 384))  # 384 = MiniLM embedding size

    embeddings = model.encode(texts)
    return np.array(embeddings)
