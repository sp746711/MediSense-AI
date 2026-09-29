"""Symptoms routes — NLP integration in Stage 5."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUser, DbSession
from app.database.models import Assessment, Symptom
from app.schemas.assessment import SymptomSubmitRequest

router = APIRouter(prefix="/assessments", tags=["Symptoms"])


@router.post("/{assessment_id}/symptoms")
def submit_symptoms(
    assessment_id: UUID,
    payload: SymptomSubmitRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> dict:
    assessment = _owned(db, assessment_id, current_user.user_id)
    if "symptoms" not in (assessment.input_types or []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This assessment was not configured for symptoms input.",
        )

    # Store raw text as a single UNKNOWN placeholder until NLP Stage 5
    # Do NOT invent structured symptoms.
    row = Symptom(
        assessment_id=assessment.assessment_id,
        symptom="raw_input_pending_nlp",
        state="UNKNOWN",
        context=payload.raw_text,
        source="user_input",
    )
    db.add(row)
    if assessment.status == "draft":
        assessment.status = "inputs_received"
    db.add(assessment)
    db.commit()
    db.refresh(row)

    return {
        "status": "received",
        "message": (
            "Symptoms text received. Structured NLP extraction will run "
            "when the symptom NLP module is fully wired."
        ),
        "symptom_id": str(row.symptom_id),
        "raw_text_stored": True,
        "extracted": [],
    }


@router.get("/{assessment_id}/symptoms")
def list_symptoms(
    assessment_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> dict:
    _owned(db, assessment_id, current_user.user_id)
    rows = db.query(Symptom).filter(Symptom.assessment_id == assessment_id).all()
    return {
        "assessment_id": str(assessment_id),
        "symptoms": [
            {
                "symptom_id": str(s.symptom_id),
                "symptom": s.symptom,
                "state": s.state,
                "duration": s.duration,
                "severity": s.severity,
                "body_area": s.body_area,
                "context": s.context,
                "source": s.source,
            }
            for s in rows
        ],
    }


def _owned(db: DbSession, assessment_id: UUID, user_id: UUID) -> Assessment:
    assessment = db.get(Assessment, assessment_id)
    if assessment is None or assessment.user_id != user_id:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment
