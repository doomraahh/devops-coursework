import random

from ab_logic import VARIANTS, pick_variant


def test_pick_variant_returns_known_variant():
    variant = pick_variant()
    assert variant.name in VARIANTS


def test_pick_variant_is_deterministic_with_seeded_rng():
    rng = random.Random(42)
    variant = pick_variant(rng)
    assert variant.name in {"A", "B"}


def test_variants_have_distinct_button_text():
    assert VARIANTS["A"].button_text != VARIANTS["B"].button_text
