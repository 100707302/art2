"""Simple JSON-backed knowledge base implementation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from .base import KnowledgeBase, KnowledgeItem


@dataclass
class JSONKnowledgeBase(KnowledgeBase):
    """Load structured fragments from a JSON file."""

    path: Path

    def __post_init__(self) -> None:
        self._items = self._load_items(self.path)

    @staticmethod
    def _load_items(path: Path) -> List[KnowledgeItem]:
        payload = json.loads(path.read_text())
        items: List[KnowledgeItem] = []
        for entry in payload:
            items.append(
                KnowledgeItem(
                    title=entry.get("title", ""),
                    description=entry.get("description", ""),
                    tags=list(entry.get("tags", [])),
                    vectors=entry.get("vectors", {}),
                    metadata=entry.get("metadata", {}),
                )
            )
        return items

    def search(
        self,
        query: Optional[str] = None,
        *,
        concepts: Optional[Iterable[str]] = None,
        limit: int = 5,
    ) -> List[KnowledgeItem]:
        filtered = self._items

        if concepts:
            concept_set = {concept.lower() for concept in concepts}
            filtered = [
                item
                for item in filtered
                if concept_set.intersection(tag.lower() for tag in item.tags)
            ]

        if query:
            ranked = sorted(
                filtered,
                key=lambda item: self._score_item(query, item),
                reverse=True,
            )
        else:
            ranked = filtered

        return ranked[:limit]

    @staticmethod
    def _score_item(query: str, item: KnowledgeItem) -> float:
        if not query:
            return 1.0

        terms = [token.strip() for token in query.lower().split() if token.strip()]
        if not terms:
            return 1.0

        haystack = f"{item.title} {item.description} {' '.join(item.tags)}".lower()
        matches = sum(1 for term in terms if term in haystack)
        return matches / len(terms)
