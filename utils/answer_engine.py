import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def build_answer(question, chunks, model):
    q_vec = model.encode([question])
    sentences = []

    for c in chunks:
        doc = nlp(c["content"])
        for sent in doc.sents:
            if len(sent.text) > 20:
                s_vec = model.encode([sent.text])
                score = cosine_similarity(q_vec, s_vec)[0][0]
                sentences.append({
                    "text": sent.text,
                    "score": score,
                    "source": c["source"],
                    "page": c["page"]
                })

    sentences = sorted(sentences, key=lambda x: x["score"], reverse=True)[:3]
    answer = " ".join([s["text"] for s in sentences])
    confidence = round(np.mean([s["score"] for s in sentences]), 2)

    return answer, confidence, sentences
