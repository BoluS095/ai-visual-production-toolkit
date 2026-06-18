# 🎨 AI Visual Production Toolkit

> End-to-end pipeline for generating, post-processing, and delivering AI visual assets at scale.

## Overview

This toolkit automates the full visual production pipeline:

1. **Brief Intake** — Parse client briefs into structured generation parameters
2. **Batch Generation** — Generate visual assets across multiple AI models (Stable Diffusion, DALL-E, Midjourney via API)
3. **Post-Processing** — Automated upscaling, color correction, format conversion, and brand overlay
4. **Quality Control** — Automated QC scoring + human review queue
5. **Delivery** — Package and deliver assets in client-specified formats

## Architecture

```
client_brief.json
    │
    ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Brief Parser │────▶│ Batch Engine │────▶│ Post-Process │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                          ┌─────────────┐       │
                          │   QC Score   │◀──────┘
                          └─────────────┘
                                │
                          ┌─────────────┐
                          │   Delivery   │
                          └─────────────┘
```

## Project Structure

```
ai-visual-production-toolkit/
├── src/
│   ├── intake/          # Brief parsing & parameter extraction
│   ├── generation/      # Multi-model generation engine
│   ├── postprocess/     # Upscaling, color, overlays, formatting
│   ├── qc/              # Quality control scoring
│   └── delivery/        # Packaging & delivery automation
├── prompts/             # Tested prompt templates by category
├── configs/             # Model configs, brand presets
├── tests/
├── requirements.txt
└── README.md
```

## Getting Started

```bash
# Clone the repo
git clone https://github.com/BoluS095/ai-visual-production-toolkit.git
cd ai-visual-production-toolkit

# Install dependencies
pip install -r requirements.txt

# Configure your API keys
cp .env.example .env
# Edit .env with your model API keys

# Run a test generation
python -m src.generation.generate --brief examples/sample_brief.json
```

## Roadmap

- [x] Project structure & architecture design
- [x] Brief parser with template support
- [ ] Stable Diffusion XL integration
- [ ] DALL-E 3 API integration
- [ ] Automated upscaling pipeline (Real-ESRGAN)
- [ ] Brand overlay system
- [ ] QC scoring model
- [ ] Delivery automation (Google Drive, Dropbox, direct)
- [ ] Web dashboard for client review

## Tech Stack

- **Python 3.11+** — Core pipeline
- **Stable Diffusion / ComfyUI** — Primary generation engine
- **OpenAI API** — DALL-E integration
- **Pillow / OpenCV** — Post-processing
- **FastAPI** — API layer
- **SQLite** — Job tracking

## License

MIT
