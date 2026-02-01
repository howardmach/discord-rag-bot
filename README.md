# Discord RAG Bot

A fully local, privacy-preserving Retrieval-Augmented Generation (RAG) chatbot that runs inside Discord.  
Powered by:

- FastAPI backend  
- ChromaDB vector store  
- BGE-small-en-v1.5 embeddings  
- Llama 3.2 (3B) running locally via Ollama  
- Discord bot interface  
- Markdown knowledge base stored locally  

No API keys. No cloud dependencies. 100% offline.

---

## 📁 Project Structure

discord-rag-bot/
  backend/
    main.py
    rag/
      embeddings.py
      vectorstore.py
      retrieval.py
      llm.py
      pipeline.py
    ingest/
      load_markdown.py
      chunk_text.py
      build_vectorstore.py
  discord_bot/
    bot.py
  data/
    <your markdown files>
  chroma/
    index/
  .env
  requirements.txt

---

## 🚀 Features

- Local Llama model via Ollama  
- Local embeddings using BGE-small-en-v1.5  
- Local vector store using ChromaDB PersistentClient  
- Markdown knowledge base ingestion with chunking + metadata  
- FastAPI `/chat` endpoint for RAG responses  
- Discord bot command: `!ask <your question>`  
- Fully offline, no external services  

---

## 🛠️ Installation

### 1. Clone the repository

git clone <your-repo-url>
cd discord-rag-bot

### 2. Create a virtual environment

python -m venv .venv
.\.venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

---

## 📦 Model Setup

### Install Ollama

https://ollama.com/download

### Pull the Llama model

ollama pull llama3.2:3b

### Start Ollama

ollama serve

---

## 🧠 Embedding Model (BGE-small-en)

The backend uses:

BAAI/bge-small-en-v1.5

To download it locally:

python - <<EOF
from sentence_transformers import SentenceTransformer
SentenceTransformer("BAAI/bge-small-en-v1.5")
EOF

---

## 📄 Knowledge Base

Place your `.md` files inside:

data/

Example:

data/AI_Bootcamp_Journey.md  
data/AI_Engineer_Training.md  
data/AI_Bootcamp_Intern_FAQ.md  

---

## 📚 Build the Vector Store

From the project root:

python -m backend.ingest.build_vectorstore

This loads markdown files, chunks them, embeds them, and stores them in ChromaDB.

---

## ⚙️ Environment Variables

Create a `.env` file:

DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN  
LLAMA_ENDPOINT=http://localhost:11434/api/generate  

---

## 🌐 Run the FastAPI Backend

uvicorn backend.main:app --reload --port 8000

Test it:

http://127.0.0.1:8000/docs

---

## 🤖 Run the Discord Bot

python -m discord_bot.bot

In Discord:

!ask What is the AI Bootcamp Journey?

---

## 🔐 Discord Bot Setup

1. Go to https://discord.com/developers/applications  
2. Click **“New Application”**  
3. Give your application a name (e.g., “RAG Assistant”) and click **Create**   
4. In the left sidebar, go to **OAuth2 → URL Generator**  
5. Under **Scopes**, check:  
   - `bot`  
6. Under **Bot Permissions**, enable:  
    - Manage Channels  
    - Send Messages  
    - Read Message History
    - Manage Messages  
7. Copy the generated URL
8. Create a Discord server to host the bot  
9. Paste it into your browser and invite the bot to your Discord server  
10. Back in your project, put your bot token into `.env` as:  
    ```
    DISCORD_TOKEN=YOUR_BOT_TOKEN
    ```  
11. Start your bot locally with:  
    ```
    python discord_bot/bot.py
    ```  
12. In Discord, test it with:  
    ```
    !ask hello
    ```  

---

## 🧩 How It Works (RAG Pipeline)

1. User sends `!ask <question>` in Discord  
2. Discord bot sends the question to FastAPI  
3. FastAPI retrieves top-k chunks from ChromaDB  
4. Builds a context block  
5. Sends prompt + context to Llama  
6. Returns the answer back to Discord  

Everything stays local.

---

## 📌 Future Enhancements

- Reranking with BGE cross-encoder  
- Conversation memory  
- Slash commands (`/ask`)  
- Streaming responses  
- Retrieval debugging UI  
- Web dashboard for chunk inspection  
