# ADR-003: Matching Algorithm Design

**Status:** Accepted

**Date:** 2025-11-18

**Context:**

The core value of DevMatch is the matching algorithm that compares job requirements to GitHub skills and produces an actionable recommendation. Several critical questions need answers:

1. **How do we score the match?** Simple percentage, weighted scoring, ML-based, confidence intervals?

2. **How do we differentiate required vs. preferred skills?** They should not be weighted equally, but by how much?

3. **What thresholds determine recommendations?** When is someone "ready to apply" vs. "needs to learn first"?

4. **How do we handle partial matches?** If someone has Python but the job requires "5+ years Python", is that a match?

5. **Should the algorithm be transparent or a black box?** Can users understand why they got a certain score?

6. **How do we account for skill importance?** Not all skills are equal - some are critical, others nice-to-have.

**Decision:**

We will implement a **transparent, multi-factor matching algorithm** with these components:

### 1. Skill Normalization
Convert all skills to canonical form to prevent mismatches:
- "JS", "JavaScript", "ES6" → "javascript"
- "Python3", "python" → "python"

### 2. Binary Matching
For each skill, determine if the candidate has it (yes/no):
- Language: Present in GitHub language statistics (any percentage)
- Framework: Detected in dependencies or code patterns
- Tool: Found in repository configuration files

### 3. Score Calculation

```
Required Match Score = (Matched Required Skills / Total Required Skills) × 100
Preferred Match Score = (Matched Preferred Skills / Total Preferred Skills) × 100
Overall Score = (0.7 × Required Score) + (0.3 × Preferred Score)
```

**Rationale for 70/30 weighting:**
- Required skills are often deal-breakers in hiring
- Most successful hires match 80-90% of required skills
- Preferred skills provide differentiation but aren't mandatory
- Industry research shows required skills are 2-3x more important in hiring decisions

### 4. Recommendation Thresholds

```
IF overall_score ≥ 80 AND required_score ≥ 85:
    → APPLY_NOW
    "Strong match! Apply with confidence."

ELIF overall_score ≥ 65 AND required_score ≥ 70:
    → COMPETITIVE
    "Good match. Consider applying while strengthening gaps."

ELIF overall_score ≥ 50:
    IF critical_missing_count ≤ 2:
        → COMPETITIVE
        "Focus on 2 key skills, then apply in 2-4 weeks."
    ELSE:
        → SKILL_GAP
        "Learn 5+ critical skills first. Estimated time: 1-3 months."

ELSE:
    → SKILL_GAP
    "Significant gap. Consider entry-level roles or alternative paths."
```

**Rationale for thresholds:**
- 80%+ represents "strong match" - few perfect 100% matches exist in real hiring
- 65-80% is "competitive" - many successful hires fall here
- 50-65% with few critical gaps is "learnable" - focused study can close gap
- <50% suggests fundamental mismatch

### 5. Evidence Collection
For each matched skill, record proof:
- Language: "45.2% of your code"
- Framework: "Used in 8 projects"
- Tool: "Present in repositories"

This provides credibility and helps users understand the match.

### 6. Gap Analysis
Rank missing skills by importance (5 → 1) and show top 10 to avoid overwhelming users.

**Rationale:**

1. **Transparency**: Users can see exactly how the score was calculated. No black-box ML that could be biased or inexplicable.

2. **Actionability**: Recommendations are specific ("learn these 2 skills") not vague ("improve your profile").

3. **Honesty**: 80% threshold acknowledges that perfect matches are rare. Sets realistic expectations.

4. **Conservatism**: We bias toward "learn first" over "apply now" to protect users from wasted applications and damaged confidence.

5. **Evidence-Based**: Showing GitHub proof builds trust and helps users articulate their skills in applications.

**Technical Implementation:**

```python
def calculate_match(job_skills: Dict, github_skills: Dict) -> MatchResult:
    # Normalize skill names
    job_skills_normalized = normalize_skills(job_skills)
    github_skills_normalized = normalize_skills(github_skills)

    # Match required skills
    required_matches = []
    required_missing = []
    for skill in job_skills['required']:
        if skill['name'] in github_skills_normalized:
            evidence = get_evidence(skill['name'], github_skills)
            required_matches.append({
                'skill': skill,
                'evidence': evidence
            })
        else:
            required_missing.append(skill)

    # Match preferred skills (same logic)
    preferred_matches = match_preferred_skills(...)

    # Calculate scores
    required_score = (len(required_matches) / len(job_skills['required'])) * 100
    preferred_score = (len(preferred_matches) / len(job_skills['preferred'])) * 100
    overall_score = (0.7 * required_score) + (0.3 * preferred_score)

    # Generate recommendation
    recommendation = generate_recommendation(
        overall_score,
        required_score,
        len(required_missing)
    )

    return MatchResult(...)
```

**Consequences:**

**Positive:**
- Users understand exactly why they got a certain score
- Recommendations are actionable (specific skills to learn)
- Conservative approach protects users from wasted effort
- Evidence builds credibility
- Algorithm is tunable (we can adjust thresholds based on feedback)
- Transparent = trustworthy

**Negative:**
- Binary matching (has/doesn't have) misses proficiency levels
- No consideration of years of experience per skill
- Thresholds are somewhat arbitrary (based on research, not data)
- Doesn't account for transferable skills (e.g., Java → C# is easy)
- No consideration of job context (startup vs. enterprise, team size)

**Mitigation Strategies:**

1. **Proficiency Signals**: Use GitHub language percentages as proxy for proficiency. 45% Python suggests strong proficiency.

2. **Experience Proxy**: Years active on GitHub provides rough experience estimate.

3. **Threshold Tuning**: Monitor user feedback ("was this helpful?") and adjust thresholds if needed.

4. **Future ML Enhancement**: Collect feedback data, train ML model to improve recommendations over time.

5. **Contextual Notes**: Add disclaimer that recommendations are guidance, not guarantees.

**Alternatives Considered:**

1. **ML-Based Matching**: Train a model on successful hire data. Rejected due to:
   - No training data available
   - Black-box nature reduces trust
   - Overfitting risk with small datasets
   - Complexity not justified for MVP

2. **Simple Percentage**: Just count matched skills / total skills. Rejected because:
   - Doesn't differentiate required vs. preferred
   - All skills weighted equally (unrealistic)
   - No nuance in recommendations

3. **Years-of-Experience Matching**: Match "5+ years Python" requirements. Rejected because:
   - GitHub activity duration ≠ professional experience
   - Adds complexity
   - Job posts often inflate requirements

4. **Fuzzy Matching**: Accept similar skills (e.g., React ≈ Vue). Rejected because:
   - Similarity is subjective
   - Could give false confidence
   - Better to be conservative and accurate

**Validation Strategy:**

1. **Test with real-world scenarios**: Apply to 20 real job postings with diverse GitHub profiles
2. **Expert review**: Ask hiring managers "does this match make sense?"
3. **User feedback**: Collect ratings ("was this helpful?") to tune thresholds
4. **A/B testing**: Try different thresholds and measure application success rates (future)

**Review Triggers:**

Re-evaluate this decision when:
- User feedback indicates recommendations are consistently wrong
- We have enough data to train an ML model (1000+ labeled examples)
- Proficiency levels become important (user requests)
- Transferable skills cause significant mismatches

**Notes:**

This algorithm intentionally favors simplicity and transparency over sophistication. The goal is to provide helpful guidance, not perfect predictions. As we collect user feedback and usage data, we can refine the approach while maintaining the core principle: transparent, actionable recommendations based on verifiable evidence.
