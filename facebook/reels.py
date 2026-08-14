import time
import random
from typing import Dict, Any
from utils.logger import logger

class ReelsWatcher:
    def __init__(self, interaction_manager=None):
        self.interaction = interaction_manager
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation(interaction_manager)

    def watch_reels(self, profile_id: str, count: int = 10) -> Dict[str, Any]:
        start_time = time.time()

        try:
            logger.info(f"Starting to watch {count} reels", profile_id)

            if not self.navigation.navigate_to_reels(profile_id):
                return self._failed_result(start_time, 'Failed to navigate to Reels')

            self.navigation.wait_for_page_load(profile_id)

            watched = 0

            for i in range(count):
                # Watch current reel
                watch_duration = random.uniform(5, 15)
                time.sleep(watch_duration)
                watched += 1

                logger.info(f"Watched reel {watched}/{count}", profile_id)

                # Scroll to next reel with PyDoll
                if i < count - 1:
                    self.navigation.scroll_page(profile_id, amount=1)
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
            return self._failed_result(start_time, str(e))

    def _failed_result(self, start_time, reason):
        return {
            'activity_type': 'reels',
            'status': 'FAILED',
            'reason': reason,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': int(time.time() - start_time)
        }
