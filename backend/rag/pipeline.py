from .retrieval import retrieve_relevant_docs
from .llm import call_llama

# Build context from retrieved chunks
def build_context(docs):
    parts = []
    for d in docs:
        parts.append(f"# {d['title']} (chunk {d['chunk_id']})\n{d['content']}")
    return "\n\n---\n\n".join(parts)

# Build RAG prompt
def build_prompt(user_query: str, context: str) -> str:
    return f"""You are a helpful assistant answering questions about an AI bootcamp.

Use ONLY the following context to answer the question. 
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{user_query}

Answer:"""

# Full RAG pipeline
def rag_answer(user_query: str) -> str:
    docs = retrieve_relevant_docs(user_query, k=5)
    context = build_context(docs)
    prompt = build_prompt(user_query, context)
    answer = call_llama(prompt)
    return answer.strip()