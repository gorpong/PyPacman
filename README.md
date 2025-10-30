# ASCII Pac-Man

A classic terminal-based ASCII version of Pac-Man, bringing the arcade experience to your command line!

## Features

- 🎮 **Classic Gameplay**: Navigate through mazes, collect dots, avoid ghosts
- 👻 **Four Unique Ghosts**: Each with distinct AI personalities (Blinky, Pinky, Inky, Clyde)
- 🎯 **Power Pellets**: Turn vulnerable ghosts blue and eat them for bonus points!
- 🎨 **ASCII Graphics**: Beautiful terminal-based visuals using Unicode characters
- 🎮 **Dual Control Schemes**: 
  - Arrow keys (↑↓←→) for traditional users
  - WASD for left-handed players
- 📊 **Score System**: Progressive scoring with ghost combo multipliers
- ❤️ **Multiple Lives**: Start with 3 lives
- 🖥️ **Terminal Optimized**: Works great in 80x24 terminals, auto-centers on larger displays
- 🐍 **Pure Python**: No external dependencies, uses only Python standard library
- 🌍 **Cross-Platform**: Runs on Linux, macOS, and Windows

## Requirements

- Python 3.8+ (tested on 3.8, 3.9, 3.10, 3.11, 3.12)
- Terminal with 80x24 character display minimum
- Terminal with ANSI color support (most modern terminals)

## Installation

### From Source (Development)

```bash
git clone https://github.com/yourusername/ascii-pacman.git
cd ascii-pacman
pip install -e .
```

### Quick Start (No Installation)

```bash
git clone https://github.com/yourusername/ascii-pacman.git
cd ascii-pacman
python -m ascii_pacman
```

## Usage

After installation, you can run the game using either command:

```bash
pacman
# or
ascii-pacman
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
ascii_pacman/
├── core/        # Core game engine and maze logic
├── entities/    # Game entities (Pac-Man, ghosts)
├── ui/          # Display and input handling
└── data/        # Level definitions
```

See `Claude.md` for detailed development planning and architecture.

### Running Tests

```bash
python -m pytest tests/
```

### Building for Distribution

```bash
python -m build
```

## Project Status

The game is feature-complete with all core mechanics implemented:
- ✅ Phase 1: Foundation and Game Engine
- ✅ Phase 2: Maze and World
- ✅ Phase 3: Pac-Man Character
- ✅ Phase 4: Ghost AI
- ✅ Refactoring: Package structure and code organization
- 🚧 Phase 5: Game Logic and Polish (upcoming)

## License

MIT License - Feel free to modify and share!

## Acknowledgments

Inspired by the original Pac-Man arcade game by Namco (1980).
