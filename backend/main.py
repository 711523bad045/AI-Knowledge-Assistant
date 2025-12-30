from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from qa_engine import answer_question
from document_loader import load_document
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from document_loader import load_document
from qa_engine import answer_question

app = FastAPI(title="AI Knowledge Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Knowledge Assistant Backend Running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    path = load_document(file)
    return {
        "message": "File uploaded and indexed successfully",
        "filename": file.filename,
        "path": path
    }

@app.get("/ask")
async def ask(question: str):
    answer = answer_question(question)
    return {"answer": answer}
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
