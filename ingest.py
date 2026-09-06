import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DOCS_FOLDER = "documents"
DB_FOLDER = "chroma_db"

def load_pdfs():
    all_text_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    for filename in os.listdir(DOCS_FOLDER):
        if not filename.endswith(".pdf"):
            continue
        path = os.path.join(DOCS_FOLDER, filename)
        reader = PdfReader(path)
        full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

        chunks = splitter.split_text(full_text)
        for chunk in chunks:
            all_text_chunks.append({"text": chunk, "source": filename})

        print(f"Processed {filename}: {len(chunks)} chunks")

    return all_text_chunks

def build_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]

    db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=DB_FOLDER,
    )
    print(f"\nVector store built: {len(texts)} total chunks stored in '{DB_FOLDER}'")

if __name__ == "__main__":
    chunks = load_pdfs()
    build_vector_store(chunks)