#!/usr/bin/env python
"""Test Pac-Man movement and dot collection."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.display import MockDisplay
from src.game_engine import GameEngine
from src.constants import GameState
from src.input_handler import MockInputHandler

def test_movement_and_dots():
    """Test Pac-Man movement and dot collection."""
    display = MockDisplay()
    input_handler = MockInputHandler()
    engine = GameEngine(display=display, input_handler=input_handler)
    engine.state = GameState.PLAYING
    
    print("Initial state:")
    print(f"  Pac-Man position: {engine.pacman.get_position()}")
    print(f"  Score: {engine.score}")
    print(f"  Dots remaining: {engine.maze.get_remaining_dots()}")
    
    # Simulate some movement
    print("\nSimulating movement (left)...")
    input_handler.add_key('a')  # Move left
    
    # Run several update cycles
    for i in range(5):
        engine.update(0.15)  # 150ms per frame
        
    print(f"  New position: {engine.pacman.get_position()}")
    print(f"  Score: {engine.score}")
    print(f"  Dots remaining: {engine.maze.get_remaining_dots()}")
    
    # Try moving up
    print("\nSimulating movement (up)...")
    input_handler.add_key('w')  # Move up
    
    for i in range(10):
        engine.update(0.15)
        
    print(f"  New position: {engine.pacman.get_position()}")
    print(f"  Score: {engine.score}")
    print(f"  Dots remaining: {engine.maze.get_remaining_dots()}")
    
    # Check if dots are being collected
    initial_dots = engine.maze.get_remaining_dots()
    
    # Move around to collect dots
    print("\nCollecting dots...")
    movements = ['a', 'a', 'w', 'w', 'd', 'd', 's', 's']
    for key in movements:
        input_handler.add_key(key)
        for i in range(3):
            engine.update(0.15)
            
    final_dots = engine.maze.get_remaining_dots()
    dots_collected = initial_dots - final_dots
    
    print(f"  Final position: {engine.pacman.get_position()}")
    print(f"  Final score: {engine.score}")
    print(f"  Dots collected: {dots_collected}")
    print(f"  Dots remaining: {final_dots}")
    
    if dots_collected > 0:
        print("✓ Dot collection is working!")
    else:
        print("✗ No dots were collected")

if __name__ == "__main__":
    test_movement_and_dots()
