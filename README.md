# ASCII Pac-Man v1.0

A complete terminal-based ASCII version of Pac-Man, bringing the arcade experience to your command line!

## **🎉 Version 1.0 - Full Release! 🎉**

## Features

### Gameplay

- 🎮 **Classic Pac-Man Gameplay**: Navigate mazes, collect dots, avoid ghosts
- 👻 **Four Unique Ghosts**: Each with distinct AI personalities (Blinky, Pinky, Inky, Clyde)
- 🎯 **Power Pellets**: Turn vulnerable ghosts blue and eat them for bonus points
- 💀 **Progressive Ghost Scoring**: 200, 400, 800, 1600 points per combo
- ❤️ **Lives System**: Start with 3 lives, respawn after death
- 📈 **Level Progression**: Increasing difficulty with faster ghosts
- 🏆 **High Score System**: Top 10 scores saved with player names

### Visual & Audio

- 🎨 **ASCII Graphics**: Beautiful terminal-based visuals using Unicode characters
- ✨ **Visual Effects**: Score popups, death animations, power pellet effects
- 📺 **Scrolling High Scores**: Arcade-style attract mode on splash screen
- 🖥️ **Terminal Optimized**: Works great in 80x24 terminals, auto-centers on larger displays

### Controls & Interface

- 🎮 **Dual Control Schemes**: 
  - Arrow keys (↑↓←→) for traditional users
  - WASD for left-handed players
- ⏸️ **Pause/Resume**: SPACE to pause, ESC or Q to quit
- 📊 **Live HUD**: Score, high score, lives, and level display

### Technical

- 🐍 **Pure Python**: No external dependencies, uses only Python standard library
- 🌍 **Cross-Platform**: Runs on Linux, macOS, and Windows
- 📦 **Easy Installation**: pip installable, console entry points
- ✅ **Well Tested**: 84 comprehensive unit tests

## Requirements

- Python 3.8+ (tested on 3.8, 3.9, 3.10, 3.11, 3.12)
- Terminal with 80x24 character display minimum
- Terminal with ANSI color support (most modern terminals)

## Installation

### From Source (Development)

```bash
git clone https://github.com/yourusername/PyPacman
cd PyPacman
pip install -e .
```

### Quick Start (No Installation)

```bash
git clone https://github.com/yourusername/PyPacman
cd PyPacman
python -m PyPacman
```

## Usage

After installation, you can run the game using either command:

```bash
pacman
# or
PyPacman
```

## Controls

### Standard Controls

- **↑/↓/←/→**: Move Pac-Man
- **Space**: Pause/Resume game
- **Q**: Quit game (with confirmation)

### Left-Handed Alternative

- **W/A/S/D**: Move Pac-Man (Up/Left/Down/Right)
- **Space**: Pause/Resume game
- **Q**: Quit game (with confirmation)

## Game Mechanics

### Scoring

- Dot: 10 points
- Power Pellet: 50 points
- Ghost (1st): 200 points
- Ghost (2nd): 400 points
- Ghost (3rd): 800 points
- Ghost (4th): 1600 points

### Ghost Behaviors

- **Blinky (Red)**: Aggressive chaser - always follows Pac-Man directly
- **Pinky (Pink)**: Ambusher - targets 4 spaces ahead of Pac-Man
- **Inky (Cyan)**: Unpredictable - uses complex targeting
- **Clyde (Orange)**: Shy - chases when far, scatters when close

## Development

The game is organized into a clean package structure:

```
PyPacman
├── CHANGELOG.md
├── AGENTS.md
├── LICENSE
├── PyPacman
│   ├── core
│   │   ├── constants.py
│   │   ├── game_engine.py
│   │   ├── game_state.py
│   │   ├── __init__.py
│   │   ├── maze.py
│   │   ├── __pycache__
│   │   └── scoring.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── levels.py
│   │   └── __pycache__
│   ├── entities
│   │   ├── base.py
│   │   ├── ghost_manager.py
│   │   ├── ghost.py
│   │   ├── __init__.py
│   │   ├── pacman.py
│   │   └── __pycache__
│   ├── __init__.py
│   ├── main.py
│   ├── __pycache__
│   └── ui
│       ├── display.py
│       ├── __init__.py
│       ├── input_handler.py
│       └── __pycache__
├── pyproject.toml
├── README.md
├── requirements.txt
├── setup.py
└── tests
    ├── __init__.py
    ├── __pycache__
    ├── test_display.py
    ├── test_game_engine.py
    ├── test_game_state.py
    ├── test_ghost.py
    ├── test_input_handler.py
    ├── test_maze.py
    ├── test_pacman.py
    └── test_scoring.py
```

See `AGENTS.md` for detailed development planning and architecture.

### Running Tests

```bash
python -m pytest tests/
```

### Building for Distribution

```bash
python -m build
```

## License

MIT License - Feel free to modify and share!

## Acknowledgments

Inspired by the original Pac-Man arcade game by Namco (1980).
