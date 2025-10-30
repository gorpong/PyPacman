"""Ghost AI system implementation."""

from typing import Tuple, Optional
from enum import Enum
from .base import MovableEntity, Position
from .pacman import PacMan
from ..core.constants import Direction, Sprites, Colors
from ..core.maze import Maze
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


class Ghost(MovableEntity):
    """Base ghost class with common behaviors."""
    
    def __init__(self, start_x: int, start_y: int, color: str, name: str) -> None:
        """Initialize a ghost."""
        super().__init__(start_x, start_y, speed=7.0)  # Slightly slower than Pac-Man
        
        self.color = color
        self.name = name
        
        # AI state
        self.mode = GhostMode.SCATTER
        self.state = GhostState.IN_HOUSE
        self.target = Position(start_x, start_y)
        
        # Timers
        self.mode_timer = 0.0
        self.vulnerable_timer = 0.0
        self.release_timer = 0.0
        
        # Behavior parameters
        self.scatter_target = Position(1, 1)  # Top-left corner by default
        self.release_delay = 0.0  # Time before leaving house
        
    def reset(self) -> None:
        """Reset ghost to starting position and state."""
        super().reset()
        self.direction = Direction.UP
        self.state = GhostState.IN_HOUSE
        self.mode = GhostMode.SCATTER
        self.mode_timer = 0.0
        self.vulnerable_timer = 0.0
        self.release_timer = 0.0
        
    def update(self, delta_time: float, maze: Maze, pacman: PacMan) -> None:
        """Update ghost AI and movement."""
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
                # Reset mode to scatter when leaving house after being eaten
                if self.mode == GhostMode.EATEN:
                    self.mode = GhostMode.SCATTER
        
        # Update AI behavior
        self._update_ai(maze, pacman)
        
        # Update movement
        if self.update_movement(delta_time, maze):
            self._perform_movement(maze)
    
    def _update_ai(self, maze: Maze, pacman: PacMan) -> None:
        """Update AI target based on current mode and state."""
        if self.state == GhostState.IN_HOUSE:
            return
        elif self.state == GhostState.LEAVING_HOUSE:
            # Calculate maze center dynamically
            maze_center_x = maze.width // 2
            maze_center_y = maze.height // 2
            
            # Find nearest walkable position to center
            self.target.x = maze_center_x
            self.target.y = maze_center_y
            
            # Adjust target to be above ghost house
            for y in range(maze_center_y - 5, maze_center_y + 5):
                if maze.is_walkable(maze_center_x, y) and not maze.is_ghost_house(maze_center_x, y):
                    self.target.y = y
                    break
            
            # Check if reached exit
            if self.position.distance_to(self.target) <= 2:
                self.state = GhostState.ACTIVE
                
        elif self.state == GhostState.ACTIVE:
            if self.mode == GhostMode.SCATTER:
                self.target = self.scatter_target
            elif self.mode == GhostMode.CHASE:
                self.target = Position(*self._get_chase_target(pacman))
            elif self.mode == GhostMode.VULNERABLE:
                # Random movement when vulnerable
                self._choose_random_target(maze)
                
        elif self.state == GhostState.RETURNING:
            self.target = self.start_position
            if self.position.distance_to(self.start_position) <= 1:
                self.state = GhostState.IN_HOUSE
                self.mode = GhostMode.SCATTER
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Get the target position for chase mode. Override in subclasses."""
        return pacman.get_position()
    
    def _choose_random_target(self, maze: Maze) -> None:
        """Choose a random direction when vulnerable."""
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        random.shuffle(directions)
        
        for direction in directions:
            dx, dy = direction
            new_x = self.position.x + dx
            new_y = self.position.y + dy
            if maze.is_walkable(new_x, new_y):
                self.target = Position(new_x, new_y)
                break
    
    def _perform_movement(self, maze: Maze) -> None:
        """Execute movement towards target."""
        best_direction = self._get_best_direction(maze)
        
        if best_direction != Direction.NONE:
            self.move(maze, best_direction)
    
    def _get_best_direction(self, maze: Maze) -> Tuple[int, int]:
        """Calculate the best direction to move towards target."""
        if self.state == GhostState.IN_HOUSE:
            return Direction.NONE
        
        # Don't reverse direction unless necessary
        reverse_direction = (-self.direction[0], -self.direction[1])
        
        possible_directions = []
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            if direction == reverse_direction and self.mode != GhostMode.VULNERABLE:
                continue
                
            dx, dy = direction
            new_x = self.position.x + dx
            new_y = self.position.y + dy
            
            if maze.is_walkable(new_x, new_y):
                # Calculate distance to target
                new_pos = Position(new_x, new_y)
                distance = new_pos.distance_to(self.target)
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
        self.state = GhostState.IN_HOUSE
        # Teleport back to starting position
        self.position.x = self.start_position.x
        self.position.y = self.start_position.y
        self.direction = Direction.NONE
        # Reset release timer so it comes back out
        self.release_timer = 0.0
    
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


class Blinky(Ghost):
    """Red ghost - aggressive chaser."""
    
    def __init__(self, start_x: int, start_y: int):
        super().__init__(start_x, start_y, Colors.RED, "Blinky")
        self.scatter_target = Position(70, 1)  # Top-right corner
        self.release_delay = 0.0  # First to leave house
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Blinky directly targets Pac-Man."""
        return pacman.get_position()


