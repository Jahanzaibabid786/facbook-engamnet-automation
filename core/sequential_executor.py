import time
from typing import List, Dict, Any, Optional
from core.browser_manager import BrowserManager
from core.profile_manager import ProfileManager
from core.session_manager import SessionManager
from utils.logger import logger
from utils.database import Database

class SequentialExecutor:
    def __init__(self):
        self.browser_manager = BrowserManager()
        self.profile_manager = ProfileManager()
        self.session_manager = SessionManager()
        self.db = Database()

    def execute_profiles(self, profile_ids: List[str], activity_config: Optional[Dict] = None) -> Dict[str, Any]:
        results = {
            'total': len(profile_ids),
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'profile_results': []
        }

        logger.info(f"Starting sequential execution for {len(profile_ids)} profiles")

        for index, profile_id in enumerate(profile_ids, 1):
            print(f"\n{'='*60}")
            print(f" Processing Profile {index}/{len(profile_ids)}")
            print(f"{'='*60}")

            try:
                profile = self.profile_manager.get_profile(profile_id)

                if not profile:
                    logger.warning(f"Profile not found: {profile_id}")
                    results['skipped'] += 1
                    results['profile_results'].append({
                        'profile_id': profile_id,
                        'status': 'SKIPPED',
                        'reason': 'Profile not found'
                    })
                    continue

                if profile['status'] != 'ACTIVE':
                    logger.warning(f"Profile {profile_id} is not ACTIVE (status: {profile['status']}), skipping")
                    results['skipped'] += 1
                    results['profile_results'].append({
                        'profile_id': profile_id,
                        'status': 'SKIPPED',
                        'reason': f"Status is {profile['status']}, not ACTIVE"
                    })
                    continue

                print(f"\nProfile: {profile['profile_name']}")
                print(f"ID: {profile_id}")
                print(f"Status: {profile['status']}")

                session_id = self.db.insert_session({
                    'profile_id': profile_id,
                    'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'RUNNING'
                })

                result = self._execute_single_profile(profile, session_id, activity_config)

                self.db.update_session(session_id, {
                    'ended_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': result['status']
                })

                if result['status'] == 'SUCCESS':
                    results['successful'] += 1
                else:
                    results['failed'] += 1

                results['profile_results'].append(result)

                self.profile_manager.update_profile_last_used(profile_id)

            except Exception as e:
                logger.error(f"Error processing profile {profile_id}: {str(e)}", profile_id)
                results['failed'] += 1
                results['profile_results'].append({
                    'profile_id': profile_id,
                    'status': 'FAILED',
                    'reason': str(e)
                })

        logger.info(f"Sequential execution completed: {results['successful']} successful, {results['failed']} failed, {results['skipped']} skipped")

        return results

    def _execute_single_profile(self, profile: Dict[str, Any], session_id: int, activity_config: Optional[Dict]) -> Dict[str, Any]:
        profile_id = profile['profile_id']
        profile_path = profile['profile_path']

        try:
            print(f"\n[{time.strftime('%H:%M:%S')}] Launching browser...")
            logger.info(f"Launching browser for profile", profile_id)

            browser_instance = self.browser_manager.launch_chrome(
                profile_path=profile_path,
                profile_id=profile_id
            )

            time.sleep(3)

            if self.browser_manager.detect_crash(profile_id):
                logger.error(f"Browser crashed immediately after launch", profile_id)
                return {
                    'profile_id': profile_id,
                    'status': 'FAILED',
                    'reason': 'Browser crashed during launch'
                }

            print(f"[{time.strftime('%H:%M:%S')}] Browser launched successfully")

            print(f"[{time.strftime('%H:%M:%S')}] Validating session...")
            validation_result = self.session_manager.validate_session(profile_id)

            if not validation_result['valid']:
                logger.error(f"Session validation failed: {validation_result.get('error')}", profile_id)
                self.browser_manager.close_browser(profile_id)
                return {
                    'profile_id': profile_id,
                    'status': 'FAILED',
                    'reason': f"Session validation failed: {validation_result.get('error', 'Unknown')}"
                }

            print(f"[{time.strftime('%H:%M:%S')}] Session validated successfully")

            print(f"[{time.strftime('%H:%M:%S')}] Running activities...")
            logger.info(f"Starting activities for profile", profile_id)

            time.sleep(5)

            print(f"[{time.strftime('%H:%M:%S')}] Activities completed (Phase 3 placeholder)")

            print(f"[{time.strftime('%H:%M:%S')}] Closing browser...")
            self.browser_manager.close_browser(profile_id)

            logger.info(f"Profile execution completed successfully", profile_id)

            return {
                'profile_id': profile_id,
                'status': 'SUCCESS',
                'reason': 'Completed successfully'
            }

        except Exception as e:
            logger.error(f"Error during profile execution: {str(e)}", profile_id)

            try:
                self.browser_manager.close_browser(profile_id)
            except:
                pass

            return {
                'profile_id': profile_id,
                'status': 'FAILED',
                'reason': str(e)
            }

    def recover_from_crash(self, profile_id: str) -> bool:
        try:
            logger.warning(f"Attempting recovery from crash", profile_id)

            profile = self.profile_manager.get_profile(profile_id)
            if not profile:
                logger.error(f"Profile not found for recovery", profile_id)
                return False

            try:
                self.browser_manager.close_browser(profile_id)
            except:
                pass

            time.sleep(2)

            print(f"\n[{time.strftime('%H:%M:%S')}] Attempting to restart browser...")
            browser_instance = self.browser_manager.launch_chrome(
                profile_path=profile['profile_path'],
                profile_id=profile_id
            )

            time.sleep(3)

            if self.browser_manager.detect_crash(profile_id):
                logger.error(f"Browser crashed again after recovery attempt", profile_id)
                return False

            validation_result = self.session_manager.validate_session(profile_id)

            if not validation_result['valid']:
                logger.error(f"Session validation failed after recovery", profile_id)
                self.browser_manager.close_browser(profile_id)
                return False

            logger.info(f"Recovery successful", profile_id)
            print(f"[{time.strftime('%H:%M:%S')}] Recovery successful")
            return True

        except Exception as e:
            logger.error(f"Recovery failed: {str(e)}", profile_id)
            return False
