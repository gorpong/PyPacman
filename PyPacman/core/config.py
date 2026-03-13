"""
Game configuration constants.

This module contains all tunable game parameters: dimensions, timing,
difficulty settings, etc. No dependencies on other internal modules.
"""
from __future__ import annotations

# === Display Dimensions ===

GAME_WIDTH: int = 80
GAME_HEIGHT: int = 24
MIN_TERMINAL_WIDTH: int = 80
MIN_TERMINAL_HEIGHT: int = 24

PLAYABLE_WIDTH: int = GAME_WIDTH - 2
PLAYABLE_HEIGHT: int = GAME_HEIGHT - 2

# === Timing ===

TARGET_FPS: int = 10
FRAME_TIME: float = 1.0 / TARGET_FPS

# === Game Settings ===

INITIAL_LIVES: int = 3
POWER_PELLET_DURATION: float = 10.0
GHOST_VULNERABLE_DURATION: float = 8.0

# === Scoring ===

SCORE_DOT: int = 10
SCORE_POWER_PELLET: int = 50
SCORE_GHOST_BASE: int = 200
SCORE_GHOST_MULTIPLIER: int = 2
SCORE_GHOST_MAX: int = 1600
SCORE_EXTRA_LIFE: int = 10000
