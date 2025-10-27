"""
Main game engine and loop.
Handles game state, timing, and coordination between components.
"""

import time
from typing import Optional
from .constants import GameState, FRAME_TIME, Colors, GAME_WIDTH, GAME_HEIGHT
from .display import Display
from .input_handler import InputHandler


class GameEngine:
    """Main game engine that manages the game loop and state."""
    
    def __init__(self, display: Optional[Display] = None, input_handler: Optional[InputHandler] = None):
        self.display = display or Display()
        self.input_handler = input_handler or InputHandler()
        
        self.state = GameState.MENU
        self.running = True
        self.last_frame_time = 0.0
        self.paused = False
        
        # Game statistics
        self.score = 0
        self.lives = 3
        self.level = 1
        
    def start(self):
        """Start the game engine."""
        try:
            self.display.clear_screen()
            self.display.hide_cursor()
            self.run_game_loop()
        except KeyboardInterrupt:
            self.quit()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        self.display.show_cursor()
        self.input_handler.cleanup()
    
    def quit(self):
        """Quit the game."""
        self.state = GameState.QUIT
        self.running = False
    
    def run_game_loop(self):
        """Main game loop."""
        self.last_frame_time = time.time()
        
        while self.running:
            current_time = time.time()
            delta_time = current_time - self.last_frame_time
            
            # Maintain target frame rate
            if delta_time >= FRAME_TIME:
                self.update(delta_time)
                self.render()
                self.last_frame_time = current_time
            else:
                # Sleep for a short time to avoid busy waiting
                time.sleep(0.001)
    
    def update(self, delta_time: float):
        """Update game logic."""
        self.handle_input()
        
        if self.state == GameState.MENU:
            self.update_menu(delta_time)
        elif self.state == GameState.PLAYING:
            self.update_game(delta_time)
        elif self.state == GameState.PAUSED:
            self.update_paused(delta_time)
        elif self.state == GameState.GAME_OVER:
            self.update_game_over(delta_time)
        elif self.state == GameState.QUIT:
            self.running = False
    
    def handle_input(self):
        """Process input based on current state."""
        key = self.input_handler.get_key()
        if key is None:
            return
        
        if self.input_handler.is_quit_key(key):
            self.quit()
            return
        
        if self.state == GameState.MENU:
            if key == ' ' or key == '\n':
                self.state = GameState.PLAYING
        
        elif self.state == GameState.PLAYING:
            if self.input_handler.is_pause_key(key):
                self.state = GameState.PAUSED
            else:
                # Handle movement input
                direction = self.input_handler.key_to_direction(key)
                if direction != (0, 0):
                    # TODO: Update Pac-Man direction
                    pass
        
        elif self.state == GameState.PAUSED:
            if self.input_handler.is_pause_key(key):
                self.state = GameState.PLAYING
        
        elif self.state == GameState.GAME_OVER:
            if key == ' ' or key == '\n':
                self.reset_game()
                self.state = GameState.PLAYING
    
    def update_menu(self, delta_time: float):
        """Update menu state."""
        pass
    
    def update_game(self, delta_time: float):
        """Update game state."""
        # TODO: Update Pac-Man position
        # TODO: Update ghosts
        # TODO: Check collisions
        # TODO: Check win/lose conditions
        pass
    
    def update_paused(self, delta_time: float):
        """Update paused state."""
        pass
    
    def update_game_over(self, delta_time: float):
        """Update game over state."""
        pass
    
    def render(self):
        """Render the current game state."""
        self.display.clear_buffer()
        
        if self.state == GameState.MENU:
            self.render_menu()
        elif self.state == GameState.PLAYING:
            self.render_game()
        elif self.state == GameState.PAUSED:
            self.render_game()
            self.render_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self.render_game_over()
        
        self.display.render()
    
    def render_menu(self):
        """Render the main menu."""
        self.display.draw_border()
        
        title_y = 8
        self.display.draw_centered_text(title_y, "ASCII PAC-MAN", Colors.YELLOW)
        
        controls_y = title_y + 4
        self.display.draw_centered_text(controls_y, "Controls:", Colors.WHITE)
        self.display.draw_centered_text(controls_y + 1, "Arrow Keys or WASD to move", Colors.WHITE)
        self.display.draw_centered_text(controls_y + 2, "SPACE to pause, ESC to quit", Colors.WHITE)
        
        start_y = controls_y + 5
        self.display.draw_centered_text(start_y, "Press SPACE to start!", Colors.YELLOW)
    
    def render_game(self):
        """Render the main game."""
        self.display.draw_border()
        
        # Draw UI
        self.display.set_string(2, 1, f"Score: {self.score:06d}", Colors.YELLOW)
        self.display.set_string(2, 2, f"Lives: {self.lives}", Colors.RED)
        self.display.set_string(GAME_WIDTH - 12, 1, f"Level: {self.level}", Colors.CYAN)
        
        # TODO: Draw maze
        # TODO: Draw Pac-Man
        # TODO: Draw ghosts
        # TODO: Draw dots and power pellets
    
    def render_pause_overlay(self):
        """Render pause overlay."""
        overlay_y = GAME_HEIGHT // 2
        self.display.draw_centered_text(overlay_y, "PAUSED", Colors.YELLOW)
        self.display.draw_centered_text(overlay_y + 1, "Press SPACE to continue", Colors.WHITE)
    
    def render_game_over(self):
        """Render game over screen."""
        self.display.draw_border()
        
        center_y = GAME_HEIGHT // 2
        self.display.draw_centered_text(center_y - 2, "GAME OVER", Colors.RED)
        self.display.draw_centered_text(center_y, f"Final Score: {self.score:06d}", Colors.YELLOW)
        self.display.draw_centered_text(center_y + 2, "Press SPACE to play again", Colors.WHITE)
        self.display.draw_centered_text(center_y + 3, "Press ESC to quit", Colors.WHITE)
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.score = 0
        self.lives = 3
        self.level = 1
        # TODO: Reset Pac-Man position
        # TODO: Reset ghosts
        # TODO: Reset maze state
