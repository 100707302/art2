"""Knowledge base utilities for the conceptual art generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence
import json
import math
import re
from collections import Counter, defaultdict

_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9']+")
_STOPWORDS = {
    "the",
    "and",
    "of",
    "in",
    "to",
    "a",
    "is",
    "for",
    "on",
    "with",
    "as",
    "by",
    "an",
    "be",
    "are",
    "that",
    "from",
    "or",
    "at",
    "into",
    "this",
    "it",
    "through",
    "their",
}


def _tokenize(text: str) -> List[str]:
    return [token.lower() for token in _WORD_RE.findall(text)]


def _filter_tokens(tokens: Iterable[str]) -> List[str]:
    return [token for token in tokens if token not in _STOPWORDS]


@dataclass
class KnowledgeEntry:
    """A single knowledge entry used for concept generation."""

    id: str
    discipline: str
    concept: str
    summary: str
    keywords: Sequence[str] = field(default_factory=list)

    def tokenise(self) -> Counter:
        tokens = _filter_tokens(_tokenize(" ".join([self.concept, self.summary, " ".join(self.keywords)])))
        return Counter(tokens)


class KnowledgeBase:
    """Container for multiple :class:`KnowledgeEntry` items with vector search."""

    def __init__(self) -> None:
        self._entries: Dict[str, KnowledgeEntry] = {}
        self._vectors: Dict[str, Counter] = {}
        self._idf: Dict[str, float] = {}

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterable[KnowledgeEntry]:
        return iter(self._entries.values())

    def add(self, entry: KnowledgeEntry) -> None:
        if entry.id in self._entries:
            raise ValueError(f"Duplicate knowledge entry id: {entry.id}")
        vector = entry.tokenise()
        self._entries[entry.id] = entry
        self._vectors[entry.id] = vector
        self._recalculate_idf()

    def extend(self, entries: Iterable[KnowledgeEntry]) -> None:
        for entry in entries:
            self.add(entry)

    def get(self, entry_id: str) -> KnowledgeEntry:
        return self._entries[entry_id]

    def _recalculate_idf(self) -> None:
        df: Dict[str, int] = defaultdict(int)
        for vector in self._vectors.values():
            for token in vector:
                df[token] += 1
        total_docs = len(self._vectors) or 1
        self._idf = {token: math.log((1 + total_docs) / (1 + freq)) + 1 for token, freq in df.items()}

    def _tfidf(self, vector: Counter) -> Dict[str, float]:
        return {token: freq * self._idf.get(token, 1.0) for token, freq in vector.items()}

    def query(
        self,
        prompt: str,
        *,
        top_k: int = 5,
        discipline_bias: Optional[Dict[str, float]] = None,
    ) -> List[KnowledgeEntry]:
        """Return the top-k knowledge entries most similar to the prompt."""

        if not self._entries:
            return []

        tokens = Counter(_filter_tokens(_tokenize(prompt)))
        query_vec = self._tfidf(tokens)
        scores: List[tuple[float, KnowledgeEntry]] = []
        for entry_id, entry in self._entries.items():
            entry_vec = self._tfidf(self._vectors[entry_id])
            score = self._cosine_similarity(query_vec, entry_vec)
            if discipline_bias and entry.discipline in discipline_bias:
                score *= discipline_bias[entry.discipline]
            scores.append((score, entry))
        scores.sort(key=lambda item: item[0], reverse=True)
        top = scores[:top_k]
        positives = [entry for score, entry in top if score > 0]
        if positives:
            return positives
        return [entry for _score, entry in top]

    @staticmethod
    def _cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        if not vec_a or not vec_b:
            return 0.0
        numerator = sum(vec_a[token] * vec_b.get(token, 0.0) for token in vec_a)
        denom_a = math.sqrt(sum(value * value for value in vec_a.values()))
        denom_b = math.sqrt(sum(value * value for value in vec_b.values()))
        if denom_a == 0 or denom_b == 0:
            return 0.0
        return numerator / (denom_a * denom_b)

    @classmethod
    def from_json(cls, path: Path | str) -> "KnowledgeBase":
        base = cls()
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        entries = [
            KnowledgeEntry(
                id=item["id"],
                discipline=item["discipline"],
                concept=item["concept"],
                summary=item["summary"],
                keywords=item.get("keywords", []),
            )
            for item in data
        ]
        base.extend(entries)
        return base

    def to_json(self, path: Path | str) -> None:
        data = [
            {
                "id": entry.id,
                "discipline": entry.discipline,
                "concept": entry.concept,
                "summary": entry.summary,
                "keywords": list(entry.keywords),
            }
            for entry in self._entries.values()
        ]
        Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


