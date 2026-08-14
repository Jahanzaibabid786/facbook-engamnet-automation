"""
Interaction Manager - Unified interface for browser interactions
Coordinates PyDoll controller, visual cursor, mouse, and keyboard actions
"""
import asyncio
import random
import time
from typing import Optional, Dict, Any
from interaction.pydoll_controller import PyDollController
from interaction.visual_cursor import VisualCursor
from utils.logger import logger

class InteractionManager:
    def __init__(self):
        self.pydoll = PyDollController()
        self.visual_cursor = VisualCursor(self.pydoll)
        self.active_profiles = {}

    async def initialize(self, profile_id: str, port: int = 9222) -> bool:
        """Initialize PyDoll connection for profile"""
        try:
            success = await self.pydoll.connect(profile_id, port)
            if success:
                self.active_profiles[profile_id] = True
                # Wait a bit for page to be ready
                await asyncio.sleep(2)
                # Inject visual cursor
                await self.visual_cursor.inject(profile_id)
            return success
        except Exception as e:
            logger.error(f"Failed to initialize interaction manager: {str(e)}", profile_id)
            return False

    async def cleanup(self, profile_id: str):
        """Cleanup PyDoll connection"""
        try:
            await self.pydoll.disconnect(profile_id)
            if profile_id in self.active_profiles:
                del self.active_profiles[profile_id]
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}", profile_id)

    async def navigate(self, profile_id: str, url: str) -> bool:
        """Navigate to URL"""
        try:
            logger.info(f"Navigating to {url}", profile_id)
            return await self.pydoll.navigate(profile_id, url)
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}", profile_id)
            return False

    async def wait_for_load(self, profile_id: str, timeout: int = 30000) -> bool:
        """Wait for page load"""
        try:
            return await self.pydoll.wait_for_load(profile_id, timeout)
        except Exception as e:
            logger.error(f"Wait for load failed: {str(e)}", profile_id)
            return False

    async def scroll(self, profile_id: str, amount: int = 300) -> bool:
        """Scroll page"""
        try:
            return await self.pydoll.scroll(profile_id, amount)
        except Exception as e:
            logger.error(f"Scroll failed: {str(e)}", profile_id)
            return False

    async def click_element(self, profile_id: str, selector: str) -> bool:
        """Click element with visual cursor animation"""
        try:
            pydoll_conn = self.pydoll.get_connection(profile_id)
            if not pydoll_conn:
                return False

            # Get element position
            element = await pydoll_conn.query_selector(selector)
            if not element:
                logger.warning(f"Element not found: {selector}", profile_id)
                return False

            # Get bounding box
            box = await element.bounding_box()
            if not box:
                return False

            # Calculate center position
            x = box['x'] + box['width'] / 2
            y = box['y'] + box['height'] / 2

            # Move cursor to element
            await self.visual_cursor.move_to(profile_id, int(x), int(y), duration=random.randint(300, 600))
            await asyncio.sleep(random.uniform(0.2, 0.5))

            # Pulse cursor (click animation)
            await self.visual_cursor.pulse(profile_id)

            # Perform actual click
            await element.click()

            await asyncio.sleep(random.uniform(0.3, 0.7))
            return True

        except Exception as e:
            logger.error(f"Click failed: {str(e)}", profile_id)
            return False

    async def type_text(self, profile_id: str, selector: str, text: str, delay: int = 100) -> bool:
        """Type text into input field"""
        try:
            pydoll_conn = self.pydoll.get_connection(profile_id)
            if not pydoll_conn:
                return False

            element = await pydoll_conn.query_selector(selector)
            if not element:
                logger.warning(f"Input element not found: {selector}", profile_id)
                return False

            # Click to focus
            await self.click_element(profile_id, selector)
            await asyncio.sleep(0.3)

            # Type with human-like delays
            await element.type(text, delay=delay)

            await asyncio.sleep(random.uniform(0.2, 0.4))
            return True

        except Exception as e:
            logger.error(f"Type text failed: {str(e)}", profile_id)
            return False

    async def evaluate_js(self, profile_id: str, script: str) -> Any:
        """Execute JavaScript in page"""
        try:
            pydoll_conn = self.pydoll.get_connection(profile_id)
            if not pydoll_conn:
                return None

            return await pydoll_conn.evaluate(script)

        except Exception as e:
            logger.error(f"JS evaluation failed: {str(e)}", profile_id)
            return None

    def run_async(self, coro):
        """Helper to run async function synchronously"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(coro)
