"""Tests for Job Scraper Service"""

import pytest
from app.services.job_scraper import JobScraperService
from app.models.responses import JobDescription


class TestJobScraperService:
    """Test job scraper service"""

    def test_scrape_direct_paste(self, sample_job_description):
        """Test direct paste of job description text"""
        scraper = JobScraperService()
        result = scraper.scrape_job(job_description_text=sample_job_description)

        assert isinstance(result, JobDescription)
        assert result.source == "direct_paste"
        assert result.raw_text == sample_job_description
        assert result.title is None  # Direct paste doesn't extract metadata
        assert result.company is None

    def test_scrape_direct_paste_with_minimal_text(self):
        """Test direct paste with minimal valid text"""
        scraper = JobScraperService()
        minimal_text = "Looking for Python developer with Django experience. " * 3

        result = scraper.scrape_job(job_description_text=minimal_text)

        assert isinstance(result, JobDescription)
        assert result.source == "direct_paste"
        assert len(result.raw_text) >= 50

    def test_scrape_requires_either_url_or_text(self):
        """Test that either URL or text must be provided"""
        scraper = JobScraperService()

        with pytest.raises(ValueError, match="Either job_url or job_description_text must be provided"):
            scraper.scrape_job()

    def test_scrape_rejects_both_url_and_text(self):
        """Test that both URL and text cannot be provided"""
        scraper = JobScraperService()

        with pytest.raises(ValueError, match="Provide either job_url OR job_description_text"):
            scraper.scrape_job(
                job_url="https://example.com/job",
                job_description_text="Some text"
            )

    def test_detect_platform_indeed(self):
        """Test platform detection for Indeed URLs"""
        scraper = JobScraperService()

        assert scraper._detect_platform("https://www.indeed.com/viewjob?jk=abc123") == "indeed"
        assert scraper._detect_platform("https://indeed.com/viewjob?jk=xyz") == "indeed"

    def test_detect_platform_google_jobs(self):
        """Test platform detection for Google Jobs URLs"""
        scraper = JobScraperService()

        assert scraper._detect_platform("https://www.google.com/search?q=software+engineer&ibp=htl;jobs") == "google_jobs"

    def test_detect_platform_linkedin(self):
        """Test platform detection for LinkedIn URLs"""
        scraper = JobScraperService()

        assert scraper._detect_platform("https://www.linkedin.com/jobs/view/123456") == "linkedin"

    def test_detect_platform_generic(self):
        """Test platform detection for generic URLs"""
        scraper = JobScraperService()

        assert scraper._detect_platform("https://somecompany.com/careers/job123") == "generic"

    @pytest.mark.asyncio
    async def test_scrape_indeed_mock(self, mocker):
        """Test Indeed scraping with mocked HTTP response"""
        scraper = JobScraperService()

        # Mock HTTP response
        mock_html = """
        <html>
            <h1 class="jobsearch-JobInfoHeader-title">Senior Python Engineer</h1>
            <div data-company-name="true">TechCorp</div>
            <div id="jobDescriptionText">
                We are seeking a Senior Python Engineer with Django experience.
                Required: Python, Django, PostgreSQL
            </div>
        </html>
        """

        mock_response = mocker.Mock()
        mock_response.text = mock_html
        mock_response.status_code = 200

        mocker.patch("httpx.get", return_value=mock_response)

        result = await scraper._scrape_indeed("https://www.indeed.com/viewjob?jk=abc123")

        assert result.title == "Senior Python Engineer"
        assert result.company == "TechCorp"
        assert "Python" in result.raw_text
        assert result.source == "indeed"

    def test_extract_text_from_html(self):
        """Test extracting clean text from HTML"""
        scraper = JobScraperService()

        html = "<div><h1>Title</h1><p>This is a paragraph.</p></div>"
        text = scraper._extract_text_from_html(html)

        assert "Title" in text
        assert "This is a paragraph" in text
        assert "<div>" not in text
        assert "<p>" not in text
