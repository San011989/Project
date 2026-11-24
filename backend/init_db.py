
"""
init_db.py
Populate ChromaDB with Sanjeev Kumar's resume chunks.

Uses:
- OpenAI text-embedding-3-small
- requests for embedding generation
- ChromaDB persistent storage
"""

import os
import requests
import chromadb

from pathlib import Path
from dotenv import load_dotenv

# ==========================================
# 1. PATH CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

# Use exactly the same path as backend/main.py
DB_DIR = BASE_DIR / "chroma_db"

DB_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables from backend/.env locally.
# On Render, environment variables are supplied through the dashboard.
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Configure it in your .env file or Render environment variables."
    )

EMBEDDING_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "resume_data"

# ==========================================
# 2. RESUME CHUNKS
# ==========================================

chunks = [
    {
        "id": "summary",
        "text": """NAME: Sanjeev Kumar
ROLE: Data Scientist and ML Engineer
SUMMARY: Results-driven Data Scientist and ML Engineer with a strong foundation in artificial intelligence, machine learning, and data analysis. Proven ability to develop and deploy predictive models, extract actionable insights from complex datasets, and enhance operational efficiency through innovative solutions. Passionate about leveraging cutting-edge AI/ML techniques to solve real-world problems, with a particular interest in robotics and educational technology."""
    },
    {
        "id": "experience_1",
        "text": """EXPERIENCE: Learning Links Foundation (Dell Technologies) - Assistant Manager (Feb 2023 - Present)
- Spearheaded implementation of a new project management system, increasing team productivity by 20% and reducing project delivery time by 15% through data-driven process optimization.
- Developed and executed a comprehensive training program for new employees, reducing onboarding time by 30% and enhancing team efficiency through structured learning modules.
- Streamlined the budget allocation process, optimizing resource utilization and achieving annual cost savings of 10% by analyzing expenditure patterns."""
    },
    {
        "id": "experience_2",
        "text": """EXPERIENCE: Wunderkastan Robotian Education Pvt Ltd - Robotic Trainer (Feb 2022 - Feb 2023)
- Delivered hands-on robotics and coding training to students using components like 555 timer IC, Arduino, CD 4017 shift register, L298N motor shield, and LEDs.
- Designed and developed engaging robotics training programs for diverse student demographics.
- Facilitated interactive workshops to enhance students' practical robotics and problem-solving skills."""
    },
    {
        "id": "experience_3",
        "text": """EXPERIENCE: White Vectors - MI Engineer (Oct 2020 - Dec 2021)
- Executed predictive modeling using machine learning and deep learning techniques to forecast outcomes.
- Performed rigorous data cleaning and preprocessing.
- Analyzed complex datasets to extract actionable insights.
- Visualized data and model results using Matplotlib and Seaborn."""
    },
    {
        "id": "experience_4",
        "text": """EXPERIENCE: Transsion Holding Pvt Ltd - Hardware Testing Engineer (Aug 2018 - Mar 2020)
- Executed comprehensive testing in the SMT department.
- Conducted rigorous hardware tests for mobile devices.
- Developed detailed test plans and procedures."""
    },
    {
        "id": "projects",
        "text": """PROJECTS built by Sanjeev Kumar:
- Second Hand Car Price Prediction
- Alzheimer's Disease Prediction using AI
- Attendance Tracker System using AI
- Corn Disease Prediction using AI
- 70 types of Dog Breed Prediction and Classification using AI
- Vehicle Tracking System (YOLO)
- Image to Text Converter using AI
- Plant Disease Prediction using AI
- Brain Tumour Detection using AI
- Monkey Pox Detection
- Company Tracker System"""
    },
    {
        "id": "skills",
        "text": """SKILLS of Sanjeev Kumar:
Machine Learning, Deep Learning, NLP, Generative AI & LLMs, Python (Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch), Data Visualization, SQL, Statistical analysis, Predictive Modeling, Data Cleaning, Feature Engineering, Git, Robotics & Embedded Systems, Circuit Testing, YOLO, ChromaDB."""
    },
    {
        "id": "education",
        "text": """EDUCATION:
- Anna University Chennai: B.E./B.Tech - Electronics and Communications Engineering (CGPA: 65-70)
- Patna Science College: Intermediate - PCM
- D.A.V Public School, Rajrappa: 10th"""
    },
    {
        "id": "certifications",
        "text": """CERTIFICATIONS:
- Data Science Certification Course from SOCIAL PRACHAR Hyderabad
- Online Certificate Program in Artificial Intelligence and Machine Learning from EXCELR"""
    },
    {
        "id": "contact",
        "text": """CONTACT INFORMATION for Sanjeev Kumar:
- Phone: +91-8860223417
- Email: sanjeevr26@gmail.com
- LinkedIn: linkedin.com/in/sanjeev-kumar-0398bb35
- Location: Hyderabad"""
    }
]

