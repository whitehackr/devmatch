"""
Comprehensive taxonomy of technical skills with aliases and categorization.

This taxonomy is used for skill extraction and normalization across job descriptions
and GitHub profiles.
"""

from typing import Dict, List, Optional
from app.models.responses import SkillCategory


# Skill taxonomy: canonical_name -> {aliases, category}
SKILL_TAXONOMY: Dict[str, Dict] = {
    # Programming Languages
    "python": {
        "aliases": ["python", "python3", "py", "python2"],
        "category": SkillCategory.LANGUAGE,
    },
    "javascript": {
        "aliases": ["javascript", "js", "es6", "es2015", "es2020", "ecmascript"],
        "category": SkillCategory.LANGUAGE,
    },
    "typescript": {
        "aliases": ["typescript", "ts"],
        "category": SkillCategory.LANGUAGE,
    },
    "java": {
        "aliases": ["java", "java8", "java11", "java17"],
        "category": SkillCategory.LANGUAGE,
    },
    "csharp": {
        "aliases": ["c#", "csharp", "c sharp", ".net"],
        "category": SkillCategory.LANGUAGE,
    },
    "go": {
        "aliases": ["go", "golang"],
        "category": SkillCategory.LANGUAGE,
    },
    "rust": {
        "aliases": ["rust"],
        "category": SkillCategory.LANGUAGE,
    },
    "ruby": {
        "aliases": ["ruby"],
        "category": SkillCategory.LANGUAGE,
    },
    "php": {
        "aliases": ["php", "php7", "php8"],
        "category": SkillCategory.LANGUAGE,
    },
    "swift": {
        "aliases": ["swift"],
        "category": SkillCategory.LANGUAGE,
    },
    "kotlin": {
        "aliases": ["kotlin"],
        "category": SkillCategory.LANGUAGE,
    },
    "scala": {
        "aliases": ["scala"],
        "category": SkillCategory.LANGUAGE,
    },
    "r": {
        "aliases": ["r"],
        "category": SkillCategory.LANGUAGE,
    },
    "matlab": {
        "aliases": ["matlab"],
        "category": SkillCategory.LANGUAGE,
    },
    "cpp": {
        "aliases": ["c++", "cpp", "cplusplus"],
        "category": SkillCategory.LANGUAGE,
    },
    "c": {
        "aliases": ["c"],
        "category": SkillCategory.LANGUAGE,
    },
    "sql": {
        "aliases": ["sql", "t-sql", "pl/sql"],
        "category": SkillCategory.LANGUAGE,
    },
    "shell": {
        "aliases": ["shell", "bash", "sh", "zsh"],
        "category": SkillCategory.LANGUAGE,
    },
    "powershell": {
        "aliases": ["powershell", "pwsh"],
        "category": SkillCategory.LANGUAGE,
    },
    # Web Frameworks
    "react": {
        "aliases": ["react", "reactjs", "react.js"],
        "category": SkillCategory.FRAMEWORK,
    },
    "angular": {
        "aliases": ["angular", "angularjs"],
        "category": SkillCategory.FRAMEWORK,
    },
    "vue": {
        "aliases": ["vue", "vuejs", "vue.js"],
        "category": SkillCategory.FRAMEWORK,
    },
    "svelte": {
        "aliases": ["svelte"],
        "category": SkillCategory.FRAMEWORK,
    },
    "nextjs": {
        "aliases": ["next.js", "nextjs", "next"],
        "category": SkillCategory.FRAMEWORK,
    },
    "nuxt": {
        "aliases": ["nuxt", "nuxtjs", "nuxt.js"],
        "category": SkillCategory.FRAMEWORK,
    },
    "django": {
        "aliases": ["django"],
        "category": SkillCategory.FRAMEWORK,
    },
    "flask": {
        "aliases": ["flask"],
        "category": SkillCategory.FRAMEWORK,
    },
    "fastapi": {
        "aliases": ["fastapi"],
        "category": SkillCategory.FRAMEWORK,
    },
    "express": {
        "aliases": ["express", "expressjs", "express.js"],
        "category": SkillCategory.FRAMEWORK,
    },
    "nestjs": {
        "aliases": ["nest", "nestjs", "nest.js"],
        "category": SkillCategory.FRAMEWORK,
    },
    "spring": {
        "aliases": ["spring", "spring boot", "springboot"],
        "category": SkillCategory.FRAMEWORK,
    },
    "rails": {
        "aliases": ["rails", "ruby on rails", "ror"],
        "category": SkillCategory.FRAMEWORK,
    },
    "laravel": {
        "aliases": ["laravel"],
        "category": SkillCategory.FRAMEWORK,
    },
    "aspnet": {
        "aliases": ["asp.net", "aspnet"],
        "category": SkillCategory.FRAMEWORK,
    },
    # Databases
    "postgresql": {
        "aliases": ["postgresql", "postgres", "psql"],
        "category": SkillCategory.DATABASE,
    },
    "mysql": {
        "aliases": ["mysql"],
        "category": SkillCategory.DATABASE,
    },
    "mongodb": {
        "aliases": ["mongodb", "mongo"],
        "category": SkillCategory.DATABASE,
    },
    "redis": {
        "aliases": ["redis"],
        "category": SkillCategory.DATABASE,
    },
    "elasticsearch": {
        "aliases": ["elasticsearch", "elastic"],
        "category": SkillCategory.DATABASE,
    },
    "cassandra": {
        "aliases": ["cassandra"],
        "category": SkillCategory.DATABASE,
    },
    "dynamodb": {
        "aliases": ["dynamodb"],
        "category": SkillCategory.DATABASE,
    },
    "sqlserver": {
        "aliases": ["sql server", "mssql", "sqlserver"],
        "category": SkillCategory.DATABASE,
    },
    "oracle": {
        "aliases": ["oracle", "oracle db"],
        "category": SkillCategory.DATABASE,
    },
    "sqlite": {
        "aliases": ["sqlite"],
        "category": SkillCategory.DATABASE,
    },
    # Cloud & DevOps
    "aws": {
        "aliases": ["aws", "amazon web services"],
        "category": SkillCategory.CLOUD,
    },
    "azure": {
        "aliases": ["azure", "microsoft azure"],
        "category": SkillCategory.CLOUD,
    },
    "gcp": {
        "aliases": ["gcp", "google cloud", "google cloud platform"],
        "category": SkillCategory.CLOUD,
    },
    "docker": {
        "aliases": ["docker"],
        "category": SkillCategory.TOOL,
    },
    "kubernetes": {
        "aliases": ["kubernetes", "k8s"],
        "category": SkillCategory.TOOL,
    },
    "terraform": {
        "aliases": ["terraform"],
        "category": SkillCategory.TOOL,
    },
    "ansible": {
        "aliases": ["ansible"],
        "category": SkillCategory.TOOL,
    },
    "jenkins": {
        "aliases": ["jenkins"],
        "category": SkillCategory.TOOL,
    },
    "gitlab-ci": {
        "aliases": ["gitlab ci", "gitlab-ci", "gitlab ci/cd"],
        "category": SkillCategory.TOOL,
    },
    "github-actions": {
        "aliases": ["github actions", "github-actions"],
        "category": SkillCategory.TOOL,
    },
    "circleci": {
        "aliases": ["circleci", "circle ci"],
        "category": SkillCategory.TOOL,
    },
    # Data Science & ML
    "pytorch": {
        "aliases": ["pytorch", "torch"],
        "category": SkillCategory.FRAMEWORK,
    },
    "tensorflow": {
        "aliases": ["tensorflow", "tf"],
        "category": SkillCategory.FRAMEWORK,
    },
    "scikit-learn": {
        "aliases": ["scikit-learn", "sklearn", "scikit learn"],
        "category": SkillCategory.FRAMEWORK,
    },
    "pandas": {
        "aliases": ["pandas"],
        "category": SkillCategory.FRAMEWORK,
    },
    "numpy": {
        "aliases": ["numpy"],
        "category": SkillCategory.FRAMEWORK,
    },
    "keras": {
        "aliases": ["keras"],
        "category": SkillCategory.FRAMEWORK,
    },
    "spark": {
        "aliases": ["spark", "apache spark", "pyspark"],
        "category": SkillCategory.FRAMEWORK,
    },
    "airflow": {
        "aliases": ["airflow", "apache airflow"],
        "category": SkillCategory.FRAMEWORK,
    },
    # Testing
    "pytest": {
        "aliases": ["pytest"],
        "category": SkillCategory.TOOL,
    },
    "jest": {
        "aliases": ["jest"],
        "category": SkillCategory.TOOL,
    },
    "junit": {
        "aliases": ["junit"],
        "category": SkillCategory.TOOL,
    },
    "selenium": {
        "aliases": ["selenium"],
        "category": SkillCategory.TOOL,
    },
    "cypress": {
        "aliases": ["cypress"],
        "category": SkillCategory.TOOL,
    },
    # Version Control & Tools
    "git": {
        "aliases": ["git"],
        "category": SkillCategory.TOOL,
    },
    "linux": {
        "aliases": ["linux", "unix"],
        "category": SkillCategory.TOOL,
    },
    "nginx": {
        "aliases": ["nginx"],
        "category": SkillCategory.TOOL,
    },
    "apache": {
        "aliases": ["apache", "apache http"],
        "category": SkillCategory.TOOL,
    },
    # Concepts
    "rest-api": {
        "aliases": ["rest", "restful", "rest api", "rest apis"],
        "category": SkillCategory.CONCEPT,
    },
    "graphql": {
        "aliases": ["graphql"],
        "category": SkillCategory.CONCEPT,
    },
    "microservices": {
        "aliases": ["microservices", "microservice"],
        "category": SkillCategory.CONCEPT,
    },
    "ci-cd": {
        "aliases": ["ci/cd", "ci-cd", "continuous integration", "continuous deployment"],
        "category": SkillCategory.CONCEPT,
    },
    "agile": {
        "aliases": ["agile", "scrum", "kanban"],
        "category": SkillCategory.CONCEPT,
    },
    "tdd": {
        "aliases": ["tdd", "test driven development", "test-driven development"],
        "category": SkillCategory.CONCEPT,
    },
}


