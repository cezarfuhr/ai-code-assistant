"""
Tests for Pydantic schemas.
"""
import pytest
from pydantic import ValidationError
from app.schemas.code import (
    CodeGenerationRequest,
    CodeExplanationRequest,
    BugDetectionRequest,
    RefactorRequest,
    DocumentationRequest,
    Bug,
    CodeResponse,
    HealthResponse,
)


class TestCodeGenerationRequest:
    """Tests for CodeGenerationRequest schema."""

    def test_valid_request(self):
        """Test valid code generation request."""
        request = CodeGenerationRequest(
            prompt="Create a function", language="python"
        )
        assert request.prompt == "Create a function"
        assert request.language == "python"
        assert request.context is None

    def test_with_context(self):
        """Test request with context."""
        request = CodeGenerationRequest(
            prompt="Create a function", language="python", context="Web application"
        )
        assert request.context == "Web application"

    def test_missing_prompt(self):
        """Test request with missing prompt raises error."""
        with pytest.raises(ValidationError):
            CodeGenerationRequest(language="python")

    def test_default_language(self):
        """Test default language is python."""
        request = CodeGenerationRequest(prompt="Test")
        assert request.language == "python"


class TestCodeExplanationRequest:
    """Tests for CodeExplanationRequest schema."""

    def test_valid_request(self):
        """Test valid explanation request."""
        request = CodeExplanationRequest(code="print('hello')", language="python")
        assert request.code == "print('hello')"
        assert request.language == "python"

    def test_missing_code(self):
        """Test missing code raises error."""
        with pytest.raises(ValidationError):
            CodeExplanationRequest(language="python")


class TestBugDetectionRequest:
    """Tests for BugDetectionRequest schema."""

    def test_valid_request(self):
        """Test valid bug detection request."""
        request = BugDetectionRequest(code="x = 1/0", language="python")
        assert request.code == "x = 1/0"
        assert request.language == "python"


class TestRefactorRequest:
    """Tests for RefactorRequest schema."""

    def test_valid_request_without_instructions(self):
        """Test valid refactor request without instructions."""
        request = RefactorRequest(code="def foo(): pass", language="python")
        assert request.code == "def foo(): pass"
        assert request.instructions is None

    def test_valid_request_with_instructions(self):
        """Test valid refactor request with instructions."""
        request = RefactorRequest(
            code="def foo(): pass",
            language="python",
            instructions="Add type hints",
        )
        assert request.instructions == "Add type hints"


class TestDocumentationRequest:
    """Tests for DocumentationRequest schema."""

    def test_valid_request(self):
        """Test valid documentation request."""
        request = DocumentationRequest(code="def foo(): pass", language="python")
        assert request.style == "google"  # default

    def test_custom_style(self):
        """Test documentation request with custom style."""
        request = DocumentationRequest(
            code="def foo(): pass", language="python", style="numpy"
        )
        assert request.style == "numpy"


class TestBug:
    """Tests for Bug schema."""

    def test_valid_bug(self):
        """Test valid bug creation."""
        bug = Bug(
            line=10,
            severity="high",
            description="Null pointer",
            suggestion="Add check",
        )
        assert bug.line == 10
        assert bug.severity == "high"

    def test_bug_without_line(self):
        """Test bug without line number."""
        bug = Bug(severity="low", description="Style issue", suggestion="Fix style")
        assert bug.line is None


class TestCodeResponse:
    """Tests for CodeResponse schema."""

    def test_success_response(self):
        """Test successful code response."""
        response = CodeResponse(
            success=True, code="print('hello')", language="python"
        )
        assert response.success is True
        assert response.code == "print('hello')"

    def test_response_with_bugs(self):
        """Test response with bugs."""
        bugs = [
            Bug(
                line=1, severity="high", description="Issue", suggestion="Fix"
            )
        ]
        response = CodeResponse(success=True, bugs=bugs, language="python")
        assert len(response.bugs) == 1

    def test_response_with_explanation(self):
        """Test response with explanation."""
        response = CodeResponse(
            success=True, explanation="Code explained", language="python"
        )
        assert response.explanation == "Code explained"


class TestHealthResponse:
    """Tests for HealthResponse schema."""

    def test_valid_health_response(self):
        """Test valid health response."""
        response = HealthResponse(
            status="healthy", version="1.0.0", service="AI Code Assistant"
        )
        assert response.status == "healthy"
        assert response.version == "1.0.0"
