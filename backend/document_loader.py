import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

UPLOAD_DIR = "uploads"
VECTOR_DB_DIR = "vector_store"

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Global vector store
vector_store = None


def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    return ""


def load_document(file):
    global vector_store

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Extract text
    text = extract_text(file_path)

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)

    # Create embeddings
    embeddings = embedding_model.encode(chunks)

    # Store in FAISS
    vector_store = FAISS.from_embeddings(
        list(zip(chunks, embeddings)),
        embedding_model
    )

    return file_path


def get_vector_store():
    return vector_store
