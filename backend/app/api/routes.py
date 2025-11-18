"""API Routes"""

from fastapi import APIRouter, HTTPException, status
from app.models.requests import AnalyzeRequest
from app.models.responses import HealthResponse, MatchResult, ErrorResponse
from app.services.job_scraper import JobScraperService
from app.services.skill_extractor import SkillExtractorService
from app.services.github_analyzer import GitHubAnalyzerService
from app.services.matching_engine import MatchingEngine
from app.config import settings

router = APIRouter()

# Initialize services
job_scraper = JobScraperService()
skill_extractor = SkillExtractorService()
github_analyzer = GitHubAnalyzerService()
matching_engine = MatchingEngine()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version=settings.version)


@router.post(
    "/api/analyze",
    response_model=MatchResult,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "GitHub user not found"},
        422: {"model": ErrorResponse, "description": "Processing error"},
        504: {"model": ErrorResponse, "description": "Timeout"},
    },
)
async def analyze_job_match(request: AnalyzeRequest) -> MatchResult:
    """
    Analyze how well a GitHub profile matches a job description.

    This endpoint:
    1. Scrapes/processes the job description
    2. Extracts required and preferred skills
    3. Analyzes the GitHub profile
    4. Calculates match scores
    5. Generates recommendation

    Args:
        request: AnalyzeRequest with job_url or job_description and github_username

    Returns:
        MatchResult with scores, matched/missing skills, and recommendation

    Raises:
        HTTPException: Various errors (validation, not found, timeout)
    """
    try:
        # Step 1: Scrape job description
        try:
            job_description = job_scraper.scrape_job(
                job_url=request.job_url,
                job_description_text=request.job_description,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": "scraping_failed",
                    "message": f"Failed to process job description: {str(e)}",
                    "suggestion": "Try pasting the job description directly instead",
                },
            )

        # Step 2: Extract skills from job description
        try:
            required_skills, preferred_skills = skill_extractor.extract_skills(
                job_description.raw_text
            )

            job_description.required_skills = required_skills
            job_description.preferred_skills = preferred_skills

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": "skill_extraction_failed",
                    "message": f"Failed to extract skills: {str(e)}",
                    "suggestion": "Ensure the job description contains technical skills",
                },
            )

        # Step 3: Analyze GitHub profile
        try:
            github_profile = await github_analyzer.analyze_profile(request.github_username)

        except Exception as e:
            error_message = str(e)

            if "not found" in error_message.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "error": "github_user_not_found",
                        "message": f"GitHub user '{request.github_username}' not found",
                        "suggestion": "Please verify the username and try again",
                    },
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={
                        "error": "github_analysis_failed",
                        "message": f"Failed to analyze GitHub profile: {error_message}",
                        "suggestion": "Try again or check if the profile is public",
                    },
                )

        # Step 4: Calculate match
        try:
            match_result = matching_engine.calculate_match(job_description, github_profile)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "matching_failed",
                    "message": f"Failed to calculate match: {str(e)}",
                },
            )

        return match_result

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_error",
                "message": f"An unexpected error occurred: {str(e)}",
            },
        )
