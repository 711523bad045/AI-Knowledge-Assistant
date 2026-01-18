import numpy as np
from sentence_transformers import SentenceTransformer
from document_loader import get_vector_store

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def answer_question(question: str):
    index, documents = get_vector_store()

    if index is None or not documents:
        return "No document uploaded yet."

    query_embedding = embedding_model.encode([question]).astype("float32")
    distances, indices = index.search(query_embedding, k=3)

    answers = [documents[i] for i in indices[0] if i < len(documents)]
    return " ".join(answers)
