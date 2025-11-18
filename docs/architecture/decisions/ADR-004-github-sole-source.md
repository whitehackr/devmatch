# ADR-004: GitHub as Sole Skill Source

**Status:** Accepted

**Date:** 2025-11-18

**Context:**

When evaluating a candidate's technical skills, multiple data sources are available:

1. **Resume/CV**: Self-reported skills, education, work history
2. **LinkedIn Profile**: Professional history, endorsements, certifications
3. **GitHub**: Actual code repositories and contributions
4. **LeetCode/HackerRank**: Coding challenge performance
5. **Stack Overflow**: Q&A activity, reputation
6. **Personal Website/Blog**: Technical writing, projects

Each source has different characteristics:

**Resume/LinkedIn:**
- **Pros**: Comprehensive work history, context about roles
- **Cons**: Self-reported (inflated/inaccurate), keyword-stuffed, no proof
- **Reliability**: Low - people routinely lie or exaggerate

**GitHub:**
- **Pros**: Actual code, verifiable, shows real work, public/auditable
- **Cons**: Not all developers use GitHub actively, open source ≠ professional work, tutorial repos inflate numbers
- **Reliability**: High - code doesn't lie (but repos can be misleading)

**Coding Platforms (LeetCode, etc.):**
- **Pros**: Objective performance metrics
- **Cons**: Algorithm skills ≠ job skills, many roles don't require LeetCode proficiency
- **Reliability**: Medium - measures one narrow skill dimension

**Stack Overflow:**
- **Pros**: Demonstrates problem-solving and communication
- **Cons**: Many excellent developers don't participate
- **Reliability**: Medium - active participation is minority behavior

**The Core Question:**

Should DevMatch analyze multiple sources (comprehensive but complex) or focus on GitHub exclusively (narrow but verifiable)?

**Decision:**

DevMatch will use **GitHub as the sole source** of skill evidence. We will not analyze resumes, LinkedIn profiles, or other sources.

**Rationale:**

1. **Verifiable Evidence**: GitHub code is public and auditable. Anyone can click through to repositories and verify the claims. Resumes are often fabricated.

2. **Actual Skills, Not Claims**: A resume might say "Expert in React", but GitHub shows if you've actually built React applications. Code is proof.

3. **Scope Management**: Analyzing multiple sources dramatically increases complexity:
   - Resume parsing is notoriously difficult (PDFs, varied formats)
   - LinkedIn scraping violates ToS and requires authentication
   - Integrating disparate data sources requires complex deduplication and weighting
   - Each source adds maintenance burden

4. **Unique Value Proposition**: Many services parse resumes. Few analyze actual code. GitHub-only analysis is differentiated.

5. **Developer Audience**: Our target users are developers/engineers who likely have GitHub profiles. For non-developers, this tool isn't applicable anyway.

6. **Honest Limitations**: By being GitHub-only, we're transparent about limitations. This builds trust compared to claiming comprehensive analysis while doing superficial keyword matching.

**Architectural Implications:**

```python
# Simple, focused architecture
class SkillAnalyzer:
    def analyze_skills(self, github_username: str) -> Skills:
        # Single source = single integration point
        github_data = self.github_client.fetch_profile(github_username)
        return self.extract_skills_from_github(github_data)

# vs. complex multi-source architecture (avoided)
class SkillAnalyzer:
    def analyze_skills(
        self,
        github_username: str = None,
        linkedin_url: str = None,
        resume_file: bytes = None,
        stackoverflow_id: int = None
    ) -> Skills:
        # Multiple sources = complex integration, deduplication, weighting...
        # Nightmare to maintain
```

**Consequences:**

**Positive:**
- **Simplicity**: Single API integration (GitHub), single data model
- **Verifiability**: Users can click through and verify every claim
- **Unique**: Different from resume-parsing tools
- **Honest**: Clear about what we analyze and don't analyze
- **Maintainable**: One integration to maintain, not five
- **Fast Development**: MVP ships in days, not weeks
- **Cost**: GitHub API is free (60 req/hour), resume parsing tools cost money

