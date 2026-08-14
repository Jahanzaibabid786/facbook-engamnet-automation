# Facebook Web Automation — Python + PyDoll

## 1. Project Overview

I want to build a **lightweight Facebook web automation system using Python and PyDoll**. The initial version should be a **CLI-based application**, but the architecture must be designed so that it can later be converted into a professional **Electron desktop application** without requiring the core automation engine to be rewritten.

The system will have two primary modules:

1. **Facebook Login & Profile Manager**
2. **Daily Facebook Activity Automation**

The application must support **multiple saved Facebook profiles**, profile reuse, sequential execution, optional parallel execution, Chrome instance management, lightweight profile storage, device/user-agent configuration, activity scheduling, and human-like browser interactions.

The main objective is to keep the system **simple, modular, lightweight, maintainable, and extensible**.

---

# 2. Technology Stack

## Core

* Python 3.x
* PyDoll for browser automation
* Chromium / Google Chrome
* Chrome profiles for persistent Facebook sessions
* CLI interface initially
* JSON-based configuration
* SQLite for profile/activity metadata where useful
* Async architecture where supported by PyDoll

## Future UI

The architecture should be prepared for:

* Electron
* React
* TypeScript
* Desktop dashboard
* Profile management UI
* Activity controls
* Logs
* Scheduler
* Start/Stop controls
* Sequential/Parallel mode selection

The browser automation engine should remain independent from the future Electron frontend.

---

# 3. High-Level Architecture

The project should be modular.

```text
facebook_automation/
│
├── main.py
│
├── config/
│   ├── settings.json
│   ├── devices.json
│   └── activity_config.json
│
├── core/
│   ├── browser_manager.py
│   ├── profile_manager.py
│   ├── session_manager.py
│   ├── device_manager.py
│   ├── activity_engine.py
│   ├── scheduler.py
│   └── instance_manager.py
│
├── facebook/
│   ├── login.py
│   ├── feed.py
│   ├── reels.py
│   ├── likes.py
│   ├── comments.py
│   ├── sharing.py
│   ├── stories.py
│   └── navigation.py
│
├── interaction/
│   ├── mouse.py
│   ├── keyboard.py
│   ├── cursor.py
│   └── human_interaction.py
│
├── profiles/
│   ├── profile_data/
│   └── metadata/
│
├── logs/
│
├── database/
│   └── app.db
│
└── utils/
    ├── logger.py
    ├── randomizer.py
    ├── validators.py
    └── helpers.py
```

The important point is that **browser management, profile management, Facebook activities, and interaction logic must remain separate modules**.

---

# 4. Module 1 — Facebook Login Manager

The first module handles Facebook account login and persistent session creation.

The CLI should provide an option similar to:

```text
1. New Facebook Login
2. Saved Profiles
3. Start Automation
4. Settings
5. Exit
```

When the user selects:

```text
New Facebook Login
```

the application should:

1. Create a new profile identifier.
2. Create a lightweight Chrome profile directory.
3. Launch a new Chrome instance.
4. Open Facebook.
5. Allow the user to manually log in.
6. Wait for the Facebook session to become available.
7. Allow the user to confirm that login is complete.
8. Validate that the session is actually usable.
9. Save the profile only after successful validation.
10. Close the browser cleanly.
11. Store the profile metadata.

---

# 5. Login Profile Validation

A critical requirement is that the application **must not save incomplete or broken profiles**.

For example, if:

* Chrome crashes
* Login does not complete
* Browser closes unexpectedly
* Session data is incomplete
* Facebook does not load correctly
* Required cookies/session state are missing
* Profile creation fails

then that profile should not be marked as usable.

The system should distinguish between:

```text
CREATING
LOGIN_PENDING
VALIDATING
ACTIVE
FAILED
DISABLED
```

Only:

```text
ACTIVE
```

profiles should be available to the automation engine.

---

# 6. Saved Profile Structure

Each Facebook profile should have its own isolated browser storage.

Example:

