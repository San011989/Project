from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import chromadb
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Restrict origins in production to your live frontend URL
origins = [
    "https://project-2q48.onrender.com",
    "http://localhost:5173",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-3.5-turbo"

class ChatRequest(BaseModel):
    message: str

def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured in environment")
    return key

def get_collection():
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        return chroma_client.get_collection(name="resume_data")
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="ChromaDB collection 'resume_data' not found. Please run init_db.py first."
        )

def get_embedding(text: str, api_key: str) -> list[float]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"input": text, "model": EMBEDDING_MODEL}
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers=headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def chat_completion(messages: list[dict], api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": CHAT_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 400
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

BASE_SYSTEM_PROMPT = """You are the personal AI assistant for Sanjeev Kumar, a Data Scientist and ML Engineer.
Your sole purpose is to answer questions about Sanjeev's professional background, skills, experience, and projects.
Answer ONLY based on the context provided below. If the answer is not in the context, say you don't have that information.
Do NOT answer unrelated questions, coding homework, or general trivia — politely decline and redirect back to Sanjeev's profile.

Relevant context retrieved from Sanjeev's resume:
---
{context}
---"""

@app.get("/")
def read_root():
    """Root endpoint to handle Render health checks."""
    return {"status": "ok", "message": "Sanjeev's Portfolio API is running"}

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    api_key = get_openai_api_key()
    collection = get_collection()

    try:
        query_embedding = get_embedding(req.message, api_key)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=["documents"]
        )

        retrieved_chunks = results["documents"][0] if results["documents"] else []
        if not retrieved_chunks:
            return {
                "response": "I can only answer questions about Sanjeev Kumar's portfolio, experience, skills, projects, education, and contact details."
            }
        context = "\n\n".join(retrieved_chunks)

        system_prompt = BASE_SYSTEM_PROMPT.format(context=context)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message}
        ]
        answer = chat_completion(messages, api_key)

        return {"response": answer}

    except requests.exceptions.HTTPError as e:
        detail = f"OpenAI API error: {e.response.status_code} - {e.response.text}"
        raise HTTPException(status_code=502, detail=detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
