# 📄 Local PDF Intelligence – RAG Application

A locally running Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content using AI.

Built using **Python, FastAPI, Ollama, and ChromaDB**, this application retrieves relevant information from uploaded documents and uses a locally running LLM to generate context-aware answers.

The application makes it possible to interact with PDF documents conversationally without relying on external LLM APIs.

## 🚀 Features

- **PDF Upload:** Upload PDF documents to build a searchable knowledge base.
- **Document Processing:** Extract text from uploaded PDF files.
- **Text Chunking:** Split documents into smaller chunks for efficient retrieval.
- **Embedding Generation:** Convert text chunks into vector embeddings.
- **Vector Storage:** Store embeddings and document content in ChromaDB.
- **Semantic Search:** Retrieve relevant document sections based on the meaning of a user's question.
- **AI-Powered Question Answering:** Ask questions about uploaded PDFs and receive context-aware answers.
- **Local LLM Integration:** Use Ollama to run language models locally.
- **REST API:** FastAPI provides endpoints for document uploads and question answering.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend API development |
| Ollama | Local LLM and embedding model execution |
| ChromaDB | Vector database for storing embeddings |
| PyPDF | PDF text extraction |
| Embeddings | Semantic representation of text |
| Uvicorn | ASGI server |

## 🏗️ RAG Architecture

The application follows a Retrieval-Augmented Generation pipeline.

### 1. Document Ingestion
- User uploads a PDF.
- Text is extracted from the document using PyPDF.

### 2. Text Chunking
- Extracted text is divided into smaller chunks.
- Chunking helps improve retrieval accuracy and provides relevant context to the LLM.

### 3. Embedding Generation
- Each text chunk is converted into a numerical vector using an embedding model through Ollama.

### 4. Vector Storage
- Generated embeddings and their corresponding text chunks are stored in ChromaDB.

### 5. Query Processing
- User submits a question.
- The question is converted into an embedding.
- ChromaDB performs semantic similarity search to retrieve relevant chunks.

### 6. Response Generation
- Retrieved document content is passed to the locally running LLM through Ollama.
- The LLM uses the retrieved context to generate an answer.

## 🔄 Workflow

```text
             PDF Upload
                  |
                  v
          Text Extraction
                  |
                  v
             Chunking
                  |
                  v
        Embedding Generation
                  |
                  v
             ChromaDB
          (Vector Storage)
                  |
                  |
User Question ----+
       |
       v
Question Embedding
       |
       v
Semantic Similarity Search
       |
       v
Retrieved Context
       |
       v
   Ollama LLM
       |
       v
  Generated Answer
```

## 📁 Project Structure

```text
RAG-Application/
│
├── main.py
├── chroma_store/
├── uploads/
├── requirements.txt
├── .env
└── README.md
```

*Note: Update this structure to match your actual project folders and files.*

## ⚙️ Installation and Setup

### Prerequisites

- Python installed
- Ollama installed
- Required Ollama models downloaded

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd RAG-Application
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Ollama Models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 5. Start Ollama

```bash
ollama serve
```

### 6. Run FastAPI

```bash
uvicorn main:app --reload
```

### 7. Open API Documentation

Visit:

```text
http://127.0.0.1:8000/docs
```

## 🧠 Key Concepts Implemented

- Retrieval-Augmented Generation (RAG)
- Text extraction and preprocessing
- Text chunking and chunk overlap
- Document embeddings
- Vector databases
- Semantic similarity search
- Context retrieval
- Prompt construction
- Local LLM inference
- REST API development using FastAPI

## 🔮 Future Improvements

- Support multiple document formats.
- Add source citations and page references.
- Implement conversation history.
- Add document management and deletion.
- Improve retrieval using reranking.
- Build an interactive frontend.
- Add RAG evaluation metrics.

## 🎯 Project Goal

The goal of this project is to build a locally running document intelligence system that connects document retrieval with language generation, allowing users to interact with their own PDF knowledge base.

**Built with Python | FastAPI | Ollama | ChromaDB** 🚀
