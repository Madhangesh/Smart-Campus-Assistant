import spacy

nlp = spacy.load("en_core_web_sm")

def summarize(chunks, mode="Short"):
    text = " ".join([c["content"] for c in chunks[:10]])
    doc = nlp(text)
    sentences = [s.text for s in doc.sents]

    if mode == "Short":
        return sentences[:5]
    return sentences[:12]
