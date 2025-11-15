"""
AI Service for code operations using OpenAI and LangChain.
"""
from typing import List, Dict, Any
import openai
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from app.core.config import settings
from app.schemas.code import Bug
import json
import re


class AIService:
    """Service for AI-powered code operations."""

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

        return {
            "code": code,
            "explanation": f"Generated {language} code based on the prompt: {prompt}",
        }

    async def explain_code(self, code: str, language: str) -> str:
        """
        Explain what a piece of code does.

        Args:
            code: Code to explain
            language: Programming language

        Returns:
            Detailed explanation of the code
        """
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

        return result["text"].strip()

    async def detect_bugs(self, code: str, language: str) -> List[Bug]:
        """
        Detect potential bugs in code.

        Args:
            code: Code to analyze
            language: Programming language

        Returns:
            List of detected bugs
        """
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
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
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
            return bugs

        except (json.JSONDecodeError, Exception) as e:
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

        return {
            "code": refactored,
            "explanation": "Code has been refactored to improve quality, readability, and maintainability.",
        }

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

        return result["text"].strip()


# Singleton instance
ai_service = AIService()
