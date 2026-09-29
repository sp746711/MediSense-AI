"""Grad-CAM explainability adapter (wired in Stage 7)."""

from typing import Any


def generate_gradcam(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    """Return unavailable until a model forward pass is available."""
    return {
        "status": "unavailable",
        "label": "Model Explainability Visualization",
        "message": (
            "Grad-CAM visualization is unavailable. "
            "It is an explainability aid, not proof of disease."
        ),
        "artifact_path": None,
    }
