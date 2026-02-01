import chromadb

# Create a persistent Chroma client (new API)
chroma_client = chromadb.PersistentClient(path="chroma/index")

# Create or load the collection
collection = chroma_client.get_or_create_collection(
    name="bootcamp_docs",
    metadata={"hnsw:space": "cosine"}  # cosine similarity
)