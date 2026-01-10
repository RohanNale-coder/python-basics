
import uuid
import faiss
import pickle
from fastapi import FastAPI, UploadFile, File
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from openai import OpenAI
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# -------------------------
# CONFIG
# -------------------------
UPLOAD_DIR = "file_store"
VECTOR_DIR = "vector_store"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384

index_path = f"{VECTOR_DIR}/index.faiss"
meta_path = f"{VECTOR_DIR}/meta.pkl"

# -------------------------
# Load / Create DB
# -------------------------
if os.path.exists(index_path):
    index = faiss.read_index(index_path)
    metadata = pickle.load(open(meta_path, "rb"))
else:
    index = faiss.IndexFlatL2(dimension)
    metadata = []

# -------------------------
# APP
# -------------------------
app = FastAPI(title="AI Assistant with File Memory")

# -------------------------
# Helpers
# -------------------------
def extract_text(path):
    if path.endswith(".pdf"):
        reader = PdfReader(path)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
    else:
        with open(path, "r", errors="ignore") as f:
            return f.read()

def save_db():
    faiss.write_index(index, index_path)
    pickle.dump(metadata, open(meta_path, "wb"))

def chat_with_ai(context, question):
    prompt = f"""
You are an intelligent assistant.

Context from user's stored files:
{context}

User Question:
{question}

Answer the question clearly.
Also provide useful suggestions or next steps.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content

# -------------------------
# Upload File
# -------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text(path)
    embedding = model.encode([text])

    index.add(embedding)
    metadata.append({
        "filename": file.filename,
        "path": path,
        "content": text
    })

    save_db()

    return {"status": "File stored successfully", "file": file.filename}

# -------------------------
# Ask Question (INTERACTIVE)
# -------------------------
@app.get("/ask")
def ask_ai(question: str):
    query_embedding = model.encode([question])
    _, indices = index.search(query_embedding, k=1)

    if not indices.any():
        return {"answer": "No relevant file found."}

    file_data = metadata[indices[0][0]]
    context = file_data["content"][:3000]

    answer = chat_with_ai(context, question)

    return {
        "answer": answer,
        "source_file": file_data["filename"]
    }