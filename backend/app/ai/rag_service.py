"""RAG service stub (Stage 15). Retrieval is separate from the LLM."""

from typing import Any


class RAGService:
    """Modular retrieval over trusted knowledge sources."""

    def __init__(self) -> None:
        self.knowledge_source_ids: list[str] = []

    def is_configured(self) -> bool:
        return False

    def retrieve(self, query: str, top_k: int = 5) -> dict[str, Any]:
        if not self.is_configured():
            return {
                "status": "unavailable",
                "chunks": [],
                "knowledge_source_ids": [],
                "message": (
                    "Trusted knowledge retrieval is not configured yet. "
                    "General explanations will be limited."
                ),
            }
        return {
            "status": "ok",
            "chunks": [],
            "knowledge_source_ids": self.knowledge_source_ids,
            "query": query,
            "top_k": top_k,
        }
