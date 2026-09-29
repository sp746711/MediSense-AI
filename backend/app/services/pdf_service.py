"""PDF assessment report service stub (Stage 16)."""

from typing import Any


def generate_assessment_pdf(_assessment_id: str) -> dict[str, Any]:
    return {
        "status": "unavailable",
        "message": "PDF report generation will be available after assessment pipeline completion.",
        "path": None,
    }
