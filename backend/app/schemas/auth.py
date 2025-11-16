"""
Pydantic schemas for authentication.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    full_name: Optional[str] = Field(None, description="User full name")


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    """Schema for decoded token data."""

    email: Optional[str] = None
    user_id: Optional[str] = None


class User(BaseModel):
    """Schema for user information."""

    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    full_name: Optional[str] = Field(None, description="User full name")
    is_active: bool = Field(default=True, description="Whether user is active")
    created_at: Optional[str] = Field(None, description="Account creation timestamp")


class CacheStats(BaseModel):
    """Schema for cache statistics."""

    enabled: bool = Field(..., description="Whether cache is enabled")
    keys: Optional[int] = Field(None, description="Number of cached keys")
    memory_used: Optional[str] = Field(None, description="Memory used by cache")
    connected_clients: Optional[int] = Field(None, description="Connected Redis clients")
    uptime_days: Optional[int] = Field(None, description="Redis uptime in days")
    error: Optional[str] = Field(None, description="Error message if any")
