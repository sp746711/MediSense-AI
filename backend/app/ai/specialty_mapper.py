"""Controlled specialty mapping (Stage 11)."""

from typing import Optional

# Controlled mappings — LLM must not invent specialties freely.
SPECIALTY_MAP = {
    "respiratory": ["Pulmonology", "Internal Medicine"],
    "cardiovascular": ["Cardiology"],
    "skin": ["Dermatology"],
    "bones": ["Orthopedics"],
    "joints": ["Orthopedics"],
    "neurological": ["Neurology"],
    "gi": ["Gastroenterology"],
    "endocrine": ["Endocrinology"],
    "thyroid": ["Endocrinology"],
    "eye": ["Ophthalmology"],
    "ent": ["ENT"],
    "dental": ["Dentistry"],
    "general": ["General Physician", "Internal Medicine"],
}


def map_specialty(domains: list[str] | None) -> dict:
    if not domains:
        return {
            "suggested_specialty": None,
            "candidates": [],
            "message": "Insufficient evidence for a suggested specialty.",
            "wording": "Suggested specialty",
        }

    candidates: list[str] = []
    for domain in domains:
        key = domain.strip().lower()
        for specialty in SPECIALTY_MAP.get(key, []):
            if specialty not in candidates:
                candidates.append(specialty)

    if not candidates:
        candidates = list(SPECIALTY_MAP["general"])

    return {
        "suggested_specialty": candidates[0],
        "candidates": candidates,
        "message": f"Suggested specialty: {candidates[0]}",
        "wording": "Suggested specialty",
    }


def primary_suggestion(domain: Optional[str]) -> Optional[str]:
    if not domain:
        return None
    result = map_specialty([domain])
    return result.get("suggested_specialty")
