"""Game entities module - characters and game objects."""
from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "MovableEntity",
    "Position",
    "PacMan",
    "Ghost",
    "Blinky",
    "Pinky",
    "Inky",
    "Clyde",
    "GhostMode",
    "GhostState",
    "GhostManager",
]

_EXPORTS: dict[str, tuple[str, str]] = {
    "MovableEntity": (".base", "MovableEntity"),
    "Position": ("..core.types", "Position"),
    "PacMan": (".pacman", "PacMan"),
    "Ghost": (".ghost", "Ghost"),
    "Blinky": (".ghost", "Blinky"),
    "Pinky": (".ghost", "Pinky"),
    "Inky": (".ghost", "Inky"),
    "Clyde": (".ghost", "Clyde"),
    "GhostMode": (".ghost", "GhostMode"),
    "GhostState": (".ghost", "GhostState"),
    "GhostManager": (".ghost_manager", "GhostManager"),
}


def __getattr__(name: str) -> Any:
    """Resolve entity exports lazily."""
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
