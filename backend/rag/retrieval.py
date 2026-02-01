from .embeddings import embed_query
from .vectorstore import collection

# Retrieve top-k relevant chunks
def retrieve_relevant_docs(query: str, k: int = 5):
    qvec = embed_query(query)

    results = collection.query(
        query_embeddings=[qvec],
        n_results=k
    )

    docs = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        docs.append({
            "title": meta.get("title", "Untitled"),
            "chunk_id": meta.get("chunk_id", 0),
            "content": text
        })

    return docs