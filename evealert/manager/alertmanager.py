import asyncio
import logging
import os
import random
import time
from typing import TYPE_CHECKING

import numpy as np
import sounddevice as sd
import soundfile as sf

from evealert.constants import (
    ALARM_SOUND_FILE,
    ALERT_IMAGE_PREFIX,
    AUDIO_CHANNELS,
    DEFAULT_COOLDOWN_TIMER,
    FACTION_IMAGE_PREFIX,
    FACTION_SOUND_FILE,
    IMG_FOLDER,
    MAIN_CHECK_SLEEP_MAX,
    MAIN_CHECK_SLEEP_MIN,
    MAX_SOUND_TRIGGERS,
    SOUND_FOLDER,
    VISION_SLEEP_INTERVAL,
    WEBHOOK_COOLDOWN,
)
from evealert.settings.helper import get_resource_path
from evealert.settings.validator import ConfigValidator
from evealert.statistics import AlarmStatistics
from evealert.tools.vision import Vision
from evealert.tools.windowscapture import WindowCapture

if TYPE_CHECKING:
    from evealert.menu.main import MainMenu

# Sound file paths
ALARM_SOUND = get_resource_path(f"{SOUND_FOLDER}/{ALARM_SOUND_FILE}")
FACTION_SOUND = get_resource_path(f"{SOUND_FOLDER}/{FACTION_SOUND_FILE}")
IMG_FOLDER_PATH = get_resource_path(IMG_FOLDER)

ALERT_FILES = [
    os.path.join(IMG_FOLDER_PATH, filename)
    for filename in os.listdir(IMG_FOLDER_PATH)
    if filename.startswith(ALERT_IMAGE_PREFIX)
]
FACTION_FILES = [
    os.path.join(IMG_FOLDER_PATH, filename)
    for filename in os.listdir(IMG_FOLDER_PATH)
    if filename.startswith(FACTION_IMAGE_PREFIX)
]

logger = logging.getLogger("alert")


