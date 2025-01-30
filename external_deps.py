import os
from dataclasses import dataclass
from openai import AsyncOpenAI
from supabase import create_client, Client

class ExternalDeps:
    openai: AsyncOpenAI
    supabase: Client
    llm_model: str
    embed_model: str
    embed_dims: int

def create_external_deps() -> ExternalDeps:
    deps = ExternalDeps()
    deps.openai = openai_client()
    deps.supabase = supabase_client()
    #deps.llm_model = os.getenv("LLM_MODEL", "llama3.2")
    #deps.embed_model = os.getenv("EMBED_MODEL", "llama3.2")
    #deps.embed_dims = int(os.getenv("EMBED_SIZE", "3072"))
    deps.llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    deps.embed_model = os.getenv("EMBED_MODEL", "text-embedding-3-small")
    deps.embed_dims = int(os.getenv("EMBED_SIZE", "1536"))
    return deps

def openai_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        #base_url='http://localhost:11434/v1',

        # Required, but ignored by Ollama
        api_key = os.getenv("OPENAI_API_KEY", "zzzz"),
    )

def supabase_client() -> Client:
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_KEY")
    )


