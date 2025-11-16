"""
API endpoints for the AI Code Assistant.
"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.code import (
    CodeGenerationRequest,
    CodeExplanationRequest,
    BugDetectionRequest,
    RefactorRequest,
    DocumentationRequest,
    CodeResponse,
    HealthResponse,
)
from app.services.ai_service import ai_service
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status of the service
    """
    return HealthResponse(
        status="healthy", version=settings.VERSION, service=settings.PROJECT_NAME
    )


@router.post("/generate", response_model=CodeResponse)
async def generate_code(request: CodeGenerationRequest):
    """
    Generate code based on a natural language prompt.

    Args:
        request: Code generation request with prompt and language

    Returns:
        Generated code and explanation

    Raises:
        HTTPException: If code generation fails
    """
    try:
        result = await ai_service.generate_code(
            prompt=request.prompt, language=request.language, context=request.context
        )

        return CodeResponse(
            success=True,
            code=result["code"],
            explanation=result["explanation"],
            language=request.language,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code generation failed: {str(e)}",
        )


@router.post("/explain", response_model=CodeResponse)
async def explain_code(request: CodeExplanationRequest):
    """
    Explain what a piece of code does.

    Args:
        request: Code explanation request with code and language

    Returns:
        Detailed explanation of the code

    Raises:
        HTTPException: If explanation fails
    """
    try:
        explanation = await ai_service.explain_code(
            code=request.code, language=request.language
        )

        return CodeResponse(
            success=True,
            code=request.code,
            explanation=explanation,
            language=request.language,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code explanation failed: {str(e)}",
        )


@router.post("/detect-bugs", response_model=CodeResponse)
async def detect_bugs(request: BugDetectionRequest):
    """
    Detect potential bugs and issues in code.

    Args:
        request: Bug detection request with code and language

    Returns:
        List of detected bugs with severity and suggestions

    Raises:
        HTTPException: If bug detection fails
    """
    try:
        bugs = await ai_service.detect_bugs(
            code=request.code, language=request.language
        )

        return CodeResponse(
            success=True,
            code=request.code,
            bugs=bugs,
            explanation=f"Found {len(bugs)} potential issue(s)",
            language=request.language,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bug detection failed: {str(e)}",
        )


@router.post("/refactor", response_model=CodeResponse)
async def refactor_code(request: RefactorRequest):
    """
    Refactor code to improve quality and maintainability.

    Args:
        request: Refactor request with code, language, and optional instructions

    Returns:
        Refactored code and explanation of changes

    Raises:
        HTTPException: If refactoring fails
    """
    try:
        result = await ai_service.refactor_code(
            code=request.code,
            language=request.language,
            instructions=request.instructions,
        )

        return CodeResponse(
            success=True,
            code=result["code"],
            explanation=result["explanation"],
            language=request.language,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code refactoring failed: {str(e)}",
        )


@router.post("/document", response_model=CodeResponse)
async def generate_documentation(request: DocumentationRequest):
    """
    Generate comprehensive documentation for code.

    Args:
        request: Documentation request with code, language, and style

    Returns:
        Code with added documentation

    Raises:
        HTTPException: If documentation generation fails
    """
    try:
        documented_code = await ai_service.generate_documentation(
            code=request.code, language=request.language, style=request.style
        )

        return CodeResponse(
            success=True,
            code=documented_code,
            explanation=f"Documentation added using {request.style} style",
            language=request.language,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Documentation generation failed: {str(e)}",
        )
