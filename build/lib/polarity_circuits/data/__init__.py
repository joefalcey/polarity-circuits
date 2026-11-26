"""Data: controlled benchmark generation and loaders for external NLI sets.

Planned loaders (v1):
  - FLog  (Yanaka et al. 2019) -- monotonicity inference
  - MED   (Yanaka et al. 2020) -- monotonicity entailment
  - FraCaS (Cooper et al. 1996) -- classic semantic suite
Keep each loader in its own module and normalise to the schema in generate.py.
"""
