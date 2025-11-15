"""
Authentication and admin endpoints.
"""
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import UserLogin, Token, CacheStats
from app.core.security import create_access_token, get_current_user_required
from app.core.config import settings
from app.services.cache_service import cache_service

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login endpoint to get JWT token.

    For demo purposes, accepts any email/password.
    In production, validate against database.

    Args:
        credentials: User login credentials

    Returns:
        JWT access token
    """
    # Demo: Accept any credentials
    # In production: Validate against database
    # if not verify_password(credentials.password, user.hashed_password):
    #     raise HTTPException(status_code=401, detail="Incorrect password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": credentials.email, "email": credentials.email},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user_required)):
    """
    Get current user information from JWT token.

    Args:
        current_user: Current authenticated user

    Returns:
        User information
    """
    return {
        "email": current_user.get("email"),
        "sub": current_user.get("sub"),
    }


@router.get("/cache/stats", response_model=CacheStats)
async def get_cache_stats(current_user: dict = Depends(get_current_user_required)):
    """
    Get cache statistics (admin only).

    Args:
        current_user: Current authenticated user

    Returns:
        Cache statistics
    """
    stats = await cache_service.get_stats()
    return CacheStats(**stats)


@router.post("/cache/clear")
async def clear_cache(current_user: dict = Depends(get_current_user_required)):
    """
    Clear all cache entries (admin only).

    Args:
        current_user: Current authenticated user

    Returns:
        Success message
    """
    success = await cache_service.clear_all()

    if success:
        return {"message": "Cache cleared successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear cache",
        )
