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
    if not relative_path:
        raise ValueError("relative_path must be provided")

    relative = Path(relative_path)

    # Allow callers to pass paths prefixed with the package name (e.g. "evealert/img")
    if relative.parts and relative.parts[0].lower() == "evealert":
        relative = Path(*relative.parts[1:])

    if relative.is_absolute():
        return str(relative)

    search_roots = [PACKAGE_ROOT, EXEC_ROOT]

    # When bundled with PyInstaller, resources might reside in the temporary
    # extraction directory referenced by sys._MEIPASS. Add it (and the nested
    # evealert folder) as fallbacks when files are copied outside the package.
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        bundle_root_path = Path(bundle_root)
        search_roots.append(bundle_root_path)
        search_roots.append(bundle_root_path / "evealert")

    for root in search_roots:
        candidate = (root / relative).resolve()
        if candidate.exists():
            return str(candidate)

    # Final fallback: return the path under the executable directory so files
    # like settings.json can be created next to the app when they don't exist
    # yet (e.g., on first run of the bundled exe).
    return str((EXEC_ROOT / relative).resolve())
