"""
Game constants and configuration settings.
"""

# Game dimensions
GAME_WIDTH = 80
GAME_HEIGHT = 24
MIN_TERMINAL_WIDTH = 80
MIN_TERMINAL_HEIGHT = 24

# Frame rate and timing
TARGET_FPS = 10
FRAME_TIME = 1.0 / TARGET_FPS

# Game states
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    QUIT = "quit"

# Key mappings
class Keys:
    # Standard controls
    UP = "up"
    DOWN = "down"
    LEFT = "left" 
    RIGHT = "right"
    
    # Left-handed alternative
    W = "w"
    A = "a"
    S = "s"
    D = "d"
    
    # Game controls
    SPACE = " "
    ESCAPE = "\x1b"
    QUIT = "q"

# Direction constants
class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)

# ASCII characters for game elements
class Sprites:
    WALL = "#"
    DOT = "."
    POWER_PELLET = "O"
    EMPTY = " "
    
    # Pac-Man sprites (direction-based)
    PACMAN_RIGHT = ">"
    PACMAN_LEFT = "<"
    PACMAN_UP = "^"
    PACMAN_DOWN = "v"
    PACMAN_CLOSED = "C"
    
    # Ghost sprites
    GHOST = "&"
    VULNERABLE_GHOST = "%"

# Colors (for terminals that support them)
class Colors:
    RESET = "\033[0m"
    YELLOW = "\033[93m"  # Pac-Man
    RED = "\033[91m"     # Blinky
    PINK = "\033[95m"    # Pinky
    CYAN = "\033[96m"    # Inky
    ORANGE = "\033[38;5;208m"  # Clyde
    BLUE = "\033[94m"    # Vulnerable ghosts
    WHITE = "\033[97m"   # Walls and dots

# Scoring
class Score:
    DOT = 10
    POWER_PELLET = 50
    GHOST_BASE = 200
    EXTRA_LIFE = 10000

# Game settings
INITIAL_LIVES = 3
POWER_PELLET_DURATION = 10.0  # seconds
GHOST_VULNERABLE_DURATION = 8.0  # seconds
