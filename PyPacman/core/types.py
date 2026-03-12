"""
Shared type definitions, protocols, and lightweight structural types.

This module has NO internal dependencies and serves as the foundation
for type contracts across the codebase.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Iterator, Protocol


DirectionType = tuple[int, int]


class Direction:
    """Direction constants as coordinate deltas."""
    UP: DirectionType = (0, -1)
    DOWN: DirectionType = (0, 1)
    LEFT: DirectionType = (-1, 0)
    RIGHT: DirectionType = (1, 0)
    NONE: DirectionType = (0, 0)

    @classmethod
    def opposite(cls, direction: DirectionType) -> DirectionType:
        """Return the opposite direction."""
        return (-direction[0], -direction[1])

    @classmethod
    def all_directions(cls) -> list[DirectionType]:
        """Return all four cardinal directions."""
        return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]


@dataclass(slots=True)
class Position:
    """Represents a 2D position in the game world."""
    x: int
    y: int

    def __iter__(self) -> Iterator[int]:
        """Allow unpacking as tuple."""
        return iter((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        """Compare positions."""
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        if isinstance(other, tuple) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        return False

    def __hash__(self) -> int:
        """Make Position hashable for use in sets and dicts."""
        return hash((self.x, self.y))

    def __add__(self, other: DirectionType | Position) -> Position:
        """Add a direction or position to this position."""
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        return Position(self.x + other[0], self.y + other[1])

    def distance_to(self, other: Position) -> float:
        """Calculate Manhattan distance to another position."""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean_distance_to(self, other: Position) -> float:
        """Calculate Euclidean distance to another position."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def as_tuple(self) -> tuple[int, int]:
        """Return position as a tuple."""
        return (self.x, self.y)


class GameMode(Enum):
    """
    Enumeration of game modes/phases.

    This represents what screen/phase the game is currently showing,
    not the internal game state (lives, score, etc.).
    """
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    HIGH_SCORE_ENTRY = "high_score_entry"
    QUIT_CONFIRM = "quit_confirm"
    QUIT = "quit"


class CellType(IntEnum):
    """Types of cells in the maze grid."""
    WALL = 0
    EMPTY = 1
    DOT = 2
    POWER_PELLET = 3
    GHOST_HOUSE = 4
    GHOST_DOOR = 5


class MazeProtocol(Protocol):
    """
    Interface for maze-like objects that entities navigate.

    This protocol defines the contract that any maze implementation
    must fulfill for entities to navigate it.
    """
    width: int
    height: int
    ghost_house_cells: set[tuple[int, int]]

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within maze bounds."""
        ...

    def is_wall(self, x: int, y: int) -> bool:
        """Check if position is a wall."""
        ...

    def is_walkable(self, x: int, y: int, is_ghost: bool = False) -> bool:
        """Check if position can be walked on."""
        ...

    def is_walkable_for_pacman(self, x: int, y: int) -> bool:
        """Check if Pac-Man can walk on this position."""
        ...

    def is_walkable_for_ghost(self, x: int, y: int) -> bool:
        """Check if a ghost can walk on this position."""
        ...

    def is_ghost_house(self, x: int, y: int) -> bool:
        """Check if position is inside the ghost house."""
        ...

    def is_ghost_door(self, x: int, y: int) -> bool:
        """Check if position is the ghost house door."""
        ...

    def get_ghost_door_position(self) -> Position | None:
        """Get the position of the ghost house door."""
        ...

    def get_ghost_spawn_positions(self) -> list[Position]:
        """Get spawn positions for ghosts."""
        ...

    def get_pacman_spawn(self) -> Position:
        """Get the Pac-Man spawn position."""
        ...


class PacManProtocol(Protocol):
    """
    Interface for Pac-Man that other entities interact with.

    This allows ghosts to target Pac-Man without importing
    the concrete PacMan class.
    """
    position: Position
    direction: DirectionType

    def get_position(self) -> Position:
        """Get current position."""
        ...


class GhostProtocol(Protocol):
    """
    Interface for ghosts that the game engine interacts with.
    """
    position: Position
    name: str

    def get_position(self) -> Position:
        """Get current position."""
        ...

    def is_vulnerable(self) -> bool:
        """Check if ghost is vulnerable to Pac-Man."""
        ...

    def is_dangerous(self) -> bool:
        """Check if ghost is dangerous to Pac-Man."""
        ...

    def can_be_eaten(self) -> bool:
        """Check if ghost can be eaten right now."""
        ...

    def get_sprite(self) -> str:
        """Get the display sprite for this ghost."""
        ...

    def get_color(self) -> str:
        """Get the display color for this ghost."""
        ...
