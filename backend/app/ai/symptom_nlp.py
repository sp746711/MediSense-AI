"""Symptom NLP stub (Stage 5)."""

from typing import Any


def extract_symptoms(raw_text: str) -> dict[str, Any]:
    """Extract structured symptoms. Returns empty extraction until NLP is wired."""
    if not raw_text or not raw_text.strip():
        return {
            "status": "empty",
            "symptoms": [],
            "message": "No symptom text provided.",
            "source": "user_input",
        }
    return {
        "status": "pending_nlp",
        "symptoms": [],
        "raw_text": raw_text.strip(),
        "message": (
            "Symptom text received. Structured NLP extraction "
            "(present/absent/negation/duration) is not yet fully wired."
        ),
        "source": "user_input",
        "nlp_version": "symptom-nlp-v0.1",
    }
