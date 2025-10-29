"""
Main game engine and loop.
Handles game state, timing, and coordination between components.
"""

import time
import sys
import os
from typing import Optional
from .constants import GameState, FRAME_TIME, Colors, GAME_WIDTH, GAME_HEIGHT, Score, BorderChars, Sprites

# Add data directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))

from .display import Display
from .input_handler import InputHandler
from .maze import Maze
from .pacman import PacMan
from .ghost_manager import GhostManager
from data.levels import get_level


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
        
        # Game objects
        self.maze = None
        self.pacman = None
        self.ghost_manager = None
        self._initialize_game()
        
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
        elif self.state == GameState.QUIT_CONFIRM:
            self.update_quit_confirm(delta_time)
        elif self.state == GameState.QUIT:
            self.running = False
    
    def handle_input(self):
        """Process input based on current state."""
        key = self.input_handler.get_key()
        if key is None:
            return
        
        if self.state == GameState.QUIT_CONFIRM:
            if key == 'y':
                self.quit()
            elif key == 'n' or key == ' ':
                # Return to previous state (we'll store it)
                self.state = getattr(self, '_previous_state', GameState.MENU)
            return
        
        if self.input_handler.is_quit_key(key):
            # Store current state and show confirmation
            self._previous_state = self.state
            self.state = GameState.QUIT_CONFIRM
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
                if direction != (0, 0) and self.pacman:
                    self.pacman.set_direction(direction)
        
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
        if not self.pacman or not self.maze or not self.ghost_manager:
            return
            
        # Update Pac-Man
        self.pacman.update(delta_time, self.maze)
        
        # Check dot collection
        px, py = self.pacman.get_position()
        if self.maze.collect_dot(px, py):
            self.score += Score.DOT
            
        # Check power pellet collection
        if self.maze.collect_power_pellet(px, py):
            self.score += Score.POWER_PELLET
            self.ghost_manager.make_all_vulnerable()
            
        # Check level completion
        if self.maze.is_level_complete():
            self.level += 1
            self._initialize_game()
            
        # Update ghosts
        self.ghost_manager.update(delta_time, self.maze, self.pacman)
        
        # Check ghost collisions
        colliding_ghost = self.ghost_manager.check_collision_with_pacman(self.pacman)
        if colliding_ghost:
            if colliding_ghost.is_vulnerable():
                # Eat the ghost
                points = self.ghost_manager.eat_ghost(colliding_ghost)
                self.score += points
            elif colliding_ghost.is_dangerous():
                # Pac-Man dies
                self.lives -= 1
                if self.lives <= 0:
                    self.state = GameState.GAME_OVER
                else:
                    # Reset positions but keep score
                    self._reset_positions()
    
    def update_paused(self, delta_time: float):
        """Update paused state."""
        pass
    
    def update_game_over(self, delta_time: float):
        """Update game over state."""
        pass
    
    def update_quit_confirm(self, delta_time: float):
        """Update quit confirmation state."""
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
        elif self.state == GameState.QUIT_CONFIRM:
            self.render_game()
            self.render_quit_confirm()
        
        self.display.render()
    
    def render_menu(self):
        """Render the main menu."""
        self.display.draw_border()
        
        title_y = 8
        self.display.draw_centered_text(title_y, "ASCII PAC-MAN", Colors.YELLOW)
        
        controls_y = title_y + 4
        self.display.draw_centered_text(controls_y, "Controls:", Colors.WHITE)
        self.display.draw_centered_text(controls_y + 1, "Arrow Keys or WASD to move", Colors.WHITE)
        self.display.draw_centered_text(controls_y + 2, "SPACE to pause, Q to quit", Colors.WHITE)
        
        start_y = controls_y + 5
        self.display.draw_centered_text(start_y, "Press SPACE to start!", Colors.YELLOW)
    
    def render_game(self):
        """Render the main game."""
        self.display.draw_border()
        
        # Draw UI at top
        self.display.set_string(2, 1, f"Score: {self.score:06d}", Colors.YELLOW)
        self.display.set_string(25, 1, f"Lives: {self.lives}", Colors.RED)
        self.display.set_string(GAME_WIDTH - 12, 1, f"Level: {self.level}", Colors.CYAN)
        
        # Draw maze starting at row 3 (below UI)
        if self.maze:
            self._render_maze()
        
        # Draw Pac-Man
        if self.pacman:
            self._render_pacman()
            
        # Draw ghosts
        if self.ghost_manager:
            self._render_ghosts()
    
    def _render_maze(self):
        """Render the maze on the display."""
        # Center the maze in the playable area
        maze_start_y = 3
        maze_start_x = (GAME_WIDTH - self.maze.width) // 2
        
        # Ensure maze fits in the display
        max_render_height = GAME_HEIGHT - maze_start_y - 1
        
        for y in range(min(self.maze.height, max_render_height)):
            for x in range(self.maze.width):
                char = self.maze.get_cell_char(x, y)
                
                # Choose color based on cell type  
                if char == Sprites.WALL:
                    color = Colors.BLUE
                elif char == Sprites.DOT:
                    color = Colors.WHITE
                elif char == Sprites.POWER_PELLET:
                    color = Colors.YELLOW
                elif char == Sprites.GHOST_HOUSE_FLOOR:
                    color = Colors.PINK
                else:
                    color = Colors.WHITE
                
                self.display.set_char(maze_start_x + x, maze_start_y + y, char, color)
    
    def render_pause_overlay(self):
        """Render pause overlay."""
        # Draw a box for the pause dialog
        box_width = 28
        box_height = 4
        box_x = (GAME_WIDTH - box_width) // 2
        box_y = GAME_HEIGHT // 2 - box_height // 2
        
        # Fill background with spaces
        for y in range(box_y, box_y + box_height):
            for x in range(box_x, box_x + box_width):
                self.display.set_char(x, y, ' ', Colors.BLACK)
        
        # Draw box border
        # Top and bottom
        for x in range(box_x, box_x + box_width):
            self.display.set_char(x, box_y, BorderChars.HORIZONTAL, Colors.YELLOW)
            self.display.set_char(x, box_y + box_height - 1, BorderChars.HORIZONTAL, Colors.YELLOW)
        
        # Left and right
        for y in range(box_y, box_y + box_height):
            self.display.set_char(box_x, y, BorderChars.VERTICAL, Colors.YELLOW)
            self.display.set_char(box_x + box_width - 1, y, BorderChars.VERTICAL, Colors.YELLOW)
        
        # Corners
        self.display.set_char(box_x, box_y, BorderChars.TOP_LEFT, Colors.YELLOW)
        self.display.set_char(box_x + box_width - 1, box_y, BorderChars.TOP_RIGHT, Colors.YELLOW)
        self.display.set_char(box_x, box_y + box_height - 1, BorderChars.BOTTOM_LEFT, Colors.YELLOW)
        self.display.set_char(box_x + box_width - 1, box_y + box_height - 1, BorderChars.BOTTOM_RIGHT, Colors.YELLOW)
        
        # Draw text
        self.display.draw_centered_text(box_y + 1, "PAUSED", Colors.YELLOW)
        self.display.draw_centered_text(box_y + 2, "Press SPACE to continue", Colors.WHITE)
    
    def render_quit_confirm(self):
        """Render quit confirmation overlay."""
        # Draw a box for the confirmation dialog
        box_width = 44
        box_height = 5
        box_x = (GAME_WIDTH - box_width) // 2
        box_y = GAME_HEIGHT // 2 - box_height // 2
        
        # Fill background with spaces
        for y in range(box_y, box_y + box_height):
            for x in range(box_x, box_x + box_width):
                self.display.set_char(x, y, ' ', Colors.BLACK)
        
        # Draw box border
        # Top and bottom
        for x in range(box_x, box_x + box_width):
            self.display.set_char(x, box_y, BorderChars.HORIZONTAL, Colors.YELLOW)
            self.display.set_char(x, box_y + box_height - 1, BorderChars.HORIZONTAL, Colors.YELLOW)
        
        # Left and right
        for y in range(box_y, box_y + box_height):
            self.display.set_char(box_x, y, BorderChars.VERTICAL, Colors.YELLOW)
            self.display.set_char(box_x + box_width - 1, y, BorderChars.VERTICAL, Colors.YELLOW)
        
        # Corners
        self.display.set_char(box_x, box_y, BorderChars.TOP_LEFT, Colors.YELLOW)
        self.display.set_char(box_x + box_width - 1, box_y, BorderChars.TOP_RIGHT, Colors.YELLOW)
        self.display.set_char(box_x, box_y + box_height - 1, BorderChars.BOTTOM_LEFT, Colors.YELLOW)
        self.display.set_char(box_x + box_width - 1, box_y + box_height - 1, BorderChars.BOTTOM_RIGHT, Colors.YELLOW)
        
        # Draw text
        self.display.draw_centered_text(box_y + 2, "Are you sure you want to quit?", Colors.YELLOW)
        self.display.draw_centered_text(box_y + 3, "Press Y to quit, N or SPACE to continue", Colors.WHITE)
    
    def render_game_over(self):
        """Render game over screen."""
        self.display.draw_border()
        
        center_y = GAME_HEIGHT // 2
        self.display.draw_centered_text(center_y - 2, "GAME OVER", Colors.RED)
        self.display.draw_centered_text(center_y, f"Final Score: {self.score:06d}", Colors.YELLOW)
        self.display.draw_centered_text(center_y + 2, "Press SPACE to play again", Colors.WHITE)
        self.display.draw_centered_text(center_y + 3, "Press Q to quit", Colors.WHITE)
    
    def _render_pacman(self):
        """Render Pac-Man on the display."""
        if not self.pacman or not self.maze:
            return
            
        # Calculate position on screen
        maze_start_y = 3
        maze_start_x = (GAME_WIDTH - self.maze.width) // 2
        
        px, py = self.pacman.get_position()
        screen_x = maze_start_x + px
        screen_y = maze_start_y + py
        
        # Draw Pac-Man sprite
        sprite = self.pacman.get_sprite()
        self.display.set_char(screen_x, screen_y, sprite, Colors.YELLOW)
    
    def _initialize_game(self):
        """Initialize the game objects for the current level."""
        layout = get_level(self.level)
        self.maze = Maze(layout)
        
        # Find a good starting position for Pac-Man 
        # Start from bottom center and look for a dot
        start_x = self.maze.width // 2
        start_y = self.maze.height - 2
        
        # Look for a position with a dot near the bottom center
        found = False
        for y in range(start_y, self.maze.height // 2, -1):
            for x in range(start_x - 5, start_x + 5):
                if self.maze.is_walkable(x, y) and self.maze.has_dot(x, y):
                    start_x, start_y = x, y
                    found = True
                    break
            if found:
                break
        
        # Fallback: find any walkable position
        if not found:
            for y in range(start_y, 0, -1):
                if self.maze.is_walkable(start_x, y):
                    start_y = y
                    break
                    
        self.pacman = PacMan(start_x, start_y)
        self.ghost_manager = GhostManager(self.maze)
    
    def _render_ghosts(self):
        """Render all ghosts on the display."""
        if not self.ghost_manager or not self.maze:
            return
            
        # Calculate maze position on screen
        maze_start_y = 3
        maze_start_x = (GAME_WIDTH - self.maze.width) // 2
        
        # Get all ghost positions and render them
        for x, y, sprite, color in self.ghost_manager.get_ghost_positions():
            screen_x = maze_start_x + x
            screen_y = maze_start_y + y
            self.display.set_char(screen_x, screen_y, sprite, color)
    
    def _reset_positions(self):
        """Reset Pac-Man and ghost positions after death."""
        if self.pacman:
            self.pacman.reset()
        if self.ghost_manager:
            self.ghost_manager.reset()
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.score = 0
        self.lives = 3
        self.level = 1
        self._initialize_game()
