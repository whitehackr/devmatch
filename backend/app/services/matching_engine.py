"""
Matching Engine

Compares job requirements against GitHub skills and generates recommendations.
Uses multi-factor scoring algorithm with weighted required/preferred split.
"""

from typing import List, Tuple
from app.models.responses import (
    JobDescription,
    GitHubProfile,
    MatchResult,
    MatchedSkill,
    Skill,
    GapAnalysis,
    RecommendationType,
)


class MatchingEngine:
    """Engine for matching job requirements to GitHub skills"""

    def __init__(self):
        # Weighting: required skills are more important than preferred
        self.required_weight = 0.7
        self.preferred_weight = 0.3

    def calculate_match(
        self, job_description: JobDescription, github_profile: GitHubProfile
    ) -> MatchResult:
        """
        Calculate match between job and GitHub profile.

        Args:
            job_description: Parsed job description with skills
            github_profile: Analyzed GitHub profile

        Returns:
            MatchResult with scores and recommendation
        """
        # Match required skills
        matched_required, missing_required = self._match_skills(
            job_description.required_skills, github_profile
        )

        # Match preferred skills
        matched_preferred, missing_preferred = self._match_skills(
            job_description.preferred_skills, github_profile
        )

        # Calculate scores
        required_score = self._calculate_score(
            len(matched_required), len(job_description.required_skills)
        )

        preferred_score = self._calculate_score(
            len(matched_preferred), len(job_description.preferred_skills)
        )

        # Overall score (weighted average)
        if len(job_description.preferred_skills) == 0:
            # If no preferred skills, overall = required
            overall_score = required_score
        else:
            overall_score = int(
                (self.required_weight * required_score)
                + (self.preferred_weight * preferred_score)
            )

        # Generate recommendation
        recommendation, recommendation_text = self._generate_recommendation(
            overall_score, required_score, len(missing_required)
        )

        # Gap analysis
        gap_analysis = self._analyze_gaps(missing_required + missing_preferred)

        return MatchResult(
            overall_score=overall_score,
            required_score=required_score,
            preferred_score=preferred_score,
            recommendation=recommendation,
            recommendation_text=recommendation_text,
            job_description=job_description,
            github_profile=github_profile,
            matched_skills=matched_required + matched_preferred,
            missing_skills=missing_required + missing_preferred,
            gap_analysis=gap_analysis,
        )

    def _match_skills(
        self, required_skills: List[Skill], github_profile: GitHubProfile
    ) -> Tuple[List[MatchedSkill], List[Skill]]:
        """
        Match skills against GitHub profile.

        Args:
            required_skills: List of skills to match
            github_profile: GitHub profile with skills

        Returns:
            Tuple of (matched_skills_with_evidence, missing_skills)
        """
        matched = []
        missing = []

        for skill in required_skills:
            evidence = self._find_evidence(skill, github_profile)

            if evidence:
                matched_skill = MatchedSkill(
                    name=skill.name,
                    category=skill.category,
                    importance=skill.importance,
                    evidence=evidence,
                )
                matched.append(matched_skill)
            else:
                missing.append(skill)

        return matched, missing

    def _find_evidence(self, skill: Skill, github_profile: GitHubProfile) -> str:
        """
        Find evidence of skill in GitHub profile.

        Args:
            skill: Skill to search for
            github_profile: GitHub profile

        Returns:
            Evidence string if found, empty string otherwise
        """
        skill_name = skill.name

        # Check languages
        for lang, percentage in github_profile.languages.items():
            if lang.lower() == skill_name.lower():
                return f"{percentage}% of code"

        # Check frameworks
        if skill_name in github_profile.frameworks:
            # Count how many projects (approximate)
            return "Used in projects"

        # Check tools
        if skill_name in github_profile.tools:
            return "Present in repositories"

        return ""

    def _calculate_score(self, matched: int, total: int) -> int:
        """
        Calculate percentage score.

        Args:
            matched: Number of matched skills
            total: Total number of skills

        Returns:
            Percentage score (0-100)
        """
        if total == 0:
            return 100  # Vacuous truth: no requirements means 100% match

        return int((matched / total) * 100)

    def _generate_recommendation(
        self, overall_score: int, required_score: int, critical_missing: int
    ) -> Tuple[RecommendationType, str]:
        """
        Generate recommendation based on scores.

        Args:
            overall_score: Overall match percentage
            required_score: Required skills match percentage
            critical_missing: Number of missing required skills

        Returns:
            Tuple of (recommendation_type, recommendation_text)
        """
        # Strong match: Apply now
        if overall_score >= 80 and required_score >= 85:
            return (
                RecommendationType.APPLY_NOW,
                "Strong match! Apply with confidence.",
            )

        # Good match: Competitive
        if overall_score >= 65 and required_score >= 70:
            return (
                RecommendationType.COMPETITIVE,
                "Good match. You're a competitive candidate - consider applying.",
            )

        # Moderate match: Depends on gaps
        if overall_score >= 50:
            if critical_missing <= 2:
                return (
                    RecommendationType.COMPETITIVE,
                    f"You're missing {critical_missing} key skill(s). Consider learning them and applying in 2-4 weeks.",
                )
            else:
                return (
                    RecommendationType.SKILL_GAP,
                    f"Focus on learning {critical_missing} critical skills first. Estimated time: 1-3 months.",
                )

        # Significant gap
        return (
            RecommendationType.SKILL_GAP,
            "Significant skill gap. Consider entry-level roles or alternative learning path first.",
        )

    def _analyze_gaps(self, missing_skills: List[Skill]) -> GapAnalysis:
        """
        Analyze skill gaps and estimate learning time.

        Args:
            missing_skills: List of missing skills

        Returns:
            GapAnalysis with metrics
        """
        # Count critical missing skills (importance >= 4)
        critical_missing = sum(1 for s in missing_skills if s.importance >= 4)

        # Estimate learning time (rough heuristic)
        # Critical skills: 4 weeks each
        # Non-critical: 2 weeks each
        critical_weeks = critical_missing * 4
        non_critical_weeks = (len(missing_skills) - critical_missing) * 2

        # Assume parallel learning for some skills
        learning_estimate_weeks = max(
            critical_weeks, int((critical_weeks + non_critical_weeks) * 0.6)
        )

        return GapAnalysis(
            critical_missing=critical_missing,
            total_missing=len(missing_skills),
            learning_estimate_weeks=learning_estimate_weeks,
        )
