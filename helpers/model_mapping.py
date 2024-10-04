_VENDORS = {
    "googlegenai":"googlegenai",
    "huggingface":"huggingface",
    "openai":"openai",
    "cohere":"cohere",
    "anthropic":"anthropic",
}

_EMBEDDING_MODELS = {
    "text-embedding-004" : _VENDORS["googlegenai"],
    "BAAI/bge-m3": _VENDORS["huggingface"],
    "BAAI/bge-en-icl": _VENDORS["huggingface"],
}

_RERANKERS = {
    "BAAI/bge-reranker-base": _VENDORS["huggingface"],
    "rerank-multilingual-v3.0": _VENDORS["cohere"],
}

_LLMS = {
    "gpt-3.5-turbo": _VENDORS["openai"],
    "gpt-4o": _VENDORS["openai"],
    "gpt-4-turbo": _VENDORS["openai"],
    "mistralai/Mixtral-8x7B-Instruct-v0.1": _VENDORS["huggingface"],
    "claude-3-haiku-20240307": _VENDORS["anthropic"],
    "claude-3-5-sonnet-20240620": _VENDORS["anthropic"],
    "gemini-1.5-pro": _VENDORS["googlegenai"],
    "meta-llama/Llama-2-7b-chat-hf": _VENDORS["huggingface"],
    "meta-llama/Llama-2-13b-chat-hf": _VENDORS["huggingface"],
    "meta-llama/Llama-2-70b-chat-hf": _VENDORS["huggingface"],
    "meta-llama/Meta-Llama-3-8B-Instruct": _VENDORS["huggingface"],
    "meta-llama/Meta-Llama-3-70B-Instruct": _VENDORS["huggingface"],
    "meta-llama/Llama-3.2-3B-Instruct": _VENDORS["huggingface"],
    "meta-llama/Llama-3.1-70B-Instruct": _VENDORS["huggingface"],
}