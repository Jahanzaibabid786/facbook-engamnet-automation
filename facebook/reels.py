import time
import random
from typing import Dict, Any
from utils.logger import logger

class ReelsWatcher:
    def __init__(self):
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation()

    def watch_reels(self, profile_id: str, count: int = 10) -> Dict[str, Any]:
        """Watch Facebook Reels"""
        start_time = time.time()

        try:
            logger.info(f"Starting to watch {count} reels", profile_id)

            if not self.navigation.navigate_to_reels(profile_id):
                return {
                    'activity_type': 'reels',
                    'status': 'FAILED',
                    'reason': 'Failed to navigate to Reels',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration': int(time.time() - start_time)
                }

            self.navigation.wait_for_page_load(profile_id)

            watched = 0

            for i in range(count):
                # Watch current reel
                watch_duration = random.uniform(5, 15)
                time.sleep(watch_duration)
                watched += 1

                logger.info(f"Watched reel {watched}/{count}", profile_id)

                # Move to next reel (scroll or swipe)
                if i < count - 1:
                    self.navigation.scroll_page(profile_id)
                    time.sleep(random.uniform(1, 2))

            duration_actual = int(time.time() - start_time)

            logger.info(f"Reels watching completed: {watched} reels in {duration_actual}s", profile_id)

            return {
                'activity_type': 'reels',
                'status': 'SUCCESS',
                'reason': f'Watched {watched} reels in {duration_actual}s',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual,
                'reels_watched': watched
            }

        except Exception as e:
            duration_actual = int(time.time() - start_time)
            logger.error(f"Reels watching failed: {str(e)}", profile_id)

            return {
                'activity_type': 'reels',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual
            }
