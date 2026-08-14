# 08 — Project Structure

> Target directory layout and module responsibilities. The structure keeps
> browser management, profile management, Facebook activities, and interaction
> logic in separate modules so the future Electron frontend can drive the same
> engine without a rewrite.

## Full Layout

```text
facebook_automation/
│
├── main.py                         CLI entry point (menu, flow orchestration)
│
├── config/
│   ├── settings.json               Global application settings
│   ├── devices.json                Centralized device configs (UA + viewport)
│   ├── activity_config.json        Activity toggles + daily_limits
│   ├── scheduler.json              Session intervals / scheduling config
│   └── browser.json                Browser/Chrome settings
│
├── core/                           Engine managers (no Facebook or UI logic)
│   ├── browser_manager.py          Start/stop/restart Chrome, crash detection
│   ├── profile_manager.py          Profile CRUD, lifecycle states, validation
│   ├── session_manager.py          Session detection/validation for a profile
│   ├── device_manager.py           Device configs (UA, viewport, platform)
│   ├── activity_engine.py          Runs configured activities (no browser code)
│   ├── scheduler.py                Builds sessions from activity pool; timing
│   ├── instance_manager.py         Tracks running Chrome instances, concurrency
│   └── window_manager.py           Auto-arranges Chrome windows into a grid
│
├── facebook/                       Facebook-specific logic (no browser/UI code)
│   ├── login.py                    Login flow + session availability checks
│   ├── navigation.py               open_home/open_reels/find_feed_content/etc.
│   ├── feed.py                     Feed browsing (scroll, pause)
│   ├── reels.py                    Watch reels, move between them
│   ├── likes.py                    Like content within limits; record
│   ├── comments.py                 Open section, focus, type, submit, record
│   ├── sharing.py                  Open share UI, choose action, complete
│   ├── stories.py                  Open/view stories
│   └── selectors.py                Centralized element selectors (optional)
│
├── interaction/                    Input abstraction (independent of FB logic)
│   ├── interaction.py              Public API: click/type_text/scroll/move_to
│   ├── mouse.py                    Mouse controller implementation
│   ├── keyboard.py                 Keyboard controller implementation
│   ├── cursor.py                   Visual cursor mechanism
│   └── human_interaction.py        Human-like randomness helpers
│
├── profiles/                       Saved profile storage (gitignored)
│   ├── profile_data/               Per-profile browser storage
│   │   ├── profile_001/chrome_data/
│   │   ├── profile_002/chrome_data/
│   │   └── ...
│   └── metadata/                   metadata.json + state.json per profile
│
├── logs/                           (gitignored)
│   ├── application.log             Global application log
│   ├── profile_001.log             Per-profile activity logs
│   ├── profile_002.log
│   └── ...
│
├── database/
│   └── app.db                      SQLite metadata (profiles/activities/sessions)
│
├── utils/
│   ├── logger.py                   Per-profile + global logging
│   ├── randomizer.py               Random timing/interaction helpers
│   ├── validators.py               Input/config validation
│   └── helpers.py                  Shared helpers
│
├── docs/                           Markdown documentation (this set)
│   ├── 01_PROJECT_OVERVIEW.md
│   ├── 03_ARCHITECTURE.md
│   ├── 04_REQUIREMENTS.md
│   ├── 05_FEATURES.md
│   ├── 07_IMPLEMENTATION_PLAN.md
│   ├── 08_PROJECT_STRUCTURE.md
│   ├── 36_RULES.md
│   └── 37_CHANGELOG.md             Version history
│
├── tests/                          Tests (added as code lands)
│
├── Project Overview.md             Original full specification
├── AGENTS.md                       Agent/contributor guidance
├── requirements.txt                Python dependencies
├── .gitignore                      Ignore profiles/, logs/, database, caches
└── README.md                       Project readme
```

## Module Responsibilities

| Path | Responsibility | Must NOT contain |
|------|----------------|------------------|
| `main.py` | CLI menu and orchestration | Business/automation logic |
| `core/browser_manager.py` | Chrome lifecycle, crash detection | Facebook logic |
| `core/profile_manager.py` | Profile CRUD, statuses, validation | Browser launch code |
| `core/session_manager.py` | Session detect/validate | UI logic |
| `core/device_manager.py` | Device/UA/viewport configs | Hardcoded UA strings |
| `core/activity_engine.py` | Runs activities | Browser-launching code |
| `core/scheduler.py` | Session composition, timing | Browser code |
| `core/instance_manager.py` | Instance tracking, concurrency cap | Activity logic |
| `core/window_manager.py` | Window arrangement | Facebook logic |
| `facebook/*` | Facebook navigation & actions | Mouse/cursor implementation |
| `interaction/*` | Mouse/keyboard/cursor abstraction | Facebook logic |
| `utils/*` | Cross-cutting helpers | Feature logic |
| `config/*.json` | Centralized configuration | Code |

## Dependency Direction

```text
main.py
  → core/*            (managers)
      → facebook/*    (FB actions)
          → interaction/*   (input abstraction)
              → utils/*     (helpers, logging)
```

Managers depend on managers; Facebook modules depend only on the interaction
abstraction; nothing depends on the UI. This keeps the engine Electron-ready.