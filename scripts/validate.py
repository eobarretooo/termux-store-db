#!/usr/bin/env python3
"""Validate package metadata against the schema and repository rules."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError as exc:
    print("Missing dependency: jsonschema. Install with: python -m pip install jsonschema")
    raise SystemExit(1) from exc


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "package.schema.json"
CATEGORIES_PATH = ROOT / "categories" / "categories.json"
PACKAGES_DIR = ROOT / "packages"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def package_exists_in_termux(name: str) -> bool | None:
    if shutil.which("pkg") is None:
        return None

    result = subprocess.run(
        ["pkg", "show", name],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def validate_file(path: Path, schema: dict, categories: set[str]) -> list[str]:
    errors: list[str] = []

    try:
        data = load_json(path)
        jsonschema.validate(instance=data, schema=schema)
    except Exception as exc:
        return [f"{path}: schema error: {exc}"]

    if not isinstance(data, dict):
        return [f"{path}: package metadata must be an object"]

    if data["category"] not in categories:
        errors.append(f"{path}: unknown category {data['category']!r}")

    expected_install = f"pkg install {data['name']}"
    if not data["install_command"].startswith(expected_install):
        errors.append(
            f"{path}: install_command should usually start with {expected_install!r}"
        )

    for screenshot in data.get("screenshots", []):
        screenshot_path = ROOT / screenshot
        if not screenshot_path.is_file():
            errors.append(f"{path}: missing screenshot {screenshot}")

    exists = package_exists_in_termux(data["name"])
    if exists is False:
        errors.append(f"{path}: package not found by pkg show {data['name']!r}")

    return errors


def package_files(args: list[str]) -> list[Path]:
    if args:
        return [Path(arg) for arg in args]

    return [
        path
        for path in sorted(PACKAGES_DIR.glob("*.json"))
        if not path.name.startswith("_") and path.name != "index.json"
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", help="package JSON files to validate")
    args = parser.parse_args()

    schema = load_json(SCHEMA_PATH)
    categories = {item["id"] for item in load_json(CATEGORIES_PATH)}

    errors: list[str] = []
    seen: set[str] = set()

    for path in package_files(args.files):
        full_path = path if path.is_absolute() else ROOT / path
        data = load_json(full_path)
        name = data.get("name") if isinstance(data, dict) else None
        if name in seen:
            errors.append(f"{full_path}: duplicate package name {name!r}")
        if isinstance(name, str):
            seen.add(name)
        errors.extend(validate_file(full_path, schema, categories))

    if errors:
        for error in errors:
            print(error)
        return 1

    print("metadata validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
