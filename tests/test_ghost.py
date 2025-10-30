"""
Unit tests for Ghost AI system.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ascii_pacman.entities.ghost import Ghost, Blinky, Pinky, Inky, Clyde, GhostMode, GhostState
from ascii_pacman.entities.ghost_manager import GhostManager
from ascii_pacman.core.maze import Maze
from ascii_pacman.entities.pacman import PacMan
from ascii_pacman.core.constants import Colors


class TestGhost(unittest.TestCase):
    """Test cases for Ghost AI."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a simple test maze
        self.test_layout = [
            "############################",
            "#..........................#",
            "#.###.####.####.####.###.##",
            "#..........................#",
            "#.###.##.########.##.###.##",
            "#.....##....##....##.....##",
            "#####.##### ## #####.######",
            "    #.##    GG    ##.#     ",
            "#####.## ###--### ##.######",
            "#........##....##........##",
            "#.##.###.##.##.##.###.##.##",
            "#..........................#",
            "############################",
        ]
        self.maze = Maze(self.test_layout)
        self.pacman = PacMan(14, 11)
    
    def test_ghost_initialization(self):
        """Test basic ghost initialization."""
        ghost = Blinky(10, 7)
        
        self.assertEqual(ghost.position.x, 10)
        self.assertEqual(ghost.position.y, 7)
        self.assertEqual(ghost.color, Colors.RED)
        self.assertEqual(ghost.name, "Blinky")
        self.assertEqual(ghost.state, GhostState.IN_HOUSE)
        self.assertEqual(ghost.mode, GhostMode.SCATTER)
    
    def test_ghost_types(self):
        """Test different ghost types have different properties."""
        blinky = Blinky(10, 7)
        pinky = Pinky(11, 7)
        inky = Inky(12, 7)
        clyde = Clyde(13, 7)
        
        # Different colors
        self.assertEqual(blinky.color, Colors.RED)
        self.assertEqual(pinky.color, Colors.PINK)
        self.assertEqual(inky.color, Colors.CYAN)
        self.assertEqual(clyde.color, Colors.ORANGE)
        
        # Different release delays
        self.assertEqual(blinky.release_delay, 0.0)
        self.assertGreater(pinky.release_delay, 0.0)
        self.assertGreater(inky.release_delay, pinky.release_delay)
        self.assertGreater(clyde.release_delay, inky.release_delay)
    
    def test_ghost_vulnerability(self):
        """Test ghost vulnerability mechanics."""
        ghost = Blinky(10, 7)
        ghost.state = GhostState.ACTIVE  # Set to active first
        
        # Initially not vulnerable but dangerous when active
        self.assertFalse(ghost.is_vulnerable())
        self.assertTrue(ghost.is_dangerous())
        
        # Make vulnerable
        ghost.make_vulnerable(8.0)
        self.assertTrue(ghost.is_vulnerable())
        self.assertFalse(ghost.is_dangerous())
        self.assertEqual(ghost.mode, GhostMode.VULNERABLE)
        
        # Time passes
        ghost.vulnerable_timer = 0.0
        self.assertFalse(ghost.is_vulnerable())
    
    def test_ghost_eaten(self):
        """Test ghost being eaten."""
        ghost = Blinky(10, 7)
        ghost.state = GhostState.ACTIVE
        original_x, original_y = ghost.start_position.x, ghost.start_position.y
        
        # Move ghost away from start
        ghost.position.x = 15
        ghost.position.y = 15
        
        ghost.get_eaten()
        self.assertEqual(ghost.mode, GhostMode.EATEN)
        self.assertEqual(ghost.state, GhostState.IN_HOUSE)
        # Should teleport back to start position
        self.assertEqual(ghost.position.x, original_x)
        self.assertEqual(ghost.position.y, original_y)
    
    def test_ghost_collision(self):
        """Test ghost collision detection."""
        ghost = Blinky(10, 7)
        
        self.assertTrue(ghost.collides_with(10, 7))
        self.assertFalse(ghost.collides_with(10, 8))
        self.assertFalse(ghost.collides_with(11, 7))
    
    def test_ghost_reset(self):
        """Test ghost reset functionality."""
        ghost = Blinky(10, 7)
        
        # Change state
        ghost.position.x = 15
        ghost.position.y = 15
        ghost.mode = GhostMode.CHASE
        ghost.state = GhostState.ACTIVE
        
        # Reset
        ghost.reset()
        
        # Should be back to original state
        self.assertEqual(ghost.position.x, 10)
        self.assertEqual(ghost.position.y, 7)
        self.assertEqual(ghost.mode, GhostMode.SCATTER)
        self.assertEqual(ghost.state, GhostState.IN_HOUSE)


