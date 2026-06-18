# 🎨 AI Visual Production Toolkit

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> End-to-end pipeline for generating, post-processing, and delivering AI visual assets at scale.

## Overview

This toolkit automates the full visual production pipeline — from creative brief to delivered assets — using multiple generative AI models. Built for agencies, studios, and creative teams who need to produce high-quality visual content at scale.

### Pipeline

```
client_brief.json
    │
    ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────┐     ┌──────────┐
│ Brief Parser │────▶│ Batch Engine │────▶│ Post-Process │────▶│  QC  │────▶│ Delivery │
└─────────────┘     └──────────────┘     └─────────────┘     └──────┘     └──────────┘
```

1. **Brief Intake** — Parse client briefs into structured generation parameters
2. **Batch Generation** — Generate visual assets across multiple AI models (Stable Diffusion, DALL-E, Midjourney via API)
3. **Post-Processing** — Automated upscaling, color correction, format conversion, and brand overlay
4. **Quality Control** — Automated QC scoring + human review queue
5. **Delivery** — Package and deliver assets in client-specified formats

## Quick Start

```bash
# Clone and install
git clone https://github.com/BoluS095/ai-visual-production-toolkit.git
cd ai-visual-production-toolkit
pip install -r requirements.txt

# Copy environment config
cp .env.example .env
# Edit .env with your API keys

# Run with sample brief
python -m src.intake.parser examples/sample_brief.json
```

## Project Structure

```
ai-visual-production-toolkit/
├── src/
│   ├── intake/          # Brief parsing and parameter extraction
│   ├── generation/      # Multi-model batch generation engine
│   ├── postprocess/     # Upscaling, color correction, overlays
│   ├── qc/              # Quality control scoring
│   └── delivery/        # Asset packaging and delivery
├── configs/             # Pipeline configuration
├── examples/            # Sample briefs and workflows
└── requirements.txt
```

## Supported Models

| Model | Status | Use Case |
|-------|--------|----------|
| Stable Diffusion XL | ✅ Ready | Product shots, backgrounds, abstract art |
| DALL-E 3 | ✅ Ready | Marketing graphics, social media content |
| Midjourney (via API) | 🔧 Beta | High-end creative, editorial imagery |
| Flux | 🔧 Beta | Photorealistic generation |

## Configuration

See `configs/default.yaml` for pipeline configuration options:

```yaml
generation:
  default_model: "sdxl"
  batch_size: 10
  quality_threshold: 0.75

postprocess:
  upscale: true
  upscale_factor: 2
  color_correction: true
  format: "png"
```

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

**Rafał Korzeniewski** — Python developer, trainer, and [PyWaw](https://pywaw.org) co-organizer.
