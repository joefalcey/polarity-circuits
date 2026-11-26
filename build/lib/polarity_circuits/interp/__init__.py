"""Interpretability: interventions, causal abstraction, probes.

Planned modules (v1):
  patch.py   activation patching / noising on the controlled set (robust first step)
  das.py     distributed alignment search via pyvene, aligning the polarity variable
  probes.py  linear vs KAN probes for the same variable (matched parameter counts)

Design rule: everything here may import torch; natlog/ must not.
"""
