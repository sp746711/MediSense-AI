from app.ai.triage_engine import apply_triage


def test_triage_does_not_force_pathway_on_insufficient():
    result = apply_triage({"evidence_state": "INSUFFICIENT_EVIDENCE"})
    assert result["pathway"] is None
    assert result["status"] == "INSUFFICIENT_EVIDENCE"
    assert result["clinically_validated"] is False
