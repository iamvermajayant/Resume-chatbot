import pdfplumber
from embed import get_embedding
from db import add_documents

def load_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    print("📄 Loading resume...")
    text = load_pdf("data/resume.pdf")

    print("✂️ Chunking text...")
    chunks = chunk_text(text)

    print("🧠 Generating embeddings...")
    embeddings = get_embedding(chunks)

    print("💾 Storing in ChromaDB...")
    add_documents(chunks, embeddings)

    print("✅ Ingestion complete!")