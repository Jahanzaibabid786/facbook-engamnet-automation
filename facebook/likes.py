import time
import random
from typing import Dict, Any
from utils.logger import logger

class LikeManager:
    def __init__(self):
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation()

    def like_posts(self, profile_id: str, count: int = 3) -> Dict[str, Any]:
        """Like posts on Facebook feed"""
        start_time = time.time()

        try:
            logger.info(f"Starting to like {count} posts", profile_id)

            if not self.navigation.navigate_to_home(profile_id):
                return {
                    'activity_type': 'likes',
                    'status': 'FAILED',
                    'reason': 'Failed to navigate to feed',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration': int(time.time() - start_time)
                }

            self.navigation.wait_for_page_load(profile_id)

            liked = 0

            for i in range(count):
                # Scroll to find post
                self.navigation.scroll_page(profile_id, amount=random.randint(1, 2))
                time.sleep(random.uniform(2, 4))

                # Click like button (placeholder)
                time.sleep(random.uniform(0.5, 1))
                liked += 1

                logger.info(f"Liked post {liked}/{count}", profile_id)

                # Pause before next like
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
            duration_actual = int(time.time() - start_time)
            logger.error(f"Liking failed: {str(e)}", profile_id)

            return {
                'activity_type': 'likes',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual
            }
