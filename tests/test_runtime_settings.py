"""Integration tests for runtime settings application.

These tests verify the runtime configuration logic without
requiring a full GUI environment.
"""

import unittest

from evealert.settings.validator import ConfigValidator


class TestRuntimeSettingsValidation(unittest.TestCase):
    """Test cases for runtime settings validation logic."""

    def test_valid_detection_scale(self):
        """Test validation of valid detection scale."""
        is_valid, error = ConfigValidator.validate_detection_scale(85)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_invalid_detection_scale_too_high(self):
        """Test validation of too high detection scale."""
        is_valid, error = ConfigValidator.validate_detection_scale(150)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        self.assertIn("between", error.lower())

    def test_invalid_detection_scale_too_low(self):
        """Test validation of too low detection scale."""
        # Detection scale of 0 is actually valid (means no detection)
        # Test with truly invalid value (-1)
        is_valid, error = ConfigValidator.validate_detection_scale(-1)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_valid_cooldown_timer(self):
        """Test validation of valid cooldown timer."""
        is_valid, error = ConfigValidator.validate_cooldown_timer(30)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_invalid_cooldown_timer_negative(self):
        """Test validation of negative cooldown timer."""
        is_valid, error = ConfigValidator.validate_cooldown_timer(-5)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_valid_cooldown_timer_zero(self):
        """Test validation of zero cooldown timer."""
        is_valid, error = ConfigValidator.validate_cooldown_timer(0)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_boundary_detection_scale_min(self):
        """Test detection scale at minimum boundary."""
        is_valid, error = ConfigValidator.validate_detection_scale(1)
        self.assertTrue(is_valid)

    def test_boundary_detection_scale_max(self):
        """Test detection scale at maximum boundary."""
        is_valid, error = ConfigValidator.validate_detection_scale(100)
        self.assertTrue(is_valid)

    def test_runtime_settings_workflow(self):
        """Test complete runtime settings update workflow."""
        # Simulate user changing settings
        detection_scale = 85
        faction_scale = 92
        cooldown = 45
        
        # Validate all settings
        valid_detection, _ = ConfigValidator.validate_detection_scale(detection_scale)
        valid_faction, _ = ConfigValidator.validate_detection_scale(faction_scale)
        valid_cooldown, _ = ConfigValidator.validate_cooldown_timer(cooldown)
        
        # All should be valid
        self.assertTrue(valid_detection)
        self.assertTrue(valid_faction)
        self.assertTrue(valid_cooldown)

    def test_runtime_settings_invalid_workflow(self):
        """Test runtime settings workflow with invalid values."""
        # Simulate user entering invalid settings
        detection_scale = 150  # Too high
        cooldown = -10  # Negative
        
        # Validate settings
        valid_detection, error_detection = ConfigValidator.validate_detection_scale(detection_scale)
        valid_cooldown, error_cooldown = ConfigValidator.validate_cooldown_timer(cooldown)
        
        # Both should be invalid
        self.assertFalse(valid_detection)
        self.assertFalse(valid_cooldown)
        self.assertIsNotNone(error_detection)
        self.assertIsNotNone(error_cooldown)


if __name__ == '__main__':
    unittest.main()
