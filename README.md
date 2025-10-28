# ASCII Pac-Man

A classic terminal-based ASCII version of Pac-Man, bringing the arcade experience to your command line!

## Features

- **Classic Gameplay**: Navigate through mazes, collect dots, avoid ghosts
- **Dual Control Schemes**: 
  - Arrow keys (↑↓←→) for traditional users
  - WASD for left-handed players
- **Terminal Optimized**: Works great in 80x24 terminals, auto-centers on larger displays
- **Pure Python**: No external dependencies, uses only Python standard library
- **Cross-Platform**: Runs on Linux, macOS, and Windows

## Requirements

- Python 3.12.4 or higher
- Terminal with ASCII support

## Installation

```bash
git clone <repository-url>
cd ascii-pacman
python src/main.py
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

## Development

This project is developed in phases. See `Claude.md` for detailed development planning and architecture.

### Running Tests

```bash
python -m pytest tests/
```

## License

MIT License - Feel free to modify and share!

## Acknowledgments

Inspired by the original Pac-Man arcade game by Namco (1980).
