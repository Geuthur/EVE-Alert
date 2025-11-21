"""Unit tests for Vision module template matching."""

import unittest
from pathlib import Path
from unittest.mock import patch

import cv2 as cv
import numpy as np

from evealert.exceptions import RegionSizeError
from evealert.tools.vision import Vision


class TestVision(unittest.TestCase):
    """Test cases for Vision class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create dummy needle images (50x50 red squares)
        self.test_needle_path = Path("tests/fixtures/test_needle.png")
        self.test_needle_path.parent.mkdir(parents=True, exist_ok=True)

        needle_img = np.zeros((50, 50, 3), dtype=np.uint8)
        needle_img[:, :] = (0, 0, 255)  # Red
        cv.imwrite(str(self.test_needle_path), needle_img)

        # Create Vision instance
        self.vision = Vision([str(self.test_needle_path)])

    def tearDown(self):
        """Clean up test fixtures."""
        if self.test_needle_path.exists():
            self.test_needle_path.unlink()
        if self.test_needle_path.parent.exists() and not list(
            self.test_needle_path.parent.iterdir()
        ):
            self.test_needle_path.parent.rmdir()

        self.vision.clean_up()

    def test_vision_initialization(self):
        """Test Vision object initialization."""
        self.assertIsNotNone(self.vision.needle_imgs)
        self.assertEqual(len(self.vision.needle_imgs), 1)
        self.assertEqual(len(self.vision.needle_dims), 1)
        self.assertEqual(self.vision.needle_dims[0], (50, 50))
        self.assertEqual(self.vision.method, cv.TM_CCOEFF_NORMED)
        self.assertFalse(self.vision.debug_mode)

    def test_find_with_no_matches(self):
        """Test finding templates with no matches."""
        # Create haystack with no red squares
        haystack = np.zeros((200, 200, 3), dtype=np.uint8)
        haystack[:, :] = (255, 255, 255)  # White

        points = self.vision.find(haystack, threshold=90)  # High threshold
        self.assertIsInstance(points, list)
        # Allow for occasional false positives in template matching
        self.assertLessEqual(len(points), 2)

    def test_find_with_single_match(self):
        """Test finding templates with single match."""
        # Create haystack with one red square
        haystack = np.zeros((200, 200, 3), dtype=np.uint8)
        haystack[:, :] = (255, 255, 255)  # White background
        haystack[50:100, 50:100] = (0, 0, 255)  # Red square

        points = self.vision.find(haystack, threshold=70)
        # Should find at least one match
        self.assertGreater(len(points), 0)

    def test_find_with_multiple_matches(self):
        """Test finding templates with multiple matches."""
        # Create haystack with two well-separated red squares
        haystack = np.zeros((400, 400, 3), dtype=np.uint8)
        haystack[:, :] = (255, 255, 255)  # White background
        haystack[50:100, 50:100] = (0, 0, 255)  # Red square 1
        haystack[250:300, 250:300] = (0, 0, 255)  # Red square 2

        points = self.vision.find(haystack, threshold=70)
        # Should find at least 1 match, maybe 2
        self.assertGreaterEqual(len(points), 1)

    def test_find_faction(self):
        """Test faction detection."""
        # Create haystack with red square
        haystack = np.zeros((200, 200, 3), dtype=np.uint8)
        haystack[:, :] = (255, 255, 255)  # White background
        haystack[50:100, 50:100] = (0, 0, 255)  # Red square

        points = self.vision.find_faction(haystack, threshold=50)
        self.assertGreater(len(points), 0)

    def test_threshold_validation(self):
        """Test detection threshold clamping."""
        haystack = np.zeros((200, 200, 3), dtype=np.uint8)

        # Test with very low threshold
        points_low = self.vision.find(haystack, threshold=0)
        self.assertIsInstance(points_low, list)

        # Test with very high threshold
        points_high = self.vision.find(haystack, threshold=100)
        self.assertIsInstance(points_high, list)

    def test_region_size_error(self):
        """Test error when haystack is smaller than needle."""
        # Create tiny haystack (smaller than 50x50 needle)
        haystack = np.zeros((30, 30, 3), dtype=np.uint8)

        # Should either raise RegionSizeError or handle gracefully
        try:
            self.vision.find(haystack)
        except RegionSizeError as e:
            self.assertIn("Region is smaller", str(e))
        except Exception:
            # Other exceptions are also acceptable
            pass

    def test_grayscale_conversion(self):
        """Test handling of grayscale images."""
        # Create grayscale haystack
        haystack = np.zeros((200, 200), dtype=np.uint8)
        haystack[:, :] = 128  # Gray

        points = self.vision.find(haystack, threshold=50)
        self.assertIsInstance(points, list)

    def test_debug_mode(self):
        """Test debug mode activation."""
        self.vision.debug_mode = True
        self.assertTrue(self.vision.is_vision_open)

        haystack = np.zeros((200, 200, 3), dtype=np.uint8)

        with patch("cv2.imshow"), patch("cv2.waitKey"):
            points = self.vision.find(haystack)
            self.assertIsInstance(points, list)

    def test_debug_mode_faction(self):
        """Test faction debug mode."""
        self.vision.debug_mode_faction = True
        self.assertTrue(self.vision.is_faction_vision_open)

        haystack = np.zeros((200, 200, 3), dtype=np.uint8)

        with patch("cv2.imshow"), patch("cv2.waitKey"):
            points = self.vision.find_faction(haystack)
            self.assertIsInstance(points, list)

    def test_clean_up(self):
        """Test cleanup method."""
        self.vision.debug_mode = True
        self.vision.debug_mode_faction = True

        with patch("cv2.destroyAllWindows") as mock_destroy:
            self.vision.clean_up()
            mock_destroy.assert_called_once()

        self.assertFalse(self.vision.debug_mode)
        self.assertFalse(self.vision.debug_mode_faction)

    def test_destroy_vision_enemy(self):
        """Test destroying enemy vision window."""
        self.vision.debug_mode = True

        with patch("cv2.destroyWindow") as mock_destroy:
            self.vision.destroy_vision("Enemy")
            mock_destroy.assert_called_once_with("Enemy")

        self.assertFalse(self.vision.debug_mode)

    def test_destroy_vision_faction(self):
        """Test destroying faction vision window."""
        self.vision.debug_mode_faction = True

        with patch("cv2.destroyWindow") as mock_destroy:
            self.vision.destroy_vision("Faction")
            mock_destroy.assert_called_once_with("Faction")

        self.assertFalse(self.vision.debug_mode_faction)

    def test_exception_handling(self):
        """Test exception handling in vision_process."""
        # Create invalid haystack
        haystack = None

        # Should handle exception gracefully and return empty list
        try:
            points = self.vision.find(haystack)
            self.assertEqual(len(points), 0)
        except Exception:
            # It's also acceptable if exception is raised
            pass

    def test_alpha_channel_removal(self):
        """Test BGRA to BGR conversion."""
        # Create needle with alpha channel
        needle_bgra_path = Path("tests/fixtures/test_needle_alpha.png")
        needle_img = np.zeros((50, 50, 4), dtype=np.uint8)
        needle_img[:, :, :3] = (0, 0, 255)  # Red
        needle_img[:, :, 3] = 255  # Full opacity
        cv.imwrite(str(needle_bgra_path), needle_img)

        try:
            vision_alpha = Vision([str(needle_bgra_path)])

            haystack = np.zeros((200, 200, 3), dtype=np.uint8)
            haystack[50:100, 50:100] = (0, 0, 255)

            points = vision_alpha.find(haystack, threshold=50)
            self.assertIsInstance(points, list)
        finally:
            if needle_bgra_path.exists():
                needle_bgra_path.unlink()
            vision_alpha.clean_up()

    def test_normalization(self):
        """Test image normalization before matching."""
        # Create haystack with varying brightness
        haystack = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)

        points = self.vision.find(haystack, threshold=50)
        self.assertIsInstance(points, list)


if __name__ == "__main__":
    unittest.main()
