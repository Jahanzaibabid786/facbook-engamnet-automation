# 07 — Implementation Plan

> Phased development roadmap derived from `Project Overview.md` §39. Each phase
> is independently shippable and validated before moving on. Map features to
> phases via `docs/05_FEATURES.md`.

## Phase 1 — Foundation: Login & Profile Validation

```text
Python project → PyDoll → Chrome launch → New login → Profile save → Profile validation
```

**Goals**
- Scaffold the project (structure per `docs/08_PROJECT_STRUCTURE.md`).
- Launch Chrome with PyDoll using a fresh, isolated profile directory.
- Implement the "New Facebook Login" flow: create profile ID → launch Chrome →
  open Facebook → manual login → wait → user confirmation → validate → save.
- Implement profile lifecycle states and the **validation-before-save** rule.
- Add `core/browser_manager.py`, `core/profile_manager.py`, `core/session_manager.py`.
- Add SQLite metadata (`profiles` table) and JSON config skeleton.
- Add global logger.

**Definition of Done**
- A profile is only persisted when it passes validation; broken/crashed sessions
  are never saved as usable.
- `docs/37_CHANGELOG.md` records the milestone.

## Phase 2 — Multi-Profile + Sequential Execution

```text
Multiple profiles → Profile selection → Sequential execution → Instance manager
```

**Goals**
- Full profile management in the CLI: view, select, validate, rename, disable,
  delete, test.
- Sequential mode: process profiles one at a time (start → activities → close).
- Browser instance manager with start/close/restart and crash detection.
- Per-instance state tracking (profile ownership, device config, start/close time).
- Error isolation: one failed profile does not stop the queue.
- Browser recovery: crash → restart → reload → validate → resume/mark failed.

**Definition of Done**
- Run automation for a selected list of profiles sequentially; failures are
  logged and skipped without killing the run.

## Phase 3 — Daily Activity Engine

```text
Activity engine → Feed → Reels → Likes → Comments → Sharing → Stories
```

**Goals**
- Implement the activity engine with **no browser-launching code**.
- Implement feed browsing (open/scroll/pause), reels, likes, comments, sharing,
  stories as independent, configurable tasks.
- Activity configuration JSON (toggles + `daily_limits`).
- Result tracking for every activity (SUCCESS/FAILED/SKIPPED/TIMEOUT/NOT_FOUND/
  SESSION_ERROR).
- Per-profile activity logs.
- Session scheduler that composes sessions from the activity pool with
  configurable intervals and randomization.

**Definition of Done**
- A profile completes a daily session and every activity writes a tracked result
  to its profile log and the `activities` table.

## Phase 4 — Device Manager

```text
Device manager → User-agent config → Viewport config → Profile→device mapping
```

**Goals**
- Centralized device configurations (Android phones/tablet, Windows 11/10/7).
- Device config drives user-agent and viewport.
- Profile→device mapping stored per profile; profiles remember their device.

**Definition of Done**
- Assigning a device to a profile changes its UA and viewport without code edits.

## Phase 5 — Parallel Mode + Window Management

```text
Parallel mode → Multiple Chrome instances → Window manager → Resource capping
```

**Goals**
- Parallel execution with a max-concurrency cap (e.g. 20 selected, 3 running).
- Window Manager auto-arranges Chrome windows into a grid.
- Resource management: close idle instances, clean temp artifacts.

**Definition of Done**
- Multiple profiles run concurrently, windows are arranged, and concurrency is
  capped correctly.

## Phase 6 — Interaction Layer

```text
Interaction layer → Custom mouse scripts → Keyboard scripts → Visual cursor
```

**Goals**
- Interaction abstraction: `click`, `type_text`, `scroll`, `move_to`.
- Mouse controller (move, click, double-click, scroll) and keyboard controller
  (typing, keys, Enter/Escape/Backspace/navigation).
- Visual-cursor mechanism independent of Facebook logic.
- Human-like randomized interaction helpers.

**Definition of Done**
- Facebook modules call the interaction abstraction only; swapping the mouse/
  cursor implementation requires no Facebook-module changes.

## Phase 7 — Electron Frontend

```text
Electron → Dashboard → Profile manager → Scheduler → Activity manager → Logs
```

**Goals**
- Electron + React + TypeScript desktop app calling the same Python engine APIs
  via IPC / local API.
- Dashboard (active/running/completed/failed), profile management, scheduler,
  activity controls, logs, settings, start/stop, sequential/parallel selection.

**Definition of Done**
- The desktop app reproduces CLI capabilities without modifying the Python engine.

## Cross-Cutting (throughout)

- Git/GitHub integration from day one (see `docs/36_RULES.md`).
- Checkpoint commits/tags before each phase's major changes.
- Update `docs/37_CHANGELOG.md` after every meaningful milestone.

## Prioritized Order of Work

1. Phase 1 → Phase 2 → Phase 3 (core value: login + daily activity, sequential).
2. Phase 4 (devices) can slot in early if needed by profile testing.
3. Phase 5 (parallel) after sequential is stable.
4. Phase 6 (interaction) as soon as custom mouse/cursor scripts are available.
5. Phase 7 (Electron) last, only when the engine is stable.