class Pinky(Ghost):
    """Pink ghost - ambusher."""
    
    def __init__(self, start_x: int, start_y: int):
        super().__init__(start_x, start_y, Colors.PINK, "Pinky")
        self.scatter_target = Position(1, 1)  # Top-left corner
        self.release_delay = 2.0  # Second to leave
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Pinky targets 4 spaces ahead of Pac-Man."""
        px, py = pacman.get_position()
        dx, dy = pacman.direction
        
        # Target 4 spaces ahead
        target_x = px + dx * 4
        target_y = py + dy * 4
        
        return (target_x, target_y)


class Inky(Ghost):
    """Cyan ghost - patrol/ambush hybrid."""
    
    def __init__(self, start_x: int, start_y: int, blinky: Optional['Blinky'] = None):
        super().__init__(start_x, start_y, Colors.CYAN, "Inky")
        self.scatter_target = Position(70, 18)  # Bottom-right corner
        self.release_delay = 5.0  # Third to leave
        self.blinky = blinky  # Reference to Blinky for targeting
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Inky uses complex targeting based on Pac-Man and Blinky."""
        px, py = pacman.get_position()
        dx, dy = pacman.direction
        
        # Get point 2 spaces ahead of Pac-Man
        intermediate_x = px + dx * 2
        intermediate_y = py + dy * 2
        
        # If we have a reference to Blinky, use full logic
        if self.blinky:
            bx, by = self.blinky.get_position()
            # Vector from Blinky to intermediate point, doubled
            target_x = intermediate_x + (intermediate_x - bx)
            target_y = intermediate_y + (intermediate_y - by)
            return (target_x, target_y)
        
        # Fallback: just target ahead of Pac-Man
        return (intermediate_x, intermediate_y)


class Clyde(Ghost):
    """Orange ghost - patrol with distance-based behavior."""
    
    def __init__(self, start_x: int, start_y: int):
        super().__init__(start_x, start_y, Colors.ORANGE, "Clyde")
        self.scatter_target = Position(1, 18)  # Bottom-left corner  
        self.release_delay = 8.0  # Last to leave
        self.chase_distance_threshold = 8  # Distance threshold for behavior change
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Clyde targets Pac-Man when far, but scatters when close."""
        px, py = pacman.get_position()
        pac_pos = Position(px, py)
        distance = self.position.distance_to(pac_pos)
        
        if distance > self.chase_distance_threshold:
            # Far away - chase Pac-Man
            return (px, py)
        else:
            # Close - head to scatter corner
            return (self.scatter_target.x, self.scatter_target.y)
