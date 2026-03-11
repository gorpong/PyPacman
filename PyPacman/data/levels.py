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

Design Guidelines:
    - Mazes should be roughly symmetrical left-to-right
    - All dots and power pellets must be reachable by Pac-Man
    - Ghost house should be centered with a door (-) on top
    - Power pellets traditionally go in corners
    - Tunnels on sides should wrap around (handled by game engine)
    - Keep maze height to 18-19 rows max to fit in 24-line display with HUD
"""

# =============================================================================
# LEVEL 1 - Classic Layout
# =============================================================================
# Inspired by the original Pac-Man arcade maze
# Size: 28 wide x 18 tall (fits in 24-line terminal with HUD)

LEVEL_1 = [
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
    "#O..##....... ........##..O#",
    "#..........................#",
    "############################",
]

# =============================================================================
# LEVEL 2 - Open Arena  
# =============================================================================
# More open layout with larger corridors
# Size: 28 wide x 18 tall

LEVEL_2 = [
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

# =============================================================================
# LEVEL 3 - Maze Runner
# =============================================================================
# More complex maze with tighter corridors
# Size: 28 wide x 18 tall

LEVEL_3 = [
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

# =============================================================================
# LEVEL 4 - Speed Run
# =============================================================================
# Wide corridors for fast gameplay
# Size: 28 wide x 18 tall  

LEVEL_4 = [
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

# =============================================================================
# LEVEL TEST - Simple Testing Maze
# =============================================================================
# Small, simple maze for testing and debugging
# Size: 28 wide x 13 tall

LEVEL_TEST = [
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

# =============================================================================
# LEVEL MINI - Compact Maze
# =============================================================================
# Very small maze for tiny terminals or quick games
# Size: 21 wide x 11 tall

LEVEL_MINI = [
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

# =============================================================================
# Level Registry
# =============================================================================

LEVELS = {
    1: LEVEL_1,
    2: LEVEL_2,
    3: LEVEL_3,
    4: LEVEL_4,
    'test': LEVEL_TEST,
    'mini': LEVEL_MINI,
}

# Level progression order
LEVEL_ORDER = [1, 2, 3, 4]


def get_level(level_num: int = 1) -> list:
    """
    Get a level layout by number.
    
    Args:
        level_num: Level number (1-based) or string key
        
    Returns:
        List of strings representing the maze layout
    """
    if level_num in LEVELS:
        return LEVELS[level_num]
    
    # Cycle through numbered levels
    if isinstance(level_num, int) and level_num > len(LEVEL_ORDER):
        cycle_index = (level_num - 1) % len(LEVEL_ORDER)
        return LEVELS[LEVEL_ORDER[cycle_index]]
    
    # Default to level 1
    return LEVELS[1]


def get_level_count() -> int:
    """Get the number of unique levels available."""
    return len(LEVEL_ORDER)


def find_spawn_point(layout: list, marker: str = 'P') -> tuple:
    """
    Find a spawn point marker in the maze layout.
    
    Args:
        layout: The maze layout (list of strings)
        marker: The character marking the spawn point
        
    Returns:
        Tuple (x, y) of the spawn position, or None if not found
    """
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            if char == marker:
                return (x, y)
    return None


def find_ghost_house_center(layout: list) -> tuple:
    """
    Find the center of the ghost house.
    
    Args:
        layout: The maze layout (list of strings)
        
    Returns:
        Tuple (x, y) of the ghost house center, or None if not found
    """
    ghost_positions = []
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            if char == 'G':
                ghost_positions.append((x, y))
    
    if not ghost_positions:
        return None
    
    # Calculate center
    avg_x = sum(p[0] for p in ghost_positions) // len(ghost_positions)
    avg_y = sum(p[1] for p in ghost_positions) // len(ghost_positions)
    return (avg_x, avg_y)
