# DevMatch

**GitHub Skills → Job Description Matcher**

Stop guessing if you're qualified. Paste a job URL + your GitHub username → Get instant match score, gap analysis, and actionable recommendations.

## The Problem

Job seekers waste countless hours applying to positions they're unqualified for, while missing opportunities where they're actually competitive. Traditional resume screening relies on keyword matching and self-reported skills, which are unreliable.

## The Solution

DevMatch analyzes your **actual code contributions** on GitHub and compares them against real job requirements using NLP and intelligent matching algorithms. You get:

- **Match Score (0-100%)**: How well you fit the role
- **Gap Analysis**: What specific skills you're missing
- **Actionable Recommendation**: Apply now, learn first, or redirect to better-fit roles
- **Evidence-Based Results**: See exactly which projects prove your skills

## Unique Value Proposition

Unlike resume matchers that rely on keywords, DevMatch proves technical competency through actual code analysis. Your GitHub repositories become your verified skill portfolio.

## Features

### Core Functionality
- ✅ **Direct Job Description Paste** (recommended, bypasses scraping)
- ✅ **Job URL Scraping** (Indeed, Google Jobs, LinkedIn support)
- ✅ **Deep GitHub Analysis** (languages, frameworks, tools)
- ✅ **NLP Skill Extraction** (100+ technical skills taxonomy)
- ✅ **Multi-Factor Matching** (weighted required/preferred skills)
- ✅ **Evidence-Based Results** (proof from actual code)
- ✅ **Actionable Recommendations** (APPLY_NOW/COMPETITIVE/SKILL_GAP)
- ✅ **Gap Analysis** (missing skills, learning time estimates)

### Technical Highlights
- 🏗️ **Stateless Architecture** (no database, easy scaling)
- 🧪 **Test-Driven Development** (80%+ test coverage)
- 📱 **Mobile-First Design** (responsive on all devices)
- ⚡ **Fast Response Times** (30-60 seconds typical)
- 🔒 **Secure** (HTTPS, input validation, no data retention)
- 📊 **Transparent Algorithm** (no black-box ML)
- 🎨 **Clean UI** (TailwindCSS, accessible design)

### Developer Experience
- 🐳 **Docker Support** (one-command local setup)
- 📚 **Comprehensive Docs** (architecture, API, deployment)
- 🏛️ **Architecture Decision Records** (ADRs for key decisions)
- 🔧 **Easy Local Development** (hot reload, detailed logs)
- 🚀 **Production-Ready** (Railway + Vercel deployment)

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional)

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

Visit `http://localhost:3000` to use the application.

### Run with Docker Compose (Recommended)

```bash
# Copy environment template
cp .env.example .env

# Optional: Add your GitHub token to .env for higher rate limits

# Start all services
docker-compose up

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Architecture

DevMatch uses a stateless, microservices-inspired architecture:

- **Frontend**: React SPA (mobile-first design)
- **Backend**: FastAPI with async request handling
- **Job Scraper**: Multi-platform scraper (Indeed, Google Jobs, direct paste)
- **NLP Engine**: spaCy for skill extraction
- **GitHub Analyzer**: Deep repository analysis via GitHub API
- **Matching Engine**: Multi-factor scoring algorithm

See [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) for detailed system design.

## API Documentation

See [docs/API.md](docs/API.md) for endpoint documentation.

## Technology Stack

**Backend:**
- FastAPI (web framework)
- spaCy (NLP)
- scikit-learn (matching algorithms)
- Playwright (web scraping)
- BeautifulSoup4 (HTML parsing)

**Frontend:**
- React 18
- TailwindCSS
- Axios

**Infrastructure:**
- Railway (backend hosting)
- Vercel (frontend hosting)
- Docker (containerization)

## Contributing

This is a portfolio project, but feedback and suggestions are welcome!

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Write tests first (TDD)
3. Implement feature
4. Ensure tests pass: `pytest` (backend), `npm test` (frontend)
5. Create PR with detailed description
6. Merge after review

### Commit Message Format

```
<type>: <concise description>

<detailed explanation in PR description>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`

## Testing

**Backend:**
```bash
cd backend
pytest --cov=app tests/
```

**Frontend:**
```bash
cd frontend
npm test
```

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for step-by-step deployment guide.

## License

MIT License - See LICENSE file for details

## Author

Built as a portfolio project demonstrating production-ready full-stack development, NLP engineering, and system architecture.

## Project Status

🚧 **In Active Development** - MVP functional, enhancements ongoing

## Demo

🔗 Live Demo: [Coming Soon]

## Screenshots

[Coming Soon]

---

**Built with clean architecture, comprehensive testing, and production-grade engineering practices.**
