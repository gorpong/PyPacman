#!/usr/bin/env python
"""Test full game rendering with Pac-Man."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.display import MockDisplay
from src.game_engine import GameEngine
from src.constants import GameState
from src.input_handler import MockInputHandler

def test_full_game():
    """Test full game rendering."""
    display = MockDisplay()
    input_handler = MockInputHandler()
    engine = GameEngine(display=display, input_handler=input_handler)
    
    # Show menu first
    engine.state = GameState.MENU
    engine.render()
    print("MENU SCREEN:")
    print("=" * 80)
    for row in display.get_last_frame():
        print(row)
    print()
    
    # Start game
    input_handler.add_key(' ')
    engine.update(0.1)
    
    # Move Pac-Man a bit
    input_handler.add_key('w')  # up
    for i in range(5):
        engine.update(0.15)
    
    engine.render()
    print("IN-GAME (after moving up):")
    print("=" * 80)
    for row in display.get_last_frame()[:15]:  # Show top portion
        print(row)
    print("...")
    
    # Test pause
    input_handler.add_key(' ')
    engine.update(0.1)
    engine.render()
    
    print("\nPAUSED SCREEN:")
    print("=" * 80) 
    for row in display.get_last_frame()[8:16]:  # Show center portion
        print(row)
    print()
    
    print(f"Game Stats:")
    print(f"  Score: {engine.score}")
    print(f"  Lives: {engine.lives}")
    print(f"  Level: {engine.level}")
    print(f"  Pac-Man position: {engine.pacman.get_position() if engine.pacman else 'N/A'}")
    print(f"  Dots remaining: {engine.maze.get_remaining_dots() if engine.maze else 'N/A'}")

if __name__ == "__main__":
    test_full_game()
