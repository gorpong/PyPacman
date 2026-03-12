"""Data module for level layouts and game data."""
from __future__ import annotations

from .levels import (
    LEVEL_ORDER,
    LEVELS,
    find_ghost_house_center,
    find_spawn_point,
    get_level,
    get_level_count,
)

__all__ = [
    "LEVELS",
    "LEVEL_ORDER",
    "get_level",
    "get_level_count",
    "find_spawn_point",
    "find_ghost_house_center",
]
