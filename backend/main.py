from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from qa_engine import answer_question
from document_loader import load_document

app = FastAPI(title="AI Knowledge Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    path = load_document(file)
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": path
    }

@app.get("/ask")
async def ask(question: str):
    return {"answer": answer_question(question)}
