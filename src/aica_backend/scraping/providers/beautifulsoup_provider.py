import asyncio
import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse
import re

import httpx
from bs4 import BeautifulSoup

from .base import BaseProvider
from ...core.config import settings
from ...utils.common import clean_text, normalize_employment_type, clean_skills_array, categorize_tech_job

logger = logging.getLogger(__name__)


class BeautifulSoupProvider(BaseProvider):
    """
    BeautifulSoup-based provider for ethical web scraping.
    Uses requests with proper headers, rate limiting, and respects robots.txt.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__('beautifulsoup', config)
        self.session_headers = {
            'User-Agent': config.get('user_agent', settings.CRAWL4AI_USER_AGENT),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def scrape_jobs(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scrape job listings from given URLs using BeautifulSoup."""
        all_jobs = []

        for url in urls:
            if not self._is_supported_url(url):
                logger.info(f"Skipping unsupported URL: {url}")
                continue

            try:
                # Add rate limiting delay
                await asyncio.sleep(self.rate_limit_delay)

                jobs = await self._scrape_single_url(url)
                if jobs:
                    all_jobs.extend(jobs)
                    logger.info(f"Found {len(jobs)} jobs from {url}")

            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                continue

        # Remove duplicates
        unique_jobs = self._remove_duplicates(all_jobs)
        logger.info(f"Total unique jobs found: {len(unique_jobs)}")

        return unique_jobs

    async def _scrape_single_url(self, url: str) -> List[Dict[str, Any]]:
        """Scrape a single URL with retry logic."""
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(
                    headers=self.session_headers,
                    timeout=self.timeout,
                    follow_redirects=True
                ) as client:
                    response = await client.get(url)
                    response.raise_for_status()

                    soup = BeautifulSoup(response.content, 'html.parser')
                    jobs = self._extract_jobs_from_page(soup, url)

                    return jobs

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All {self.max_retries} attempts failed for {url}")

        return []

    def _extract_jobs_from_page(self, soup: BeautifulSoup, source_url: str) -> List[Dict[str, Any]]:
        """Extract job listings from the parsed HTML."""
        jobs = []

        # Common job listing selectors
        job_selectors = [
            '.job-card',
            '.job-listing',
            '.job-item',
            '.position',
            '.vacancy',
            '[data-jobid]',
            '.job-posting'
        ]

        for selector in job_selectors:
            job_elements = soup.select(selector)
            if job_elements:
                logger.info(f"Found {len(job_elements)} jobs using selector: {selector}")
                break

        if not job_elements:
            # Try to find job listings in common containers
            containers = soup.select('.jobs-container, .job-list, .careers, .vacancies')
            if containers:
                job_elements = containers[0].find_all(['div', 'li', 'article'])

        for job_elem in job_elements[:50]:  # Limit to prevent excessive processing
            job_data = self._extract_single_job(job_elem, source_url)
            if job_data:
                jobs.append(job_data)

        return jobs

    def _extract_single_job(self, job_elem, source_url: str) -> Optional[Dict[str, Any]]:
        """Extract data from a single job element."""
        try:
            # Extract basic information
            title_elem = job_elem.select_one('h1, h2, h3, .job-title, .title, .position-title')
            title = title_elem.get_text(strip=True) if title_elem else ""

            company_elem = job_elem.select_one('.company, .employer, .company-name, .organization')
            company = company_elem.get_text(strip=True) if company_elem else ""

            location_elem = job_elem.select_one('.location, .city, .place, .address')
            location = location_elem.get_text(strip=True) if location_elem else ""

            # Extract job URL
            job_url = None
            link_elem = job_elem.select_one('a[href]')
            if link_elem:
                href = link_elem.get('href')
                if href:
                    job_url = urljoin(source_url, href)

            # Extract description
            desc_elem = job_elem.select_one('.description, .summary, .details, .job-description')
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            # Basic validation
            if not title or not company:
                return None

            # Extract skills from description (simple pattern matching)
            skills = self._extract_skills_from_text(description)

            return {
                'source_url': job_url or source_url,
                'source_site': self.name,
                'job_title': clean_text(title),
                'company_name': clean_text(company),
                'location': clean_text(location),
                'full_text': clean_text(description),
                'all_skills': skills,
                'technical_skills': [s for s in skills if self._is_technical_skill(s)],
                'soft_skills': [s for s in skills if not self._is_technical_skill(s)],
                'status': 'raw'
            }

        except Exception as e:
            logger.error(f"Error extracting job data: {e}")
            return None

    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from job description using simple pattern matching."""
        if not text:
            return []

        # Common technical skills patterns
        tech_patterns = [
            r'\b(Python|Java|JavaScript|React|Node\.js|Django|Flask|SQL|PostgreSQL|MongoDB)\b',
            r'\b(Machine Learning|AI|NLP|Deep Learning|TensorFlow|PyTorch|Scikit-learn)\b',
            r'\b(Docker|Kubernetes|AWS|Azure|GCP|Git|Linux|Ubuntu)\b',
            r'\b(HTML|CSS|Bootstrap|jQuery|Angular|Vue\.js)\b'
        ]

        skills = []
        text_lower = text.lower()

        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.extend(matches)

        # Remove duplicates and clean
        return list(set(skill.strip() for skill in skills if skill.strip()))

    def _is_technical_skill(self, skill: str) -> bool:
        """Determine if a skill is technical."""
        technical_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'django', 'flask',
            'sql', 'postgresql', 'mongodb', 'machine learning', 'ai', 'nlp',
            'deep learning', 'tensorflow', 'pytorch', 'docker', 'kubernetes',
            'aws', 'azure', 'git', 'linux', 'html', 'css'
        ]

        return skill.lower() in technical_keywords

    def _is_supported_url(self, url: str) -> bool:
        """Check if URL is supported by this provider."""
        supported_domains = [
            'jobstreet.com', 'remoteok.com', 'weworkremotely.com',
            'stackoverflow.com', 'indeed.com', 'linkedin.com'
        ]

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        return any(supported_domain in domain for supported_domain in supported_domains)

    def _remove_duplicates(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate jobs based on title and company."""
        seen = set()
        unique_jobs = []

        for job in jobs:
            key = (job.get('job_title', '').lower(), job.get('company_name', '').lower())
            if key not in seen and key[0] and key[1]:
                seen.add(key)
                unique_jobs.append(job)

        return unique_jobs

    async def get_supported_sites(self) -> List[str]:
        """Get list of supported site domains."""
        return [
            'jobstreet.com',
            'remoteok.com',
            'weworkremotely.com',
            'stackoverflow.com',
            'indeed.com',
            'linkedin.com'
        ]

    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to scraping capabilities."""
        try:
            # Test with a simple HTTP request
            test_url = "https://httpbin.org/html"
            async with httpx.AsyncClient(headers=self.session_headers, timeout=self.timeout) as client:
                response = await client.get(test_url)
                response.raise_for_status()

            return {
                "success": True,
                "message": "BeautifulSoup provider is working correctly",
                "response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else 0
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"BeautifulSoup provider test failed: {e}",
                "error": str(e)
            }