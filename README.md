# art2

A lightweight toolkit for generating conceptual art scaffolds based on the formula:

```
A = ⟨◇(Sₒ ∧ Rᴹ) → Iᴱᴿ⟩ + Tropes(m, s, e) + Ψ(Eσ) · ∂t
```

The package lets you combine a small, vectorised knowledge base with adjustable rhetorical and affective parameters so that artists — even newcomers — can rapidly prototype rich, theory-grounded concepts.

## Installation

The toolkit has no external dependencies and runs on Python 3.10+.

```
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

(Editable install is optional; you can also run the CLI via `python -m art2.cli …`.)

## Usage

1. Prepare or extend the JSON knowledge base (`data/knowledge_base.json`). Each item needs an `id`, `discipline`, `concept`, `summary`, and optional `keywords` array.
2. Invoke the CLI with a semiotic object, a possible world statement, and at least one representamen.

Example:

```
python -m art2.cli "temporal commons" "If memory condensed into weather" light-installation soundscape --knowledge data/knowledge_base.json --interpretant "collective ritual" --bias philosophy:1.3 sociology:1.1 --affect "arrival|0.4|0.0|haze" "recognition|0.9|0.5|choral hum" "release|0.6|1.0|temperature drop"
```

The CLI outputs a JSON blueprint containing:

- the modal-semiotic formula populated with your inputs
- the knowledge entries selected through TF-IDF retrieval (with optional discipline bias)
- trope recommendations across morphology/structure/experience
- a normalised affective timeline, if provided

Pass `--output path.json` to save the blueprint to a file.

## Library API

```python
from art2 import (
    KnowledgeBase,
    ArtConceptGenerator,
    GenerationParameters,
    TropesLibrary,
    AffectiveEvent,
    AffectiveTimeline,
)

knowledge = KnowledgeBase.from_json("data/knowledge_base.json")

generator = ArtConceptGenerator(knowledge)
params = GenerationParameters(
    semiotic_object="urban lullabies",
    representamen=("projection", "participatory choir"),
    possible_world="Cities breathe with the tempo of sleepers",
    interpretant_focus=("collective rest",),
    tropes=TropesLibrary().recommend(),
    affective_timeline=AffectiveTimeline(
        [
            AffectiveEvent("soft entry", 0.2, 0.0, ("dim light",)),
            AffectiveEvent("shared resonance", 0.9, 0.6, ("vocal harmony", "vibration")),
            AffectiveEvent("afterglow", 0.5, 1.0, ("warm air",)),
        ]
    ),
)

concept = generator.generate(params)
```

## Extending the knowledge base

Use the `KnowledgeBase.to_json` method or edit the JSON manually. The retrieval logic is intentionally lightweight so that you can swap in your own embeddings or connect to external vector stores.

## License

MIT
