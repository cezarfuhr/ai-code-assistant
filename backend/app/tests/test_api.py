"""
Tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.schemas.code import Bug

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self):
        """Test health check returns correct status."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "service" in data


class TestCodeGeneration:
    """Tests for code generation endpoint."""

    @patch("app.api.endpoints.ai_service.generate_code")
    @pytest.mark.asyncio
    async def test_generate_code_success(self, mock_generate):
        """Test successful code generation."""
        mock_generate.return_value = {
            "code": "def hello():\n    print('Hello, World!')",
            "explanation": "Generated a simple hello function",
        }

        response = client.post(
            "/api/v1/generate",
            json={"prompt": "Create a hello world function", "language": "python"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "code" in data
        assert data["language"] == "python"

    def test_generate_code_missing_prompt(self):
        """Test code generation with missing prompt."""
        response = client.post("/api/v1/generate", json={"language": "python"})
        assert response.status_code == 422  # Validation error


class TestCodeExplanation:
    """Tests for code explanation endpoint."""

    @patch("app.api.endpoints.ai_service.explain_code")
    @pytest.mark.asyncio
    async def test_explain_code_success(self, mock_explain):
        """Test successful code explanation."""
        mock_explain.return_value = (
            "This function prints 'Hello, World!' to the console."
        )

        response = client.post(
            "/api/v1/explain",
            json={
                "code": "def hello():\n    print('Hello, World!')",
                "language": "python",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "explanation" in data

    def test_explain_code_missing_code(self):
        """Test code explanation with missing code."""
        response = client.post("/api/v1/explain", json={"language": "python"})
        assert response.status_code == 422


class TestBugDetection:
    """Tests for bug detection endpoint."""

    @patch("app.api.endpoints.ai_service.detect_bugs")
    @pytest.mark.asyncio
    async def test_detect_bugs_success(self, mock_detect):
        """Test successful bug detection."""
        mock_detect.return_value = [
            Bug(
                line=1,
                severity="high",
                description="Potential null pointer",
                suggestion="Add null check",
            )
        ]

        response = client.post(
            "/api/v1/detect-bugs",
            json={"code": "x = null.value", "language": "javascript"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "bugs" in data
        assert len(data["bugs"]) > 0

    @patch("app.api.endpoints.ai_service.detect_bugs")
    @pytest.mark.asyncio
    async def test_detect_bugs_none_found(self, mock_detect):
        """Test bug detection when no bugs found."""
        mock_detect.return_value = []

        response = client.post(
            "/api/v1/detect-bugs",
            json={"code": "print('clean code')", "language": "python"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["bugs"] == []


class TestCodeRefactoring:
    """Tests for code refactoring endpoint."""

    @patch("app.api.endpoints.ai_service.refactor_code")
    @pytest.mark.asyncio
    async def test_refactor_code_success(self, mock_refactor):
        """Test successful code refactoring."""
        mock_refactor.return_value = {
            "code": "def calculate_total(items):\n    return sum(items)",
            "explanation": "Refactored to use built-in sum function",
        }

        response = client.post(
            "/api/v1/refactor",
            json={
                "code": "def calculate_total(items):\n    total = 0\n    for item in items:\n        total += item\n    return total",
                "language": "python",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "code" in data
        assert "explanation" in data

    @patch("app.api.endpoints.ai_service.refactor_code")
    @pytest.mark.asyncio
    async def test_refactor_code_with_instructions(self, mock_refactor):
        """Test refactoring with specific instructions."""
        mock_refactor.return_value = {
            "code": "refactored code",
            "explanation": "Applied instructions",
        }

        response = client.post(
            "/api/v1/refactor",
            json={
                "code": "some code",
                "language": "python",
                "instructions": "Use list comprehension",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestDocumentation:
    """Tests for documentation generation endpoint."""

    @patch("app.api.endpoints.ai_service.generate_documentation")
    @pytest.mark.asyncio
    async def test_generate_documentation_success(self, mock_doc):
        """Test successful documentation generation."""
        mock_doc.return_value = '"""Documented function."""\ndef hello():\n    pass'

        response = client.post(
            "/api/v1/document",
            json={"code": "def hello():\n    pass", "language": "python"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "code" in data

    @patch("app.api.endpoints.ai_service.generate_documentation")
    @pytest.mark.asyncio
    async def test_generate_documentation_with_style(self, mock_doc):
        """Test documentation with specific style."""
        mock_doc.return_value = "documented code"

        response = client.post(
            "/api/v1/document",
            json={
                "code": "def hello():\n    pass",
                "language": "python",
                "style": "numpy",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root(self):
        """Test root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "docs" in data
