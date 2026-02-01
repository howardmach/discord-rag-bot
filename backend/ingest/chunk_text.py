# Split text into overlapping chunks for better retrieval
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0
    text_len = len(text)

    # Loop until end of text
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # move with overlap

    return chunks