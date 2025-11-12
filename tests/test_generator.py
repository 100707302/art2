from art2 import (
    KnowledgeBase,
    ArtConceptGenerator,
    GenerationParameters,
    TropesLibrary,
    AffectiveEvent,
    AffectiveTimeline,
)


def test_generate_concept(tmp_path):
    kb = KnowledgeBase.from_json("data/knowledge_base.json")
    generator = ArtConceptGenerator(kb)
    params = GenerationParameters(
        semiotic_object="weathered memory",
        representamen=("fog chamber", "choral score"),
        possible_world="Cities dream of their citizens",
        interpretant_focus=("collective memory",),
        tropes=TropesLibrary().recommend(),
        affective_timeline=AffectiveTimeline(
            [
                AffectiveEvent("approach", 0.3, 0.0, ("diffused light",)),
                AffectiveEvent("immersion", 0.8, 0.5, ("voice", "moisture")),
            ]
        ),
    )

    result = generator.generate(params)

    assert "formula" in result
    assert result["knowledge_sources"], "Expected knowledge selections"
    assert result["tropes"]["morphology"], "Expected morphology tropes"
    assert result["affective_timeline"], "Expected affective timeline entries"

