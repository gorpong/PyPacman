"""
Tests for maze functionality.
"""

import unittest
from PyPacman.core.maze import Maze, Cell


class TestMaze(unittest.TestCase):
    """Test maze functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Simple test maze with all features
        # Note: P is the spawn point (empty), dots are marked with .
        self.test_layout = [
            "##########",
            "#O......O#",
            "#.##--##.#",
            "#.#GGGG#.#",
            "#.#GGGG#.#",
            "#.######.#",
            "#...P....#",
            "#........#",
            "##########",
        ]
        self.maze = Maze(self.test_layout)
    
    def test_maze_dimensions(self):
        """Test maze dimensions are correct."""
        self.assertEqual(self.maze.width, 10)
        self.assertEqual(self.maze.height, 9)
    
    def test_wall_detection(self):
        """Test wall detection."""
        # Corners should be walls
        self.assertTrue(self.maze.is_wall(0, 0))
        self.assertTrue(self.maze.is_wall(9, 0))
        self.assertTrue(self.maze.is_wall(0, 8))
        self.assertTrue(self.maze.is_wall(9, 8))
        
        # Center corridors should not be walls
        self.assertFalse(self.maze.is_wall(1, 1))
        self.assertFalse(self.maze.is_wall(5, 7))
    
    def test_valid_position(self):
        """Test position validation."""
        # Valid positions
        self.assertTrue(self.maze.is_valid_position(0, 0))
        self.assertTrue(self.maze.is_valid_position(9, 8))
        self.assertTrue(self.maze.is_valid_position(5, 4))
        
        # Invalid positions
        self.assertFalse(self.maze.is_valid_position(-1, 0))
        self.assertFalse(self.maze.is_valid_position(0, -1))
        self.assertFalse(self.maze.is_valid_position(10, 0))
        self.assertFalse(self.maze.is_valid_position(0, 9))
    
    def test_walkable_for_pacman(self):
        """Test walkable position detection for Pac-Man."""
        # Empty spaces and dots should be walkable
        self.assertTrue(self.maze.is_walkable_for_pacman(1, 1))
        self.assertTrue(self.maze.is_walkable_for_pacman(2, 1))
        
        # Spawn point (P) should be walkable
        self.assertTrue(self.maze.is_walkable_for_pacman(4, 6))
        
        # Walls should not be walkable
        self.assertFalse(self.maze.is_walkable_for_pacman(0, 0))
        
        # Ghost house should not be walkable for Pac-Man
        self.assertFalse(self.maze.is_walkable_for_pacman(4, 3))
        
        # Ghost door should not be walkable for Pac-Man
        self.assertFalse(self.maze.is_walkable_for_pacman(4, 2))
        
        # Out of bounds should not be walkable
        self.assertFalse(self.maze.is_walkable_for_pacman(-1, 0))
        self.assertFalse(self.maze.is_walkable_for_pacman(20, 20))
    
    def test_walkable_for_ghost(self):
        """Test walkable position detection for ghosts."""
        # Empty spaces should be walkable
        self.assertTrue(self.maze.is_walkable_for_ghost(1, 1))
        
        # Walls should not be walkable
        self.assertFalse(self.maze.is_walkable_for_ghost(0, 0))
        
        # Ghost house should be walkable for ghosts
        self.assertTrue(self.maze.is_walkable_for_ghost(4, 3))
        
        # Ghost door should be walkable for ghosts
        self.assertTrue(self.maze.is_walkable_for_ghost(4, 2))
    
    def test_dot_detection(self):
        """Test dot detection."""
        # Should have dots at these positions (marked with . in layout)
        self.assertTrue(self.maze.has_dot(2, 1))
        self.assertTrue(self.maze.has_dot(1, 6))  # Dot before P
        self.assertTrue(self.maze.has_dot(5, 7))  # Dot in bottom row
        
        # Should not have dots where there aren't any
        self.assertFalse(self.maze.has_dot(0, 0))  # Wall
        self.assertFalse(self.maze.has_dot(1, 1))  # Power pellet
        self.assertFalse(self.maze.has_dot(4, 6))  # Spawn point (P)
    
    def test_power_pellet_detection(self):
        """Test power pellet detection."""
        # Should have power pellets in corners
        self.assertTrue(self.maze.has_power_pellet(1, 1))
        self.assertTrue(self.maze.has_power_pellet(8, 1))
        
        # Should not have pellets where there aren't any
        self.assertFalse(self.maze.has_power_pellet(2, 1))  # Dot
        self.assertFalse(self.maze.has_power_pellet(0, 0))  # Wall
    
    def test_dot_collection(self):
        """Test dot collection."""
        # Should be able to collect dot
        self.assertTrue(self.maze.collect_dot(2, 1))
        
        # Should not have dot after collection
        self.assertFalse(self.maze.has_dot(2, 1))
        
        # Should not be able to collect same dot again
        self.assertFalse(self.maze.collect_dot(2, 1))
        
        # Should not be able to collect non-dot
        self.assertFalse(self.maze.collect_dot(0, 0))
    
    def test_power_pellet_collection(self):
        """Test power pellet collection."""
        # Should be able to collect pellet
        self.assertTrue(self.maze.collect_power_pellet(1, 1))
        
        # Should not have pellet after collection
        self.assertFalse(self.maze.has_power_pellet(1, 1))
        
        # Should not be able to collect same pellet again
        self.assertFalse(self.maze.collect_power_pellet(1, 1))
    
    def test_remaining_counts(self):
        """Test counting remaining items."""
        initial_dots = self.maze.get_remaining_dots()
        initial_pellets = self.maze.get_remaining_pellets()
        
        # Collect a dot
        self.maze.collect_dot(2, 1)
        self.assertEqual(self.maze.get_remaining_dots(), initial_dots - 1)
        
        # Collect a pellet
        self.maze.collect_power_pellet(1, 1)
        self.assertEqual(self.maze.get_remaining_pellets(), initial_pellets - 1)
    
    def test_level_completion(self):
        """Test level completion detection."""
        # Should not be complete initially
        self.assertFalse(self.maze.is_level_complete())
        
        # Collect all dots and pellets
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                self.maze.collect_dot(x, y)
                self.maze.collect_power_pellet(x, y)
        
        # Should be complete now
        self.assertTrue(self.maze.is_level_complete())
    
    def test_reset(self):
        """Test maze reset."""
        # Collect some items
        self.maze.collect_dot(2, 1)
        self.maze.collect_power_pellet(1, 1)
        
        # Reset maze
        self.maze.reset()
        
        # Items should be available again
        self.assertTrue(self.maze.has_dot(2, 1))
        self.assertTrue(self.maze.has_power_pellet(1, 1))
        self.assertEqual(self.maze.get_remaining_dots(), self.maze.total_dots)
        self.assertEqual(self.maze.get_remaining_pellets(), self.maze.total_pellets)
    
    def test_ghost_house_detection(self):
        """Test ghost house detection."""
        # Should detect ghost house interior
        self.assertTrue(self.maze.is_ghost_house(4, 3))
        self.assertTrue(self.maze.is_ghost_house(5, 3))
        
        # Should not detect ghost house elsewhere
        self.assertFalse(self.maze.is_ghost_house(1, 1))
    
    def test_ghost_door_detection(self):
        """Test ghost door detection."""
        # Should detect ghost door
        self.assertTrue(self.maze.is_ghost_door(4, 2))
        self.assertTrue(self.maze.is_ghost_door(5, 2))
        
        # Should not detect door elsewhere
        self.assertFalse(self.maze.is_ghost_door(1, 1))
        self.assertFalse(self.maze.is_ghost_door(4, 3))  # Ghost house, not door
    
    def test_pacman_spawn_point(self):
        """Test Pac-Man spawn point detection."""
        spawn = self.maze.get_pacman_spawn()
        self.assertEqual(spawn, (4, 6))
    
    def test_ghost_spawn_positions(self):
        """Test ghost spawn positions."""
        spawns = self.maze.get_ghost_spawn_positions()
        # Should have 8 ghost positions from the GGGG x 2 rows in layout
        self.assertEqual(len(spawns), 8)
        # All should be in the ghost house area
        for x, y in spawns:
            self.assertTrue(self.maze.is_ghost_house(x, y))
    
    def test_get_cell_char(self):
        """Test getting display character for cells."""
        # Wall
        self.assertEqual(self.maze.get_cell_char(0, 0), '█')
        
        # Dot
        self.assertEqual(self.maze.get_cell_char(2, 1), '·')
        
        # Power pellet
        self.assertEqual(self.maze.get_cell_char(1, 1), '●')
        
        # Ghost door
        self.assertEqual(self.maze.get_cell_char(4, 2), '─')
        
        # After collecting dot, should be empty
        self.maze.collect_dot(2, 1)
        self.assertEqual(self.maze.get_cell_char(2, 1), ' ')
    
    def test_empty_maze(self):
        """Test handling of empty maze."""
        empty_maze = Maze([])
        self.assertEqual(empty_maze.width, 0)
        self.assertEqual(empty_maze.height, 0)
        self.assertFalse(empty_maze.is_valid_position(0, 0))
    
    def test_default_spawn_when_no_marker(self):
        """Test default spawn point when P marker is missing."""
        simple_layout = [
            "#####",
            "#...#",
            "#####",
        ]
        maze = Maze(simple_layout)
        spawn = maze.get_pacman_spawn()
        # Should default to center-ish position
        self.assertIsNotNone(spawn)
        self.assertEqual(len(spawn), 2)
    
    def test_ghost_door_position(self):
        """Test getting ghost door position."""
        door_pos = self.maze.get_ghost_door_position()
        self.assertIsNotNone(door_pos)
        # Should be at the center of the door cells (row 2)
        self.assertEqual(door_pos[1], 2)


class TestMazeBackwardsCompatibility(unittest.TestCase):
    """Test that old maze features still work (backwards compatibility)."""
    
    def test_old_style_walkable(self):
        """Test that is_walkable still works with is_ghost parameter."""
        layout = [
            "#####",
            "#...#",
            "#####",
        ]
        maze = Maze(layout)
        # Default should be Pac-Man walkability (is_ghost=False)
        self.assertTrue(maze.is_walkable(1, 1))
        self.assertFalse(maze.is_walkable(0, 0))
    
    def test_walkable_with_ghost_parameter(self):
        """Test is_walkable with explicit is_ghost parameter."""
        layout = [
            "#####",
            "#-G-#",
            "#####",
        ]
        maze = Maze(layout)
        # Ghost door not walkable for Pac-Man
        self.assertFalse(maze.is_walkable(1, 1, is_ghost=False))
        # Ghost door walkable for ghosts
        self.assertTrue(maze.is_walkable(1, 1, is_ghost=True))


if __name__ == '__main__':
    unittest.main()
