from sentence_transformers import SentenceTransformer

# Load model once (ok here)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(texts):
    return model.encode(texts)