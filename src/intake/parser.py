"""Brief parser — converts client briefs into structured generation parameters."""
import json
from pathlib import Path


def load_brief(brief_path: str) -> dict:
    """Load and validate a client brief from JSON."""
    path = Path(brief_path)
    if not path.exists():
        raise FileNotFoundError(f"Brief not found: {brief_path}")

    with open(path) as f:
        brief = json.load(f)

    required = ["client", "project", "deliverables"]
    missing = [k for k in required if k not in brief]
    if missing:
        raise ValueError(f"Brief missing required fields: {missing}")

    return brief


def extract_generation_params(brief: dict) -> list[dict]:
    """Extract generation parameters from each deliverable in a brief."""
    params = []
    for deliverable in brief.get("deliverables", []):
        param = {
            "type": deliverable.get("type", "generic"),
            "platform": deliverable.get("platform", "universal"),
            "dimensions": deliverable.get("dimensions", "1024x1024"),
            "quantity": deliverable.get("quantity", 1),
            "style": deliverable.get("style", ""),
            "description": deliverable.get("description", ""),
            "color_palette": deliverable.get("color_palette", []),
        }
        params.append(param)
    return params


def validate_brief(brief: dict) -> list[str]:
    """Return a list of warnings/issues with the brief."""
    warnings = []
    if not brief.get("deliverables"):
        warnings.append("No deliverables specified")
    if not brief.get("brand_assets"):
        warnings.append("No brand assets provided — output may lack brand consistency")
    for i, d in enumerate(brief.get("deliverables", [])):
        if not d.get("description"):
            warnings.append(f"Deliverable {i+1} has no description")
        if d.get("quantity", 0) > 100:
            warnings.append(f"Deliverable {i+1} requests {d['quantity']} assets — consider batching")
    return warnings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.intake.parser <brief.json>")
        sys.exit(1)
    brief = load_brief(sys.argv[1])
    warnings = validate_brief(brief)
    if warnings:
        print("⚠️  Warnings:")
        for w in warnings:
            print(f"   - {w}")
    params = extract_generation_params(brief)
    print(f"\n✅ Parsed {len(params)} deliverable(s)")
    for p in params:
        print(f"   {p['type']} ({p['platform']}) — {p['quantity']}x at {p['dimensions']}")
