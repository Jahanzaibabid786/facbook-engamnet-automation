"""
PyDoll Browser Controller
Manages PyDoll browser connections and provides browser automation primitives
"""
import asyncio
from typing import Optional, Dict, Any
from pydoll import Pydoll
from utils.logger import logger

class PyDollController:
    def __init__(self):
        self.active_connections: Dict[str, Pydoll] = {}

    async def connect(self, profile_id: str, port: int = 9222) -> bool:
        """Connect to Chrome DevTools Protocol"""
        try:
            if profile_id in self.active_connections:
                logger.warning(f"PyDoll already connected for profile {profile_id}")
                return True

            pydoll = Pydoll()
            await pydoll.connect(f"http://localhost:{port}")

            self.active_connections[profile_id] = pydoll
            logger.info(f"PyDoll connected for profile {profile_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect PyDoll: {str(e)}", profile_id)
            return False

    async def disconnect(self, profile_id: str):
        """Disconnect PyDoll"""
        try:
            if profile_id in self.active_connections:
                pydoll = self.active_connections[profile_id]
                await pydoll.close()
                del self.active_connections[profile_id]
                logger.info(f"PyDoll disconnected for profile {profile_id}")
        except Exception as e:
            logger.error(f"Failed to disconnect PyDoll: {str(e)}", profile_id)

    def get_connection(self, profile_id: str) -> Optional[Pydoll]:
        """Get active PyDoll connection"""
        return self.active_connections.get(profile_id)

    async def navigate(self, profile_id: str, url: str) -> bool:
        """Navigate to URL"""
        try:
            pydoll = self.get_connection(profile_id)
            if not pydoll:
                logger.error(f"No PyDoll connection for profile {profile_id}")
                return False

            await pydoll.goto(url)
            logger.info(f"Navigated to {url}", profile_id)
            return True

        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}", profile_id)
            return False

    async def wait_for_load(self, profile_id: str, timeout: int = 30000) -> bool:
        """Wait for page load"""
        try:
            pydoll = self.get_connection(profile_id)
            if not pydoll:
                return False

            await pydoll.wait_for_load_state("networkidle", timeout=timeout)
            return True

        except Exception as e:
            logger.error(f"Wait for load failed: {str(e)}", profile_id)
            return False

    async def get_element(self, profile_id: str, selector: str):
        """Get element by selector"""
        try:
            pydoll = self.get_connection(profile_id)
            if not pydoll:
                return None

            return await pydoll.query_selector(selector)

        except Exception as e:
            logger.error(f"Get element failed: {str(e)}", profile_id)
            return None

    async def scroll(self, profile_id: str, amount: int = 300):
        """Scroll page"""
        try:
            pydoll = self.get_connection(profile_id)
            if not pydoll:
                return False

            await pydoll.evaluate(f"window.scrollBy(0, {amount})")
            return True

        except Exception as e:
            logger.error(f"Scroll failed: {str(e)}", profile_id)
            return False
