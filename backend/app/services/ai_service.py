"""
AI Service for code operations using OpenAI and LangChain with caching.
"""
from typing import List, Dict, Any
import openai
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.code import Bug
from app.services.cache_service import cache_service
import json
import re

logger = get_logger(__name__)


class AIService:
    """Service for AI-powered code operations with caching."""

    def __init__(self):
        """Initialize AI service with OpenAI configuration."""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        openai.api_key = settings.OPENAI_API_KEY
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            openai_api_key=settings.OPENAI_API_KEY,
        )
        logger.info("AI Service initialized", model=settings.OPENAI_MODEL)

    async def generate_code(
        self, prompt: str, language: str, context: str = None
    ) -> Dict[str, Any]:
        """
        Generate code based on a prompt.

        Args:
            prompt: Description of the code to generate
            language: Programming language
            context: Additional context

        Returns:
            Dictionary with generated code and explanation
        """
        # Try to get from cache
        cache_key_params = {
            "prompt": prompt,
            "language": language,
            "context": context or "",
        }
        cached = await cache_service.get("generate", **cache_key_params)

        if cached:
            logger.info(
                "Cache hit for code generation",
                language=language,
                prompt_length=len(prompt),
            )
            return cached

        logger.info(
            "Generating code",
            language=language,
            prompt_length=len(prompt),
            has_context=context is not None,
        )

        template = """You are an expert {language} programmer. Generate clean, efficient, and well-documented code.

Task: {prompt}

{context_section}

Provide the code with inline comments explaining key parts.

Code:"""

        context_section = f"Context: {context}" if context else ""

        prompt_template = PromptTemplate(
            input_variables=["language", "prompt", "context_section"],
            template=template,
        )

        chain = LLMChain(llm=self.llm, prompt=prompt_template)

        result = await chain.ainvoke(
            {
                "language": language,
                "prompt": prompt,
                "context_section": context_section,
            }
        )

        code = result["text"].strip()

        response = {
            "code": code,
            "explanation": f"Generated {language} code based on the prompt: {prompt}",
        }

        # Cache the result
        await cache_service.set("generate", response, **cache_key_params)

        logger.info(
            "Code generated successfully",
            language=language,
            code_length=len(code),
        )

        return response

    async def explain_code(self, code: str, language: str) -> str:
        """
        Explain what a piece of code does.

        Args:
            code: Code to explain
            language: Programming language

        Returns:
            Detailed explanation of the code
        """
        # Try to get from cache
        cache_key_params = {"code": code, "language": language}
        cached = await cache_service.get("explain", **cache_key_params)

        if cached:
            logger.info("Cache hit for code explanation", language=language)
            return cached.get("explanation", "")

        logger.info("Explaining code", language=language, code_length=len(code))

        template = """You are an expert {language} programmer. Explain the following code in detail.

Code:
```{language}
{code}
```

Provide a clear, structured explanation that covers:
1. Overall purpose
2. Key components and their functions
3. Flow of execution
4. Important details or edge cases

Explanation:"""

        prompt_template = PromptTemplate(
            input_variables=["language", "code"], template=template
        )

        chain = LLMChain(llm=self.llm, prompt=prompt_template)

        result = await chain.ainvoke({"language": language, "code": code})

        explanation = result["text"].strip()

        # Cache the result
        await cache_service.set(
            "explain", {"explanation": explanation}, **cache_key_params
        )

        logger.info("Code explained successfully", explanation_length=len(explanation))

        return explanation

    async def detect_bugs(self, code: str, language: str) -> List[Bug]:
        """
        Detect potential bugs in code.

        Args:
            code: Code to analyze
            language: Programming language

        Returns:
            List of detected bugs
        """
        # Try to get from cache
        cache_key_params = {"code": code, "language": language}
        cached = await cache_service.get("detect_bugs", **cache_key_params)

        if cached:
            logger.info("Cache hit for bug detection", language=language)
            return [Bug(**bug) for bug in cached.get("bugs", [])]

        logger.info("Detecting bugs", language=language, code_length=len(code))

        template = """You are an expert {language} code reviewer. Analyze the following code for bugs, vulnerabilities, and issues.

Code:
```{language}
{code}
```

Identify potential bugs, security vulnerabilities, performance issues, and code smells.

For each issue found, provide:
- Line number (if applicable, otherwise null)
- Severity (low, medium, high, critical)
- Description
- Suggestion to fix

Format your response as a JSON array of objects with keys: line, severity, description, suggestion.

Response:"""

        prompt_template = PromptTemplate(
            input_variables=["language", "code"], template=template
        )

        chain = LLMChain(llm=self.llm, prompt=prompt_template)

        result = await chain.ainvoke({"language": language, "code": code})

        # Parse the response
        response_text = result["text"].strip()

        # Try to extract JSON from the response
        try:
            # Look for JSON array in the response
            json_match = re.search(r"\[.*\]", response_text, re.DOTALL)
            if json_match:
                bugs_data = json.loads(json_match.group())
            else:
                # If no JSON found, create a general bug report
                bugs_data = [
                    {
                        "line": None,
                        "severity": "medium",
                        "description": "Code analysis completed",
                        "suggestion": response_text,
                    }
                ]

            bugs = [Bug(**bug) for bug in bugs_data]

            # Cache the result
            bugs_dict = [bug.model_dump() for bug in bugs]
            await cache_service.set(
                "detect_bugs", {"bugs": bugs_dict}, **cache_key_params
            )

            logger.info("Bugs detected", bug_count=len(bugs))

            return bugs

        except (json.JSONDecodeError, Exception) as e:
            logger.warning("Failed to parse bug detection response", error=str(e))
            # If parsing fails, return a general response
            return [
                Bug(
                    line=None,
                    severity="info",
                    description="Bug analysis completed",
                    suggestion=response_text,
                )
            ]

    async def refactor_code(
        self, code: str, language: str, instructions: str = None
    ) -> Dict[str, Any]:
        """
        Refactor code to improve quality.

        Args:
            code: Code to refactor
            language: Programming language
            instructions: Specific refactoring instructions

        Returns:
            Dictionary with refactored code and explanation
        """
        # Try to get from cache
        cache_key_params = {
            "code": code,
            "language": language,
            "instructions": instructions or "",
        }
        cached = await cache_service.get("refactor", **cache_key_params)

        if cached:
            logger.info("Cache hit for code refactoring", language=language)
            return cached

        logger.info(
            "Refactoring code",
            language=language,
            code_length=len(code),
            has_instructions=instructions is not None,
        )

        instructions_section = (
            f"\nSpecific instructions: {instructions}" if instructions else ""
        )

        template = """You are an expert {language} programmer specializing in code refactoring.

Original Code:
```{language}
{code}
```
{instructions_section}

Refactor this code to:
1. Improve readability and maintainability
2. Follow best practices and design patterns
3. Optimize performance where possible
4. Add proper error handling
5. Improve naming conventions

Provide the refactored code and explain the changes made.

Refactored Code:"""

        prompt_template = PromptTemplate(
            input_variables=["language", "code", "instructions_section"],
            template=template,
        )

        chain = LLMChain(llm=self.llm, prompt=prompt_template)

        result = await chain.ainvoke(
            {
                "language": language,
                "code": code,
                "instructions_section": instructions_section,
            }
        )

        refactored = result["text"].strip()

        response = {
            "code": refactored,
            "explanation": "Code has been refactored to improve quality, readability, and maintainability.",
        }

        # Cache the result
        await cache_service.set("refactor", response, **cache_key_params)

        logger.info("Code refactored successfully", refactored_length=len(refactored))

        return response

    async def generate_documentation(
        self, code: str, language: str, style: str = "google"
    ) -> str:
        """
        Generate documentation for code.

        Args:
            code: Code to document
            language: Programming language
            style: Documentation style (google, numpy, sphinx)

        Returns:
            Code with added documentation
        """
        # Try to get from cache
        cache_key_params = {"code": code, "language": language, "style": style}
        cached = await cache_service.get("document", **cache_key_params)

        if cached:
            logger.info("Cache hit for documentation generation", language=language)
            return cached.get("documented_code", "")

        logger.info(
            "Generating documentation",
            language=language,
            code_length=len(code),
            style=style,
        )

        template = """You are an expert {language} programmer. Add comprehensive documentation to the following code.

Code:
```{language}
{code}
```

Add documentation following the {style} style guide. Include:
1. Module/file-level docstrings
2. Function/method docstrings with parameters, returns, and examples
3. Class docstrings
4. Inline comments for complex logic

Provide the fully documented code:"""

        prompt_template = PromptTemplate(
            input_variables=["language", "code", "style"], template=template
        )

        chain = LLMChain(llm=self.llm, prompt=prompt_template)

        result = await chain.ainvoke(
            {"language": language, "code": code, "style": style}
        )

        documented = result["text"].strip()

        # Cache the result
        await cache_service.set(
            "document", {"documented_code": documented}, **cache_key_params
        )

        logger.info("Documentation generated successfully", doc_length=len(documented))

        return documented


# Singleton instance
ai_service = AIService()
