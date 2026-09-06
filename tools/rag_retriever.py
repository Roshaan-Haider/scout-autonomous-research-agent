from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import tool

DB_FOLDER = "chroma_db"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Chroma(persist_directory=DB_FOLDER, embedding_function=embeddings)

@tool
def rag_retriever(query: str) -> str:
    """Search a local knowledge base of SEC filings (10-Ks, 10-Qs, 8-Ks, and proxy
    statements) from major public companies including Amazon, Apple, Microsoft,
    NVIDIA, Tesla, Meta, Netflix, Intel, AMD, JPMorgan, Goldman Sachs, Ford, GM,
    Pfizer, Johnson & Johnson, Walmart, Verizon, ExxonMobil, and Delta. Use this
    for financials, business strategy, risk factors, governance, or filing content.
    Note: filings rarely name competitors explicitly — they describe competitive
    dynamics narratively. If a query doesn't return clear results, don't retry
    the same query — try a different angle or conclude based on available context."""
    results = vector_store.similarity_search(query, k=4)
    formatted = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in results
    )
    return formatted