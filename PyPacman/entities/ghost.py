"""Ghost AI system implementation."""

from typing import Tuple, Optional, List, Dict, Deque
from collections import deque
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


class GhostSpeed:
    """Speed multipliers for ghost movement."""
    NORMAL: float = 1.0
    VULNERABLE: float = 0.5
    EATEN: float = 2.0
    IN_HOUSE: float = 0.6
    LEAVING_HOUSE: float = 0.8


# Type alias for direction tuples - generic name for future flexibility
DirectionType = Tuple[int, int]


class Ghost(MovableEntity):
    """Base ghost class with common behaviors."""
    
    BASE_SPEED: float = 7.0
    
    def __init__(self, start_x: int, start_y: int, color: str, name: str) -> None:
        """Initialize a ghost."""
        super().__init__(start_x, start_y, speed=self.BASE_SPEED)
        
        self.color: str = color
        self.name: str = name
        
        # AI state
        self.mode: GhostMode = GhostMode.SCATTER
        self.state: GhostState = GhostState.IN_HOUSE
        self.target: Position = Position(start_x, start_y)
        
        # Timers
        self.mode_timer: float = 0.0
        self.vulnerable_timer: float = 0.0
        self.release_timer: float = 0.0
        
        # Behavior parameters
        self.scatter_target: Position = Position(1, 1)
        self.release_delay: float = 0.0
        
        # House exit tracking
        self.house_exit_target: Optional[Position] = None
        
        # Pathfinding for returning ghosts
        self.return_path: List[Position] = []
        self.path_target: Optional[Position] = None
        
    def reset(self) -> None:
        """Reset ghost to starting position and state."""
        super().reset()
        self.direction = Direction.UP
        self.state = GhostState.IN_HOUSE
        self.mode = GhostMode.SCATTER
        self.mode_timer = 0.0
        self.vulnerable_timer = 0.0
        self.release_timer = 0.0
        self.house_exit_target = None
        self.return_path = []
        self.path_target = None
    
    def get_current_speed(self) -> float:
        """
        Calculate the current movement speed based on mode and state.
        
        Returns:
            The effective speed for this update
        """
        base: float = self.BASE_SPEED
        
        # State-based speed modifiers (highest priority)
        if self.state == GhostState.IN_HOUSE:
            return base * GhostSpeed.IN_HOUSE
        elif self.state == GhostState.LEAVING_HOUSE:
            return base * GhostSpeed.LEAVING_HOUSE
        elif self.state == GhostState.RETURNING:
            return base * GhostSpeed.EATEN
        
        # Mode-based speed modifiers (for ACTIVE state)
        if self.mode == GhostMode.VULNERABLE:
            return base * GhostSpeed.VULNERABLE
        elif self.mode == GhostMode.EATEN:
            return base * GhostSpeed.EATEN
        
        return base * GhostSpeed.NORMAL
    
    def update_movement(self, delta_time: float, maze: Maze) -> bool:
        """
        Update movement based on current speed and time.
        
        Args:
            delta_time: Time since last update
            maze: The maze object
            
        Returns:
            True if ghost should move this frame
        """
        self.move_timer += delta_time
        
        current_speed: float = self.get_current_speed()
        move_delay: float = 1.0 / current_speed
        
        if self.move_timer >= move_delay:
            self.move_timer = 0.0
            return True
        
        return False
    
    def set_scatter_target_for_maze(self, maze: Maze) -> None:
        """Set appropriate scatter target based on maze dimensions."""
        self.scatter_target = Position(1, 1)
    
    def find_house_exit(self, maze: Maze) -> Optional[Position]:
        """
        Find the ghost house exit (position just outside the door).
        
        Args:
            maze: The maze object
            
        Returns:
            Position just outside the door, or None if not found
        """
        door_pos: Optional[Tuple[int, int]] = maze.get_ghost_door_position()
        if door_pos:
            door_x, door_y = door_pos
            # Return position just above the door (outside the house)
            for check_y in range(door_y - 1, max(0, door_y - 3), -1):
                if maze.is_walkable(door_x, check_y, is_ghost=False):
                    return Position(door_x, check_y)
            # Return door position itself as fallback
            return Position(door_x, door_y)
        
        # Fallback: find center top of ghost house area
        if maze.ghost_house_cells:
            ghost_cells: List[Tuple[int, int]] = list(maze.ghost_house_cells)
            min_y: int = min(c[1] for c in ghost_cells)
            center_x: int = sum(c[0] for c in ghost_cells) // len(ghost_cells)
            
            for y in range(min_y - 1, -1, -1):
                if maze.is_walkable(center_x, y, is_ghost=False):
                    return Position(center_x, y)
        
        return Position(maze.width // 2, maze.height // 2 - 3)
    
    def find_house_entrance(self, maze: Maze) -> Optional[Position]:
        """
        Find the ghost house entrance (door position) for returning ghosts.
        
        Args:
            maze: The maze object
            
        Returns:
            Position of the ghost house door
        """
        door_pos: Optional[Tuple[int, int]] = maze.get_ghost_door_position()
        if door_pos:
            return Position(door_pos[0], door_pos[1])
        
        # Fallback to start position
        return Position(self.start_position.x, self.start_position.y)
    
    def _find_path_to_target(self, maze: Maze, target: Position) -> List[Position]:
        """
        Find a path from current position to target using BFS.
        
        Args:
            maze: The maze object
            target: The target position to reach
            
        Returns:
            List of positions forming the path (excluding current position)
        """
        start: Tuple[int, int] = (self.position.x, self.position.y)
        goal: Tuple[int, int] = (target.x, target.y)
        
        if start == goal:
            return []
        
        # BFS setup
        queue: Deque[Tuple[int, int]] = deque([start])
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        
        # Direction offsets for neighbors
        directions: List[DirectionType] = [
            Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT
        ]
        
        while queue:
            current: Tuple[int, int] = queue.popleft()
            
            if current == goal:
                # Reconstruct path
                path: List[Position] = []
                while current != start:
                    path.append(Position(current[0], current[1]))
                    prev: Optional[Tuple[int, int]] = came_from.get(current)
                    if prev is None:
                        break
                    current = prev
                path.reverse()
                return path
            
            # Explore neighbors
            for dx, dy in directions:
                next_x: int = current[0] + dx
                next_y: int = current[1] + dy
                next_pos: Tuple[int, int] = (next_x, next_y)
                
                if next_pos in came_from:
                    continue
                
                # Check if we can move there (ghosts can use ghost house/door when returning)
                if maze.is_walkable_for_ghost(next_x, next_y):
                    came_from[next_pos] = current
                    queue.append(next_pos)
        
        # No path found - return empty
        return []
    
    def _get_next_path_direction(self, maze: Maze) -> Optional[DirectionType]:
        """
        Get the next direction from the pre-calculated path.
        
        Args:
            maze: The maze object
            
        Returns:
            Direction to move, or None if no path
        """
        if not self.return_path:
            return None
        
        next_pos: Position = self.return_path[0]
        
        # Calculate direction to next path position
        dx: int = next_pos.x - self.position.x
        dy: int = next_pos.y - self.position.y
        
        # Normalize to unit direction
        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)
        
        # Check if we've reached this path node
        if self.position.x == next_pos.x and self.position.y == next_pos.y:
            self.return_path.pop(0)
            if self.return_path:
                return self._get_next_path_direction(maze)
            return None
        
        return (dx, dy)
        
    def update(self, delta_time: float, maze: Maze, pacman: PacMan) -> None:
        """Update ghost AI and movement."""
        # Update mode timer
        self.mode_timer += delta_time
        
        # Update vulnerable timer
        if self.vulnerable_timer > 0:
            self.vulnerable_timer -= delta_time
            if self.vulnerable_timer <= 0:
                self.vulnerable_timer = 0
                if self.mode == GhostMode.VULNERABLE:
                    self.mode = GhostMode.SCATTER
        
        # Handle house release timing
        if self.state == GhostState.IN_HOUSE:
            self.release_timer += delta_time
            if self.release_timer >= self.release_delay:
                self.state = GhostState.LEAVING_HOUSE
                if self.house_exit_target is None:
                    self.house_exit_target = self.find_house_exit(maze)
        
        # Update AI behavior
        self._update_ai(maze, pacman)
        
        # Update movement
        if self.update_movement(delta_time, maze):
            self._perform_movement(maze)
    
    def _update_ai(self, maze: Maze, pacman: PacMan) -> None:
        """Update AI target based on current mode and state."""
        if self.state == GhostState.IN_HOUSE:
            self._bob_in_house(maze)
            return
            
        elif self.state == GhostState.LEAVING_HOUSE:
            if self.house_exit_target is None:
                self.house_exit_target = self.find_house_exit(maze)
            
            if self.house_exit_target:
                self.target = self.house_exit_target
                
                current_x, current_y = self.position.x, self.position.y
                exit_x, exit_y = self.house_exit_target.x, self.house_exit_target.y
                
                at_target: bool = (abs(current_x - exit_x) <= 1 and 
                                   abs(current_y - exit_y) <= 1)
                not_in_house: bool = (not maze.is_ghost_house(current_x, current_y) and 
                                      not maze.is_ghost_door(current_x, current_y))
                
                if at_target or not_in_house:
                    self.state = GhostState.ACTIVE
                    self.house_exit_target = None
                    self.set_scatter_target_for_maze(maze)
                
        elif self.state == GhostState.ACTIVE:
            if self.mode == GhostMode.SCATTER:
                self.target = self.scatter_target
            elif self.mode == GhostMode.CHASE:
                chase_target: Tuple[int, int] = self._get_chase_target(pacman)
                self.target = Position(chase_target[0], chase_target[1])
            elif self.mode == GhostMode.VULNERABLE:
                self._flee_from_pacman(maze, pacman)
            elif self.mode == GhostMode.EATEN:
                self.state = GhostState.RETURNING
                self._init_return_path(maze)
                
        elif self.state == GhostState.RETURNING:
            self._update_returning(maze)
    
    def _init_return_path(self, maze: Maze) -> None:
        """Initialize the path for returning to ghost house."""
        entrance: Optional[Position] = self.find_house_entrance(maze)
        if entrance:
            self.path_target = entrance
            self.return_path = self._find_path_to_target(maze, entrance)
            self.target = entrance
        else:
            self.target = Position(self.start_position.x, self.start_position.y)
            self.return_path = []
    
    def _update_returning(self, maze: Maze) -> None:
        """Update AI when returning to ghost house."""
        current_x, current_y = self.position.x, self.position.y
        
        # Check if we've reached the ghost house interior
        if maze.is_ghost_house(current_x, current_y):
            self.state = GhostState.IN_HOUSE
            self.mode = GhostMode.SCATTER
            self.release_timer = self.release_delay * 0.3
            self.return_path = []
            self.path_target = None
            return
        
        # Check if we're at the door - continue into the house
        if maze.is_ghost_door(current_x, current_y):
            # Target the start position inside the house
            inside_target: Position = Position(self.start_position.x, self.start_position.y)
            self.return_path = self._find_path_to_target(maze, inside_target)
            self.target = inside_target
            return
        
        # If we have no path or reached end of path, recalculate
        if not self.return_path:
            self._init_return_path(maze)
    
    def _bob_in_house(self, maze: Maze) -> None:
        """Simple up/down movement while in ghost house."""
        if self.direction == Direction.UP or self.direction == Direction.NONE:
            new_y: int = self.position.y - 1
            if not maze.is_walkable_for_ghost(self.position.x, new_y):
                self.direction = Direction.DOWN
            else:
                self.direction = Direction.UP
        else:
            new_y = self.position.y + 1
            if not maze.is_walkable_for_ghost(self.position.x, new_y):
                self.direction = Direction.UP
            else:
                self.direction = Direction.DOWN
        
        dx, dy = self.direction
        self.target = Position(self.position.x + dx, self.position.y + dy)
    
    def _flee_from_pacman(self, maze: Maze, pacman: PacMan) -> None:
        """Choose a direction away from Pac-Man when vulnerable."""
        px, py = pacman.get_position()
        
        best_distance: float = -1
        best_target: Optional[Position] = None
        
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            dx, dy = direction
            new_x: int = self.position.x + dx * 3
            new_y: int = self.position.y + dy * 3
            
            distance: float = ((new_x - px) ** 2 + (new_y - py) ** 2) ** 0.5
            
            if distance > best_distance:
                check_x: int = self.position.x + dx
                check_y: int = self.position.y + dy
                if maze.is_walkable_for_ghost(check_x, check_y):
                    if not maze.is_ghost_house(check_x, check_y):
                        best_distance = distance
                        best_target = Position(new_x, new_y)
        
        if best_target:
            self.target = best_target
        else:
            self._choose_random_target(maze)
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Get the target position for chase mode. Override in subclasses."""
        return pacman.get_position()
    
    def _choose_random_target(self, maze: Maze) -> None:
        """Choose a random direction when needed."""
        directions: List[DirectionType] = [
            Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT
        ]
        random.shuffle(directions)
        
        for direction in directions:
            dx, dy = direction
            new_x: int = self.position.x + dx
            new_y: int = self.position.y + dy
            if maze.is_walkable_for_ghost(new_x, new_y):
                if not maze.is_ghost_house(new_x, new_y):
                    self.target = Position(new_x, new_y)
                    break
    
    def _perform_movement(self, maze: Maze) -> None:
        """Execute movement towards target."""
        # For returning ghosts, use pathfinding
        if self.state == GhostState.RETURNING and self.return_path:
            path_direction: Optional[DirectionType] = self._get_next_path_direction(maze)
            if path_direction:
                dx, dy = path_direction
                new_x: int = self.position.x + dx
                new_y: int = self.position.y + dy
                
                if maze.is_walkable_for_ghost(new_x, new_y):
                    self.direction = path_direction
                    self.position.x = new_x
                    self.position.y = new_y
                    return
        
        # Standard movement for other states
        best_direction: DirectionType = self._get_best_direction(maze)
        
        if best_direction != Direction.NONE:
            self.direction = best_direction
            dx, dy = best_direction
            new_x: int = self.position.x + dx
            new_y: int = self.position.y + dy
            
            can_move: bool = self._can_move_to_cell(maze, new_x, new_y)
            
            if can_move:
                self.position.x = new_x
                self.position.y = new_y
    
    def _can_move_to_cell(self, maze: Maze, x: int, y: int) -> bool:
        """
        Check if ghost can move to the specified cell.
        
        Args:
            maze: The maze object
            x: Target x coordinate
            y: Target y coordinate
            
        Returns:
            True if the ghost can move to this cell
        """
        if not maze.is_walkable_for_ghost(x, y):
            return False
        
        # Returning ghosts can enter ghost house and door
        if self.state == GhostState.RETURNING:
            return True
        
        # Active ghosts shouldn't enter ghost house or door
        if self.state == GhostState.ACTIVE:
            if maze.is_ghost_house(x, y) or maze.is_ghost_door(x, y):
                return False
        
        return True
    
    def _get_best_direction(self, maze: Maze) -> DirectionType:
        """
        Calculate the best direction to move towards target.
        
        Args:
            maze: The maze object
            
        Returns:
            The best direction tuple to move
        """
        if self.state == GhostState.IN_HOUSE:
            return self.direction
        
        reverse_direction: DirectionType = (-self.direction[0], -self.direction[1])
        
        # Determine if we can reverse direction
        can_reverse: bool = self._should_allow_reverse()
        
        possible_directions: List[Tuple[DirectionType, float]] = []
        
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            # Skip reverse unless allowed
            if direction == reverse_direction and not can_reverse:
                continue
                
            dx, dy = direction
            new_x: int = self.position.x + dx
            new_y: int = self.position.y + dy
            
            if self._can_move_to_cell(maze, new_x, new_y):
                new_pos: Position = Position(new_x, new_y)
                distance: float = new_pos.distance_to(self.target)
                possible_directions.append((direction, distance))
        
        if not possible_directions:
            # Must reverse - no other option
            return reverse_direction
        
        # Sort by distance to target (shortest first)
        possible_directions.sort(key=lambda x: x[1])
        
        return possible_directions[0][0]
    
    def _should_allow_reverse(self) -> bool:
        """
        Determine if the ghost should be allowed to reverse direction.
        
        Returns:
            True if reversing is allowed in current state
        """
        # Returning ghosts use pathfinding, so greedy reversal isn't needed
        # But allow it as fallback if path fails
        if self.state == GhostState.RETURNING:
            return True
        
        # Leaving house ghosts can reverse
        if self.state == GhostState.LEAVING_HOUSE:
            return True
        
        # Vulnerable ghosts can reverse
        if self.mode == GhostMode.VULNERABLE:
            return True
        
        # Normal active ghosts cannot reverse (classic Pac-Man rule)
        return False
    
    def set_mode(self, mode: GhostMode, duration: float = 0.0) -> None:
        """Set ghost mode and optional timer."""
        self.mode = mode
        self.mode_timer = 0.0
        
        if mode == GhostMode.VULNERABLE:
            self.vulnerable_timer = duration
    
    def make_vulnerable(self, duration: float) -> None:
        """Make ghost vulnerable (after power pellet)."""
        if self.mode != GhostMode.EATEN and self.state != GhostState.RETURNING:
            previous_mode: GhostMode = self.mode
            self.set_mode(GhostMode.VULNERABLE, duration)
            if self.state == GhostState.ACTIVE and previous_mode != GhostMode.VULNERABLE:
                self.direction = (-self.direction[0], -self.direction[1])
    
    def get_eaten(self) -> None:
        """Handle ghost being eaten by Pac-Man."""
        self.mode = GhostMode.EATEN
        self.state = GhostState.RETURNING
        self.vulnerable_timer = 0.0
        self.return_path = []  # Will be calculated in _update_ai
        self.path_target = None
    
    def is_vulnerable(self) -> bool:
        """Check if ghost is vulnerable to Pac-Man."""
        return self.mode == GhostMode.VULNERABLE and self.vulnerable_timer > 0
    
    def is_dangerous(self) -> bool:
        """Check if ghost is dangerous to Pac-Man."""
        return (self.state == GhostState.ACTIVE and 
                self.mode in [GhostMode.SCATTER, GhostMode.CHASE])
    
    def can_be_eaten(self) -> bool:
        """Check if this ghost can be eaten by Pac-Man right now."""
        return self.is_vulnerable() and self.state == GhostState.ACTIVE
    
    def get_sprite(self) -> str:
        """Get the sprite character for this ghost."""
        if self.mode == GhostMode.EATEN or self.state == GhostState.RETURNING:
            return Sprites.EATEN_GHOST
        elif self.mode == GhostMode.VULNERABLE:
            return Sprites.VULNERABLE_GHOST
        else:
            return Sprites.GHOST
    
    def get_color(self) -> str:
        """Get the color for this ghost."""
        if self.mode == GhostMode.VULNERABLE:
            if self.vulnerable_timer < 2.0 and int(self.vulnerable_timer * 4) % 2 == 0:
                return Colors.WHITE
            return Colors.BLUE
        elif self.mode == GhostMode.EATEN or self.state == GhostState.RETURNING:
            return Colors.WHITE
        else:
            return self.color


class Blinky(Ghost):
    """Red ghost - aggressive chaser, first to leave house."""
    
    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__(start_x, start_y, Colors.RED, "Blinky")
        self.release_delay = 0.0
    
    def set_scatter_target_for_maze(self, maze: Maze) -> None:
        """Blinky scatters to top-right corner."""
        self.scatter_target = Position(maze.width - 2, 1)
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Blinky directly targets Pac-Man."""
        return pacman.get_position()


