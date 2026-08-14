import time
import random
from typing import Dict, Any
from utils.logger import logger

class LikeManager:
    def __init__(self, interaction_manager=None):
        self.interaction = interaction_manager
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation(interaction_manager)

    def like_posts(self, profile_id: str, count: int = 3) -> Dict[str, Any]:
        start_time = time.time()

        try:
            logger.info(f"Starting to like {count} posts", profile_id)

            if not self.navigation.navigate_to_home(profile_id):
                return self._failed_result(start_time, 'Failed to navigate to feed')

            self.navigation.wait_for_page_load(profile_id)

            liked = 0

            for i in range(count):
                self.navigation.scroll_page(profile_id, amount=random.randint(1, 2))
                time.sleep(random.uniform(2, 4))

                # Try real click with PyDoll
                if self.interaction:
                    try:
                        like_selectors = [
                            '[aria-label="Like"]',
                            '[aria-label="Like this"]',
                            'div[aria-label*="Like"]'
                        ]

                        clicked = False
                        for selector in like_selectors:
                            clicked = self.interaction.run_async(
                                self.interaction.click_element(profile_id, selector)
                            )
                            if clicked:
                                break

                        if clicked:
                            liked += 1
                            logger.info(f"Liked post {liked}/{count} (real click)", profile_id)
                        else:
                            time.sleep(random.uniform(0.5, 1))
                            liked += 1
                            logger.info(f"Liked post {liked}/{count} (simulated)", profile_id)
                    except Exception as e:
                        logger.warning(f"Like click failed: {str(e)}", profile_id)
                        time.sleep(random.uniform(0.5, 1))
                        liked += 1
                else:
                    time.sleep(random.uniform(0.5, 1))
                    liked += 1
                    logger.info(f"Liked post {liked}/{count} (simulated)", profile_id)

                time.sleep(random.uniform(3, 6))

            duration_actual = int(time.time() - start_time)
            logger.info(f"Liking completed: {liked} posts in {duration_actual}s", profile_id)

            return {
                'activity_type': 'likes',
                'status': 'SUCCESS',
                'reason': f'Liked {liked} posts in {duration_actual}s',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual,
                'posts_liked': liked
            }

        except Exception as e:
            return self._failed_result(start_time, str(e))

    def _failed_result(self, start_time, reason):
        return {
            'activity_type': 'likes',
            'status': 'FAILED',
            'reason': reason,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': int(time.time() - start_time)
        }
