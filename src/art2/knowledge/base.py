"""Abstract interfaces for knowledge base connectors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Mapping, Optional


@dataclass
class KnowledgeItem:
    """Structured information retrieved from a knowledge base."""

    title: str
    description: str
    tags: List[str]
    vectors: Mapping[str, List[float]]
    metadata: Mapping[str, str]


class KnowledgeBase:
    """Interface for retrieving multimodal knowledge fragments."""

    def search(
        self,
        query: Optional[str] = None,
        *,
        concepts: Optional[Iterable[str]] = None,
        limit: int = 5,
    ) -> List[KnowledgeItem]:
        """Retrieve relevant knowledge fragments.

        Args:
            query: Free-form text prompt to match.
            concepts: Optional set of concept identifiers to focus on.
            limit: Maximum number of items to return.
        """

        raise NotImplementedError