```text
profiles/
│
├── profile_001/
│   ├── chrome_data/
│   ├── metadata.json
│   └── state.json
│
├── profile_002/
│   ├── chrome_data/
│   ├── metadata.json
│   └── state.json
│
└── profile_003/
```

The metadata could contain information such as:

```json
{
    "profile_id": "profile_001",
    "name": "Facebook Account 01",
    "status": "active",
    "device_type": "android",
    "browser_type": "chrome",
    "user_agent_id": "android_01",
    "created_at": "...",
    "last_used": "...",
    "total_sessions": 12
}
```

Sensitive session information should remain inside the browser's profile storage rather than unnecessarily duplicating it into JSON.

---

# 7. Lightweight Profile Requirement

The saved Chrome profiles should be kept as lightweight as practical.

The system should avoid unnecessarily storing:

* Cache
* Temporary files
* Browser logs
* Unnecessary downloaded files
* Temporary session artifacts
* Unused browser data

The system should preserve only the browser state required for the saved Facebook session to remain usable.

The profile manager should therefore have a controlled cleanup mechanism.

Conceptually:

```text
Persistent Session Data
        +
Required Cookies
        +
Required Local Storage
        +
Required Browser Preferences
        +
Required Session State
        =
Lightweight Saved Profile
```

The system should never blindly delete browser storage that is required for session persistence.

---

# 8. Profile Usability Check

Before a saved profile is presented as usable, the application should perform a validation process.

Example:

```text
Load Profile
      ↓
Start Chrome
      ↓
Open Facebook
      ↓
Check Page
      ↓
Check Session State
      ↓
Check Account Availability
      ↓
Mark Profile
      ↓
ACTIVE / FAILED
```

A profile that repeatedly fails validation should automatically be marked:

```text
FAILED
```

or

```text
DISABLED
```

rather than continuously being used by the automation engine.

---

# 9. Device / User-Agent System

The application should have a centralized **Device Manager**.

Instead of hardcoding a user-agent string throughout the application, every profile should reference a device configuration.

Example:

```text
device_id
device_type
platform
browser
screen_size
user_agent
```

Supported device categories should include:

### Android

Examples:

* Android phone
* Small Android phone
* Medium Android phone
* Large Android phone
* Android tablet

### Windows

Examples:

* Windows 11
* Windows 10
* Windows 7

The device configuration should also control the browser viewport and related browser configuration where applicable.

Example:

```json
{
    "device_id": "android_01",
    "type": "android",
    "platform": "Android",
    "screen_width": 412,
    "screen_height": 915,
    "user_agent": "..."
}
```

The profile manager should remember which device configuration belongs to each saved profile.

---

# 10. Profile-to-Device Mapping

Each profile should have a stable configuration.

For example:

```text
Profile 001
    ↓
Android Device 01
    ↓
Android User-Agent 01
    ↓
Mobile viewport
```

Another profile:

```text
Profile 002
    ↓
Windows 11 Device 03
    ↓
Windows User-Agent 03
    ↓
Desktop viewport
```

This configuration should be managed centrally rather than duplicated across multiple scripts.

---

# 11. Browser Instance Manager

The application needs a dedicated browser-instance manager.

Its responsibility is:

* Start Chrome
* Assign profile
* Assign device configuration
* Assign viewport
* Launch the browser
* Track process
* Track window
* Close browser
* Restart browser
* Detect browser crashes
* Maintain instance state

Example:

```text
Instance Manager
       │
       ├── Profile 001 → Chrome Instance 1
       ├── Profile 002 → Chrome Instance 2
       ├── Profile 003 → Chrome Instance 3
       └── Profile 004 → Chrome Instance 4
```

---

# 12. Sequential Mode

The application must support **Sequential Mode**.

Example:

```text
Profile 001
   ↓
Start
   ↓
Daily Activities
   ↓
Close
   ↓
Profile 002
   ↓
Start
   ↓
Daily Activities
   ↓
Close
   ↓
Profile 003
```

This mode should use minimal system resources and is the preferred lightweight execution architecture.

The scheduler should be able to process profiles one by one.

---

