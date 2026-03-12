# ASCII Pac-Man

A terminal-based ASCII version of the classic Pac-Man arcade game, implemented in pure Python.

Official repository: `https://github.com/gorpong/PyPacman`

## Current State

- Version: `1.0.0`
- Runtime requirement: Python `3.11+`
- Runtime dependencies: Python standard library only
- Packaging and tool configuration: `pyproject.toml`
- Test suite: `112` tests passing

## Features

- Classic Pac-Man gameplay with dots, power pellets, lives, and level progression
- Four ghosts with distinct chase behaviors: Blinky, Pinky, Inky, and Clyde
- Progressive ghost scoring: `200 / 400 / 800 / 1600`
- High score persistence with top-10 name entry
- Scrolling high scores on the menu screen
- Unicode terminal rendering with HUD, borders, and score popups
- Dual control scheme: arrow keys or `W/A/S/D`
- Optimized for `80x24` terminals with centering on larger terminals

## Installation

Install from the repository root:

```bash
python -m pip install .
```

Clone the repository:

```bash
git clone https://github.com/gorpong/PyPacman.git
cd PyPacman
```

For development:

```bash
python -m pip install -e ".[dev]"
```

## Running The Game

After installation, either console script works:

```bash
pacman
```

```bash
pypacman
```

You can also run the module directly from the repository:

```bash
python -m PyPacman.main
```

## Controls

- Arrow keys: move Pac-Man
- `W/A/S/D`: alternate movement controls
- `Space`: pause or resume
- `Q` or `Esc`: quit with confirmation

## Scoring

- Dot: `10`
- Power pellet: `50`
- Ghost 1: `200`
- Ghost 2: `400`
- Ghost 3: `800`
- Ghost 4: `1600`
- Extra life threshold: `10000`

## Development

### Test And Typecheck

Run the tests:

```bash
python -m pytest
```

Run type checking after installing the dev extras:

```bash
python -m mypy PyPacman
```

### Architecture

The codebase now uses a typed core with protocol-based boundaries to reduce import coupling.

Internal modules prefer leaf-module imports over package-barrel imports to keep the runtime import graph narrow and reduce circular import risk.

- `PyPacman/core/types.py`
  - Shared structural types such as `Position`, `Direction`, `GameMode`, and `CellType`
  - Lightweight protocols including `MazeProtocol`, `PacManProtocol`, and `GhostProtocol`
- `PyPacman/core/config.py`
  - Tunable dimensions, timing, and scoring configuration
- `PyPacman/core/colors.py` and `PyPacman/core/sprites.py`
  - Rendering constants separated from gameplay logic
- `PyPacman/core/game_engine.py`
  - Main game loop, screen flow, and orchestration
- `PyPacman/core/maze.py`
  - Maze parsing, collision rules, and spawn resolution
- `PyPacman/entities/`
  - Pac-Man, ghosts, and shared movement behavior
- `PyPacman/ui/`
  - Display rendering and keyboard input
- `PyPacman/data/levels.py`
  - Maze layouts and layout helpers

### Project Layout

```text
PyPacman/
├── AGENTS.md
├── CHANGELOG.md
├── README.md
├── pyproject.toml
├── PyPacman/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── colors.py
│   │   ├── config.py
│   │   ├── game_engine.py
│   │   ├── game_state.py
│   │   ├── maze.py
│   │   ├── scoring.py
│   │   ├── sprites.py
│   │   └── types.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── levels.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── ghost.py
│   │   ├── ghost_manager.py
│   │   └── pacman.py
│   └── ui/
│       ├── __init__.py
│       ├── display.py
│       └── input_handler.py
└── tests/
    ├── test_display.py
    ├── test_game_engine.py
    ├── test_game_state.py
    ├── test_ghost.py
    ├── test_input_handler.py
    ├── test_maze.py
    ├── test_pacman.py
    └── test_scoring.py
```

## Notes

- The runtime stays dependency-free; `pytest`, `pytest-cov`, and `mypy` are development extras only.
- The current package supports `python -m PyPacman.main`; there is no `PyPacman/__main__.py` entrypoint at the moment.

## License

MIT License.
