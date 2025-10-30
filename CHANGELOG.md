# Changelog

All notable changes to ASCII Pac-Man will be documented in this file.

## [1.0.0] - 2024

### 🎉 Initial Release

Complete implementation of classic Pac-Man gameplay in ASCII terminal format.

### Added

#### Core Gameplay
- Classic Pac-Man maze navigation and gameplay
- 470 dots and 4 power pellets to collect
- Level completion and progression
- Game states: Menu, Playing, Paused, Game Over

#### Characters
- Pac-Man character with directional sprites and mouth animation
- Four ghosts with unique AI personalities:
  - **Blinky (Red)**: Direct aggressive chaser
  - **Pinky (Pink)**: Ambusher targeting ahead of Pac-Man
  - **Inky (Cyan)**: Complex patrol/ambush hybrid
  - **Clyde (Orange)**: Distance-based behavior switcher
- Ghost house with timed release mechanics
- Scatter/Chase mode alternation
- Vulnerability system after power pellets

#### Scoring & Progression
- Dot collection: 10 points each
- Power pellets: 50 points each
- Progressive ghost scoring: 200, 400, 800, 1600 points
- High score persistence to ~/.ascii_pacman_scores.json
- Top 10 leaderboard with player names
- Lives system (3 lives)
- Level progression with difficulty scaling

#### Visual & UI
- 74x20 character maze display
- Auto-centering for terminals larger than 80x24
- Score, high score, lives, and level HUD
- Visual score popups for pellets and ghosts
- Death animation with pause effect
- High score entry screen with blinking cursor
- Scrolling high scores on splash screen (after 10s idle)
- Game over screen with leaderboard

#### Controls
- Arrow keys for movement
- WASD alternative controls
- SPACE to pause/start
- Q or ESC to quit
- Quit confirmation dialog

#### Technical
- Pure Python implementation (stdlib only)
- Clean package structure (core/, entities/, ui/, data/)
- Console entry points: `ascii-pacman` and `pacman`
- Comprehensive test suite (84 tests)
- Cross-platform support (Linux, macOS, Windows)
- Position-based entity system
- MovableEntity base class for code reuse

### Development Timeline
- Phase 1: Foundation and Game Engine
- Phase 2: Maze and World
- Phase 3: Pac-Man Character
- Phase 4: Ghost AI
- Refactoring: Package Structure
- Phase 5: Game Logic and Polish
- Phase 6: Final Integration and Testing

### Testing
- 84 comprehensive unit tests
- Coverage of all major systems
- Integration testing via unit test suite
- All tests passing

---

## Future Considerations

Potential enhancements for future versions:
- Additional maze layouts
- Bonus fruit items
- Enhanced sound effects (visual cues)
- Level completion animations
- More ghost AI variations
- Configurable difficulty settings
