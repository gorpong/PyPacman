"""Base classes for game entities."""

from typing import Tuple, Optional, Iterator
from dataclasses import dataclass
from ..core.constants import Direction
from ..core.maze import Maze


@dataclass
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
        elif isinstance(other, tuple) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        return False
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate Manhattan distance to another position."""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def euclidean_distance_to(self, other: 'Position') -> float:
        """Calculate Euclidean distance to another position."""
        import math
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


class MovableEntity:
    """Base class for all moving entities in the game."""
    
    def __init__(self, start_x: int, start_y: int, speed: float = 8.0):
        """
        Initialize a movable entity.
        
        Args:
            start_x: Starting X position
            start_y: Starting Y position
            speed: Movement speed in cells per second
        """
        self.start_position = Position(start_x, start_y)
        self.position = Position(start_x, start_y)
        
        # Movement properties
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.speed = speed
        self.move_timer = 0.0
        self.moving = False
        
    def reset(self) -> None:
        """Reset entity to starting position."""
        self.position.x = self.start_position.x
        self.position.y = self.start_position.y
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.moving = False
        self.move_timer = 0.0
        
    def get_position(self) -> Tuple[int, int]:
        """Get current position as tuple."""
        return (self.position.x, self.position.y)
    
    def set_position(self, x: int, y: int) -> None:
        """Set the entity's position."""
        self.position.x = x
        self.position.y = y
        
    def can_move_to(self, maze: Maze, x: int, y: int) -> bool:
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
    
    def move(self, maze: Maze, direction: Tuple[int, int]) -> bool:
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
        new_x = self.position.x + dx
        new_y = self.position.y + dy
        
        # Handle maze wrapping (tunnels)
        if new_x < 0:
            new_x = maze.width - 1
        elif new_x >= maze.width:
            new_x = 0
            
        if self.can_move_to(maze, new_x, new_y):
            self.position.x = new_x
            self.position.y = new_y
            self.direction = direction
            self.moving = True
            return True
        
        self.moving = False
        return False
    
    def update_movement(self, delta_time: float, maze: Maze) -> bool:
        """
        Update movement based on speed and time.
        
        Args:
            delta_time: Time since last update
            maze: The maze object
            
        Returns:
            True if entity moved this frame
        """
        self.move_timer += delta_time
        move_delay = 1.0 / self.speed
        
        if self.move_timer >= move_delay:
            self.move_timer = 0.0
            return True
        
        return False
    
    def collides_with(self, other_x: int, other_y: int) -> bool:
        """Check if entity collides with given position."""
        return self.position.x == other_x and self.position.y == other_y
    
    def collides_with_entity(self, other: 'MovableEntity') -> bool:
        """Check if entity collides with another entity."""
        return self.position == other.position
