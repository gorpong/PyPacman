"""
ANSI color code definitions.

This module contains all terminal color escape sequences.
No dependencies on other internal modules.
"""
from __future__ import annotations


class Colors:
    """ANSI escape codes for terminal colors."""

    RESET: str = "\033[0m"

    BLACK: str = "\033[40m"

    WHITE: str = "\033[97m"
    YELLOW: str = "\033[93m"
    RED: str = "\033[91m"
    PINK: str = "\033[95m"
    CYAN: str = "\033[96m"
    BLUE: str = "\033[94m"
    GREEN: str = "\033[92m"

    ORANGE: str = "\033[38;5;208m"
