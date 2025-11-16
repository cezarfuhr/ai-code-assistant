"""
Code history database model.
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class OperationType(str, enum.Enum):
    """Types of code operations."""
    GENERATE = "generate"
    EXPLAIN = "explain"
    DETECT_BUGS = "detect_bugs"
    REFACTOR = "refactor"
    DOCUMENT = "document"


class CodeHistory(Base):
    """Code history model for tracking user's code operations."""

    __tablename__ = "code_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Operation details
    operation_type = Column(SQLEnum(OperationType), nullable=False)
    language = Column(String, nullable=False)

    # Input/Output
    input_code = Column(Text, nullable=True)
    prompt = Column(Text, nullable=True)
    output_code = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)

    # Metadata
    model_used = Column(String, nullable=True)
    cache_hit = Column(String, default=False)
    processing_time_ms = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="code_history")

    def __repr__(self):
        return f"<CodeHistory {self.operation_type} - {self.language}>"
