"""
Main FastAPI application for AI Code Assistant.
"""
import uuid
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.database import init_db, close_db
from app.core.rate_limit import limiter
from app.api.endpoints import router as api_router
from app.api.auth import router as auth_router
from app.services.cache_service import cache_service
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url=f"{settings.API_V1_STR}/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Middleware for request tracking
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with request ID and timing."""
    request_id = str(uuid.uuid4())

    # Bind request ID to logger context
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        path=request.url.path,
        method=request.method,
    )

    start_time = time.time()

    logger.info(
        "Request started",
        client=request.client.host if request.client else "unknown",
    )

    try:
        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            "Request completed",
            status_code=response.status_code,
            duration_ms=round(process_time * 1000, 2),
        )

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))

        return response

    except Exception as e:
        process_time = time.time() - start_time

        logger.error(
            "Request failed",
            error=str(e),
            duration_ms=round(process_time * 1000, 2),
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "request_id": request_id},
            headers={"X-Request-ID": request_id},
        )


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info(
        "Starting AI Code Assistant",
        version=settings.VERSION,
        redis_enabled=settings.REDIS_ENABLED,
        database_enabled=True,
    )

    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))

    # Connect to Redis cache
    await cache_service.connect()

    logger.info("Application startup complete")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down AI Code Assistant")

    # Close database connections
    await close_db()

    # Disconnect from Redis
    await cache_service.disconnect()

    logger.info("Application shutdown complete")


# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR, tags=["code"])
app.include_router(auth_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
