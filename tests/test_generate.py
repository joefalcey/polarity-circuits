"""Tests for the controlled benchmark generator.

The critical property: every generated item's label must agree with the
symbolic engine's verdict.  If these ever disagree, the dataset is lying.
"""

from __future__ import annotations

from polarity_circuits.data.generate import build_tree, generate
from polarity_circuits.natlog import entails


def test_schema_present():
    items = generate(n=50, seed=7)
    assert len(items) == 50
    required = {
        "id",
        "premise",
        "hypothesis",
        "label",
        "template",
        "position",
        "local_polarity",
        "direction",
        "premise_terms",
        "hypothesis_terms",
        "premise_tree",
        "hypothesis_tree",
    }
    assert required <= set(items[0])


def test_roughly_balanced():
    items = generate(n=400, seed=3)
    positives = sum(i["label"] for i in items)
    assert 0.3 < positives / len(items) < 0.7


def test_all_positions_and_templates_covered():
    items = generate(n=400, seed=5)
    assert {i["template"] for i in items} == {"every", "no", "some", "not_every"}
    assert {i["position"] for i in items} == {"restrictor", "scope"}
    assert {i["direction"] for i in items} == {"generalise", "specialise"}


def test_labels_agree_with_engine():
    """The generated label must equal the engine's verdict, in both directions."""
    for item in generate(n=300, seed=11):
        (pr, ps) = item["premise_terms"]
        (hr, hs) = item["hypothesis_terms"]
        premise = build_tree(item["template"], pr, ps)
        hypothesis = build_tree(item["template"], hr, hs)
        engine_says = entails(premise, hypothesis)
        assert engine_says == bool(item["label"]), item


def test_local_polarity_matches_template():
    """every/not-every: restrictor DOWN, scope UP; no: both DOWN; some: both UP."""
    expected = {
        ("every", "restrictor"): "down",
        ("every", "scope"): "up",
        ("no", "restrictor"): "down",
        ("no", "scope"): "down",
        ("some", "restrictor"): "up",
        ("some", "scope"): "up",
        ("not_every", "restrictor"): "up",
        ("not_every", "scope"): "down",
    }
    for item in generate(n=400, seed=2):
        key = (item["template"], item["position"])
        assert item["local_polarity"] == expected[key], item
