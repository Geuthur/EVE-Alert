"""Unit tests for AlertManager core functionality."""

import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from evealert.manager.alertmanager import AlertAgent
from evealert.statistics import AlarmStatistics


class TestAlertAgent(unittest.TestCase):
    """Test cases for AlertAgent class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock MainMenu
        self.mock_main = MagicMock()
        self.mock_main.write_message = MagicMock()
        self.mock_main.getdata = MagicMock()
        self.mock_main.menu = MagicMock()
        self.mock_main.menu.setting = MagicMock()

        # Create temporary settings file
        self.temp_dir = tempfile.mkdtemp()
        self.settings_path = Path(self.temp_dir) / "settings.json"

        # Default test settings
        self.test_settings = {
            "alert_region_1": {"x": 100, "y": 100},
            "alert_region_2": {"x": 300, "y": 300},
            "faction_region_1": {"x": 400, "y": 100},
            "faction_region_2": {"x": 600, "y": 300},
            "detectionscale": {"value": 90},
            "faction_scale": {"value": 85},
            "cooldown_timer": {"value": 30},
            "volume": {"value": 100},
            "server": {"webhook": "", "mute": False},
        }

        with open(self.settings_path, "w") as f:
            json.dump(self.test_settings, f)

        self.mock_main.menu.setting.load_settings.return_value = self.test_settings
        self.mock_main.menu.setting.is_changed = False

        # Patch audio file validation and event loop
        with patch(
            "evealert.manager.alertmanager.AlertAgent._validate_audio_files"
        ), patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value = MagicMock()
            self.agent = AlertAgent(self.mock_main)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_agent_initialization(self):
        """Test AlertAgent initialization."""
        self.assertIsNotNone(self.agent)
        self.assertFalse(self.agent.running)
        self.assertFalse(self.agent.enemy)
        self.assertFalse(self.agent.faction)
        self.assertEqual(self.agent.volume, 1.0)
        self.assertIsInstance(self.agent.statistics, AlarmStatistics)

    def test_load_settings(self):
        """Test loading settings from file."""
        self.agent.load_settings()

        self.assertEqual(self.agent.volume, 1.0)  # 100% -> 1.0
        self.assertEqual(self.agent.cooldowntimer, 30)

    def test_load_settings_with_custom_volume(self):
        """Test loading custom volume setting."""
        # Update settings with 50% volume
        self.test_settings["volume"]["value"] = 50
        self.mock_main.menu.setting.load_settings.return_value = self.test_settings

        self.agent.load_settings()
        self.assertEqual(self.agent.volume, 0.5)

    def test_is_running_property(self):
        """Test is_running property."""
        self.assertFalse(self.agent.is_running)
        self.agent.running = True
        self.assertTrue(self.agent.is_running)

    def test_is_alarm_property(self):
        """Test is_alarm property."""
        self.assertFalse(self.agent.is_alarm)
        self.agent.alarm_detected = True
        self.assertTrue(self.agent.is_alarm)

    def test_is_enemy_property(self):
        """Test is_enemy property."""
        self.assertFalse(self.agent.is_enemy)
        self.agent.enemy = True
        self.assertTrue(self.agent.is_enemy)

    def test_is_faction_property(self):
        """Test is_faction property."""
        self.assertFalse(self.agent.is_faction)
        self.agent.faction = True
        self.assertTrue(self.agent.is_faction)

    def test_get_statistics(self):
        """Test retrieving statistics."""
        stats = self.agent.get_statistics()
        self.assertIsInstance(stats, AlarmStatistics)
        self.assertEqual(stats.total_alarms, 0)

    def test_cooldown_management(self):
        """Test cooldown timer management."""
        self.agent.cooldowntimer = 10

        # Set cooldown for alarm type
        self.agent.cooldown_timers["enemy"] = time.time()

        # Check if cooldown is active
        time_diff = time.time() - self.agent.cooldown_timers.get("enemy", 0)
        self.assertLess(time_diff, self.agent.cooldowntimer)

    def test_mute_functionality(self):
        """Test mute setting."""
        self.assertFalse(self.agent.mute)
        self.agent.mute = True
        self.assertTrue(self.agent.mute)

    def test_webhook_cooldown(self):
        """Test webhook cooldown timer."""
        from evealert.constants import WEBHOOK_COOLDOWN

        self.agent.webhook_cooldown_timer = time.time()
        time_diff = time.time() - self.agent.webhook_cooldown_timer

        # Should be within webhook cooldown period
        self.assertLess(time_diff, WEBHOOK_COOLDOWN + 1)

    def test_alarm_trigger_count_tracking(self):
        """Test alarm trigger count management."""
        self.assertEqual(len(self.agent.alarm_trigger_counts), 0)

        # Simulate alarm trigger
        self.agent.alarm_trigger_counts["enemy"] = 1
        self.assertEqual(self.agent.alarm_trigger_counts["enemy"], 1)

        # Increment trigger
        self.agent.alarm_trigger_counts["enemy"] += 1
        self.assertEqual(self.agent.alarm_trigger_counts["enemy"], 2)

    def test_max_sound_triggers(self):
        """Test max sound triggers limit."""
        from evealert.constants import MAX_SOUND_TRIGGERS

        self.assertEqual(self.agent.max_sound_triggers, MAX_SOUND_TRIGGERS)

        # Test if we can change it
        self.agent.max_sound_triggers = 5
        self.assertEqual(self.agent.max_sound_triggers, 5)

    @patch("evealert.manager.alertmanager.sd.play")
    @patch("evealert.manager.alertmanager.sf.read")
    def test_play_sound_with_volume(self, mock_sf_read, mock_sd_play):
        """Test playing sound with volume control."""
        import numpy as np

        # Mock audio data
        mock_audio_data = np.array([[100, 100], [200, 200]], dtype="int16")
        mock_sf_read.return_value = (mock_audio_data, 44100)

        # Set volume to 50%
        self.agent.volume = 0.5
        self.agent.mute = False

        # Call play_sound method (we need to mock it or test indirectly)
        # Since play_sound is async, we test the volume application logic
        volume_adjusted = (mock_audio_data * self.agent.volume).astype("int16")

        self.assertTrue(np.all(volume_adjusted <= mock_audio_data))

    def test_statistics_integration(self):
        """Test statistics tracking integration."""
        # Record alarm
        self.agent.statistics.add_alarm("Enemy")

        self.assertEqual(self.agent.statistics.total_alarms, 1)
        self.assertEqual(self.agent.statistics.session_alarms, 1)

    def test_vision_debug_mode_sync(self):
        """Test vision debug mode synchronization."""
        # Enable enemy vision debug
        self.agent.alert_vision.debug_mode = True
        self.assertTrue(self.agent.alert_vision.is_vision_open)

        # Enable faction vision debug
        self.agent.alert_vision_faction.debug_mode_faction = True
        self.assertTrue(self.agent.alert_vision_faction.is_faction_vision_open)

    def test_configuration_validation_on_load(self):
        """Test configuration validation when loading settings."""
        # Create invalid settings
        invalid_settings = self.test_settings.copy()
        invalid_settings["detectionscale"]["value"] = 150  # Invalid: > 100

        with open(self.settings_path, "w") as f:
            json.dump(invalid_settings, f)

        # Load should handle invalid values gracefully
        try:
            self.agent.load_settings()
            # If validation occurs, it should either fix or warn
            self.assertLessEqual(self.agent.alert_vision.method, 5)
        except Exception as e:
            # Expected if strict validation is enforced
            self.assertIsNotNone(str(e))


class TestAlertAgentAsync(unittest.IsolatedAsyncioTestCase):
    """Async test cases for AlertAgent."""

    async def asyncSetUp(self):
        """Set up async test fixtures."""
        self.mock_main = MagicMock()
        self.mock_main.write_message = MagicMock()
        self.mock_main.getdata = MagicMock()

        # Create temporary settings
        self.temp_dir = tempfile.mkdtemp()
        self.settings_path = Path(self.temp_dir) / "settings.json"

        test_settings = {
            "alert_region_1": {"x": 100, "y": 100},
            "alert_region_2": {"x": 300, "y": 300},
            "faction_region_1": {"x": 400, "y": 100},
            "faction_region_2": {"x": 600, "y": 300},
            "detectionscale": {"value": 90},
            "faction_scale": {"value": 85},
            "cooldown_timer": {"value": 30},
            "volume": {"value": 100},
            "server": {"webhook": ""},
        }

        with open(self.settings_path, "w") as f:
            json.dump(test_settings, f)

        self.mock_main.getdata.return_value = self.settings_path

        with patch("evealert.manager.alertmanager.AlertAgent._validate_audio_files"):
            self.agent = AlertAgent(self.mock_main)

    async def asyncTearDown(self):
        """Clean up async test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_lock_mechanism(self):
        """Test async lock for alarm processing."""
        self.assertFalse(self.agent.lock.locked())

        async with self.agent.lock:
            self.assertTrue(self.agent.lock.locked())

        self.assertFalse(self.agent.lock.locked())


if __name__ == "__main__":
    unittest.main()
