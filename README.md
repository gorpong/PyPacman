# ASCII Pac-Man 🎮

A fully-featured terminal-based ASCII version of the classic Pac-Man arcade game, implemented in pure Python with no external dependencies.

## Features ✨

- **Complete Pac-Man Experience**: Four ghosts with distinct AI personalities (Blinky, Pinky, Inky, Clyde)
- **Dual Control Schemes**: Arrow keys ↑↓←→ OR WASD for left-handed players  
- **Full Game Mechanics**: Dots, power pellets, ghost vulnerability, progressive scoring (200→400→800→1600)
- **Professional Package**: Installable via pip with console commands
- **Terminal Optimized**: 80x24 terminals with automatic centering for larger displays
- **Pure Python**: No external dependencies, uses only Python standard library
- **Cross-Platform**: Linux, macOS, and Windows compatible

## Requirements 📋

- **Python**: 3.8+ (tested on 3.8-3.12)
- **Terminal**: 80x24 minimum with ASCII support  
- **Dependencies**: None (stdlib only)

## Installation 🚀

### From Source (Recommended for Development)
```bash
git clone <repository-url>
cd ascii-pacman
pip install -e .
```

### Running the Game
After installation, use either command:
```bash
ascii-pacman
# OR
pacman
```

### Development Mode
```bash
python -m ascii_pacman
```

## Game Mechanics 🎯

- **Scoring System**:
  - Dots: 10 points each
  - Power Pellets: 50 points each
  - Ghosts: 200→400→800→1600 points (progressive bonus)
- **Lives**: Start with 3 lives
- **Ghost AI**: Each ghost has unique behavior:
  - **Blinky (Red)**: Direct aggressive chaser
  - **Pinky (Pink)**: Ambusher (targets ahead of Pac-Man)
  - **Inky (Cyan)**: Complex patrol/ambush hybrid
  - **Clyde (Orange)**: Distance-based behavior

## Controls 🎮

- **Movement**: Arrow keys ↑↓←→ OR WASD keys
- **Pause**: SPACE bar
- **Quit**: Q key (shows confirmation dialog)
- **Menu**: SPACE or ENTER to select

## Development 🛠️

### Project Structure
```
ascii_pacman/
├── core/           # Game engine, maze, constants
├── entities/       # Pac-Man, ghosts, base classes  
├── ui/            # Display and input handling
├── data/          # Level definitions
└── main.py        # Entry point
```

### Running Tests
```bash
python -m pytest tests/
```

### Architecture
This project follows professional Python packaging standards and is ready for PyPI distribution. See `Claude.md` for detailed development documentation.

## Contributing 🤝

1. Check `Claude.md` for current development status
2. Review `docs/` directory for development history
3. Follow the established code patterns and type annotations
4. Ensure all tests pass before submitting changes

## License 📄

MIT License - Feel free to modify and distribute!

## Acknowledgments 🙏

Inspired by the original Pac-Man arcade game by Namco (1980). Built with modern Python best practices for educational and entertainment purposes.
