"""
Simple robots.txt checker for ethical web scraping.
Follows KISS principle - keep it simple for thesis project.
"""

import logging
from typing import Optional
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

logger = logging.getLogger(__name__)


class SimpleRobotsChecker:
    """
    Simple robots.txt checker that respects website crawling policies.
    """

    def __init__(self, user_agent: str = "*"):
        """
        Initialize the robots checker.

        Args:
            user_agent: User agent string to check against robots.txt
        """
        self.user_agent = user_agent

    def _get_robots_url(self, base_url: str) -> str:
        """Generate the robots.txt URL for a given base URL."""
        parsed = urlparse(base_url)
        return f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    async def can_fetch(self, url: str, user_agent: Optional[str] = None) -> bool:
        """
        Check if a URL can be fetched according to robots.txt.

        Args:
            url: The URL to check
            user_agent: Optional user agent override

        Returns:
            True if the URL can be fetched, False otherwise
        """
        try:
            robots_url = self._get_robots_url(url)
            ua = user_agent or self.user_agent

            # Try to fetch and parse robots.txt
            parser = await self._fetch_and_parse_robots(robots_url)
            if parser:
                return parser.can_fetch(ua, url)
            else:
                # If robots.txt doesn't exist, assume allowed
                logger.debug(f"Could not fetch robots.txt for {robots_url}, assuming allowed")
                return True

        except Exception as e:
            logger.error(f"Error checking robots.txt for {url}: {e}")
            # Default to allowed if we can't check
            return True

    async def _fetch_and_parse_robots(self, robots_url: str) -> Optional[RobotFileParser]:
        """
        Fetch and parse robots.txt from a URL.

        Returns:
            RobotFileParser instance or None if failed
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(robots_url)
                response.raise_for_status()

                parser = RobotFileParser()
                parser.parse(response.text)
                return parser

        except Exception as e:
            logger.debug(f"Failed to fetch robots.txt from {robots_url}: {e}")
            return None

    async def get_crawl_delay(self, url: str, user_agent: Optional[str] = None) -> Optional[float]:
        """
        Get the crawl delay specified in robots.txt.

        Args:
            url: URL to check
            user_agent: Optional user agent override

        Returns:
            Crawl delay in seconds, or None if not specified
        """
        try:
            robots_url = self._get_robots_url(url)
            ua = user_agent or self.user_agent

            parser = await self._fetch_and_parse_robots(robots_url)
            if parser:
                return parser.crawl_delay(ua)

        except Exception as e:
            logger.error(f"Error getting crawl delay for {url}: {e}")

        return None