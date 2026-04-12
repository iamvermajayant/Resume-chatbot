from config import settings

def generate_answer(query):
    from embed import get_embedding
    from store import search
    from google import genai

    # Init Gemini inside function
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    # Step 1: Embed query
    query_embedding = get_embedding([query])[0]

    # Step 2: Search similar chunks
    docs = search(query_embedding, top_k=3)

    context = "\n".join(docs)

    # Step 3: Prompt
    prompt = f"""
    You are Jayant's AI assistant.
    Answer ONLY from the context.

    Context:
    {context}

    Question:
    {query}

    If not found, say "I don't have that information."
    """

    # Step 4: Gemini call
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text, docs