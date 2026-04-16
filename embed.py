from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    use_auth_token=os.getenv("HF_TOKEN")
)

def get_embedding(texts):
    return model.encode(texts)