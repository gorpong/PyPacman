"""
Pac-Man character class.
Handles player movement, animation, and collision with dots/pellets.
"""

from typing import Tuple
from .constants import Direction, Sprites


class PacMan:
    """The player-controlled Pac-Man character."""
    
    def __init__(self, start_x: int, start_y: int):
        """
        Initialize Pac-Man at the given position.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
        """
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        
        # Movement
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.moving = False
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.mouth_open = True
        
        # Speed (cells per second)
        self.speed = 8.0
        self.move_timer = 0.0
        
    def reset(self):
        """Reset Pac-Man to starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.moving = False
        self.animation_frame = 0
        self.mouth_open = True
        
    def set_direction(self, direction: Tuple[int, int]):
        """
        Set the next direction for Pac-Man to move.
        
        Args:
            direction: Direction tuple (dx, dy)
        """
        if direction != Direction.NONE:
            self.next_direction = direction
            
    def can_move(self, maze, dx: int, dy: int) -> bool:
        """
        Check if Pac-Man can move in the given direction.
        
        Args:
            maze: The maze object
            dx: X direction
            dy: Y direction
            
        Returns:
            True if the move is valid
        """
        new_x = self.x + dx
        new_y = self.y + dy
        return maze.is_walkable(new_x, new_y)
        
    def update(self, delta_time: float, maze):
        """
        Update Pac-Man's position and animation.
        
        Args:
            delta_time: Time since last update in seconds
            maze: The maze object
        """
        # Update animation
        self.animation_timer += delta_time
        if self.animation_timer >= 0.1:  # Toggle mouth every 0.1 seconds
            self.mouth_open = not self.mouth_open
            self.animation_timer = 0.0
            
        # Update movement
        self.move_timer += delta_time
        move_delay = 1.0 / self.speed
        
        if self.move_timer >= move_delay:
            self.move_timer = 0.0
            
            # Try to change direction if requested
            if self.next_direction != self.direction:
                dx, dy = self.next_direction
                if self.can_move(maze, dx, dy):
                    self.direction = self.next_direction
                    
            # Move in current direction
            dx, dy = self.direction
            if self.can_move(maze, dx, dy):
                self.x += dx
                self.y += dy
                self.moving = True
                
                # Wrap around edges if needed (tunnel)
                if self.x < 0:
                    self.x = maze.width - 1
                elif self.x >= maze.width:
                    self.x = 0
            else:
                self.moving = False
                
    def get_sprite(self) -> str:
        """
        Get the current sprite character for Pac-Man.
        
        Returns:
            The character to display
        """
        if not self.mouth_open:
            return Sprites.PACMAN_CLOSED
            
        # Return direction-based sprite
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
            
    def get_position(self) -> Tuple[int, int]:
        """Get current position."""
        return (self.x, self.y)
