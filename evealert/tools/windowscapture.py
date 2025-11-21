from typing import TYPE_CHECKING, Optional, Tuple

import mss
import numpy as np

from evealert.settings.logger import logging

if TYPE_CHECKING:
    from evealert.menu.main import MainMenu

logger = logging.getLogger("tools")


class WindowCapture:
    """Handles screen capture for specified regions."""

    def __init__(self, mainmenu: "MainMenu"):
        self.main = mainmenu

    def get_screenshot_value(
        self, y1: int, x1: int, x2: int, y2: int
    ) -> Tuple[Optional[np.ndarray], Optional[mss.screenshot.ScreenShot]]:
        """
        Capture a screenshot of the specified region.

        Args:
            y1: Top coordinate
            x1: Left coordinate
            x2: Right coordinate (exclusive)
            y2: Bottom coordinate (exclusive)

        Returns:
            Tuple of (numpy_array, raw_screenshot) or (None, None) on error
        """
        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
            try:
                screenshot = sct.grab(monitor)
            except Exception as e:
                logger.error("Screenshot capture failed: %s", e)
                return None, None

        # Convert directly to NumPy array and keep only RGB channels
        # This is more efficient than converting through PIL Image
        img_array = np.array(screenshot)[:, :, :3]  # Drop alpha channel

        return img_array, screenshot
