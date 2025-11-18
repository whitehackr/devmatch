# DevMatch API Documentation

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://devmatch-api.railway.app` (or your Railway domain)

## Authentication

No authentication required for MVP. All endpoints are public.

## Rate Limiting

**Current**: No rate limiting implemented
**Future**: 10 requests per minute per IP address

## Endpoints

### Health Check

Check if the API is running and healthy.

**Endpoint**: `GET /health`

**Response**: `200 OK`

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

**Example**:
```bash
curl http://localhost:8000/health
```

---

### Analyze Job Match

Analyze how well a GitHub profile matches a job description.

**Endpoint**: `POST /api/analyze`

**Content-Type**: `application/json`

**Request Body**:

```json
{
  "job_url": "https://www.indeed.com/viewjob?jk=abc123",
  "github_username": "octocat"
}
```

**OR** (Direct JD Paste - Recommended):

```json
{
  "job_description": "We are seeking a Senior Python Engineer...",
  "github_username": "octocat"
}
```

**Request Schema**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_url` | string (URL) | Conditional* | URL of job posting (Indeed, Google Jobs, LinkedIn, or generic) |
| `job_description` | string | Conditional* | Direct paste of job description text |
| `github_username` | string | Yes | GitHub username to analyze |

*Either `job_url` OR `job_description` must be provided, not both.

**Response**: `200 OK`

```json
{
  "overall_score": 85,
  "required_score": 90,
  "preferred_score": 75,
  "recommendation": "APPLY_NOW",
  "recommendation_text": "Strong match! Apply with confidence.",
  "job_description": {
    "title": "Senior Python Engineer",
    "company": "TechCorp",
    "source": "indeed",
    "required_skills": [
      {
        "name": "Python",
        "category": "language",
        "importance": 5
      },
      {
        "name": "Django",
        "category": "framework",
        "importance": 4
      }
    ],
    "preferred_skills": [
      {
        "name": "AWS",
        "category": "cloud",
        "importance": 3
      }
    ]
  },
  "github_profile": {
    "username": "octocat",
    "account_age_years": 8,
    "repos_analyzed": 45,
    "total_repos": 120,
    "languages": {
      "Python": 45.2,
      "JavaScript": 30.1,
      "Go": 15.7,
      "Shell": 9.0
    },
    "frameworks": [
      "Django",
      "Flask",
      "React",
      "FastAPI"
    ],
    "tools": [
      "Docker",
      "GitHub Actions",
      "PostgreSQL"
    ]
  },
  "matched_skills": [
    {
      "skill": "Python",
      "category": "language",
      "importance": 5,
      "evidence": "45.2% of code"
    },
    {
      "skill": "Django",
      "category": "framework",
      "importance": 4,
      "evidence": "Used in 8 projects"
    }
  ],
  "missing_skills": [
    {
      "skill": "Kubernetes",
      "category": "tool",
      "importance": 4
    }
  ],
  "gap_analysis": {
    "critical_missing": 1,
    "total_missing": 3,
    "learning_estimate_weeks": 4
  }
}
```

**Response Schema**:

| Field | Type | Description |
|-------|------|-------------|
| `overall_score` | integer (0-100) | Weighted average of required and preferred match scores |
| `required_score` | integer (0-100) | Percentage of required skills matched |
| `preferred_score` | integer (0-100) | Percentage of preferred skills matched |
| `recommendation` | enum | One of: `APPLY_NOW`, `COMPETITIVE`, `SKILL_GAP` |
| `recommendation_text` | string | Human-readable recommendation |
| `job_description` | object | Parsed job description details |
| `github_profile` | object | Analyzed GitHub profile data |
| `matched_skills` | array | Skills the candidate has with evidence |
| `missing_skills` | array | Skills the candidate lacks |
| `gap_analysis` | object | Summary of skill gaps |

**Recommendation Types**:

| Recommendation | Criteria | Meaning |
|----------------|----------|---------|
| `APPLY_NOW` | Overall ≥80% AND Required ≥85% | Strong match, apply immediately |
| `COMPETITIVE` | Overall ≥65% AND Required ≥70% | Good match, competitive candidate |
| `SKILL_GAP` | Below competitive threshold | Significant gaps, learn first |

**Error Responses**:

#### 400 Bad Request

Invalid input (missing fields, malformed URL, etc.)

```json
{
  "error": "validation_error",
  "message": "Either job_url or job_description must be provided",
  "details": {
    "field": "job_url",
    "issue": "missing"
  }
}
```

#### 404 Not Found

GitHub user doesn't exist

```json
{
  "error": "github_user_not_found",
  "message": "GitHub user 'nonexistentuser' not found",
  "suggestion": "Please verify the username and try again"
}
```

#### 422 Unprocessable Entity

Scraping failed or job description parsing failed

```json
{
  "error": "scraping_failed",
  "message": "Failed to extract job description from URL",
  "suggestion": "Try pasting the job description directly instead",
  "url": "https://..."
}
```

#### 500 Internal Server Error

Unexpected error during processing

```json
{
  "error": "internal_error",
  "message": "An unexpected error occurred",
  "request_id": "req_abc123"
}
```

#### 504 Gateway Timeout

Request took longer than 60 seconds

```json
{
  "error": "timeout",
  "message": "Analysis took too long to complete",
  "suggestion": "Try again with a simpler job description or fewer GitHub repositories"
}
```

**Example Requests**:

**Using cURL (Job URL)**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://www.indeed.com/viewjob?jk=abc123",
    "github_username": "torvalds"
  }'
```

