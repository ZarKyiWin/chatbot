from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_core.retrievers import RetrieverLike
from langchain_cohere import CohereRerank
from .model_mapping import _RERANKERS, _VENDORS
from .config import Config
from .custom_types import _RERANKER_TYPES

def get_reranker(
    base_retriever: RetrieverLike,
    model_name: _RERANKER_TYPES,
    top_k: int = 3,
) -> ContextualCompressionRetriever:
    reranker_vendor = _RERANKERS[model_name]
    if reranker_vendor == _VENDORS["huggingface"]:
        model = HuggingFaceCrossEncoder(model_name=model_name)
        compressor = CrossEncoderReranker(model=model, top_n=top_k)
    elif reranker_vendor == _VENDORS["cohere"]:
        compressor = CohereRerank(
            model=model_name, cohere_api_key=Config.COHERE_API_KEY, top_n=top_k
        )
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=base_retriever
    )

    return compression_retriever