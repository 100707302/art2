"""Core concept generation primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Mapping, Sequence

from .knowledge.base import KnowledgeBase, KnowledgeItem


@dataclass
class ArtConcept:
    """Container for a generated art concept description."""

    title: str
    modal_hypothesis: str
    semiotic_binding: str
    interpretant_paths: List[str]
    tropes: Mapping[str, List[str]]
    affective_timeline: List[str]
    references: List[str] = field(default_factory=list)

    def as_markdown(self) -> str:
        """Render the concept as a markdown document."""

        sections = [f"# {self.title}"]
        sections.append("## Modal Hypothesis" )
        sections.append(self.modal_hypothesis)
        sections.append("## Semiotic Binding")
        sections.append(self.semiotic_binding)
        sections.append("## Interpretant Paths")
        for idx, path in enumerate(self.interpretant_paths, start=1):
            sections.append(f"{idx}. {path}")
        sections.append("## Tropes")
        for dimension, items in self.tropes.items():
            joined = ", ".join(items)
            sections.append(f"- **{dimension}**: {joined}")
        sections.append("## Affective Timeline")
        for idx, beat in enumerate(self.affective_timeline, start=1):
            sections.append(f"{idx}. {beat}")
        if self.references:
            sections.append("## References")
            for ref in self.references:
                sections.append(f"- {ref}")
        return "\n".join(sections)


@dataclass
class ArtGenerator:
    """Generate art concepts from knowledge fragments."""

    knowledge_base: KnowledgeBase

    def generate(
        self,
        *,
        query: str,
        modal_prefix: str,
        semiotic_focus: Sequence[str],
        interpretant_prompts: Sequence[str],
        trope_presets: Mapping[str, Sequence[str]],
        affective_beats: Sequence[str],
        references: Iterable[str] = (),
        knowledge_limit: int = 5,
    ) -> ArtConcept:
        """Generate a complete art concept."""

        fragments = self.knowledge_base.search(query, concepts=semiotic_focus, limit=knowledge_limit)
        combined_description = self._compose_description(fragments, semiotic_focus)
        interpretants = self._build_interpretant_paths(interpretant_prompts, fragments)
        tropes = {dimension: list(options) for dimension, options in trope_presets.items()}
        affective_timeline = list(affective_beats)

        return ArtConcept(
            title=query.title(),
            modal_hypothesis=f"◇ {modal_prefix}",
            semiotic_binding=combined_description,
            interpretant_paths=interpretants,
            tropes=tropes,
            affective_timeline=affective_timeline,
            references=list(references),
        )

    @staticmethod
    def _compose_description(
        fragments: Sequence[KnowledgeItem],
        focus_tags: Sequence[str],
    ) -> str:
        if not fragments:
            return "No matching fragments were found; consider expanding the knowledge base."

        lines = [
            "This concept binds the following knowledge fragments:",
        ]
        for item in fragments:
            lines.append(f"- {item.title}: {item.description}")
        if focus_tags:
            focus = ", ".join(focus_tags)
            lines.append(f"Key focus tags: {focus}.")
        return "\n".join(lines)

    @staticmethod
    def _build_interpretant_paths(
        prompts: Sequence[str],
        fragments: Sequence[KnowledgeItem],
    ) -> List[str]:
        if not prompts:
            return ["Encourage the audience to explore personal associations freely."]

        fragment_titles = [item.title for item in fragments]
        results: List[str] = []
        for prompt in prompts:
            if fragment_titles:
                joined = ", ".join(fragment_titles)
                results.append(f"{prompt} (guided by fragments: {joined}).")
            else:
                results.append(f"{prompt} (requires speculative expansion beyond current fragments).")
        return results
