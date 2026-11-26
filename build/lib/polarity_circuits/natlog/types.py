"""Core types for the natural-logic fragment.

Deliberately dependency-free (no torch, no numpy) so this subpackage can be
installed and used on its own.  Keep it that way: the engine is meant to be a
small, trustworthy, importable tool, not a research script.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Polarity(Enum):
    """Entailment direction of a context."""

    UP = "up"  # upward entailing
    DOWN = "down"  # downward entailing

    def flip(self) -> "Polarity":
        return Polarity.DOWN if self is Polarity.UP else Polarity.UP

    def __str__(self) -> str:  # nicer diagrams
        return "\u2191" if self is Polarity.UP else "\u2193"


@dataclass
class Node:
    """A node in a tiny formal language.

    kind is one of: "pred", "quant", "not", "if".
    `polarity` is filled in by assign_polarity() and is for inspection only;
    the entailment checker recomputes direction contextually.
    """

    kind: str
    name: str | None = None
    children: list["Node"] = field(default_factory=list)
    polarity: Polarity | None = None

    # -- convenience constructors -------------------------------------------
    @staticmethod
    def pred(name: str) -> "Node":
        return Node("pred", name)

    @staticmethod
    def quant(name: str, restrictor: "Node", scope: "Node") -> "Node":
        return Node("quant", name, [restrictor, scope])

    @staticmethod
    def neg(child: "Node") -> "Node":
        return Node("not", None, [child])

    @staticmethod
    def if_(antecedent: "Node", consequent: "Node") -> "Node":
        return Node("if", None, [antecedent, consequent])

    def __str__(self) -> str:
        return _render(self)


def _render(node: Node) -> str:
    if node.kind == "pred":
        return node.name or "?"
    if node.kind == "quant":
        return f"{node.name}({_render(node.children[0])}, {_render(node.children[1])})"
    if node.kind == "not":
        return f"not({_render(node.children[0])})"
    if node.kind == "if":
        return f"if({_render(node.children[0])}, {_render(node.children[1])})"
    return f"<{node.kind}>"
