"""Unit tests for EVE Alert configuration validator."""

import unittest

from evealert.settings.validator import ConfigValidator


class TestConfigValidator(unittest.TestCase):
    """Test cases for ConfigValidator class."""

    def test_validate_region_coordinates_valid(self):
        """Test valid region coordinates."""
        is_valid, error = ConfigValidator.validate_region_coordinates(
            100, 100, 300, 300
        )
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_region_coordinates_invalid_x(self):
        """Test invalid x coordinates (x1 >= x2)."""
        is_valid, error = ConfigValidator.validate_region_coordinates(
            300, 100, 100, 300
        )
        self.assertFalse(is_valid)
        self.assertIn("x1", error.lower())
        self.assertIn("x2", error.lower())

    def test_validate_region_coordinates_invalid_y(self):
        """Test invalid y coordinates (y1 >= y2)."""
        is_valid, error = ConfigValidator.validate_region_coordinates(
            100, 300, 300, 100
        )
        self.assertFalse(is_valid)
        self.assertIn("y1", error.lower())
        self.assertIn("y2", error.lower())

    def test_validate_region_coordinates_negative(self):
        """Test negative coordinates."""
        is_valid, error = ConfigValidator.validate_region_coordinates(
            -10, 100, 300, 300
        )
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_region_coordinates_too_small(self):
        """Test region too small."""
        is_valid, error = ConfigValidator.validate_region_coordinates(
            100, 100, 105, 105
        )
        self.assertFalse(is_valid)
        self.assertIn("too small", error.lower())

    def test_validate_detection_scale_valid(self):
        """Test valid detection scale."""
        is_valid, error = ConfigValidator.validate_detection_scale(85)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_detection_scale_boundary_low(self):
        """Test detection scale at lower boundary."""
        is_valid, error = ConfigValidator.validate_detection_scale(1)
        self.assertTrue(is_valid)

    def test_validate_detection_scale_boundary_high(self):
        """Test detection scale at upper boundary."""
        is_valid, error = ConfigValidator.validate_detection_scale(100)
        self.assertTrue(is_valid)

    def test_validate_detection_scale_too_low(self):
        """Test detection scale below minimum."""
        is_valid, error = ConfigValidator.validate_detection_scale(-1)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_detection_scale_too_high(self):
        """Test detection scale above maximum."""
        is_valid, error = ConfigValidator.validate_detection_scale(150)
        self.assertFalse(is_valid)
        self.assertIn("between", error.lower())

    def test_validate_cooldown_timer_valid(self):
        """Test valid cooldown timer."""
        is_valid, error = ConfigValidator.validate_cooldown_timer(30)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_cooldown_timer_zero(self):
        """Test cooldown timer at zero."""
        is_valid, error = ConfigValidator.validate_cooldown_timer(0)
        self.assertTrue(is_valid)

    def test_validate_cooldown_timer_negative(self):
        """Test negative cooldown timer."""
        is_valid, error = ConfigValidator.validate_cooldown_timer(-5)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_cooldown_timer_too_high(self):
        """Test cooldown timer exceeding maximum."""
        is_valid, error = ConfigValidator.validate_cooldown_timer(50000)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_webhook_url_valid_https(self):
        """Test valid HTTPS webhook URL."""
        is_valid, error = ConfigValidator.validate_webhook_url(
            "https://discord.com/api/webhooks/123/abc"
        )
        self.assertTrue(is_valid)

    def test_validate_webhook_url_valid_http(self):
        """Test valid HTTP webhook URL."""
        is_valid, error = ConfigValidator.validate_webhook_url(
            "http://example.com/webhook"
        )
        self.assertTrue(is_valid)

    def test_validate_webhook_url_valid_discord(self):
        """Test valid Discord webhook URL."""
        url = "https://discord.com/api/webhooks/123456789/abcdefgh"
        is_valid, error = ConfigValidator.validate_webhook_url(url)
        self.assertTrue(is_valid)

    def test_validate_webhook_url_empty(self):
        """Test empty webhook URL (should be valid - optional)."""
        is_valid, error = ConfigValidator.validate_webhook_url("")
        self.assertTrue(is_valid)

    def test_validate_webhook_url_invalid_protocol(self):
        """Test webhook URL without http/https."""
        is_valid, error = ConfigValidator.validate_webhook_url("ftp://example.com")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_webhook_url_invalid_discord(self):
        """Test invalid Discord webhook URL."""
        is_valid, error = ConfigValidator.validate_webhook_url(
            "https://discord.com/invalid"
        )
        self.assertFalse(is_valid)

    def test_validate_settings_dict_valid(self):
        """Test valid settings dictionary."""
        settings = {
            "alert_region_1": {"x": 100, "y": 100},
            "alert_region_2": {"x": 300, "y": 300},
            "faction_region_1": {"x": 400, "y": 100},
            "faction_region_2": {"x": 600, "y": 300},
            "detectionscale": {"value": 90},
            "faction_scale": {"value": 85},
            "cooldown_timer": {"value": 30},
        }
        is_valid, errors = ConfigValidator.validate_settings_dict(settings)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_validate_settings_dict_invalid_region(self):
        """Test settings with invalid region."""
        settings = {
            "alert_region_1": {"x": 300, "y": 100},
            "alert_region_2": {"x": 100, "y": 300},  # Invalid: x1 > x2
            "faction_region_1": {"x": 400, "y": 100},
            "faction_region_2": {"x": 600, "y": 300},
            "detectionscale": {"value": 90},
            "faction_scale": {"value": 85},
            "cooldown_timer": {"value": 30},
        }
        is_valid, errors = ConfigValidator.validate_settings_dict(settings)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)

    def test_validate_settings_dict_invalid_scale(self):
        """Test settings with invalid detection scale."""
        settings = {
            "alert_region_1": {"x": 100, "y": 100},
            "alert_region_2": {"x": 300, "y": 300},
            "faction_region_1": {"x": 400, "y": 100},
            "faction_region_2": {"x": 600, "y": 300},
            "detectionscale": {"value": 150},  # Invalid: > 100
            "faction_scale": {"value": 85},
            "cooldown_timer": {"value": 30},
        }
        is_valid, errors = ConfigValidator.validate_settings_dict(settings)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)


if __name__ == '__main__':
    unittest.main()
