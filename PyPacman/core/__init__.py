"""
Core game modules.

This package exposes a convenient public API while keeping imports lazy to
avoid widening the runtime import graph during package initialization.
"""
from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "Position",
    "Direction",
    "DirectionType",
    "GameMode",
    "CellType",
    "MazeProtocol",
    "PacManProtocol",
    "GhostProtocol",
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
    "Sprites",
    "BorderChars",
    "Colors",
    "GameEngine",
    "Maze",
    "GameState",
    "ScoringSystem",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "Position": (".types", "Position"),
    "Direction": (".types", "Direction"),
    "DirectionType": (".types", "DirectionType"),
    "GameMode": (".types", "GameMode"),
    "CellType": (".types", "CellType"),
    "MazeProtocol": (".types", "MazeProtocol"),
    "PacManProtocol": (".types", "PacManProtocol"),
    "GhostProtocol": (".types", "GhostProtocol"),
    "GAME_WIDTH": (".config", "GAME_WIDTH"),
    "GAME_HEIGHT": (".config", "GAME_HEIGHT"),
    "MIN_TERMINAL_WIDTH": (".config", "MIN_TERMINAL_WIDTH"),
    "MIN_TERMINAL_HEIGHT": (".config", "MIN_TERMINAL_HEIGHT"),
    "PLAYABLE_WIDTH": (".config", "PLAYABLE_WIDTH"),
    "PLAYABLE_HEIGHT": (".config", "PLAYABLE_HEIGHT"),
    "TARGET_FPS": (".config", "TARGET_FPS"),
    "FRAME_TIME": (".config", "FRAME_TIME"),
    "INITIAL_LIVES": (".config", "INITIAL_LIVES"),
    "POWER_PELLET_DURATION": (".config", "POWER_PELLET_DURATION"),
    "GHOST_VULNERABLE_DURATION": (".config", "GHOST_VULNERABLE_DURATION"),
    "SCORE_DOT": (".config", "SCORE_DOT"),
    "SCORE_POWER_PELLET": (".config", "SCORE_POWER_PELLET"),
    "SCORE_GHOST_BASE": (".config", "SCORE_GHOST_BASE"),
    "SCORE_GHOST_MULTIPLIER": (".config", "SCORE_GHOST_MULTIPLIER"),
    "SCORE_EXTRA_LIFE": (".config", "SCORE_EXTRA_LIFE"),
    "Sprites": (".sprites", "Sprites"),
    "BorderChars": (".sprites", "BorderChars"),
    "Colors": (".colors", "Colors"),
    "GameEngine": (".game_engine", "GameEngine"),
    "Maze": (".maze", "Maze"),
    "GameState": (".game_state", "GameState"),
    "ScoringSystem": (".scoring", "ScoringSystem"),
}


def __getattr__(name: str) -> Any:
    """Resolve public exports lazily to avoid eager import chains."""
    try:
        module_name, attr_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Expose lazy exports to introspection tools."""
    return sorted(list(globals().keys()) + __all__)
