"""
Schemas for code history and favorites.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class HistoryCreate(BaseModel):
    """Schema for creating history entry."""
    operation_type: str
    language: str
    input_code: Optional[str] = None
    prompt: Optional[str] = None
    output_code: Optional[str] = None
    explanation: Optional[str] = None
    model_used: Optional[str] = None


class HistoryResponse(BaseModel):
    """Schema for history response."""
    id: str
    operation_type: str
    language: str
    input_code: Optional[str]
    prompt: Optional[str]
    output_code: Optional[str]
    explanation: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class FavoriteCreate(BaseModel):
    """Schema for creating favorite."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    code: str = Field(..., min_length=1)
    language: str
    tags: Optional[str] = None


class FavoriteResponse(BaseModel):
    """Schema for favorite response."""
    id: str
    title: str
    description: Optional[str]
    code: str
    language: str
    tags: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UsageStats(BaseModel):
    """Schema for user usage statistics."""
    monthly_requests: int
    max_monthly_requests: int
    requests_remaining: int
    history_count: int
    favorites_count: int
