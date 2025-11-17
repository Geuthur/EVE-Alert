"""Logging configuration for EVE Alert application."""

import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from evealert.constants import (
    LOG_BACKUP_COUNT,
    LOG_DATE_FORMAT,
    LOG_DEFAULT_LEVEL,
    LOG_FORMAT_STRING,
    LOG_MAX_BYTES,
)
from evealert.settings.helper import get_resource_path

# Create logs directory
LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)

# Create formatter
LOG_FORMAT = logging.Formatter(
    LOG_FORMAT_STRING,
    datefmt=LOG_DATE_FORMAT,
)


def create_fh(name: str, level: Optional[int] = None) -> RotatingFileHandler:
    """
    Create a rotating file handler for logging.

    Args:
        name: Name of the log file (without extension)
        level: Optional logging level for this handler

    Returns:
        Configured RotatingFileHandler instance
    """
    fh = RotatingFileHandler(
        filename=Path(LOG_PATH, f"{name}.log"),
        encoding="utf-8",
        mode="a",
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
    )
    fh.setFormatter(LOG_FORMAT)
    if level is not None:
        fh.setLevel(level)
    return fh


def create_console_handler(level: Optional[int] = None) -> logging.StreamHandler:
    """
    Create a console handler for logging to stdout.

    Args:
        level: Optional logging level for this handler

    Returns:
        Configured StreamHandler instance
    """
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(LOG_FORMAT)
    if level is not None:
        ch.setLevel(level)
    return ch


def setup_logger(
    name: str, level: Optional[str] = None, console_output: bool = False
) -> logging.Logger:
    """
    Create a logger with file and optional console output.

    Args:
        name: Name of the logger
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Whether to also log to console

    Returns:
        Configured Logger instance
    """
    # Try to load log level from settings
    if level is None:
        config_path = get_resource_path("settings.json")
        try:
            with open(config_path, encoding="utf-8") as config_file:
                settings = json.load(config_file)
                level = settings.get("log_level", LOG_DEFAULT_LEVEL)
        except (FileNotFoundError, json.JSONDecodeError):
            level = LOG_DEFAULT_LEVEL

    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    logger.propagate = False  # Prevent duplicate logs

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Add file handler
    logger.addHandler(create_fh(name))

    # Add console handler if requested
    if console_output:
        logger.addHandler(create_console_handler())

    return logger


# Create default loggers for different modules
# These can be imported and used throughout the application
main_log = setup_logger("main")
alert_log = setup_logger("alert")
menu_log = setup_logger("menu")
tools_log = setup_logger("tools")
test_log = setup_logger("test")
validator_log = setup_logger("validator")

# Root logger configuration
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors from third-party libraries
    format=LOG_FORMAT_STRING,
    datefmt=LOG_DATE_FORMAT,
)

__all__ = [
    "setup_logger",
    "main_log",
    "alert_log",
    "menu_log",
    "tools_log",
    "test_log",
    "validator_log",
]
