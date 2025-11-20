"""Custom exceptions for EVE Alert application."""


class EVEAlertException(Exception):
    """Base exception for all EVE Alert errors."""


class ScreenshotError(EVEAlertException):
    """Raised when screenshot capture or processing fails."""


class RegionSizeError(EVEAlertException):
    """Raised when a region size is invalid or too small."""


class WrongImageType(EVEAlertException):
    """Raised when an image has an unexpected or unsupported type."""


class ConfigurationError(EVEAlertException):
    """Raised when configuration is invalid or missing."""


class ValidationError(EVEAlertException):
    """Raised when validation of settings or inputs fails."""


class AudioError(EVEAlertException):
    """Raised when audio playback or file loading fails."""


class WebhookError(EVEAlertException):
    """Raised when webhook operations fail."""