class AlertAgent:
    """Alert Agent for EVE Online local chat monitoring.

    This class manages the complete alert system including:
    - Screenshot capture and analysis
    - Enemy and faction detection via template matching
    - Audio alerts with cooldown management
    - Discord webhook notifications
    - Vision debug windows
    """

    def __init__(self, main: "MainMenu"):
        """Initialize the Alert Agent.

        Args:
            main: Reference to the MainMenu instance
        """
        self.main = main
        self.loop = asyncio.get_event_loop()
        self.wincap = WindowCapture(self.main)
        self.alert_vision = Vision(ALERT_FILES)
        self.alert_vision_faction = Vision(FACTION_FILES)

        # Main Settings
        self.running = False
        self.check = False

        # Main lock for alarm processing - prevents multiple simultaneous alarm checks
        self.lock = asyncio.Lock()
        # Note: Vision threads don't need separate locks as they only write to
        # self.enemy and self.faction flags, which are atomic operations in Python

        # Vision Settings
        self.enemy = False
        self.faction = False

        # Alarm Settings
        self.cooldown_timers = {}
        self.cooldowntimer = DEFAULT_COOLDOWN_TIMER
        self.alarm_detected = False
        self.mute = False
        self.volume = 1.0  # Default volume: 100% (0.0 to 1.0)

        # Webhook Settings
        self.webhook_cooldown_timer = 0
        self.webhook_sent = False

        # Sound Settings
        self.p = sd
        self.alarm_trigger_counts = {}
        self.max_sound_triggers = MAX_SOUND_TRIGGERS
        self.currently_playing_sounds = {}

        # Statistics
        self.statistics = AlarmStatistics()

        self.load_settings()
        self._validate_audio_files()

    def _validate_audio_files(self):
        """Validate that required audio files exist."""
        valid_alarm, error_alarm = ConfigValidator.validate_audio_file(
            ALARM_SOUND, "Alarm sound"
        )
        valid_faction, error_faction = ConfigValidator.validate_audio_file(
            FACTION_SOUND, "Faction sound"
        )

        if not valid_alarm:
            logger.warning(error_alarm)
            self.main.write_message(f"Warning: {error_alarm}", "red")

        if not valid_faction:
            logger.warning(error_faction)
            self.main.write_message(f"Warning: {error_faction}", "red")

    @property
    def is_running(self) -> bool:
        return self.running

    @property
    def is_alarm(self) -> bool:
        return self.alarm_detected

    @property
    def is_enemy(self) -> bool:
        return self.enemy

    @property
    def is_faction(self) -> bool:
        return self.faction

    def get_statistics(self) -> AlarmStatistics:
        """Get alarm statistics tracker.

        Returns:
            AlarmStatistics instance with current statistics
        """
        return self.statistics

    def clean_up(self) -> None:
        self.stop()
        self.main.write_message("System: EVE Alert stopped.", "green")

    def start(self) -> bool:
        self.loop.run_until_complete(self.vision_check())
        if self.check is True:

            self.vison_t = self.loop.create_task(self.vision_thread())
            self.vision_faction_t = self.loop.create_task(self.vision_faction_thread())

            # Start the Alarm
            self.alert_t = self.loop.create_task(self.run())

            self.running = True
            self.main.write_message("System: EVE Alert started.", "green")
            self.loop.run_forever()
            logger.debug("Alle Tasks wurden gestartet")
            return True
        return False

    def stop(self) -> None:
        self.loop.stop()
        self.running = False
        self.currently_playing_sounds = {}
        self.alarm_trigger_counts = {}
        self.cooldown_timers = {}
        self.alert_vision.debug_mode = False
        self.alert_vision_faction.debug_mode_faction = False
        self.main.update_alert_button()
        self.main.update_faction_button()

    def load_settings(self) -> None:
        settings = self.main.menu.setting.load_settings()

        if settings:
            # Validate settings
            is_valid, errors = ConfigValidator.validate_settings_dict(settings)
            if not is_valid:
                error_msg = "Configuration validation failed:\n" + "\n".join(errors)
                logger.error(error_msg)
                self.main.write_message(
                    "Settings validation failed. Check logs.", "red"
                )
                for error in errors:
                    self.main.write_message(f"  - {error}", "red")
                return
            self.x1 = int(settings["alert_region_1"]["x"])
            self.y1 = int(settings["alert_region_1"]["y"])
            self.x2 = int(settings["alert_region_2"]["x"])
            self.y2 = int(settings["alert_region_2"]["y"])
            self.x1_faction = int(settings["faction_region_1"]["x"])
            self.y1_faction = int(settings["faction_region_1"]["y"])
            self.x2_faction = int(settings["faction_region_2"]["x"])
            self.y2_faction = int(settings["faction_region_2"]["y"])
            self.detection = int(settings["detectionscale"]["value"])
            self.detection_faction = int(settings["faction_scale"]["value"])
            self.cooldowntimer = int(settings["cooldown_timer"]["value"])
            self.volume = (
                settings.get("volume", {}).get("value", 100) / 100.0
            )  # Convert to 0.0-1.0
            self.mute = settings["server"]["mute"]
            if self.main.menu.setting.is_changed:
                vision_opened = False
                factiom_vision_opened = False
                if self.alert_vision.is_vision_open:
                    vision_opened = True
                if self.alert_vision_faction.is_faction_vision_open:
                    factiom_vision_opened = True
                # Reload the Vision
                self.alert_vision = Vision(ALERT_FILES)
                self.alert_vision_faction = Vision(FACTION_FILES)
                if vision_opened:
                    self.set_vision()
                if factiom_vision_opened:
                    self.set_vision_faction()
                self.main.write_message("Settings: Loaded.", "green")

    def set_vision(self) -> None:
        if self.is_running:
            self.alert_vision.debug_mode = not self.alert_vision.debug_mode
            self.main.update_alert_button()

    def set_vision_faction(self) -> None:
        if self.is_running:
            self.alert_vision_faction.debug_mode_faction = (
                not self.alert_vision_faction.debug_mode_faction
            )
            self.main.update_faction_button()

    async def vision_check(self) -> None:
        """Validate that screenshot capture works for configured alert region."""
        self.load_settings()
        screenshot, _ = self.wincap.get_screenshot_value(
            self.y1, self.x1, self.x2, self.y2
        )
        if screenshot is not None:
            self.check = True
        else:
            self.main.write_message("Wrong Alert Settings.", "red")
            self.check = False

    async def vision_thread(self) -> None:
        """Continuously check for enemy detection in the alert region."""
        while True:
            screenshot, _ = self.wincap.get_screenshot_value(
                self.y1, self.x1, self.x2, self.y2
            )
            if screenshot is not None:
                enemy = self.alert_vision.find(screenshot, self.detection)
                if enemy == "Error":
                    self.clean_up()
                if enemy:
                    self.enemy = True
                else:
                    self.enemy = False
            else:
                self.main.write_message("Wrong Alert Settings.", "red")
                self.clean_up()
            await asyncio.sleep(VISION_SLEEP_INTERVAL)

    async def vision_faction_thread(self) -> None:
        """Continuously check for faction detection in the faction region."""
        while True:
            screenshot_faction, _ = self.wincap.get_screenshot_value(
                self.y1_faction, self.x1_faction, self.x2_faction, self.y2_faction
            )
            if screenshot_faction is not None:
                faction = self.alert_vision_faction.find_faction(
                    screenshot_faction, self.detection_faction
                )

                if faction:
                    self.faction = True
                else:
                    self.faction = False
            await asyncio.sleep(VISION_SLEEP_INTERVAL)

    async def reset_alarm(self, alarm_type: str) -> None:
        """Reset alarm counters and cooldown for the given alarm type."""
        if alarm_type in self.alarm_trigger_counts:
            self.alarm_trigger_counts[alarm_type] = 0
            self.cooldown_timers[alarm_type] = 0

        if self.main.webhook and alarm_type == "Enemy":
            if self.webhook_sent is True:
                self.main.webhook.execute(
                    f"Alarm Reset: {self.main.menu.setting.system_name.get()}!"
                )
            self.webhook_sent = False

    async def alarm_detection(
        self, alarm_text: str, sound: str = ALARM_SOUND, alarm_type: str = "Enemy"
    ) -> None:
        """Trigger an alarm with text message, sound, and webhook notification."""
        self.main.write_message(
            f"{alarm_text}",
            "red",
        )
        # Track alarm in statistics
        self.statistics.add_alarm(alarm_type)
        await self.play_sound(sound, alarm_type)
        await self.send_webhook_message(alarm_type)

    async def send_webhook_message(self, alarm_type: str) -> None:
        """Send webhook notification for enemy alarms with cooldown."""
        current_time = time.time()
        # Ensure to limit the webhook sending to once per WEBHOOK_COOLDOWN
        if current_time < self.webhook_cooldown_timer:
            logger.info("Webhook is in cooldown period. Message not sent.")
            return

        if self.main.webhook and alarm_type == "Enemy" and self.webhook_sent is False:
            # Send the webhook message
            try:
                msg = f"Enemy Appears in {self.main.menu.setting.system_name.get()}!"
                self.main.webhook.execute(msg)
                self.webhook_cooldown_timer = current_time + WEBHOOK_COOLDOWN
                self.webhook_sent = True

            except Exception as e:
                logger.error("Error sending webhook: %s", e)

    async def play_sound(self, sound: str, alarm_type: str) -> None:
        """Play alarm sound with trigger limits and cooldown management."""
        if self.mute:
            return

        # Initialize counter and cooldown timer if not present
        if alarm_type not in self.alarm_trigger_counts:
            self.alarm_trigger_counts[alarm_type] = 0
        if alarm_type not in self.cooldown_timers:
            self.cooldown_timers[alarm_type] = 0

        # Check cooldown timer
        current_time = time.time()
        if current_time < self.cooldown_timers[alarm_type]:
            self.main.write_message(
                f"{alarm_type} Sound is in cooldown period.", "yellow"
            )
            return

        # Increment the counter
        self.alarm_trigger_counts[alarm_type] += 1

        # Check if the alarm has been triggered three times
        if self.alarm_trigger_counts[alarm_type] > self.max_sound_triggers:
            self.cooldown_timers[alarm_type] = current_time + self.cooldowntimer
            self.alarm_trigger_counts[alarm_type] = 0
            self.main.write_message(
                f"{alarm_type} Sound is now in cooldown for {self.cooldowntimer} seconds.",
                "yellow",
            )
            return

        if alarm_type not in self.currently_playing_sounds:
            self.currently_playing_sounds[alarm_type] = True
            try:
                # Read audio data with soundfile
                data, samplerate = sf.read(sound, dtype="int16")

                # Check data shape and adjust channels if necessary
                if data.ndim == 1:
                    # Convert Mono -> Stereo
                    data = np.stack([data, data], axis=-1)
                elif data.ndim == 2 and data.shape[1] == 1:
                    # (N, 1) -> (N, AUDIO_CHANNELS)
                    data = np.repeat(data, AUDIO_CHANNELS, axis=1)

                # Apply volume
                data_with_volume = (data * self.volume).astype("int16")

                # Play the audio data
                sd.play(data_with_volume, samplerate)
                await asyncio.sleep(
                    len(data) / samplerate
                )  # Wait for the sound to finish
            except Exception as e:
                if self.alarm_trigger_counts[alarm_type] <= 1:
                    self.main.open_error_window(
                        "Error Playing Sound. Check Logs for more information."
                    )
                logger.exception("Error Playing Sound: %s", e)
            finally:
                self.currently_playing_sounds.pop(alarm_type, None)

    async def run(self) -> None:
        """Main alert checking loop."""
        async with self.lock:
            while True:
                # Reload settings if changed
                if self.main.menu.setting.is_changed:
                    self.load_settings()
                    self.main.menu.setting.changed = False

                # Reset alarm status
                self.alarm_detected = False

                try:
                    if self.faction:
                        self.alarm_detected = True
                        await self.alarm_detection(
                            "Faction Spawn!", FACTION_SOUND, "Faction"
                        )
                    if self.enemy:
                        self.alarm_detected = True
                        await self.alarm_detection(
                            "Enemy Appears!", ALARM_SOUND, "Enemy"
                        )
                except ValueError as e:
                    logger.error("Alert System Error: %s", e)
                    self.stop()
                    self.main.write_message("Something went wrong.", "red")
                    return

                # Check if any of the images was detected
                if not self.faction:
                    await self.reset_alarm("Faction")
                if not self.enemy:
                    await self.reset_alarm("Enemy")

                sleep_time = random.uniform(MAIN_CHECK_SLEEP_MIN, MAIN_CHECK_SLEEP_MAX)
                self.main.write_message(
                    f"Next check in {sleep_time:.2f} seconds...",
                )
                await asyncio.sleep(sleep_time)
