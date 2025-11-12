"""Command line interface for generating art concepts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .pipeline import GenerationPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate art concepts using semiotic logic.")
    parser.add_argument("config", type=Path, help="Path to a JSON configuration file.")
    parser.add_argument(
        "--knowledge-root",
        type=Path,
        default=Path("."),
        help="Directory containing knowledge base files referenced by the config.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write the generated concept markdown.",
    )
    return parser


def load_config(path: Path) -> Any:
    return json.loads(path.read_text())


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    payload = load_config(args.config)
    pipeline = GenerationPipeline.from_dict(payload, args.knowledge_root)
    concept = pipeline.run()

    document = concept.as_markdown()
    if args.output:
        args.output.write_text(document)
    else:
        print(document)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
