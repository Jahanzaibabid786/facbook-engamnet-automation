# 37 — Changelog

> Version history for the Facebook Web Automation project. Keep this in sync
> with Git tags and milestones. See `docs/36_RULES.md` for the Git workflow.

## Versioning

Semantic-ish versioning with tags on every meaningful milestone:

- `v0.1.0` — Phase 1 milestone
- `v0.2.0` — Phase 2 milestone
- ... increment per phase and per feature/fix release.

## Template

```text
## [Unreleased]

### Added
- ...

### Changed
- ...

### Fixed
- ...

---

## [0.1.0] - YYYY-MM-DD

### Added
- Phase 1: project scaffold, PyDoll Chrome launch, new-login flow,
  profile validation, SQLite metadata, logging.
```

## History

### [0.1.0] - 2026-08-14

**Phase 1: Foundation — Login & Profile Validation** ✅

#### Added
- New Facebook Login flow with manual login support
- Profile creation with validation-before-save rule
- Profile lifecycle states: CREATING → LOGIN_PENDING → VALIDATING → ACTIVE/FAILED
- Chrome profile isolation and lightweight storage management
- Browser manager: launch/close/restart Chrome, crash detection
- Profile manager: CRUD operations, status management, cleanup
- Session manager: validation and session state detection
- SQLite database schema (profiles, activities, sessions tables)
- Per-profile and global logging system
- CLI interface with main menu (9 options, Phase 1 features active)
- Complete project documentation (AGENTS.md + 9 docs/ files)
- Configuration system: settings.json, devices.json, activity_config.json, scheduler.json, browser.json
- README.md, requirements.txt, .gitignore
- Git repository initialization and GitHub connection

#### Architecture
- Strict separation established: Browser ≠ Facebook Logic ≠ Interaction
- Centralized configuration (no hardcoded user-agents, timeouts, or paths)
- Module isolation maintained for future Electron frontend compatibility
- Clean internal APIs exposed by managers

#### Definition of Done
- ✅ Profiles only saved when validated as usable
- ✅ Broken/crashed/incomplete sessions marked FAILED, never ACTIVE
- ✅ Clean module separation maintained throughout
- ✅ Initial commit created and pushed to GitHub

#### GitHub
- Repository: https://github.com/Jahanzaibabid786/facbook-engamnet-automation
- Commit: 08cfa87 (Phase 1: Foundation - Login & Profile Validation)

#### Next
Phase 2: Multi-profile + Sequential Execution
