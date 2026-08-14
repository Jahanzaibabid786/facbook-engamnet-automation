# 03 — Architecture

## 1. High-Level Layout

```text
facebook_automation/
│
├── main.py                      CLI entry point
├── config/                      settings.json, devices.json, activity_config.json
├── core/                        browser, profile, session, device, activity, scheduler, instance managers
├── facebook/                    login, feed, reels, likes, comments, sharing, stories, navigation
├── interaction/                 mouse, keyboard, cursor, human_interaction
├── profiles/                    profile_data/ + metadata/
├── logs/                        application.log + per-profile logs
├── database/app.db              SQLite metadata
└── utils/                       logger, randomizer, validators, helpers
```

The important point: **browser management, profile management, Facebook
activities, and interaction logic must remain separate modules.**

## 2. Layered Data Flow

### Login Flow (Module 1)

```text
Create Profile → Launch Chrome → Facebook Login (manual) → Wait for session
→ Confirm → Validate → Save Profile (only if valid) → Close → Store metadata
```

### Activity Flow (Module 2)

```text
Activity Engine
    ↓
Browser Session
    ↓
Facebook Navigation
    ↓
Interaction Layer
```

The activity engine **must not** contain browser-launching code directly.

### Interaction Flow

```text
Facebook Action
    ↓
Interaction Manager
    ↓
Mouse Controller / Keyboard Controller / Visual Cursor
```

Facebook modules request interactions through the abstraction
(`interaction.click(element)`, `interaction.type_text(text)`,
`interaction.scroll(amount)`, `interaction.move_to(element)`) so the underlying
mouse/cursor implementation can be swapped later without touching Facebook logic.

## 3. Separation of Responsibilities

| Manager | Responsibility |
|---------|----------------|
| ProfileManager | Manages profiles and their lifecycle states |
| BrowserManager | Manages Chrome start/stop/restart and crashes |
| DeviceManager | Manages device configs (user-agent, viewport) |
| FacebookManager | Manages Facebook navigation |
| ActivityEngine | Manages daily activities as independent tasks |
| InteractionManager | Manages mouse/keyboard/visual-cursor interaction |
| Scheduler | Manages timing of sessions and intervals |
| Logger | Manages per-profile + global logs |

## 4. Core Design Principle

```text
UI ≠ Automation Engine
Browser ≠ Facebook Logic
Facebook Logic ≠ Interaction Logic
Profile ≠ Activity
Device ≠ Profile
Scheduler ≠ Browser
```

- Browser management, profile management, Facebook activities, and interaction
  logic are separated.
- The Python engine is completely independent of any future desktop UI.

## 5. Instance Manager & Execution Modes

### Sequential

```text
Profile 001 → Start → Activities → Close
Profile 002 → Start → Activities → Close
Profile 003 → Start → Activities → Close
```

Minimal system resources; the preferred lightweight architecture.

### Parallel

```text
            ┌─ Profile 001
Start ──────┼─ Profile 002
            └─ Profile 003      (Max Instances: 3, for example)
```

Each profile gets its own browser instance, profile directory, session, device
config, activity state, and logging context. A **window manager** automatically
arranges Chrome windows into a grid by computing instance count, monitor size,
row, column, and x/y coordinates.

## 6. Profile Lifecycle

```text
Create → Launch Chrome → Login → Validate → Save → Validate Saved → ACTIVE → Use
```

Failed validation produces `FAILED` / `DISABLED` and the profile is excluded
from active automation. Only `ACTIVE` profiles reach the automation engine.

## 7. Future Electron Architecture

```text
Electron Frontend (dashboard, profiles, devices, activities, scheduler, running
instances, logs, settings)
      │ IPC / Local API
      ↓
Python Automation Engine
      ├── Profile Manager / Browser Manager / Device Manager
      ├── Activity Engine / Scheduler / Interaction Manager / Logger
```

The CLI and the Electron UI both call the **same clean internal APIs**, so
converting to Electron does not require rewriting the automation engine.