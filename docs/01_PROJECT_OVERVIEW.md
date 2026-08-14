# 01 — Project Overview

## 1. What This Is

A **lightweight Facebook web automation system** written in **Python + PyDoll**. The first version is a **CLI application**, but the architecture is designed so it can later be converted into a professional **Electron desktop application** without rewriting the core automation engine.

The system has **two primary modules**:

1. **Facebook Login & Profile Manager** — create, validate, save, and manage multiple persistent Facebook profiles.
2. **Daily Facebook Activity Automation** — execute configurable, human-like daily activity on those profiles.

## 2. Core Capabilities

- Multiple saved Facebook profiles with isolated Chrome storage
- Profile reuse, validation, rename, disable, delete, test
- Sequential and optional parallel execution
- Chrome instance management with automatic window arrangement
- Lightweight profile storage
- Device / user-agent configuration (Android + Windows)
- Activity scheduling and randomization
- Human-like browser interactions (mouse, keyboard, visual cursor)
- Per-profile and global logging
- SQLite metadata + JSON configuration
- Error handling, recovery, and resource management

## 3. Driving Goals

> Simple · Modular · Lightweight · Maintainable · Extensible

The most important architectural principle:

```text
UI ≠ Automation Engine
Browser ≠ Facebook Logic
Facebook Logic ≠ Interaction Logic
Profile ≠ Activity
Device ≠ Profile
Scheduler ≠ Browser
```

Each component has one clear responsibility. This separation makes the future
Electron frontend straightforward to build without touching the Python engine.

## 4. Technology Stack

| Layer | Technology |
|-------|------------|
| Core | Python 3.x, PyDoll, Chromium/Chrome |
| Storage | Chrome profiles, JSON config, SQLite metadata |
| Interface | CLI (initial) → Electron + React + TypeScript (future) |
| Concurrency | Async where PyDoll supports; sequential + parallel |

## 5. Key Concepts

- **Profile lifecycle states:** `CREATING → LOGIN_PENDING → VALIDATING → ACTIVE` / `FAILED` / `DISABLED`. Only `ACTIVE` profiles are automatable.
- **Lightweight profile:** preserve only session cookies, local storage, preferences, and session state needed for persistence. Never blindly delete required storage.
- **Device Manager:** every profile references a device config (type, platform, viewport, user-agent) centrally — never hardcode user-agent strings.
- **Instance Manager:** owns Chrome start/stop/restart, crash detection, and tracks which profile owns which instance.
- **Activity Engine:** runs feed, reels, likes, comments, shares, stories as independent tasks, respecting configured limits.

## 6. Development Phases

| Phase | Scope |
|-------|-------|
| Phase 1 | Python project, PyDoll, Chrome launch, new login, profile save & validation |
| Phase 2 | Multiple profiles, selection, sequential execution, instance manager |
| Phase 3 | Facebook activity engine (feed, reels, likes, comments, sharing, stories) |
| Phase 4 | Device manager, user-agent & viewport config, profile→device mapping |
| Phase 5 | Parallel mode, multiple instances, window manager, resource capping |
| Phase 6 | Interaction layer, custom mouse/keyboard, visual cursor |
| Phase 7 | Electron frontend: dashboard, profiles, scheduler, activities, logs |

See `docs/07_IMPLEMENTATION_PLAN.md` for the detailed roadmap.

## 7. Reference

The authoritative full specification lives in `Project Overview.md` (40 sections).
This document is the condensed, stable overview.