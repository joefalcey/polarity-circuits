# Research notes — gap memo (write this BEFORE building)

Fill this in during week 0. One page. Its job is to stop you from rebuilding
something that already exists, and to give you the exact sentence that states
your contribution. Revisit it at the end of every week.

## 1. The claim, in one sentence

> We show that [model family] [does / does not] implement the monotonicity
> calculus, by aligning the symbolic polarity variable with an internal
> representation using interchange interventions on a benchmark whose
> derivations are known by construction.

## 2. What already exists (literature scan)

| Work | What it does | Why it is not this project |
| --- | --- | --- |
| MacCartney & Manning 2009 | natural logic formalism | symbolic only |
| Yanaka et al. 2019 (FLog) | monotonicity benchmark; models fail systematically | behavioural, natural data, no internal analysis |
| Yanaka et al. 2020 (MED) | monotonicity entailment data | as above |
| Geiger et al. 2025 | causal abstraction framework | general; few semantic case studies |
| Wu et al. 2024 (pyvene) | intervention tooling | infrastructure |
| Prove What You Can (2026) | neuro-symbolic NLI pipeline | builds a better system; does not test internal implementation |

Search terms that matter: `monotonicity probing`, `natural logic interpretability`,
`causal abstraction semantics`, `polarity circuit`, `downward entailing neuron`.
Also check the citations *of* FLog/MED — anyone doing internals will cite them.

## 3. The gap

<!-- one paragraph. be specific about what nobody has done. -->

## 4. What would falsify the claim

- Abstraction found at some layers but not others -> boundary condition (still a result).
- No abstraction anywhere, but behavioural success -> the model uses a non-monotonic heuristic. This is the *interesting* outcome.
- Abstraction and behaviour both absent -> the benchmark is too hard; fix difficulty before concluding.

## 5. Decision log for week 0

- [ ] Confirm FLog / MED licences and download routes.
- [ ] Confirm which small models have published SAEs (Gemma Scope covers Gemma-2-2b).
- [ ] Confirm compute: local GPU? IMS cluster? Colab Pro?
- [ ] Email one person whose work this extends, before building. Ask one question.

## 6. Lab notebook (append-only)

| Date | Tried | Expected | Observed | Next |
| --- | --- | --- | --- | --- |
| | | | | |
