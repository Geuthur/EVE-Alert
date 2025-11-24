"""Helper utilities for EVE Alert application.

Provides resource path resolution and constants.
"""

import sys
from pathlib import Path

# Path to application icon
ICON = "img/eve.ico"

# Absolute path to the evealert package root
PACKAGE_ROOT = Path(__file__).resolve().parent.parent

# Directory containing the running executable/script (writable location)
EXEC_ROOT = Path(sys.argv[0]).resolve().parent


def get_resource_path(relative_path: str) -> str:
    """Get the absolute path to a resource file.

    Always reads from the executable's directory structure.
    For bundled exe: reads from folder next to the exe.
    For development: reads from package directory.

    Args:
        relative_path: Path like "sound/alarm.wav" or "img/icon.png"

    Returns:
        Absolute path to the resource file

    Example:
        >>> get_resource_path("sound/alarm.wav")
        'C:/path/to/exe/sound/alarm.wav'
    """
    if not relative_path:
        raise ValueError("relative_path must be provided")

    relative = Path(relative_path)

    if relative.is_absolute():
        return str(relative)

    # If running as bundled exe, use exe directory
    if getattr(sys, 'frozen', False):
        # We are running as compiled exe
        exe_dir = Path(sys.executable).parent
        resource_path = (exe_dir / relative).resolve()
        return str(resource_path)
    
    # Development mode: strip 'evealert/' prefix and use PACKAGE_ROOT
    relative_stripped = relative
    if relative.parts and relative.parts[0].lower() == "evealert":
        relative_stripped = Path(*relative.parts[1:])
    
    resource_path = (PACKAGE_ROOT / relative_stripped).resolve()
    
    # Fallback to EXEC_ROOT if not found in PACKAGE_ROOT
    if not resource_path.exists():
        resource_path = (EXEC_ROOT / relative_stripped).resolve()
    
    return str(resource_path)
