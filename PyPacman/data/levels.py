"""
Level layouts for ASCII Pac-Man.
Each level is a list of strings representing the maze.

Legend:
    # = Wall
    . = Dot (10 points)
    O = Power Pellet (50 points, makes ghosts vulnerable)
    o = Power Pellet (alternate notation)
    G = Ghost house interior (ghosts spawn here)
    - = Ghost house door (ghosts can pass through)
    P = Pac-Man spawn point (treated as empty space)
    F = Fruit spawn point (treated as empty space, for future use)
      = Empty space (no dot)
"""
from __future__ import annotations

from ..core.types import Position

LEVEL_1: list[str] = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#O####.#####.##.#####.####O#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "     #.##..........##.#     ",
    "######.##.###--###.##.######",
    "      ....#GGGGGG#....      ",
    "######.##.########.##.######",
    "     #.##....P.....##.#     ",
    "######.##.########.##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#O####.#####.##.#####.####O#",
    "#..........................#",
    "############################",
]

LEVEL_2: list[str] = [
    "############################",
    "#O..........##..........O#",
    "#.####.####.##.####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##          ##.#     ",
    "######.##.###--###.##.######",
    "      ....#GGGGGG#....      ",
    "######.##.########.##.######",
    "     #.##.....P....##.#     ",
    "######.##.########.##.######",
    "#............##............#",
    "#.##.######.####.######.##.#",
    "#O..........    ..........O#",
    "#.########.####.########...#",
    "#..........................#",
    "############################",
]

LEVEL_3: list[str] = [
    "############################",
    "#O............##..........O#",
    "#.###.#######.##.#######.###",
    "#..........................#",
    "###.###.##.########.##.###.#",
    "#.......##....##....##.....#",
    "#.###.#.##### ## #####.###.#",
    "#.....#.##          ##.#...#",
    "######..##.###--###.##..####",
    "      ....#GGGGGG#....      ",
    "######..##.########.##..####",
    "#.....#.##....P....##.#...#",
    "#.###.#.##.########.##.###.#",
    "#.......##....##....##.....#",
    "###.###.##.########.##.###.#",
    "#O........................O#",
    "#.###.#######.##.#######.###",
    "#..........................#",
    "############################",
]

LEVEL_4: list[str] = [
    "############################",
    "#O..........##..........O#",
    "#.####.####.##.####.####.#",
    "#..........................#",
    "#.##.##.##.####.##.##.##.#",
    "#......##..####..##......#",
    "######.###.####.###.######",
    "     #.##..    ..##.#     ",
    "######.##.##--##.##.######",
    "      ....#GGGG#....      ",
    "######.##.######.##.######",
    "     #.##...P....##.#     ",
    "######.##.######.##.######",
    "#..........####..........#",
    "#.####.###.####.###.####.#",
    "#O....##..........##....O#",
    "#.####.##.######.##.####.#",
    "#..........................#",
    "############################",
]

LEVEL_TEST: list[str] = [
    "############################",
    "#O..........##..........O#",
    "#.###.####.####.####.###.#",
    "#........................#",
    "#.###.##.########.##.###.#",
    "#.....##....##....##.....#",
    "#####.##### ## #####.#####",
    "    #.##...----...##.#    ",
    "#####.##.#GGGGGG#.##.#####",
    "#.......#..GG..#.........#",
    "#.##.###.###### #.###.##.#",
    "#O.........P...........O#",
    "############################",
]

LEVEL_MINI: list[str] = [
    "#####################",
    "#O.......##.......O#",
    "#.###.##.##.##.###.#",
    "#.................#",
    "#.##.####--####.##.#",
    "#....#GGGGGG#....#",
    "#.##.########.##.#",
    "#.......P.........#",
    "#.#####.##.#####.#",
    "#O.................O#",
    "#####################",
]

LEVELS: dict[int | str, list[str]] = {
    1: LEVEL_1,
    2: LEVEL_2,
    3: LEVEL_3,
    4: LEVEL_4,
    'test': LEVEL_TEST,
    'mini': LEVEL_MINI,
}

LEVEL_ORDER: list[int] = [1, 2, 3, 4]


def get_level(level_num: int = 1) -> list[str]:
    """
    Get a level layout by number.

    Args:
        level_num: Level number (1-based) or string key

    Returns:
        List of strings representing the maze layout
    """
    if level_num in LEVELS:
        return LEVELS[level_num]

    if isinstance(level_num, int) and level_num > len(LEVEL_ORDER):
        cycle_index = (level_num - 1) % len(LEVEL_ORDER)
        return LEVELS[LEVEL_ORDER[cycle_index]]

    return LEVELS[1]


def get_level_count() -> int:
    """Get the number of unique levels available."""
    return len(LEVEL_ORDER)


def find_spawn_point(layout: list[str], marker: str = 'P') -> Position | None:
    """
    Find a spawn point marker in the maze layout.

    Args:
        layout: The maze layout (list of strings)
        marker: The character marking the spawn point

    Returns:
        Position of the spawn point, or None if not found
    """
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            if char == marker:
                return Position(x, y)
    return None


def find_ghost_house_center(layout: list[str]) -> Position | None:
    """
    Find the center of the ghost house.

    Args:
        layout: The maze layout (list of strings)

    Returns:
        Position of the ghost house center, or None if not found
    """
    ghost_positions: list[tuple[int, int]] = []
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            if char == 'G':
                ghost_positions.append((x, y))

    if not ghost_positions:
        return None

    avg_x = sum(p[0] for p in ghost_positions) // len(ghost_positions)
    avg_y = sum(p[1] for p in ghost_positions) // len(ghost_positions)
    return Position(avg_x, avg_y)
