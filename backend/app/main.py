"""
DevMatch API - Main Application

FastAPI application for analyzing GitHub profile fit to job descriptions.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import settings

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Analyze GitHub skills vs job requirements",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.

    This is where we could:
    - Load spaCy models
    - Initialize connections
    - Warm up caches
    """
    print(f"Starting {settings.app_name} v{settings.version}")
    print(f"Environment: {settings.environment}")

    # Pre-load spaCy model for faster first request
    # This is optional but recommended for production
    # try:
    #     import spacy
    #     spacy.load("en_core_web_sm")
    #     print("spaCy model loaded successfully")
    # except Exception as e:
    #     print(f"Warning: Could not pre-load spaCy model: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print(f"Shutting down {settings.app_name}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
