#!/usr/bin/env python
"""Test rendering to see current issues."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.display import MockDisplay
from src.game_engine import GameEngine
from src.constants import GameState

def test_quit_confirm():
    """Test the quit confirmation dialog."""
    display = MockDisplay()
    engine = GameEngine(display=display)
    engine.state = GameState.QUIT_CONFIRM
    engine.render()
    
    print("Quit Confirmation Dialog:")
    print("-" * 50)
    for row in display.get_last_frame():
        print(row)
    print("-" * 50)
    print()

def test_maze_render():
    """Test the maze rendering."""
    display = MockDisplay()
    engine = GameEngine(display=display)
    engine.state = GameState.PLAYING
    engine.render()
    
    print("Game with Maze:")
    print("-" * 50)
    for row in display.get_last_frame():
        print(row)
    print("-" * 50)

if __name__ == "__main__":
    test_quit_confirm()
    test_maze_render()
