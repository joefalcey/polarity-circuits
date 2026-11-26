"""Command line entry point.

    polarity-circuits generate --out data/controlled --n 500
    polarity-circuits score    --config configs/controlled.yaml
    polarity-circuits patch    --config configs/controlled.yaml
    polarity-circuits figures
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def cmd_generate(args: argparse.Namespace) -> None:
    from .data.generate import generate

    items = generate(n=args.n, seed=args.seed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "controlled.jsonl"
    with path.open("w", encoding="utf-8") as fh:
        for item in items:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")
    n_pos = sum(i["label"] for i in items)
    print(f"wrote {len(items)} items ({n_pos} positive) -> {path}")


def _not_implemented(name: str) -> None:
    raise SystemExit(
        f"`{name}` is not implemented yet.\n"
        "Next step is the behavioural scoring pass; see docs/research_notes.md."
    )


def cmd_score(args: argparse.Namespace) -> None:
    _not_implemented("score")


def cmd_patch(args: argparse.Namespace) -> None:
    _not_implemented("patch")


def cmd_figures(args: argparse.Namespace) -> None:
    _not_implemented("figures")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="polarity-circuits")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="write the controlled benchmark")
    gen.add_argument("--out", default="data/controlled")
    gen.add_argument("--n", type=int, default=400)
    gen.add_argument("--seed", type=int, default=13)
    gen.set_defaults(func=cmd_generate)

    for name, fn, help_text in (
        ("score", cmd_score, "score models on the benchmark"),
        ("patch", cmd_patch, "run activation patching"),
        ("figures", cmd_figures, "build paper figures"),
    ):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--config", default="configs/controlled.yaml")
        p.set_defaults(func=fn)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
