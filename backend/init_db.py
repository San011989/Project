"""
init_db.py - Populate ChromaDB with resume chunks using raw requests for embeddings.
This avoids any httpx/httpx2 dependency issues by using the requests library directly.
"""
import os
import requests
import chromadb
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing from .env file.")

EMBEDDING_MODEL = "text-embedding-3-small"

def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Call OpenAI embeddings API directly via requests."""
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
    response.raise_for_status()
    data = response.json()
    embeddings = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
    return embeddings

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

def main():
    print("Generating embeddings via OpenAI API (using requests)...")
    texts = [c["text"] for c in chunks]
    embeddings = get_embeddings(texts)
    print(f"Got {len(embeddings)} embeddings. Dimension: {len(embeddings[0])}")

    print("Initializing ChromaDB (persistent)...")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    existing = [c.name for c in chroma_client.list_collections()]
    if "resume_data" in existing:
        print("Deleting existing 'resume_data' collection...")
        chroma_client.delete_collection("resume_data")

    collection = chroma_client.create_collection(
        name="resume_data",
        metadata={"hnsw:space": "cosine"}
    )

    print(f"Adding {len(chunks)} chunks to ChromaDB...")
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=[c["id"] for c in chunks]
    )

    print(f"\nDone! {len(chunks)} resume chunks stored in ChromaDB.")
    print("ChromaDB is ready at ./chroma_db")

if __name__ == "__main__":
    main()