"""X-ray model adapter.

Loads trained checkpoints when configured. Never invents findings.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from app.core.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)


class XRayModelService:
    """Interface for region-specific X-ray models (ResNet/CNN)."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._model = None
        self._loaded = False
        self.model_version: Optional[str] = None

    def load_model(self) -> bool:
        """Load checkpoint if configured. Does not train at startup."""
        checkpoint = (self.settings.xray_chest_checkpoint or "").strip()
        if not checkpoint:
            logger.info("No X-ray checkpoint configured (XRAY_CHEST_CHECKPOINT).")
            self._loaded = False
            return False

        path = Path(checkpoint)
        if not path.is_absolute():
            path = self.settings.xray_model_path / path
        if not path.exists():
            logger.warning("X-ray checkpoint path does not exist: %s", path)
            self._loaded = False
            return False

        # Stage 7 will load torch/resnet weights here.
        # For foundation stage we only validate presence.
        self.model_version = f"{self.settings.xray_default_model}@file"
        self._loaded = True
        logger.info("X-ray checkpoint present: %s", path)
        return True

    def is_available(self) -> bool:
        if not self._loaded:
            self.load_model()
        return self._loaded

    def analyze(self, image_path: str, region: Optional[str] = None) -> dict[str, Any]:
        """Run inference or return a clear unavailable status."""
        if not self.is_available():
            return {
                "status": "unavailable",
                "region": region or "unknown",
                "model_version": None,
                "prediction": None,
                "confidence_if_valid": None,
                "uncertainty": "Model not configured",
                "explainability_artifact": None,
                "message": (
                    "X-ray received successfully. Automated interpretation for this "
                    "X-ray type is currently unavailable. If you have the associated "
                    "radiology report, upload it for supported text-based analysis."
                ),
            }

        # Placeholder until Stage 7 wires real inference — still no fabricated finding.
        return {
            "status": "unavailable",
            "region": region or "chest",
            "model_version": self.model_version,
            "prediction": None,
            "confidence_if_valid": None,
            "uncertainty": "Inference pipeline not yet activated",
            "explainability_artifact": None,
            "message": (
                "X-ray model checkpoint is present but inference is not yet enabled. "
                "No finding was generated."
            ),
        }

    def get_explanation(self, image_path: str) -> dict[str, Any]:
        return {
            "status": "unavailable",
            "label": "Model Explainability Visualization",
            "message": "Grad-CAM explainability is not available without an active model run.",
        }
