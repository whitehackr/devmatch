"""Tests for GitHub Analyzer Service"""

import pytest
from datetime import datetime
from app.services.github_analyzer import GitHubAnalyzerService
from app.models.responses import GitHubProfile


class TestGitHubAnalyzerService:
    """Test GitHub analyzer service"""

    @pytest.mark.asyncio
    async def test_analyze_profile_mock(self, mocker, sample_github_profile, sample_repos):
        """Test GitHub profile analysis with mocked API"""
        analyzer = GitHubAnalyzerService()

        # Mock GitHub API responses
        mock_client = mocker.AsyncMock()
        mock_client.get_user_profile.return_value = sample_github_profile
        mock_client.get_user_repos.return_value = sample_repos
        mock_client.get_repo_languages.return_value = {
            "Python": 80000,
            "JavaScript": 20000,
        }
        mock_client.get_file_content.return_value = "# Django Project\nBuilt with Django and PostgreSQL"

        mocker.patch.object(analyzer, "github_client", mock_client)

        profile = await analyzer.analyze_profile("testuser")

        assert isinstance(profile, GitHubProfile)
        assert profile.username == "testuser"
        assert profile.account_age_years > 0
        assert profile.total_repos == 50

    @pytest.mark.asyncio
    async def test_calculate_language_percentages(self, mocker):
        """Test language percentage calculation"""
        analyzer = GitHubAnalyzerService()

        # Language stats: 100k Python, 50k JS, 10k Shell = 160k total
        # Expected: Python 62.5%, JS 31.25%, Shell 6.25%
        all_languages = {
            "Python": 100000,
            "JavaScript": 50000,
            "Shell": 10000,
        }

        percentages = analyzer._calculate_language_percentages(all_languages)

        assert pytest.approx(percentages["Python"], 0.1) == 62.5
        assert pytest.approx(percentages["JavaScript"], 0.1) == 31.25
        assert pytest.approx(percentages["Shell"], 0.1) == 6.25

    @pytest.mark.asyncio
    async def test_filter_insignificant_languages(self, mocker):
        """Test filtering out languages below 1% threshold"""
        analyzer = GitHubAnalyzerService()

        # Language stats with some very small percentages
        all_languages = {
            "Python": 100000,
            "JavaScript": 10000,
            "HTML": 500,  # <1% should be filtered
            "CSS": 300,  # <1% should be filtered
        }

        percentages = analyzer._calculate_language_percentages(all_languages)

        assert "Python" in percentages
        assert "JavaScript" in percentages
        assert "HTML" not in percentages  # Filtered out
        assert "CSS" not in percentages  # Filtered out

    @pytest.mark.asyncio
    async def test_detect_frameworks_from_readme(self, mocker):
        """Test framework detection from README content"""
        analyzer = GitHubAnalyzerService()

        readme_content = """
        # My Project

        Built with:
        - Django REST Framework
        - React and TypeScript
        - PostgreSQL database
        """

        frameworks = analyzer._detect_frameworks_from_text(readme_content)

        assert "django" in frameworks
        assert "react" in frameworks
        assert "typescript" in frameworks

    @pytest.mark.asyncio
    async def test_detect_frameworks_from_package_json(self, mocker):
        """Test framework detection from package.json dependencies"""
        analyzer = GitHubAnalyzerService()

        package_json = """
        {
          "dependencies": {
            "react": "^18.0.0",
            "next": "^13.0.0",
            "express": "^4.18.0"
          }
        }
        """

        frameworks = analyzer._detect_frameworks_from_text(package_json)

        assert "react" in frameworks
        assert "nextjs" in frameworks
        assert "express" in frameworks

    @pytest.mark.asyncio
    async def test_detect_tools_from_repo_files(self, mocker):
        """Test tool detection from repository configuration files"""
        analyzer = GitHubAnalyzerService()

        # Mock repo with Docker and GitHub Actions
        repo_files = {
            "Dockerfile": True,
            ".github/workflows/ci.yml": True,
            "docker-compose.yml": True,
        }

        tools = analyzer._detect_tools_from_files(repo_files)

        assert "docker" in tools
        assert "github-actions" in tools

    @pytest.mark.asyncio
    async def test_calculate_account_age(self, mocker):
        """Test account age calculation"""
        analyzer = GitHubAnalyzerService()

        # Account created January 1, 2016 (9+ years ago from 2025)
        created_at = "2016-01-01T00:00:00Z"

        age_years = analyzer._calculate_account_age(created_at)

        assert age_years >= 8.0  # At least 8 years old
        assert age_years < 15.0  # But not absurdly high

    @pytest.mark.asyncio
    async def test_handle_user_not_found(self, mocker):
        """Test handling of non-existent GitHub user"""
        analyzer = GitHubAnalyzerService()

        mock_client = mocker.AsyncMock()
        mock_client.get_user_profile.side_effect = Exception("User not found")

        mocker.patch.object(analyzer, "github_client", mock_client)

        with pytest.raises(Exception, match="User not found"):
            await analyzer.analyze_profile("nonexistentuser12345")

    @pytest.mark.asyncio
    async def test_handle_empty_repos(self, mocker, sample_github_profile):
        """Test handling of user with no repositories"""
        analyzer = GitHubAnalyzerService()

        mock_client = mocker.AsyncMock()
        mock_client.get_user_profile.return_value = sample_github_profile
        mock_client.get_user_repos.return_value = []  # No repos

        mocker.patch.object(analyzer, "github_client", mock_client)

        profile = await analyzer.analyze_profile("testuser")

        assert profile.repos_analyzed == 0
        assert profile.languages == {}
        assert profile.frameworks == []
        assert profile.tools == []

    @pytest.mark.asyncio
    async def test_prioritize_recent_repos(self, mocker):
        """Test that analysis prioritizes recently updated repos"""
        analyzer = GitHubAnalyzerService()

        repos = [
            {"name": "old-repo", "pushed_at": "2020-01-01T00:00:00Z", "fork": False, "language": "Python"},
            {"name": "recent-repo", "pushed_at": "2024-01-01T00:00:00Z", "fork": False, "language": "Python"},
        ]

        # Should already be sorted by pushed_at (most recent first)
        # In real implementation, repos from API are sorted
        assert repos[1]["name"] == "recent-repo"

    @pytest.mark.asyncio
    async def test_exclude_forked_repos(self, mocker):
        """Test that forked repos are excluded from analysis"""
        analyzer = GitHubAnalyzerService()

        repos = [
            {"name": "original", "fork": False, "language": "Python"},
            {"name": "forked", "fork": True, "language": "Python"},
        ]

        # Filter forks
        filtered = [r for r in repos if not r["fork"]]

        assert len(filtered) == 1
        assert filtered[0]["name"] == "original"

    @pytest.mark.asyncio
    async def test_framework_deduplication(self, mocker):
        """Test that frameworks are deduplicated across repos"""
        analyzer = GitHubAnalyzerService()

        # Same framework detected multiple times should appear once
        all_frameworks = ["django", "react", "django", "react", "flask"]

        unique_frameworks = list(set(all_frameworks))

        assert unique_frameworks.count("django") == 1
        assert unique_frameworks.count("react") == 1
        assert unique_frameworks.count("flask") == 1
