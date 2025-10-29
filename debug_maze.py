#!/usr/bin/env python
"""Debug maze and Pac-Man position."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.maze import Maze
from data.levels import get_level

def debug_maze():
    """Debug the maze layout."""
    layout = get_level(1)
    maze = Maze(layout)
    
    print("Maze dimensions:", maze.width, "x", maze.height)
    print("\nMaze layout with coordinates:")
    print("   ", end="")
    for x in range(0, min(maze.width, 50), 5):
        print(f"{x:5}", end="")
    print()
    
    for y in range(maze.height):
        print(f"{y:2}: ", end="")
        for x in range(min(maze.width, 50)):
            char = layout[y][x] if x < len(layout[y]) else ' '
            print(char, end="")
        print()
    
    # Find good starting position
    print("\nFinding good starting position...")
    start_x = maze.width // 2
    start_y = maze.height - 3
    
    print(f"Initial attempt: ({start_x}, {start_y})")
    for y in range(start_y, 0, -1):
        if maze.is_walkable(start_x, y):
            print(f"Found walkable position: ({start_x}, {y})")
            char = layout[y][start_x] if start_x < len(layout[y]) else ' '
            print(f"Character at position: '{char}'")
            print(f"Has dot: {maze.has_dot(start_x, y)}")
            print(f"Has pellet: {maze.has_power_pellet(start_x, y)}")
            break
    
    # Check some positions with dots
    print("\nPositions with dots:")
    count = 0
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.has_dot(x, y):
                print(f"  ({x}, {y})")
                count += 1
                if count >= 10:
                    print("  ... and more")
                    return
                    
if __name__ == "__main__":
    debug_maze()
