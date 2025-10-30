"""Ghost Manager for coordinating all four ghosts."""

from typing import List, Optional, Tuple
from .ghost import Ghost, Blinky, Pinky, Inky, Clyde, GhostMode, GhostState
from .pacman import PacMan
from .base import Position
from ..core.constants import GHOST_VULNERABLE_DURATION
from ..core.maze import Maze


class GhostManager:
    """Manages all four ghosts and their coordinated behaviors."""
    
    def __init__(self, maze: Maze):
        """Initialize the ghost manager with ghost starting positions."""
        # Find ghost house position
        ghost_house_pos = self._find_ghost_house_center(maze)
        
        # Create the four ghosts with proper references
        blinky = Blinky(ghost_house_pos.x - 1, ghost_house_pos.y)
        pinky = Pinky(ghost_house_pos.x, ghost_house_pos.y)
        inky = Inky(ghost_house_pos.x + 1, ghost_house_pos.y, blinky)  # Pass Blinky reference
        clyde = Clyde(ghost_house_pos.x, ghost_house_pos.y + 1)
        
        self.ghosts: List[Ghost] = [blinky, pinky, inky, clyde]
        
        # Mode timing configuration
        self.mode_timer = 0.0
        self.current_mode_duration = 7.0  # Start with 7 seconds scatter
        self.mode_sequence = [
            (GhostMode.SCATTER, 7.0),
            (GhostMode.CHASE, 20.0),
            (GhostMode.SCATTER, 7.0),
            (GhostMode.CHASE, 20.0),
            (GhostMode.SCATTER, 5.0),
            (GhostMode.CHASE, 20.0),
            (GhostMode.SCATTER, 5.0),
            (GhostMode.CHASE, float('inf'))  # Chase forever after this
        ]
        self.sequence_index = 0
        
        # Track eaten ghosts for scoring
        self.ghosts_eaten_in_sequence = 0
        self.vulnerability_expired = False
        
    def _find_ghost_house_center(self, maze: Maze) -> Position:
        """Find the center of the ghost house in the maze."""
        ghost_positions = []
        
        # Find all ghost house positions
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.is_ghost_house(x, y):
                    ghost_positions.append((x, y))
        
        if ghost_positions:
            # Calculate center of ghost house
            avg_x = sum(pos[0] for pos in ghost_positions) // len(ghost_positions)
            avg_y = sum(pos[1] for pos in ghost_positions) // len(ghost_positions)
            return Position(avg_x, avg_y)
        
        # Fallback to center of maze
        return Position(maze.width // 2, maze.height // 2)
    
    def reset(self) -> None:
        """Reset all ghosts to starting state."""
        for ghost in self.ghosts:
            ghost.reset()
        
        self.mode_timer = 0.0
        self.sequence_index = 0
        self.current_mode_duration = self.mode_sequence[0][1]
        self.ghosts_eaten_in_sequence = 0
    
    def update(self, delta_time: float, maze: Maze, pacman: PacMan) -> None:
        """Update all ghosts and mode timing."""
        # Update global mode timing
        self.mode_timer += delta_time
        
        # Check if vulnerable ghosts have expired
        any_vulnerable = any(ghost.is_vulnerable() for ghost in self.ghosts)
        was_vulnerable = self.ghosts_eaten_in_sequence > 0 or any(g.vulnerable_timer > 0 for g in self.ghosts)
        
        if was_vulnerable and not any_vulnerable:
            self.ghosts_eaten_in_sequence = 0  # Reset eaten counter
            self.vulnerability_expired = True  # Signal that vulnerability just ended
        else:
            self.vulnerability_expired = False
        
        # Handle mode sequence timing
        if (self.sequence_index < len(self.mode_sequence) and 
            self.mode_timer >= self.current_mode_duration):
            
            # Switch to next mode
            self.sequence_index += 1
            if self.sequence_index < len(self.mode_sequence):
                next_mode, duration = self.mode_sequence[self.sequence_index]
                self._set_all_ghost_mode(next_mode)
                self.current_mode_duration = duration
                self.mode_timer = 0.0
        
        # Update each ghost
        for ghost in self.ghosts:
            ghost.update(delta_time, maze, pacman)
    
    def _set_all_ghost_mode(self, mode: GhostMode) -> None:
        """Set mode for all active ghosts."""
        for ghost in self.ghosts:
            if ghost.mode != GhostMode.VULNERABLE and ghost.mode != GhostMode.EATEN:
                ghost.set_mode(mode)
    
    def make_all_vulnerable(self) -> None:
        """Make all ghosts vulnerable after power pellet consumption."""
        for ghost in self.ghosts:
            ghost.make_vulnerable(GHOST_VULNERABLE_DURATION)
        self.ghosts_eaten_in_sequence = 0  # Reset the counter
    
    def check_collision_with_pacman(self, pacman: PacMan) -> Optional[Ghost]:
        """Check if any ghost collides with Pac-Man."""
        px, py = pacman.get_position()
        
        for ghost in self.ghosts:
            if ghost.collides_with(px, py):
                return ghost
        
        return None
    
    def get_ghost_positions(self) -> List[Tuple[int, int, str, str]]:
        """Get positions of all ghosts for rendering."""
        positions = []
        for ghost in self.ghosts:
            x, y = ghost.get_position()
            sprite = ghost.get_sprite()
            color = ghost.get_color()
            positions.append((x, y, sprite, color))
        
        return positions
    
    def get_vulnerable_ghosts(self) -> List[Ghost]:
        """Get list of currently vulnerable ghosts."""
        return [ghost for ghost in self.ghosts if ghost.is_vulnerable()]
    
    def get_dangerous_ghosts(self) -> List[Ghost]:
        """Get list of currently dangerous ghosts."""
        return [ghost for ghost in self.ghosts if ghost.is_dangerous()]
    
    def eat_ghost(self, ghost: Ghost) -> int:
        """
        Handle ghost being eaten by Pac-Man.
        
        Returns:
            Points scored for eating the ghost
        """
        if ghost.is_vulnerable():
            ghost.get_eaten()
            
            # Calculate score based on sequence
            base_score = 200
            score = base_score * (2 ** self.ghosts_eaten_in_sequence)
            self.ghosts_eaten_in_sequence += 1
            
            # Cap at 1600 points
            return min(score, 1600)
        
        return 0
    
    def are_all_ghosts_home(self) -> bool:
        """Check if all ghosts are in the ghost house."""
        return all(ghost.state == GhostState.IN_HOUSE for ghost in self.ghosts)
    
    def get_ghost_by_name(self, name: str) -> Optional[Ghost]:
        """Get a specific ghost by name."""
        for ghost in self.ghosts:
            if ghost.name.lower() == name.lower():
                return ghost
        return None
