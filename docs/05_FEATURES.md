# 05 — Features

> Catalog of the system's features, mapped to the requirements in
> `docs/04_REQUIREMENTS.md` and the phases in `docs/07_IMPLEMENTATION_PLAN.md`.
> Status is `PLANNED` until the feature is implemented; update it as work lands.

## Module 1 — Facebook Login & Profile Manager

| Feature | Description | Req | Phase |
|---------|-------------|-----|-------|
| New Facebook Login | Create profile → launch Chrome → manual login → validate → save | FR-1 | 1 |
| Session Wait & Confirm | Wait for session availability; user confirms completion | FR-1.3–1.4 | 1 |
| Validation-before-save | Only save usable sessions; never save broken profiles | FR-2 | 1 |
| Profile Lifecycle States | CREATING / LOGIN_PENDING / VALIDATING / ACTIVE / FAILED / DISABLED | FR-2.2 | 1 |
| Auto-Fail on Repeat | Repeated validation failure → FAILED / DISABLED | FR-2.4 | 1 |
| Isolated Profile Storage | Per-profile `chrome_data/`, `metadata.json`, `state.json` | FR-3 | 1 |
| Lightweight Profiles | Cleanup of cache/temp/unused data; preserve session state | FR-3.4 | 1 |
| Profile Management UI | View, rename, disable, delete, test, select profiles | FR-12.2 | 2 |
| Profile Validation | Re-validate a saved profile against Facebook | FR-2.5 | 2 |

## Device / User-Agent System

| Feature | Description | Req | Phase |
|---------|-------------|-----|-------|
| Device Manager | Centralized device configs (type, platform, viewport, UA) | FR-4 | 4 |
| Android Devices | Phone sizes (small/medium/large) and tablets | FR-4.2 | 4 |
| Windows Devices | Windows 11 / 10 / 7 desktop configs | FR-4.2 | 4 |
| Viewport Control | Device config drives browser viewport | FR-4.3 | 4 |
| Profile→Device Mapping | Each profile remembers its device config | FR-4.4 | 4 |

## Browser Instance Manager

| Feature | Description | Req | Phase |
|---------|-------------|-----|-------|
| Instance Lifecycle | Start/close/restart Chrome per profile | FR-5 | 2 |
| Crash Detection | Detect and react to browser crashes | FR-5.2 | 2 |
| Instance State | Track profile ownership, device config, start/close time | FR-5.3 | 2 |
| Sequential Mode | One profile at a time; minimal resources | FR-6.1 | 2 |
| Parallel Mode | Concurrent instances with max-concurrency cap | FR-6.2–6.3 | 5 |
| Window Manager | Auto-arrange Chrome windows into a grid | FR-6.4 | 5 |

## Module 2 — Daily Activity Engine

| Feature | Description | Req | Phase |
|---------|-------------|-----|-------|
| Feed Browsing | Open home/feed, scroll with pauses | FR-7.2 | 3 |
| Reels Activity | Watch several reels with configurable intervals | FR-7.2 | 3 |
| Likes | Like content within configured daily limits; record actions | FR-7.2 | 3 |
| Comments | Open section → focus → type → submit → record | FR-7.2 | 3 |
| Sharing | Open share UI → select action → complete → record | FR-7.2 | 3 |
| Stories | Open/view stories with configured behavior | FR-7.2 | 3 |
| Activity Configuration | JSON toggles + daily_limits | FR-8 | 3 |
| Session Scheduler | Compose sessions from activity pool; configurable intervals | FR-8.2 | 3 |
| Activity Randomization | Vary activity order per session while respecting limits | FR-8.2 | 3 |
| Result Tracking | Every activity returns status/timestamp/duration | FR-10 | 3 |

## Interaction Layer

| Feature | Description | Req | Phase |
|---------|-------------|-----|-------|
| Interaction Abstraction | click / type_text / scroll / move_to API | FR-9.1 | 6 |
| Mouse Controller | Movement, click, double-click, scroll | FR-9.2 | 6 |
| Keyboard Controller | Typing, key presses, Enter/Escape/Backspace/navigation | FR-9.2 | 6 |
| Visual Cursor | Custom cursor animation independent of FB logic | FR-9.3 | 6 |
| Human Interaction | Randomized, human-like behavior helpers | FR-9 | 6 |

## Observability & Data

| Feature | Description | Req | Phase |
|---------|-------------|-----|-------|
| Activity Logging | Per-profile logs + global application.log | FR-10.3 | 3 |
| SQLite Metadata | profiles / activities / sessions tables | FR-11 | 1 |
| CLI Menu | Full menu + profiles + start-automation screens | FR-12 | 1–2 |
| Error Handling | Exceptions handled per component; queue continues | FR-13 | 1+ |
| Browser Recovery | Crash → restart → reload → validate → resume/fail | FR-13.3 | 2 |
| Activity Retry | Timeout → retry → continue or log | FR-13.3 | 3 |
| Resource Management | Close idle instances, clean temp data, cap concurrency | FR-14 | 2–5 |

## Future UI (Electron)

| Feature | Description | Req | Phase |
|---------|-------------|-----|-------|
| Dashboard | Active profiles, running count, completed/failed today | NFR-5 | 7 |
| Profile Management UI | Manage profiles in a desktop UI | NFR-5 | 7 |
| Scheduler UI | Configure and control scheduling | NFR-5 | 7 |
| Activity Controls | Configure activities from the UI | NFR-5 | 7 |
| Logs UI | Browse logs in the desktop app | NFR-5 | 7 |
| Start/Stop & Mode Select | Start/stop controls; sequential/parallel selection | NFR-5 | 7 |