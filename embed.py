# from sentence_transformers import SentenceTransformer

# # Load model once (ok here)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def get_embedding(texts):
#     return model.encode(texts)



from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    use_auth_token=os.getenv("HF_TOKEN")
)