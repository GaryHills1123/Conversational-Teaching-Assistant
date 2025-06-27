import os
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
        doc = DocxDocument(path)
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

    # Load and parse DOCX files
    docs = []
    print("📄 Scanning source_content/ for DOCX files...")
    for file in os.listdir("source_content"):
        if file.endswith(".docx"):
            full_path = os.path.join("source_content", file)
            text = extract_text_from_docx(full_path)
            print(f"📘 {file}: {len(text)} characters extracted")
            if text.strip():
                docs.append(Document(page_content=text, metadata={"source": file}))
    
    print(f"✅ Loaded {len(docs)} documents.")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"✂️ Split into {len(chunks)} chunks.")

    # 🚨 Fail fast if chunking failed
    if not chunks:
        raise ValueError("❌ No content chunks were generated. Check if DOCX files are formatted with readable text.")

    # Build and save FAISS index
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(faiss_index_path)

    if debug:
        print("✅ FAISS index built and saved.")
    return vectorstore
