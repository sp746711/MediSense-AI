"""Medical report NLP stub (Stage 6)."""

from typing import Any


def structure_report_text(text: str | None) -> dict[str, Any]:
    if not text:
        return {
            "status": "unavailable",
            "findings": [],
            "reference_ranges": [],
            "message": "No report text available for NLP structuring.",
            "source": "uploaded_report",
        }
    return {
        "status": "pending_nlp",
        "findings": [],
        "reference_ranges": [],
        "message": "Report NLP structuring is not yet fully wired.",
        "source": "uploaded_report",
    }
