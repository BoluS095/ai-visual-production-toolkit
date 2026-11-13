# AI Visual Production Toolkit

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/BoluS095/ai-visual-production-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/BoluS095/ai-visual-production-toolkit/actions/workflows/tests.yml)

A Python project for turning creative briefs into structured visual-production jobs. **The repository is an early-stage prototype, not yet a complete image-generation or delivery platform.** The README distinguishes working code from planned pipeline components.

## Current status

### Implemented
- Load UTF-8 JSON client briefs.
- Validate required fields, deliverable structure, positive quantities, WIDTHxHEIGHT dimensions, and color-palette types.
- Normalize deliverables into generation parameters.
- Produce quality warnings for missing descriptions, missing brand assets, empty deliverable lists, and oversized batches.
- Run a standard-library unit-test suite on Python 3.10, 3.11, and 3.12 through GitHub Actions.

### Planned (not implemented yet)
- Image-generation adapters (for example, Stable Diffusion or hosted model APIs).
- Batch orchestration, retries, and resumable jobs.
- Image post-processing and quality-control scoring.
- Packaging and delivery workflows.

The generation/, postprocess/, qc/, and delivery/ packages are extension points at this stage. Model integrations and production-readiness are not claimed.

## Quick start

Python 3.10 or newer is required. The brief parser uses only the Python standard library.

```bash
git clone https://github.com/BoluS095/ai-visual-production-toolkit.git
cd ai-visual-production-toolkit

# Parse and validate the included example
python -m src.intake.parser examples/sample_brief.json

# Run the test suite
python -m unittest discover -s tests -v
```

## Brief format

A brief is a UTF-8 JSON object with non-empty client and project strings and a deliverables array. Each deliverable is an object. quantity must be a positive integer; dimensions must be positive WIDTHxHEIGHT; and color_palette must be an array of strings.

Example:

```json
{
  "client": "Example Brand",
  "project": "Spring campaign",
  "brand_assets": {
    "logo_url": "https://example.com/logo.png"
  },
  "deliverables": [
    {
      "type": "social_post",
      "platform": "instagram",
      "dimensions": "1080x1080",
      "quantity": 4,
      "description": "Product launch posts",
      "color_palette": ["#1A1A2E", "#E94560"]
    }
  ]
}
```

Run the parser with:

```bash
python -m src.intake.parser examples/sample_brief.json
```

## Project layout

```
src/
  intake/
    parser.py        # Implemented brief loading, validation, and normalization
  generation/        # Planned model adapters and batch execution
  postprocess/       # Planned image processing
  qc/                # Planned quality checks
  delivery/          # Planned packaging and delivery
configs/
  default.yaml       # Initial target configuration (not all settings are wired yet)
examples/
  sample_brief.json
tests/
  test_parser.py
.github/
  workflows/
    tests.yml
```

## Configuration and dependencies

configs/default.yaml records intended pipeline defaults; the settings are not all consumed by executable pipeline components yet. requirements.txt lists dependencies anticipated for later image/model integrations. They are not needed to run the current brief parser or its tests.

Do not put API keys in committed files. Use local environment variables for credentials when model adapters are added.

## Contributing

Issues and pull requests are welcome. Please include focused tests for parser or pipeline changes and clearly label unfinished or provider-specific functionality.

## License

MIT. See LICENSE.
