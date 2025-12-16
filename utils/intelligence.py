from collections import Counter
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_topics(chunks):
    nouns = []
    for c in chunks:
        doc = nlp(c["content"])
        nouns.extend([t.text.lower() for t in doc if t.pos_ == "NOUN"])

    return Counter(nouns).most_common(10)