# 13. Parallel Mode

The application should also have an optional **Parallel Mode**.

Example:

```text
             ┌── Profile 001
             │
Start ───────┼── Profile 002
             │
             ├── Profile 003
             │
             └── Profile 004
```

Each profile should have its own:

* Browser instance
* Profile directory
* Session
* Device configuration
* Activity state
* Logging context

The instance manager should maintain a maximum-concurrency setting.

Example:

```text
Max Instances: 3
```

Even if 20 profiles are selected, only three browser instances would run simultaneously.

---

# 14. Window Arrangement

The browser-instance manager should automatically arrange Chrome windows on the screen.

For example:

```text
┌───────────────┬───────────────┐
│ Chrome #1     │ Chrome #2     │
│ Profile 001   │ Profile 002   │
├───────────────┼───────────────┤
│ Chrome #3     │ Chrome #4     │
│ Profile 003   │ Profile 004   │
└───────────────┴───────────────┘
```

The arrangement engine should calculate:

* Number of active instances
* Monitor width
* Monitor height
* Window width
* Window height
* Row
* Column
* X coordinate
* Y coordinate

This should be implemented as a separate `WindowManager`.

---

# 15. Module 2 — Daily Facebook Activity Engine

The second major module is the **Daily Activity Engine**.

Its purpose is to execute a configurable sequence of Facebook activities using a saved profile.

The activity engine should not contain browser-launching code directly.

Instead:

```text
Activity Engine
       ↓
Browser Session
       ↓
Facebook Navigation
       ↓
Interaction Layer
```

This separation will make the future Electron application easier to build.

---

# 16. Daily Activity Types

The activity engine should support configurable activities such as:

### Home Feed

* Open Facebook home/feed
* Scroll through feed
* Pause between sections
* Continue browsing

### Reels

* Open Reels
* Watch several reels
* Move between reels
* Maintain configurable viewing intervals

### Likes

* Like selected feed/reel content
* Support configurable activity limits
* Record completed actions

### Sharing

* Open share interface
* Select the appropriate sharing action
* Complete the share workflow
* Record the result

### Stories

* Open story interface
* View available stories
* Support configured story activity

### Comments

* Open comment section
* Focus comment field
* Type comment
* Submit comment
* Record completion

The activity engine should treat every activity as an independent task.

---

# 17. Activity Configuration

Instead of hardcoding daily behavior, the application should use a configuration system.

Example:

```json
{
    "feed_scrolling": true,
    "reels": true,
    "likes": true,
    "comments": true,
    "sharing": true,
    "stories": true,
    "daily_limits": {
        "reels": 10,
        "likes": 3,
        "comments": 2,
        "shares": 2
    }
}
```

This makes it easy to change behavior without modifying the core engine.

---

# 18. Activity Scheduler

The activity engine should not necessarily perform every action continuously.

It should support sessions such as:

```text
Session 1
    ↓
Open Facebook
    ↓
Feed browsing
    ↓
Reels
    ↓
Close

Later

Session 2
    ↓
Open Facebook
    ↓
Feed
    ↓
Like
    ↓
Comment
    ↓
Close

Later

Session 3
    ↓
Stories
    ↓
Feed
    ↓
Share
    ↓
Close
```

The scheduler should support configurable intervals between sessions.

---

# 19. Activity Randomization

The activity configuration should allow variation.

Instead of always executing:

```text
Feed → Reel → Like → Comment → Share
```

the engine can select from configured activities.

Conceptually:

```text
Activity Pool
│
├── Feed
├── Reels
├── Like
├── Comment
├── Share
└── Story
```

The scheduler can construct a session from this pool while respecting the configured activity limits.

---

# 20. Interaction Layer

A separate interaction layer should be created because I will provide additional mouse and visual-cursor scripts later.

The architecture should support:

```text
Facebook Action
       ↓
Interaction Manager
       ↓
Mouse Controller
       ↓
Keyboard Controller
       ↓
Visual Cursor
```

The Facebook modules should not directly depend on one particular mouse implementation.

For example:

```python
interaction.click(element)
interaction.type_text(text)
interaction.scroll(amount)
interaction.move_to(element)
```

The underlying implementation can later be replaced.

---

# 21. Visual Cursor Integration

The system should support a custom visual cursor mechanism.

For example:

```text
Move Cursor
     ↓
Visual Cursor Animation
     ↓
Mouse Position
     ↓
Click
```

The cursor module should be independent from Facebook-specific logic.

Therefore, if a Facebook module needs to click a Share button, it should request:

```text
InteractionManager.click(share_button)
```

rather than implementing cursor behavior itself.

This allows the custom visual-cursor script to be integrated later without changing Facebook activity modules.

---

# 22. Keyboard Interaction

The interaction system should support:

* Click
* Double click
* Mouse movement
* Scroll
* Keyboard typing
* Key presses
* Text entry
* Enter
* Escape
* Backspace
* Navigation keys

Example flow:

```text
Find Comment Field
        ↓
Click
        ↓
Focus
        ↓
Type Text
        ↓
Press Enter
        ↓
Verify Result
```

---

# 23. Facebook Navigation Layer

Facebook-specific navigation should be separated into reusable functions.

Example:

```python
open_facebook()
open_home()
open_reels()
open_stories()
find_feed_content()
find_reel()
find_like_button()
find_comment_box()
find_share_button()
```

This prevents the main activity engine from becoming a huge script.

---

# 24. Activity Result Tracking

Every activity should return a result.

Example:

```python
{
    "profile_id": "profile_001",
    "activity": "reel_watch",
    "status": "success",
    "timestamp": "...",
    "duration": 42
}
```

Possible states:

```text
SUCCESS
FAILED
SKIPPED
TIMEOUT
NOT_FOUND
SESSION_ERROR
```

---

# 25. Logging System

Every profile should have a separate activity log.

Example:

```text
logs/
│
├── profile_001.log
├── profile_002.log
└── profile_003.log
```

The global application log should also exist:

```text
logs/application.log
```

CLI output could look like:

```text
[09:10:22] Profile 001 loaded
[09:10:24] Chrome started
[09:10:28] Facebook session detected
[09:10:35] Feed session started
[09:11:02] Reels activity completed
[09:11:35] Profile session completed
```

---

# 26. Profile Database

SQLite can maintain lightweight metadata.

Suggested tables:

### profiles

```text
id
profile_name
profile_path
status
device_id
created_at
last_used
last_validated
```

### activities

```text
id
profile_id
activity_type
status
timestamp
duration
```

### sessions

```text
id
profile_id
started_at
ended_at
status
```

The database should store metadata, not unnecessarily duplicate browser session information.

---

# 27. CLI Interface

The initial CLI should be simple.

Example:

```text
========================================
 Facebook Automation System
========================================

1. New Facebook Login
2. View Saved Profiles
3. Validate Profiles
4. Start Automation
5. Activity Settings
6. Device Settings
7. Browser Settings
8. Logs
9. Exit

Select option:
```

---

# 28. Saved Profiles Interface

Example:

```text
Saved Facebook Profiles

ID       Name              Device       Status
------------------------------------------------
001      Account 01        Android      ACTIVE
002      Account 02        Windows 11   ACTIVE
003      Account 03        Android      FAILED
004      Account 04        Windows 10   ACTIVE
```

The user should be able to:

```text
Select Profiles
Validate
Rename
Disable
Delete
Test
Start
```

---

# 29. Start Automation Interface

Example:

```text
Select Execution Mode:

1. Sequential
2. Parallel

Select Profiles:

[1] Account 01
[2] Account 02
[3] Account 03
[4] Account 04

Select Device Configuration:

Automatic / Profile Default

Start? Y/N
```

---

# 30. Profile Lifecycle

The complete lifecycle should be:

```text
Create Profile
      ↓
Launch Chrome
      ↓
Facebook Login
      ↓
Validate Login
      ↓
Save Session
      ↓
Validate Saved Profile
      ↓
ACTIVE
      ↓
Use Profile
      ↓
Daily Automation
      ↓
Update Last Used
      ↓
Next Session
```