**Using cURL (Direct Paste)**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "We are looking for a Senior Backend Engineer with 5+ years of Python experience. Must have Django, PostgreSQL, and AWS knowledge.",
    "github_username": "gvanrossum"
  }'
```

**Using JavaScript (Fetch API)**:
```javascript
const response = await fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    job_description: "Senior Python Engineer...",
    github_username: "octocat"
  })
});

const result = await response.json();
console.log(`Match Score: ${result.overall_score}%`);
console.log(`Recommendation: ${result.recommendation}`);
```

**Using Python (Requests)**:
```python
import requests

response = requests.post(
    'http://localhost:8000/api/analyze',
    json={
        'job_description': 'Senior Python Engineer...',
        'github_username': 'octocat'
    }
)

result = response.json()
print(f"Match Score: {result['overall_score']}%")
print(f"Recommendation: {result['recommendation']}")
```

---

## Data Models

### Skill

```json
{
  "name": "Python",
  "category": "language",
  "importance": 5
}
```

**Fields**:
- `name` (string): Canonical skill name
- `category` (enum): One of `language`, `framework`, `database`, `cloud`, `tool`, `concept`
- `importance` (integer 1-5): Importance score (5 = critical, 1 = nice-to-have)

### Matched Skill

```json
{
  "skill": "Python",
  "category": "language",
  "importance": 5,
  "evidence": "45.2% of code"
}
```

**Fields**:
- Inherits from `Skill`
- `evidence` (string): Proof of skill from GitHub

### GitHub Profile

```json
{
  "username": "octocat",
  "account_age_years": 8,
  "repos_analyzed": 45,
  "total_repos": 120,
  "languages": { "Python": 45.2 },
  "frameworks": ["Django"],
  "tools": ["Docker"]
}
```

**Fields**:
- `username` (string): GitHub username
- `account_age_years` (float): Years since account creation
- `repos_analyzed` (integer): Number of repos analyzed (max 100)
- `total_repos` (integer): Total public repos
- `languages` (object): Language → percentage mapping
- `frameworks` (array): Detected frameworks
- `tools` (array): Detected tools

---

## CORS Configuration

**Allowed Origins**:
- Development: `http://localhost:3000`
- Production: Your Vercel domain

**Allowed Methods**: `GET`, `POST`, `OPTIONS`

**Allowed Headers**: `Content-Type`, `Authorization`

---

## Performance

**Typical Response Times**:
- Job scraping: 10-20 seconds
- Skill extraction: 3-5 seconds
- GitHub analysis: 15-25 seconds
- Matching: <1 second
- **Total**: 30-50 seconds

**Timeout**: 60 seconds (hard limit)

---

## Rate Limits (Future)

| Tier | Requests per Minute | Requests per Day |
|------|---------------------|------------------|
| Free | 10 | 100 |
| Authenticated (GitHub PAT) | 60 | 5000 |

---

## Versioning

Current version: `v1`

API versioning will be introduced when breaking changes are necessary. Version is specified in URL path: `/api/v1/analyze`

---

## Support

For issues or questions:
- GitHub Issues: [your-repo/issues]
- Documentation: [docs link]

---

## Changelog

### v1.0.0 (2025-11-18)
- Initial release
- POST `/api/analyze` endpoint
- Support for Indeed, Google Jobs, direct paste
- GitHub profile analysis
- Multi-factor matching algorithm
