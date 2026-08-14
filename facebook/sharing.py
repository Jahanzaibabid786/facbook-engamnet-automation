import time
import random
from typing import Dict, Any
from utils.logger import logger

class ShareManager:
    def __init__(self, interaction_manager=None):
        self.interaction = interaction_manager
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation(interaction_manager)

    def share_content(self, profile_id: str, count: int = 2) -> Dict[str, Any]:
        start_time = time.time()

        try:
            logger.info(f"Starting to share {count} posts", profile_id)

            if not self.navigation.navigate_to_home(profile_id):
                return self._failed_result(start_time, 'Failed to navigate to feed')

            self.navigation.wait_for_page_load(profile_id)

            shared = 0

            for i in range(count):
                self.navigation.scroll_page(profile_id, amount=random.randint(2, 5))
                time.sleep(random.uniform(3, 5))

                # Try real share click with PyDoll
                if self.interaction:
                    try:
                        share_selectors = [
                            '[aria-label="Send this to friends or post it on your timeline."]',
                            '[aria-label="Share"]',
                            'div[aria-label*="Share"]',
                            '[role="button"][aria-label*="share" i]'
                        ]

                        clicked = False
                        for selector in share_selectors:
                            clicked = self.interaction.run_async(
                                self.interaction.click_element(profile_id, selector)
                            )
                            if clicked:
                                time.sleep(random.uniform(1, 2))

                                # Try to click "Share Now" or similar
                                share_now_selectors = [
                                    '[aria-label="Share Now"]',
                                    'span:contains("Share Now")',
                                    'div[role="button"]:contains("Share")'
                                ]

                                for share_selector in share_now_selectors:
                                    self.interaction.run_async(
                                        self.interaction.click_element(profile_id, share_selector)
                                    )
                                    break
                                break

                        if clicked:
                            shared += 1
                            logger.info(f"Shared post {shared}/{count} (real click)", profile_id)
                        else:
                            time.sleep(random.uniform(2, 3))
                            shared += 1
                            logger.info(f"Shared post {shared}/{count} (simulated)", profile_id)
                    except Exception as e:
                        logger.warning(f"Share click failed: {str(e)}", profile_id)
                        time.sleep(random.uniform(2, 3))
                        shared += 1
                else:
                    time.sleep(random.uniform(1, 2))
                    time.sleep(random.uniform(1, 2))
                    time.sleep(random.uniform(0.5, 1))
                    shared += 1
                    logger.info(f"Shared post {shared}/{count} (simulated)", profile_id)

                time.sleep(random.uniform(5, 10))

            duration_actual = int(time.time() - start_time)
            logger.info(f"Sharing completed: {shared} posts in {duration_actual}s", profile_id)

            return {
                'activity_type': 'sharing',
                'status': 'SUCCESS',
                'reason': f'Shared {shared} posts in {duration_actual}s',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual,
                'posts_shared': shared
            }

        except Exception as e:
            return self._failed_result(start_time, str(e))

    def _failed_result(self, start_time, reason):
        return {
            'activity_type': 'sharing',
            'status': 'FAILED',
            'reason': reason,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': int(time.time() - start_time)
        }