class Pinky(Ghost):
    """Pink ghost - ambusher, targets ahead of Pac-Man."""
    
    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__(start_x, start_y, Colors.PINK, "Pinky")
        self.release_delay = 3.0
    
    def set_scatter_target_for_maze(self, maze: Maze) -> None:
        """Pinky scatters to top-left corner."""
        self.scatter_target = Position(1, 1)
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Pinky targets 4 spaces ahead of Pac-Man."""
        px, py = pacman.get_position()
        dx, dy = pacman.direction
        
        target_x: int = px + dx * 4
        target_y: int = py + dy * 4
        
        return (target_x, target_y)


class Inky(Ghost):
    """Cyan ghost - uses Blinky's position for complex targeting."""
    
    def __init__(self, start_x: int, start_y: int, blinky: Optional['Blinky'] = None) -> None:
        super().__init__(start_x, start_y, Colors.CYAN, "Inky")
        self.release_delay = 6.0
        self.blinky: Optional[Blinky] = blinky
    
    def set_scatter_target_for_maze(self, maze: Maze) -> None:
        """Inky scatters to bottom-right corner."""
        self.scatter_target = Position(maze.width - 2, maze.height - 2)
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Inky uses complex targeting based on Pac-Man and Blinky."""
        px, py = pacman.get_position()
        dx, dy = pacman.direction
        
        intermediate_x: int = px + dx * 2
        intermediate_y: int = py + dy * 2
        
        if self.blinky:
            bx, by = self.blinky.get_position()
            target_x: int = intermediate_x + (intermediate_x - bx)
            target_y: int = intermediate_y + (intermediate_y - by)
            return (target_x, target_y)
        
        return (intermediate_x, intermediate_y)


class Clyde(Ghost):
    """Orange ghost - shy, runs away when close to Pac-Man."""
    
    def __init__(self, start_x: int, start_y: int) -> None:
        super().__init__(start_x, start_y, Colors.ORANGE, "Clyde")
        self.release_delay = 9.0
        self.shy_distance: int = 8
    
    def set_scatter_target_for_maze(self, maze: Maze) -> None:
        """Clyde scatters to bottom-left corner."""
        self.scatter_target = Position(1, maze.height - 2)
    
    def _get_chase_target(self, pacman: PacMan) -> Tuple[int, int]:
        """Clyde chases when far, scatters when close."""
        px, py = pacman.get_position()
        pac_pos: Position = Position(px, py)
        distance: float = self.position.distance_to(pac_pos)
        
        if distance > self.shy_distance:
            return (px, py)
        else:
            return (self.scatter_target.x, self.scatter_target.y)
