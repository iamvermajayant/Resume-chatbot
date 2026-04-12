import numpy as np

documents = []
embeddings = None


def store_data(chunks, emb):
    global documents, embeddings
    documents = chunks
    embeddings = np.array(emb)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query_embedding, top_k=3):
    scores = []

    for i, emb in enumerate(embeddings):
        score = cosine_similarity(query_embedding, emb)
        scores.append((score, documents[i]))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [doc for _, doc in scores[:top_k]]