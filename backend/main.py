from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from qa_engine import answer_question
from document_loader import load_document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    result = load_document(file)
    return {"message": "File processed", "details": result}

@app.get("/ask")
def ask(question: str):
    answer = answer_question(question)
    return {"answer": answer}
