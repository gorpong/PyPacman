"""Pac-Man character implementation."""
from __future__ import annotations

from ..core.sprites import Sprites
from ..core.types import Direction, DirectionType, MazeProtocol, Position
from .base import MovableEntity


class PacMan(MovableEntity):
    """The player-controlled Pac-Man character."""

    def __init__(self, start_x: int, start_y: int) -> None:
        """Initialize Pac-Man at the given position."""
        super().__init__(start_x, start_y, speed=8.0)

        self.direction: DirectionType = Direction.RIGHT
        self.next_direction: DirectionType = Direction.RIGHT

        self.animation_frame: int = 0
        self.animation_timer: float = 0.0
        self.mouth_open: bool = True

    def reset(self) -> None:
        """Reset Pac-Man to starting position."""
        super().reset()
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.animation_frame = 0
        self.mouth_open = True

    def set_direction(self, direction: DirectionType) -> None:
        """
        Set the next direction for Pac-Man to move.

        Args:
            direction: Direction tuple (dx, dy)
        """
        if direction != Direction.NONE:
            self.next_direction = direction

    def update(self, delta_time: float, maze: MazeProtocol) -> None:
        """
        Update Pac-Man's position and animation.

        Args:
            delta_time: Time since last update in seconds
            maze: The maze object
        """
        self.animation_timer += delta_time
        if self.animation_timer >= 0.1:
            self.mouth_open = not self.mouth_open
            self.animation_timer = 0.0

        if self.update_movement(delta_time, maze):
            if self.next_direction != self.direction:
                dx, dy = self.next_direction
                new_x = self.position.x + dx
                new_y = self.position.y + dy

                if self.can_move_to(maze, new_x, new_y):
                    self.direction = self.next_direction

            self.move(maze, self.direction)

    def get_sprite(self) -> str:
        """
        Get the current sprite character for Pac-Man.

        Returns:
            The character to display
        """
        if not self.mouth_open:
            return Sprites.PACMAN_CLOSED

        if self.direction == Direction.RIGHT:
            return Sprites.PACMAN_RIGHT
        elif self.direction == Direction.LEFT:
            return Sprites.PACMAN_LEFT
        elif self.direction == Direction.UP:
            return Sprites.PACMAN_UP
        elif self.direction == Direction.DOWN:
            return Sprites.PACMAN_DOWN
        else:
            return Sprites.PACMAN_CLOSED
