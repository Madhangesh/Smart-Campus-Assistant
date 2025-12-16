def retrieve_chunks(indices, chunks):
    results = []
    for i in indices:
        i = int(i)  # <-- CAST TO INTEGER
        if i < len(chunks):
            results.append(chunks[i])
    return results
