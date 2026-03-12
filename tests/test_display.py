"""
Tests for display and rendering functionality.
"""

import unittest
from PyPacman.ui.display import MockDisplay
from PyPacman.core.config import GAME_WIDTH, GAME_HEIGHT
from PyPacman.core.colors import Colors


class TestDisplay(unittest.TestCase):
    """Test display functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.display = MockDisplay()

    def test_clear_buffer(self) -> None:
        """Test buffer clearing."""
        # Set some characters
        self.display.set_char(5, 5, 'X')
        self.display.set_char(10, 10, 'Y')

        self.display.clear_buffer()

        # Check that buffer is cleared
        for y in range(GAME_HEIGHT):
            for x in range(GAME_WIDTH):
                self.assertEqual(self.display.buffer[y][x], ' ')

    def test_set_char(self) -> None:
        """Test setting individual characters."""
        self.display.clear_buffer()

        # Test valid positions
        self.display.set_char(0, 0, 'A')
        self.display.set_char(GAME_WIDTH - 1, GAME_HEIGHT - 1, 'Z')

        # Check characters were set (accounting for color codes)
        self.assertTrue('A' in self.display.buffer[0][0])
        self.assertTrue('Z' in self.display.buffer[GAME_HEIGHT - 1][GAME_WIDTH - 1])

        # Test invalid positions (should not crash)
        self.display.set_char(-1, 0, 'X')
        self.display.set_char(0, -1, 'X')
        self.display.set_char(GAME_WIDTH, 0, 'X')
        self.display.set_char(0, GAME_HEIGHT, 'X')

    def test_set_string(self) -> None:
        """Test setting strings."""
        self.display.clear_buffer()

        test_string = "HELLO"
        self.display.set_string(5, 10, test_string)

        # Check each character was set
        for i, char in enumerate(test_string):
            self.assertTrue(char in self.display.buffer[10][5 + i])

    def test_draw_border(self) -> None:
        """Test border drawing."""
        self.display.clear_buffer()
        self.display.draw_border()

        # Check corners
        self.assertTrue('╔' in self.display.buffer[0][0])
        self.assertTrue('╗' in self.display.buffer[0][GAME_WIDTH - 1])
        self.assertTrue('╚' in self.display.buffer[GAME_HEIGHT - 1][0])
        self.assertTrue('╝' in self.display.buffer[GAME_HEIGHT - 1][GAME_WIDTH - 1])

        # Check top and bottom borders
        for x in range(1, GAME_WIDTH - 1):
            self.assertTrue('═' in self.display.buffer[0][x])
            self.assertTrue('═' in self.display.buffer[GAME_HEIGHT - 1][x])

        # Check left and right borders
        for y in range(1, GAME_HEIGHT - 1):
            self.assertTrue('║' in self.display.buffer[y][0])
            self.assertTrue('║' in self.display.buffer[y][GAME_WIDTH - 1])

    def test_draw_centered_text(self) -> None:
        """Test centered text drawing."""
        self.display.clear_buffer()

        text = "TEST"
        expected_x = (GAME_WIDTH - len(text)) // 2
        self.display.draw_centered_text(5, text)

        # Check text is positioned correctly
        for i, char in enumerate(text):
            self.assertTrue(char in self.display.buffer[5][expected_x + i])

    def test_get_game_bounds(self) -> None:
        """Test game bounds calculation."""
        bounds = self.display.get_game_bounds()
        expected = (1, 1, GAME_WIDTH - 2, GAME_HEIGHT - 2)
        self.assertEqual(bounds, expected)

    def test_render_stores_frame(self) -> None:
        """Test that mock display stores rendered frames."""
        self.display.clear_buffer()
        self.display.set_char(10, 10, 'X')

        initial_frames = len(self.display.rendered_frames)
        self.display.render()

        # Check frame was stored
        self.assertEqual(len(self.display.rendered_frames), initial_frames + 1)

        # Check character appears in frame
        last_frame = self.display.get_last_frame()
        self.assertEqual(last_frame[10][10], 'X')


if __name__ == '__main__':
    unittest.main()
