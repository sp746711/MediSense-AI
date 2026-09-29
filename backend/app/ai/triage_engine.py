"""Rule-based triage / safety engine stub (Stage 10).

The LLM must NEVER independently decide the pathway.
"""

from typing import Any

PATHWAYS = ("EMERGENCY", "CONSULTATION", "MILD")
RULES_VERSION = "triage-rules-v0.1"


def apply_triage(evidence: dict[str, Any]) -> dict[str, Any]:
    """Apply safety rules to structured evidence.

    Foundation behavior: if evidence is insufficient, do not force a pathway.
    """
    state = (evidence or {}).get("evidence_state")
    if state in {"INSUFFICIENT_EVIDENCE", None}:
        return {
            "pathway": None,
            "status": "INSUFFICIENT_EVIDENCE",
            "rules_version": RULES_VERSION,
            "rules_triggered": [],
            "message": "Available information is insufficient for a specific conclusion.",
            "clinically_validated": False,
        }

    if state == "CONFLICTING_EVIDENCE":
        return {
            "pathway": None,
            "status": "CONFLICTING_EVIDENCE",
            "rules_version": RULES_VERSION,
            "rules_triggered": [],
            "message": (
                "The available inputs contain conflicting information. "
                "Please review the information provided."
            ),
            "clinically_validated": False,
        }

    return {
        "pathway": "CONSULTATION",
        "status": "ok",
        "rules_version": RULES_VERSION,
        "rules_triggered": ["default_consultation_when_evidence_present"],
        "message": "Suggested pathway based on rule engine (not clinically validated).",
        "clinically_validated": False,
    }
