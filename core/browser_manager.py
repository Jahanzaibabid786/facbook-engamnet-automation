import json
import subprocess
import time
import psutil
from pathlib import Path
from typing import Optional, Dict, Any, List
from utils.logger import logger

class BrowserManager:
    def __init__(self, config_path: str = "config/browser.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)['browser']
        self.browser_type = self.config.get('type', 'chrome')
        self.headless = self.config.get('headless', False)
        self.arguments = self.config.get('arguments', [])
        self.facebook_url = self.config.get('facebook_url', 'https://www.facebook.com')
        self.active_instances = {}

    def launch_chrome(
        self,
        profile_path: str,
        user_agent: Optional[str] = None,
        viewport: Optional[Dict[str, int]] = None,
        profile_id: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            profile_dir = Path(profile_path).resolve()
            profile_dir.mkdir(parents=True, exist_ok=True)

            self._setup_chrome_preferences(profile_dir)

            chrome_path = self._find_chrome_executable()
            if not chrome_path:
                raise Exception("Chrome executable not found")

            args = [
                chrome_path,
                f"--user-data-dir={profile_dir}",
                f"--profile-directory=Default",
                self.facebook_url
            ]

            if user_agent:
                args.append(f"--user-agent={user_agent}")

            if viewport:
                args.append(f"--window-size={viewport['screen_width']},{viewport['screen_height']}")

            for arg in self.arguments:
                args.append(arg)

            if self.headless:
                args.append("--headless")

            logger.info(f"Launching Chrome with profile: {profile_path}", profile_id)

            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') else 0
            )

            time.sleep(3)

            if process.poll() is not None:
                raise Exception("Chrome process terminated immediately after launch")

            instance = {
                'process': process,
                'pid': process.pid,
                'profile_path': str(profile_dir),
                'profile_id': profile_id,
                'started_at': time.time()
            }

            if profile_id:
                self.active_instances[profile_id] = instance

            logger.info(f"Chrome started successfully (PID: {process.pid})", profile_id)
            return instance

        except Exception as e:
            logger.error(f"Failed to launch Chrome: {str(e)}", profile_id)
            raise

    def close_browser(self, profile_id: str) -> bool:
        try:
            if profile_id not in self.active_instances:
                logger.warning(f"No active instance found for profile: {profile_id}", profile_id)
                return False

            instance = self.active_instances[profile_id]
            process = instance['process']

            if process.poll() is None:
                logger.info(f"Closing Chrome (PID: {process.pid})", profile_id)

                try:
                    parent = psutil.Process(process.pid)
                    children = parent.children(recursive=True)

                    for child in children:
                        try:
                            child.terminate()
                        except:
                            pass

                    parent.terminate()

                    gone, alive = psutil.wait_procs([parent] + children, timeout=5)

                    for p in alive:
                        try:
                            p.kill()
                        except:
                            pass

                except Exception as e:
                    logger.warning(f"Error during graceful shutdown, forcing: {str(e)}", profile_id)
                    process.kill()

            del self.active_instances[profile_id]
            logger.info(f"Chrome closed successfully", profile_id)
            return True

        except Exception as e:
            logger.error(f"Failed to close Chrome: {str(e)}", profile_id)
            return False

    def is_browser_running(self, profile_id: str) -> bool:
        if profile_id not in self.active_instances:
            return False

        process = self.active_instances[profile_id]['process']
        return process.poll() is None

    def detect_crash(self, profile_id: str) -> bool:
        if profile_id not in self.active_instances:
            return False

        if not self.is_browser_running(profile_id):
            logger.error(f"Browser crashed for profile: {profile_id}", profile_id)
            return True

        return False

    def _find_chrome_executable(self) -> Optional[str]:
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe",
        ]

        for path in possible_paths:
            chrome_path = Path(path)
            if chrome_path.exists():
                return str(chrome_path)

        return None

    def _setup_chrome_preferences(self, profile_dir: Path):
        try:
            default_dir = profile_dir / "Default"
            default_dir.mkdir(parents=True, exist_ok=True)

            prefs_file = default_dir / "Preferences"

            # Only create preferences if they don't exist (first run)
            # Don't overwrite existing preferences as they contain session cookies
            if prefs_file.exists():
                logger.info(f"Chrome preferences already exist, preserving session data")
                return

            preferences = {
                "browser": {
                    "show_home_button": True,
                    "check_default_browser": False
                },
                "sync_promo": {
                    "show_on_first_run_allowed": False
                },
                "distribution": {
                    "skip_first_run_ui": True,
                    "show_welcome_page": False,
                    "import_bookmarks": False,
                    "import_history": False,
                    "import_search_engine": False,
                    "suppress_first_run_bubble": True,
                    "make_chrome_default_for_user": False
                },
                "first_run_tabs": [self.facebook_url],
                "profile": {
                    "default_content_setting_values": {
                        "notifications": 2
                    }
                }
            }

            with open(prefs_file, 'w') as f:
                json.dump(preferences, f, indent=2)

            local_state_file = profile_dir / "Local State"

            # Only create Local State if it doesn't exist
            if not local_state_file.exists():
                local_state = {
                    "browser": {
                        "check_default_browser": False
                    },
                    "profile": {
                        "info_cache": {}
                    }
                }

                with open(local_state_file, 'w') as f:
                    json.dump(local_state, f, indent=2)

            first_run = profile_dir / "First Run"
            if not first_run.exists():
                first_run.touch()

            logger.info(f"Chrome preferences and state files created")

        except Exception as e:
            logger.warning(f"Failed to setup Chrome preferences: {str(e)}")

    def get_instance_info(self, profile_id: str) -> Optional[Dict[str, Any]]:
        return self.active_instances.get(profile_id)

    def get_all_instances(self) -> Dict[str, Dict[str, Any]]:
        return self.active_instances.copy()
