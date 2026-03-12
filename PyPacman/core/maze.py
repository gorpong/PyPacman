"""
Maze system for ASCII Pac-Man.
Handles maze layout, walls, dots, power pellets, and collision detection.
"""
from __future__ import annotations

from .sprites import Sprites
from .types import CellType, Position


class Maze:
    """Manages the game maze including walls, dots, and pellets."""

    def __init__(self, layout: list[str]) -> None:
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
        self.layout: list[str] = layout
        self.height: int = len(layout)
        self.width: int = max(len(row) for row in layout) if layout else 0

        self.grid: list[list[CellType]] = []
        self.dots: set[tuple[int, int]] = set()
        self.power_pellets: set[tuple[int, int]] = set()
        self.ghost_house_cells: set[tuple[int, int]] = set()
        self.ghost_door_cells: set[tuple[int, int]] = set()

        self.pacman_spawn: Position | None = None
        self.fruit_spawn: Position | None = None
        self.ghost_spawns: list[Position] = []

        self._parse_layout()

        self.collected_dots: set[tuple[int, int]] = set()
        self.collected_pellets: set[tuple[int, int]] = set()

        self.total_dots: int = len(self.dots)
        self.total_pellets: int = len(self.power_pellets)

    def _parse_layout(self) -> None:
        """Parse the string layout into a grid and item sets."""
        for y, row in enumerate(self.layout):
            grid_row: list[CellType] = []
            for x, char in enumerate(row):
                cell_type = CellType.EMPTY
                pos = (x, y)

                if char == '#':
                    cell_type = CellType.WALL
                elif char == '.':
                    cell_type = CellType.DOT
                    self.dots.add(pos)
                elif char in ('o', 'O'):
                    cell_type = CellType.POWER_PELLET
                    self.power_pellets.add(pos)
                elif char == 'G':
                    cell_type = CellType.GHOST_HOUSE
                    self.ghost_house_cells.add(pos)
                    self.ghost_spawns.append(Position(x, y))
                elif char == '-':
                    cell_type = CellType.GHOST_DOOR
                    self.ghost_door_cells.add(pos)
                elif char == 'P':
                    cell_type = CellType.EMPTY
                    self.pacman_spawn = Position(x, y)
                elif char == 'F':
                    cell_type = CellType.EMPTY
                    self.fruit_spawn = Position(x, y)

                grid_row.append(cell_type)

            while len(grid_row) < self.width:
                grid_row.append(CellType.EMPTY)

            self.grid.append(grid_row)

        if self.fruit_spawn is None and self.pacman_spawn is not None:
            self.fruit_spawn = self.pacman_spawn

    def is_wall(self, x: int, y: int) -> bool:
        """Check if a position contains a wall."""
        if not self.is_valid_position(x, y):
            return True
        return self.grid[y][x] == CellType.WALL

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

        if cell == CellType.WALL:
            return False

        if cell in (CellType.GHOST_HOUSE, CellType.GHOST_DOOR):
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
        return self.get_remaining_dots() == 0 and self.get_remaining_pellets() == 0

    def reset(self) -> None:
        """Reset all collected items (for new game/level)."""
        self.collected_dots.clear()
        self.collected_pellets.clear()

    def get_pacman_spawn(self) -> Position:
        """
        Get the Pac-Man spawn position.

        Returns:
            Position of spawn point, or center of maze if not defined
        """
        if self.pacman_spawn:
            return self.pacman_spawn
        return Position(self.width // 2, self.height * 3 // 4)

    def get_ghost_spawn_positions(self) -> list[Position]:
        """
        Get spawn positions for ghosts.

        Returns:
            List of Positions for ghost spawns
        """
        if self.ghost_spawns:
            return self.ghost_spawns.copy()
        center = Position(self.width // 2, self.height // 2)
        return [center, center, center, center]

    def get_fruit_spawn(self) -> Position:
        """
        Get the fruit spawn position.

        Returns:
            Position of fruit spawn point
        """
        if self.fruit_spawn:
            return self.fruit_spawn
        return self.get_pacman_spawn()

    def get_ghost_door_position(self) -> Position | None:
        """
        Get the position of the ghost house door.

        Returns:
            Position of door, or None if not found
        """
        if self.ghost_door_cells:
            doors = list(self.ghost_door_cells)
            center_x = sum(d[0] for d in doors) // len(doors)
            center_y = sum(d[1] for d in doors) // len(doors)
            return Position(center_x, center_y)
        return None

    def get_wall_char(self, x: int, y: int) -> str:
        """Get the appropriate wall character."""
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

        if cell == CellType.WALL:
            return self.get_wall_char(x, y)
        elif self.has_power_pellet(x, y):
            return Sprites.POWER_PELLET
        elif self.has_dot(x, y):
            return Sprites.DOT
        elif cell == CellType.GHOST_HOUSE:
            return Sprites.EMPTY
        elif cell == CellType.GHOST_DOOR:
            return Sprites.GHOST_DOOR
        else:
            return Sprites.EMPTY
