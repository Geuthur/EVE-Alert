"""Integration tests for EVE Alert system."""
import unittest
from unittest.mock import MagicMock, patch
import numpy as np

from evealert.tools.windowscapture import WindowCapture
from evealert.tools.vision import Vision
from evealert.constants import (
    DEFAULT_COOLDOWN_TIMER,
    DETECTION_SCALE_MIN,
    DETECTION_SCALE_MAX,
)


class TestIntegration(unittest.TestCase):
    """Test integration between components."""

    def test_window_capture_initialization(self):
        """Test WindowCapture can be initialized."""
        capture = WindowCapture(0, 0, 100, 100)
        self.assertIsNotNone(capture)

    def test_vision_initialization(self):
        """Test Vision can be initialized with image paths."""
        vision = Vision(
            img_enemy_path="evealert/img/image_1.png",
            img_faction_path="evealert/img/image_faction_1.png",
        )
        self.assertIsNotNone(vision)

    @patch("evealert.tools.windowscapture.mss.mss")
    def test_screenshot_returns_numpy_array(self, mock_mss):
        """Test screenshot returns valid numpy array."""
        # Mock screenshot
        mock_screenshot = MagicMock()
        mock_screenshot.rgb = b"\x00" * (100 * 100 * 3)
        mock_screenshot.size = (100, 100)
        
        mock_sct = MagicMock()
        mock_sct.grab.return_value = mock_screenshot
        mock_mss.return_value.__enter__.return_value = mock_sct

        capture = WindowCapture(0, 0, 100, 100)
        screenshot, _ = capture.get_screenshot_value()
        
        self.assertIsInstance(screenshot, np.ndarray)

    def test_vision_with_invalid_image_paths(self):
        """Test Vision handles invalid image paths gracefully."""
        with self.assertRaises(Exception):
            vision = Vision(
                img_enemy_path="nonexistent.png",
                img_faction_path="nonexistent.png",
            )

    def test_constants_are_valid(self):
        """Test that all constants have valid values."""
        self.assertIsInstance(DETECTION_SCALE_MIN, (int, float))
        self.assertIsInstance(DETECTION_SCALE_MAX, (int, float))
        self.assertGreater(DETECTION_SCALE_MAX, DETECTION_SCALE_MIN)
        
        self.assertIsInstance(DEFAULT_COOLDOWN_TIMER, int)
        self.assertGreater(DEFAULT_COOLDOWN_TIMER, 0)


if __name__ == "__main__":
    unittest.main()
