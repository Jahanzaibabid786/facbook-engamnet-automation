"""
Visual Cursor Manager
Injects and controls the fake visual cursor in the browser
"""
import asyncio
from typing import Optional, Tuple
from pathlib import Path
from utils.logger import logger

class VisualCursor:
    def __init__(self, pydoll_controller):
        self.controller = pydoll_controller
        self.cursor_injected = {}
        self.cursor_script = self._load_cursor_script()

    def _load_cursor_script(self) -> str:
        """Load the visual cursor JavaScript"""
        cursor_js = '''
        (function() {
            if (window.__FakeCursor) return; // Already injected

            const cfg = {
                size: 18,
                color: 'rgba(0,150,255,0.95)',
                smoothing: 0.18,
                clickPulseDuration: 150,
                hideNativeCursor: true
            };

            let cursorEl = null;
            let enabled = false;
            let mouseX = window.innerWidth / 2;
            let mouseY = window.innerHeight / 2;
            let targetX = mouseX;
            let targetY = mouseY;
            let rafId = null;

            function createCursor() {
                const el = document.createElement('div');
                el.style.cssText = `
                    position: fixed;
                    left: 0; top: 0;
                    width: ${cfg.size}px;
                    height: ${cfg.size}px;
                    border-radius: 50%;
                    background: ${cfg.color};
                    box-shadow: 0 0 10px rgba(0,150,255,0.45);
                    transform: translate(-50%, -50%);
                    pointer-events: none;
                    z-index: 2147483647;
                    transition: transform 120ms;
                `;

                const dot = document.createElement('div');
                dot.style.cssText = `
                    position: absolute;
                    left: 50%; top: 50%;
                    width: 6px; height: 6px;
                    border-radius: 50%;
                    transform: translate(-50%, -50%);
                    background: white;
                    opacity: 0.95;
                `;
                el.appendChild(dot);

                document.body.appendChild(el);
                return el;
            }

            function tick() {
                const dx = targetX - mouseX;
                const dy = targetY - mouseY;
                mouseX += dx * cfg.smoothing;
                mouseY += dy * cfg.smoothing;

                if (cursorEl) {
                    cursorEl.style.left = mouseX + 'px';
                    cursorEl.style.top = mouseY + 'px';
                }
                rafId = requestAnimationFrame(tick);
            }

            function enableCursor() {
                if (enabled) return;
                cursorEl = createCursor();
                enabled = true;
                if (cfg.hideNativeCursor) {
                    document.documentElement.style.cursor = 'none';
                }
                rafId = requestAnimationFrame(tick);
            }

            function moveTo(x, y, duration = 400) {
                return new Promise(resolve => {
                    const startX = mouseX;
                    const startY = mouseY;
                    const start = performance.now();

                    function anim(now) {
                        const t = Math.min(1, (now - start) / duration);
                        const ease = t < 0.5 ? 2*t*t : -1 + (4 - 2*t)*t;
                        targetX = startX + (x - startX) * ease;
                        targetY = startY + (y - startY) * ease;
                        if (t < 1) requestAnimationFrame(anim);
                        else resolve();
                    }
                    requestAnimationFrame(anim);
                });
            }

            function pulse() {
                if (!cursorEl) return;
                cursorEl.style.transform = 'translate(-50%, -50%) scale(0.9)';
                setTimeout(() => {
                    if (cursorEl) cursorEl.style.transform = 'translate(-50%, -50%) scale(1)';
                }, cfg.clickPulseDuration);
            }

            window.__FakeCursor = {
                enable: enableCursor,
                moveTo: moveTo,
                pulse: pulse,
                isEnabled: () => enabled
            };

            // Auto-enable
            enableCursor();
        })();
        '''
        return cursor_js

    async def inject(self, profile_id: str) -> bool:
        """Inject visual cursor into browser"""
        try:
            pydoll = self.controller.get_connection(profile_id)
            if not pydoll:
                logger.error(f"No PyDoll connection for profile {profile_id}")
                return False

            await pydoll.evaluate(self.cursor_script)
            self.cursor_injected[profile_id] = True
            logger.info(f"Visual cursor injected for profile {profile_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to inject cursor: {str(e)}", profile_id)
            return False

    async def move_to(self, profile_id: str, x: int, y: int, duration: int = 400) -> bool:
        """Move cursor to position"""
        try:
            if not self.cursor_injected.get(profile_id):
                await self.inject(profile_id)

            pydoll = self.controller.get_connection(profile_id)
            if not pydoll:
                return False

            await pydoll.evaluate(f"window.__FakeCursor.moveTo({x}, {y}, {duration})")
            return True

        except Exception as e:
            logger.error(f"Cursor move failed: {str(e)}", profile_id)
            return False

    async def pulse(self, profile_id: str) -> bool:
        """Show click animation"""
        try:
            if not self.cursor_injected.get(profile_id):
                await self.inject(profile_id)

            pydoll = self.controller.get_connection(profile_id)
            if not pydoll:
                return False

            await pydoll.evaluate("window.__FakeCursor.pulse()")
            return True

        except Exception as e:
            logger.error(f"Cursor pulse failed: {str(e)}", profile_id)
            return False
