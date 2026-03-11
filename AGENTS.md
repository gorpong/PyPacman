# AGENTS.md

Instructions for AI coding agents working in this repo.
If any instructions conflicts with a user request, ask before proceeding.

## Project summary

- This is a terminal-based ASCII version of the classic Pac-Man arcade game, implemented in Python 3.12.4+
- Primary goal: Playable and fun, but not a full commercial product
- Non-Goals: no in-game purchases

## Target Specifications

- **Terminal Size**: Optimized for 80x24 terminals, with automatic centering for larger displays
- **Controls**:
  - Arrow keys (↑↓←→) for standard users
  - WASD keys for left-handed users
  - ESC to quit, SPACE to pause
- **Python Version**: 3.12.4 or better
- **Dependencies**: Minimal - using only Python standard library

## Technical Architecture

### Core Design Patterns

- **Game Loop**: Traditional game loop with fixed timestep
- **State Machine**: Clean separation of game states
- **Component System**: Modular design for easy testing and maintenance
- **Observer Pattern**: For score updates and game events

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

## Current Status

### **🎉 VERSION 1.0 RELEASED 🎉**

All development phases complete. The game is feature-complete, tested, and ready for use.

### Completed Phases

✅ **Phase 1: Foundation and Game Engine** - Complete
✅ **Phase 2: Maze and World** - Complete
✅ **Phase 3: Pac-Man Character** - Complete
✅ **Phase 4: Ghost AI** - Complete
✅ **Refactoring: Package Structure** - Complete
✅ **Phase 5: Game Logic and Polish** - Complete
✅ **Phase 6: Final Integration and Testing** - Complete

### Version 1.0 Features

- ✅ Complete classic Pac-Man gameplay
- ✅ Four ghosts with unique AI personalities
- ✅ Progressive scoring system (200/400/800/1600)
- ✅ Lives system with death/respawn mechanics
- ✅ Level progression with difficulty scaling
- ✅ High score persistence (top 10 with names)
- ✅ Visual effects (score popups, animations)
- ✅ Scrolling high scores on splash screen
- ✅ Dual control schemes (arrows + WASD)
- ✅ 84 comprehensive tests, all passing
- ✅ PyPI-ready package structure

**Current Branch**: `master`
**Version**: 1.0
**Status**: Released and ready for distribution
**Tests**: 84/84 passing ✅

## Documentation Maintenance 📚

**IMPORTANT**: Always keep README.md and AGENTS.md files up to date when making changes that affect:

- Installation instructions
- Usage/commands  
- Feature descriptions
- Project structure
- Development status
- Architecture changes

This ensures new contributors and users always have current information.
