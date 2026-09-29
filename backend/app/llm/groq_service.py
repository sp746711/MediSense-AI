"""Groq-hosted open model provider."""

from typing import Any

from app.core.config import get_settings


class GroqService:
    def is_available(self) -> bool:
        return bool(get_settings().groq_api_key)

    def generate(self, prompt: str, **_kwargs: Any) -> dict[str, Any]:
        if not self.is_available():
            return {"status": "unavailable", "content": None, "message": "Groq API key not configured"}
        # Full HTTP client wiring in Stage 15
        return {
            "status": "unavailable",
            "content": None,
            "message": "Groq client not yet activated for this environment.",
        }
