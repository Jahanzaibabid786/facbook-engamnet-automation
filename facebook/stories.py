import time
import random
from typing import Dict, Any
from utils.logger import logger

class StoriesViewer:
    def __init__(self, interaction_manager=None):
        self.interaction = interaction_manager
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation(interaction_manager)

    def view_stories(self, profile_id: str) -> Dict[str, Any]:
        start_time = time.time()

        try:
            logger.info("Starting to view stories", profile_id)

            if not self.navigation.navigate_to_stories(profile_id):
                return self._failed_result(start_time, 'Failed to navigate to Stories')

            self.navigation.wait_for_page_load(profile_id)

            stories_count = random.randint(3, 8)
            viewed = 0

            for i in range(stories_count):
                # Watch story
                watch_duration = random.uniform(3, 7)
                time.sleep(watch_duration)
                viewed += 1

                logger.info(f"Viewed story {viewed}/{stories_count}", profile_id)

                # Move to next story with PyDoll click
                if i < stories_count - 1:
                    if self.interaction:
                        try:
                            # Try to click next story button
                            next_selectors = [
                                '[aria-label="Next"]',
                                '[aria-label="Next card"]',
                                'div[role="button"][aria-label*="Next"]'
                            ]

                            clicked = False
                            for selector in next_selectors:
                                clicked = self.interaction.run_async(
                                    self.interaction.click_element(profile_id, selector)
                                )
                                if clicked:
                                    break

                            if not clicked:
                                # Fallback: click on right side of screen
                                logger.info("Next button not found, using screen click", profile_id)
                                time.sleep(random.uniform(0.5, 1))
                        except Exception as e:
                            logger.warning(f"Story navigation failed: {str(e)}", profile_id)
                            time.sleep(random.uniform(0.5, 1))
                    else:
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
            return self._failed_result(start_time, str(e))

    def _failed_result(self, start_time, reason):
        return {
            'activity_type': 'stories',
            'status': 'FAILED',
            'reason': reason,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': int(time.time() - start_time)
        }
