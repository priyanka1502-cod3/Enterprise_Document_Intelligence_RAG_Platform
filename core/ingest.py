from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def load_documents(file_path: str) -> List[Document]:
    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        loader = PyPDFLoader(str(path))
        docs = loader.load()

    elif path.suffix.lower() == ".txt":
        loader = TextLoader(str(path), encoding="utf-8")
        docs = loader.load()

    else:
        raise ValueError("Unsupported file type")

    return docs


def split_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)
    return chunks