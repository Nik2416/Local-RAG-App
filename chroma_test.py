import chromadb
import ollama


# PersistentClient()	Creates a database that saves data locally
# 1. Create a persistent ChromaDB client
client=chromadb.PersistentClient(
  path="./chroma_db"
)


# get_or_create_collection()	Creates a collection or opens an existing one
# 2. Create a Collection
collection=client.get_or_create_collection(
  name='pdf_documents',
  metadata={"hnsw:space":"cosine"}
)

#3. Sample documents
documents=[
  "Machine learning is a branch of artificial intelligence.",
  "Python is a popular programming language for data science.",
  "Deep learning uses neural networks to learn complex patterns."
]



#4. Generate embeddings using Ollama 
response=ollama.embed(
  model='nomic-embed-text',
  input=documents
)

embeddings= response['embeddings']


# upsert()	Inserts new records or updates existing IDs
#5. Store documents and embeddings in ChromaDB
collection.upsert(
  ids=['docs1','docs2','docs3'],
  documents=documents,
  embeddings=embeddings,
  metadatas=[
    {'source':'sample.pdf','page':1},
    {'source':'sample.pdf','page':2},
    {'source':'sample.pdf','page':3}
  ]
)

print('Documents stored successfully!')

#6.Search for relevant documents
question = 'What is artificial intelligence?'

query_response= ollama.embed(
  model='nomic-embed-text',
  input=question
)

query_embedding=query_response['embeddings'][0]


# query()	Searches for similar vectors
results=collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print('\nRelevant Documents:')

for document in results["documents"][0]:
  print(document)