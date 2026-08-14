import sys
import time
from typing import Optional
from core.browser_manager import BrowserManager
from core.profile_manager import ProfileManager
from core.session_manager import SessionManager
from facebook.login import FacebookLogin
from utils.logger import logger

class FacebookAutomation:
    def __init__(self):
        self.profile_manager = ProfileManager()
        self.browser_manager = BrowserManager()
        self.session_manager = SessionManager()
        self.facebook_login = FacebookLogin()

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
            print("9. Exit")
            print("\nSelect option: ", end='')

            choice = input().strip()

            if choice == '1':
                self.new_facebook_login()
            elif choice == '2':
                self.view_saved_profiles()
            elif choice == '3':
                self.validate_profiles()
            elif choice == '4':
                print("\n[Phase 2 Feature] Start Automation - Coming soon")
                input("\nPress Enter to continue...")
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
        print("\n[Phase 2 Feature] Profile validation - Coming soon")
        print("\nThis feature will re-validate saved profiles against Facebook.")
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