# Build reverse lookup: alias -> canonical name
_ALIAS_TO_CANONICAL: Dict[str, str] = {}
for canonical, data in SKILL_TAXONOMY.items():
    for alias in data["aliases"]:
        _ALIAS_TO_CANONICAL[alias.lower()] = canonical


def normalize_skill_name(skill: str) -> Optional[str]:
    """
    Normalize a skill name to its canonical form.

    Args:
        skill: Raw skill name (e.g., "JS", "python3", "React.js")

    Returns:
        Canonical skill name (e.g., "javascript", "python", "react") or None if not found
    """
    skill_lower = skill.lower().strip()
    return _ALIAS_TO_CANONICAL.get(skill_lower)


def get_skill_category(canonical_skill: str) -> Optional[SkillCategory]:
    """
    Get the category of a canonical skill name.

    Args:
        canonical_skill: Canonical skill name

    Returns:
        SkillCategory or None if not found
    """
    skill_data = SKILL_TAXONOMY.get(canonical_skill)
    return skill_data["category"] if skill_data else None


def get_all_skill_patterns() -> List[str]:
    """
    Get all skill aliases for pattern matching.

    Returns:
        List of all skill aliases
    """
    patterns = []
    for data in SKILL_TAXONOMY.values():
        patterns.extend(data["aliases"])
    return patterns
