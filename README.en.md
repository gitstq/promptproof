[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

# PromptProof

> Proof first, pay later. Turn AI video prompts into a priced checklist, and only pay final-render prices for the shots that pass.

## 🎉 Introduction

AI video generation bills by the second, yet most people work like this: an idea pops up, they write a paragraph, render it straight at the highest resolution, and re-roll when it disappoints. The money goes up in smoke on shots that a cheap low-res proof would have killed in seconds.

PromptProof is a small, fully local tool that sits *in front of* your generator and does three things: it turns a prompt from a paragraph into a structured shot — subject, action, camera and style as separate fields; it validates and de-duplicates a whole batch, then arranges it into a two-stage checklist — proof everything at 768P, review, and only render finals for approved shots; and it prices the whole batch before you spend anything.

It is inspired by a real image-to-video working habit — proof cheaply first, pay for the final only once you know it works — but it is not tied to any generation service and calls no API. Use it with ComfyUI, a web tool, anything: it only handles the step *before* generation. **What makes it different: zero dependencies, fully offline, your own prices as configuration, and honest savings math (if you approve everything, the proofs are an extra quality-check cost, and the tool says so).**

## ✨ Features

- 🧩 **Structured shots** — subject / action / camera / style / first frame / negative as named fields, so a missing piece is obvious
- ✅ **Batch validation** — empty subjects, empty actions, out-of-range durations and bad resolutions, listed in one pass
- 🧹 **Automatic de-duplication** — shots are fingerprinted by creative content, so the same idea at a different duration still counts as a duplicate
- 💰 **Cost estimates** — priced from a per-second rate table holding *your* provider's real prices; edit one JSON file
- 🎬 **Two-stage plans** — proof everything, render finals only for approved shots, with the difference versus rendering everything at final quality
- 📋 **Checklist export** — a Markdown checklist with copy-ready prompts, or CSV for planning and billing
- 🔒 **Fully offline** — no network, no uploads; unpublished ideas never leave your machine

## 🚀 Quick Start

Requirements: Python 3.10 or newer on Windows, macOS or Linux. There is nothing else to install.

```bash
# 1. Get the code (git clone once it is published; locally, just enter the folder)
cd promptproof

# 2. Validate the example shots file
python -m promptproof validate examples/shots.json

# 3. Build a two-stage plan, approving only cat-desk for the final render
python -m promptproof plan examples/shots.json --approve cat-desk --rates examples/rates.json --out plan.md

# 4. Open plan.md: run the proofs first, review, then run the finals
```

Optional — install it as a command:

```bash
pip install .
promptproof validate examples/shots.json
```

## 📖 User Guide

### Shot file format (JSON)

```json
[
  {
    "id": "cat-desk",
    "subject": "an orange cat sitting at a small wooden desk",
    "action": "turns its head towards the camera and blinks slowly",
    "camera": "slow push-in, medium shot",
    "style": "warm natural light, cinematic",
    "source_image": "cat_first_frame.png",
    "negative": "no text, no watermark",
    "duration_sec": 5,
    "final_resolution": "2K"
  }
]
```

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Shot name; you approve finals by id |
| `subject` / `action` | yes | What is in the shot and what it does; empty values fail validation |
| `camera` / `style` | no | Camera move and look; camera defaults to `static` |
| `source_image` | no | First-frame image for image-to-video |
| `negative` | no | Things that must not appear |
| `duration_sec` | no | Length in seconds, 1–15, default 5 |
| `final_resolution` | no | `768P` / `1080P` / `2K`, default `2K` |

### The three commands

```bash
# Validate: exit code 1 on problems, so it works as a gate in scripts
python -m promptproof validate my_shots.json

# Print one shot's composed prompt, ready to paste into your generator
python -m promptproof prompt my_shots.json cat-desk

# Export a CSV plan (--format csv), or drop --out to print to the terminal
python -m promptproof plan my_shots.json --approve cat-desk,harbour-dawn --format csv
```

### Configuring prices

Copy `examples/rates.json` and replace the numbers with your provider's actual per-second prices (any currency, as long as the table is consistent):

```json
{ "768P": 0.20, "1080P": 0.40, "2K": 0.80 }
```

> The numbers in this repository are worked examples only — they are not any provider's real pricing. Set your own before trusting a total.

### Typical uses

1. **Batched image-to-video work** — write the week's 20 shots as one JSON file, validate and de-duplicate them, see the proof total at a glance, and pay final prices only for the half that survives review.
2. **Client billing** — the CSV plan *is* your quote breakdown: what the proofs cost, what the finals cost, no arguments later.
3. **A reusable prompt library** — a structured shots file is a real asset, unlike a paragraph buried in a chat history.

_Screenshots / demo GIF: to be added (the terminal output of the `plan` command is the checklist itself)._

## 💡 Design Notes and Roadmap

Three rules shaped the design: **zero dependencies** (if the standard library can do it, no package gets added — tools should outlive their dependencies), **price it before you run it** (any batch that costs money should start as a readable checklist), and **no provider lock-in** (prices and resolutions are configuration, so switching providers means editing one file, not the tool).

Roadmap:

- [ ] Import shots from CSV spreadsheets (how many creators already plan their shots)
- [ ] Write approval state back into the shots file, for a traceable proofing record
- [ ] Export a batch brief that a ComfyUI workflow folder can carry alongside it
- [ ] Multi-currency support and a budget cap that makes validation fail loudly

Good first contributions: new export formats, extra validation rules, and example shot libraries from real projects.

## 📦 Packaging and Deployment

PromptProof is a **tool / script project**: there is no executable to build and no Release download. Integrate it in whichever way suits you:

- **Run it in place** — copy or clone the folder, then `python -m promptproof ...`. Best for occasional use.
- **Install the command** — run `pip install .` in the project root, then use `promptproof` from any directory; remove it with `pip uninstall promptproof`.
- **Embed it in your own code**:

```python
from promptproof.models import load_shots
from promptproof.planner import build_plan, to_markdown_checklist

shots = load_shots("my_shots.json")
plan = build_plan(shots, approved_ids={"cat-desk"})
print(plan.total_cost, to_markdown_checklist(plan))
```

- **Compatibility** — Python 3.10+ on Windows, macOS and Linux; no network access needed, runs fine on an offline machine.
- **Troubleshooting** — `no rate configured` means your rates file has no entry for that resolution; add it. A reported duplicate is not an error: the same creative idea was written twice — delete one, or change a creative field to make it a genuinely different shot.

## 🤝 Contributing

Issues and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). In short: open an issue first and describe the problem or idea; keep pull requests focused and include tests; use `feat:` / `fix:` / `docs:` style commit prefixes; and make sure `python -m unittest discover -s tests -v` passes before you submit.

## 📄 License

PromptProof is released under the MIT License — see [LICENSE](LICENSE). You may use, copy, modify and distribute it, including commercially, as long as you keep the copyright and license notices. The software is provided "as is", without any warranty.
