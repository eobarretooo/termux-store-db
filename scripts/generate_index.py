#!/usr/bin/env python3
"""Generate packages/index.json from per-package metadata files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES_DIR = ROOT / "packages"
OUTPUT = PACKAGES_DIR / "index.json"


def build_index() -> list[dict]:
    index: list[dict] = []
    seen: set[str] = set()

    for path in sorted(PACKAGES_DIR.glob("*.json")):
        if path.name.startswith("_") or path.name == "index.json":
            continue

        data = json.loads(path.read_text(encoding="utf-8"))
        name = data["name"]
        if name in seen:
            raise ValueError(f"duplicate package metadata: {name}")
        seen.add(name)

        index.append(
            {
                "name": name,
                "category": data["category"],
                "short_description": data["short_description"],
                "gui": data["gui"],
                "x11_required": data["x11_required"],
                "rating": data.get(
                    "community_rating",
                    {"works_great": 0, "unstable": 0, "broken": 0},
                ),
            }
        )

    return index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if packages/index.json is not up to date",
    )
    args = parser.parse_args()

    generated = json.dumps(build_index(), indent=2, ensure_ascii=False) + "\n"

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != generated:
            print("packages/index.json is out of date. Run scripts/generate_index.py")
            return 1
        print("packages/index.json is up to date")
        return 0

    OUTPUT.write_text(generated, encoding="utf-8")
    print(f"generated {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
