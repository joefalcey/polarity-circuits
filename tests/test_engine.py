"""Golden tests for the natural-logic fragment.

These are the tests that make the engine trustworthy.  Add a case every time
you discover a bug or a counterexample -- the file is also a record of the
fragment's intended scope.
"""

from __future__ import annotations

import pytest

from polarity_circuits.natlog import (
    Node,
    Polarity,
    assign_polarity,
    entails,
    lex_entails,
    pretty,
)
from polarity_circuits.natlog.engine import DEFAULT_LEXICON


def Q(name: str, r: str, s: str) -> Node:
    return Node.quant(name, Node.pred(r), Node.pred(s))


# -- polarity assignment ----------------------------------------------------


def test_restrictor_down_scope_up():
    tree = assign_polarity(Q("every", "dog", "brown"))
    assert tree.children[0].polarity is Polarity.DOWN
    assert tree.children[1].polarity is Polarity.UP


def test_no_is_downward_in_both_arguments():
    tree = assign_polarity(Q("no", "dog", "brown"))
    assert tree.children[0].polarity is Polarity.DOWN
    assert tree.children[1].polarity is Polarity.DOWN


def test_negation_flips():
    tree = assign_polarity(Node.neg(Q("every", "dog", "brown")))
    quant = tree.children[0]
    assert quant.children[0].polarity is Polarity.UP
    assert quant.children[1].polarity is Polarity.DOWN


def test_pretty_renders_markers():
    tree = assign_polarity(Q("every", "dog", "brown"))
    assert pretty(tree) == "every(dog\u2193, brown\u2191)"


# -- entailment -------------------------------------------------------------


def test_restrictor_downward_entailing():
    # Every animal is brown |= Every dog is brown  (specialise in DE restrictor)
    assert entails(Q("every", "animal", "brown"), Q("every", "dog", "brown"))


def test_restrictor_wrong_direction_fails():
    # Every dog is brown |/= Every animal is brown
    assert not entails(Q("every", "dog", "brown"), Q("every", "animal", "brown"))


def test_scope_upward_entailing():
    # Every dog is brown |= Every dog is colored  (generalise in UE scope)
    assert entails(Q("every", "dog", "brown"), Q("every", "dog", "colored"))


def test_negation_flips_restrictor():
    # Not every dog is brown |= Not every animal is brown
    assert entails(
        Node.neg(Q("every", "dog", "brown")),
        Node.neg(Q("every", "animal", "brown")),
    )


def test_no_scope_downward():
    # No dog is colored |= No dog is brown
    assert entails(Q("no", "dog", "colored"), Q("no", "dog", "brown"))


def test_some_is_upward_in_restrictor():
    # Some dog is brown |= Some animal is brown
    assert entails(Q("some", "dog", "brown"), Q("some", "animal", "brown"))


def test_hypernym_transitivity():
    # dog -> animal -> entity
    assert lex_entails("dog", "entity", DEFAULT_LEXICON)
    assert entails(Q("every", "entity", "brown"), Q("every", "dog", "brown"))


def test_quantifier_mismatch_fails():
    assert not entails(Q("every", "dog", "brown"), Q("some", "dog", "brown"))


def test_identical_is_entailment():
    assert entails(Q("every", "dog", "brown"), Q("every", "dog", "brown"))


def test_unsupported_kind_raises():
    with pytest.raises(ValueError):
        entails(Node("mystery"), Node("mystery"))
