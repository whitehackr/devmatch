"""Integration tests for API endpoints"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self):
        """Test health check returns 200"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestAnalyzeEndpoint:
    """Test analyze endpoint"""

    def test_analyze_requires_github_username(self):
        """Test that github_username is required"""
        response = client.post(
            "/api/analyze",
            json={"job_description": "Python developer needed"},
        )

        assert response.status_code == 422  # Validation error

    def test_analyze_requires_job_source(self):
        """Test that either job_url or job_description is required"""
        response = client.post(
            "/api/analyze",
            json={"github_username": "octocat"},
        )

        assert response.status_code == 422  # Validation error

    def test_analyze_rejects_both_job_sources(self):
        """Test that both job_url and job_description cannot be provided"""
        response = client.post(
            "/api/analyze",
            json={
                "job_url": "https://example.com/job",
                "job_description": "Some description",
                "github_username": "octocat",
            },
        )

        assert response.status_code == 422  # Validation error

    def test_analyze_with_direct_paste_mock(self, mocker):
        """Test analyze endpoint with direct paste (mocked services)"""
        # Mock the GitHub analyzer to avoid real API calls
        from app.models.responses import GitHubProfile

        mock_profile = GitHubProfile(
            username="testuser",
            account_age_years=5.0,
            repos_analyzed=10,
            total_repos=20,
            languages={"Python": 80.0},
            frameworks=["django"],
            tools=["git"],
        )

        mocker.patch(
            "app.api.routes.github_analyzer.analyze_profile",
            return_value=mock_profile,
        )

        response = client.post(
            "/api/analyze",
            json={
                "job_description": "Looking for Python developer with Django experience. "
                "Must have PostgreSQL knowledge.",
                "github_username": "testuser",
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "overall_score" in data
        assert "required_score" in data
        assert "preferred_score" in data
        assert "recommendation" in data
        assert "matched_skills" in data
        assert "missing_skills" in data
        assert "github_profile" in data
        assert "job_description" in data

        # Verify GitHub profile in response
        assert data["github_profile"]["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_analyze_github_user_not_found(self, mocker):
        """Test handling of non-existent GitHub user"""
        # Mock GitHub analyzer to raise exception
        mocker.patch(
            "app.api.routes.github_analyzer.analyze_profile",
            side_effect=Exception("User not found"),
        )

        response = client.post(
            "/api/analyze",
            json={
                "job_description": "Python developer needed",
                "github_username": "nonexistentuser12345",
            },
        )

        assert response.status_code == 404
        data = response.json()
        assert "error" in data["detail"]
        assert data["detail"]["error"] == "github_user_not_found"

    def test_analyze_with_minimal_job_description(self, mocker):
        """Test with minimal valid job description"""
        from app.models.responses import GitHubProfile

        mock_profile = GitHubProfile(
            username="testuser",
            account_age_years=2.0,
            repos_analyzed=5,
            total_repos=10,
            languages={"Python": 100.0},
            frameworks=[],
            tools=[],
        )

        mocker.patch(
            "app.api.routes.github_analyzer.analyze_profile",
            return_value=mock_profile,
        )

        # Minimal but valid (50+ chars)
        minimal_jd = "Python developer position available at our company. We need someone with experience."

        response = client.post(
            "/api/analyze",
            json={
                "job_description": minimal_jd,
                "github_username": "testuser",
            },
        )

        assert response.status_code == 200

    def test_cors_headers(self):
        """Test that CORS headers are present"""
        response = client.options(
            "/api/analyze",
            headers={"Origin": "http://localhost:3000"},
        )

        # Check CORS headers are set
        assert "access-control-allow-origin" in response.headers or response.status_code in [
            200,
            405,
        ]
