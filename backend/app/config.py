"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # App
    app_name: str = "DevMatch API"
    version: str = "1.0.0"
    environment: str = "development"

    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]

    # GitHub API
    github_token: str = ""  # Optional: for higher rate limits
    github_api_base: str = "https://api.github.com"

    # Timeouts (seconds)
    scraping_timeout: int = 30
    github_timeout: int = 25
    total_request_timeout: int = 60

    # Analysis limits
    max_repos_to_analyze: int = 100
    max_readmes_to_fetch: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
