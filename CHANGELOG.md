# Changelog

All notable changes to ASCII Pac-Man are documented in this file.

## [Unreleased]

### Changed

- Refactored the old monolithic core constants module into focused modules:
  `core/config.py`, `core/colors.py`, `core/sprites.py`, and `core/types.py`
- Introduced protocol-based boundaries with `MazeProtocol`,
  `PacManProtocol`, and `GhostProtocol` to reduce concrete cross-module
  dependencies
- Centralized shared structural types such as `Position`, `Direction`,
  `GameMode`, and `CellType` in `core/types.py`
- Standardized much of the spatial API on `Position` objects instead of raw
  `(x, y)` tuples
- Replaced internal package-barrel imports with leaf-module imports in runtime
  code to further reduce circular import risk
- Consolidated packaging and tool configuration into `pyproject.toml`
- Raised the supported Python runtime to `3.11+`
- Expanded and updated the automated test suite to `112` tests
- Restored explicit directional key constants such as `Keys.UP` and
  `Keys.ESCAPE` for the input API

### Removed

- Removed `PyPacman/core/constants.py`
- Removed legacy packaging files `setup.py` and `requirements.txt`

### Notes

- The protocol/type refactor is intended as an architectural cleanup; gameplay
  behavior remains the same

## [1.0.0] - 2025-10-30

### Added

- Complete classic Pac-Man gameplay loop in an ASCII terminal interface
- Four ghosts with distinct personalities:
  Blinky, Pinky, Inky, and Clyde
- Dot and power pellet collection
- Progressive ghost scoring: `200 / 400 / 800 / 1600`
- Lives system, respawning, and level progression
- High score persistence with top-10 leaderboard and player names
- Score popups, death pause effect, and scrolling high scores on the menu
- Arrow-key and `W/A/S/D` controls
- Pause, quit confirmation, and game-over flows
- Pure-stdlib runtime with package structure split across `core`, `entities`,
  `ui`, and `data`
- Initial automated test suite with `84` tests
