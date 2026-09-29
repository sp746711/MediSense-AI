"""Controlled follow-up question engine (Stage 9)."""

from typing import Any

# Categories of controlled follow-ups — LLM must not freely invent unlimited questions.
FOLLOWUP_TEMPLATES = {
    "duration": "How long have you had this symptom?",
    "severity": "How severe is the symptom on a scale you would describe (mild, moderate, severe)?",
    "associated": "Are there any other symptoms occurring together with this one?",
    "negatives": "Are there important symptoms that are NOT present (for example, no fever, no chest pain)?",
    "context": "Is there any recent context (injury, travel, known condition) you can share?",
}


def suggest_followups(evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    evidence = evidence or {}
    missing = evidence.get("missing") or []
    questions: list[dict[str, str]] = []

    for category in ("duration", "severity", "associated", "negatives", "context"):
        if not missing or category in missing or evidence.get("evidence_state") == "INSUFFICIENT_EVIDENCE":
            questions.append(
                {
                    "category": category,
                    "question": FOLLOWUP_TEMPLATES[category],
                }
            )

    # Cap to a controlled set
    questions = questions[:5]
    return {
        "needed": bool(questions),
        "questions": questions,
        "message": (
            "Available information is insufficient for a specific conclusion. "
            "What information may help?"
            if questions
            else "No additional follow-up questions at this time."
        ),
    }
