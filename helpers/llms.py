from .model_mapping import _LLMS, _VENDORS
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import LanguageModelLike
from .config import Config
from .custom_types import _LLM_TYPES

def get_llm(
    model_name: _LLM_TYPES, temperature: float = 0.7, top_p: float = 0.9
) -> LanguageModelLike:
    llm_vendor = _LLMS[model_name]

    if llm_vendor == _VENDORS["googlegenai"]:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=Config.GOOGLE_API_KEY,
            top_p=top_p,
            max_retries=0,
        )

    elif llm_vendor == _VENDORS["openai"]:
        llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=Config.OPENAI_API_KEY,
            model_kwargs={"top_p": top_p},
            max_retries=0,
        )
    
    elif llm_vendor == _VENDORS["anthropic"]:
        llm = ChatAnthropic(
            model_name=model_name,
            temperature=temperature,
            api_key=Config.ANTHROPIC_API_KEY,
            top_p=top_p,
            max_retries=0,
        )
    elif llm_vendor == _VENDORS["huggingface"]:
        base_model = HuggingFaceEndpoint(
            repo_id=model_name,
            temperature=temperature,
            huggingfacehub_api_token=Config.HUGGINGFACEHUB_API_TOKEN,
            top_p=top_p,
        )
        llm = ChatHuggingFace(llm=base_model)
    else:
        print("Invalid LLM.")
        pass

    return llm