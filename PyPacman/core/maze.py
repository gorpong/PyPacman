"""
Maze system for ASCII Pac-Man.
Handles maze layout, walls, dots, power pellets, and collision detection.
"""

from typing import Tuple, List, Optional
from .constants import Sprites


class Cell:
    """Represents a single cell in the maze."""
    WALL = 0
    EMPTY = 1
    DOT = 2
    POWER_PELLET = 3
    GHOST_HOUSE = 4
    GHOST_DOOR = 5


class Maze:
    """Manages the game maze including walls, dots, and pellets."""
    
    def __init__(self, layout: List[str]):
        """
        Initialize maze from a string layout.
        
        Args:
            layout: List of strings where each character represents:
                '#' = wall
                '.' = dot
                'o' or 'O' = power pellet
                ' ' = empty space
                'G' = ghost house interior
                '-' = ghost house door
                'P' = Pac-Man spawn point (treated as empty)
                'F' = Fruit spawn point (treated as empty)
        """
        self.layout = layout
        self.height = len(layout)
        self.width = max(len(row) for row in layout) if layout else 0
        
        # Parse the layout into a grid
        self.grid: List[List[int]] = []
        self.dots: set = set()
        self.power_pellets: set = set()
        self.ghost_house_cells: set = set()
        self.ghost_door_cells: set = set()
        
        # Spawn points
        self.pacman_spawn: Optional[Tuple[int, int]] = None
        self.fruit_spawn: Optional[Tuple[int, int]] = None
        self.ghost_spawns: List[Tuple[int, int]] = []
        
        self._parse_layout()
        
        # Track collected items
        self.collected_dots: set = set()
        self.collected_pellets: set = set()
        
        # Initial counts
        self.total_dots = len(self.dots)
        self.total_pellets = len(self.power_pellets)
    
    def _parse_layout(self):
        """Parse the string layout into a grid and item sets."""
        for y, row in enumerate(self.layout):
            grid_row = []
            for x, char in enumerate(row):
                cell_type = Cell.EMPTY
                pos = (x, y)
                
                if char == '#':
                    cell_type = Cell.WALL
                elif char == '.':
                    cell_type = Cell.DOT
                    self.dots.add(pos)
                elif char in ('o', 'O'):
                    cell_type = Cell.POWER_PELLET
                    self.power_pellets.add(pos)
                elif char == 'G':
                    cell_type = Cell.GHOST_HOUSE
                    self.ghost_house_cells.add(pos)
                    self.ghost_spawns.append(pos)
                elif char == '-':
                    cell_type = Cell.GHOST_DOOR
                    self.ghost_door_cells.add(pos)
                elif char == 'P':
                    cell_type = Cell.EMPTY
                    self.pacman_spawn = pos
                elif char == 'F':
                    cell_type = Cell.EMPTY
                    self.fruit_spawn = pos
                # else: empty space (cell_type remains EMPTY)
                
                grid_row.append(cell_type)
            
            # Pad row to width if needed
            while len(grid_row) < self.width:
                grid_row.append(Cell.EMPTY)
            
            self.grid.append(grid_row)
        
        # If no fruit spawn specified, default to center below ghost house
        if self.fruit_spawn is None and self.pacman_spawn is not None:
            self.fruit_spawn = self.pacman_spawn
    
    def is_wall(self, x: int, y: int) -> bool:
        """Check if a position contains a wall."""
        if not self.is_valid_position(x, y):
            return True  # Out of bounds is treated as wall
        return self.grid[y][x] == Cell.WALL
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within maze bounds."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_walkable(self, x: int, y: int, is_ghost: bool = False) -> bool:
        """
        Check if a position can be walked on.
        
        Args:
            x: X coordinate
            y: Y coordinate  
            is_ghost: If True, ghost house and doors are walkable
            
        Returns:
            True if the position can be walked on
        """
        if not self.is_valid_position(x, y):
            return False
        
        cell = self.grid[y][x]
        
        if cell == Cell.WALL:
            return False
        
        if cell == Cell.GHOST_HOUSE or cell == Cell.GHOST_DOOR:
            # Only ghosts can walk through ghost house/door
            return is_ghost
        
        return True
    
    def is_walkable_for_pacman(self, x: int, y: int) -> bool:
        """Check if Pac-Man can walk on this position."""
        return self.is_walkable(x, y, is_ghost=False)
    
    def is_walkable_for_ghost(self, x: int, y: int) -> bool:
        """Check if a ghost can walk on this position."""
        return self.is_walkable(x, y, is_ghost=True)
    
    def has_dot(self, x: int, y: int) -> bool:
        """Check if there's an uncollected dot at position."""
        pos = (x, y)
        return pos in self.dots and pos not in self.collected_dots
    
    def has_power_pellet(self, x: int, y: int) -> bool:
        """Check if there's an uncollected power pellet at position."""
        pos = (x, y)
        return pos in self.power_pellets and pos not in self.collected_pellets
    
    def collect_dot(self, x: int, y: int) -> bool:
        """
        Collect a dot at the given position.
        Returns True if a dot was collected.
        """
        pos = (x, y)
        if pos in self.dots and pos not in self.collected_dots:
            self.collected_dots.add(pos)
            return True
        return False
    
    def collect_power_pellet(self, x: int, y: int) -> bool:
        """
        Collect a power pellet at the given position.
        Returns True if a pellet was collected.
        """
        pos = (x, y)
        if pos in self.power_pellets and pos not in self.collected_pellets:
            self.collected_pellets.add(pos)
            return True
        return False
    
    def is_ghost_house(self, x: int, y: int) -> bool:
        """Check if position is part of the ghost house interior."""
        return (x, y) in self.ghost_house_cells
    
    def is_ghost_door(self, x: int, y: int) -> bool:
        """Check if position is the ghost house door."""
        return (x, y) in self.ghost_door_cells
    
    def get_remaining_dots(self) -> int:
        """Get the number of dots remaining to collect."""
        return self.total_dots - len(self.collected_dots)
    
    def get_remaining_pellets(self) -> int:
        """Get the number of power pellets remaining."""
        return self.total_pellets - len(self.collected_pellets)
    
    def is_level_complete(self) -> bool:
        """Check if all dots and pellets have been collected."""
        return (self.get_remaining_dots() == 0 and 
                self.get_remaining_pellets() == 0)
    
    def reset(self):
        """Reset all collected items (for new game/level)."""
        self.collected_dots.clear()
        self.collected_pellets.clear()
    
    def get_pacman_spawn(self) -> Tuple[int, int]:
        """
        Get the Pac-Man spawn position.
        
        Returns:
            Tuple (x, y) of spawn position, or center of maze if not defined
        """
        if self.pacman_spawn:
            return self.pacman_spawn
        # Default to center-bottom of maze
        return (self.width // 2, self.height * 3 // 4)
    
    def get_ghost_spawn_positions(self) -> List[Tuple[int, int]]:
        """
        Get spawn positions for ghosts.
        
        Returns:
            List of (x, y) tuples for ghost spawns
        """
        if self.ghost_spawns:
            return self.ghost_spawns.copy()
        # Default to center of maze
        center = (self.width // 2, self.height // 2)
        return [center, center, center, center]
    
    def get_fruit_spawn(self) -> Tuple[int, int]:
        """
        Get the fruit spawn position.
        
        Returns:
            Tuple (x, y) of fruit spawn position
        """
        if self.fruit_spawn:
            return self.fruit_spawn
        # Default to Pac-Man spawn or center
        return self.get_pacman_spawn()
    
    def get_ghost_door_position(self) -> Optional[Tuple[int, int]]:
        """
        Get the position of the ghost house door.
        
        Returns:
            Tuple (x, y) of door position, or None if not found
        """
        if self.ghost_door_cells:
            # Return the center door position if multiple
            doors = list(self.ghost_door_cells)
            center_x = sum(d[0] for d in doors) // len(doors)
            center_y = sum(d[1] for d in doors) // len(doors)
            return (center_x, center_y)
        return None
    
    def get_wall_char(self, x: int, y: int) -> str:
        """
        Get the appropriate wall character.
        """
        if not self.is_wall(x, y):
            return ' '
        return Sprites.WALL
    
    def get_cell_char(self, x: int, y: int) -> str:
        """
        Get the ASCII character to display for a cell.
        
        Returns:
            Character to display at this position
        """
        if not self.is_valid_position(x, y):
            return Sprites.EMPTY
        
        cell = self.grid[y][x]
        
        if cell == Cell.WALL:
            return self.get_wall_char(x, y)
        elif self.has_power_pellet(x, y):
            return Sprites.POWER_PELLET
        elif self.has_dot(x, y):
            return Sprites.DOT
        elif cell == Cell.GHOST_HOUSE:
            return Sprites.EMPTY  # Ghost house interior is empty
        elif cell == Cell.GHOST_DOOR:
            return Sprites.GHOST_DOOR  # Show the door
        else:
            return Sprites.EMPTY
