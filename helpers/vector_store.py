from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from typing import List, Dict, get_args, Optional, Any
from langchain_core.vectorstores.base import VectorStore
from .custom_types import _EMBEDDING_TYPES, _VECTOR_DB, _IngestDataResult
from .embedding_models import get_embedding_model
import chromadb
from .config import Config

def get_vector_store_instance(
        embedding_model : _EMBEDDING_TYPES,
        index_name: str,
        dimension: Optional[int] = None,
) -> VectorStore:
    embedding = get_embedding_model(embedding_model, dimension)

    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    vector_store = Chroma(
        collection_name=index_name,
        client=chroma_client,
        embedding_function=embedding,
    )

    return vector_store

def ingest_data(
        urls: List[str],
        embedding_model: _EMBEDDING_TYPES,
        index_name: str,
        dimension: Optional[int] = None,
        chunk_size: int = 2000,
        chunk_overlap: int = 20,
) -> _IngestDataResult:
    try:
        loader = WebBaseLoader(urls)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        docs = text_splitter.split_documents(data)
        vector_store = get_vector_store_instance(
            embedding_model=embedding_model,
            index_name=index_name,
            dimension=dimension,
        )
        vector_store.add_documents(docs)

    except:
        pass
    
    return {
        "index_name": index_name,
        "embedding_model": embedding_model,
        "dimension": dimension,
    }