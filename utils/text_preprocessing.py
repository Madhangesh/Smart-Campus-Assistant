# import spacy

# nlp = spacy.load("en_core_web_sm")

# def clean_and_chunk(text, chunk_size=5):
#     doc = nlp(text)
#     sentences = [sent.text.strip() for sent in doc.sents if len(sent.text) > 20]

#     chunks = []
#     for i in range(0, len(sentences), chunk_size):
#         chunk = " ".join(sentences[i:i+chunk_size])
#         chunks.append(chunk)

#     return chunks
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_and_chunk(pages, chunk_size=4):
    chunks = []

    for page in pages:
        doc = nlp(page["text"])
        sentences = [s.text.strip() for s in doc.sents if len(s.text) > 25]

        for i in range(0, len(sentences), chunk_size):
            chunk_text = " ".join(sentences[i:i+chunk_size])
            chunks.append({
                "content": chunk_text,
                "page": page["page"],
                "source": page["source"]
            })
    return chunks
