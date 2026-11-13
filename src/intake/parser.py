"""Strict, dependency-free parsing of AI visual production briefs."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

_DIMENSIONS_RE = re.compile(r"^\s*(\d+)\s*[xX]\s*(\d+)\s*$")
DEFAULT_DIMENSIONS = "1024x1024"
DEFAULT_MAX_BATCH_SIZE = 50


def _positive_integer(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")
    return value


def _validate_dimensions(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string using positive WIDTHxHEIGHT dimensions")
    match = _DIMENSIONS_RE.fullmatch(value)
    if not match or int(match.group(1)) <= 0 or int(match.group(2)) <= 0:
        raise ValueError(f"{field_name} must use positive WIDTHxHEIGHT dimensions")
    return f"{int(match.group(1))}x{int(match.group(2))}"


def _validate_deliverable(deliverable: Any, index: int) -> None:
    prefix = f"deliverables[{index}]"
    if not isinstance(deliverable, dict):
        raise ValueError(f"{prefix} must be a JSON object")
    _positive_integer(deliverable.get("quantity", 1), f"{prefix}.quantity")
    _validate_dimensions(deliverable.get("dimensions", DEFAULT_DIMENSIONS),
                         f"{prefix}.dimensions")
    for key in ("type", "platform", "style", "description"):
        value = deliverable.get(key, "")
        if value is not None and not isinstance(value, str):
            raise ValueError(f"{prefix}.{key} must be a string")
    palette = deliverable.get("color_palette", [])
    if not isinstance(palette, list) or any(not isinstance(color, str) for color in palette):
        raise ValueError(f"{prefix}.color_palette must be a list of strings")


def _validate_brief_structure(brief: Any) -> dict[str, Any]:
    if not isinstance(brief, dict):
        raise ValueError("Brief must be a JSON object")
    for key in ("client", "project"):
        value = brief.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Brief field '{key}' must be a non-empty string")
    deliverables = brief.get("deliverables")
    if not isinstance(deliverables, list):
        raise ValueError("Brief field 'deliverables' must be a list")
    for index, deliverable in enumerate(deliverables):
        _validate_deliverable(deliverable, index)
    return brief


def load_brief(brief_path: str | Path) -> dict[str, Any]:
    """Load a UTF-8 JSON brief and validate its required structure and types."""
    path = Path(brief_path)
    if not path.is_file():
        raise FileNotFoundError(f"Brief not found: {path}")
    try:
        with path.open(encoding="utf-8") as handle:
            brief = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"Brief is not valid UTF-8: {path}") from exc
    return _validate_brief_structure(brief)


def extract_generation_params(brief: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert validated deliverables into normalized generation parameters."""
    _validate_brief_structure(brief)
    params = []
    for deliverable in brief["deliverables"]:
        params.append({
            "type": deliverable.get("type") or "generic",
            "platform": deliverable.get("platform") or "universal",
            "dimensions": _validate_dimensions(
                deliverable.get("dimensions", DEFAULT_DIMENSIONS), "dimensions"
            ),
            "quantity": deliverable.get("quantity", 1),
            "style": deliverable.get("style") or "",
            "description": deliverable.get("description") or "",
            "color_palette": deliverable.get("color_palette", []),
        })
    return params


def validate_brief(
    brief: dict[str, Any],
    *,
    max_batch_size: int = DEFAULT_MAX_BATCH_SIZE,
) -> list[str]:
    """Return actionable quality warnings for a structurally valid brief."""
    _validate_brief_structure(brief)
    _positive_integer(max_batch_size, "max_batch_size")
    warnings = []
    if not brief["deliverables"]:
        warnings.append("No deliverables specified")
    if not brief.get("brand_assets"):
        warnings.append("No brand assets provided — output may lack brand consistency")
    for index, deliverable in enumerate(brief["deliverables"], start=1):
        if not (deliverable.get("description") or "").strip():
            warnings.append(f"Deliverable {index} has no description")
        quantity = deliverable.get("quantity", 1)
        if quantity > max_batch_size:
            warnings.append(
                f"Deliverable {index} requests {quantity} assets — "
                f"consider batching at {max_batch_size} or fewer"
            )
    return warnings


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate and inspect a visual production brief.")
    parser.add_argument("brief", help="Path to a JSON client brief")
    args = parser.parse_args(argv)
    try:
        brief = load_brief(args.brief)
        warnings = validate_brief(brief)
        params = extract_generation_params(brief)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    print(f"Parsed {len(params)} deliverable(s)")
    for param in params:
        print(
            f"  {param['type']} ({param['platform']}) — "
            f"{param['quantity']}x at {param['dimensions']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