If validation fails:

```text
Create
  ↓
Login
  ↓
Validation Failed
  ↓
FAILED
  ↓
Do Not Include in Active Automation
```

---

# 31. Error Handling

Every major component should have proper exception handling.

Examples:

```text
Chrome failed to start
Profile directory unavailable
Facebook page timeout
Session unavailable
Element not found
Interaction failed
Browser crashed
Window arrangement failed
Activity timeout
```

The system should log the error and continue with the next profile where appropriate.

A single failed profile should not unnecessarily terminate the entire automation queue.

---

# 32. Recovery System

The automation engine should support recovery.

Example:

```text
Profile 001
   ↓
Browser Crash
   ↓
Detect Crash
   ↓
Restart Instance
   ↓
Reload Profile
   ↓
Validate Session
   ↓
Resume / Mark Failed
```

Similarly:

```text
Activity Timeout
      ↓
Retry
      ↓
If successful → Continue
      ↓
If failed → Log
      ↓
Continue Next Activity
```

---

# 33. Resource Management

Because the system should remain lightweight, resource management is important.

The application should:

* Avoid unnecessary browser instances
* Close inactive sessions
* Clean temporary browser artifacts
* Avoid loading unnecessary components
* Use sequential mode when possible
* Limit parallel instances
* Avoid excessive memory usage
* Keep the CLI engine lightweight
* Separate persistent data from temporary data

The browser instance manager should always know:

```text
How many browsers are running?
Which profile owns each browser?
Which device configuration is active?
When was the instance started?
When should it be closed?
```

---

# 34. Configuration Architecture

All configurable values should be centralized.

Example:

```text
config/
│
├── settings.json
├── devices.json
├── activities.json
├── scheduler.json
└── browser.json
```

This allows future Electron UI controls to modify configuration without changing Python source code.

---

# 35. Future Electron Architecture

The final architecture should eventually look like:

```text
Electron Frontend
        │
        │ IPC / Local API
        ↓
Python Automation Engine
        │
        ├── Profile Manager
        ├── Browser Manager
        ├── Device Manager
        ├── Activity Engine
        ├── Scheduler
        ├── Interaction Manager
        └── Logger
```

The Electron application would provide:

```text
Dashboard
Profiles
Devices
Activities
Scheduler
Running Instances
Logs
Settings
```

The Python engine should remain the actual automation backend.

---

# 36. Future Dashboard Concept

The future desktop application could contain:

```text
┌──────────────────────────────────────────┐
│ Facebook Automation                      │
├────────────┬─────────────────────────────┤
│ Dashboard  │ Active Profiles: 5          │
│ Profiles   │ Running: 2                  │
│ Activities │ Completed Today: 31         │
│ Scheduler  │ Failed: 1                   │
│ Devices    │                             │
│ Logs       │ [Start] [Stop]              │
│ Settings   │                             │
└────────────┴─────────────────────────────┘
```

The CLI version should therefore use clean internal APIs so that the Electron frontend can later call the same functionality.

---

# 37. Core Design Principle

The most important architectural principle is:

```text
UI ≠ Automation Engine
Browser ≠ Facebook Logic
Facebook Logic ≠ Interaction Logic
Profile ≠ Activity
Device ≠ Profile
Scheduler ≠ Browser
```

Each component should have one clear responsibility.

For example:

```text
ProfileManager
    manages profiles

BrowserManager
    manages Chrome

DeviceManager
    manages device configurations

FacebookManager
    manages Facebook navigation

ActivityEngine
    manages activities

InteractionManager
    manages mouse/keyboard interaction

Scheduler
    manages timing

Logger
    manages logs
```

This will make the project much easier to maintain and eventually convert into an Electron application.

---

# 38. Complete Workflow

The complete system should ultimately work like this:

