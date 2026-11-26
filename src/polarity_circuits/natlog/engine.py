"""A minimal natural-logic engine for monotonicity.

Scope of this fragment
----------------------
Quantified sentences (every / no / some / few), sentential negation, and
conditionals.  Lexical entailment is hypernymy only.  That is enough to
generate a controlled benchmark and to compute the ground-truth polarity tree
of every item -- which is the point: the symbolic computation is *known by
construction*, unlike on naturally occurring NLI data.

Not implemented (on purpose, for v1): relative clauses, coordination,
quantifier scope ambiguity, comparatives, presupposition, antonyms.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .types import Node, Polarity

# Monotonicity signature of each quantifier *in a positive context*:
# (restrictor, scope).  DOWN means the argument is downward entailing.
QUANT_SIGNATURES: dict[str, tuple[Polarity, Polarity]] = {
    "every": (Polarity.DOWN, Polarity.UP),
    "no": (Polarity.DOWN, Polarity.DOWN),
    "some": (Polarity.UP, Polarity.UP),
    "few": (Polarity.DOWN, Polarity.DOWN),
}

# A deliberately tiny lexicon: child -> direct hypernyms, split by sort so that
# generated sentences stay well-formed (a noun goes in the restrictor, an
# adjective in the scope).
NOUN_LEXICON: dict[str, set[str]] = {
    "dog": {"animal"},
    "cat": {"animal"},
    "animal": {"entity"},
}

ADJECTIVE_LEXICON: dict[str, set[str]] = {
    "brown": {"colored"},
    "red": {"colored"},
    "colored": {"visible"},
}

# Merged view for the entailment checker (keys do not collide).
DEFAULT_LEXICON: dict[str, set[str]] = {**NOUN_LEXICON, **ADJECTIVE_LEXICON}


def combine(context: Polarity, signature: Polarity) -> Polarity:
    """Effective polarity of an argument, given the context it sits in."""
    return context.flip() if signature is Polarity.DOWN else context


def assign_polarity(node: Node, context: Polarity = Polarity.UP) -> Node:
    """Annotate every node with its polarity. Returns the same tree (mutated)."""
    node.polarity = context
    if node.kind == "quant":
        restrictor_sig, scope_sig = QUANT_SIGNATURES[node.name]  # type: ignore[index]
        assign_polarity(node.children[0], combine(context, restrictor_sig))
        assign_polarity(node.children[1], combine(context, scope_sig))
    elif node.kind == "not":
        assign_polarity(node.children[0], context.flip())
    elif node.kind == "if":
        assign_polarity(node.children[0], context.flip())  # antecedent is DE
        assign_polarity(node.children[1], context)
    return node


def quant_node(node: Node) -> Node:
    """Descend through outer negations to the first quantifier."""
    while node.kind == "not":
        node = node.children[0]
    return node


def slot(node: Node, position: str) -> Node:
    """Return the restrictor or scope node of the (outermost) quantifier."""
    q = quant_node(node)
    if position == "restrictor":
        return q.children[0]
    if position == "scope":
        return q.children[1]
    raise ValueError(f"unknown position: {position!r}")


# ---------------------------------------------------------------------------
# Lexical entailment
# ---------------------------------------------------------------------------


def hypernyms(term: str, lexicon: Mapping[str, Sequence[str]]) -> set[str]:
    """Transitive closure of the hypernym relation."""
    seen: set[str] = set()
    stack = list(lexicon.get(term, ()))
    while stack:
        t = stack.pop()
        if t in seen:
            continue
        seen.add(t)
        stack.extend(lexicon.get(t, ()))
    return seen


def lex_entails(a: str, b: str, lexicon: Mapping[str, Sequence[str]]) -> bool:
    """Does `a` entail `b` lexically (i.e. is a a hyponym of, or equal to, b)?"""
    return a == b or b in hypernyms(a, lexicon)


# ---------------------------------------------------------------------------
# Entailment checking
# ---------------------------------------------------------------------------


def entails(
    premise: Node,
    hypothesis: Node,
    lexicon: Mapping[str, Sequence[str]] | None = None,
) -> bool:
    """Gold-label check: does `premise` entail `hypothesis` in this fragment?

    The rule is the natural-logic one.  At an upward-entailing position we may
    generalise (premise term is the narrower one); at a downward-entailing
    position we may only specialise.
    """
    lex = DEFAULT_LEXICON if lexicon is None else lexicon
    assign_polarity(premise)
    return _check(premise, hypothesis, Polarity.UP, lex)


def _check(
    p: Node,
    h: Node,
    context: Polarity,
    lexicon: Mapping[str, Sequence[str]],
) -> bool:
    if p.kind != h.kind:
        return False

    if p.kind == "pred":
        assert p.name is not None and h.name is not None
        if context is Polarity.UP:
            return lex_entails(p.name, h.name, lexicon)
        return lex_entails(h.name, p.name, lexicon)

    if p.kind == "quant":
        if p.name != h.name:
            return False
        restrictor_sig, scope_sig = QUANT_SIGNATURES[p.name]  # type: ignore[index]
        return _check(p.children[0], h.children[0], combine(context, restrictor_sig), lexicon) and _check(
            p.children[1], h.children[1], combine(context, scope_sig), lexicon
        )

    if p.kind == "not":
        return _check(p.children[0], h.children[0], context.flip(), lexicon)

    if p.kind == "if":
        return _check(p.children[0], h.children[0], context.flip(), lexicon) and _check(
            p.children[1], h.children[1], context, lexicon
        )

    raise ValueError(f"unsupported node kind: {p.kind!r}")


def pretty(node: Node) -> str:
    """Render a tree with polarity markers, e.g. every(dog↓, brown↑)."""
    if node.kind == "pred":
        return f"{node.name}{node.polarity or ''}"
    if node.kind == "quant":
        return f"{node.name}({pretty(node.children[0])}, {pretty(node.children[1])})"
    if node.kind == "not":
        return f"not({pretty(node.children[0])})"
    if node.kind == "if":
        return f"if({pretty(node.children[0])}, {pretty(node.children[1])})"
    return f"<{node.kind}>"
