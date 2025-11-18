"""
Skill Extractor Service

Extracts technical skills from job description text using NLP and pattern matching.
Classifies skills as required vs preferred and assigns importance scores.
"""

import re
from typing import List, Tuple, Dict
from collections import defaultdict

from app.models.responses import Skill, SkillCategory
from app.utils.skill_taxonomy import (
    normalize_skill_name,
    get_skill_category,
    get_all_skill_patterns,
)


class SkillExtractorService:
    """Service for extracting skills from job descriptions"""

    def __init__(self):
        """Initialize skill extractor"""
        self.skill_patterns = get_all_skill_patterns()

        # Section keywords for classification
        self.required_keywords = [
            "required",
            "must have",
            "must-have",
            "essential",
            "mandatory",
            "requirement",
            "requirements",
            "qualifications",
        ]

        self.preferred_keywords = [
            "preferred",
            "nice to have",
            "nice-to-have",
            "bonus",
            "plus",
            "optional",
            "desired",
        ]

    def extract_skills(self, text: str) -> Tuple[List[Skill], List[Skill]]:
        """
        Extract skills from job description text.

        Args:
            text: Job description text

        Returns:
            Tuple of (required_skills, preferred_skills)
        """
        if not text or not text.strip():
            return [], []

        # Normalize text
        text_lower = text.lower()

        # Detect sections
        sections = self._detect_sections(text_lower)

        # Extract skills with counts and context
        skill_counts = self._count_skill_mentions(text_lower)

        if not skill_counts:
            return [], []

        # Calculate importance scores
        skill_scores = self._calculate_importance_scores(skill_counts, text_lower, sections)

        # Classify as required vs preferred
        required_skills, preferred_skills = self._classify_skills(skill_scores, sections, text_lower)

        return required_skills, preferred_skills

    def _detect_sections(self, text: str) -> Dict[str, Tuple[int, int]]:
        """
        Detect requirement and preferred sections in text.

        Args:
            text: Lowercased job description

        Returns:
            Dict with 'required' and 'preferred' section positions (start, end)
        """
        sections = {}

        # Find required section
        for keyword in self.required_keywords:
            match = re.search(rf"\b{re.escape(keyword)}\b", text)
            if match:
                # Section starts at keyword, ends at next section or end of text
                start = match.start()

                # Find end (next section keyword or end of text)
                end = len(text)
                for other_keyword in self.preferred_keywords:
                    other_match = re.search(rf"\b{re.escape(other_keyword)}\b", text[start:])
                    if other_match:
                        end = start + other_match.start()
                        break

                sections["required"] = (start, end)
                break

        # Find preferred section
        for keyword in self.preferred_keywords:
            match = re.search(rf"\b{re.escape(keyword)}\b", text)
            if match:
                start = match.start()
                end = len(text)

                # If required section exists and comes after, end at required section
                if "required" in sections and sections["required"][0] > start:
                    end = sections["required"][0]

                sections["preferred"] = (start, end)
                break

        return sections

    def _count_skill_mentions(self, text: str) -> Dict[str, int]:
        """
        Count mentions of each skill in text.

        Args:
            text: Lowercased job description

        Returns:
            Dict mapping canonical skill name -> count
        """
        skill_counts = defaultdict(int)

        # Pattern matching for each skill alias
        for pattern in self.skill_patterns:
            # Use word boundaries to avoid partial matches
            # Special handling for patterns with special characters
            if any(char in pattern for char in ["+", "#", "."]):
                # Exact match for special patterns
                escaped_pattern = re.escape(pattern)
                regex = rf"(?<!\w){escaped_pattern}(?!\w)"
            else:
                regex = rf"\b{re.escape(pattern)}\b"

            matches = re.findall(regex, text, re.IGNORECASE)

            if matches:
                canonical = normalize_skill_name(pattern)
                if canonical:
                    skill_counts[canonical] += len(matches)

        return dict(skill_counts)

    def _calculate_importance_scores(
        self,
        skill_counts: Dict[str, int],
        text: str,
        sections: Dict[str, Tuple[int, int]],
    ) -> Dict[str, int]:
        """
        Calculate importance score (1-5) for each skill.

        Scoring factors:
        - Frequency of mentions
        - Context (required section vs preferred)
        - Position in text (earlier = slightly more important)

        Args:
            skill_counts: Skill mention counts
            text: Lowercased job description
            sections: Detected sections

        Returns:
            Dict mapping canonical skill name -> importance score (1-5)
        """
        scores = {}

        for skill, count in skill_counts.items():
            # Base score from frequency
            if count >= 5:
                score = 5
            elif count >= 3:
                score = 4
            elif count == 2:
                score = 3
            else:
                score = 2

            # Bonus if in required section
            if "required" in sections:
                # Check if skill appears in required section
                req_start, req_end = sections["required"]
                required_text = text[req_start:req_end]

                # Get skill aliases
                from app.utils.skill_taxonomy import SKILL_TAXONOMY

                if skill in SKILL_TAXONOMY:
                    aliases = SKILL_TAXONOMY[skill]["aliases"]
                    for alias in aliases:
                        if alias.lower() in required_text:
                            score = min(5, score + 1)  # Cap at 5
                            break

            scores[skill] = score

        return scores

    def _classify_skills(
        self,
        skill_scores: Dict[str, int],
        sections: Dict[str, Tuple[int, int]],
        text: str,
    ) -> Tuple[List[Skill], List[Skill]]:
        """
        Classify skills as required or preferred.

        Required criteria:
        - Appears in requirements section, OR
        - Importance score >= 4

        Args:
            skill_scores: Skill importance scores
            sections: Detected sections
            text: Lowercased job description

        Returns:
            Tuple of (required_skills, preferred_skills)
        """
        from app.utils.skill_taxonomy import SKILL_TAXONOMY

        required_skills = []
        preferred_skills = []

        for skill, importance in skill_scores.items():
            category = get_skill_category(skill)

            if not category:
                continue  # Skip if category not found

            # Check if in required section
            in_required_section = False
            if "required" in sections:
                req_start, req_end = sections["required"]
                required_text = text[req_start:req_end]

                aliases = SKILL_TAXONOMY[skill]["aliases"]
                for alias in aliases:
                    if alias.lower() in required_text:
                        in_required_section = True
                        break

            # Classify
            skill_obj = Skill(name=skill, category=category, importance=importance)

            if in_required_section or importance >= 4:
                required_skills.append(skill_obj)
            else:
                preferred_skills.append(skill_obj)

        # Sort by importance (descending)
        required_skills.sort(key=lambda s: s.importance, reverse=True)
        preferred_skills.sort(key=lambda s: s.importance, reverse=True)

        return required_skills, preferred_skills
