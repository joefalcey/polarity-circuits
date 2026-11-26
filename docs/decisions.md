# Decisions (ADR log)

One entry per decision that would be expensive to reverse. Format: context,
decision, consequences. Append-only; supersede rather than delete.

---

## ADR-001 — Monotonicity first, not negation or scope

**Context.** Three candidate formal-semantic phenomena were on the table.
Monotonicity has the cleanest formalism (a total function from position to
polarity), the most established benchmark lineage (FLog, MED), and the least
ambiguity about what the "correct" symbolic computation is.

**Decision.** v1 covers monotonicity only.

**Consequences.** Fast to a defensible result. Negation and scope become
extensions rather than rewrites, because the method (controlled derivation ->
behaviour -> causal abstraction) is phenomenon-agnostic. Risk: a reviewer may
say monotonicity is a narrow slice of semantics; answer with the method framing
and point to the planned extensions.

---

## ADR-002 — Synthetic controlled data before natural data

**Context.** FLog/MED offer realism; the controlled generator offers known
derivations. Causal abstraction needs a target variable with a gold value.

**Decision.** Build the controlled set first, use FLog/MED for external validity
only.

**Consequences.** Reviewers may question ecological validity, so the FLog/MED
results are not optional. Mitigation: report both, and be explicit that the
controlled set is an instrument, not a claim about natural language.

---

## ADR-003 — `natlog/` stays torch-free

**Context.** The engine is the reusable artifact; the experiments are the paper.

**Decision.** No torch/numpy imports under `natlog/`, enforced by a test.

**Consequences.** The engine can be installed and cited independently, which is
the cheapest route to citations. Slight duplication cost when the experiments
want batched operations.
