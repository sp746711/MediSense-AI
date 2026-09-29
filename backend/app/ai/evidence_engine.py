"""Evidence combination engine stub (Stage 8)."""

from typing import Any


def combine_evidence(
    symptoms: list[dict[str, Any]] | None = None,
    report_findings: list[dict[str, Any]] | None = None,
    xray_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Combine multimodal evidence without collapsing uncertainty."""
    return {
        "symptoms": symptoms or [],
        "report": report_findings or [],
        "xray": xray_result,
        "supporting": [],
        "contradictory": [],
        "missing": [],
        "unknown": [],
        "evidence_state": "INSUFFICIENT_EVIDENCE",
        "message": "Evidence engine not yet fully wired.",
    }
