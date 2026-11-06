import chromadb
import pypdf
import ollama

# Ollama Model Configuration

CHAT_MODEL = "qwen2.5:3b"
EMBED_MODEL = "nomic-embed-text"

# RAG Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3

UPLOAD_FOLDER='uploads'
ALLOWED_EXTENSIONS={'.pdf'}

#Vector db configurations
client =chromadb.PersistentClient(path='./chroma_store')
COLLECTION_NAME='documents'


from pypdf import PdfReader

def extract_text(filepath):
    if filepath.lower().endswith('.pdf'):
        reader= PdfReader(filepath)
        return '\n'.join(page.extract_text() or "" for page in reader.pages)
    with open(filepath,'r',encoding='utf-8',errors='ignore') as f:
        return f.read()

def chunk_text(text,size=CHUNK_SIZE,overlap=CHUNK_OVERLAP):
    text=text.strip()
    if not text:
        return []
    
    chunks=[]
    start=0
    step= max(size-overlap,1)
    while start< len(text):
        chunk=text[start:start+size].strip()
        if chunk:
          chunks.append(chunk)
          start+=step
    return chunks


def embed(text):
    response= ollama.embeddings(model=EMBED_MODEL,prompt=text)
    return response['embedding']

def _fresh_collection():
    try:
       client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    return client.get_or_create_collection(COLLECTION_NAME)

def index_file(filepath):
    text=extract_text(filepath)
    chunks=chunk_text(text)
    if not chunks:
        raise ValueError(
            "Couldn't read any text from that file. "
            "If it's a scanned PDF (just images),it has no selected text."
        )
    collection= _fresh_collection()

    embeddings=[embed(chunk) for chunk in chunks]
    ids=[f"chunk-{i}" for i in range(len(chunks))]

    collection.add(ids=ids,documents=chunks,embeddings=embeddings)
    return len(chunks)


def retrieve(question,k=TOP_K):
    collection= client.get_or_create_collection(COLLECTION_NAME)

    question_vector =embed(question)
    results=collection.query(
        query_embeddings=[question_vector],
        n_results=k
    )
    return results['documents'][0] if results['documents'] else []


def answer(question,model=CHAT_MODEL):
    chunks =retrieve(question)
    if not chunks:
        return "No document loaded yet. Upload a file first ,then ask away."
    context = "\n\n".join(chunks)
    prompt=(
        "Use onle the context below to answer the question."
        "If the answer isn't in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:{question}"
    )

    response = ollama.chat(
        model=model or CHAT_MODEL,
        messages=[
            {
                'role':'user',
                'content':prompt
            }
        ],
    )
    return response['message']['content']

def has_document():
    try:
        collection= client.get_or_create_collection(COLLECTION_NAME)
    except Exception:
        return False

def list_chat_models():
    data=ollama.list()
    models = data.get("models",[]) if isinstance(data,dict) else data.models 

    names=[]

    for m in models:
        name =m.get('model') or m.get('name') if isinstance(m,dict) else getattr(m,"model",None)
        if name and 'embed' not in name.lower():
            names.append(name)
    return sorted(names)


