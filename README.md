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

```text
discord-rag-bot/
├── backend/                   # Core RAG engine and API logic
│   ├── main.py                # Main backend application entry point
│   ├── rag/                   # Retrieval-Augmented Generation module
│   │   ├── embeddings.py      # Generates text vector embeddings via BGE
│   │   ├── vectorstore.py     # ChromaDB initialization and connection
│   │   ├── retrieval.py       # Queries the database for context matching
│   │   ├── llm.py             # Interfaces with the Language Model 
│   │   └── pipeline.py        # Combines retrieval and generation workflows
│   └── ingest/                # Data pipeline for populating the database
│       ├── load_markdown.py   # Parses source files from the data directory
│       ├── chunk_text.py      # Splits documents into optimal semantic sizes
│       └── build_vectorstore.py# Embeds chunks and saves them to ChromaDB
├── discord_bot/               # Discord gateway application
│   └── bot.py                 # Handles bot logic, events, and !ask commands
├── data/                      # Storehouse for your source documentation
│   └── <your markdown files>  # Raw .md context files (e.g., knowledge base)
├── chroma/                    # Local persistent storage for vector data
│   └── index/                 # Binary index files managed by ChromaDB
├── .env                       # Environment variables (API keys, bot tokens)
└── requirements.txt           # Project dependencies and pinned packages
```

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

```
python -m venv .venv
.\.venv\Scripts\activate
```

For VS Code users,

1. **Open the Project Folder**
   Launch VS Code and open the repository folder via `File` > `Open Folder...` (Select `discord-rag-bot`).

2. **Open the Command Palette**
   Access the VS Code command hub using your operating system's shortcut:
   * **Windows/Linux:** `Ctrl + Shift + P`
   * **Mac:** `Cmd + Shift + P`

3. **Select the Create Tool**
   Type `Python: Create Environment` into the search bar and select it from the dropdown options.

4. **Choose Environment Type**
   When prompted, select **`Venv`** to utilize Python's native virtual environment module.

5. **Select Python Interpreter**
   Choose your preferred Python version from the global list installed on your computer (e.g., *Python 3.12* or *Python 3.13*).

6. **Automate Dependency Installation**
   If a `requirements.txt` file is present in your directory, VS Code will display a checkbox next to it. 
   * **Check the box** next to `requirements.txt` to automatically install all dependencies.
   * Click **OK**.

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

There is no download needed as **bge-small-en-v1.5** is part of **sentence-transformers**.

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

---

## 🔐 Discord Bot Setup

## 🤖 Setting Up the Discord Bot Application

Follow these steps to create your Discord developer application, configure its permissions, and connect it to your server.

### Step-by-Step Configuration

1. **Create the Application**
   * Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   * Click the **New Application** button in the top right.
   * Name your application (e.g., `RAG Assistant`) and click **Create**.

2. **Generate the Bot Invite URL**
   * In the left sidebar, navigate to **OAuth2** → **URL Generator**.
   * Under the **Scopes** section, check the box for:
     * [x] `bot`

3. **Configure Bot Permissions**
   * Once you check `bot`, a **Bot Permissions** grid will appear below. Enable the following settings:
     * [x] `Manage Channels`
     * [x] `Send Messages`
     * [x] `Read Message History`
     * [x] `Manage Messages`

4. **Invite the Bot to Your Server**
   * Scroll to the bottom of the page and **Copy** the uniquely generated URL.
   * Create a new Discord server (or open an existing one where you have administrative access).
   * Paste the copied URL into a new browser tab, select your server, and authorize the bot.

5. **Configure Environment Tokens**
   * Return to your project directory. 
   * Locate your environment configuration file (e.g., `.env` or configuration file) and replace the placeholder text with your actual token:
     ```
     YOUR_DISCORD_BOT_TOKEN
     ```

6. **Launch and Test**
   * **Start Local Host:** Spin up your bot locally on your machine. *(For the exact startup commands, reference the **Run Discord Bot** section below).*
   * **Verify Connection:** Ensure the bot appears as "Online" in your Discord server's member list.
   * **Run Test Commands:** In any text channel the bot has access to, verify its RAG functionality by running the following test queries:
      ```
      !ask hello
      ```
      and then:
      ```
      !ask What is the AI Bootcamp Journey?
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

## Feedback System

After the bot sends an answer, users can manually react with 👍 or 👎 to rate the response.

The bot does not add reactions automatically and does not react to its own messages.

When a user adds a reaction, the bot records the feedback and sends it to the FastAPI backend for logging or analytics.

---

## 📌 Future Enhancements

- Reranking with BGE cross-encoder  
- Conversation memory  
- Slash commands (`/ask`)  
- Streaming responses  
- Retrieval debugging UI  
- Web dashboard for chunk inspection  