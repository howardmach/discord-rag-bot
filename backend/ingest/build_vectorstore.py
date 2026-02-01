import uuid
from ..rag.vectorstore import collection
from ..rag.embeddings import embed_texts
from .load_markdown import load_markdown_files
from .chunk_text import chunk_text

# Build vector store with chunking
def build_vectorstore():
    docs = load_markdown_files()

    ids = []
    texts = []
    metadatas = []

    # Loop through markdown docs
    for d in docs:
        chunks = chunk_text(d["content"], chunk_size=500, overlap=100)

        # Add each chunk separately
        for idx, chunk in enumerate(chunks):
            ids.append(str(uuid.uuid4()))  # unique ID
            texts.append(chunk)            # chunk text
            metadatas.append({
                "title": d["title"],       # original doc title
                "chunk_id": idx            # chunk number
            })

    # Embed all chunks
    embeddings = embed_texts(texts)

    # Add to ChromaDB
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Indexed {len(texts)} chunks into ChromaDB.")

if __name__ == "__main__":
    build_vectorstore()