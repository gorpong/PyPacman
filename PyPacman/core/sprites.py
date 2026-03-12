"""
ASCII sprite and border character definitions.

This module contains all visual character constants used for rendering.
No dependencies on other internal modules.
"""
from __future__ import annotations


class Sprites:
    """ASCII characters for game elements."""

    WALL: str = "█"
    DOT: str = "·"
    POWER_PELLET: str = "●"
    EMPTY: str = " "
    GHOST_HOUSE_FLOOR: str = " "
    GHOST_DOOR: str = "─"

    PACMAN_RIGHT: str = ">"
    PACMAN_LEFT: str = "<"
    PACMAN_UP: str = "^"
    PACMAN_DOWN: str = "v"
    PACMAN_CLOSED: str = "O"

    GHOST: str = "⌂"
    VULNERABLE_GHOST: str = "▒"
    EATEN_GHOST: str = "×"


class BorderChars:
    """Box-drawing characters for UI borders."""

    HORIZONTAL: str = "═"
    VERTICAL: str = "║"
    TOP_LEFT: str = "╔"
    TOP_RIGHT: str = "╗"
    BOTTOM_LEFT: str = "╚"
    BOTTOM_RIGHT: str = "╝"

    HORIZONTAL_SINGLE: str = "─"
    VERTICAL_SINGLE: str = "│"
    TOP_LEFT_SINGLE: str = "┌"
    TOP_RIGHT_SINGLE: str = "┐"
    BOTTOM_LEFT_SINGLE: str = "└"
    BOTTOM_RIGHT_SINGLE: str = "┘"
