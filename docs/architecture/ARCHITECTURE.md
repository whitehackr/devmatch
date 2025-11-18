# DevMatch System Architecture

## Overview

DevMatch is a stateless web application that analyzes job-seeker fit by comparing job requirements against actual GitHub code contributions. The system uses NLP for skill extraction, GitHub API for profile analysis, and a multi-factor matching algorithm to generate actionable recommendations.

## Architecture Diagram

```
┌─────────────────┐
│  User Browser   │
│   (React SPA)   │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────────────────────────────┐
│         Frontend (Vercel)               │
│  - Input validation                     │
│  - Results visualization                │
│  - Mobile-first UI                      │
└────────┬────────────────────────────────┘
         │ REST API
         ▼
┌─────────────────────────────────────────┐
│       Backend (Railway)                 │
│       FastAPI Application               │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   API Layer                      │  │
│  │   POST /api/analyze              │  │
│  │   GET /health                    │  │
│  └──────────┬───────────────────────┘  │
│             │                           │
│  ┌──────────▼───────────────────────┐  │
│  │   Orchestration Service          │  │
│  │   - Input validation             │  │
│  │   - Service coordination         │  │
│  │   - Error handling               │  │
│  └──┬────┬────┬────┬────────────────┘  │
│     │    │    │    │                    │
│  ┌──▼─┐ ┌▼──┐ ┌▼─┐ ┌▼────────────┐    │
│  │Job │ │NLP│ │GH│ │  Matching   │    │
│  │Scr │ │Eng│ │Ana│ │   Engine    │    │
│  └──┬─┘ └┬──┘ └┬─┘ └─────────────┘    │
│     │    │     │                        │
└─────┼────┼─────┼────────────────────────┘
      │    │     │
   ┌──▼──┐ │  ┌──▼────────┐
   │ Web │ │  │  GitHub   │
   │Sites│ │  │    API    │
   └─────┘ │  └───────────┘
      ┌────▼─────┐
      │  spaCy   │
      │  Models  │
      └──────────┘
```

## System Components

### Frontend (React SPA)

**Responsibilities:**
- User input collection (job URL, GitHub username, or direct JD paste)
- API request orchestration
- Results visualization with charts and breakdowns
- Mobile-responsive UI
- Error handling and user feedback

**Technology:**
- React 18 (UI framework)
- TailwindCSS (styling)
- Axios (HTTP client)
- React Router (navigation)

**Key Design Decisions:**
- No state management library (Redux/MobX) - simple useState sufficient for MVP
- Mobile-first responsive design
- Progressive loading indicators for long-running operations
- Optimistic UI updates where possible

### Backend (FastAPI)

**Responsibilities:**
- HTTP API endpoints
- Request validation
- Service orchestration
- Error handling and logging
- CORS management

**Technology:**
- FastAPI (web framework)
- Pydantic (data validation)
- Uvicorn (ASGI server)

**Key Design Decisions:**
- Synchronous request processing (async workers in future)
- Single endpoint for analysis (simplifies API surface)
- Comprehensive error responses with user-friendly messages

### Job Scraper Service

**Responsibilities:**
- Extract job details from URLs (Indeed, Google Jobs, LinkedIn)
- Accept direct JD text paste (bypasses scraping)
- Parse HTML/JavaScript-rendered content
- Normalize job data structure

**Technology:**
- Playwright (JavaScript rendering)
- BeautifulSoup4 (HTML parsing)
- Custom platform detection logic

**Supported Platforms:**
1. **Indeed** - Server-rendered, simple HTTP
2. **Google Jobs** - Structured data, easy extraction
3. **Direct Paste** - User-provided text (most reliable)
4. **Generic Fallback** - Best-effort extraction

**Key Design Decisions:**
- Platform-specific scrapers for reliability
- Fallback to generic scraper for unknown sites
- Direct paste option for scraping-resistant sites
- Timeout: 30 seconds max per scrape

### NLP Skill Extraction Service

**Responsibilities:**
- Parse job description text
- Extract technical skills (languages, frameworks, tools)
- Classify skills as required vs preferred
- Assign importance scores (1-5)

**Technology:**
- spaCy (en_core_web_sm model)
- Custom skill taxonomy (500+ tech terms)
- Pattern matching + NER

**Algorithm:**
1. Text preprocessing (lowercase, clean whitespace)
2. Section detection ("Requirements" vs "Nice-to-Have")
3. Named entity recognition (ORG, PRODUCT entities)
4. Direct pattern matching against skill taxonomy
5. Importance scoring based on frequency and context
6. Categorization (required vs preferred)

