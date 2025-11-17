"""Custom exceptions for EVE Alert application."""


class EVEAlertException(Exception):
    """Base exception for all EVE Alert errors."""

    pass


class ScreenshotError(EVEAlertException):
    """Raised when screenshot capture or processing fails."""

    pass


class RegionSizeError(EVEAlertException):
    """Raised when a region size is invalid or too small."""

    pass


class WrongImageType(EVEAlertException):
    """Raised when an image has an unexpected or unsupported type."""

    pass


class ConfigurationError(EVEAlertException):
    """Raised when configuration is invalid or missing."""

    pass


class ValidationError(EVEAlertException):
    """Raised when validation of settings or inputs fails."""

    pass


class AudioError(EVEAlertException):
    """Raised when audio playback or file loading fails."""

    pass


class WebhookError(EVEAlertException):
    """Raised when webhook operations fail."""

    pass
