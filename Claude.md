# ASCII Pac-Man Development Plan

## Project Overview
This is a terminal-based ASCII version of the classic Pac-Man arcade game, implemented in Python 3.12.4+. The game features traditional gameplay with both standard arrow key controls and left-handed alternatives (WASD).

## Target Specifications
- **Terminal Size**: Optimized for 80x24 terminals, with automatic centering for larger displays
- **Controls**: 
  - Arrow keys (↑↓←→) for standard users
  - WASD keys for left-handed users
  - ESC to quit, SPACE to pause
- **Python Version**: 3.12.4 or better
- **Dependencies**: Minimal - using only Python standard library

## Development Phases

### Phase 1: Foundation and Game Engine (branch: `phase-1-foundation`)
**Deliverables:**
- Basic game loop and terminal management
- Screen rendering system with centering
- Input handling for both control schemes
- Basic game state management (playing, paused, game over)
- Unit tests for core engine components

**Key Components:**
- `game_engine.py` - Main game loop and state management
- `display.py` - Terminal display and rendering
- `input_handler.py` - Keyboard input processing
- `constants.py` - Game constants and configuration

### Phase 2: Maze and World (branch: `phase-2-maze`)
**Deliverables:**
- Maze layout system with ASCII art
- Wall collision detection
- Dot/pellet placement and collection
- Power pellet mechanics
- Maze renderer with proper ASCII characters

**Key Components:**
- `maze.py` - Maze data structure and collision detection
- `level_data.py` - Maze layouts and configurations
- Enhanced display system for maze rendering

### Phase 3: Pac-Man Character (branch: `phase-3-pacman`)
**Deliverables:**
- Pac-Man character with position and movement
- Direction-based sprite changes (>, <, ^, v)
- Smooth movement within the grid system
- Mouth animation (opening/closing effect)
- Dot consumption and scoring

**Key Components:**
- `pacman.py` - Pac-Man character class
- `sprite.py` - ASCII sprite management
- Score tracking system

### Phase 4: Ghost AI (branch: `phase-4-ghosts`)
**Deliverables:**
- Four ghosts with different AI behaviors
- Ghost house and release mechanics
- Scatter and chase mode AI
- Vulnerable (blue) state after power pellets
- Ghost-Pac-Man collision detection

**Key Components:**
- `ghost.py` - Base ghost class and AI
- `ai_behaviors.py` - Different ghost personality algorithms
- Enhanced collision system

### Phase 5: Game Logic and Polish (branch: `phase-5-gameplay`)
**Deliverables:**
- Complete scoring system
- Lives and game over conditions
- Level progression
- Sound effects (ASCII-based visual cues)
- High score tracking
- Game balance and difficulty scaling

**Key Components:**
- `scoring.py` - Score calculation and tracking
- `game_state.py` - Lives, levels, and progression
- `effects.py` - Visual effects and feedback

### Phase 6: Final Integration and Testing (branch: `phase-6-final`)
**Deliverables:**
- Complete integration testing
- Performance optimization
- Cross-platform compatibility testing
- Documentation and README
- Final polish and bug fixes

## Technical Architecture

### Core Design Patterns
- **Game Loop**: Traditional game loop with fixed timestep
- **State Machine**: Clean separation of game states
- **Component System**: Modular design for easy testing and maintenance
- **Observer Pattern**: For score updates and game events

### File Structure
```
ascii-pacman/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── game_engine.py       # Core game loop
│   ├── display.py           # Terminal rendering
│   ├── input_handler.py     # Input processing
│   ├── maze.py              # Maze logic
│   ├── pacman.py            # Player character
│   ├── ghost.py             # Ghost AI
│   ├── constants.py         # Game constants
│   └── utils.py             # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_game_engine.py
│   ├── test_maze.py
│   ├── test_pacman.py
│   └── test_ghosts.py
├── data/
│   └── levels.py            # Level data
├── requirements.txt
├── README.md
├── Claude.md               # This file
└── .gitignore
```

### Testing Strategy
- **Unit Tests**: pytest for all core components
- **Integration Tests**: Game loop and component interaction
- **Manual Tests**: Gameplay testing and user experience
- **Continuous Integration**: Each phase must pass all tests before merging

### Branch Strategy and Git Workflow
1. **Phase Branches**: Each phase gets its own feature branch (e.g., `phase-2-maze`, `phase-3-pacman`)
2. **Development Process**: 
   - Work on features in phase branches
   - Commit frequently with descriptive messages
   - All tests must pass before declaring phase complete
   - **Do NOT merge to main until explicit approval**
3. **Code Review Process**:
   - Phase must be tested and reviewed before merge approval
   - Maintainer will give explicit go-ahead to merge
   - Only then merge phase branch to main and create next phase branch
4. **Main Branch**: Always represents a stable, working game state
5. **Commit Standards**:
   - Descriptive commit messages
   - Atomic commits for specific features
   - Clean history before merging

## Success Criteria
- [ ] Game runs smoothly in 80x24 terminal
- [ ] Both control schemes work perfectly
- [ ] Classic Pac-Man gameplay experience
- [ ] No external dependencies beyond Python stdlib
- [ ] Comprehensive test coverage (>80%)
- [ ] Clean, maintainable code architecture
- [ ] Cross-platform compatibility (Linux, macOS, Windows)

## Development Timeline
Each phase is estimated to be completed in sequence, with the foundation being the most critical for establishing the architecture that all subsequent phases will build upon.

## Current Status
**Phase 4: Ghost AI - IN PROGRESS**
Phase 2 (Maze and World) and Phase 3 (Pac-Man Character) have been completed and merged to master.

### Completed Phases:
✅ **Phase 1: Foundation and Game Engine** - Complete
✅ **Phase 2: Maze and World** - Complete  
✅ **Phase 3: Pac-Man Character** - Complete

### Phase 2 & 3 Achievements:
✅ **Arrow Key Detection** - Fixed input handler for responsive controls
✅ **Constants Refactoring** - Centralized all display constants
✅ **Maze System** - 74x20 properly connected maze with 470 dots + 4 pellets
✅ **Pac-Man Implementation** - Full character with movement, animation, collision
✅ **Dot Collection** - Working scoring system with proper mechanics
✅ **Game States** - Menu, playing, paused, quit confirmation all working
✅ **Comprehensive Testing** - 52 tests passing

### Phase 4: Ghost AI - COMPLETED ✅
Fully implemented four-ghost AI system with classic Pac-Man behaviors:
- ✅ **Basic Ghost class** - Movement, rendering, state management  
- ✅ **Ghost house mechanics** - Timed release sequence (0s, 2s, 5s, 8s)
- ✅ **Individual AI personalities**:
  - **Blinky (Red)**: Direct aggressive chaser
  - **Pinky (Pink)**: Ambusher (targets 4 spaces ahead)  
  - **Inky (Cyan)**: Complex targeting (patrol/ambush hybrid)
  - **Clyde (Orange)**: Distance-based behavior (chase when far, scatter when close)
- ✅ **Mode switching** - Scatter/Chase alternating with proper timings
- ✅ **Power pellet vulnerability** - 8-second vulnerable state with visual changes
- ✅ **Collision detection** - Ghost-Pac-Man interactions
- ✅ **Complete mechanics** - Death, respawn, ghost eating with progressive scoring
- ✅ **Comprehensive testing** - 63 tests passing including ghost AI suite

**Status**: Phase 4 complete, ready for Phase 5 (Game Logic and Polish)
**Current Branch**: `phase-4-ghosts`
