"""Tropes and rhetorical pattern utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence


@dataclass
class TropesProfile:
    """Selected tropes for the morphology, structure and experience axes."""

    morphology: Sequence[str] = field(default_factory=tuple)
    structure: Sequence[str] = field(default_factory=tuple)
    experience: Sequence[str] = field(default_factory=tuple)

    def as_dict(self) -> Dict[str, Sequence[str]]:
        return {
            "morphology": tuple(self.morphology),
            "structure": tuple(self.structure),
            "experience": tuple(self.experience),
        }


class TropesLibrary:
    """Convenience collection for looking up standard trope suggestions."""

    def __init__(self) -> None:
        self._categories: Dict[str, List[str]] = {
            "morphology": [
                "material inversion",
                "scale exaggeration",
                "palimpsest layering",
                "color-monochrome tension",
            ],
            "structure": [
                "temporal loop",
                "fragmented narrative",
                "mirrored spatial axis",
                "processual reveal",
            ],
            "experience": [
                "guided stillness",
                "collective participation",
                "ambient estrangement",
                "sensorial crescendo",
            ],
        }

    def add(self, category: str, tropes: Iterable[str]) -> None:
        self._categories.setdefault(category, [])
        for trope in tropes:
            if trope not in self._categories[category]:
                self._categories[category].append(trope)

    def get(self, category: str) -> Sequence[str]:
        return tuple(self._categories.get(category, ()))

    def recommend(self, *, focus: str | None = None) -> TropesProfile:
        focus_categories = {focus} if focus else self._categories.keys()
        return TropesProfile(
            morphology=self._categories.get("morphology", []) if "morphology" in focus_categories else (),
            structure=self._categories.get("structure", []) if "structure" in focus_categories else (),
            experience=self._categories.get("experience", []) if "experience" in focus_categories else (),
        )

