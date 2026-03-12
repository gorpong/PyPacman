"""
Tests for game engine functionality.
"""

import unittest
from PyPacman.core.game_engine import GameEngine
from PyPacman.ui.display import MockDisplay
from PyPacman.ui.input_handler import MockInputHandler, Keys
from PyPacman.core.types import GameMode


class TestGameEngine(unittest.TestCase):
    """Test game engine functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.display = MockDisplay()
        self.input_handler = MockInputHandler()
        self.game = GameEngine(self.display, self.input_handler)

    def test_initial_state(self):
        """Test initial game state."""
        self.assertEqual(self.game.state, GameMode.MENU)
        self.assertTrue(self.game.running)
        self.assertEqual(self.game.scoring.get_score(), 0)
        self.assertEqual(self.game.game_state.get_lives(), 3)
        self.assertEqual(self.game.game_state.get_level(), 1)
        self.assertFalse(self.game.show_high_scores)
        self.assertEqual(self.game.menu_idle_timer, 0.0)

    def test_quit_functionality(self):
        """Test quit functionality."""
        self.assertTrue(self.game.running)

        self.game.quit()

        self.assertEqual(self.game.state, GameMode.QUIT)
        self.assertFalse(self.game.running)

    def test_menu_to_game_transition(self):
        """Test transition from menu to game."""
        self.game.state = GameMode.MENU

        self.input_handler.add_key(Keys.SPACE)
        self.game.handle_input()

        self.assertEqual(self.game.state, GameMode.PLAYING)

    def test_game_to_pause_transition(self):
        """Test transition from game to pause."""
        self.game.state = GameMode.PLAYING

        self.input_handler.add_key(Keys.SPACE)
        self.game.handle_input()

        self.assertEqual(self.game.state, GameMode.PAUSED)

    def test_pause_to_game_transition(self):
        """Test transition from pause to game."""
        self.game.state = GameMode.PAUSED

        self.input_handler.add_key(Keys.SPACE)
        self.game.handle_input()

        self.assertEqual(self.game.state, GameMode.PLAYING)

    def test_q_shows_quit_confirmation(self):
        """Test Q key shows quit confirmation from any state."""
        states = [GameMode.MENU, GameMode.PLAYING, GameMode.PAUSED, GameMode.GAME_OVER]

        for state in states:
            with self.subTest(state=state):
                self.game.running = True
                self.game.state = state

                self.input_handler.add_key(Keys.QUIT)
                self.game.handle_input()

                self.assertEqual(self.game.state, GameMode.QUIT_CONFIRM)
                self.assertTrue(self.game.running)

    def test_reset_game(self):
        """Test game reset functionality."""
        self.game.scoring.score = 1000
        self.game.game_state.lives = 1
        self.game.game_state.level = 5

        self.game.reset_game()

        self.assertEqual(self.game.scoring.get_score(), 0)
        self.assertEqual(self.game.game_state.get_lives(), 3)
        self.assertEqual(self.game.game_state.get_level(), 1)

    def test_update_calls_correct_handler(self):
        """Test update calls correct state handler."""
        states = [GameMode.MENU, GameMode.PLAYING, GameMode.PAUSED, GameMode.GAME_OVER, GameMode.QUIT_CONFIRM]

        for state in states:
            with self.subTest(state=state):
                self.game.state = state
                self.game.update(0.016)

    def test_render_calls_correct_handler(self):
        """Test render calls correct state handler."""
        states = [GameMode.MENU, GameMode.PLAYING, GameMode.PAUSED, GameMode.GAME_OVER, GameMode.QUIT_CONFIRM]

        for state in states:
            with self.subTest(state=state):
                self.game.state = state
                initial_frames = len(self.display.rendered_frames)

                self.game.render()

                self.assertEqual(len(self.display.rendered_frames), initial_frames + 1)

    def test_movement_input_in_game_state(self):
        """Test movement input is processed in game state."""
        self.game.state = GameMode.PLAYING

        movement_keys = ['up', 'down', 'left', 'right',
                         Keys.W, Keys.A, Keys.S, Keys.D]

        for key in movement_keys:
            with self.subTest(key=key):
                self.input_handler.add_key(key)
                self.game.handle_input()

    def test_game_over_to_playing_transition(self):
        """Test transition from game over to playing."""
        self.game.state = GameMode.GAME_OVER

        self.input_handler.add_key(Keys.SPACE)
        self.game.handle_input()

        self.assertEqual(self.game.state, GameMode.PLAYING)

    def test_quit_confirmation_yes(self):
        """Test quit confirmation with Y."""
        self.game.state = GameMode.QUIT_CONFIRM

        self.input_handler.add_key('y')
        self.game.handle_input()

        self.assertEqual(self.game.state, GameMode.QUIT)
        self.assertFalse(self.game.running)

    def test_quit_confirmation_no(self):
        """Test quit confirmation with N."""
        self.game._previous_mode = GameMode.PLAYING
        self.game.state = GameMode.QUIT_CONFIRM

        self.input_handler.add_key('n')
        self.game.handle_input()

        self.assertEqual(self.game.state, GameMode.PLAYING)

    def test_menu_idle_timer(self):
        """Test menu idle timer triggers high scores."""
        self.game.state = GameMode.MENU
        self.assertFalse(self.game.show_high_scores)

        for _ in range(11):
            self.game.update_menu(1.0)

        self.assertTrue(self.game.show_high_scores)
        self.assertGreater(self.game.menu_idle_timer, 10.0)

    def test_menu_high_scores_dismiss(self):
        """Test that any key dismisses high scores."""
        self.game.state = GameMode.MENU
        self.game.show_high_scores = True
        self.game.menu_idle_timer = 15.0

        self.input_handler.add_key('a')
        self.game.handle_input()

        self.assertFalse(self.game.show_high_scores)
        self.assertEqual(self.game.menu_idle_timer, 0.0)
        self.assertEqual(self.game.state, GameMode.MENU)

    def test_menu_scroll_animation(self):
        """Test high score scroll animation."""
        self.game.state = GameMode.MENU
        self.game.show_high_scores = True
        initial_offset = self.game.high_score_scroll_offset

        self.game.update_menu(1.0)

        self.assertGreater(self.game.high_score_scroll_offset, initial_offset)


if __name__ == '__main__':
    unittest.main()