```text
                    APPLICATION
                         │
             ┌───────────┴───────────┐
             │                       │
        LOGIN MANAGER          AUTOMATION ENGINE
             │                       │
       New Facebook Login       Select Profiles
             │                       │
       Launch Chrome            Select Mode
             │                       │
       Manual Login             Sequential/Parallel
             │                       │
       Validate Session              │
             │                       │
       Save Profile                  │
             │                       │
             └───────────┬───────────┘
                         │
                  Browser Manager
                         │
              ┌──────────┴──────────┐
              │                     │
          Profile 001           Profile 002
              │                     │
          Device Config         Device Config
              │                     │
          Facebook Session      Facebook Session
              │                     │
              └──────────┬──────────┘
                         │
                  Activity Engine
                         │
       ┌─────────┬───────┼───────┬─────────┐
       │         │       │       │         │
      Feed     Reels   Likes  Comments   Stories
       │         │       │       │         │
       └─────────┴───────┴───────┴─────────┘
                         │
                 Interaction Layer
                         │
              Mouse + Keyboard +
                 Visual Cursor
                         │
                       Logs
```

---

# 39. Initial Development Priority

The first implementation should remain CLI-based and lightweight.

### Phase 1

```text
Python Project
    ↓
PyDoll
    ↓
Chrome Launch
    ↓
New Login
    ↓
Profile Save
    ↓
Profile Validation
```

### Phase 2

```text
Multiple Profiles
    ↓
Profile Selection
    ↓
Sequential Execution
    ↓
Browser Instance Manager
```

### Phase 3

```text
Facebook Activity Engine
    ↓
Feed
    ↓
Reels
    ↓
Likes
    ↓
Comments
    ↓
Sharing
    ↓
Stories
```

### Phase 4

```text
Device Manager
    ↓
User-Agent Configuration
    ↓
Viewport Configuration
    ↓
Profile-to-Device Mapping
```

### Phase 5

```text
Parallel Mode
    ↓
Multiple Chrome Instances
    ↓
Window Manager
    ↓
Resource Limiting
```

### Phase 6

```text
Interaction Layer
    ↓
Custom Mouse Scripts
    ↓
Keyboard Scripts
    ↓
Visual Cursor Integration
```

### Phase 7

```text
Electron Frontend
    ↓
Dashboard
    ↓
Profile Manager
    ↓
Scheduler
    ↓
Activity Manager
    ↓
Logs
```

---

# 40. Final Product Goal

The final product should be a **modular Facebook browser-automation platform** built around Python and PyDoll.

Its core capabilities will be:

* Multiple Facebook profile management
* Persistent saved Chrome sessions
* Lightweight profile storage
* Profile validation
* Device configuration
* User-agent configuration
* Android and Windows device profiles
* Sequential automation
* Parallel automation
* Multiple Chrome instances
* Automatic window arrangement
* Daily activity engine
* Feed browsing
* Reels activity
* Likes
* Comments
* Sharing
* Stories
* Configurable scheduling
* Activity logging
* Session tracking
* Error handling
* Browser recovery
* Custom mouse interaction
* Keyboard interaction
* Visual cursor integration
* CLI-first architecture
* Electron-ready backend architecture

The codebase should remain **simple, modular, lightweight, and extensible**, with the Python/PyDoll automation engine completely separated from the future desktop UI layer.


Before writing any project code, initialize a Git repository and connect it to a GitHub repository.

Configure automatic version-control workflow:

* Create the GitHub repository if it does not exist.
* Create a proper `.gitignore`.
* Make an initial commit before coding.
* After every meaningful feature, fix, or milestone, create a clear commit.
* Automatically push commits to GitHub.
* Use meaningful commit messages and version tags where appropriate.
* Keep the project history clean so previous working versions can be restored easily.
* Never overwrite or delete working history unnecessarily.
* Before major changes, create a checkpoint commit/tag.
* Make rollback/revert easy so the project can safely move backward or forward between versions.
* Keep Git/GitHub integration separate from the application logic.
* Document the Git workflow in `docs/37_CHANGELOG.md`.

The goal is to maintain a continuously backed-up, versioned GitHub repository throughout development, with reliable undo/rollback and clear version history.
