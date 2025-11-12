# Art2 – Semiotic Logic Art Concept Toolkit

Art2 provides a configurable pipeline for transforming philosophical, sociological,
and aesthetic knowledge fragments into actionable contemporary-art concepts. The
system implements the formula

```
A = ⟦◇(Sₒ ∧ Rᴹ) → Iᴱᴿ⟧ + Tropes(m, s, e) + Ψ(Eσ) · ∂t
```

by combining modular knowledge sources, semiotic reasoning, and affective
sequencing. Users can plug in different knowledge bases, adjust rhetorical
presets, and export structured concept dossiers.

## Features

- **Pluggable knowledge bases** – load JSON vector-like knowledge fragments and
  filter them by query, tags, or both.
- **Formula-aware generator** – wrap the modal/semiotic/interpretant/trope/time
  dimensions into a coherent art concept.
- **Config-driven pipeline** – describe projects declaratively and reuse across
  research sessions.
- **Markdown export** – output ready-to-share concept briefs.

## Quickstart

1. Ensure Python 3.10+ is available.
2. Create a virtual environment and install the project in editable mode (no
   third-party dependencies are required).
3. Prepare a knowledge base JSON file following the structure in
   `data/sample_knowledge.json`.
4. Author a configuration file similar to `data/sample_config.json`.
5. Run the CLI:

```bash
PYTHONPATH=src python -m art2.cli data/sample_config.json --knowledge-root data --output concept.md
```

The generated `concept.md` file contains a fully structured concept document
covering modal hypotheses, semiotic binding, interpretant paths, tropes across
morphology/structure/experience, and an affective timeline.

## Configuration Schema

The configuration file is standard JSON with the following keys:

| Key | Description |
| --- | ----------- |
| `query` | Title and primary search term for the concept. |
| `modal_prefix` | Text appended to the modal operator `◇`. |
| `semiotic_focus` | List of tags to filter knowledge fragments. |
| `interpretant_prompts` | Narrative prompts for recursive interpretant chains. |
| `tropes` | Object with `morphology`, `structure`, `experience` lists describing rhetorical levers. |
| `affective_beats` | Ordered list capturing the Ψ(Eσ) · ∂t emotional curve. |
| `references` | Optional bibliography strings to append. |
| `knowledge_file` | JSON file containing the knowledge fragments (relative to `--knowledge-root`). |
| `knowledge_limit` | Maximum number of fragments to merge. |

## Extending the System

- Implement new subclasses of `KnowledgeBase` to source data from APIs,
  databases, or embedding services.
- Derive custom pipelines if you need to post-process concepts or integrate with
  creative coding environments.
- Feed the generated Markdown into presentation tools, installation briefs, or
  grant proposals.

## License

MIT License.