**Negative:**
- **Coverage Bias**: Excludes talented developers without active GitHub
- **False Negatives**: Private repos (work code) not analyzed
- **Hobby vs. Professional**: GitHub may show side projects, not job skills
- **Gaming**: Users could fake repos (though this requires actual code)
- **Narrow View**: Doesn't capture soft skills, communication, leadership
- **Entry-Level Disadvantage**: New developers may have thin GitHub profiles

**Mitigation Strategies:**

1. **Clear Messaging**: UI explicitly states "We analyze your public GitHub repositories" so expectations are set.

2. **Disclaimer**: Results page notes "This analysis is based on public code only and may not reflect your full skill set."

3. **Future Enhancement Path**: If the product validates, we can add resume upload as optional supplement, not replacement.

4. **Target Audience**: Focus marketing on developers with active GitHub profiles (where the tool works best).

5. **Private Repo Support**: Future feature could request OAuth to analyze private repos (with explicit user permission).

**User Segments & Applicability:**

| User Type | GitHub Activity | Tool Effectiveness |
|-----------|----------------|-------------------|
| **Active OSS Contributor** | High | Excellent |
| **Professional with Side Projects** | Medium | Good |
| **Employed Developer (Private Repos Only)** | Low | Poor |
| **Entry-Level / Bootcamp Grad** | Low-Medium | Fair |
| **Non-Developer** | None | Not Applicable |

**Alternatives Considered:**

1. **GitHub + Resume Upload**:
   - **Pros**: More comprehensive skill picture
   - **Cons**: Resume parsing is complex (PDFs, formats), adds significant development time
   - **Rejected**: Premature optimization before validating core concept

2. **GitHub + LinkedIn Scraping**:
   - **Pros**: Work history context
   - **Cons**: LinkedIn scraping violates ToS, requires login, fragile
   - **Rejected**: Legal/ethical concerns, technical fragility

3. **Resume Only (No GitHub)**:
   - **Pros**: Simpler for users (most have resumes)
   - **Cons**: Loses unique value prop, becomes commodity keyword matcher
   - **Rejected**: No differentiation

4. **Coding Platform Integration (LeetCode API)**:
   - **Pros**: Objective skill measurement
   - **Cons**: LeetCode skills ≠ job skills, limited coverage
   - **Rejected**: Narrow skill dimension, not all developers use platforms

**Philosophical Foundation:**

This decision reflects a core belief: **verifiable evidence > self-reported claims**. In hiring, candidates routinely exaggerate. GitHub provides objective proof that can't be faked (without writing actual code, at which point it's not fake anymore).

By constraining our scope to verifiable evidence, we trade coverage for credibility. This is the right trade-off for a tool that advises people on career decisions.

**Review Triggers:**

Re-evaluate this decision when:
- User feedback indicates GitHub-only is too limiting (>30% of feedback)
- Competitors successfully integrate multiple sources
- GitHub API limitations cause problems
- We have engineering resources to add sources without compromising quality
- Revenue/growth plateaus due to narrow applicability

**Future Evolution Path:**

If DevMatch succeeds, we could add sources in this order:
1. **Private GitHub repos** (OAuth, user permission) - natural extension
2. **Resume upload** (optional supplement) - user-controlled
3. **Portfolio links** (personal websites, blog posts) - manual review
4. **LinkedIn** (only if official API access granted) - ethical approach

**Notes:**

This is a philosophical and practical decision. We're building a tool that proves skills through code, not a comprehensive career assessment platform. By focusing on doing one thing exceptionally well (GitHub analysis), we create a defensible position and ship faster than trying to be everything to everyone.

The developers who benefit most from DevMatch are precisely those who should be using it: people who actively code and share their work. This creates a virtuous cycle where using the tool correlates with being a strong candidate.
