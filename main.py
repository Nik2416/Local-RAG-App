import os
import uvicorn

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app import (
    has_document,
    list_chat_models,
    index_file,
    answer,
    ALLOWED_EXTENSIONS,
    UPLOAD_FOLDER,
    CHAT_MODEL,
)
from werkzeug.utils import secure_filename
# -------------------------------
# Configuration
# -------------------------------

app = FastAPI(
    title="Offline PDF RAG Application",
    description="Chat with your PDFs using Ollama and ChromaDB",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")


app.state.upload_folder = UPLOAD_FOLDER
app.state.max_content_length = 25 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------------
# Request Model
# -------------------------------

class ChatRequest(BaseModel):
    question: str | None = None
    model: str | None = None


# -------------------------------
# Helper Function
# -------------------------------

def _allowed(filename: str) -> bool:
    return (
        os.path.splitext(filename)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# -------------------------------
# Home Route
# -------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "has_document": has_document()
        }
    )


# -------------------------------
# Get Available Ollama Models
# -------------------------------

@app.get("/api/models")
def api_models():

    try:
        models = list_chat_models()

        return {
            "models": models,
            "default": CHAT_MODEL
        }

    except Exception:

        return JSONResponse(
            status_code=500,
            content={
                "models": [],
                "error": "Couldn't reach Ollama."
            }
        )


# -------------------------------
# Upload PDF / TXT / MD
# -------------------------------

@app.post("/upload")
def upload(file: UploadFile = File(...)):

    if not file.filename:
        return JSONResponse(
            status_code=400,
            content={"error": "No file selected."}
        )

    if not _allowed(file.filename):
        return JSONResponse(
            status_code=400,
            content={
                "error": "Use a .pdf, .txt, or .md file."
            }
        )

    filename = secure_filename(file.filename)

    if not filename:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid filename."}
        )

    path = os.path.join(
        app.state.upload_folder,
        filename
    )

    # Read uploaded file
    contents = file.file.read()

    # Check maximum file size
    if len(contents) > app.state.max_content_length:
        return JSONResponse(
            status_code=413,
            content={"error": "File exceeds 25 MB limit."}
        )

    # Save file locally
    with open(path, "wb") as f:
        f.write(contents)

    try:
        chunk_count = index_file(path)

    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Couldn't process the file: {e}"
            }
        )

    return {
        "filename": filename,
        "chunks": chunk_count
    }


# -------------------------------
# Chat Route
# -------------------------------

@app.post("/chat")
def chat(data: ChatRequest):

    question = (data.question or "").strip()

    model = (data.model or "").strip() or CHAT_MODEL

    if not question:
        return JSONResponse(
            status_code=400,
            content={"error": "Ask a question first."}
        )

    try:
        reply = answer(question, model)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Couldn't get an answer: {e}"
            }
        )

    return {
        "answer": reply
    }


# -------------------------------
# Run Application
# -------------------------------

