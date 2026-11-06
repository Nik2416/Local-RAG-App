CHAT_MODEL = "qwen2.5:3b"
EMBED_MODEL = "nomic-embed-text"

# RAG Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3

import ollama

# Test LLM
response = ollama.chat(
    model=CHAT_MODEL,
    messages=[
        {
            "role": "user",
            "content": "What is RAG?"
        }
    ]
)

print("LLM Response:")
print(response["message"]["content"])


# Test embedding model
embedding = ollama.embed(
    model=EMBED_MODEL,
    input="Artificial Intelligence is transforming technology."
)

print("\nEmbedding:")
print(embedding["embeddings"][0][:5])

print("\nEmbedding dimensions:")
print(len(embedding["embeddings"][0]))

# Ollama – Local LLM and model interaction.
# PDF Extraction – Reading PDF files using PyPDF.
# Text Chunking – Why we split documents.
# Embeddings – How text becomes vectors.
# ChromaDB – Storing and searching vectors.
# Retrieval – Finding relevant PDF chunks.
# Prompt Engineering – Passing retrieved content to the LLM.
# Flask – Connecting everything to a web interface.