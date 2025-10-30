"""Tests for game state management."""

import unittest
from ascii_pacman.core.game_state import GameState


class TestGameState(unittest.TestCase):
    """Test game state management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game_state = GameState(starting_lives=3)
    
    def test_initialization(self):
        """Test game state initializes correctly."""
        self.assertEqual(self.game_state.get_lives(), 3)
        self.assertEqual(self.game_state.get_level(), 1)
        self.assertFalse(self.game_state.is_game_over())
    
    def test_lose_life(self):
        """Test losing lives."""
        # Lose first life
        game_over = self.game_state.lose_life()
        self.assertFalse(game_over)
        self.assertEqual(self.game_state.get_lives(), 2)
        
        # Lose second life
        game_over = self.game_state.lose_life()
        self.assertFalse(game_over)
        self.assertEqual(self.game_state.get_lives(), 1)
        
        # Lose last life
        game_over = self.game_state.lose_life()
        self.assertTrue(game_over)
        self.assertEqual(self.game_state.get_lives(), 0)
        self.assertTrue(self.game_state.is_game_over())
    
    def test_add_life(self):
        """Test adding extra life."""
        self.game_state.add_life()
        self.assertEqual(self.game_state.get_lives(), 4)
    
    def test_next_level(self):
        """Test level progression."""
        self.assertEqual(self.game_state.get_level(), 1)
        
        level = self.game_state.next_level()
        self.assertEqual(level, 2)
        self.assertEqual(self.game_state.get_level(), 2)
        
        self.game_state.next_level()
        self.assertEqual(self.game_state.get_level(), 3)
    
    def test_reset(self):
        """Test reset functionality."""
        # Change state
        self.game_state.lose_life()
        self.game_state.next_level()
        
        # Reset
        self.game_state.reset()
        
        self.assertEqual(self.game_state.get_lives(), 3)
        self.assertEqual(self.game_state.get_level(), 1)
        self.assertFalse(self.game_state.is_game_over())
    
    def test_ghost_speed_multiplier(self):
        """Test ghost speed increases with level."""
        # Level 1
        mult1 = self.game_state.get_ghost_speed_multiplier()
        self.assertEqual(mult1, 1.0)
        
        # Level 2
        self.game_state.next_level()
        mult2 = self.game_state.get_ghost_speed_multiplier()
        self.assertEqual(mult2, 1.05)
        
        # Level 10
        for _ in range(8):
            self.game_state.next_level()
        mult10 = self.game_state.get_ghost_speed_multiplier()
        self.assertEqual(mult10, 1.45)
        
        # Test cap at 2.0
        for _ in range(50):
            self.game_state.next_level()
        mult_max = self.game_state.get_ghost_speed_multiplier()
        self.assertEqual(mult_max, 2.0)
    
    def test_pacman_speed_multiplier(self):
        """Test Pac-Man speed increases with level (slower than ghosts)."""
        # Level 1
        mult1 = self.game_state.get_pacman_speed_multiplier()
        self.assertEqual(mult1, 1.0)
        
        # Level 2
        self.game_state.next_level()
        mult2 = self.game_state.get_pacman_speed_multiplier()
        self.assertEqual(mult2, 1.03)
        
        # Test cap at 1.5
        for _ in range(50):
            self.game_state.next_level()
        mult_max = self.game_state.get_pacman_speed_multiplier()
        self.assertEqual(mult_max, 1.5)


if __name__ == '__main__':
    unittest.main()
