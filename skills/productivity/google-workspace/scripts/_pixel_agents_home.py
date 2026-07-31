"""Resolve PIXEL_AGENTS_HOME for standalone skill scripts.

Skill scripts may run outside the Pixel Agents process (e.g. system Python,
nix env, CI) where ``pixel_constants`` is not importable.  This module
provides the same ``get_pixel_agents_home()`` and ``display_pixel_agents_home()``
contracts as ``pixel_constants`` without requiring it on ``sys.path``.

When ``pixel_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``pixel_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``PIXEL_AGENTS_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from pixel_constants import display_pixel_agents_home as display_pixel_agents_home
    from pixel_constants import get_pixel_agents_home as get_pixel_agents_home
except (ModuleNotFoundError, ImportError):

    def get_pixel_agents_home() -> Path:
        """Return the Pixel Agents home directory (default: ~/.pixel-agents).

        Mirrors ``pixel_constants.get_pixel_agents_home()``."""
        val = os.environ.get("PIXEL_AGENTS_HOME", "").strip()
        return Path(val) if val else Path.home() / ".pixel-agents"

    def display_pixel_agents_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``pixel_constants.display_pixel_agents_home()``."""
        home = get_pixel_agents_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
