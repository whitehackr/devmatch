"""
GitHub Analyzer Service

Analyzes GitHub profiles to extract technical skills from actual code.
Uses GitHub REST API to fetch repositories, languages, and project details.
"""

import httpx
import re
import json
from datetime import datetime
from typing import Dict, List, Set, Optional
from collections import defaultdict

from app.models.responses import GitHubProfile
from app.config import settings
from app.utils.skill_taxonomy import normalize_skill_name


class GitHubClient:
    """GitHub API client"""

    def __init__(self):
        self.base_url = settings.github_api_base
        self.token = settings.github_token
        self.timeout = settings.github_timeout

        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "DevMatch-Analyzer/1.0",
        }

        # Only add Authorization header if token exists and is not empty
        if self.token and self.token.strip():
            self.headers["Authorization"] = f"token {self.token}"

    async def get_user_profile(self, username: str) -> Dict:
        """Fetch user profile from GitHub API"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/users/{username}",
                headers=self.headers,
            )

            if response.status_code == 404:
                raise Exception(f"GitHub user '{username}' not found")

            response.raise_for_status()
            return response.json()

    async def get_user_repos(self, username: str, max_repos: int = 100) -> List[Dict]:
        """Fetch user's public repositories"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/users/{username}/repos",
                params={
                    "sort": "pushed",  # Most recently pushed
                    "per_page": min(max_repos, 100),
                    "type": "owner",  # Exclude forks by default
                },
                headers=self.headers,
            )

            response.raise_for_status()
            return response.json()

    async def get_repo_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Fetch language statistics for a repository"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/languages",
                    headers=self.headers,
                )
                response.raise_for_status()
                return response.json()
            except Exception:
                return {}

    async def get_file_content(self, owner: str, repo: str, path: str) -> Optional[str]:
        """Fetch file content from repository"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/contents/{path}",
                    headers=self.headers,
                )

                if response.status_code == 404:
                    return None

                response.raise_for_status()
                data = response.json()

                # Decode content (base64 encoded)
                if "content" in data:
                    import base64
                    content = base64.b64decode(data["content"]).decode("utf-8")
                    return content

                return None
            except Exception:
                return None

    async def check_file_exists(self, owner: str, repo: str, path: str) -> bool:
        """Check if a file exists in repository"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/contents/{path}",
                    headers=self.headers,
                )
                return response.status_code == 200
            except Exception:
                return False


