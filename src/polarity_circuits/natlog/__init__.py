"""Dependency-free natural-logic fragment for monotonicity."""

from .engine import (
    ADJECTIVE_LEXICON,
    DEFAULT_LEXICON,
    NOUN_LEXICON,
    QUANT_SIGNATURES,
    assign_polarity,
    combine,
    entails,
    hypernyms,
    lex_entails,
    pretty,
    quant_node,
    slot,
)
from .types import Node, Polarity

__all__ = [
    "ADJECTIVE_LEXICON",
    "DEFAULT_LEXICON",
    "NOUN_LEXICON",
    "QUANT_SIGNATURES",
    "Node",
    "Polarity",
    "assign_polarity",
    "combine",
    "entails",
    "hypernyms",
    "lex_entails",
    "pretty",
    "quant_node",
    "slot",
]
