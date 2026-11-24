
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv

import os
import requests
import chromadb

# ==========================================
# 1. PATH AND ENVIRONMENT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"

load_dotenv(BASE_DIR / ".env")

DB_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4.1-mini")

COLLECTION_NAME = "resume_data"

# ==========================================
# 2. FASTAPI INITIALIZATION
# ==========================================

app = FastAPI(
    title="Sanjeev Kumar Portfolio API",
    description="RAG-based Resume Chatbot API",
    version="1.0.0"
)

origins = [
    "https://project-2q48.onrender.com",
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 3. REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):
    message: str

# ==========================================
# 4. OPENAI API KEY
# ==========================================

def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY")

    if not key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured."
        )

    return key

# ==========================================
# 5. CHROMADB CONNECTION
# ==========================================

def get_collection():
    try:
        print("ChromaDB directory:", DB_DIR)

        chroma_client = chromadb.PersistentClient(
            path=str(DB_DIR)
        )

        collection = chroma_client.get_collection(
            name=COLLECTION_NAME
        )

        print("Collection:", collection.name)
        print("Total stored chunks:", collection.count())

        return collection

    except Exception as e:
        print("ChromaDB connection error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=(
                "ChromaDB collection not found or unavailable. "
                "Run init_db.py using the same database path."
            )
        )

# ==========================================
# 6. GENERATE EMBEDDINGS
# ==========================================

def get_embedding(text: str, api_key: str) -> list[float]:

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": text,
        "model": EMBEDDING_MODEL
    }

    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    return response.json()["data"][0]["embedding"]

# ==========================================
# 7. OPENAI CHAT COMPLETION
# ==========================================

def chat_completion(messages: list[dict], api_key: str) -> str:

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": CHAT_MODEL,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 500
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

# ==========================================
# 8. SYSTEM PROMPT
# ==========================================

BASE_SYSTEM_PROMPT = """
You are the personal AI assistant for Sanjeev Kumar.

Your purpose is to answer questions about:
- Professional background
- Technical skills
- Work experience
- Projects
- Education
- Certifications
- Professional achievements
- Contact details, if provided

STRICT RULES:

1. Answer only using the supplied resume context.
2. Never invent facts or qualifications.
3. If the answer is unavailable in the context, clearly say:
   "I could not find this information in Sanjeev Kumar's resume."
4. Do not answer unrelated questions or general trivia.
5. Be professional, clear and concise.

RESUME CONTEXT:

{context}
"""

# ==========================================
# 9. ROOT ENDPOINT
# ==========================================

@app.get("/")
def read_root():

    return {
        "status": "ok",
        "message": "Sanjeev's Portfolio API is running",
        "database_path": str(DB_DIR)
    }

# ==========================================
# 10. DATABASE HEALTH CHECK
# ==========================================

@app.get("/api/health")
def database_health():

    collection = get_collection()

    return {
        "status": "healthy",
        "database_path": str(DB_DIR),
        "collection": collection.name,
        "total_chunks": collection.count()
    }

# ==========================================
# 11. CHAT ENDPOINT WITH RAG
# ==========================================

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):

    try:

        # Step 1: Validate input
        message = req.message.strip()

        if not message:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        # Step 2: Get API key
        api_key = get_openai_api_key()

        # Step 3: Connect to ChromaDB
        collection = get_collection()

        total_chunks = collection.count()

        print("\n========== RAG DEBUG ==========")
        print("User question:", message)
        print("Total chunks:", total_chunks)

        # Step 4: Check database
        if total_chunks == 0:

            return {
                "response": "The resume database is empty. Please initialize the database.",
                "retrieved_chunks": []
            }

        # Step 5: Generate question embedding
        query_embedding = get_embedding(
            message,
            api_key
        )

        print("Query embedding generated successfully.")

        # Step 6: Retrieve relevant chunks
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(5, total_chunks),
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        # Step 7: Prepare retrieved chunks
        retrieved_chunks = []

        for chunk_id, document, distance, metadata in zip(
            ids,
            documents,
            distances,
            metadatas
        ):

            retrieved_chunks.append({
                "chunk_id": chunk_id,
                "content": document,
                "distance": float(distance),
                "metadata": metadata or {}
            })

            print("\nRetrieved Chunk:", chunk_id)
            print("Distance:", distance)
            print("Content:", document[:300])

        print("\nRetrieved chunk count:", len(retrieved_chunks))
        print("================================\n")

        # Step 8: Check retrieval
        if not retrieved_chunks:

            return {
                "response": "I could not retrieve relevant resume information.",
                "retrieved_chunks": []
            }

        # Step 9: Build context
        context = "\n\n".join(
            chunk["content"]
            for chunk in retrieved_chunks
        )

        # Step 10: Prepare system prompt
        system_prompt = BASE_SYSTEM_PROMPT.format(
            context=context
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ]

        # Step 11: Generate answer
        answer = chat_completion(
            messages,
            api_key
        )

        # Step 12: Return answer and chunks
        return {
            "response": answer,
            "retrieved_chunks": retrieved_chunks,
            "total_chunks_in_database": total_chunks
        }

    except HTTPException:
        raise

    except requests.exceptions.HTTPError as e:

        error_detail = (
            e.response.text
            if e.response is not None
            else str(e)
        )

        print("OpenAI HTTP error:", error_detail)

        raise HTTPException(
            status_code=502,
            detail=f"OpenAI API error: {error_detail}"
        )

    except requests.exceptions.RequestException as e:

        print("OpenAI connection error:", str(e))

        raise HTTPException(
            status_code=502,
            detail=f"Could not connect to OpenAI: {str(e)}"
        )

    except Exception as e:

        print("Unexpected error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
