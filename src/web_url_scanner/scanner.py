"""
URL Scanner - A script to scan websites and generate reports of all links and broken links.
"""

import re
import os
import asyncio
import csv
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Set, Optional
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from src.web_url_scanner.logger import setup_logger
from src.web_url_scanner.config import REPORTS_DIR

# Set up logger
logger = setup_logger()


@dataclass
class ScannerConfig:
    """Configuration for the web scanner."""

    max_depth: int = 3
    max_concurrent: int = 10
    timeout: float = 5.0
    rate_limit: Optional[float] = None
    max_urls: int = 10000
    max_file_size_mb: int = 100
    headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.headers is None:
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0"
            }


class WebUrlScanner:
    def __init__(self, base_url: str, config: Optional[ScannerConfig] = None):
        """
        Initialize the web scanner.

        Args:
            base_url: The starting URL to scan
            config: Optional configuration object
        """
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.config = config or ScannerConfig()
        self.visited_urls: Set[str] = set()
        self.broken_urls: Set[str] = set()
        self.url_depths: Dict[str, int] = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Use the reports directory from config
        self.output_file = REPORTS_DIR / f"{self.base_domain}_{self.timestamp}.csv"
        self._semaphore = asyncio.Semaphore(self.config.max_concurrent)

    def is_valid_url(self, url: str) -> bool:
        """
        Validate if a URL is properly formatted and belongs to the same domain.

        Args:
            url: The URL to validate

        Returns:
            bool: True if URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.netloc == self.base_domain
        except Exception:
            return False

    async def fetch_url(self, client: httpx.AsyncClient, url: str) -> str:
        """
        Fetch a URL with rate limiting and error handling.

        Args:
            client: The httpx client to use
            url: The URL to fetch

        Returns:
            str: The response text if successful, empty string otherwise
        """
        if not self.is_valid_url(url):
            logger.warning(f"Invalid URL skipped: {url}")
            return ""

        if self.config.rate_limit:
            await asyncio.sleep(self.config.rate_limit)

        try:
            response = await client.get(
                url, timeout=self.config.timeout, headers=self.config.headers
            )
            if response.status_code == httpx.codes.OK:
                return response.text
            else:
                self.broken_urls.add(url)
                logger.error(f"Broken link found: {url} (Status: {response.status_code})")
                return ""
        except httpx.TimeoutException:
            self.broken_urls.add(url)
            logger.error(f"Timeout error fetching {url} (timeout: {self.config.timeout}s)")
            return ""
        except Exception as e:
            self.broken_urls.add(url)
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""

    def extract_links(self, html: str, current_url: str) -> Set[str]:
        """
        Extract and normalize links from HTML content.

        Args:
            html: The HTML content to parse
            current_url: The URL where the HTML was found

        Returns:
            Set[str]: Set of normalized URLs
        """
        if not html:
            return set()

        soup = BeautifulSoup(html, "html.parser")
        links = set()

        for a in soup.find_all("a", href=True):
            href = a["href"]
            absolute_url = urljoin(current_url, href)

            # Only include links from the same domain
            if self.is_valid_url(absolute_url):
                # Clean the URL
                absolute_url = re.sub(r"#.*$", "", absolute_url)
                absolute_url = re.sub(r"/$", "", absolute_url)
                links.add(absolute_url)

        return links

    async def process_url(self, client: httpx.AsyncClient, url: str, depth: int):
        """
        Process a single URL and its discovered links.

        Args:
            client: The httpx client to use
            url: The URL to process
            depth: Current depth in the crawl
        """
        if depth > self.config.max_depth or url in self.visited_urls:
            return

        if len(self.visited_urls) >= self.config.max_urls:
            logger.warning(f"Maximum URL limit ({self.config.max_urls}) reached")
            return

        async with self._semaphore:
            self.visited_urls.add(url)
            self.url_depths[url] = depth
            logger.info(f"Processing URL: {url} (Depth: {depth})")

            html = await self.fetch_url(client, url)
            if html:
                new_links = self.extract_links(html, url)
                tasks = []
                for link in new_links:
                    if link not in self.visited_urls:
                        tasks.append(self.process_url(client, link, depth + 1))
                if tasks:
                    await asyncio.gather(*tasks)

    async def scan(self):
        """Start the scanning process."""
        async with httpx.AsyncClient() as client:
            await self.process_url(client, self.base_url, 0)

    def save_results(self):
        """Save scanning results to a CSV file."""
        max_file_size = self.config.max_file_size_mb * 1024 * 1024  # Convert MB to bytes
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "URL", "Depth", "Status"])

            # Write all visited URLs
            for url in self.visited_urls:
                status = "Broken" if url in self.broken_urls else "Working"
                writer.writerow([timestamp, url, self.url_depths[url], status])

                # Check file size after each write
                if os.path.getsize(self.output_file) > max_file_size:
                    logger.warning(
                        f"Output file size limit ({self.config.max_file_size_mb}MB) reached"
                    )
                    break

        logger.info(f"Results saved to {self.output_file}")
        logger.info(f"Total URLs scanned: {len(self.visited_urls)}")
        logger.info(f"Broken URLs found: {len(self.broken_urls)}")


async def main():
    # Example usage with custom configuration
    config = ScannerConfig(
        max_depth=3,
        max_concurrent=10,
        timeout=5.0,
        rate_limit=0.5,  # 500ms delay between requests
        max_urls=10000,
        max_file_size_mb=100,
    )

    base_url = input("Enter the website URL to scan: ")
    scanner = WebUrlScanner(base_url, config)

    logger.info(f"Starting scan of {base_url}")
    await scanner.scan()
    scanner.save_results()


if __name__ == "__main__":
    asyncio.run(main())