class TestGhostManager(unittest.TestCase):
    """Test cases for Ghost Manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_layout = [
            "############################",
            "#..........................#",
            "#.###.####.####.####.###.##",
            "#..........................#",
            "#.###.##.########.##.###.##",
            "#.....##....##....##.....##",
            "#####.##### ## #####.######",
            "    #.##    GG    ##.#     ",
            "#####.## ###--### ##.######",
            "#........##....##........##",
            "#.##.###.##.##.##.###.##.##",
            "#..........................#",
            "############################",
        ]
        self.maze = Maze(self.test_layout)
        self.pacman = PacMan(14, 11)
        self.ghost_manager = GhostManager(self.maze)
    
    def test_ghost_manager_initialization(self):
        """Test ghost manager creates all four ghosts."""
        self.assertEqual(len(self.ghost_manager.ghosts), 4)
        
        # Check ghost types
        self.assertIsInstance(self.ghost_manager.ghosts[0], Blinky)
        self.assertIsInstance(self.ghost_manager.ghosts[1], Pinky)
        self.assertIsInstance(self.ghost_manager.ghosts[2], Inky)
        self.assertIsInstance(self.ghost_manager.ghosts[3], Clyde)
    
    def test_make_all_vulnerable(self):
        """Test making all ghosts vulnerable."""
        # Set ghosts to active state first
        for ghost in self.ghost_manager.ghosts:
            ghost.state = GhostState.ACTIVE
            ghost.mode = GhostMode.CHASE
        
        self.ghost_manager.make_all_vulnerable()
        
        # All should be vulnerable now
        for ghost in self.ghost_manager.ghosts:
            self.assertTrue(ghost.is_vulnerable())
    
    def test_collision_detection(self):
        """Test collision detection with Pac-Man."""
        # Move a ghost to Pac-Man's position and make it active
        test_ghost = self.ghost_manager.ghosts[0]
        test_ghost.state = GhostState.ACTIVE  # Must be active to collide
        px, py = self.pacman.get_position()
        test_ghost.position.x = px
        test_ghost.position.y = py
        
        colliding_ghost = self.ghost_manager.check_collision_with_pacman(self.pacman)
        self.assertEqual(colliding_ghost, test_ghost)
    
    def test_no_collision(self):
        """Test no collision when ghosts are away."""
        # Ensure no ghost is at Pac-Man's position
        px, py = self.pacman.get_position()
        for ghost in self.ghost_manager.ghosts:
            ghost.position.x = 1
            ghost.position.y = 1
        
        colliding_ghost = self.ghost_manager.check_collision_with_pacman(self.pacman)
        self.assertIsNone(colliding_ghost)
    
    def test_reset_all_ghosts(self):
        """Test resetting all ghosts."""
        # Change all ghost states
        for ghost in self.ghost_manager.ghosts:
            ghost.position.x = 20
            ghost.mode = GhostMode.CHASE
            ghost.state = GhostState.ACTIVE
        
        self.ghost_manager.reset()
        
        # All should be reset
        for ghost in self.ghost_manager.ghosts:
            self.assertEqual(ghost.state, GhostState.IN_HOUSE)
            self.assertEqual(ghost.mode, GhostMode.SCATTER)
    
    def test_get_ghost_positions(self):
        """Test getting ghost positions for rendering."""
        positions = self.ghost_manager.get_ghost_positions()
        
        # Should return 4 positions
        self.assertEqual(len(positions), 4)
        
        # Each position should have x, y, sprite, color
        for x, y, sprite, color in positions:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
            self.assertIsInstance(sprite, str)
            self.assertIsInstance(color, str)
    
    def test_get_vulnerable_ghosts(self):
        """Test getting list of vulnerable ghosts."""
        # Make some ghosts vulnerable
        self.ghost_manager.ghosts[0].state = GhostState.ACTIVE
        self.ghost_manager.ghosts[1].state = GhostState.ACTIVE
        
        self.ghost_manager.ghosts[0].make_vulnerable(5.0)
        self.ghost_manager.ghosts[1].make_vulnerable(5.0)
        
        vulnerable = self.ghost_manager.get_vulnerable_ghosts()
        self.assertEqual(len(vulnerable), 2)
    
    def test_get_dangerous_ghosts(self):
        """Test getting list of dangerous ghosts."""
        # Make ghosts active and dangerous
        for ghost in self.ghost_manager.ghosts:
            ghost.state = GhostState.ACTIVE
            ghost.mode = GhostMode.CHASE
        
        dangerous = self.ghost_manager.get_dangerous_ghosts()
        self.assertEqual(len(dangerous), 4)
    
    def test_eat_ghost_scoring(self):
        """Test progressive scoring when eating ghosts."""
        ghost = self.ghost_manager.ghosts[0]
        ghost.state = GhostState.ACTIVE
        ghost.make_vulnerable(5.0)
        
        # First ghost: 200
        score1 = self.ghost_manager.eat_ghost(ghost)
        self.assertEqual(score1, 200)
        
        # Second ghost
        ghost2 = self.ghost_manager.ghosts[1]
        ghost2.state = GhostState.ACTIVE
        ghost2.make_vulnerable(5.0)
        score2 = self.ghost_manager.eat_ghost(ghost2)
        self.assertEqual(score2, 400)
        
        # Third ghost
        ghost3 = self.ghost_manager.ghosts[2]
        ghost3.state = GhostState.ACTIVE
        ghost3.make_vulnerable(5.0)
        score3 = self.ghost_manager.eat_ghost(ghost3)
        self.assertEqual(score3, 800)
        
        # Fourth ghost
        ghost4 = self.ghost_manager.ghosts[3]
        ghost4.state = GhostState.ACTIVE
        ghost4.make_vulnerable(5.0)
        score4 = self.ghost_manager.eat_ghost(ghost4)
        self.assertEqual(score4, 1600)


if __name__ == '__main__':
    unittest.main()
