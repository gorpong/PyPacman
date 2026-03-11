"""Ghost Manager for coordinating all four ghosts."""

from typing import List, Optional, Tuple
from .ghost import Ghost, Blinky, Pinky, Inky, Clyde, GhostMode, GhostState, DirectionType
from .pacman import PacMan
from .base import Position
from ..core.constants import GHOST_VULNERABLE_DURATION
from ..core.maze import Maze


class GhostManager:
    """Manages all four ghosts and their coordinated behaviors."""
    
    def __init__(self, maze: Maze) -> None:
        """Initialize the ghost manager with ghost starting positions."""
        self.maze: Maze = maze
        
        # Find ghost spawn positions from maze
        ghost_spawns: List[Tuple[int, int]] = maze.get_ghost_spawn_positions()
        
        # Ensure we have at least 4 spawn positions
        while len(ghost_spawns) < 4:
            if ghost_spawns:
                ghost_spawns.append(ghost_spawns[0])
            else:
                ghost_spawns.append((maze.width // 2, maze.height // 2))
        
        # Create the four ghosts at their spawn positions
        blinky: Blinky = Blinky(ghost_spawns[0][0], ghost_spawns[0][1])
        pinky: Pinky = Pinky(ghost_spawns[1][0], ghost_spawns[1][1])
        inky: Inky = Inky(ghost_spawns[2][0], ghost_spawns[2][1], blinky)
        clyde: Clyde = Clyde(
            ghost_spawns[3][0] if len(ghost_spawns) > 3 else ghost_spawns[0][0],
            ghost_spawns[3][1] if len(ghost_spawns) > 3 else ghost_spawns[0][1]
        )
        
        self.ghosts: List[Ghost] = [blinky, pinky, inky, clyde]
        
        # Set initial scatter targets based on maze
        for ghost in self.ghosts:
            ghost.set_scatter_target_for_maze(maze)
        
        # Track previous positions for crossing detection
        self.previous_ghost_positions: List[Tuple[int, int]] = []
        self._update_previous_positions()
        
        # Mode timing configuration
        self.mode_timer: float = 0.0
        self.current_mode_duration: float = 7.0
        self.mode_sequence: List[Tuple[GhostMode, float]] = [
            (GhostMode.SCATTER, 7.0),
            (GhostMode.CHASE, 20.0),
            (GhostMode.SCATTER, 7.0),
            (GhostMode.CHASE, 20.0),
            (GhostMode.SCATTER, 5.0),
            (GhostMode.CHASE, 20.0),
            (GhostMode.SCATTER, 5.0),
            (GhostMode.CHASE, float('inf'))
        ]
        self.sequence_index: int = 0
        
        # Track eaten ghosts for scoring
        self.ghosts_eaten_in_sequence: int = 0
        self.vulnerability_expired: bool = False
    
    def _update_previous_positions(self) -> None:
        """Store current ghost positions as previous positions."""
        self.previous_ghost_positions = [ghost.get_position() for ghost in self.ghosts]
    
    def reset(self) -> None:
        """Reset all ghosts to starting state."""
        for ghost in self.ghosts:
            ghost.reset()
            ghost.set_scatter_target_for_maze(self.maze)
        
        self._update_previous_positions()
        
        self.mode_timer = 0.0
        self.sequence_index = 0
        self.current_mode_duration = self.mode_sequence[0][1]
        self.ghosts_eaten_in_sequence = 0
        self.vulnerability_expired = False
    
    def update(self, delta_time: float, maze: Maze, pacman: PacMan) -> None:
        """Update all ghosts and mode timing."""
        # Store previous positions before updating
        self._update_previous_positions()
        
        # Track if any ghost was vulnerable before this update
        was_any_vulnerable: bool = any(ghost.is_vulnerable() for ghost in self.ghosts)
        
        # Update global mode timing
        self.mode_timer += delta_time
        
        # Handle mode sequence timing (only if no ghosts are vulnerable)
        if not was_any_vulnerable:
            if (self.sequence_index < len(self.mode_sequence) and 
                self.mode_timer >= self.current_mode_duration):
                
                self.sequence_index += 1
                if self.sequence_index < len(self.mode_sequence):
                    next_mode, duration = self.mode_sequence[self.sequence_index]
                    self._set_all_ghost_mode(next_mode)
                    self.current_mode_duration = duration
                    self.mode_timer = 0.0
        
        # Update each ghost
        for ghost in self.ghosts:
            ghost.update(delta_time, maze, pacman)
        
        # Check if vulnerable ghosts have expired
        any_vulnerable_now: bool = any(ghost.is_vulnerable() for ghost in self.ghosts)
        
        if was_any_vulnerable and not any_vulnerable_now:
            self.ghosts_eaten_in_sequence = 0
            self.vulnerability_expired = True
        else:
            self.vulnerability_expired = False
    
    def _set_all_ghost_mode(self, mode: GhostMode) -> None:
        """Set mode for all active ghosts that aren't vulnerable or eaten."""
        for ghost in self.ghosts:
            if ghost.mode not in (GhostMode.VULNERABLE, GhostMode.EATEN):
                if ghost.state != GhostState.RETURNING:
                    ghost.set_mode(mode)
    
    def make_all_vulnerable(self) -> None:
        """Make all ghosts vulnerable after power pellet consumption."""
        for ghost in self.ghosts:
            ghost.make_vulnerable(GHOST_VULNERABLE_DURATION)
        self.ghosts_eaten_in_sequence = 0
    
    def check_collision_with_pacman(
        self, 
        pacman: PacMan, 
        previous_pacman_pos: Optional[Tuple[int, int]] = None
    ) -> Optional[Ghost]:
        """
        Check if any ghost collides with Pac-Man.
        
        This checks for:
        1. Same cell collision (ghost and Pac-Man in same position)
        2. Crossing collision (ghost and Pac-Man swapped positions)
        
        Args:
            pacman: The Pac-Man instance
            previous_pacman_pos: Pac-Man's position before this frame's movement
            
        Returns:
            The colliding ghost, or None if no collision
        """
        px, py = pacman.get_position()
        
        for i, ghost in enumerate(self.ghosts):
            # Skip ghosts that can't collide
            if ghost.state != GhostState.ACTIVE:
                continue
            if ghost.mode == GhostMode.EATEN:
                continue
            
            gx, gy = ghost.get_position()
            
            # Check 1: Same cell collision
            if gx == px and gy == py:
                if ghost.is_vulnerable():
                    self.eat_ghost(ghost)
                return ghost
            
            # Check 2: Crossing collision (swap detection)
            if previous_pacman_pos is not None and i < len(self.previous_ghost_positions):
                prev_px, prev_py = previous_pacman_pos
                prev_gx, prev_gy = self.previous_ghost_positions[i]
                
                pacman_moved_to_ghost: bool = (px == prev_gx and py == prev_gy)
                ghost_moved_to_pacman: bool = (gx == prev_px and gy == prev_py)
                
                # Full swap
                if pacman_moved_to_ghost and ghost_moved_to_pacman:
                    if ghost.is_vulnerable():
                        self.eat_ghost(ghost)
                    return ghost
                
                # Pac-Man caught up to stationary ghost
                if pacman_moved_to_ghost and (gx == prev_gx and gy == prev_gy):
                    if ghost.is_vulnerable():
                        self.eat_ghost(ghost)
                    return ghost
                
                # Ghost caught up to stationary Pac-Man
                if ghost_moved_to_pacman and (px == prev_px and py == prev_py):
                    if ghost.is_vulnerable():
                        self.eat_ghost(ghost)
                    return ghost
        
        return None
    
    def eat_ghost(self, ghost: Ghost) -> int:
        """
        Handle ghost being eaten by Pac-Man.
        
        Args:
            ghost: The ghost being eaten
            
        Returns:
            Points scored for eating the ghost
        """
        if ghost.is_vulnerable():
            ghost.get_eaten()
            
            base_score: int = 200
            score: int = base_score * (2 ** self.ghosts_eaten_in_sequence)
            self.ghosts_eaten_in_sequence += 1
            
            return min(score, 1600)
        
        return 0
    
    def get_ghost_positions(self) -> List[Tuple[int, int, str, str]]:
        """Get positions of all ghosts for rendering."""
        positions: List[Tuple[int, int, str, str]] = []
        for ghost in self.ghosts:
            x, y = ghost.get_position()
            sprite: str = ghost.get_sprite()
            color: str = ghost.get_color()
            positions.append((x, y, sprite, color))
        
        return positions
    
    def get_vulnerable_ghosts(self) -> List[Ghost]:
        """Get list of currently vulnerable ghosts."""
        return [ghost for ghost in self.ghosts if ghost.is_vulnerable()]
    
    def get_dangerous_ghosts(self) -> List[Ghost]:
        """Get list of currently dangerous ghosts."""
        return [ghost for ghost in self.ghosts if ghost.is_dangerous()]
    
    def are_all_ghosts_home(self) -> bool:
        """Check if all ghosts are in the ghost house."""
        return all(ghost.state == GhostState.IN_HOUSE for ghost in self.ghosts)
    
    def get_ghost_by_name(self, name: str) -> Optional[Ghost]:
        """Get a specific ghost by name."""
        for ghost in self.ghosts:
            if ghost.name.lower() == name.lower():
                return ghost
        return None
