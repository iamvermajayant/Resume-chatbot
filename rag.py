from config import settings
from embed import get_embedding
from db import query_db
from google import genai

# Initialize client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_answer(query):
    # Step 1: Embed query
    query_embedding = get_embedding([query])[0]

    # Step 2: Retrieve context
    docs = query_db(query_embedding)
    context = "\n".join(docs)

    # Step 3: Prompt
    prompt = f"""
    You are Jayant's AI assistant.
    Answer ONLY from the context below.

    Context:
    {context}

    Question:
    {query}

    If not found, say: "I don't have that information."
    """

    # ✅ NEW API CALL
    response = client.models.generate_content(
        model="gemini-2.5-flash",   # ✅ correct model
        contents=prompt
    )

    return response.text, docs