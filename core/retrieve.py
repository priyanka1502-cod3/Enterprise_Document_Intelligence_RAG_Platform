from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from core.config import INDEX_PATH, EMBEDDING_MODEL

_embeddings = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def load_vectorstore():
    return FAISS.load_local(
        INDEX_PATH,
        get_embeddings(),
        allow_dangerous_deserialization=True
    )


def search_documents(query: str, k: int = 3):
    vectorstore = load_vectorstore()
    return vectorstore.similarity_search(query, k=k)