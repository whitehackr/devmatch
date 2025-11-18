"""Pytest configuration and fixtures"""

import pytest
from typing import Dict, Any


@pytest.fixture
def sample_job_description() -> str:
    """Sample job description for testing"""
    return """
    Senior Python Engineer

    TechCorp is seeking a Senior Python Engineer to join our backend team.

    Required Skills:
    - 5+ years of Python experience
    - Strong Django or Flask framework knowledge
    - PostgreSQL database expertise
    - RESTful API design
    - Git version control

    Preferred Skills:
    - AWS cloud experience
    - Docker and Kubernetes
    - Redis caching
    - GraphQL
    - CI/CD pipelines

    Responsibilities:
    - Design and implement scalable backend services
    - Collaborate with frontend team
    - Code review and mentoring
    """


@pytest.fixture
def sample_github_languages() -> Dict[str, int]:
    """Sample GitHub language statistics (bytes)"""
    return {
        "Python": 100000,
        "JavaScript": 50000,
        "Shell": 10000,
        "HTML": 5000,
    }


@pytest.fixture
def sample_github_profile() -> Dict[str, Any]:
    """Sample GitHub profile data"""
    return {
        "login": "testuser",
        "created_at": "2016-01-01T00:00:00Z",
        "public_repos": 50,
    }


@pytest.fixture
def sample_repos() -> list:
    """Sample GitHub repositories"""
    return [
        {
            "name": "django-project",
            "description": "E-commerce backend built with Django",
            "language": "Python",
            "fork": False,
            "pushed_at": "2024-01-01T00:00:00Z",
        },
        {
            "name": "react-app",
            "description": "Frontend built with React and TypeScript",
            "language": "JavaScript",
            "fork": False,
            "pushed_at": "2023-12-01T00:00:00Z",
        },
        {
            "name": "data-analysis",
            "description": "Data analysis scripts using pandas and numpy",
            "language": "Python",
            "fork": False,
            "pushed_at": "2023-11-01T00:00:00Z",
        },
    ]
