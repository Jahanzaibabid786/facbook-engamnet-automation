# 04 — Requirements

> Derived from `Project Overview.md`. Functional requirements are grouped by
> module; non-functional requirements apply to the whole system. Each item has
> a stable ID so it can be referenced from code, tests, and the changelog.

## 1. Functional Requirements

### FR-1 — Login Manager

- FR-1.1 The CLI offers a "New Facebook Login" option.
- FR-1.2 Creating a login must: create a profile identifier, create a lightweight
  Chrome profile directory, launch Chrome, open Facebook, and allow manual login.
- FR-1.3 The application must wait for the Facebook session to become available.
- FR-1.4 The user must be able to confirm that login is complete.
- FR-1.5 The session must be validated as actually usable before saving.
- FR-1.6 The profile must be saved **only after successful validation**, then the
  browser closes cleanly and metadata is stored.

### FR-2 — Profile Validation

- FR-2.1 A profile must never be saved/marked usable if Chrome crashed, login did
  not complete, the browser closed unexpectedly, session data is incomplete,
  Facebook did not load, required cookies/session state are missing, or profile
  creation failed.
- FR-2.2 Profiles carry a lifecycle status from
  `CREATING`, `LOGIN_PENDING`, `VALIDATING`, `ACTIVE`, `FAILED`, `DISABLED`.
- FR-2.3 Only `ACTIVE` profiles are available to the automation engine.
- FR-2.4 A profile that repeatedly fails validation is automatically marked
  `FAILED` or `DISABLED` rather than being used continuously.
- FR-2.5 Validation flow: Load Profile → Start Chrome → Open Facebook → Check Page
  → Check Session State → Check Account Availability → Mark `ACTIVE` / `FAILED`.

### FR-3 — Profile Storage

- FR-3.1 Each profile has isolated browser storage under `profiles/profile_XXX/`
  containing `chrome_data/`, `metadata.json`, and `state.json`.
- FR-3.2 Metadata covers profile_id, name, status, device_type, browser_type,
  user_agent_id, created_at, last_used, total_sessions.
- FR-3.3 Sensitive session information stays inside the browser profile storage;
  it is not duplicated into JSON.
- FR-3.4 Saved profiles must be kept lightweight (no cache, temp files, logs,
  downloads, or unused browser data) while preserving everything required for
  session persistence.

### FR-4 — Device / User-Agent System

- FR-4.1 A centralized Device Manager provides device configs: device_id,
  device_type, platform, browser, screen_size, user_agent.
- FR-4.2 Supported categories include Android (phone sizes, tablet) and Windows
  (11, 10, 7).
- FR-4.3 The device config controls browser viewport and related settings.
- FR-4.4 The profile manager remembers each profile's device configuration.
- FR-4.5 Config is managed centrally; user-agent strings are never hardcoded
  throughout the app.

### FR-5 — Browser Instance Manager

- FR-5.1 The instance manager starts Chrome, assigns profile, device config and
  viewport, launches the browser, tracks process and window.
- FR-5.2 It closes and restarts browsers and detects crashes.
- FR-5.3 It maintains per-instance state: which profile owns it, which device
  config is active, when it started, when it should close.

### FR-6 — Execution Modes

- FR-6.1 **Sequential mode** processes profiles one at a time (start → activities
  → close) with minimal resources.
- FR-6.2 **Parallel mode** runs multiple profiles concurrently, each with its own
  browser instance, profile directory, session, device config, activity state,
  and logging context.
- FR-6.3 A maximum-concurrency setting caps simultaneous instances (e.g. 20
  profiles selected, only 3 run at once).
- FR-6.4 The **Window Manager** arranges Chrome windows automatically (instance
  count, monitor size, row, column, x/y coordinates).

### FR-7 — Daily Activity Engine

- FR-7.1 The engine executes a configurable sequence of activities using a saved
  profile; it contains **no browser-launching code**.
