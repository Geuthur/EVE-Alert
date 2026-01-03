"""Configuration validation utilities for EVE Alert."""

import logging
import os
from typing import Any, Dict, Optional, Tuple

from evealert.constants import DETECTION_SCALE_MAX, DETECTION_SCALE_MIN

logger = logging.getLogger("validator")


class ConfigValidator:
    """Validates EVE Alert configuration settings."""

    @staticmethod
    def validate_region_coordinates(
        x1: int, y1: int, x2: int, y2: int, region_name: str = "Region"
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate region coordinates.

        Args:
            x1: Left coordinate
            y1: Top coordinate
            x2: Right coordinate
            y2: Bottom coordinate
            region_name: Name of the region for error messages

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not all(isinstance(coord, (int, float)) for coord in [x1, y1, x2, y2]):
            return False, f"{region_name}: Coordinates must be numeric"

        if x1 >= x2:
            return False, f"{region_name}: x1 ({x1}) must be less than x2 ({x2})"

        if y1 >= y2:
            return False, f"{region_name}: y1 ({y1}) must be less than y2 ({y2})"

        # TODO Has been disabled for now: re-enable if needed
        # Only check horizontal coordinates for negativity; vertical can be negative for multi-monitor setups
        #if any(coord < 0 for coord in [x1, x2]):
        #    return False, f"{region_name}: Coordinates cannot be negative"

        # Check minimum size (at least 10x10 pixels)
        width = x2 - x1
        height = y2 - y1
        if width < 10 or height < 10:
            return (
                False,
                f"{region_name}: Region too small ({width}x{height}). Minimum 10x10 pixels",
            )

        return True, None

    @staticmethod
    def validate_detection_scale(
        scale: int, scale_name: str = "Detection scale"
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate detection scale value.

        Args:
            scale: Detection scale percentage
            scale_name: Name of the scale for error messages

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(scale, (int, float)):
            return False, f"{scale_name}: Must be numeric"

        if not DETECTION_SCALE_MIN <= scale <= DETECTION_SCALE_MAX:
            return (
                False,
                f"{scale_name}: Must be between {DETECTION_SCALE_MIN} and {DETECTION_SCALE_MAX}",
            )

        return True, None

    @staticmethod
    def validate_cooldown_timer(timer: int) -> Tuple[bool, Optional[str]]:
        """
        Validate cooldown timer value.

        Args:
            timer: Cooldown timer in seconds

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(timer, (int, float)):
            return False, "Cooldown timer: Must be numeric"

        if timer < 0:
            return False, "Cooldown timer: Cannot be negative"

        if timer > 3600:  # Max 1 hour
            return False, "Cooldown timer: Cannot exceed 3600 seconds (1 hour)"

        return True, None

    @staticmethod
    def validate_webhook_url(url: str) -> Tuple[bool, Optional[str]]:
        """
        Validate webhook URL format.

        Args:
            url: Webhook URL

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url:
            return True, None  # Empty URL is valid (webhook is optional)

        if not isinstance(url, str):
            return False, "Webhook URL: Must be a string"

        # Basic URL validation
        if not url.startswith(("http://", "https://")):
            return False, "Webhook URL: Must start with http:// or https://"

        # Discord webhook validation
        if "discord.com" in url and "/api/webhooks/" not in url:
            return False, "Webhook URL: Invalid Discord webhook format"

        return True, None

    @staticmethod
    def validate_audio_file(
        file_path: str, file_name: str = "Audio file"
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate audio file exists and is accessible.

        Args:
            file_path: Path to audio file
            file_name: Name of the file for error messages

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_path:
            return False, f"{file_name}: Path cannot be empty"

        if not isinstance(file_path, str):
            return False, f"{file_name}: Path must be a string"

        if not os.path.exists(file_path):
            return False, f"{file_name}: File not found at {file_path}"

        if not os.path.isfile(file_path):
            return False, f"{file_name}: Path is not a file: {file_path}"

        # Check file extension
        valid_extensions = [".wav", ".mp3", ".ogg", ".flac"]
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in valid_extensions:
            return (
                False,
                f"{file_name}: Invalid audio format. Supported: {', '.join(valid_extensions)}",
            )

        return True, None

    @staticmethod
    def validate_settings_dict(settings: Dict[str, Any]) -> Tuple[bool, list]:
        """
        Validate complete settings dictionary.

        Args:
            settings: Settings dictionary to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Validate alert region
        if "alert_region_1" in settings and "alert_region_2" in settings:
            try:
                x1 = int(settings["alert_region_1"]["x"])
                y1 = int(settings["alert_region_1"]["y"])
                x2 = int(settings["alert_region_2"]["x"])
                y2 = int(settings["alert_region_2"]["y"])
                valid, error = ConfigValidator.validate_region_coordinates(
                    x1, y1, x2, y2, "Alert Region"
                )
                if not valid:
                    errors.append(error)
            except (KeyError, ValueError, TypeError) as e:
                errors.append(f"Alert Region: Invalid format - {str(e)}")

        # Validate faction region
        if "faction_region_1" in settings and "faction_region_2" in settings:
            try:
                x1 = int(settings["faction_region_1"]["x"])
                y1 = int(settings["faction_region_1"]["y"])
                x2 = int(settings["faction_region_2"]["x"])
                y2 = int(settings["faction_region_2"]["y"])
                valid, error = ConfigValidator.validate_region_coordinates(
                    x1, y1, x2, y2, "Faction Region"
                )
                if not valid:
                    errors.append(error)
            except (KeyError, ValueError, TypeError) as e:
                errors.append(f"Faction Region: Invalid format - {str(e)}")

        # Validate detection scale
        if "detectionscale" in settings:
            try:
                scale = int(settings["detectionscale"]["value"])
                valid, error = ConfigValidator.validate_detection_scale(
                    scale, "Alert Detection Scale"
                )
                if not valid:
                    errors.append(error)
            except (KeyError, ValueError, TypeError) as e:
                errors.append(f"Alert Detection Scale: Invalid format - {str(e)}")

        # Validate faction scale
        if "faction_scale" in settings:
            try:
                scale = int(settings["faction_scale"]["value"])
                valid, error = ConfigValidator.validate_detection_scale(
                    scale, "Faction Detection Scale"
                )
                if not valid:
                    errors.append(error)
            except (KeyError, ValueError, TypeError) as e:
                errors.append(f"Faction Detection Scale: Invalid format - {str(e)}")

        # Validate cooldown timer
        if "cooldown_timer" in settings:
            try:
                timer = int(settings["cooldown_timer"]["value"])
                valid, error = ConfigValidator.validate_cooldown_timer(timer)
                if not valid:
                    errors.append(error)
            except (KeyError, ValueError, TypeError) as e:
                errors.append(f"Cooldown Timer: Invalid format - {str(e)}")

        # Validate webhook URL
        if "server" in settings and "webhook" in settings["server"]:
            try:
                url = settings["server"]["webhook"]
                valid, error = ConfigValidator.validate_webhook_url(url)
                if not valid:
                    errors.append(error)
            except (KeyError, TypeError) as e:
                errors.append(f"Webhook URL: Invalid format - {str(e)}")

        return len(errors) == 0, errors
