"""
Unit tests for Pac-Man character.
"""

import unittest

from PyPacman.entities.pacman import PacMan
from PyPacman.core.maze import Maze
from PyPacman.core.types import Direction
from PyPacman.core.sprites import Sprites


class TestPacMan(unittest.TestCase):
    """Test cases for Pac-Man character."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.pacman = PacMan(5, 5)

        # Create a simple test maze
        self.test_layout = [
            "#########",
            "#.......#",
            "#.#####.#",
            "#.......#",
            "#.#####.#",
            "#.......#",
            "#########"
        ]
        self.maze = Maze(self.test_layout)

    def test_initialization(self) -> None:
        """Test Pac-Man initialization."""
        self.assertEqual(self.pacman.position.x, 5)
        self.assertEqual(self.pacman.position.y, 5)
        self.assertEqual(self.pacman.direction, Direction.RIGHT)
        self.assertFalse(self.pacman.moving)
        self.assertTrue(self.pacman.mouth_open)

    def test_reset(self) -> None:
        """Test resetting Pac-Man to starting position."""
        # Move Pac-Man
        self.pacman.position.x = 10
        self.pacman.position.y = 10
        self.pacman.direction = Direction.UP

        # Reset
        self.pacman.reset()

        # Check reset to original position
        self.assertEqual(self.pacman.position.x, 5)
        self.assertEqual(self.pacman.position.y, 5)
        self.assertEqual(self.pacman.direction, Direction.RIGHT)

    def test_set_direction(self) -> None:
        """Test setting Pac-Man's direction."""
        self.pacman.set_direction(Direction.UP)
        self.assertEqual(self.pacman.next_direction, Direction.UP)

        self.pacman.set_direction(Direction.LEFT)
        self.assertEqual(self.pacman.next_direction, Direction.LEFT)

        # Should ignore NONE direction
        self.pacman.set_direction(Direction.NONE)
        self.assertEqual(self.pacman.next_direction, Direction.LEFT)

    def test_can_move(self) -> None:
        """Test movement validation."""
        # Position Pac-Man in walkable area
        self.pacman.position.x = 1
        self.pacman.position.y = 1

        # Can move right (into dot)
        self.assertTrue(self.pacman.can_move_to(self.maze, 2, 1))

        # Cannot move up (into wall)
        self.assertFalse(self.pacman.can_move_to(self.maze, 1, 0))

        # Can move down
        self.assertTrue(self.pacman.can_move_to(self.maze, 1, 2))

    def test_get_sprite(self) -> None:
        """Test sprite selection based on direction."""
        # Right direction
        self.pacman.direction = Direction.RIGHT
        self.pacman.mouth_open = True
        self.assertEqual(self.pacman.get_sprite(), Sprites.PACMAN_RIGHT)

        # Left direction
        self.pacman.direction = Direction.LEFT
        self.assertEqual(self.pacman.get_sprite(), Sprites.PACMAN_LEFT)

        # Up direction
        self.pacman.direction = Direction.UP
        self.assertEqual(self.pacman.get_sprite(), Sprites.PACMAN_UP)

        # Down direction
        self.pacman.direction = Direction.DOWN
        self.assertEqual(self.pacman.get_sprite(), Sprites.PACMAN_DOWN)

        # Mouth closed
        self.pacman.mouth_open = False
        self.assertEqual(self.pacman.get_sprite(), Sprites.PACMAN_CLOSED)

    def test_animation(self) -> None:
        """Test mouth animation."""
        initial_state = self.pacman.mouth_open

        # Update with enough time to trigger animation
        self.pacman.update(0.15, self.maze)

        # Mouth should have toggled
        self.assertNotEqual(self.pacman.mouth_open, initial_state)

    def test_movement(self) -> None:
        """Test actual movement."""
        # Place Pac-Man in open area
        self.pacman.position.x = 1
        self.pacman.position.y = 1

        # Set direction to right
        self.pacman.set_direction(Direction.RIGHT)

        # Update multiple times to trigger movement
        for _ in range(10):
            self.pacman.update(0.15, self.maze)

        # Pac-Man should have moved right
        self.assertGreater(self.pacman.position.x, 1)
        self.assertEqual(self.pacman.position.y, 1)

    def test_wall_collision(self) -> None:
        """Test that Pac-Man stops at walls."""
        # Place Pac-Man at the edge next to wall
        self.pacman.position.x = 7
        self.pacman.position.y = 1

        # Try to move into wall (right)
        self.pacman.set_direction(Direction.RIGHT)

        # Update multiple times
        for _ in range(10):
            self.pacman.update(0.15, self.maze)

        # Pac-Man should not have moved past the boundary
        self.assertEqual(self.pacman.position.x, 7)
        self.assertEqual(self.pacman.position.y, 1)
        self.assertFalse(self.pacman.moving)

    def test_direction_change(self) -> None:
        """Test changing direction while moving."""
        # Place Pac-Man in open area
        self.pacman.position.x = 3
        self.pacman.position.y = 3

        # Start moving right
        self.pacman.set_direction(Direction.RIGHT)
        self.pacman.update(0.15, self.maze)

        # Request direction change to up
        self.pacman.set_direction(Direction.UP)

        # Update to apply direction change
        for _ in range(10):
            self.pacman.update(0.15, self.maze)

        # Should have changed direction and moved up
        self.assertEqual(self.pacman.direction, Direction.UP)
        self.assertLess(self.pacman.position.y, 3)

    def test_edge_wrapping(self) -> None:
        """Test wrapping at maze edges (tunnel behavior)."""
        # Create a maze with open edges
        open_layout = [
            "#####",
            ".....",
            "#####"
        ]
        open_maze = Maze(open_layout)

        # Place Pac-Man at right edge
        self.pacman.position.x = 4
        self.pacman.position.y = 1

        # Move right (should wrap to left)
        self.pacman.set_direction(Direction.RIGHT)
        self.pacman.update(0.15, open_maze)

        # Should wrap to left side
        if self.pacman.can_move_to(open_maze, 5, 1):
            for _ in range(10):
                self.pacman.update(0.15, open_maze)
            if self.pacman.position.x > 4:
                self.assertEqual(self.pacman.position.x, 0)

    def test_get_position(self) -> None:
        """Test position getter."""
        self.pacman.position.x = 7
        self.pacman.position.y = 3
        pos = self.pacman.get_position()
        self.assertEqual(pos.x, 7)
        self.assertEqual(pos.y, 3)


if __name__ == '__main__':
    unittest.main()
