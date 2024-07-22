import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")
    LANGFUSE_SECRET_KEY: str | None = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_PUBLIC_KEY: str | None = os.getenv("LANGFUSE_PUBLIC_KEY")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    HUGGINGFACEHUB_API_TOKEN: str | None = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    LANGFUSE_BASEURL: str | None = os.getenv("LANGFUSE_BASEURL")
