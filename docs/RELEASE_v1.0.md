# ASCII Pac-Man v1.0 - Release Notes

## 🎉 Version 1.0 - Initial Release

We're excited to announce the first full release of ASCII Pac-Man! This is a complete, feature-rich implementation of the classic arcade game in pure Python for the terminal.

## What's Included

### Complete Gameplay
- Full Pac-Man experience in ASCII/terminal format
- 74x20 character maze with 470 dots and 4 power pellets
- Level completion and progression system
- Lives system (3 lives) with respawn mechanics
- Progressive difficulty scaling

### Ghost AI
Four ghosts with authentic behaviors from the original game:
- **Blinky (Red)**: Aggressive direct pursuit
- **Pinky (Pink)**: Ambushes by targeting ahead of Pac-Man
- **Inky (Cyan)**: Complex targeting using both Blinky and Pac-Man positions
- **Clyde (Orange)**: Switches between chase and scatter based on distance

### Scoring System
- Dots: 10 points
- Power Pellets: 50 points
- Ghosts: 200, 400, 800, 1600 (progressive combo)
- High score persistence with top 10 leaderboard
- Player name entry for high scores

### Visual Polish
- Score popups when collecting items
- Death animation with pause
- Scrolling high scores on splash screen
- Clean HUD with score, high score, lives, and level
- Smooth animations and transitions

### Controls
- **Movement**: Arrow keys or WASD
- **Pause**: SPACE
- **Quit**: Q or ESC
- **Start**: SPACE from menu

## Installation

```bash
pip install -e .
```

## Running the Game

After installation:
```bash
ascii-pacman
```
or
```bash
pacman
```

## System Requirements

- Python 3.8 or higher
- Terminal with 80x24 minimum size
- ANSI color support (most modern terminals)
- Works on Linux, macOS, and Windows

## Technical Details

- **Lines of Code**: ~2,500
- **Test Coverage**: 84 comprehensive tests
- **Dependencies**: None (pure Python stdlib)
- **Package Structure**: Professional, PyPI-ready
- **Architecture**: Clean separation of concerns (core/entities/ui/data)

## Development History

This project was developed through 6 phases plus a refactoring stage:
1. Foundation and Game Engine
2. Maze and World
3. Pac-Man Character
4. Ghost AI
5. Game Logic and Polish
6. Final Integration and Testing

Each phase was completed with comprehensive testing before merging to master.

## Known Limitations

- Single maze layout
- No bonus fruit items
- Visual effects only (no sound)
- Terminal-based graphics

## Future Enhancements

Potential additions for future versions:
- Multiple maze layouts
- Bonus fruit scoring
- More visual effect variations
- Level completion celebrations
- Configurable game settings

## Credits

Developed as a faithful ASCII recreation of the classic Pac-Man arcade game.

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please see the README.md file.

---

**Enjoy the game! 🎮👻**
