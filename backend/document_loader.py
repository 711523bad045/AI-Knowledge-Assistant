import os
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

UPLOAD_DIR = "uploads"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

index = None
documents = []


def simple_text_splitter(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def extract_text(file_path):
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
    global index, documents

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    text = extract_text(file_path)
    chunks = simple_text_splitter(text)

    embeddings = embedding_model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    if index is None:
        index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)
    documents.extend(chunks)

    return {"chunks_added": len(chunks)}


def get_vector_store():
    return index, documents
