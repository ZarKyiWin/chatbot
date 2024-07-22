from typing import Literal, TypedDict, Optional, Dict, List

_VECTOR_DB = Literal["chromadb", "elasticsearch"]

_EMBEDDING_TYPES = Literal[
    "text-embedding-3-large",
    "text-embedding-3-small",
    "text-embedding-ada-002",
    "text-embedding-004",
    "BAAI/bge-m3"
]

_RERANKER_TYPES = Literal[
    "BAAI/bge-reranker-base",
    "rerank-multilingual-v3.0"
]

_LLM_TYPES = Literal[
    "gpt-3.5-turbo",
    "gpt-4o",
    "gpt-4-turbo",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-20240620",
    "gemini-1.5-pro",
    "meta-llama/Llama-2-7b-chat-hf",
    "meta-llama/Llama-2-13b-chat-hf",
    "meta-llama/Llama-2-70b-chat-hf",
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "meta-llama/Meta-Llama-3-70B-Instruct",
]

class _IngestDataResult(TypedDict):
    index_name: str
    embedding_model: str
    dimension: Optional[int]

class _LangfuseArgs(TypedDict):
    session_id: Optional[str]
    user_id: Optional[str]
    trace_id: Optional[str]
    metadata: Optional[Dict]

class _SourceDocuments(TypedDict):
    page_content: str
    source: str


class _TokenUsage(TypedDict):
    input_tokens: int
    output_tokens: int
    total_tokens: int

class _ChainResult(TypedDict):
    answer: str
    source_documents: List[_SourceDocuments]
    token_usage: _TokenUsage


__all__ = [
    "_VECTOR_DB",
    "_LLM_TYPES",
    "_EMBEDDING_TYPES",
    "_RERANKER_TYPES",
    "_LangfuseArgs",
    "_ChainResult",
]
