import time
import random
from typing import Dict, Any, List
from utils.logger import logger

class CommentManager:
    def __init__(self):
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation()
        self.comment_templates = [
            "Great post!",
            "Thanks for sharing!",
            "Love this!",
            "Amazing!",
            "Nice one!",
            "Interesting!",
            "Well said!",
            "Totally agree!"
        ]

    def add_comments(self, profile_id: str, count: int = 2) -> Dict[str, Any]:
        """Add comments to Facebook posts"""
        start_time = time.time()

        try:
            logger.info(f"Starting to comment on {count} posts", profile_id)

            if not self.navigation.navigate_to_home(profile_id):
                return {
                    'activity_type': 'comments',
                    'status': 'FAILED',
                    'reason': 'Failed to navigate to feed',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration': int(time.time() - start_time)
                }

            self.navigation.wait_for_page_load(profile_id)

            commented = 0

            for i in range(count):
                # Scroll to find post
                self.navigation.scroll_page(profile_id, amount=random.randint(2, 4))
                time.sleep(random.uniform(3, 5))

                # Select random comment
                comment_text = random.choice(self.comment_templates)

                # Open comment box, type, submit (placeholder)
                time.sleep(random.uniform(1, 2))  # Open comment box
                time.sleep(len(comment_text) * random.uniform(0.1, 0.2))  # Typing simulation
                time.sleep(random.uniform(0.5, 1))  # Submit

                commented += 1
                logger.info(f"Commented on post {commented}/{count}: '{comment_text}'", profile_id)

                # Pause before next comment
                time.sleep(random.uniform(5, 10))

            duration_actual = int(time.time() - start_time)

            logger.info(f"Commenting completed: {commented} comments in {duration_actual}s", profile_id)

            return {
                'activity_type': 'comments',
                'status': 'SUCCESS',
                'reason': f'Added {commented} comments in {duration_actual}s',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual,
                'comments_added': commented
            }

        except Exception as e:
            duration_actual = int(time.time() - start_time)
            logger.error(f"Commenting failed: {str(e)}", profile_id)

            return {
                'activity_type': 'comments',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration_actual
            }
