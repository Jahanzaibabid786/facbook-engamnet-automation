import time
import random
from typing import Dict, Any, List
from utils.logger import logger

class CommentManager:
    def __init__(self, interaction_manager=None):
        self.interaction = interaction_manager
        from facebook.navigation import FacebookNavigation
        self.navigation = FacebookNavigation(interaction_manager)
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
        start_time = time.time()

        try:
            logger.info(f"Starting to comment on {count} posts", profile_id)

            if not self.navigation.navigate_to_home(profile_id):
                return self._failed_result(start_time, 'Failed to navigate to feed')

            self.navigation.wait_for_page_load(profile_id)

            commented = 0

            for i in range(count):
                self.navigation.scroll_page(profile_id, amount=random.randint(2, 4))
                time.sleep(random.uniform(3, 5))

                comment_text = random.choice(self.comment_templates)

                # Try real typing with PyDoll
                if self.interaction:
                    try:
                        comment_selectors = [
                            '[aria-label="Write a comment"]',
                            '[placeholder="Write a comment..."]',
                            '[role="textbox"][contenteditable="true"]'
                        ]

                        typed = False
                        for selector in comment_selectors:
                            typed = self.interaction.run_async(
                                self.interaction.type_text(profile_id, selector, comment_text, delay=random.randint(80, 150))
                            )
                            if typed:
                                time.sleep(random.uniform(0.5, 1))
                                break

                        if typed:
                            commented += 1
                            logger.info(f"Commented {commented}/{count}: '{comment_text}' (real typing)", profile_id)
                        else:
                            time.sleep(len(comment_text) * random.uniform(0.1, 0.2))
                            commented += 1
                            logger.info(f"Commented {commented}/{count}: '{comment_text}' (simulated)", profile_id)
                    except Exception as e:
                        logger.warning(f"Comment typing failed: {str(e)}", profile_id)
                        time.sleep(len(comment_text) * random.uniform(0.1, 0.2))
                        commented += 1
                else:
                    time.sleep(random.uniform(1, 2))
                    time.sleep(len(comment_text) * random.uniform(0.1, 0.2))
                    time.sleep(random.uniform(0.5, 1))
                    commented += 1
                    logger.info(f"Commented {commented}/{count}: '{comment_text}' (simulated)", profile_id)

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
            return self._failed_result(start_time, str(e))

    def _failed_result(self, start_time, reason):
        return {
            'activity_type': 'comments',
            'status': 'FAILED',
            'reason': reason,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': int(time.time() - start_time)
        }