- FR-7.2 Supported activities: home feed (open/scroll/pause), reels (watch/move,
  configurable intervals), likes (limits + recording), sharing (open share UI →
  choose action → complete → record), stories (open/view/configured activity),
  comments (open section → focus field → type → submit → record).
- FR-7.3 Every activity is treated as an independent task.

### FR-8 — Activity Configuration

- FR-8.1 Behavior is driven by configuration, not hardcoded: feed_scrolling,
  reels, likes, comments, sharing, stories toggles plus `daily_limits`
  (reels, likes, comments, shares).
- FR-8.2 The scheduler can construct sessions from an activity pool, respecting
  configured limits, with configurable intervals between sessions.

### FR-9 — Interaction Layer

- FR-9.1 A separate interaction layer exposes an abstraction:
  `interaction.click(element)`, `type_text(text)`, `scroll(amount)`,
  `move_to(element)`.
- FR-9.2 The interaction layer supports click, double click, mouse movement,
  scroll, keyboard typing, key presses, text entry, Enter, Escape, Backspace,
  and navigation keys.
- FR-9.3 A visual-cursor mechanism is supported and stays independent of
  Facebook-specific logic so it can be swapped later.

### FR-10 — Result Tracking & Logging

- FR-10.1 Every activity returns a result: profile_id, activity, status,
  timestamp, duration.
- FR-10.2 Activity states: `SUCCESS`, `FAILED`, `SKIPPED`, `TIMEOUT`,
  `NOT_FOUND`, `SESSION_ERROR`.
- FR-10.3 Logging: per-profile log files plus a global `application.log`, with
  timestamped CLI output.

### FR-11 — Database

- FR-11.1 SQLite stores metadata in tables `profiles`, `activities`, `sessions`.
- FR-11.2 The database stores metadata, not a duplicate of browser session data.

### FR-12 — CLI Interface

- FR-12.1 Main menu: New Facebook Login, View Saved Profiles, Validate Profiles,
  Start Automation, Activity Settings, Device Settings, Browser Settings, Logs,
  Exit.
- FR-12.2 Profiles screen supports: select, validate, rename, disable, delete,
  test, start.
- FR-12.3 Start Automation screen supports execution mode selection (sequential /
  parallel), profile selection, device selection (automatic / profile default),
  and a start confirmation.

### FR-13 — Error Handling & Recovery

- FR-13.1 Every major component handles exceptions (Chrome start failure,
  profile dir unavailable, page timeout, session unavailable, element not found,
  interaction failed, browser crash, window arrangement failure, activity timeout).
- FR-13.2 Log the error and continue with the next profile where appropriate; a
  single failed profile must not terminate the whole queue.
- FR-13.3 Recovery: browser crash → detect → restart instance → reload profile →
  validate session → resume or mark failed. Activity timeout → retry → continue
  or log and move on.

### FR-14 — Resource Management

- FR-14.1 The system avoids unnecessary browser instances, closes inactive
  sessions, cleans temporary artifacts, limits parallel instances, and separates
  persistent from temporary data.

## 2. Non-Functional Requirements

- NFR-1 **Modularity** — browser, profile, Facebook, and interaction logic are
  separate; each component has one responsibility.
- NFR-2 **Extensibility** — new activities/devices are added via configuration
  and new modules without rewriting the core.
- NFR-3 **Lightweight** — low memory/CPU footprint; sequential by default;
  parallel capped.
- NFR-4 **Maintainability** — centralized configuration, clean internal APIs,
  documented modules.
- NFR-5 **Electron-readiness** — the Python engine exposes clean internal APIs
  callable from a future Electron frontend without rewriting.
- NFR-6 **Reliability** — validation-before-save, crash detection, recovery,
  and per-profile error isolation.
- NFR-7 **Human-like behavior** — randomized timing and interactions to behave
  naturally; activity limits respected.
- NFR-8 **Security/privacy** — sensitive session data remains in browser profile
  storage; not duplicated into JSON or unnecessarily exposed.
- NFR-9 **Versioning** — meaningful commits, version tags, checkpoints before
  major changes, easy rollback, documented in `docs/37_CHANGELOG.md`.