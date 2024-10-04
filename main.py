import streamlit as st
import time
from helpers import (
    invoke_conversational_retrieval_chain,
    create_conversational_retrieval_chain,
    get_llm,
    get_retriever,
    get_reranker,
    ingest_data
)
from dotenv import load_dotenv
import re

load_dotenv()

index_name = "test14"
def initialize_chat():
    llm = get_llm(model_name="meta-llama/Llama-3.2-3B-Instruct")
    retriever = get_retriever(
        index_name=index_name,
        embedding_model="BAAI/bge-m3",
    )
    reranker = get_reranker(
        base_retriever=retriever, model_name="BAAI/bge-reranker-base"
    )
    return create_conversational_retrieval_chain(llm=llm, retriever=reranker)

def response_generator(prompt):
    if "context" in st.session_state:
        del st.session_state["context"]
    
    response = invoke_conversational_retrieval_chain(
        chain=st.session_state.chain,
        input=prompt,
        trace=False,
    )
    
    answer = response["answer"]
    source_documents = response["source_documents"]
    token_usage = response["token_usage"]
    st.session_state.token_usage = token_usage
    st.session_state.context = [
        [i["page_content"], i["source"]] for i in source_documents
    ]
    for word in answer.split():
        yield word + " "
        time.sleep(0.05)


st.title("Simple chat")

if "chain" not in st.session_state:
    st.session_state.chain = initialize_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.session_state["ingest"] = False
    st.text("Data Source: URLs")
    urls = st.text_area(label="Enter URLs separated by comma")
    if st.button(label="Ingest Data"):
        ingest = ingest_data(urls = urls.split(","), embedding_model="BAAI/bge-m3", index_name=index_name)
        st.session_state["ingest"] = True
    if st.session_state["ingest"]:
        st.text("Data Ingested")
    if "context" in st.session_state:
        st.text(f"Input tokens - {st.session_state.token_usage['input_tokens']}")
        st.text(f"Output tokens - {st.session_state.token_usage['output_tokens']}")
        st.text(f"Total tokens - {st.session_state.token_usage['total_tokens']}")
        for i in range(0, len(st.session_state.context)):
            text = st.session_state.context[i][0]

            sentences = re.split(r"(?<=[.!?]) +", text)

            cleaned_sentences = [" ".join(sentence.split()) for sentence in sentences]

            cleaned_text = "\n\n".join(cleaned_sentences)
            st.text(
                f"Document {i}\nSource: {st.session_state.context[i][1]}\n{cleaned_text}\n---------------------"
            )
