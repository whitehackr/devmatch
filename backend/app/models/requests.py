"""Request models"""

from pydantic import BaseModel, Field, model_validator
from typing import Optional


class AnalyzeRequest(BaseModel):
    """Request model for job analysis"""

    job_url: Optional[str] = Field(
        None,
        description="URL of the job posting (Indeed, Google Jobs, LinkedIn, etc.)",
        examples=["https://www.indeed.com/viewjob?jk=abc123"],
    )

    job_description: Optional[str] = Field(
        None,
        description="Direct paste of job description text",
        examples=["We are seeking a Senior Python Engineer with 5+ years experience..."],
        min_length=50,
        max_length=50000,
    )

    github_username: str = Field(
        ...,
        description="GitHub username to analyze",
        examples=["octocat"],
        min_length=1,
        max_length=39,  # GitHub username max length
    )

    @model_validator(mode="after")
    def validate_job_source(self) -> "AnalyzeRequest":
        """Validate that either job_url or job_description is provided"""
        if not self.job_url and not self.job_description:
            raise ValueError("Either job_url or job_description must be provided")

        if self.job_url and self.job_description:
            raise ValueError("Provide either job_url OR job_description, not both")

        return self
