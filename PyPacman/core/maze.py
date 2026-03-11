"""
Maze system for ASCII Pac-Man.
Handles maze layout, walls, dots, power pellets, and collision detection.
"""

from typing import Tuple, List, Set
from .constants import Sprites


class Cell:
    """Represents a single cell in the maze."""
    WALL = 0
    EMPTY = 1
    DOT = 2
    POWER_PELLET = 3
    GHOST_HOUSE = 4


class Maze:
    """Manages the game maze including walls, dots, and pellets."""
    
    def __init__(self, layout: List[str]):
        """
        Initialize maze from a string layout.
        
        Args:
            layout: List of strings where each character represents:
                '#' = wall
                '.' = dot
                'o' = power pellet
                ' ' = empty space
                'G' = ghost house
        """
        self.layout = layout
        self.height = len(layout)
        self.width = max(len(row) for row in layout) if layout else 0
        
        # Parse the layout into a grid
        self.grid = []
        self.dots = set()
        self.power_pellets = set()
        self.ghost_house_cells = set()
        
        self._parse_layout()
        
        # Track collected items
        self.collected_dots = set()
        self.collected_pellets = set()
        
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
                elif char == 'o' or char == 'O':
                    cell_type = Cell.POWER_PELLET
                    self.power_pellets.add(pos)
                elif char == 'G':
                    cell_type = Cell.GHOST_HOUSE
                    self.ghost_house_cells.add(pos)
                
                grid_row.append(cell_type)
            
            # Pad row to width if needed
            while len(grid_row) < self.width:
                grid_row.append(Cell.EMPTY)
            
            self.grid.append(grid_row)
    
    def is_wall(self, x: int, y: int) -> bool:
        """Check if a position contains a wall."""
        if not self.is_valid_position(x, y):
            return True  # Out of bounds is treated as wall
        return self.grid[y][x] == Cell.WALL
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within maze bounds."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_walkable(self, x: int, y: int) -> bool:
        """Check if a position can be walked on (not a wall)."""
        return self.is_valid_position(x, y) and not self.is_wall(x, y)
    
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
        """Check if position is part of the ghost house."""
        return (x, y) in self.ghost_house_cells
    
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
    
    def get_wall_char(self, x: int, y: int) -> str:
        """
        Get the appropriate wall character.
        For simplicity and better appearance, use block characters.
        """
        if not self.is_wall(x, y):
            return ' '
        
        # Use sprite constant for walls
        # This provides a clean, retro arcade look
        return Sprites.WALL
    
    def get_cell_char(self, x: int, y: int) -> str:
        """
        Get the ASCII character to display for a cell.
        
        Returns:
            Character to display at this position
        """
        if not self.is_valid_position(x, y):
            return Sprites.EMPTY
        
        if self.is_wall(x, y):
            return self.get_wall_char(x, y)
        elif self.has_power_pellet(x, y):
            return Sprites.POWER_PELLET
        elif self.has_dot(x, y):
            return Sprites.DOT
        elif self.is_ghost_house(x, y):
            return Sprites.GHOST_HOUSE_FLOOR
        else:
            return Sprites.EMPTY