**Skill Taxonomy:**
- Languages: Python, JavaScript, Java, Go, etc.
- Frameworks: React, Django, Spring, etc.
- Databases: PostgreSQL, MongoDB, Redis, etc.
- Cloud: AWS, Azure, GCP, Docker, Kubernetes
- Tools: Git, CI/CD, Linux, etc.

**Key Design Decisions:**
- Deterministic extraction (no ML black box for MVP)
- Importance scoring based on frequency + context
- Required skills = in requirements section OR importance ≥4
- spaCy model loaded once at startup (performance)

### GitHub Analysis Service

**Responsibilities:**
- Fetch user's public repositories
- Analyze language usage across repos
- Detect frameworks from dependencies and code patterns
- Extract tools from repo configuration files
- Calculate years of experience

**Technology:**
- GitHub REST API
- Regex pattern matching
- Dependency file parsing (package.json, requirements.txt, etc.)

**Analysis Pipeline:**
1. Fetch user profile metadata
2. List all public repositories (up to 100, sorted by recent activity)
3. For each repo:
   - Get language statistics
   - Fetch README.md (framework mentions)
   - Parse package manager files
   - Detect configuration files (Docker, CI/CD)
4. Aggregate results:
   - Language percentages
   - Framework list with project counts
   - Tools detected

**Key Design Decisions:**
- Limit to 100 most recent repos (performance vs coverage)
- Exclude forks unless actively maintained
- Prioritize language statistics (most reliable signal)
- Framework detection via multiple signals (code + dependencies)
- Rate limit: 60 req/hour (public), 5000 with PAT

### Matching Engine

**Responsibilities:**
- Compare required skills vs GitHub skills
- Calculate match scores
- Identify skill gaps
- Generate recommendations

**Algorithm:**

```python
# Score Calculation
required_match_score = (matched_required / total_required) * 100
preferred_match_score = (matched_preferred / total_preferred) * 100
overall_score = (0.7 * required_match_score) + (0.3 * preferred_match_score)

# Recommendation Logic
if overall_score >= 80 and required_match_score >= 85:
    recommendation = "APPLY_NOW"
elif overall_score >= 65 and required_match_score >= 70:
    recommendation = "COMPETITIVE"
elif overall_score >= 50:
    if critical_missing_count <= 2:
        recommendation = "COMPETITIVE"
    else:
        recommendation = "SKILL_GAP"
else:
    recommendation = "SKILL_GAP"
```

**Key Design Decisions:**
- Required skills weighted 70% (deal-breakers)
- Preferred skills weighted 30% (nice-to-have)
- Thresholds based on job market research
- Transparent scoring (no black-box ML)
- Evidence collection for credibility

## Data Flow

1. **User Input** → Frontend validates and sends to backend
2. **Backend Receives** → Validates request schema
3. **Job Analysis** → Scraper fetches JD, NLP extracts skills
4. **GitHub Analysis** → API fetches repos, analyzes code
5. **Matching** → Engine compares skills, calculates score
6. **Response** → Backend returns structured result
7. **Display** → Frontend renders results with visualizations

**Total Processing Time:** 30-60 seconds
- Job scraping: 10-20s
- Skill extraction: 3-5s
- GitHub analysis: 15-25s
- Matching: <1s
- Network overhead: 5-10s

## Data Models

### JobInput
```python
{
    "job_url": "https://...",  # Optional if job_description provided
    "job_description": "...",  # Optional if job_url provided
    "github_username": "octocat"
}
```

### JobDescription
```python
{
    "title": "Senior Python Engineer",
    "company": "TechCorp",
    "raw_text": "...",
    "required_skills": [
        {"name": "Python", "importance": 5, "category": "language"},
        {"name": "Django", "importance": 4, "category": "framework"}
    ],
    "preferred_skills": [...]
}
```

### GitHubProfile
```python
{
    "username": "octocat",
    "repos_analyzed": 45,
    "years_active": 8,
    "languages": {
        "Python": 45.2,
        "JavaScript": 30.1,
        "Go": 15.7
    },
    "frameworks": ["Django", "React", "FastAPI"],
    "tools": ["Docker", "GitHub Actions", "PostgreSQL"]
}
```

