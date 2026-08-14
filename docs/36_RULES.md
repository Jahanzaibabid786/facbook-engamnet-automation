# 36 — Rules

> Development rules for this project: architecture, code, and Git/GitHub
> workflow. These are binding for all contributors and AI agents.

## 1. Architecture Rules

- **One responsibility per component.** The principle is absolute:

  ```text
  UI ≠ Automation Engine
  Browser ≠ Facebook Logic
  Facebook Logic ≠ Interaction Logic
  Profile ≠ Activity
  Device ≠ Profile
  Scheduler ≠ Browser
  ```

- **Separation of layers.** Browser management, profile management, Facebook
  activities, and interaction logic must remain separate modules. The activity
  engine must not contain browser-launching code. Facebook modules must not
  implement mouse/cursor behavior; they call `InteractionManager.click(...)`,
  `.type_text(...)`, `.scroll(...)`, `.move_to(...)`.
- **Keep the engine UI-independent.** The Python engine exposes clean internal
  APIs so a future Electron frontend can call the same functionality without a
  rewrite.
- **Centralize configuration.** All configurable values live in `config/*.json`
  (settings, devices, activities, scheduler, browser). Never hardcode user-agent
  strings, viewports, or activity limits in code.

## 2. Data & Storage Rules

- **Validation before save.** Never save or mark a profile usable unless its
  Facebook session is validated as actually usable. Broken, incomplete, crashed,
  or failed sessions are marked `FAILED`/`DISABLED`, never `ACTIVE`.
- **Only `ACTIVE` profiles run.** The automation engine may only use `ACTIVE`
  profiles.
- **Keep profiles lightweight.** Preserve only session cookies, local storage,
  preferences, and session state required for persistence. Clean cache, temp
  files, logs, and downloads. Never blindly delete storage required for session
  persistence.
- **Metadata only in SQLite.** The database stores metadata (profiles,
  activities, sessions); it does not duplicate browser session data.
- **Sensitive data stays in the browser profile.** Don't duplicate session
  credentials into JSON or logs.

## 3. Code Rules

- **Simple, modular, lightweight, maintainable, extensible.** Prefer small,
  single-purpose modules over monoliths.
- **Error handling everywhere.** Every major component handles exceptions
  (Chrome start failure, page timeout, session unavailable, element not found,
  interaction failed, browser crash, window arrangement failure, activity
  timeout). Log the error and continue with the next profile where appropriate —
  one failed profile must not terminate the whole queue.
- **Activity results are structured.** Each activity returns
  `{ profile_id, activity, status, timestamp, duration }` with states
  `SUCCESS` / `FAILED` / `SKIPPED` / `TIMEOUT` / `NOT_FOUND` / `SESSION_ERROR`.
- **Separation of persistent and temporary data.** Don't mix the two.
- **Central device manager.** Profiles reference a device config; never hardcode
  UA strings throughout the app.

## 4. Git & GitHub Workflow

> Full version history is documented in `docs/37_CHANGELOG.md`. Git/GitHub
> integration is kept separate from application logic.

### Setup (before writing project code)

1. **Initialize a Git repository** in the project root.
2. **Create the GitHub repository** if it does not exist, and connect the local
   repo to it as `origin`.
3. Create a proper `.gitignore` covering: `profiles/`, `logs/`, `database/`,
   `__pycache__/`, `*.pyc`, `.venv/`, caches, and OS/editor files.
4. **Make an initial commit** before coding begins.

### Committing

- After **every meaningful feature, fix, or milestone**, create a clear commit.
- Use **meaningful commit messages** describing what and why.
- Keep the project history clean so previous working versions can be restored
  easily.
- **Never overwrite or delete working history unnecessarily.** Do not `--force`
  push, `--hard` reset, or rewrite published history.

### Checkpoints & Tags

- **Before major changes**, create a checkpoint commit and/or tag so the project
  can move backward or forward safely.
- Use version tags where appropriate (e.g. `v0.1.0`, `v0.2.0`).
- Tag each Phase milestone (Phase 1 → 7).

### Rollback / Revert

- Make rollback/revert easy: prefer new commits that revert changes; keep a
  tagged, known-good point at every milestone.
- If a change breaks things, `git revert` (or checkout of a checkpoint tag) must
  restore a working state.

### Push

- **Automatically push commits to GitHub** after committing.
- Keep the remote continuously backed up and in sync.

### Documentation

- Record every released version and notable change in `docs/37_CHANGELOG.md`.
- Keep `docs/37_CHANGELOG.md` in sync with tags and milestones.

## 5. Definition of Done

A feature or milestone is done only when all of the following hold:

- [ ] Code follows the architecture and code rules above.
- [ ] Errors are handled and logged; failures do not kill the queue.
- [ ] Configuration lives in `config/*.json`, not in code.
- [ ] Tests pass (once the test suite exists).
- [ ] A meaningful commit was created and **pushed to GitHub**.
- [ ] Checkpoint tag added before/after major changes where applicable.
- [ ] `docs/37_CHANGELOG.md` updated.