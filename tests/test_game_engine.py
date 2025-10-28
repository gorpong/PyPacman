"""
Tests for game engine functionality.
"""

import unittest
from src.game_engine import GameEngine
from src.display import MockDisplay
from src.input_handler import MockInputHandler
from src.constants import GameState, Keys


class TestGameEngine(unittest.TestCase):
    """Test game engine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.display = MockDisplay()
        self.input_handler = MockInputHandler()
        self.game = GameEngine(self.display, self.input_handler)
    
    def test_initial_state(self):
        """Test initial game state."""
        self.assertEqual(self.game.state, GameState.MENU)
        self.assertTrue(self.game.running)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.lives, 3)
        self.assertEqual(self.game.level, 1)
    
    def test_quit_functionality(self):
        """Test quit functionality."""
        self.assertTrue(self.game.running)
        
        self.game.quit()
        
        self.assertEqual(self.game.state, GameState.QUIT)
        self.assertFalse(self.game.running)
    
    def test_menu_to_game_transition(self):
        """Test transition from menu to game."""
        self.game.state = GameState.MENU
        
        # Simulate space key press
        self.input_handler.add_key(Keys.SPACE)
        self.game.handle_input()
        
        self.assertEqual(self.game.state, GameState.PLAYING)
    
    def test_game_to_pause_transition(self):
        """Test transition from game to pause."""
        self.game.state = GameState.PLAYING
        
        # Simulate space key press
        self.input_handler.add_key(Keys.SPACE)
        self.game.handle_input()
        
        self.assertEqual(self.game.state, GameState.PAUSED)
    
    def test_pause_to_game_transition(self):
        """Test transition from pause to game."""
        self.game.state = GameState.PAUSED
        
        # Simulate space key press
        self.input_handler.add_key(Keys.SPACE)
        self.game.handle_input()
        
        self.assertEqual(self.game.state, GameState.PLAYING)
    
    def test_q_shows_quit_confirmation(self):
        """Test Q key shows quit confirmation from any state."""
        states = [GameState.MENU, GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER]
        
        for state in states:
            with self.subTest(state=state):
                # Reset game
                self.game.running = True
                self.game.state = state
                
                # Simulate Q key press
                self.input_handler.add_key(Keys.QUIT)
                self.game.handle_input()
                
                self.assertEqual(self.game.state, GameState.QUIT_CONFIRM)
                self.assertTrue(self.game.running)  # Should not quit immediately
    
    def test_reset_game(self):
        """Test game reset functionality."""
        # Modify game state
        self.game.score = 1000
        self.game.lives = 1
        self.game.level = 5
        
        self.game.reset_game()
        
        # Check state is reset
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.lives, 3)
        self.assertEqual(self.game.level, 1)
    
    def test_update_calls_correct_handler(self):
        """Test update calls correct state handler."""
        # This is more of an integration test to ensure no crashes occur
        states = [GameState.MENU, GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER, GameState.QUIT_CONFIRM]
        
        for state in states:
            with self.subTest(state=state):
                self.game.state = state
                # Should not crash
                self.game.update(0.016)  # ~60 FPS delta time
    
    def test_render_calls_correct_handler(self):
        """Test render calls correct state handler."""
        states = [GameState.MENU, GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER, GameState.QUIT_CONFIRM]
        
        for state in states:
            with self.subTest(state=state):
                self.game.state = state
                initial_frames = len(self.display.rendered_frames)
                
                # Should not crash and should render a frame
                self.game.render()
                
                self.assertEqual(len(self.display.rendered_frames), initial_frames + 1)
    
    def test_movement_input_in_game_state(self):
        """Test movement input is processed in game state."""
        self.game.state = GameState.PLAYING
        
        # Test arrow keys
        movement_keys = [Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT, 
                        Keys.W, Keys.A, Keys.S, Keys.D]
        
        for key in movement_keys:
            with self.subTest(key=key):
                self.input_handler.add_key(key)
                # Should not crash (actual movement will be implemented in later phases)
                self.game.handle_input()
    
    def test_game_over_to_playing_transition(self):
        """Test transition from game over to playing."""
        self.game.state = GameState.GAME_OVER
        
        # Simulate space key press
        self.input_handler.add_key(Keys.SPACE)
        self.game.handle_input()
        
        self.assertEqual(self.game.state, GameState.PLAYING)
    
    def test_quit_confirmation_yes(self):
        """Test quit confirmation with Y."""
        self.game.state = GameState.QUIT_CONFIRM
        
        # Simulate Y key press
        self.input_handler.add_key('y')
        self.game.handle_input()
        
        self.assertEqual(self.game.state, GameState.QUIT)
        self.assertFalse(self.game.running)
    
    def test_quit_confirmation_no(self):
        """Test quit confirmation with N."""
        self.game._previous_state = GameState.PLAYING
        self.game.state = GameState.QUIT_CONFIRM
        
        # Simulate N key press
        self.input_handler.add_key('n')
        self.game.handle_input()
        
        self.assertEqual(self.game.state, GameState.PLAYING)


if __name__ == '__main__':
    unittest.main()
