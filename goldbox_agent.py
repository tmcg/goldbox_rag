from __future__ import annotations as _annotations

import os, httpx, asyncio, logging
import system_prompts

from typing import List, Dict
from dotenv import load_dotenv

from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from openai import AsyncOpenAI
from external_deps import create_external_deps, ExternalDeps

load_dotenv()

pages_table = "site_pages"
deps = create_external_deps()
logger = logging.getLogger('gbox')

goldbox_expert = Agent(
    model = OpenAIModel(deps.llm_model, openai_client = deps.openai),
    system_prompt = system_prompts.goldbox_expert,
    deps_type = ExternalDeps,
    retries = 2,
)

async def get_embedding(text: str, client: AsyncOpenAI, embed_model: str, embed_dims: int) -> List[float]:
    try:
        response = await client.embeddings.create(
            model = embed_model,
            input = text
        )
        
        return response.data[0].embedding
    except Exception as e:
        # Return zero vector on error
        logger.error(f"Error getting embedding: {e}")
        return [0] * embed_dims


@goldbox_expert.tool
async def retrieve_walkthrough_documents(ctx: RunContext[ExternalDeps], user_query: str) -> str:
    """
    Retrieve relevant walkthrough documents based on the query with RAG.
    
    Args:
        ctx: The context including the Supabase client and OpenAI client
        user_query: The user's question or query
        
    Returns:
        A formatted string containing the top 5 most relevant walkthrough documents
    """
    try:
        query_embedding = await get_embedding(user_query, ctx.deps.openai, ctx.deps.embed_model, ctx.deps.embed_dims)

        print(f"calling retrieve_walkthrough_documents for: {user_query}")

        result = ctx.deps.supabase.rpc(
            'match_site_pages_3k',
            {
                'query_embedding': query_embedding,
                'match_count': 5,
                'filter': {'source': 'goldbox_walkthrough'}
            }
        ).execute()

        if not result.data:
            return "No relevant documentation found."

        def format_chunk(doc: Dict):
            return f"# {doc['title']}\n\n{doc['content']}"

        all_chunks = [format_chunk(doc) for doc in result.data]
        return "\n\n---\n\n".join(all_chunks)
    except Exception as e:
        logging.error(f"Error retrieving relevant documents: {e}")
        return f"Error retrieving relevant documents: {str(e)}"
    
#@goldbox_expert.tool
async def list_walkthrough_documents(ctx: RunContext[ExternalDeps]) -> List[str]:
    """
    Retrieve a list of all available walkthrough documents.
    
    Returns:
        List[str]: List of unique URLs for all walkthrough documents
    """    
    try:
        print(f"calling: list_walkthrough_documents")

        result = ctx.deps.supabase.from_(pages_table) \
            .select('url') \
            .eq('metadata->>source', 'goldbox_walkthrough') \
            .execute()
        
        if not result.data:
            return []
        
        urls_raw = [doc['url'] for doc in result.data]
        urls_set = sorted(set(urls_raw))

        logger.info(urls_set)

        return urls_set
    except Exception as e:
        logging.error(f"Error retrieving walkthrough documents: {e}")
        return []

#@goldbox_expert.tool
async def get_walkthrough_document(ctx: RunContext[ExternalDeps], url: str) -> str:
    """
    Retrieve the full content of a specific walkthrough document by combining all its chunks.
    The URL provided must be from the list of urls returned from the list_walkthrough_documents tool.
    Do not hallucinate any URLs.
    
    Args:
        ctx: The context including the Supabase client
        url: The URL of the page to retrieve
        
    Returns:
        str: The complete walkthrough document content with all chunks combined in order
    """
    try:
        print(f"calling: get_walkthrough_document: {url}")

        result = ctx.deps.supabase.from_(pages_table) \
            .select('title, content, chunk_number') \
            .eq('url', url) \
            .eq('metadata->>source', 'goldbox_walkthrough') \
            .order('chunk_number') \
            .execute()
        
        if not result.data:
            return f"No content found for URL: {url}"
        
        page_title = result.data[0]['title'].split(' - ')[0]
        page_content = [f"# {page_title}\n"]

        for chunk in result.data:
            page_content.append(chunk['content'])
        
        return "\n\n".join(page_content)
    except Exception as e:
        logger.error(f"Error retrieving walkthrough document: {e}")
        return f"Error retrieving walkthrough document: {str(e)}"
