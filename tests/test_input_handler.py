"""
Tests for input handling functionality.
"""

import unittest
from PyPacman.ui.input_handler import MockInputHandler, Keys
from PyPacman.core.types import Direction


class TestInputHandler(unittest.TestCase):
    """Test input handler functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.input_handler = MockInputHandler()

    def test_arrow_key_to_direction(self) -> None:
        """Test arrow key to direction mapping."""
        self.assertEqual(self.input_handler.key_to_direction('up'), Direction.UP)
        self.assertEqual(self.input_handler.key_to_direction('down'), Direction.DOWN)
        self.assertEqual(self.input_handler.key_to_direction('left'), Direction.LEFT)
        self.assertEqual(self.input_handler.key_to_direction('right'), Direction.RIGHT)

    def test_wasd_key_to_direction(self) -> None:
        """Test WASD key to direction mapping."""
        self.assertEqual(self.input_handler.key_to_direction(Keys.W), Direction.UP)
        self.assertEqual(self.input_handler.key_to_direction(Keys.S), Direction.DOWN)
        self.assertEqual(self.input_handler.key_to_direction(Keys.A), Direction.LEFT)
        self.assertEqual(self.input_handler.key_to_direction(Keys.D), Direction.RIGHT)

    def test_invalid_key_to_direction(self) -> None:
        """Test invalid key returns no direction."""
        self.assertEqual(self.input_handler.key_to_direction('x'), Direction.NONE)
        self.assertEqual(self.input_handler.key_to_direction(''), Direction.NONE)

    def test_is_quit_key(self) -> None:
        """Test quit key detection."""
        self.assertTrue(self.input_handler.is_quit_key(Keys.QUIT))
        self.assertFalse(self.input_handler.is_quit_key(Keys.SPACE))
        self.assertFalse(self.input_handler.is_quit_key('x'))

    def test_is_pause_key(self) -> None:
        """Test pause key detection."""
        self.assertTrue(self.input_handler.is_pause_key(Keys.SPACE))
        self.assertFalse(self.input_handler.is_pause_key(Keys.QUIT))
        self.assertFalse(self.input_handler.is_pause_key('x'))

    def test_mock_input_queue(self) -> None:
        """Test mock input handler queue functionality."""
        self.assertIsNone(self.input_handler.get_key())

        self.input_handler.add_key('up')
        self.input_handler.add_key(Keys.SPACE)

        self.assertEqual(self.input_handler.get_key(), 'up')
        self.assertEqual(self.input_handler.get_key(), Keys.SPACE)
        self.assertIsNone(self.input_handler.get_key())

    def test_arrow_keys_work_correctly(self) -> None:
        """Test that arrow keys work correctly."""
        # Arrow keys should return direction keys
        self.input_handler.add_key('up')
        result = self.input_handler.get_key()
        self.assertEqual(result, 'up')

        self.input_handler.add_key('down')
        result = self.input_handler.get_key()
        self.assertEqual(result, 'down')


if __name__ == '__main__':
    unittest.main()
