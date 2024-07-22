from uuid import UUID
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import LanguageModelLike
from langchain_core.retrievers import RetrieverLike
from langchain_core.runnables import Runnable
from typing import Any, Optional
from langfuse.callback import CallbackHandler
from .custom_types import _LangfuseArgs, _ChainResult
from .config import Config
from langchain_core.outputs import LLMResult
from langchain.callbacks.base import BaseCallbackHandler

class LLMResultHandler(BaseCallbackHandler):
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        if response.generations[0][0].message.usage_metadata:
            token_usage = response.generations[0][0].message.usage_metadata
        else:
            usage = response.generations[0][0].message.response_metadata["token_usage"]
            token_usage = {
                "input_tokens": usage.prompt_tokens,
                "output_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
            }

        self.response = token_usage


def create_conversational_retrieval_chain(
        llm: LanguageModelLike, retriever: RetrieverLike, instruction: Optional[str] = None
) -> Runnable:
    condense_question_system_template = """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."""

    condense_question_prompt = ChatPromptTemplate.from_messages(
        {
            ("system", condense_question_system_template),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        }
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, condense_question_prompt
    )

    system_prompt = (
        instruction + """\n\n{context}"""
        if instruction
        else """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, say that you don't know. Use three sentences maximum and keep the question concise
        \n\n
        {context}"""
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    qa_chain = create_stuff_documents_chain(llm, qa_prompt)

    convo_qa_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return convo_qa_chain


def invoke_conversational_retrieval_chain(
        chain: Runnable,
        input: str,
        trace: bool = True,
        langfuse_args: Optional[_LangfuseArgs] = None,
) -> _ChainResult:
    langfuse_handler = (
        CallbackHandler(
            public_key=Config.LANGFUSE_PUBLIC_KEY,
            secret_key=Config.LANGFUSE_SECRET_KEY,
            host=Config.LANGFUSE_BASEURL,
            **langfuse_args if langfuse_args else {},
        )
        if trace
        else None
    )

    llm_result_handler = LLMResultHandler()
    result = chain.invoke(
        {"input": input, "chat_history": []},
        config={
            "callbacks": (
                [llm_result_handler, langfuse_handler]
                if langfuse_handler
                else [llm_result_handler]
            )
        },
    )
    
    answer = result["answer"]
    source_documents = [
        {
            "page_content": doc.page_content, "source": doc.metadata["source"]
        }
        for doc in result["context"]
    ]

    token_usage = llm_result_handler.response

    output = {
        "answer": answer,
        "source_documents":source_documents,
        "token_usage":token_usage,
    }

    if langfuse_handler:
        langfuse_handler.flush()

    return output