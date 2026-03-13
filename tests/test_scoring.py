"""Tests for scoring system."""

import unittest
import os
import tempfile
from pathlib import Path
from PyPacman.core.scoring import ScoringSystem


class TestScoringSystem(unittest.TestCase):
    """Test scoring system."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        self.scoring = ScoringSystem()
        self.scoring.high_score_file = Path(self.temp_file.name)
        self.scoring.high_scores = []
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temp file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_initialization(self):
        """Test scoring system initializes correctly."""
        self.assertEqual(self.scoring.get_score(), 0)
        self.assertEqual(self.scoring.get_high_score(), 0)
        self.assertEqual(self.scoring.ghosts_eaten_combo, 0)
    
    def test_dot_scoring(self):
        """Test dot collection scoring."""
        points = self.scoring.add_dot()
        self.assertEqual(points, 10)
        self.assertEqual(self.scoring.get_score(), 10)
        
        self.scoring.add_dot()
        self.assertEqual(self.scoring.get_score(), 20)
    
    def test_power_pellet_scoring(self):
        """Test power pellet scoring."""
        points = self.scoring.add_power_pellet()
        self.assertEqual(points, 50)
        self.assertEqual(self.scoring.get_score(), 50)
    
    def test_ghost_scoring_progressive(self):
        """Test progressive ghost scoring."""
        # First ghost: 200
        points1 = self.scoring.add_ghost()
        self.assertEqual(points1, 200)
        self.assertEqual(self.scoring.get_score(), 200)
        
        # Second ghost: 400
        points2 = self.scoring.add_ghost()
        self.assertEqual(points2, 400)
        self.assertEqual(self.scoring.get_score(), 600)
        
        # Third ghost: 800
        points3 = self.scoring.add_ghost()
        self.assertEqual(points3, 800)
        self.assertEqual(self.scoring.get_score(), 1400)
        
        # Fourth ghost: 1600
        points4 = self.scoring.add_ghost()
        self.assertEqual(points4, 1600)
        self.assertEqual(self.scoring.get_score(), 3000)
    
    def test_ghost_combo_reset(self):
        """Test ghost combo resets properly."""
        self.scoring.add_ghost()  # 200
        self.scoring.add_ghost()  # 400
        
        # Reset combo
        self.scoring.reset_ghost_combo()
        
        # Next ghost should be 200 again
        points = self.scoring.add_ghost()
        self.assertEqual(points, 200)
    
    def test_high_score_update(self):
        """Test high score tracking."""
        self.scoring.add_dot()
        self.scoring.add_dot()
        self.assertEqual(self.scoring.get_score(), 20)
        
        # Check if it's a high score
        self.assertTrue(self.scoring.is_high_score())
        
        # Add high score
        rank = self.scoring.add_high_score("TEST")
        self.assertGreater(rank, 0)
        self.assertEqual(self.scoring.get_high_score(), 20)
        
        # Reset score
        self.scoring.reset()
        self.assertEqual(self.scoring.get_score(), 0)
        self.assertEqual(self.scoring.get_high_score(), 20)  # High score persists
        
        # Score of 0 shouldn't be high score if we have scores
        self.assertFalse(self.scoring.is_high_score())
    
    def test_reset(self):
        """Test reset functionality."""
        self.scoring.add_dot()
        self.scoring.add_ghost()
        
        self.scoring.reset()
        
        self.assertEqual(self.scoring.get_score(), 0)
        self.assertEqual(self.scoring.ghosts_eaten_combo, 0)

    def test_ghost_scoring_uses_config_constants(self):
        """Test that ghost scoring uses SCORE_GHOST_BASE from config."""
        from PyPacman.core.config import SCORE_GHOST_BASE
        points = self.scoring.add_ghost()
        self.assertEqual(points, SCORE_GHOST_BASE)

    def test_ghost_scoring_max_cap(self):
        """Test that ghost scoring caps at 1600."""
        # Eat 5 ghosts - the 5th should still be 1600, not 3200
        self.scoring.add_ghost()  # 200
        self.scoring.add_ghost()  # 400
        self.scoring.add_ghost()  # 800
        self.scoring.add_ghost()  # 1600
        points5 = self.scoring.add_ghost()  # Should cap at 1600
        self.assertEqual(points5, 1600)

    def test_ghost_combo_count(self):
        """Test that ghost combo count increments correctly."""
        self.assertEqual(self.scoring.ghosts_eaten_combo, 0)
        self.scoring.add_ghost()
        self.assertEqual(self.scoring.ghosts_eaten_combo, 1)
        self.scoring.add_ghost()
        self.assertEqual(self.scoring.ghosts_eaten_combo, 2)

    def test_get_ghost_points_without_adding(self):
        """Test getting ghost points without modifying state."""
        # First ghost would be 200
        points = self.scoring.get_next_ghost_points()
        self.assertEqual(points, 200)
        # State should not change
        self.assertEqual(self.scoring.ghosts_eaten_combo, 0)
        self.assertEqual(self.scoring.get_score(), 0)

    def test_get_ghost_points_reflects_combo(self):
        """Test that get_next_ghost_points reflects current combo."""
        self.scoring.add_ghost()  # combo becomes 1
        points = self.scoring.get_next_ghost_points()
        self.assertEqual(points, 400)  # Next would be 400

    def test_get_ghost_points_respects_cap(self):
        """Test that get_next_ghost_points respects the 1600 cap."""
        self.scoring.add_ghost()  # 200, combo=1
        self.scoring.add_ghost()  # 400, combo=2
        self.scoring.add_ghost()  # 800, combo=3
        self.scoring.add_ghost()  # 1600, combo=4
        points = self.scoring.get_next_ghost_points()
        self.assertEqual(points, 1600)  # Capped


if __name__ == '__main__':
    unittest.main()
