import requests
from document_loader import get_vector_store
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def answer_question(question: str):
    vector_store = get_vector_store()

    if vector_store is None:
        return "No document uploaded yet."

    # Convert question to embedding
    question_embedding = embedding_model.encode(question)

    # Retrieve relevant document chunks
    docs = vector_store.similarity_search_by_vector(
        question_embedding,
        k=3
    )

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an AI assistant.
Answer ONLY using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()
