"""Ollama offline LLM provider."""

from typing import Any

from app.core.config import get_settings


class OllamaService:
    def is_available(self) -> bool:
        # Presence of base URL is not enough; Stage 15 will ping /api/tags.
        return bool(get_settings().ollama_base_url)

    def generate(self, prompt: str, **_kwargs: Any) -> dict[str, Any]:
        return {
            "status": "unavailable",
            "content": None,
            "message": "Ollama offline client not yet activated for this environment.",
        }