### MatchResult
```python
{
    "overall_score": 85,
    "required_score": 90,
    "preferred_score": 75,
    "recommendation": "APPLY_NOW",
    "matched_skills": [
        {"skill": "Python", "evidence": "45.2% of code", "importance": 5}
    ],
    "missing_skills": [
        {"skill": "Kubernetes", "importance": 4}
    ],
    "job_description": {...},
    "github_profile": {...}
}
```

## Deployment Architecture

### Frontend (Vercel)
- Static site hosting on Vercel Edge Network
- Global CDN for low latency
- Automatic HTTPS
- Environment variables for API URL

### Backend (Railway)
- Containerized Python application
- Auto-scaling (future)
- Health check endpoint: `/health`
- Environment variables for configuration

### Infrastructure Diagram

```
                    ┌──────────────┐
                    │   Cloudflare │
                    │      DNS     │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │    Vercel    │
                    │   CDN/Edge   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
User ──HTTPS───────▶│   Frontend   │
                    │    (React)   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Railway    │
                    │   (Backend)  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
          ┌───▼──┐    ┌────▼────┐  ┌───▼────┐
          │ Web  │    │ GitHub  │  │ spaCy  │
          │Sites │    │   API   │  │ Models │
          └──────┘    └─────────┘  └────────┘
```

## Scalability Considerations

### Current Limitations (MVP)
- Single backend instance
- Synchronous processing
- No caching
- Rate limited by GitHub API (60 req/hour)

### Future Improvements
- Horizontal scaling (multiple backend instances)
- Job queue for async processing (Celery + Redis)
- Caching layer (Redis) for GitHub profiles and job descriptions
- GitHub OAuth for higher rate limits (5000 req/hour)
- Database for user history and analytics

## Security Considerations

- **Input Validation**: All inputs validated via Pydantic schemas
- **Rate Limiting**: TODO - implement rate limiting per IP
- **CORS**: Restricted to frontend domain only
- **No Sensitive Data**: No user credentials stored
- **GitHub API**: Read-only access, public repos only
- **Web Scraping**: Respects robots.txt (best effort)

## Error Handling

- **Invalid Input**: 400 Bad Request with clear message
- **GitHub User Not Found**: 404 with suggestion to check username
- **Scraping Failure**: Partial results or fallback to direct paste
- **Timeout**: Retry once, then graceful degradation
- **API Errors**: Logged for debugging, user sees friendly message

## Monitoring & Observability

**Current (MVP):**
- Health check endpoint
- Basic logging to stdout
- Railway/Vercel dashboards

**Future:**
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Analytics (user behavior, match accuracy)
- Alerting (error rates, downtime)

## Testing Strategy

- **Unit Tests**: Each service isolated, mocked dependencies, 80% coverage
- **Integration Tests**: Service combinations, controlled inputs
- **E2E Tests**: Full user flow, real GitHub profiles
- **Performance Tests**: Response time <60s under load

## Technology Choices & Rationale

| Technology | Rationale |
|------------|-----------|
| **FastAPI** | Modern, fast, automatic API docs, type safety |
| **React** | Component-based, large ecosystem, familiar |
| **spaCy** | Production-ready NLP, pre-trained models |
| **Playwright** | Handles JavaScript rendering, reliable |
| **Railway** | Easy deployment, containerization, free tier |
| **Vercel** | Best-in-class frontend hosting, zero config |
| **No Database** | Reduces complexity, enables stateless scaling |

## Architecture Decision Records

See `docs/architecture/decisions/` for detailed ADRs:

- [ADR-001: Stateless Architecture](decisions/ADR-001-stateless-architecture.md)
- [ADR-002: Web Scraping Strategy](decisions/ADR-002-web-scraping-strategy.md)
- [ADR-003: Matching Algorithm Design](decisions/ADR-003-matching-algorithm.md)
- [ADR-004: GitHub as Sole Skill Source](decisions/ADR-004-github-sole-source.md)

## Future Enhancements

1. **User Accounts**: Save history, track applications
2. **Resume Analysis**: Cross-reference resume with GitHub
3. **Learning Paths**: Personalized skill development plans
4. **Job Alerts**: Notify when new matching jobs posted
5. **LinkedIn Integration**: Analyze LinkedIn profile too
6. **Interview Prep**: Generate questions based on skill gaps
7. **Team Features**: Recruiters analyze candidates

---

**This architecture balances simplicity (stateless, no DB) with functionality (comprehensive analysis) to deliver an MVP that demonstrates production-ready engineering while remaining maintainable.**
