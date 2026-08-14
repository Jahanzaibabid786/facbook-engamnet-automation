# Facebook Web Automation

A lightweight Facebook web automation system built with Python + PyDoll. Manages multiple persistent Facebook profiles and executes configurable, human-like daily activities.

## Project Status

**Phase 1: Foundation** ✅ Complete (2026-08-14)
- Login & profile validation system
- CLI interface
- SQLite metadata
- Core managers (Browser, Profile, Session)
- Logging system

**Next:** Phase 2 — Multi-profile + Sequential Execution

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Features (Phase 1)

- ✅ New Facebook Login with manual login flow
- ✅ Profile creation with validation-before-save
- ✅ Profile lifecycle states (CREATING → LOGIN_PENDING → VALIDATING → ACTIVE/FAILED)
- ✅ Chrome profile isolation and management
- ✅ Per-profile and global logging
- ✅ SQLite metadata storage

## Architecture

The project follows strict separation of concerns:
- **core/** — Browser, profile, session, device managers
- **facebook/** — Facebook-specific navigation and actions
- **interaction/** — Mouse/keyboard/cursor abstraction (Phase 6)
- **config/** — Centralized JSON configuration
- **utils/** — Logger, database, helpers

See [AGENTS.md](AGENTS.md) for full project guidance and architecture principles.

## Documentation

- [AGENTS.md](AGENTS.md) — Start here
- [docs/01_PROJECT_OVERVIEW.md](docs/01_PROJECT_OVERVIEW.md) — Project summary
- [docs/03_ARCHITECTURE.md](docs/03_ARCHITECTURE.md) — Architecture
- [docs/04_REQUIREMENTS.md](docs/04_REQUIREMENTS.md) — Requirements
- [docs/05_FEATURES.md](docs/05_FEATURES.md) — Feature catalog
- [docs/07_IMPLEMENTATION_PLAN.md](docs/07_IMPLEMENTATION_PLAN.md) — Roadmap
- [docs/08_PROJECT_STRUCTURE.md](docs/08_PROJECT_STRUCTURE.md) — Structure
- [docs/36_RULES.md](docs/36_RULES.md) — Development rules
- [docs/37_CHANGELOG.md](docs/37_CHANGELOG.md) — Version history

## Requirements

- Python 3.x
- PyDoll (browser automation)
- Chrome/Chromium browser

## License

[Add license information]

## Contributing

See [AGENTS.md](AGENTS.md) and [docs/36_RULES.md](docs/36_RULES.md) for development guidelines.
