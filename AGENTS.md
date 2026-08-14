# AGENTS.md

Guidance for AI agents and human contributors working in this repository. Read this first, then the docs it links to.

## Project Summary

**Facebook Web Automation** — a lightweight, modular Facebook browser-automation platform built with **Python + PyDoll**. It manages multiple persistent Chrome profiles and runs daily, human-like Facebook activity (feed browsing, reels, likes, comments, shares, stories) either sequentially or in parallel across multiple Chrome instances.

The initial version is a **CLI application**. The architecture is designed so a future **Electron + React + TypeScript** desktop frontend can drive the same Python engine through clean internal APIs — without rewriting the core automation engine.

Two primary modules:

1. **Facebook Login & Profile Manager** — creates, validates, saves, and manages persistent Facebook sessions.
2. **Daily Facebook Activity Automation** — executes a configurable, randomized sequence of human-like activities on a saved profile.

## Read These First

| File | Purpose |
|------|---------|
| `Project Overview.md` | The original, full 40-section specification (source of truth) |
| `docs/01_PROJECT_OVERVIEW.md` | Condensed project overview |
| `docs/03_ARCHITECTURE.md` | Architecture, module responsibilities, separation of concerns |
| `docs/04_REQUIREMENTS.md` | Functional and non-functional requirements |
| `docs/05_FEATURES.md` | Feature catalog with status |
| `docs/07_IMPLEMENTATION_PLAN.md` | Phased development roadmap (Phase 1–7) |
| `docs/08_PROJECT_STRUCTURE.md` | Directory tree and module responsibilities |
| `docs/36_RULES.md` | Development and Git workflow rules |
| `docs/37_CHANGELOG.md` | Version history / changelog |

## Non-Negotiable Architecture Principle

The single most important rule:

```text
UI ≠ Automation Engine
Browser ≠ Facebook Logic
Facebook Logic ≠ Interaction Logic
Profile ≠ Activity
Device ≠ Profile
Scheduler ≠ Browser
```

Each component has **exactly one responsibility**:

- **ProfileManager** — manages profiles
- **BrowserManager** — manages Chrome
- **DeviceManager** — manages device configurations (user-agent + viewport)
- **FacebookManager** — manages Facebook navigation
- **ActivityEngine** — manages activities
- **InteractionManager** — manages mouse/keyboard/cursor interaction
- **Scheduler** — manages timing
- **Logger** — manages logs

Never couple these layers. A Facebook module must request an interaction via
`InteractionManager.click(...)` / `.type_text(...)` / `.scroll(...)`, never by
implementing mouse/cursor behavior itself.

## Tech Stack

- Python 3.x
- PyDoll (browser automation)
- Chromium / Google Chrome
- Chrome profiles (persistent Facebook sessions)
- CLI (initial), JSON config, SQLite metadata
- Async architecture where PyDoll supports it
- Future frontend: Electron + React + TypeScript

## Development Rules (Highlights)

- Keep the project **simple, modular, lightweight, maintainable, extensible**.
- Centralize all configurable values in `config/*.json` — never hardcode.
- A profile is only usable when its status is `ACTIVE`. Never mark incomplete
  or broken profiles as usable.
- Every major component must have proper exception handling; one failed profile
  must not kill the whole queue.
- Separate persistent data from temporary data; keep saved profiles lightweight.
- Write meaningful commits, tag versions, and document in `docs/37_CHANGELOG.md`.
  The full Git workflow is in `docs/36_RULES.md`.

## Commands (after the project is scaffolded)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI
python main.py

# Run tests (once added)
pytest
```

## Git Workflow (Summary)

See `docs/36_RULES.md` for the full workflow. Key points:

- Initialize Git and connect to a GitHub repository **before writing project code**.
- Create a proper `.gitignore`; make an initial commit before coding.
- Commit after every meaningful feature, fix, or milestone; push to GitHub.
- Create checkpoint commits/tags before major changes so rollback is easy.
- Never unnecessarily overwrite or delete working history.
- Keep Git/GitHub integration separate from application logic.
- Document all versions in `docs/37_CHANGELOG.md`.