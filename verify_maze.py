#!/usr/bin/env python
"""Verify maze connectivity - ensure all dots are reachable."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.maze import Maze
from data.levels import get_level
from collections import deque

def flood_fill_reachable(maze, start_x, start_y):
    """Use flood fill to find all reachable positions."""
    reachable = set()
    queue = deque([(start_x, start_y)])
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) in reachable:
            continue
            
        if not maze.is_walkable(x, y):
            continue
            
        reachable.add((x, y))
        
        # Check all 4 directions
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_x, next_y = x + dx, y + dy
            if (next_x, next_y) not in reachable:
                queue.append((next_x, next_y))
    
    return reachable

def verify_maze_connectivity():
    """Verify that all dots and pellets are reachable."""
    layout = get_level(1)
    maze = Maze(layout)
    
    # Find a starting position (any walkable position)
    start_x = start_y = None
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.is_walkable(x, y):
                start_x, start_y = x, y
                break
        if start_x is not None:
            break
    
    if start_x is None:
        print("❌ No walkable positions found in maze!")
        return False
    
    print(f"Starting flood fill from ({start_x}, {start_y})")
    reachable = flood_fill_reachable(maze, start_x, start_y)
    
    # Check all dots
    unreachable_dots = []
    for dot_pos in maze.dots:
        if dot_pos not in reachable:
            unreachable_dots.append(dot_pos)
    
    # Check all pellets
    unreachable_pellets = []
    for pellet_pos in maze.power_pellets:
        if pellet_pos not in reachable:
            unreachable_pellets.append(pellet_pos)
    
    print(f"Total walkable positions: {len(reachable)}")
    print(f"Total dots: {len(maze.dots)}")
    print(f"Total pellets: {len(maze.power_pellets)}")
    print(f"Unreachable dots: {len(unreachable_dots)}")
    print(f"Unreachable pellets: {len(unreachable_pellets)}")
    
    if unreachable_dots:
        print("❌ Unreachable dot positions:")
        for pos in unreachable_dots[:10]:  # Show first 10
            print(f"  {pos}")
        if len(unreachable_dots) > 10:
            print(f"  ... and {len(unreachable_dots) - 10} more")
        return False
    
    if unreachable_pellets:
        print("❌ Unreachable pellet positions:")
        for pos in unreachable_pellets:
            print(f"  {pos}")
        return False
    
    print("✅ All dots and pellets are reachable!")
    return True

if __name__ == "__main__":
    verify_maze_connectivity()
