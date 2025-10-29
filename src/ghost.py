"""
Ghost AI system for ASCII Pac-Man.
Implements the four ghosts with different AI behaviors.
"""

from typing import Tuple, Optional, List
from enum import Enum
from .constants import Direction, Sprites, Colors
import random


class GhostMode(Enum):
    """Ghost behavior modes."""
    SCATTER = "scatter"
    CHASE = "chase"
    VULNERABLE = "vulnerable"
    EATEN = "eaten"


class GhostState(Enum):
    """Ghost current state."""
    IN_HOUSE = "in_house"
    LEAVING_HOUSE = "leaving_house"
    ACTIVE = "active"
    RETURNING = "returning"


class Ghost:
    """Base ghost class with common behaviors."""
    
    def __init__(self, start_x: int, start_y: int, color: str, name: str):
        """
        Initialize a ghost.
        
        Args:
            start_x: Starting X position
            start_y: Starting Y position
            color: Display color for the ghost
            name: Ghost name (for debugging)
        """
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        
        self.color = color
        self.name = name
        
        # Movement
        self.direction = Direction.UP
        self.next_direction = Direction.UP
        self.speed = 7.0  # Cells per second (slightly slower than Pac-Man)
        self.move_timer = 0.0
        
        # AI state
        self.mode = GhostMode.SCATTER
        self.state = GhostState.IN_HOUSE
        self.target_x = start_x
        self.target_y = start_y
        
        # Timers
        self.mode_timer = 0.0
        self.vulnerable_timer = 0.0
        self.release_timer = 0.0
        
        # Behavior parameters
        self.scatter_target = (1, 1)  # Top-left corner by default
        self.release_delay = 0.0  # Time before leaving house
        
    def reset(self):
        """Reset ghost to starting position and state."""
        self.x = self.start_x
        self.y = self.start_y
        self.direction = Direction.UP
        self.state = GhostState.IN_HOUSE
        self.mode = GhostMode.SCATTER
        self.mode_timer = 0.0
        self.vulnerable_timer = 0.0
        self.release_timer = 0.0
        
    def update(self, delta_time: float, maze, pacman):
        """
        Update ghost AI and movement.
        
        Args:
            delta_time: Time since last update
            maze: The maze object
            pacman: Pac-Man character object
        """
        # Update timers
        self.mode_timer += delta_time
        if self.vulnerable_timer > 0:
            self.vulnerable_timer -= delta_time
            if self.vulnerable_timer <= 0:
                self.mode = GhostMode.SCATTER
        
        if self.state == GhostState.IN_HOUSE:
            self.release_timer += delta_time
            if self.release_timer >= self.release_delay:
                self.state = GhostState.LEAVING_HOUSE
        
        # Update AI behavior
        self._update_ai(maze, pacman)
        
        # Update movement
        self._update_movement(delta_time, maze)
    
    def _update_ai(self, maze, pacman):
        """Update AI target based on current mode and state."""
        if self.state == GhostState.IN_HOUSE:
            return
        elif self.state == GhostState.LEAVING_HOUSE:
            # Head to house exit
            self.target_x = 37  # Center of maze (approximately)
            self.target_y = 10
            if abs(self.x - self.target_x) <= 1 and abs(self.y - self.target_y) <= 1:
                self.state = GhostState.ACTIVE
        elif self.state == GhostState.ACTIVE:
            if self.mode == GhostMode.SCATTER:
                self.target_x, self.target_y = self.scatter_target
            elif self.mode == GhostMode.CHASE:
                self.target_x, self.target_y = self._get_chase_target(pacman)
            elif self.mode == GhostMode.VULNERABLE:
                # Random movement when vulnerable
                self._choose_random_target(maze)
        elif self.state == GhostState.RETURNING:
            self.target_x = self.start_x
            self.target_y = self.start_y
            if abs(self.x - self.start_x) <= 1 and abs(self.y - self.start_y) <= 1:
                self.state = GhostState.IN_HOUSE
                self.mode = GhostMode.SCATTER
    
    def _get_chase_target(self, pacman) -> Tuple[int, int]:
        """Get the target position for chase mode. Override in subclasses."""
        return pacman.get_position()
    
    def _choose_random_target(self, maze):
        """Choose a random direction when vulnerable."""
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        random.shuffle(directions)
        
        for direction in directions:
            dx, dy = direction
            new_x, new_y = self.x + dx, self.y + dy
            if maze.is_walkable(new_x, new_y):
                self.target_x = new_x
                self.target_y = new_y
                break
    
    def _update_movement(self, delta_time: float, maze):
        """Update ghost movement towards target."""
        self.move_timer += delta_time
        move_delay = 1.0 / self.speed
        
        if self.move_timer >= move_delay:
            self.move_timer = 0.0
            
            # Calculate best direction to target
            best_direction = self._get_best_direction(maze)
            
            if best_direction != Direction.NONE:
                dx, dy = best_direction
                new_x = self.x + dx
                new_y = self.y + dy
                
                if maze.is_walkable(new_x, new_y):
                    self.x = new_x
                    self.y = new_y
                    self.direction = best_direction
                    
                    # Handle maze edge wrapping
                    if self.x < 0:
                        self.x = maze.width - 1
                    elif self.x >= maze.width:
                        self.x = 0
    
    def _get_best_direction(self, maze) -> Tuple[int, int]:
        """Calculate the best direction to move towards target."""
        if self.state == GhostState.IN_HOUSE:
            return Direction.NONE
            
        current_pos = (self.x, self.y)
        target_pos = (self.target_x, self.target_y)
        
        # Don't reverse direction unless necessary
        reverse_direction = (-self.direction[0], -self.direction[1])
        
        possible_directions = []
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            if direction == reverse_direction:
                continue
                
            dx, dy = direction
            new_x, new_y = self.x + dx, self.y + dy
            
            if maze.is_walkable(new_x, new_y):
                # Calculate distance to target
                distance = abs(new_x - target_pos[0]) + abs(new_y - target_pos[1])
                possible_directions.append((direction, distance))
        
        if not possible_directions:
            # Can only reverse
            return reverse_direction
        
        # Choose direction with shortest distance to target
        possible_directions.sort(key=lambda x: x[1])
        return possible_directions[0][0]
    
    def set_mode(self, mode: GhostMode, duration: float = 0.0):
        """Set ghost mode and optional timer."""
        self.mode = mode
        self.mode_timer = 0.0
        
        if mode == GhostMode.VULNERABLE:
            self.vulnerable_timer = duration
    
    def make_vulnerable(self, duration: float):
        """Make ghost vulnerable (after power pellet)."""
        if self.state == GhostState.ACTIVE and self.mode != GhostMode.EATEN:
            self.set_mode(GhostMode.VULNERABLE, duration)
            # Reverse direction when becoming vulnerable
            self.direction = (-self.direction[0], -self.direction[1])
    
    def get_eaten(self):
        """Handle ghost being eaten by Pac-Man."""
        self.mode = GhostMode.EATEN
        self.state = GhostState.RETURNING
    
    def is_vulnerable(self) -> bool:
        """Check if ghost is vulnerable to Pac-Man."""
        return self.mode == GhostMode.VULNERABLE and self.vulnerable_timer > 0
    
    def is_dangerous(self) -> bool:
        """Check if ghost is dangerous to Pac-Man."""
        return (self.state == GhostState.ACTIVE and 
                self.mode in [GhostMode.SCATTER, GhostMode.CHASE])
    
    def get_sprite(self) -> str:
        """Get the sprite character for this ghost."""
        if self.mode == GhostMode.VULNERABLE:
            return Sprites.VULNERABLE_GHOST
        elif self.mode == GhostMode.EATEN:
            return " "  # Invisible when returning
        else:
            return Sprites.GHOST
    
    def get_color(self) -> str:
        """Get the color for this ghost."""
        if self.mode == GhostMode.VULNERABLE:
            return Colors.BLUE
        elif self.mode == GhostMode.EATEN:
            return Colors.WHITE
        else:
            return self.color
    
    def get_position(self) -> Tuple[int, int]:
        """Get current position."""
        return (self.x, self.y)
    
    def collides_with(self, other_x: int, other_y: int) -> bool:
        """Check if ghost collides with given position."""
        return self.x == other_x and self.y == other_y


