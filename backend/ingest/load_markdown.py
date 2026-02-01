import os

# Load all markdown files from the /data folder
def load_markdown_files(folder: str = "data"):
    docs = []
    for fname in os.listdir(folder):
        if fname.endswith(".md"):
            path = os.path.join(folder, fname)
            with open(path, "r", encoding="utf-8") as f:
                docs.append({
                    "id": fname,                     # use filename as ID
                    "title": fname.replace(".md", ""),  # title without extension
                    "content": f.read()              # markdown text
                })
    return docs