import os, json, asyncio, logging
import system_prompts

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlparse
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from openai import AsyncOpenAI

from external_deps import create_external_deps, ExternalDeps
from system_utils import init_logging

init_logging("goldbox_rag_crawl.log")
load_dotenv()

# Make the httpx logger a little quieter
#httpx_logger = logging.getLogger('httpx')
#httpx_logger.setLevel(logging.WARN)

pages_table = "site_pages"
deps = create_external_deps()
logger = logging.getLogger('gbox')
logger.info(f"Using LLM model: {deps.llm_model}")
logger.info(f"Using Embedding model: {deps.embed_model}")

@dataclass
class ProcessedChunk:
    url: str
    chunk_number: int
    title: str
    summary: str
    content: str
    metadata: Dict[str, Any]
    embedding: List[float]


def chunk_text(text: str, chunk_size: int = 5000) -> List[str]:
    """Split text into chunks, respecting code blocks and paragraphs."""
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        # Calculate end position
        end = start + chunk_size

        # If we're at the end of the text, just take what's left
        if end >= text_length:
            chunks.append(text[start:].strip())
            break

        # Try to find a code block boundary first (```)
        chunk = text[start:end]
        code_block = chunk.rfind('```')
        if code_block != -1 and code_block > chunk_size * 0.3:
            end = start + code_block

        # If no code block, try to break at a paragraph
        elif '\n\n' in chunk:
            # Find the last paragraph break
            last_break = chunk.rfind('\n\n')
            if last_break > chunk_size * 0.3:  # Only break if we're past 30% of chunk_size
                end = start + last_break

        # If no paragraph break, try to break at a sentence
        elif '. ' in chunk:
            # Find the last sentence break
            last_period = chunk.rfind('. ')
            if last_period > chunk_size * 0.3:  # Only break if we're past 30% of chunk_size
                end = start + last_period + 1

        # Extract chunk and clean it up
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start position for next chunk
        start = max(start + 1, end)

    return chunks


async def get_summary(chunk: str, url: str) -> Dict[str, str]:
    title = "Error"
    summary = "Error"

    try:
        system_content = system_prompts.extract_summary
        user_content = f"The URL is '{url}'. The document content is {chunk[:1000]}"

        response = await deps.openai.chat.completions.create(
            model = deps.llm_model,
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"}
        )

        response_content = response.choices[0].message.content 
        json_content = json.loads(response_content)
        title = json_content['title']
        summary = json_content['summary']
    except Exception as e:
        logger.error(f"Error getting title and summary: {e}")

    return {"title": title, "summary": summary}


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


async def insert_chunk(chunk: ProcessedChunk):
    try:
        data = {
            "url": chunk.url,
            "chunk_number": chunk.chunk_number,
            "title": chunk.title,
            "summary": chunk.summary,
            "content": chunk.content,
            "metadata": chunk.metadata,
            "embedding": chunk.embedding,
        }

        logger.info(f"Inserting chunk {chunk.chunk_number} for {chunk.url}")
        table = deps.supabase.table(pages_table)
        result = table.insert(data).execute()

        return result
    except Exception as e:
        logger.error(f"Error inserting chunk: {e}")
        return None


async def process_chunk(chunk: str, chunk_number: int, url: str) -> ProcessedChunk:
    extracted = await get_summary(chunk, url)
    embedding = await get_embedding(chunk, deps.openai, deps.embed_model, deps.embed_dims)
    metadata = {
        "source": "goldbox_walkthrough",
        "chunk_size": len(chunk),
        "crawled_at": datetime.now(timezone.utc).isoformat(),
        "url_path": urlparse(url).path
    }

    return ProcessedChunk(
        url = url,
        chunk_number = chunk_number,
        title = extracted['title'],
        summary = extracted['summary'],
        content = chunk,
        metadata = metadata,
        embedding = embedding
    )


async def process_document(url: str, markdown: str):
    chunks = chunk_text(markdown)
    logger.info(f"Processing {url}")

    process_tasks = [
        process_chunk(chunk, i, url)
        for i, chunk in enumerate(chunks)
    ]

    processed_chunks = await asyncio.gather(*process_tasks)

    insert_tasks = [
        insert_chunk(chunk)
        for chunk in processed_chunks
    ]
    await asyncio.gather(*insert_tasks)


async def crawl_walkthrough_urls(urls: List[str], max_concurrent: int = 5):
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable_gpu", "--disable-dev-shm-usage", "--no-sandbox"]
    )

    # GameBanshee stores the main page content 
    # inside the tag <div class="curvebox"/>
    crawl_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        css_selector='.curvebox'
    )

    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_url(url: str):
            async with semaphore:
                result = await crawler.arun(
                    url=url,
                    config=crawl_config,
                    session_id="session1"
                )

                if result.success:
                    logger.info(f"Successfully crawled: {url}")
                    await process_document(url, result.markdown_v2.raw_markdown)
                else:
                    logger.warning(f"Failed: {url} - Error: {result.error.message}")

                return url

        await asyncio.gather(*[process_url(url) for url in urls])
    finally:
        await crawler.close()


def reset_walkthrough_urls():
    try:
        logger.info(f"Resetting all URLs")
        table = deps.supabase.table(pages_table)
        table.delete().neq("id", -1).execute()
    except Exception as e:
        logger.error(f"Error resetting URLs: {e}")


def get_walkthrough_urls() -> List[str]:
    reset_walkthrough_urls()
    from goldbox_pool import get_urls as get_urls_pool
    return get_urls_pool()


async def main():
    urls = get_walkthrough_urls()
    if not urls:
        logger.warning("No URLs found to crawl")

    logger.info(f"Found {len(urls)} URLs to crawl")
    await crawl_walkthrough_urls(urls)

if __name__=="__main__":
    asyncio.run(main())