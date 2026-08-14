import time
import random
from typing import Dict, Any
from utils.logger import logger

class StoriesViewer:
    def __init__(self):
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation()

    def view_stories(self, profile_id: str) -> Dict[str, Any]:
        """View Facebook Stories"""
        start_time = time.time()

        try:
            logger.info("Starting to view stories", profile_id)

            if not self.navigation.navigate_to_stories(profile_id):
                return {
                    'activity_type': 'stories',
                    'status': 'FAILED',
                    'reason': 'Failed to navigate to Stories',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration': int(time.time() - start_time)
                }

            self.navigation.wait_for_page_load(profile_id)

            # View multiple stories
            stories_count = random.randint(3, 8)
            viewed = 0

            for i in range(stories_count):
                # Watch story
                watch_duration = random.uniform(3, 7)
                time.sleep(watch_duration)
                viewed += 1

                logger.info(f"Viewed story {viewed}/{stories_count}", profile_id)

                # Move to next story
                if i < stories_count - 1:
                    time.sleep(random.uniform(0.5, 1))

            duration_actual = int(time.time() - start_time)

            logger.info(f"Stories viewing completed: {viewed} stories in {duration_actual}s", profile_id)

            return {
                'activity_type': 'stories',
                'status': 'SUCCESS',
                'reason': f'Viewed {viewed} stories in {duration_actual}s',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual,
                'stories_viewed': viewed
            }

        except Exception as e:
            duration_actual = int(time.time() - start_time)
            logger.error(f"Stories viewing failed: {str(e)}", profile_id)

            return {
                'activity_type': 'stories',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual
            }
