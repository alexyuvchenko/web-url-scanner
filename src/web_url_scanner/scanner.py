"""
URL Scanner - A script to scan websites and generate reports of all links and broken links.
"""

import asyncio
import sys

from .logger import setup_logger

# Set up logger
logger = setup_logger()


class WebUrlScanner:
    def __init__(self, base_url: str, max_depth: int = 3):
        self.base_url = base_url
        self.max_depth = max_depth
        logger.info(
            f"Initializing scanner with base URL: {base_url} and max depth: {max_depth}"
        )

    async def scan_url(self, url: str, depth: int) -> None:
        """
        Scan a single URL and extract all links from it.
        """
        logger.info(f"Scanning URL: {url} at depth {depth}")
        pass

    def generate_report(self) -> None:
        """
        Generate a CSV report with all found URLs and their depths.
        """
        logger.info("Generating report")
        pass

    async def run(self) -> None:
        """
        Main entry point to run the scanner.
        """
        logger.info("Starting URL scan")
        await self.scan_url(self.base_url, 0)
        self.generate_report()
        logger.info("URL scan completed")


async def main():
    logger.info("Web URL Scanner Started")

    try:
        base_url = "https://www.akamai.com/products/akamai-guardicore-segmentation"
        scanner = WebUrlScanner(base_url)
        await scanner.run()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("Web URL Scanner Finished")


if __name__ == "__main__":
    asyncio.run(main())
