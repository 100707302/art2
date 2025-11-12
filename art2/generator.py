"""Concept generation engine implementing the logical-semiotic formula."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence

from .emotion import AffectiveTimeline
from .knowledge import KnowledgeBase, KnowledgeEntry
from .tropes import TropesProfile


@dataclass
class GenerationParameters:
    """User-facing switches that influence how a concept is generated."""

    semiotic_object: str
    representamen: Sequence[str]
    possible_world: str
    interpretant_focus: Sequence[str] = field(default_factory=tuple)
    discipline_bias: Optional[Dict[str, float]] = None
    tropes: Optional[TropesProfile] = None
    affective_timeline: Optional[AffectiveTimeline] = None
    knowledge_prompt: Optional[str] = None
    knowledge_top_k: int = 4


class ArtConceptGenerator:
    """Generate art concepts using logical, semiotic and affective scaffolds."""

    def __init__(self, knowledge_base: KnowledgeBase) -> None:
        self._knowledge_base = knowledge_base

    def generate(self, params: GenerationParameters) -> Dict[str, object]:
        """Produce a structured concept document."""

        knowledge_prompt = params.knowledge_prompt or params.semiotic_object
        discipline_bias = params.discipline_bias or {}
        selections = self._knowledge_base.query(
            knowledge_prompt,
            top_k=params.knowledge_top_k,
            discipline_bias=discipline_bias,
        )

        possible_world_statement = f"◇({params.semiotic_object} ∧ {', '.join(params.representamen)})"
        interpretant_notes = list(params.interpretant_focus)
        interpretant_notes.extend(entry.summary for entry in selections)

        structure = {
            "formula": {
                "possible_world": params.possible_world,
                "semiotic_expression": possible_world_statement,
                "interpretant_triggers": interpretant_notes,
            },
            "knowledge_sources": [self._format_entry(entry) for entry in selections],
            "tropes": params.tropes.as_dict() if params.tropes else None,
            "affective_timeline": params.affective_timeline.to_bullets()
            if params.affective_timeline
            else None,
        }
        structure["summary"] = self._compose_summary(params, structure)
        return structure

    @staticmethod
    def _format_entry(entry: KnowledgeEntry) -> Dict[str, object]:
        return {
            "id": entry.id,
            "discipline": entry.discipline,
            "concept": entry.concept,
            "summary": entry.summary,
            "keywords": list(entry.keywords),
        }

    def _compose_summary(self, params: GenerationParameters, structure: Dict[str, object]) -> str:
        representamen = ", ".join(params.representamen)
        knowledge_highlights = "; ".join(
            f"{item['concept']} ({item['discipline']})" for item in structure["knowledge_sources"]
        ) or "custom research"
        tropes_text = "; ".join(
            f"{axis}: {', '.join(values)}"
            for axis, values in (params.tropes.as_dict().items() if params.tropes else [])
            if values
        )
        affective_text = " → ".join(structure["affective_timeline"] or []) if structure["affective_timeline"] else ""

        summary_parts: List[str] = [
            f"Starting from the possible world '{params.possible_world}', the work binds {params.semiotic_object} to {representamen} to yield recursive interpretants.",
            f"Knowledge anchors: {knowledge_highlights}.",
        ]
        if tropes_text:
            summary_parts.append(f"Rhetorical pathways: {tropes_text}.")
        if affective_text:
            summary_parts.append(f"Affective arc: {affective_text}.")
        return " \n".join(summary_parts)

