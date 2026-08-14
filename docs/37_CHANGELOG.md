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

### [0.2.0] - 2026-08-14

**Phase 2: Multi-Profile + Sequential Execution** ✅

#### Added
- **Sequential Execution Engine** (`core/sequential_executor.py`)
  - Process multiple profiles one at a time
  - Automatic browser launch → session validation → activities → close per profile
  - Error isolation: failed profiles don't stop the queue
  - Browser crash recovery with automatic restart and re-validation
  - Per-profile session tracking in database
- **Enhanced Profile Selection UI**
  - Interactive profile selection (comma-separated indices or "0" for all)
  - Filter profiles by status (ACTIVE profiles only for automation)
  - Display profile statistics (last used, total sessions)
- **Profile Validation Feature** (CLI option 3)
  - Re-validate saved profiles against Facebook
  - Launch browser → check session → update status
  - Batch validation with detailed status reporting
- **Start Automation Feature** (CLI option 4)
  - Select ACTIVE profiles for sequential execution
  - Live progress display with timestamps
  - Execution summary with success/failed/skipped counts
- **Profile Statistics**
  - Track `last_used` timestamp per profile
  - Track `total_sessions` counter per profile
  - Display in profile list and automation selection UI

#### Enhanced
- `main.py`: Added sequential execution integration and enhanced profile management UI
- `core/profile_manager.py`: Added `update_profile_last_used()` method
- `utils/database.py`: Session tracking with start/end times and status

#### Architecture
- Error isolation maintained: one profile failure doesn't terminate the queue
- Sequential mode is the default lightweight execution model
- Browser recovery system: crash → detect → restart → validate → resume/fail
- Clean separation: execution engine remains independent of activity logic (Phase 3)

#### Definition of Done
- ✅ Multiple profiles can be selected and executed sequentially
- ✅ Failed profiles are logged and skipped without killing the run
- ✅ Browser crashes trigger automatic recovery attempts
- ✅ Profile validation works against live Facebook sessions
- ✅ Statistics tracked per profile (last used, total sessions)

#### GitHub
- Repository: https://github.com/Jahanzaibabid786/facbook-engamnet-automation
- Previous: 08cfa87 (Phase 1), ddc8a7c (Bug fix: --no-sandbox removal)
- Current: [pending commit]

#### Next
Phase 3: Daily Activity Engine (Feed, Reels, Likes, Comments, Sharing, Stories)

---

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
