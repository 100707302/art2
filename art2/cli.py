"""Command line interface for generating art concepts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .emotion import AffectiveEvent, AffectiveTimeline
from .generator import ArtConceptGenerator, GenerationParameters
from .knowledge import KnowledgeBase
from .tropes import TropesLibrary, TropesProfile


def _load_knowledge(path: Path | None) -> KnowledgeBase:
    if path and path.exists():
        return KnowledgeBase.from_json(path)
    raise FileNotFoundError("Knowledge base file not found. Use --knowledge to specify a JSON file.")


def _parse_representamen(values: Sequence[str]) -> Sequence[str]:
    if not values:
        raise ValueError("At least one representamen (medium/form) must be provided")
    return values


def _parse_tropes(args: argparse.Namespace, library: TropesLibrary) -> TropesProfile:
    if args.tropes == "auto":
        return library.recommend()
    morphology = args.tropes_morphology or ()
    structure = args.tropes_structure or ()
    experience = args.tropes_experience or ()
    return TropesProfile(morphology=morphology, structure=structure, experience=experience)


def _parse_affective(args: argparse.Namespace) -> AffectiveTimeline | None:
    events: list[AffectiveEvent] = []
    for payload in args.affect or ():
        label, intensity, timestamp, *modalities = payload.split("|")
        events.append(
            AffectiveEvent(
                label=label,
                intensity=float(intensity),
                timestamp=float(timestamp),
                modalities=tuple(modalities),
            )
        )
    if not events:
        return None
    timeline = AffectiveTimeline(events)
    timeline.normalize()
    return timeline


def _parse_bias(pairs: Sequence[str]) -> dict[str, float]:
    bias: dict[str, float] = {}
    for pair in pairs:
        discipline, value = pair.split(":")
        bias[discipline] = float(value)
    return bias


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an art concept scaffold from a knowledge base")
    parser.add_argument("semiotic_object", help="Core concept or object for the work")
    parser.add_argument("possible_world", help="Statement describing the possible world scenario")
    parser.add_argument(
        "representamen",
        nargs="+",
        help="Representational forms/mediums that will embody the concept",
    )
    parser.add_argument(
        "--knowledge",
        type=Path,
        required=True,
        help="Path to a JSON knowledge base file",
    )
    parser.add_argument(
        "--interpretant",
        nargs="*",
        default=(),
        help="Specific interpretant prompts to privilege",
    )
    parser.add_argument(
        "--knowledge-prompt",
        help="Override the search prompt used for knowledge retrieval",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=4,
        help="Number of knowledge entries to retrieve",
    )
    parser.add_argument(
        "--bias",
        nargs="*",
        default=(),
        help="Discipline bias in the form discipline:value",
    )
    parser.add_argument(
        "--tropes",
        choices=["auto", "manual"],
        default="auto",
        help="Automatically load trope suggestions or configure manually",
    )
    parser.add_argument("--tropes-morphology", nargs="*")
    parser.add_argument("--tropes-structure", nargs="*")
    parser.add_argument("--tropes-experience", nargs="*")
    parser.add_argument(
        "--affect",
        nargs="*",
        metavar="LABEL|INTENSITY|TIME|MODALITY…",
        help="Define affective timeline events",
    )
    parser.add_argument("--output", type=Path, help="Optional output file to write JSON results")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    knowledge = _load_knowledge(args.knowledge)
    representamen = _parse_representamen(args.representamen)
    tropes_profile = _parse_tropes(args, TropesLibrary())
    affective_timeline = _parse_affective(args)
    bias = _parse_bias(args.bias)

    generator = ArtConceptGenerator(knowledge)
    params = GenerationParameters(
        semiotic_object=args.semiotic_object,
        representamen=representamen,
        possible_world=args.possible_world,
        interpretant_focus=args.interpretant,
        discipline_bias=bias or None,
        tropes=tropes_profile,
        affective_timeline=affective_timeline,
        knowledge_prompt=args.knowledge_prompt,
        knowledge_top_k=args.top_k,
    )

    result = generator.generate(params)
    output_text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(output_text, encoding="utf-8")
    else:
        print(output_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

