"""Controlled monotonicity benchmark generator.

Every item carries the polarity tree that *licenses its label*.  That is the
whole point: on naturally occurring NLI data nobody knows what the correct
symbolic computation is, so causal abstraction has nothing clean to align to.
Here we build the derivation first and the sentence second, so the ground
truth is exact by construction.

Item schema (JSONL)
-------------------
id, premise, hypothesis, label (0/1), template, position, local_polarity,
direction ("generalise" | "specialise"), premise_terms, hypothesis_terms,
premise_tree, hypothesis_tree

Difficulty knobs to implement next (see docs/research_notes.md):
  - nesting depth of sentential embedding
  - distractor clauses
  - lexical overlap between premise and hypothesis
  - surface-order perturbation
"""

from __future__ import annotations

import random
from typing import Any

from ..natlog import (
    ADJECTIVE_LEXICON,
    NOUN_LEXICON,
    Node,
    Polarity,
    assign_polarity,
    pretty,
    slot,
)

TEMPLATE_TEXT: dict[str, str] = {
    "every": "Every {r} is {s}.",
    "no": "No {r} is {s}.",
    "some": "Some {r} is {s}.",
    "not_every": "It is not the case that every {r} is {s}.",
}

QUANT_OF: dict[str, str] = {
    "every": "every",
    "no": "no",
    "some": "some",
    "not_every": "every",
}

# Which slot a lexical substitution may target.
SORTS: dict[str, dict[str, set[str]]] = {
    "restrictor": NOUN_LEXICON,  # nouns
    "scope": ADJECTIVE_LEXICON,  # adjectives
}


def build_tree(template: str, restrictor: str, scope: str) -> Node:
    q = Node.quant(QUANT_OF[template], Node.pred(restrictor), Node.pred(scope))
    if template == "not_every":
        return Node.neg(q)
    return q


def render(template: str, restrictor: str, scope: str) -> str:
    return TEMPLATE_TEXT[template].format(r=restrictor, s=scope)


def _edges(lexicon: dict[str, set[str]]) -> list[tuple[str, str]]:
    """(hyponym, hypernym) pairs from the lexicon, one level deep."""
    return [(child, parent) for child, parents in lexicon.items() for parent in parents]


def generate(
    n: int = 400,
    seed: int = 13,
    templates: tuple[str, ...] = ("every", "no", "some", "not_every"),
    positions: tuple[str, ...] = ("restrictor", "scope"),
) -> list[dict[str, Any]]:
    """Generate a balanced set of monotonicity items with exact gold labels."""
    rng = random.Random(seed)

    edges_by_position = {pos: _edges(lex) for pos, lex in SORTS.items()}
    for pos, edges in edges_by_position.items():
        if not edges:
            raise ValueError(f"lexicon for {pos!r} has no hypernym edges")

    # A filler for the slot we are NOT substituting, drawn from the other sort.
    fillers = {
        "restrictor": sorted({w for e in edges_by_position["restrictor"] for w in e}),
        "scope": sorted({w for e in edges_by_position["scope"] for w in e}),
    }

    items: list[dict[str, Any]] = []
    for i in range(n):
        template = rng.choice(templates)
        position = rng.choice(positions)
        other = "scope" if position == "restrictor" else "restrictor"

        narrower, broader = rng.choice(edges_by_position[position])
        filler = rng.choice(fillers[other])

        # Which direction is logically licensed at this slot?
        #   UP  -> may generalise (narrow premise, broad hypothesis)
        #   DOWN-> may only specialise (broad premise, narrow hypothesis)
        probe = build_tree(template, narrower, narrower)
        local_pol = slot(assign_polarity(probe), position).polarity
        assert local_pol is not None
        generalising_is_valid = local_pol is Polarity.UP

        want_positive = rng.random() < 0.5
        generalise = generalising_is_valid if want_positive else not generalising_is_valid
        direction = "generalise" if generalise else "specialise"

        if generalise:
            premise_term, hypothesis_term = narrower, broader
        else:
            premise_term, hypothesis_term = broader, narrower

        # Only the selected slot is substituted; the other is held constant.
        r = premise_term if position == "restrictor" else filler
        s = premise_term if position == "scope" else filler
        h_r = hypothesis_term if position == "restrictor" else r
        h_s = hypothesis_term if position == "scope" else s

        items.append(
            {
                "id": f"ctrl-{i:05d}",
                "premise": render(template, r, s),
                "hypothesis": render(template, h_r, h_s),
                "label": 1 if generalise == generalising_is_valid else 0,
                "template": template,
                "position": position,
                "local_polarity": local_pol.value,
                "direction": direction,
                "premise_terms": [r, s],
                "hypothesis_terms": [h_r, h_s],
                "premise_tree": pretty(assign_polarity(build_tree(template, r, s))),
                "hypothesis_tree": pretty(build_tree(template, h_r, h_s)),
            }
        )

    rng.shuffle(items)
    return items