class GitHubAnalyzerService:
    """Service for analyzing GitHub profiles"""

    def __init__(self):
        self.github_client = GitHubClient()
        self.max_repos = settings.max_repos_to_analyze
        self.max_readmes = settings.max_readmes_to_fetch

    async def analyze_profile(self, username: str) -> GitHubProfile:
        """
        Analyze a GitHub profile to extract skills.

        Args:
            username: GitHub username

        Returns:
            GitHubProfile with extracted skills

        Raises:
            Exception: If user not found or API error
        """
        # Fetch user profile
        profile_data = await self.github_client.get_user_profile(username)

        # Calculate account age
        account_age = self._calculate_account_age(profile_data["created_at"])

        # Fetch repositories
        repos = await self.github_client.get_user_repos(username, self.max_repos)

        # Filter out forks (unless we want to include them)
        repos = [r for r in repos if not r.get("fork", False)]

        total_repos = profile_data["public_repos"]
        repos_analyzed = len(repos)

        # Aggregate language statistics
        all_languages = await self._aggregate_language_stats(username, repos)

        # Calculate language percentages
        language_percentages = self._calculate_language_percentages(all_languages)

        # Detect frameworks
        frameworks = await self._detect_frameworks(username, repos[: self.max_readmes])

        # Detect tools
        tools = await self._detect_tools(username, repos[: self.max_readmes])

        return GitHubProfile(
            username=username,
            account_age_years=account_age,
            repos_analyzed=repos_analyzed,
            total_repos=total_repos,
            languages=language_percentages,
            frameworks=list(frameworks),
            tools=list(tools),
        )

    async def _aggregate_language_stats(
        self, username: str, repos: List[Dict]
    ) -> Dict[str, int]:
        """
        Aggregate language statistics across all repositories.

        Args:
            username: GitHub username
            repos: List of repository data

        Returns:
            Dict mapping language -> total bytes
        """
        all_languages = defaultdict(int)

        for repo in repos:
            repo_name = repo["name"]
            languages = await self.github_client.get_repo_languages(username, repo_name)

            for lang, bytes_count in languages.items():
                all_languages[lang] += bytes_count

        return dict(all_languages)

    def _calculate_language_percentages(self, languages: Dict[str, int]) -> Dict[str, float]:
        """
        Calculate language percentages and filter insignificant ones.

        Args:
            languages: Dict mapping language -> bytes

        Returns:
            Dict mapping language -> percentage (filtered to >=1%)
        """
        if not languages:
            return {}

        total_bytes = sum(languages.values())

        percentages = {}
        for lang, bytes_count in languages.items():
            percentage = (bytes_count / total_bytes) * 100

            # Filter out languages below 1% threshold
            if percentage >= 1.0:
                percentages[lang] = round(percentage, 1)

        return percentages

    async def _detect_frameworks(self, username: str, repos: List[Dict]) -> Set[str]:
        """
        Detect frameworks from README files and dependency files.

        Args:
            username: GitHub username
            repos: List of repositories to analyze

        Returns:
            Set of canonical framework names
        """
        frameworks = set()

        for repo in repos:
            repo_name = repo["name"]

            # Check README
            readme = await self.github_client.get_file_content(username, repo_name, "README.md")
            if readme:
                frameworks.update(self._detect_frameworks_from_text(readme))

            # Check package.json (JavaScript/Node)
            package_json = await self.github_client.get_file_content(
                username, repo_name, "package.json"
            )
            if package_json:
                frameworks.update(self._detect_frameworks_from_text(package_json))

            # Check requirements.txt (Python)
            requirements = await self.github_client.get_file_content(
                username, repo_name, "requirements.txt"
            )
            if requirements:
                frameworks.update(self._detect_frameworks_from_text(requirements))

            # Check Gemfile (Ruby)
            gemfile = await self.github_client.get_file_content(username, repo_name, "Gemfile")
            if gemfile:
                frameworks.update(self._detect_frameworks_from_text(gemfile))

            # Check composer.json (PHP)
            composer = await self.github_client.get_file_content(
                username, repo_name, "composer.json"
            )
            if composer:
                frameworks.update(self._detect_frameworks_from_text(composer))

        return frameworks

    def _detect_frameworks_from_text(self, text: str) -> Set[str]:
        """
        Detect frameworks from text content (README, package files, etc.).

        Args:
            text: File content

        Returns:
            Set of canonical framework names
        """
        frameworks = set()
        text_lower = text.lower()

        # Framework patterns to search for
        framework_patterns = [
            "django",
            "flask",
            "fastapi",
            "react",
            "angular",
            "vue",
            "svelte",
            "next.js",
            "nuxt",
            "express",
            "nestjs",
            "spring",
            "rails",
            "laravel",
            "asp.net",
            "pytorch",
            "tensorflow",
            "scikit-learn",
            "pandas",
            "numpy",
            "keras",
            "spark",
            "airflow",
        ]

        for pattern in framework_patterns:
            # Use word boundaries for matching
            if re.search(rf"\b{re.escape(pattern)}\b", text_lower):
                canonical = normalize_skill_name(pattern)
                if canonical:
                    frameworks.add(canonical)

        return frameworks

    async def _detect_tools(self, username: str, repos: List[Dict]) -> Set[str]:
        """
        Detect tools from repository configuration files.

        Args:
            username: GitHub username
            repos: List of repositories

        Returns:
            Set of canonical tool names
        """
        tools = set()

        # Always present in GitHub repos
        tools.add("git")

        for repo in repos:
            repo_name = repo["name"]

            # Check for common tool indicators
            file_checks = {
                "Dockerfile": "docker",
                "docker-compose.yml": "docker",
                ".github/workflows": "github-actions",
                ".gitlab-ci.yml": "gitlab-ci",
                "Jenkinsfile": "jenkins",
                ".circleci/config.yml": "circleci",
                "pytest.ini": "pytest",
                "jest.config.js": "jest",
                "nginx.conf": "nginx",
            }

            for file_path, tool in file_checks.items():
                exists = await self.github_client.check_file_exists(username, repo_name, file_path)
                if exists:
                    canonical = normalize_skill_name(tool)
                    if canonical:
                        tools.add(canonical)

        return tools

    def _detect_tools_from_files(self, repo_files: Dict[str, bool]) -> Set[str]:
        """
        Detect tools from repository file checks.

        Args:
            repo_files: Dict mapping file path -> exists boolean

        Returns:
            Set of canonical tool names
        """
        tools = set()

        file_to_tool = {
            "Dockerfile": "docker",
            "docker-compose.yml": "docker",
            ".github/workflows": "github-actions",
            ".gitlab-ci.yml": "gitlab-ci",
            "Jenkinsfile": "jenkins",
        }

        for file_path, tool in file_to_tool.items():
            if repo_files.get(file_path):
                canonical = normalize_skill_name(tool)
                if canonical:
                    tools.add(canonical)

        return tools

    def _calculate_account_age(self, created_at: str) -> float:
        """
        Calculate account age in years.

        Args:
            created_at: ISO 8601 timestamp (e.g., "2016-01-01T00:00:00Z")

        Returns:
            Years since account creation
        """
        created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        now = datetime.now(created_date.tzinfo)
        age_seconds = (now - created_date).total_seconds()
        age_years = age_seconds / (365.25 * 24 * 60 * 60)  # Account for leap years
        return round(age_years, 1)
