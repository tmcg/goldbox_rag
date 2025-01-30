import os, asyncio, logging, re

from typing import List
from dataclasses import dataclass
from urllib.parse import urlparse
from dotenv import load_dotenv
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

from system_utils import init_logging

init_logging("goldbox_rag_crawl2md.log")
load_dotenv()

# Make the httpx logger a little quieter
#httpx_logger = logging.getLogger('httpx')
#httpx_logger.setLevel(logging.WARN)

pages_table = "site_pages"
logger = logging.getLogger('gbox')

async def process_document(url: str, markdown: str):
    logger.info(f"Processing {url}")

    crawlpath = "./crawl"
    if not os.path.exists(crawlpath):
        os.makedirs(crawlpath)

    filename = re.sub("https?://", "", url)
    filename = re.sub("\\.php", ":md", filename)
    filename = re.sub("\\.html", ":md", filename)
    filename = re.sub("[./]", "_", filename)
    filename = re.sub(":md", ".md", filename)
    filename = re.sub(":", "_", filename)

    filepath = crawlpath + "/" + filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)


async def crawl_walkthrough_urls(urls: List[str], max_concurrent: int = 1):
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable_gpu", "--disable-dev-shm-usage", "--no-sandbox"]
    )

    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": True,
            "ignore_images": True,
            "escape_html": True,
            "body_width": 120
        }
    )

    # GameBanshee stores the main page content 
    # inside the tag <div class="curvebox"/>
    crawl_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        css_selector='.curvebox',
        markdown_generator=md_generator
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
                    logger.warning(f"Failed: {url} - Error: {result.error_message}")

                return url

        await asyncio.gather(*[process_url(url) for url in urls])
    finally:
        await crawler.close()

def get_walkthrough_urls() -> List[str]:
    from goldbox_urls import get_urls
    return get_urls()


async def main():
    urls = get_walkthrough_urls()
    if not urls:
        logger.warning("No URLs found to crawl")

    logger.info(f"Found {len(urls)} URLs to crawl")
    await crawl_walkthrough_urls(urls)

if __name__=="__main__":
    asyncio.run(main())