# ==========================================
# 3. GENERATE OPENAI EMBEDDINGS
# ==========================================

def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings using the OpenAI API."""

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": texts,
        "model": EMBEDDING_MODEL
    }

    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers=headers,
        json=payload,
        timeout=60
    )

    if not response.ok:
        raise RuntimeError(
            f"OpenAI embedding error: "
            f"{response.status_code} - {response.text}"
        )

    data = response.json()["data"]

    # Preserve the original input order
    embeddings = [
        item["embedding"]
        for item in sorted(data, key=lambda x: x["index"])
    ]

    if len(embeddings) != len(texts):
        raise RuntimeError(
            f"Expected {len(texts)} embeddings, "
            f"but received {len(embeddings)}."
        )

    return embeddings


# ==========================================
# 4. INITIALIZE CHROMADB
# ==========================================

def main():

    print("\n====================================")
    print("SANJEEV RESUME RAG DATABASE SETUP")
    print("====================================")

    print("\nDatabase directory:", DB_DIR)

    # Step 1: Generate embeddings
    print("\nStep 1: Generating OpenAI embeddings...")

    texts = [chunk["text"] for chunk in chunks]

    embeddings = get_embeddings(texts)

    print("Embeddings generated:", len(embeddings))
    print("Embedding dimension:", len(embeddings[0]))

    # Step 2: Connect to ChromaDB
    print("\nStep 2: Initializing ChromaDB...")

    chroma_client = chromadb.PersistentClient(
        path=str(DB_DIR)
    )

    # Step 3: Remove existing collection if present
    existing = [
        collection.name
        for collection in chroma_client.list_collections()
    ]

    if COLLECTION_NAME in existing:

        print("\nExisting collection found.")
        print("Deleting old collection...")

        chroma_client.delete_collection(
            name=COLLECTION_NAME
        )

    # Step 4: Create collection
    print("\nStep 3: Creating collection...")

    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    # Step 5: Insert documents and embeddings
    print("\nStep 4: Inserting resume chunks...")

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=[chunk["id"] for chunk in chunks],
        metadatas=[
            {"section": chunk["id"]}
            for chunk in chunks
        ]
    )

    # Step 6: Verify collection
    print("\nStep 5: Verifying database...")

    total_chunks = collection.count()

    print("Collection name:", collection.name)
    print("Total chunks stored:", total_chunks)

    if total_chunks != len(chunks):
        raise RuntimeError(
            f"Database verification failed. "
            f"Expected {len(chunks)}, got {total_chunks}."
        )

    # Step 7: Display stored chunks
    stored = collection.get(
        include=["documents", "metadatas"]
    )

    for index, chunk_id in enumerate(stored["ids"]):

        print(f"\nChunk {index + 1}: {chunk_id}")
        print("Section:", stored["metadatas"][index]["section"])
        print("Content:", stored["documents"][index][:200])

    print("\n====================================")
    print("DATABASE INITIALIZATION SUCCESSFUL")
    print(f"Total chunks: {total_chunks}")
    print("Database path:", DB_DIR)
    print("====================================")


# ==========================================
# 5. RUN SCRIPT
# ==========================================

if __name__ == "__main__":
    main()
