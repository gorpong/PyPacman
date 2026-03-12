"""Base classes for game entities."""
from __future__ import annotations

from ..core.types import Direction, DirectionType, MazeProtocol, Position


class MovableEntity:
    """Base class for all moving entities in the game."""

    def __init__(self, start_x: int, start_y: int, speed: float = 8.0) -> None:
        """
        Initialize a movable entity.

        Args:
            start_x: Starting X position
            start_y: Starting Y position
            speed: Movement speed in cells per second
        """
        self.start_position: Position = Position(start_x, start_y)
        self.position: Position = Position(start_x, start_y)

        self.direction: DirectionType = Direction.NONE
        self.next_direction: DirectionType = Direction.NONE
        self.speed: float = speed
        self.move_timer: float = 0.0
        self.moving: bool = False

    def reset(self) -> None:
        """Reset entity to starting position."""
        self.position = Position(self.start_position.x, self.start_position.y)
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.moving = False
        self.move_timer = 0.0

    def get_position(self) -> Position:
        """Get current position."""
        return self.position

    def set_position(self, x: int, y: int) -> None:
        """Set the entity's position."""
        self.position = Position(x, y)

    def can_move_to(self, maze: MazeProtocol, x: int, y: int) -> bool:
        """
        Check if entity can move to the given position.

        Args:
            maze: The maze object
            x: Target X position
            y: Target Y position

        Returns:
            True if the position is walkable
        """
        return maze.is_walkable(x, y)

    def move(self, maze: MazeProtocol, direction: DirectionType) -> bool:
        """
        Attempt to move in the given direction.

        Args:
            maze: The maze object
            direction: Direction tuple (dx, dy)

        Returns:
            True if movement was successful
        """
        if direction == Direction.NONE:
            return False

        dx, dy = direction
        new_x: int = self.position.x + dx
        new_y: int = self.position.y + dy

        if new_x < 0:
            new_x = maze.width - 1
        elif new_x >= maze.width:
            new_x = 0

        if self.can_move_to(maze, new_x, new_y):
            self.position = Position(new_x, new_y)
            self.direction = direction
            self.moving = True
            return True

        self.moving = False
        return False

    def update_movement(self, delta_time: float, maze: MazeProtocol) -> bool:
        """
        Update movement based on speed and time.

        Args:
            delta_time: Time since last update
            maze: The maze object

        Returns:
            True if entity moved this frame
        """
        self.move_timer += delta_time
        move_delay: float = 1.0 / self.speed

        if self.move_timer >= move_delay:
            self.move_timer = 0.0
            return True

        return False

    def collides_with(self, other_x: int, other_y: int) -> bool:
        """Check if entity collides with given position."""
        return self.position.x == other_x and self.position.y == other_y

    def collides_with_entity(self, other: MovableEntity) -> bool:
        """Check if entity collides with another entity."""
        return self.position == other.position
