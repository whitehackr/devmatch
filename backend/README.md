# DevMatch Backend

FastAPI backend for DevMatch - GitHub Skills to Job Description Matcher

## Setup

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Install Playwright browsers
playwright install chromium
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Optional: GitHub Personal Access Token for higher rate limits
GITHUB_TOKEN=your_token_here

# CORS allowed origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.vercel.app

# Environment
ENVIRONMENT=development
```

## Development

### Run Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: `http://localhost:8000`

API Documentation (Swagger): `http://localhost:8000/docs`

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_github_service.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py      # Request schemas
│   │   └── responses.py     # Response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── job_scraper.py   # Job scraping service
│   │   ├── skill_extractor.py # NLP skill extraction
│   │   ├── github_analyzer.py # GitHub analysis
│   │   └── matching_engine.py # Matching algorithm
│   └── utils/
│       ├── __init__.py
│       └── skill_taxonomy.py # Skill database
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_job_scraper.py
│   ├── test_skill_extractor.py
│   ├── test_github_analyzer.py
│   ├── test_matching_engine.py
│   └── test_api.py          # Integration tests
├── requirements.txt
└── README.md
```

## API Endpoints

See [../docs/API.md](../docs/API.md) for detailed API documentation.

- `GET /health` - Health check
- `POST /api/analyze` - Analyze job match

## Architecture

See [../docs/architecture/ARCHITECTURE.md](../docs/architecture/ARCHITECTURE.md) for system architecture.

## Testing Philosophy

- **Unit Tests**: Test each service in isolation with mocked dependencies
- **Integration Tests**: Test API endpoints with real service integration
- **Test Coverage**: Target 80%+ coverage
- **TDD**: Write tests before implementation

## Deployment

See [../docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md) for deployment instructions.

## License

MIT
