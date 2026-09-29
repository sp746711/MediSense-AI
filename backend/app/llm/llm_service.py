"""LLM provider orchestration: Groq → Gemini → Ollama → safe unavailable."""

from typing import Any, Optional

from app.core.config import get_settings
from app.llm.gemini_service import GeminiService
from app.llm.groq_service import GroqService
from app.llm.ollama_service import OllamaService
from app.utils.logging import get_logger

logger = get_logger(__name__)

UNAVAILABLE_MESSAGE = "AI Assistant is temporarily unavailable."


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.providers = {
            "groq": GroqService(),
            "gemini": GeminiService(),
            "ollama": OllamaService(),
        }

    def _ordered_providers(self) -> list[str]:
        order = [
            self.settings.llm_provider,
            self.settings.llm_fallback,
            self.settings.llm_offline,
        ]
        seen: set[str] = set()
        result: list[str] = []
        for name in order:
            key = (name or "").strip().lower()
            if key and key not in seen and key in self.providers:
                seen.add(key)
                result.append(key)
        return result

    def generate(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        for name in self._ordered_providers():
            provider = self.providers[name]
            if not provider.is_available():
                logger.info("LLM provider unavailable: %s", name)
                continue
            try:
                result = provider.generate(prompt, **kwargs)
                if result.get("status") == "ok":
                    result["provider"] = name
                    return result
            except Exception as exc:  # noqa: BLE001
                logger.warning("LLM provider %s failed: %s", name, exc)
                continue
        return {
            "status": "unavailable",
            "message": UNAVAILABLE_MESSAGE,
            "provider": None,
            "content": None,
        }

    def generate_assistant_reply(
        self,
        user_message: str,
        assessment_context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Generate a grounded reply; never invent triage/providers/findings."""
        context_lines = []
        if assessment_context:
            context_lines.append(
                f"Assessment status: {assessment_context.get('status')}"
            )
            context_lines.append(
                f"Pathway (rules engine): {assessment_context.get('pathway') or 'not determined'}"
            )
            context_lines.append(
                f"Suggested specialty: {assessment_context.get('specialty') or 'not determined'}"
            )
            context_lines.append(
                f"Input types: {assessment_context.get('input_types')}"
            )
        else:
            context_lines.append("No assessment context available for this user yet.")

        system_constraints = (
            "You are MediSense AI Assistant. Explain and summarize only. "
            "Do NOT invent diagnosis, triage pathway, X-ray findings, report values, "
            "doctors, facilities, appointments, or prescriptions. "
            "If information is missing, say it is unavailable. "
            "Triage pathway is decided only by the rules engine."
        )

        prompt = (
            f"{system_constraints}\n\n"
            f"Context:\n" + "\n".join(context_lines) + "\n\n"
            f"User question: {user_message}\n"
        )

        result = self.generate(prompt)
        if result.get("status") != "ok":
            # Safe offline-style grounded response without inventing clinical content
            return {
                "status": "unavailable",
                "message": UNAVAILABLE_MESSAGE,
                "answer": (
                    "AI Assistant is temporarily unavailable. "
                    "Based on stored assessment context only: "
                    + (
                        f"pathway={assessment_context.get('pathway')}, "
                        f"specialty={assessment_context.get('specialty')}, "
                        f"inputs={assessment_context.get('input_types')}."
                        if assessment_context
                        else "no completed assessment is available yet."
                    )
                    + " Please try again later or review your assessment details in the app."
                ),
                "provider": None,
                "grounded": True,
            }

        return {
            "status": "ok",
            "answer": result.get("content"),
            "provider": result.get("provider"),
            "message": "ok",
            "grounded": True,
        }
