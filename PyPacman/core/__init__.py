"""
Core game modules.

This package provides the foundational types, configuration, and
game logic components.
"""
from __future__ import annotations

from .colors import Colors
from .config import (
    FRAME_TIME,
    GAME_HEIGHT,
    GAME_WIDTH,
    GHOST_VULNERABLE_DURATION,
    INITIAL_LIVES,
    MIN_TERMINAL_HEIGHT,
    MIN_TERMINAL_WIDTH,
    PLAYABLE_HEIGHT,
    PLAYABLE_WIDTH,
    POWER_PELLET_DURATION,
    SCORE_DOT,
    SCORE_EXTRA_LIFE,
    SCORE_GHOST_BASE,
    SCORE_GHOST_MULTIPLIER,
    SCORE_POWER_PELLET,
    TARGET_FPS,
)
from .game_engine import GameEngine
from .game_state import GameState
from .maze import Maze
from .scoring import ScoringSystem
from .sprites import BorderChars, Sprites
from .types import (
    CellType,
    Direction,
    DirectionType,
    GameMode,
    GhostProtocol,
    MazeProtocol,
    PacManProtocol,
    Position,
)

__all__ = [
    # Types
    "Position",
    "Direction",
    "DirectionType",
    "GameMode",
    "CellType",
    # Protocols
    "MazeProtocol",
    "PacManProtocol",
    "GhostProtocol",
    # Config
    "GAME_WIDTH",
    "GAME_HEIGHT",
    "MIN_TERMINAL_WIDTH",
    "MIN_TERMINAL_HEIGHT",
    "PLAYABLE_WIDTH",
    "PLAYABLE_HEIGHT",
    "TARGET_FPS",
    "FRAME_TIME",
    "INITIAL_LIVES",
    "POWER_PELLET_DURATION",
    "GHOST_VULNERABLE_DURATION",
    "SCORE_DOT",
    "SCORE_POWER_PELLET",
    "SCORE_GHOST_BASE",
    "SCORE_GHOST_MULTIPLIER",
    "SCORE_EXTRA_LIFE",
    # Visual
    "Sprites",
    "BorderChars",
    "Colors",
    # Classes
    "GameEngine",
    "Maze",
    "GameState",
    "ScoringSystem",
]
