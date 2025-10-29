"""
Tests for maze functionality.
"""

import unittest
from src.maze import Maze, Cell


class TestMaze(unittest.TestCase):
    """Test maze functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Simple test maze
        self.test_layout = [
            "########",
            "#.....o#",
            "#.###..#",
            "#....G.#",
            "########",
        ]
        self.maze = Maze(self.test_layout)
    
    def test_maze_dimensions(self):
        """Test maze dimensions are correct."""
        self.assertEqual(self.maze.width, 8)
        self.assertEqual(self.maze.height, 5)
    
    def test_wall_detection(self):
        """Test wall detection."""
        # Corners should be walls
        self.assertTrue(self.maze.is_wall(0, 0))
        self.assertTrue(self.maze.is_wall(7, 0))
        self.assertTrue(self.maze.is_wall(0, 4))
        self.assertTrue(self.maze.is_wall(7, 4))
        
        # Center should not be wall
        self.assertFalse(self.maze.is_wall(1, 1))
        self.assertFalse(self.maze.is_wall(5, 1))
    
    def test_valid_position(self):
        """Test position validation."""
        # Valid positions
        self.assertTrue(self.maze.is_valid_position(0, 0))
        self.assertTrue(self.maze.is_valid_position(7, 4))
        self.assertTrue(self.maze.is_valid_position(3, 2))
        
        # Invalid positions
        self.assertFalse(self.maze.is_valid_position(-1, 0))
        self.assertFalse(self.maze.is_valid_position(0, -1))
        self.assertFalse(self.maze.is_valid_position(8, 0))
        self.assertFalse(self.maze.is_valid_position(0, 5))
    
    def test_walkable(self):
        """Test walkable position detection."""
        # Empty spaces should be walkable
        self.assertTrue(self.maze.is_walkable(1, 1))
        self.assertTrue(self.maze.is_walkable(5, 1))
        
        # Walls should not be walkable
        self.assertFalse(self.maze.is_walkable(0, 0))
        self.assertFalse(self.maze.is_walkable(3, 2))
        
        # Out of bounds should not be walkable
        self.assertFalse(self.maze.is_walkable(-1, 0))
        self.assertFalse(self.maze.is_walkable(10, 10))
    
    def test_dot_detection(self):
        """Test dot detection."""
        # Should have dots initially
        self.assertTrue(self.maze.has_dot(1, 1))
        self.assertTrue(self.maze.has_dot(2, 1))
        
        # Should not have dots where there aren't any
        self.assertFalse(self.maze.has_dot(0, 0))  # Wall
        self.assertFalse(self.maze.has_dot(6, 1))  # Power pellet
    
    def test_power_pellet_detection(self):
        """Test power pellet detection."""
        # Should have power pellet
        self.assertTrue(self.maze.has_power_pellet(6, 1))
        
        # Should not have pellets where there aren't any
        self.assertFalse(self.maze.has_power_pellet(1, 1))  # Dot
        self.assertFalse(self.maze.has_power_pellet(0, 0))  # Wall
    
    def test_dot_collection(self):
        """Test dot collection."""
        # Should be able to collect dot
        self.assertTrue(self.maze.collect_dot(1, 1))
        
        # Should not have dot after collection
        self.assertFalse(self.maze.has_dot(1, 1))
        
        # Should not be able to collect same dot again
        self.assertFalse(self.maze.collect_dot(1, 1))
        
        # Should not be able to collect non-dot
        self.assertFalse(self.maze.collect_dot(0, 0))
    
    def test_power_pellet_collection(self):
        """Test power pellet collection."""
        # Should be able to collect pellet
        self.assertTrue(self.maze.collect_power_pellet(6, 1))
        
        # Should not have pellet after collection
        self.assertFalse(self.maze.has_power_pellet(6, 1))
        
        # Should not be able to collect same pellet again
        self.assertFalse(self.maze.collect_power_pellet(6, 1))
    
    def test_remaining_counts(self):
        """Test counting remaining items."""
        initial_dots = self.maze.get_remaining_dots()
        initial_pellets = self.maze.get_remaining_pellets()
        
        # Collect a dot
        self.maze.collect_dot(1, 1)
        self.assertEqual(self.maze.get_remaining_dots(), initial_dots - 1)
        
        # Collect a pellet
        self.maze.collect_power_pellet(6, 1)
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
        self.maze.collect_dot(1, 1)
        self.maze.collect_power_pellet(6, 1)
        
        # Reset maze
        self.maze.reset()
        
        # Items should be available again
        self.assertTrue(self.maze.has_dot(1, 1))
        self.assertTrue(self.maze.has_power_pellet(6, 1))
        self.assertEqual(self.maze.get_remaining_dots(), self.maze.total_dots)
        self.assertEqual(self.maze.get_remaining_pellets(), self.maze.total_pellets)
    
    def test_ghost_house_detection(self):
        """Test ghost house detection."""
        # Should detect ghost house
        self.assertTrue(self.maze.is_ghost_house(5, 3))
        
        # Should not detect ghost house elsewhere
        self.assertFalse(self.maze.is_ghost_house(1, 1))
    
    def test_get_cell_char(self):
        """Test getting display character for cells."""
        # Wall - now using block character
        self.assertEqual(self.maze.get_cell_char(0, 0), '█')
        
        # Dot
        self.assertEqual(self.maze.get_cell_char(1, 1), '.')
        
        # Power pellet
        self.assertEqual(self.maze.get_cell_char(6, 1), 'O')
        
        # After collecting dot
        self.maze.collect_dot(1, 1)
        self.assertEqual(self.maze.get_cell_char(1, 1), ' ')
    
    def test_empty_maze(self):
        """Test handling of empty maze."""
        empty_maze = Maze([])
        self.assertEqual(empty_maze.width, 0)
        self.assertEqual(empty_maze.height, 0)
        self.assertFalse(empty_maze.is_valid_position(0, 0))


if __name__ == '__main__':
    unittest.main()
