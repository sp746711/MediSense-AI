"""Medical report upload routes — OCR/NLP in Stage 6."""

import uuid
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.core.dependencies import CurrentUser, DbSession
from app.database.models import Assessment, MedicalReport
from app.utils.file_validation import validate_report_file

router = APIRouter(prefix="/assessments", tags=["Medical Reports"])


@router.post("/{assessment_id}/reports")
async def upload_report(
    assessment_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
    file: UploadFile = File(...),
) -> dict:
    assessment = _owned(db, assessment_id, current_user.user_id)
    if "medical_report" not in (assessment.input_types or []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This assessment was not configured for medical report input.",
        )

    settings = get_settings()
    content = await file.read()
    validation = validate_report_file(file.filename or "", content, settings.max_upload_size_mb)
    if not validation["ok"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation["message"])

    reports_dir = settings.upload_path / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}{validation['extension']}"
    dest = reports_dir / stored_name
    dest.write_bytes(content)

    report = MedicalReport(
        assessment_id=assessment.assessment_id,
        file_name=Path(file.filename or "report").name,
        stored_name=stored_name,
        file_type=validation["file_type"],
        extracted_text=None,
        structured_findings=None,
        reference_ranges=None,
        ocr_metadata={"status": "pending", "message": "OCR pipeline not yet executed"},
    )
    db.add(report)
    if assessment.status == "draft":
        assessment.status = "inputs_received"
    db.add(assessment)
    db.commit()
    db.refresh(report)

    return {
        "status": "received",
        "report_id": str(report.report_id),
        "file_name": report.file_name,
        "message": (
            "Medical report uploaded successfully. Text extraction and medical NLP "
            "will run when the report processing module is fully wired."
        ),
        "structured_findings": None,
    }


@router.get("/{assessment_id}/reports")
def list_reports(
    assessment_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> dict:
    _owned(db, assessment_id, current_user.user_id)
    rows = (
        db.query(MedicalReport)
        .filter(MedicalReport.assessment_id == assessment_id)
        .all()
    )
    return {
        "assessment_id": str(assessment_id),
        "reports": [
            {
                "report_id": str(r.report_id),
                "file_name": r.file_name,
                "file_type": r.file_type,
                "created_at": r.created_at.isoformat(),
                "has_extracted_text": bool(r.extracted_text),
                "structured_findings": r.structured_findings,
            }
            for r in rows
        ],
    }


def _owned(db: DbSession, assessment_id: UUID, user_id: UUID) -> Assessment:
    assessment = db.get(Assessment, assessment_id)
    if assessment is None or assessment.user_id != user_id:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment
