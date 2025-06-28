
import os
import time
import psutil
from dotenv import load_dotenv
load_dotenv()
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document as DocxDocument

def extract_text_from_docx(path):
    """Extracts text from a .docx file using python-docx."""
    try:
        print(f"📂 Opening DOCX: {path}")
        doc = DocxDocument(path)
        print(f"📝 Paragraph count: {len(doc.paragraphs)}")
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        print(f"❌ Failed to extract text from {path}: {e}")
        return ""

def load_or_build_vectorstore(debug=False):
    """Loads FAISS index from disk if available, else builds it from .docx files."""
    faiss_index_path = "faiss_index"
    embeddings = OpenAIEmbeddings()

    # Load existing index
    if os.path.exists(faiss_index_path):
        if debug:
            print("📦 Loading existing FAISS index from disk...")
        return FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = []
    print("📄 Scanning source_content/ for DOCX files...")
    for file in os.listdir("source_content"):
        if file.endswith(".docx"):
            full_path = os.path.join("source_content", file)

            if os.path.getsize(full_path) > 2_000_000:  # 2 MB size guard
                print(f"⛔ Skipping {file} – exceeds 2MB limit for Render runtime.")
                continue

            text = extract_text_from_docx(full_path)
            print(f"📘 {file}: {len(text)} characters extracted")

            if text.strip():
                chunks = text_splitter.create_documents([text])
                print(f"🧩 Split into {len(chunks)} chunks.")
                for chunk in chunks:
                    docs.append(chunk)
                    time.sleep(0.2)  # Sleep to reduce memory pressure
    if not docs:
        print("⚠️ No documents were created. Your .docx may be empty or unsupported.")
        return None

    print("⚙️ Creating new FAISS index from parsed documents...")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(faiss_index_path)
    print("✅ FAISS index saved.")

    return vectorstore
