
from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

# LangChain PDF
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load PDF (make sure to upload your textbook.pdf)
try:
    loader = PyPDFLoader("pdfs/textbook.pdf")
    pages = loader.load()
    db = FAISS.from_documents(pages, OpenAIEmbeddings())
except:
    db = None

class QuestionRequest(BaseModel):
    question: str

@app.post("/generate")
async def generate(req: QuestionRequest):
    prompt = f"""
    You are a nursing exam tutor.

    Question:
    {req.question}

    Generate:
    1. Similar question
    2. Harder question
    3. Explanation
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"result": response.choices[0].message.content}

@app.post("/evidence")
async def evidence(req: QuestionRequest):
    if db:
        docs = db.similarity_search(req.question)
        return {"evidence": docs[0].page_content}
    return {"evidence": "No PDF loaded yet."}
