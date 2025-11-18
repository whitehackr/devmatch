"""Tests for Skill Extractor Service"""

import pytest
from app.services.skill_extractor import SkillExtractorService
from app.models.responses import SkillCategory


class TestSkillExtractorService:
    """Test skill extractor service"""

    def test_extract_skills_from_simple_text(self):
        """Test extracting skills from simple job description"""
        extractor = SkillExtractorService()

        text = """
        We are looking for a Python developer with Django experience.
        Must have PostgreSQL knowledge and AWS cloud skills.
        """

        required, preferred = extractor.extract_skills(text)

        skill_names = [s.name for s in required + preferred]
        assert "python" in skill_names
        assert "django" in skill_names
        assert "postgresql" in skill_names
        assert "aws" in skill_names

    def test_extract_skills_with_requirements_section(self, sample_job_description):
        """Test skill extraction with clear requirements section"""
        extractor = SkillExtractorService()

        required, preferred = extractor.extract_skills(sample_job_description)

        # Check required skills
        required_names = [s.name for s in required]
        assert "python" in required_names
        assert "django" in required_names or "flask" in required_names
        assert "postgresql" in required_names

        # Check preferred skills
        preferred_names = [s.name for s in preferred]
        assert "aws" in preferred_names
        assert "docker" in preferred_names

    def test_skill_importance_scoring(self):
        """Test that skills mentioned multiple times get higher importance"""
        extractor = SkillExtractorService()

        text = """
        Python Python Python required. Must have Python experience.
        Java mentioned once.
        """

        required, preferred = extractor.extract_skills(text)

        all_skills = required + preferred
        python_skill = next((s for s in all_skills if s.name == "python"), None)
        java_skill = next((s for s in all_skills if s.name == "java"), None)

        assert python_skill is not None
        assert java_skill is not None
        assert python_skill.importance > java_skill.importance

    def test_skill_categorization(self):
        """Test that skills are correctly categorized"""
        extractor = SkillExtractorService()

        text = """
        Required: Python, React, PostgreSQL, AWS, Docker
        """

        required, preferred = extractor.extract_skills(text)

        all_skills = required + preferred

        python_skill = next((s for s in all_skills if s.name == "python"), None)
        react_skill = next((s for s in all_skills if s.name == "react"), None)
        postgres_skill = next((s for s in all_skills if s.name == "postgresql"), None)
        aws_skill = next((s for s in all_skills if s.name == "aws"), None)
        docker_skill = next((s for s in all_skills if s.name == "docker"), None)

        assert python_skill.category == SkillCategory.LANGUAGE
        assert react_skill.category == SkillCategory.FRAMEWORK
        assert postgres_skill.category == SkillCategory.DATABASE
        assert aws_skill.category == SkillCategory.CLOUD
        assert docker_skill.category == SkillCategory.TOOL

    def test_normalize_skill_aliases(self):
        """Test that skill aliases are normalized to canonical form"""
        extractor = SkillExtractorService()

        text = """
        Experience with JS, React.js, and PostgreSQL.
        Python3 and golang required.
        """

        required, preferred = extractor.extract_skills(text)

        all_skills = required + preferred
        skill_names = [s.name for s in all_skills]

        # Check aliases are normalized
        assert "javascript" in skill_names  # JS -> javascript
        assert "react" in skill_names  # React.js -> react
        assert "postgresql" in skill_names
        assert "python" in skill_names  # Python3 -> python
        assert "go" in skill_names  # golang -> go

    def test_detect_required_vs_preferred(self):
        """Test distinguishing required from preferred skills"""
        extractor = SkillExtractorService()

        text = """
        Requirements:
        - Python required
        - Django must have

        Nice to have:
        - AWS experience
        - Docker knowledge
        """

        required, preferred = extractor.extract_skills(text)

        required_names = [s.name for s in required]
        preferred_names = [s.name for s in preferred]

        assert "python" in required_names
        assert "django" in required_names
        assert "aws" in preferred_names
        assert "docker" in preferred_names

    def test_empty_text(self):
        """Test handling of empty text"""
        extractor = SkillExtractorService()

        required, preferred = extractor.extract_skills("")

        assert required == []
        assert preferred == []

    def test_no_technical_skills(self):
        """Test handling of text with no technical skills"""
        extractor = SkillExtractorService()

        text = """
        We are looking for a great communicator who loves teamwork
        and has excellent problem-solving abilities.
        """

        required, preferred = extractor.extract_skills(text)

        assert len(required + preferred) == 0

    def test_skill_importance_based_on_context(self):
        """Test that 'required' context increases importance"""
        extractor = SkillExtractorService()

        text = """
        Required: Python
        Nice to have: Java
        """

        required, preferred = extractor.extract_skills(text)

        python_skill = next((s for s in required + preferred if s.name == "python"), None)
        java_skill = next((s for s in required + preferred if s.name == "java"), None)

        # Python should have higher importance due to "required" context
        assert python_skill.importance >= java_skill.importance

    def test_deduplication(self):
        """Test that duplicate skills are deduplicated"""
        extractor = SkillExtractorService()

        text = """
        Python Python Python
        React React
        Django
        """

        required, preferred = extractor.extract_skills(text)

        all_skills = required + preferred
        skill_names = [s.name for s in all_skills]

        # Each skill should appear only once
        assert skill_names.count("python") == 1
        assert skill_names.count("react") == 1
        assert skill_names.count("django") == 1
