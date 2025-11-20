"""Helper utilities for EVE Alert application.

Provides resource path resolution and constants.
"""

import os

# Path to application icon
ICON = "img/eve.ico"


def get_resource_path(relative_path: str) -> str:
    """Get the absolute path to a resource file.

    Resolves relative paths within the evealert directory structure.
    Useful for accessing images, sounds, and configuration files.

    Args:
        relative_path: Path relative to the evealert directory

    Returns:
        Absolute path to the resource file

    Example:
        >>> get_resource_path("img/online.png")
        'C:/path/to/evealert/img/online.png'
    """
    base_path = os.path.abspath("evealert/.")
    return os.path.join(base_path, relative_path)
