"""
Job Scraper Service

Extracts job descriptions from URLs or accepts direct text paste.
Supports multiple platforms: Indeed, Google Jobs, LinkedIn, and generic sites.
"""

import httpx
from bs4 import BeautifulSoup
from typing import Optional
from urllib.parse import urlparse

from app.models.responses import JobDescription
from app.config import settings


class JobScraperService:
    """Service for scraping job descriptions from various sources"""

    def __init__(self):
        self.timeout = settings.scraping_timeout

    def scrape_job(
        self,
        job_url: Optional[str] = None,
        job_description_text: Optional[str] = None,
    ) -> JobDescription:
        """
        Scrape job description from URL or accept direct paste.

        Args:
            job_url: URL of job posting
            job_description_text: Direct paste of job description

        Returns:
            JobDescription object

        Raises:
            ValueError: If neither or both parameters provided
        """
        # Validate input
        if not job_url and not job_description_text:
            raise ValueError("Either job_url or job_description_text must be provided")

        if job_url and job_description_text:
            raise ValueError("Provide either job_url OR job_description_text, not both")

        # Direct paste (recommended path)
        if job_description_text:
            return JobDescription(
                title=None,
                company=None,
                source="direct_paste",
                raw_text=job_description_text,
                required_skills=[],
                preferred_skills=[],
            )

        # URL scraping (fallback)
        platform = self._detect_platform(job_url)

        if platform == "indeed":
            # Use async context for Indeed scraping
            import asyncio
            return asyncio.run(self._scrape_indeed(job_url))
        elif platform == "google_jobs":
            import asyncio
            return asyncio.run(self._scrape_google_jobs(job_url))
        elif platform == "linkedin":
            import asyncio
            return asyncio.run(self._scrape_linkedin(job_url))
        else:
            import asyncio
            return asyncio.run(self._scrape_generic(job_url))

    def _detect_platform(self, url: str) -> str:
        """
        Detect job platform from URL.

        Args:
            url: Job posting URL

        Returns:
            Platform identifier: "indeed", "google_jobs", "linkedin", or "generic"
        """
        url_lower = url.lower()
        parsed = urlparse(url_lower)
        domain = parsed.netloc

        if "indeed.com" in domain:
            return "indeed"
        elif "google.com" in domain and "jobs" in url_lower:
            return "google_jobs"
        elif "linkedin.com" in domain:
            return "linkedin"
        else:
            return "generic"

    async def _scrape_indeed(self, url: str) -> JobDescription:
        """
        Scrape job description from Indeed.

        Indeed is server-rendered, so we can use simple HTTP requests.

        Args:
            url: Indeed job URL

        Returns:
            JobDescription
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                follow_redirects=True,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract job title
            title_elem = soup.find("h1", class_="jobsearch-JobInfoHeader-title")
            title = title_elem.get_text(strip=True) if title_elem else None

            # Extract company name
            company_elem = soup.find("div", {"data-company-name": "true"})
            company = company_elem.get_text(strip=True) if company_elem else None

            # Extract job description
            desc_elem = soup.find("div", id="jobDescriptionText")
            if desc_elem:
                raw_text = desc_elem.get_text(separator="\n", strip=True)
            else:
                # Fallback: get all text
                raw_text = soup.get_text(separator="\n", strip=True)

            return JobDescription(
                title=title,
                company=company,
                source="indeed",
                raw_text=raw_text,
                required_skills=[],
                preferred_skills=[],
            )

    async def _scrape_google_jobs(self, url: str) -> JobDescription:
        """
        Scrape job description from Google Jobs.

        Google Jobs uses structured data (JSON-LD), making extraction easier.

        Args:
            url: Google Jobs URL

        Returns:
            JobDescription
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                follow_redirects=True,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Try to find JSON-LD structured data
            script_tags = soup.find_all("script", type="application/ld+json")

            title = None
            company = None
            raw_text = ""

            for script in script_tags:
                try:
                    import json
                    data = json.loads(script.string)

                    if isinstance(data, dict) and data.get("@type") == "JobPosting":
                        title = data.get("title")
                        company = data.get("hiringOrganization", {}).get("name")
                        raw_text = data.get("description", "")
                        break
                except (json.JSONDecodeError, AttributeError):
                    continue

            # Fallback: extract visible text
            if not raw_text:
                raw_text = soup.get_text(separator="\n", strip=True)

            return JobDescription(
                title=title,
                company=company,
                source="google_jobs",
                raw_text=raw_text,
                required_skills=[],
                preferred_skills=[],
            )

    async def _scrape_linkedin(self, url: str) -> JobDescription:
        """
        Scrape job description from LinkedIn.

        LinkedIn requires JavaScript rendering (uses Playwright).
        Note: LinkedIn has strong anti-bot measures, may fail.

        Args:
            url: LinkedIn job URL

        Returns:
            JobDescription
        """
        # LinkedIn scraping is complex and often blocked
        # For MVP, we'll attempt basic extraction but recommend direct paste

        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await page.goto(url, timeout=self.timeout * 1000)
                await page.wait_for_load_state("networkidle")

                # Extract title
                title_elem = await page.query_selector(".top-card-layout__title")
                title = await title_elem.text_content() if title_elem else None

                # Extract company
                company_elem = await page.query_selector(".topcard__org-name-link")
                company = await company_elem.text_content() if company_elem else None

                # Extract description
                desc_elem = await page.query_selector(".description__text")
                raw_text = await desc_elem.text_content() if desc_elem else ""

                await browser.close()

                return JobDescription(
                    title=title.strip() if title else None,
                    company=company.strip() if company else None,
                    source="linkedin",
                    raw_text=raw_text.strip(),
                    required_skills=[],
                    preferred_skills=[],
                )

        except Exception as e:
            # LinkedIn scraping often fails - return partial result
            return JobDescription(
                title=None,
                company=None,
                source="linkedin",
                raw_text=f"Failed to scrape LinkedIn. Error: {str(e)}. Please paste job description directly.",
                required_skills=[],
                preferred_skills=[],
            )

    async def _scrape_generic(self, url: str) -> JobDescription:
        """
        Generic scraper for unknown job sites.

        Uses Playwright for JavaScript rendering with heuristic content detection.

        Args:
            url: Generic job URL

        Returns:
            JobDescription
        """
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await page.goto(url, timeout=self.timeout * 1000)
                await page.wait_for_load_state("networkidle")

                # Try to find title (usually in <h1>)
                title_elem = await page.query_selector("h1")
                title = await title_elem.text_content() if title_elem else None

                # Extract all visible text
                raw_text = await page.evaluate("() => document.body.innerText")

                await browser.close()

                return JobDescription(
                    title=title.strip() if title else None,
                    company=None,
                    source="generic",
                    raw_text=raw_text.strip(),
                    required_skills=[],
                    preferred_skills=[],
                )

        except Exception as e:
            # Fallback to simple HTTP request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                title_elem = soup.find("h1")
                title = title_elem.get_text(strip=True) if title_elem else None

                raw_text = soup.get_text(separator="\n", strip=True)

                return JobDescription(
                    title=title,
                    company=None,
                    source="generic",
                    raw_text=raw_text,
                    required_skills=[],
                    preferred_skills=[],
                )

    def _extract_text_from_html(self, html: str) -> str:
        """
        Extract clean text from HTML.

        Args:
            html: HTML string

        Returns:
            Clean text without HTML tags
        """
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n", strip=True)
