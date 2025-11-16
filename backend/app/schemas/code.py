"""
Pydantic schemas for code-related requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class CodeGenerationRequest(BaseModel):
    """Request schema for code generation."""

    prompt: str = Field(..., description="Description of the code to generate")
    language: str = Field(default="python", description="Programming language")
    context: Optional[str] = Field(None, description="Additional context")


class CodeExplanationRequest(BaseModel):
    """Request schema for code explanation."""

    code: str = Field(..., description="Code to explain")
    language: str = Field(default="python", description="Programming language")


class BugDetectionRequest(BaseModel):
    """Request schema for bug detection."""

    code: str = Field(..., description="Code to analyze for bugs")
    language: str = Field(default="python", description="Programming language")


class RefactorRequest(BaseModel):
    """Request schema for code refactoring."""

    code: str = Field(..., description="Code to refactor")
    language: str = Field(default="python", description="Programming language")
    instructions: Optional[str] = Field(None, description="Specific refactoring instructions")


class DocumentationRequest(BaseModel):
    """Request schema for documentation generation."""

    code: str = Field(..., description="Code to document")
    language: str = Field(default="python", description="Programming language")
    style: str = Field(default="google", description="Documentation style (google, numpy, sphinx)")


class Bug(BaseModel):
    """Bug information."""

    line: Optional[int] = Field(None, description="Line number where bug was found")
    severity: str = Field(..., description="Bug severity (low, medium, high, critical)")
    description: str = Field(..., description="Description of the bug")
    suggestion: str = Field(..., description="Suggestion to fix the bug")


class CodeResponse(BaseModel):
    """Response schema for code operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    code: Optional[str] = Field(None, description="Generated or modified code")
    explanation: Optional[str] = Field(None, description="Explanation of the code or operation")
    bugs: Optional[List[Bug]] = Field(None, description="List of detected bugs")
    language: str = Field(..., description="Programming language")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    service: str
