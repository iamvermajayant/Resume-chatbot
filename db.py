import chromadb
from config import settings

# ✅ THIS IS THE FIX
client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)

collection = client.get_or_create_collection(name="resume")


def add_documents(chunks, embeddings):
    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )


def query_db(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    return results["documents"][0] if results["documents"] else []


def debug_count():
    return collection.count()