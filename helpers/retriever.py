from .custom_types import _VECTOR_DB, _EMBEDDING_TYPES
from typing import Optional
from langchain_core.retrievers import RetrieverLike
from .vector_store import get_vector_store_instance

def get_retriever(
    index_name: str,
    embedding_model: _EMBEDDING_TYPES,
    dimension: Optional[int] = None,
    top_k: int = 4,
    score_threshold: float = 0.01,
) -> RetrieverLike:
    vector_store = get_vector_store_instance(
        embedding_model=embedding_model,
        index_name=index_name,
        dimension=dimension,
    )

    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": top_k, "score_threshold": score_threshold},
    )

    return retriever
