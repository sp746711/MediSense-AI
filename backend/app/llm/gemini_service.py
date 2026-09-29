"""Gemini LLM provider (fallback)."""

from typing import Any

from app.core.config import get_settings


class GeminiService:
    def is_available(self) -> bool:
        return bool(get_settings().gemini_api_key)

    def generate(self, prompt: str, **_kwargs: Any) -> dict[str, Any]:
        if not self.is_available():
            return {"status": "unavailable", "content": None, "message": "Gemini API key not configured"}
        return {
            "status": "unavailable",
            "content": None,
            "message": "Gemini client not yet activated for this environment.",
        }
