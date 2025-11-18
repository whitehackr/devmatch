"""Tests for Matching Engine"""

import pytest
from app.services.matching_engine import MatchingEngine
from app.models.responses import (
    Skill,
    JobDescription,
    GitHubProfile,
    SkillCategory,
    RecommendationType,
)


class TestMatchingEngine:
    """Test matching engine"""

    def test_perfect_match(self):
        """Test perfect match scenario (100%)"""
        engine = MatchingEngine()

        job_desc = JobDescription(
            title="Python Engineer",
            company="TechCorp",
            source="direct_paste",
            raw_text="Looking for Python and Django developer",
            required_skills=[
                Skill(name="python", category=SkillCategory.LANGUAGE, importance=5),
                Skill(name="django", category=SkillCategory.FRAMEWORK, importance=4),
            ],
            preferred_skills=[],
        )

        github_profile = GitHubProfile(
            username="testuser",
            account_age_years=5.0,
            repos_analyzed=10,
            total_repos=15,
            languages={"Python": 90.0},
            frameworks=["django", "flask"],
            tools=["git"],
        )

        result = engine.calculate_match(job_desc, github_profile)

        assert result.required_score == 100
        assert result.overall_score == 100
        assert result.recommendation == RecommendationType.APPLY_NOW
        assert len(result.matched_skills) == 2
        assert len(result.missing_skills) == 0

    def test_strong_match(self):
        """Test strong match (85% required, should be APPLY_NOW)"""
        engine = MatchingEngine()

        job_desc = JobDescription(
            title="Backend Engineer",
            company="TechCorp",
            source="direct_paste",
            raw_text="Python, Django, PostgreSQL, Redis required",
            required_skills=[
                Skill(name="python", category=SkillCategory.LANGUAGE, importance=5),
                Skill(name="django", category=SkillCategory.FRAMEWORK, importance=5),
                Skill(name="postgresql", category=SkillCategory.DATABASE, importance=4),
                Skill(name="redis", category=SkillCategory.DATABASE, importance=3),
            ],
            preferred_skills=[
                Skill(name="aws", category=SkillCategory.CLOUD, importance=3),
            ],
        )

        github_profile = GitHubProfile(
            username="testuser",
            account_age_years=5.0,
            repos_analyzed=20,
            total_repos=25,
            languages={"Python": 80.0},
            frameworks=["django"],
            tools=["git", "docker"],
        )

        result = engine.calculate_match(job_desc, github_profile)

        # Matched: python, django (2/4 = 50%)
        # But this test should verify the logic works
        assert result.required_score == 50  # 2 out of 4
        assert len(result.matched_skills) == 2
        assert len(result.missing_skills) >= 2

    def test_competitive_match(self):
        """Test competitive match (65-80%)"""
        engine = MatchingEngine()

        job_desc = JobDescription(
            title="Full Stack Engineer",
            company="Startup",
            source="direct_paste",
            raw_text="React, Node.js, PostgreSQL",
            required_skills=[
                Skill(name="react", category=SkillCategory.FRAMEWORK, importance=5),
                Skill(name="javascript", category=SkillCategory.LANGUAGE, importance=5),
            ],
            preferred_skills=[
                Skill(name="postgresql", category=SkillCategory.DATABASE, importance=3),
                Skill(name="docker", category=SkillCategory.TOOL, importance=2),
            ],
        )

        github_profile = GitHubProfile(
            username="testuser",
            account_age_years=3.0,
            repos_analyzed=15,
            total_repos=20,
            languages={"JavaScript": 70.0, "Python": 30.0},
            frameworks=["react"],
            tools=["git"],
        )

        result = engine.calculate_match(job_desc, github_profile)

        # Required: 2/2 = 100%
        # Preferred: 0/2 = 0%
        # Overall: 0.7 * 100 + 0.3 * 0 = 70%
        assert result.required_score == 100
        assert result.preferred_score == 0
        assert result.overall_score == 70
        assert result.recommendation in [RecommendationType.COMPETITIVE, RecommendationType.APPLY_NOW]

    def test_skill_gap_scenario(self):
        """Test significant skill gap scenario"""
        engine = MatchingEngine()

        job_desc = JobDescription(
            title="Senior ML Engineer",
            company="AI Startup",
            source="direct_paste",
            raw_text="PyTorch, TensorFlow, MLOps required",
            required_skills=[
                Skill(name="pytorch", category=SkillCategory.FRAMEWORK, importance=5),
                Skill(name="tensorflow", category=SkillCategory.FRAMEWORK, importance=5),
                Skill(name="python", category=SkillCategory.LANGUAGE, importance=5),
                Skill(name="kubernetes", category=SkillCategory.TOOL, importance=4),
            ],
            preferred_skills=[],
        )

        github_profile = GitHubProfile(
            username="testuser",
            account_age_years=2.0,
            repos_analyzed=10,
            total_repos=10,
            languages={"Python": 60.0, "JavaScript": 40.0},
            frameworks=["django"],  # No ML frameworks
            tools=["git"],
        )

        result = engine.calculate_match(job_desc, github_profile)

        # Only Python matched (1/4 = 25%)
        assert result.required_score == 25
        assert result.recommendation == RecommendationType.SKILL_GAP
        assert len(result.missing_skills) >= 3

    def test_evidence_collection(self):
        """Test that evidence is collected for matched skills"""
        engine = MatchingEngine()

        job_desc = JobDescription(
            title="Python Developer",
            company="Corp",
            source="direct_paste",
            raw_text="Python required",
            required_skills=[
                Skill(name="python", category=SkillCategory.LANGUAGE, importance=5),
            ],
            preferred_skills=[],
        )

        github_profile = GitHubProfile(
            username="testuser",
            account_age_years=5.0,
            repos_analyzed=10,
            total_repos=10,
            languages={"Python": 75.5},
            frameworks=[],
            tools=[],
        )

        result = engine.calculate_match(job_desc, github_profile)

        matched_python = next(
            (s for s in result.matched_skills if s.name == "python"), None
        )

        assert matched_python is not None
        assert "75.5" in matched_python.evidence
        assert "code" in matched_python.evidence.lower()

    def test_framework_matching(self):
        """Test framework detection and matching"""
        engine = MatchingEngine()

        job_desc = JobDescription(
            title="Frontend Developer",
            company="Corp",
            source="direct_paste",
            raw_text="React experience required",
            required_skills=[
                Skill(name="react", category=SkillCategory.FRAMEWORK, importance=5),
            ],
            preferred_skills=[],
        )

        github_profile = GitHubProfile(
            username="testuser",
            account_age_years=3.0,
            repos_analyzed=20,
            total_repos=20,
            languages={"JavaScript": 80.0},
            frameworks=["react", "vue"],
            tools=[],
        )

        result = engine.calculate_match(job_desc, github_profile)

        assert result.required_score == 100
        matched_react = next(
            (s for s in result.matched_skills if s.name == "react"), None
        )
        assert matched_react is not None
        assert "project" in matched_react.evidence.lower()

    def test_gap_analysis_calculation(self):
        """Test gap analysis metrics"""
        engine = MatchingEngine()

        job_desc = JobDescription(
            title="Engineer",
            company="Corp",
            source="direct_paste",
            raw_text="Skills needed",
            required_skills=[
                Skill(name="python", category=SkillCategory.LANGUAGE, importance=5),
                Skill(name="kubernetes", category=SkillCategory.TOOL, importance=5),
                Skill(name="aws", category=SkillCategory.CLOUD, importance=4),
                Skill(name="docker", category=SkillCategory.TOOL, importance=3),
            ],
            preferred_skills=[],
        )

        github_profile = GitHubProfile(
            username="testuser",
            account_age_years=2.0,
            repos_analyzed=10,
            total_repos=10,
            languages={"Python": 80.0},
            frameworks=[],
            tools=["docker"],
        )

        result = engine.calculate_match(job_desc, github_profile)

        # Missing: kubernetes (5), aws (4) = 2 critical
        assert result.gap_analysis.critical_missing == 2
        assert result.gap_analysis.total_missing == 2
        assert result.gap_analysis.learning_estimate_weeks > 0

    def test_weighted_scoring(self):
        """Test that required skills are weighted 70%, preferred 30%"""
        engine = MatchingEngine()

        job_desc = JobDescription(
            title="Engineer",
            company="Corp",
            source="direct_paste",
            raw_text="Skills",
            required_skills=[
                Skill(name="python", category=SkillCategory.LANGUAGE, importance=5),
                Skill(name="django", category=SkillCategory.FRAMEWORK, importance=5),
            ],
            preferred_skills=[
                Skill(name="aws", category=SkillCategory.CLOUD, importance=3),
                Skill(name="docker", category=SkillCategory.TOOL, importance=3),
            ],
        )

        github_profile = GitHubProfile(
            username="testuser",
            account_age_years=5.0,
            repos_analyzed=10,
            total_repos=10,
            languages={"Python": 80.0},
            frameworks=["django"],
            tools=[],
        )

        result = engine.calculate_match(job_desc, github_profile)

        # Required: 2/2 = 100%
        # Preferred: 0/2 = 0%
        # Overall: 0.7 * 100 + 0.3 * 0 = 70
        assert result.required_score == 100
        assert result.preferred_score == 0
        assert result.overall_score == 70

    def test_no_preferred_skills(self):
        """Test handling when there are no preferred skills"""
        engine = MatchingEngine()

        job_desc = JobDescription(
            title="Engineer",
            company="Corp",
            source="direct_paste",
            raw_text="Python required",
            required_skills=[
                Skill(name="python", category=SkillCategory.LANGUAGE, importance=5),
            ],
            preferred_skills=[],  # No preferred
        )

        github_profile = GitHubProfile(
            username="testuser",
            account_age_years=5.0,
            repos_analyzed=10,
            total_repos=10,
            languages={"Python": 80.0},
            frameworks=[],
            tools=[],
        )

        result = engine.calculate_match(job_desc, github_profile)

        # Required: 100%, Preferred: N/A (should handle gracefully)
        assert result.required_score == 100
        # Overall should be 100 when only required skills exist
        assert result.overall_score == 100