class Blinky(Ghost):
    """Red ghost - aggressive chaser."""
    
    def __init__(self, start_x: int, start_y: int):
        super().__init__(start_x, start_y, Colors.RED, "Blinky")
        self.scatter_target = (70, 1)  # Top-right corner
        self.release_delay = 0.0  # First to leave house
    
    def _get_chase_target(self, pacman) -> Tuple[int, int]:
        """Blinky directly targets Pac-Man."""
        return pacman.get_position()


class Pinky(Ghost):
    """Pink ghost - ambusher."""
    
    def __init__(self, start_x: int, start_y: int):
        super().__init__(start_x, start_y, Colors.PINK, "Pinky")
        self.scatter_target = (1, 1)  # Top-left corner
        self.release_delay = 2.0  # Second to leave
    
    def _get_chase_target(self, pacman) -> Tuple[int, int]:
        """Pinky targets 4 spaces ahead of Pac-Man."""
        px, py = pacman.get_position()
        dx, dy = pacman.direction
        
        # Target 4 spaces ahead
        target_x = px + dx * 4
        target_y = py + dy * 4
        
        return (target_x, target_y)


class Inky(Ghost):
    """Cyan ghost - patrol/ambush hybrid."""
    
    def __init__(self, start_x: int, start_y: int):
        super().__init__(start_x, start_y, Colors.CYAN, "Inky")
        self.scatter_target = (70, 18)  # Bottom-right corner
        self.release_delay = 5.0  # Third to leave
    
    def _get_chase_target(self, pacman) -> Tuple[int, int]:
        """Inky uses complex targeting based on Pac-Man and Blinky."""
        px, py = pacman.get_position()
        dx, dy = pacman.direction
        
        # Get point 2 spaces ahead of Pac-Man
        intermediate_x = px + dx * 2
        intermediate_y = py + dy * 2
        
        # For simplicity, just target ahead of Pac-Man
        # (Full Inky logic requires Blinky's position)
        return (intermediate_x, intermediate_y)


class Clyde(Ghost):
    """Orange ghost - patrol with distance-based behavior."""
    
    def __init__(self, start_x: int, start_y: int):
        super().__init__(start_x, start_y, Colors.ORANGE, "Clyde")
        self.scatter_target = (1, 18)  # Bottom-left corner  
        self.release_delay = 8.0  # Last to leave
    
    def _get_chase_target(self, pacman) -> Tuple[int, int]:
        """Clyde targets Pac-Man when far, but scatters when close."""
        px, py = pacman.get_position()
        distance = abs(self.x - px) + abs(self.y - py)
        
        if distance > 8:
            # Far away - chase Pac-Man
            return (px, py)
        else:
            # Close - head to scatter corner
            return self.scatter_target
