"""Response models"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = "healthy"
    version: str = "1.0.0"


class SkillCategory(str, Enum):
    """Skill categories"""

    LANGUAGE = "language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    CLOUD = "cloud"
    TOOL = "tool"
    CONCEPT = "concept"


class Skill(BaseModel):
    """Skill model"""

    name: str = Field(..., description="Canonical skill name")
    category: SkillCategory = Field(..., description="Skill category")
    importance: int = Field(
        ..., ge=1, le=5, description="Importance score (1=nice-to-have, 5=critical)"
    )


class MatchedSkill(Skill):
    """Matched skill with evidence"""

    evidence: str = Field(..., description="Proof of skill from GitHub")


class JobDescription(BaseModel):
    """Parsed job description"""

    title: Optional[str] = Field(None, description="Job title")
    company: Optional[str] = Field(None, description="Company name")
    source: str = Field(..., description="Source of job description (indeed, direct_paste, etc.)")
    raw_text: str = Field(..., description="Full job description text")
    required_skills: List[Skill] = Field(default_factory=list, description="Required skills")
    preferred_skills: List[Skill] = Field(default_factory=list, description="Preferred skills")


class GitHubProfile(BaseModel):
    """Analyzed GitHub profile"""

    username: str = Field(..., description="GitHub username")
    account_age_years: float = Field(..., description="Years since account creation")
    repos_analyzed: int = Field(..., description="Number of repos analyzed")
    total_repos: int = Field(..., description="Total public repos")
    languages: Dict[str, float] = Field(
        default_factory=dict, description="Language -> percentage mapping"
    )
    frameworks: List[str] = Field(default_factory=list, description="Detected frameworks")
    tools: List[str] = Field(default_factory=list, description="Detected tools")


class GapAnalysis(BaseModel):
    """Skill gap analysis"""

    critical_missing: int = Field(..., description="Number of critical (importance >=4) missing skills")
    total_missing: int = Field(..., description="Total missing skills")
    learning_estimate_weeks: int = Field(..., description="Estimated weeks to close gap")


class RecommendationType(str, Enum):
    """Recommendation types"""

    APPLY_NOW = "APPLY_NOW"
    COMPETITIVE = "COMPETITIVE"
    SKILL_GAP = "SKILL_GAP"


class MatchResult(BaseModel):
    """Complete match result"""

    overall_score: int = Field(..., ge=0, le=100, description="Overall match percentage")
    required_score: int = Field(..., ge=0, le=100, description="Required skills match percentage")
    preferred_score: int = Field(..., ge=0, le=100, description="Preferred skills match percentage")

    recommendation: RecommendationType = Field(..., description="Recommendation type")
    recommendation_text: str = Field(..., description="Human-readable recommendation")

    job_description: JobDescription = Field(..., description="Parsed job description")
    github_profile: GitHubProfile = Field(..., description="Analyzed GitHub profile")

    matched_skills: List[MatchedSkill] = Field(
        default_factory=list, description="Skills the candidate has"
    )
    missing_skills: List[Skill] = Field(default_factory=list, description="Skills the candidate lacks")

    gap_analysis: GapAnalysis = Field(..., description="Skill gap analysis")


class ErrorResponse(BaseModel):
    """Error response"""

    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    suggestion: Optional[str] = Field(None, description="Suggestion for resolution")
    details: Optional[Dict] = Field(None, description="Additional error details")
