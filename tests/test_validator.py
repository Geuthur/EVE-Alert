"""Unit tests for EVE Alert configuration validator."""

import unittest
from evealert.settings.validator import ConfigValidator


class TestConfigValidator(unittest.TestCase):
    """Test cases for ConfigValidator class."""

    def test_validate_region_coordinates_valid(self):
        """Test valid region coordinates."""
        valid, error = ConfigValidator.validate_region_coordinates(10, 10, 100, 100)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_region_coordinates_invalid_x(self):
        """Test invalid x coordinates (x1 >= x2)."""
        valid, error = ConfigValidator.validate_region_coordinates(100, 10, 50, 100)
        self.assertFalse(valid)
        self.assertIn("x1", error)
        self.assertIn("x2", error)

    def test_validate_region_coordinates_invalid_y(self):
        """Test invalid y coordinates (y1 >= y2)."""
        valid, error = ConfigValidator.validate_region_coordinates(10, 100, 100, 50)
        self.assertFalse(valid)
        self.assertIn("y1", error)
        self.assertIn("y2", error)

    def test_validate_region_coordinates_negative(self):
        """Test negative coordinates."""
        valid, error = ConfigValidator.validate_region_coordinates(-10, -10, 100, 100)
        self.assertFalse(valid)
        self.assertIn("negative", error.lower())

    def test_validate_region_coordinates_too_small(self):
        """Test region too small."""
        valid, error = ConfigValidator.validate_region_coordinates(10, 10, 15, 15)
        self.assertFalse(valid)
        self.assertIn("too small", error.lower())

    def test_validate_detection_scale_valid(self):
        """Test valid detection scale."""
        valid, error = ConfigValidator.validate_detection_scale(50)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_detection_scale_boundary_low(self):
        """Test detection scale at lower boundary."""
        valid, error = ConfigValidator.validate_detection_scale(0)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_detection_scale_boundary_high(self):
        """Test detection scale at upper boundary."""
        valid, error = ConfigValidator.validate_detection_scale(100)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_detection_scale_too_low(self):
        """Test detection scale below minimum."""
        valid, error = ConfigValidator.validate_detection_scale(-10)
        self.assertFalse(valid)
        self.assertIn("between", error.lower())

    def test_validate_detection_scale_too_high(self):
        """Test detection scale above maximum."""
        valid, error = ConfigValidator.validate_detection_scale(150)
        self.assertFalse(valid)
        self.assertIn("between", error.lower())

    def test_validate_cooldown_timer_valid(self):
        """Test valid cooldown timer."""
        valid, error = ConfigValidator.validate_cooldown_timer(60)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_cooldown_timer_zero(self):
        """Test cooldown timer at zero."""
        valid, error = ConfigValidator.validate_cooldown_timer(0)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_cooldown_timer_negative(self):
        """Test negative cooldown timer."""
        valid, error = ConfigValidator.validate_cooldown_timer(-10)
        self.assertFalse(valid)
        self.assertIn("negative", error.lower())

    def test_validate_cooldown_timer_too_high(self):
        """Test cooldown timer exceeding maximum."""
        valid, error = ConfigValidator.validate_cooldown_timer(5000)
        self.assertFalse(valid)
        self.assertIn("3600", error)

    def test_validate_webhook_url_empty(self):
        """Test empty webhook URL (should be valid - optional)."""
        valid, error = ConfigValidator.validate_webhook_url("")
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_webhook_url_valid_http(self):
        """Test valid HTTP webhook URL."""
        valid, error = ConfigValidator.validate_webhook_url(
            "http://example.com/webhook"
        )
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_webhook_url_valid_https(self):
        """Test valid HTTPS webhook URL."""
        valid, error = ConfigValidator.validate_webhook_url(
            "https://example.com/webhook"
        )
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_webhook_url_valid_discord(self):
        """Test valid Discord webhook URL."""
        valid, error = ConfigValidator.validate_webhook_url(
            "https://discord.com/api/webhooks/123456/abcdef"
        )
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_webhook_url_invalid_protocol(self):
        """Test webhook URL without http/https."""
        valid, error = ConfigValidator.validate_webhook_url("ftp://example.com/webhook")
        self.assertFalse(valid)
        self.assertIn("http", error.lower())

    def test_validate_webhook_url_invalid_discord(self):
        """Test invalid Discord webhook URL."""
        valid, error = ConfigValidator.validate_webhook_url(
            "https://discord.com/channels/123456"
        )
        self.assertFalse(valid)
        self.assertIn("discord", error.lower())

    def test_validate_settings_dict_valid(self):
        """Test valid settings dictionary."""
        settings = {
            "alert_region_1": {"x": 10, "y": 10},
            "alert_region_2": {"x": 100, "y": 100},
            "faction_region_1": {"x": 10, "y": 10},
            "faction_region_2": {"x": 100, "y": 100},
            "detectionscale": {"value": 50},
            "faction_scale": {"value": 50},
            "cooldown_timer": {"value": 60},
            "server": {"webhook": "https://discord.com/api/webhooks/123/abc", "mute": False},
        }
        valid, errors = ConfigValidator.validate_settings_dict(settings)
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

    def test_validate_settings_dict_invalid_region(self):
        """Test settings with invalid region."""
        settings = {
            "alert_region_1": {"x": 100, "y": 10},
            "alert_region_2": {"x": 10, "y": 100},  # x1 > x2
        }
        valid, errors = ConfigValidator.validate_settings_dict(settings)
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)

    def test_validate_settings_dict_invalid_scale(self):
        """Test settings with invalid detection scale."""
        settings = {
            "detectionscale": {"value": 150},  # Too high
        }
        valid, errors = ConfigValidator.validate_settings_dict(settings)
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
