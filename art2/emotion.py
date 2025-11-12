"""Emotional timeline models for concept generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Sequence


@dataclass
class AffectiveEvent:
    """Single emotional beat occurring at a relative timestamp."""

    label: str
    intensity: float
    timestamp: float
    modalities: Sequence[str] = field(default_factory=tuple)

    def describe(self) -> str:
        modes = ", ".join(self.modalities) if self.modalities else "multimodal cues"
        return f"t={self.timestamp:.2f}: {self.label} (intensity {self.intensity:.2f}, via {modes})"


class AffectiveTimeline:
    """Container for affective events with helpful summaries."""

    def __init__(self, events: Iterable[AffectiveEvent] | None = None) -> None:
        self._events: List[AffectiveEvent] = []
        if events:
            for event in events:
                self.add_event(event)

    def add_event(self, event: AffectiveEvent) -> None:
        self._events.append(event)
        self._events.sort(key=lambda e: e.timestamp)

    def __iter__(self):
        return iter(self._events)

    def to_bullets(self) -> List[str]:
        return [event.describe() for event in self._events]

    def normalize(self) -> None:
        if not self._events:
            return
        max_intensity = max(event.intensity for event in self._events) or 1.0
        for event in self._events:
            event.intensity /= max_intensity

