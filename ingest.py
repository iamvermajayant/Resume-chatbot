import pdfplumber
from embed import get_embedding
from store import store_data


def load_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text


def chunk_text(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def run_ingestion():
    print("📄 Loading PDF...")

    text = load_pdf("data/resume.pdf")

    print("✂️ Chunking...")
    chunks = chunk_text(text)

    print("🧠 Creating embeddings...")
    embeddings = get_embedding(chunks)

    print("💾 Storing in memory...")
    store_data(chunks, embeddings)

    print("✅ Ingestion done!")