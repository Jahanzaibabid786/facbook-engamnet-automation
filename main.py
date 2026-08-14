import sys
import time
from typing import Optional, List
from core.browser_manager import BrowserManager
from core.profile_manager import ProfileManager
from core.session_manager import SessionManager
from core.sequential_executor import SequentialExecutor
from facebook.login import FacebookLogin
from utils.logger import logger
from utils.profile_cleaner import ProfileCleaner

class FacebookAutomation:
    def __init__(self):
        self.profile_manager = ProfileManager()
        self.browser_manager = BrowserManager()
        self.session_manager = SessionManager()
        self.facebook_login = FacebookLogin()
        self.sequential_executor = SequentialExecutor()

    def show_main_menu(self):
        while True:
            print("\n" + "="*60)
            print(" Facebook Automation System")
            print("="*60)
            print("\n1. New Facebook Login")
            print("2. View Saved Profiles")
            print("3. Validate Profiles")
            print("4. Start Automation")
            print("5. Activity Settings")
            print("6. Device Settings")
            print("7. Browser Settings")
            print("8. Logs")
            print("9. Clean All Profiles")
            print("0. Exit")
            print("\nSelect option: ", end='')

            choice = input().strip()

            if choice == '1':
                self.new_facebook_login()
            elif choice == '2':
                self.view_saved_profiles()
            elif choice == '3':
                self.validate_profiles()
            elif choice == '4':
                self.start_automation()
            elif choice == '5':
                print("\n[Phase 3 Feature] Activity Settings - Coming soon")
                input("\nPress Enter to continue...")
            elif choice == '6':
                print("\n[Phase 4 Feature] Device Settings - Coming soon")
                input("\nPress Enter to continue...")
            elif choice == '7':
                print("\n[Phase 1 Feature] Browser Settings - Coming soon")
                input("\nPress Enter to continue...")
            elif choice == '8':
                print("\n[Phase 1 Feature] Logs Viewer - Coming soon")
                input("\nPress Enter to continue...")
            elif choice == '9':
                self.clean_all_profiles()
            elif choice == '0':
                print("\nExiting...")
                sys.exit(0)
            else:
                print("\nInvalid option. Please try again.")
                input("\nPress Enter to continue...")

    def new_facebook_login(self):
        try:
            print("\n" + "="*60)
            print(" New Facebook Login")
            print("="*60)

            print("\nEnter profile name: ", end='')
            profile_name = input().strip()

            if not profile_name:
                print("\nProfile name cannot be empty.")
                input("\nPress Enter to continue...")
                return

            logger.info(f"Starting new Facebook login: {profile_name}")

            print("\nCreating profile...")
            profile_data = self.profile_manager.create_profile(profile_name)
            profile_id = profile_data['profile_id']
            profile_path = profile_data['profile_path']

            logger.info(f"Profile created: {profile_id}", profile_id)

            self.profile_manager.update_profile_status(profile_id, 'LOGIN_PENDING')

            print(f"\nLaunching Chrome for profile: {profile_id}")
            browser_instance = self.browser_manager.launch_chrome(
                profile_path=profile_path,
                profile_id=profile_id
            )

            time.sleep(3)

            if self.browser_manager.detect_crash(profile_id):
                logger.error(f"Browser crashed during launch", profile_id)
                self.profile_manager.update_profile_status(
                    profile_id,
                    'FAILED',
                    'Browser crashed during launch'
                )
                print("\nBrowser crashed. Profile marked as FAILED.")
                input("\nPress Enter to continue...")
                return

            login_result = self.facebook_login.wait_for_manual_login(
                profile_id=profile_id,
                timeout=300
            )

            if not login_result['success']:
                logger.error(f"Login failed or timed out", profile_id)
                self.profile_manager.update_profile_status(
                    profile_id,
                    'FAILED',
                    'Login failed or timed out'
                )
                self.browser_manager.close_browser(profile_id)
                print("\nLogin failed. Profile marked as FAILED.")
                input("\nPress Enter to continue...")
                return

            print("\nVerifying login...")
            login_verified = self.facebook_login.verify_login_success(profile_id)

            if not login_verified:
                logger.error(f"Login verification failed", profile_id)
                self.profile_manager.update_profile_status(
                    profile_id,
                    'FAILED',
                    'Login verification failed'
                )
                self.browser_manager.close_browser(profile_id)
                print("\nLogin verification failed. Profile marked as FAILED.")
                input("\nPress Enter to continue...")
                return

            print("\nValidating session...")
            self.profile_manager.update_profile_status(profile_id, 'VALIDATING')

            validation_result = self.session_manager.validate_session(profile_id)

            if not validation_result['valid']:
                logger.error(f"Session validation failed", profile_id)
                self.profile_manager.update_profile_status(
                    profile_id,
                    'FAILED',
                    f"Session validation failed: {validation_result.get('error', 'Unknown error')}"
                )
                self.browser_manager.close_browser(profile_id)
                print("\nSession validation failed. Profile marked as FAILED.")
                input("\nPress Enter to continue...")
                return

            self.profile_manager.update_profile_status(profile_id, 'ACTIVE')
            logger.info(f"Profile successfully saved as ACTIVE", profile_id)

            print("\n" + "="*60)
            print(" Profile Saved Successfully!")
            print("="*60)
            print(f"\nProfile ID: {profile_id}")
            print(f"Profile Name: {profile_name}")
            print(f"Status: ACTIVE")

            print("\nClosing browser...")
            self.browser_manager.close_browser(profile_id)

            self.profile_manager.cleanup_profile(profile_id)

            logger.info(f"New login flow completed successfully", profile_id)

            input("\nPress Enter to continue...")

        except Exception as e:
            logger.error(f"Error during new Facebook login: {str(e)}")
            print(f"\nError: {str(e)}")
            input("\nPress Enter to continue...")

    def view_saved_profiles(self):
        print("\n" + "="*60)
        print(" Saved Facebook Profiles")
        print("="*60)

        profiles = self.profile_manager.get_all_profiles()

        if not profiles:
            print("\nNo saved profiles found.")
            input("\nPress Enter to continue...")
            return

        print(f"\n{'ID':<15} {'Name':<25} {'Status':<15} {'Created':<20}")
        print("-" * 75)

        for profile in profiles:
            profile_id = profile['profile_id']
            name = profile['profile_name'][:24]
            status = profile['status']
            created = profile['created_at'][:19] if profile['created_at'] else 'N/A'

            print(f"{profile_id:<15} {name:<25} {status:<15} {created:<20}")

        input("\nPress Enter to continue...")

    def validate_profiles(self):
        print("\n" + "="*60)
        print(" Validate Profiles")
        print("="*60)

        profiles = self.profile_manager.get_all_profiles()

        if not profiles:
            print("\nNo profiles found.")
            input("\nPress Enter to continue...")
            return

        print("\nSelect profiles to validate:")
        print("\n0. All profiles")

        for idx, profile in enumerate(profiles, 1):
            print(f"{idx}. {profile['profile_name']} ({profile['profile_id']}) - {profile['status']}")

        print("\nEnter selection (comma-separated, e.g., 1,3,5 or 0 for all): ", end='')
        selection = input().strip()

        if not selection:
            print("\nNo selection made.")
            input("\nPress Enter to continue...")
            return

        selected_profiles = []

        if selection == '0':
            selected_profiles = [p['profile_id'] for p in profiles]
        else:
            try:
                indices = [int(x.strip()) for x in selection.split(',')]
                for idx in indices:
                    if 1 <= idx <= len(profiles):
                        selected_profiles.append(profiles[idx - 1]['profile_id'])
            except ValueError:
                print("\nInvalid selection format.")
                input("\nPress Enter to continue...")
                return

        if not selected_profiles:
            print("\nNo valid profiles selected.")
            input("\nPress Enter to continue...")
            return

        print(f"\nValidating {len(selected_profiles)} profile(s)...")

        for profile_id in selected_profiles:
            profile = self.profile_manager.get_profile(profile_id)
            print(f"\nValidating: {profile['profile_name']} ({profile_id})")

            try:
                browser_instance = self.browser_manager.launch_chrome(
                    profile_path=profile['profile_path'],
                    profile_id=profile_id
                )

                time.sleep(3)

                if self.browser_manager.detect_crash(profile_id):
                    print(f"  Status: FAILED (Browser crashed)")
                    self.profile_manager.update_profile_status(profile_id, 'FAILED', 'Browser crashed during validation')
                    continue

                validation_result = self.session_manager.validate_session(profile_id)

                if validation_result['valid']:
                    print(f"  Status: ACTIVE (Session valid)")
                    self.profile_manager.update_profile_status(profile_id, 'ACTIVE')
                else:
                    print(f"  Status: FAILED ({validation_result.get('error', 'Unknown error')})")
                    self.profile_manager.update_profile_status(profile_id, 'FAILED', validation_result.get('error'))

                self.browser_manager.close_browser(profile_id)
                time.sleep(1)

            except Exception as e:
                print(f"  Status: FAILED ({str(e)})")
                self.profile_manager.update_profile_status(profile_id, 'FAILED', str(e))
                try:
                    self.browser_manager.close_browser(profile_id)
                except:
                    pass

        print("\nValidation completed.")
        input("\nPress Enter to continue...")

    def start_automation(self):
        print("\n" + "="*60)
        print(" Start Automation - Sequential Execution")
        print("="*60)

        profiles = self.profile_manager.get_all_profiles(status='ACTIVE')

        if not profiles:
            print("\nNo ACTIVE profiles found.")
            print("\nTip: Create profiles using 'New Facebook Login' and ensure they pass validation.")
            input("\nPress Enter to continue...")
            return

        print(f"\nFound {len(profiles)} ACTIVE profile(s):")

        for idx, profile in enumerate(profiles, 1):
            last_used = profile.get('last_used', 'Never')
            if last_used and last_used != 'Never':
                last_used = last_used[:19]
            sessions = profile.get('total_sessions', 0)
            print(f"{idx}. {profile['profile_name']} - Last used: {last_used} - Sessions: {sessions}")

        print("\nSelect profiles to run (comma-separated, e.g., 1,2,3 or 0 for all): ", end='')
        selection = input().strip()

        if not selection:
            print("\nNo selection made.")
            input("\nPress Enter to continue...")
            return

        selected_profile_ids = []

        if selection == '0':
            selected_profile_ids = [p['profile_id'] for p in profiles]
        else:
            try:
                indices = [int(x.strip()) for x in selection.split(',')]
                for idx in indices:
                    if 1 <= idx <= len(profiles):
                        selected_profile_ids.append(profiles[idx - 1]['profile_id'])
            except ValueError:
                print("\nInvalid selection format.")
                input("\nPress Enter to continue...")
                return

        if not selected_profile_ids:
            print("\nNo valid profiles selected.")
            input("\nPress Enter to continue...")
            return

        print(f"\n{'='*60}")
        print(f" Executing {len(selected_profile_ids)} Profile(s) Sequentially")
        print(f"{'='*60}")
        print("\nNote: Daily activities will be added in Phase 3.")
        print("      This run validates sessions and demonstrates sequential execution.\n")

        print("Press Enter to start or Ctrl+C to cancel: ", end='')
        input()

        start_time = time.time()

        results = self.sequential_executor.execute_profiles(selected_profile_ids)

        elapsed_time = time.time() - start_time

        print(f"\n{'='*60}")
        print(" Execution Summary")
        print(f"{'='*60}")
        print(f"\nTotal profiles: {results['total']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
        print(f"Skipped: {results['skipped']}")
        print(f"Total time: {int(elapsed_time)}s")

        print("\nDetails:")
        for result in results['profile_results']:
            print(f"  {result['profile_id']}: {result['status']} - {result.get('reason', 'N/A')}")

        input("\nPress Enter to continue...")

    def clean_all_profiles(self):
        print("\n" + "="*60)
        print(" Clean All Profiles")
        print("="*60)
        print("\n⚠️  WARNING: This will permanently delete ALL profiles!")
        print("   - All profile data and Chrome profiles")
        print("   - All profile metadata")
        print("   - All activity and session history")
        print("\nThis action CANNOT be undone.")
        print("\nType 'DELETE' to confirm: ", end='')

        confirmation = input().strip()

        if confirmation != 'DELETE':
            print("\nCancelled. No profiles were deleted.")
            input("\nPress Enter to continue...")
            return

        print("\nCleaning all profiles...")

        try:
            cleaner = ProfileCleaner()
            success = cleaner.clean_all_profiles()

            if success:
                print("\n✅ All profiles cleaned successfully!")
                logger.info("All profiles cleaned by user")
            else:
                print("\n❌ Failed to clean profiles. Check logs for details.")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            logger.error(f"Failed to clean profiles: {str(e)}")

        input("\nPress Enter to continue...")


def main():
    try:
        print("\n" + "="*60)
        print(" Facebook Web Automation - Phase 1")
        print(" Python + PyDoll")
        print("="*60)
        print("\nInitializing...")

        app = FacebookAutomation()

        logger.info("Application started")

        app.show_main_menu()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
