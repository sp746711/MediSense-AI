"""Report OCR stub (Stage 6)."""

from typing import Any


def extract_text_from_file(file_path: str) -> dict[str, Any]:
    return {
        "status": "unavailable",
        "extracted_text": None,
        "message": "Unable to extract readable text from this document.",
        "ocr_version": "report-ocr-v0.1",
        "file_path": file_path,
    }
