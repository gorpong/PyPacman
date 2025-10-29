#!/usr/bin/env python
"""Test Pac-Man rendering and movement."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.display import MockDisplay
from src.game_engine import GameEngine
from src.constants import GameState, Direction
from src.input_handler import MockInputHandler

def test_pacman_in_maze():
    """Test Pac-Man rendering in the maze."""
    display = MockDisplay()
    input_handler = MockInputHandler()
    engine = GameEngine(display=display, input_handler=input_handler)
    engine.state = GameState.PLAYING
    
    # Move Pac-Man up a bit for visibility
    if engine.pacman:
        engine.pacman.y -= 2
    
    engine.render()
    
    print("Game with Pac-Man:")
    print("-" * 50)
    for i, row in enumerate(display.get_last_frame()):
        print(f"{i:2}: {row}")
    print("-" * 50)
    
    # Check if Pac-Man sprite appears
    frame_str = '\n'.join(display.get_last_frame())
    if '>' in frame_str or '<' in frame_str or '^' in frame_str or 'v' in frame_str or 'C' in frame_str:
        print("✓ Pac-Man sprite found in display")
    else:
        print("✗ Pac-Man sprite not found")
        
    print(f"Pac-Man position: {engine.pacman.get_position() if engine.pacman else 'None'}")
    print(f"Score: {engine.score}")
    print(f"Dots remaining: {engine.maze.get_remaining_dots() if engine.maze else 'N/A'}")

if __name__ == "__main__":
    test_pacman_in_maze()
