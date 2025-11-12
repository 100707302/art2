"""High-level pipeline orchestrating the concept formula."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .generator import ArtConcept, ArtGenerator
from .knowledge.jsonkb import JSONKnowledgeBase


@dataclass
class PipelineConfig:
    """Configuration bundle for the generation pipeline."""

    query: str
    modal_prefix: str
    semiotic_focus: Sequence[str]
    interpretant_prompts: Sequence[str]
    tropes: Mapping[str, Sequence[str]]
    affective_beats: Sequence[str]
    references: Sequence[str]
    knowledge_path: Path
    knowledge_limit: int = 5


class GenerationPipeline:
    """Generate concepts using the semiotic logic formula."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self._knowledge_base = JSONKnowledgeBase(config.knowledge_path)
        self._generator = ArtGenerator(self._knowledge_base)

    def run(self) -> ArtConcept:
        """Execute the pipeline."""

        return self._generator.generate(
            query=self.config.query,
            modal_prefix=self.config.modal_prefix,
            semiotic_focus=self.config.semiotic_focus,
            interpretant_prompts=self.config.interpretant_prompts,
            trope_presets=self.config.tropes,
            affective_beats=self.config.affective_beats,
            references=self.config.references,
            knowledge_limit=self.config.knowledge_limit,
        )

    @staticmethod
    def from_dict(payload: Mapping[str, object], knowledge_root: Path) -> "GenerationPipeline":
        """Create a pipeline from loosely structured data."""

        config = PipelineConfig(
            query=str(payload.get("query", "Untitled Concept")),
            modal_prefix=str(payload.get("modal_prefix", "an unresolved conjunction of bodies and signals")),
            semiotic_focus=tuple(payload.get("semiotic_focus", [])),
            interpretant_prompts=tuple(payload.get("interpretant_prompts", [])),
            tropes={key: tuple(value) for key, value in payload.get("tropes", {}).items()},
            affective_beats=tuple(payload.get("affective_beats", [])),
            references=tuple(payload.get("references", [])),
            knowledge_path=knowledge_root / str(payload.get("knowledge_file", "knowledge.json")),
            knowledge_limit=int(payload.get("knowledge_limit", 5)),
        )
        return GenerationPipeline(config)
