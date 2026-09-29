from app.ai.evidence_engine import combine_evidence


def test_evidence_insufficient_by_default():
    result = combine_evidence()
    assert result["evidence_state"] == "INSUFFICIENT_EVIDENCE"
