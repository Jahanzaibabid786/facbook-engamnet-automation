import time
import random
from typing import Dict, Any
from utils.logger import logger

class FacebookNavigation:
    def __init__(self, interaction_manager=None):
        self.base_url = "https://www.facebook.com"
        self.interaction = interaction_manager
        self.endpoints = {
            'home': '/',
            'feed': '/',
            'reels': '/reel',
            'stories': '/stories',
            'notifications': '/notifications',
            'messages': '/messages'
        }

    def set_interaction_manager(self, interaction_manager):
        """Set the interaction manager after initialization"""
        self.interaction = interaction_manager

    def navigate_to_home(self, profile_id: str) -> bool:
        """Navigate to Facebook home/feed"""
        try:
            if self.interaction:
                # Real navigation with PyDoll
                url = self.base_url + self.endpoints['home']
                result = self.interaction.run_async(
                    self.interaction.navigate(profile_id, url)
                )
                if result:
                    self.interaction.run_async(
                        self.interaction.wait_for_load(profile_id)
                    )
                return result
            else:
                # Fallback to simulation
                logger.info("Navigating to Facebook home (simulated)", profile_id)
                time.sleep(random.uniform(1, 2))
                return True
        except Exception as e:
            logger.error(f"Failed to navigate to home: {str(e)}", profile_id)
            return False

    def navigate_to_reels(self, profile_id: str) -> bool:
        """Navigate to Facebook Reels"""
        try:
            if self.interaction:
                url = self.base_url + self.endpoints['reels']
                result = self.interaction.run_async(
                    self.interaction.navigate(profile_id, url)
                )
                if result:
                    self.interaction.run_async(
                        self.interaction.wait_for_load(profile_id)
                    )
                return result
            else:
                logger.info("Navigating to Reels (simulated)", profile_id)
                time.sleep(random.uniform(1, 2))
                return True
        except Exception as e:
            logger.error(f"Failed to navigate to Reels: {str(e)}", profile_id)
            return False

    def navigate_to_stories(self, profile_id: str) -> bool:
        """Navigate to Stories"""
        try:
            if self.interaction:
                url = self.base_url + self.endpoints['stories']
                result = self.interaction.run_async(
                    self.interaction.navigate(profile_id, url)
                )
                if result:
                    self.interaction.run_async(
                        self.interaction.wait_for_load(profile_id)
                    )
                return result
            else:
                logger.info("Navigating to Stories (simulated)", profile_id)
                time.sleep(random.uniform(1, 2))
                return True
        except Exception as e:
            logger.error(f"Failed to navigate to Stories: {str(e)}", profile_id)
            return False

    def scroll_page(self, profile_id: str, amount: int = 1) -> bool:
        """Scroll the page"""
        try:
            if self.interaction:
                # Real scrolling with PyDoll
                scroll_pixels = amount * 300
                result = self.interaction.run_async(
                    self.interaction.scroll(profile_id, scroll_pixels)
                )
                return result
            else:
                # Simulated scroll
                time.sleep(random.uniform(0.5, 1.5))
                return True
        except Exception as e:
            logger.error(f"Failed to scroll page: {str(e)}", profile_id)
            return False

    def wait_for_page_load(self, profile_id: str, timeout: int = 10) -> bool:
        """Wait for page to load"""
        try:
            if self.interaction:
                result = self.interaction.run_async(
                    self.interaction.wait_for_load(profile_id, timeout * 1000)
                )
                return result
            else:
                time.sleep(random.uniform(2, 4))
                return True
        except Exception as e:
            logger.error(f"Page load timeout: {str(e)}", profile_id)
            return False
