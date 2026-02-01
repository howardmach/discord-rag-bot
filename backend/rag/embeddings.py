from sentence_transformers import SentenceTransformer

# Lazy-load embedding model
_model = None

# Get the embedding model, loading it if necessary
def get_model():
    global _model
    if _model is None:
        # Use BGE-small-en-v1.5 (local, no API key)
        _model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    return _model

# Embed a list of texts into vectors
def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    return model.encode(texts, normalize_embeddings=True).tolist()

# Embed a single query text into a vector
def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]