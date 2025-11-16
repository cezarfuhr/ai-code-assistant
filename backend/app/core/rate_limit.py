"""
Rate limiting configuration using SlowAPI.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings


def get_limiter() -> Limiter:
    """
    Create and configure rate limiter.

    Returns:
        Configured Limiter instance
    """
    return Limiter(
        key_func=get_remote_address,
        enabled=settings.RATE_LIMIT_ENABLED,
        default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
        storage_uri=settings.REDIS_URL if settings.REDIS_ENABLED else "memory://",
    )


# Create limiter instance
limiter = get_limiter()
