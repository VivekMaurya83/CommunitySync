"""
Production Health Check Endpoints
Add these to verify deployment health in Render
"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from backend.database import engine

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    Used by Render to verify service is running
    """
    return {
        "status": "healthy",
        "service": "CommunitySync API",
        "version": "1.0.0"
    }

@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check - verifies database connectivity
    Used by Render before routing traffic
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

# Add to main.py:
# from backend.routes.health import router as health_router
# app.include_router(health_router, prefix="/api/health")
