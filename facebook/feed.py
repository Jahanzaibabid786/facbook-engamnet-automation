import time
import random
from typing import Dict, Any
from utils.logger import logger

class FeedBrowser:
    def __init__(self):
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation()

    def browse_feed(self, profile_id: str, duration: int = 30) -> Dict[str, Any]:
        """Browse Facebook feed by scrolling and pausing"""
        start_time = time.time()

        try:
            logger.info(f"Starting feed browsing for {duration} seconds", profile_id)

            if not self.navigation.navigate_to_home(profile_id):
                return {
                    'activity_type': 'feed_browsing',
                    'status': 'FAILED',
                    'reason': 'Failed to navigate to home',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration': int(time.time() - start_time)
                }

            self.navigation.wait_for_page_load(profile_id)

            # Simulate browsing: scroll, pause, scroll
            elapsed = 0
            scrolls = 0

            while elapsed < duration:
                # Scroll
                self.navigation.scroll_page(profile_id, amount=random.randint(1, 3))
                scrolls += 1

                # Pause to "read"
                pause_time = random.uniform(3, 7)
                time.sleep(pause_time)

                elapsed = time.time() - start_time

            duration_actual = int(time.time() - start_time)

            logger.info(f"Feed browsing completed: {scrolls} scrolls, {duration_actual}s", profile_id)

            return {
                'activity_type': 'feed_browsing',
                'status': 'SUCCESS',
                'reason': f'Completed {scrolls} scrolls in {duration_actual}s',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual,
                'scrolls': scrolls
            }

        except Exception as e:
            duration_actual = int(time.time() - start_time)
            logger.error(f"Feed browsing failed: {str(e)}", profile_id)

            return {
                'activity_type': 'feed_browsing',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual
            }
