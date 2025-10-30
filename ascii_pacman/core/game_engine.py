"""Main game engine with improved organization."""

import time
from typing import Optional
from .constants import GameState, FRAME_TIME, Colors, GAME_WIDTH, GAME_HEIGHT, Score, Sprites
from .maze import Maze
from ..ui import Display, InputHandler
from ..entities import PacMan, GhostManager, Position
from ..data.levels import get_level


class GameEngine:
    """Main game engine that manages the game loop and state."""
    
    def __init__(self, display: Optional[Display] = None, input_handler: Optional[InputHandler] = None) -> None:
        """Initialize the game engine."""
        self.display = display or Display()
        self.input_handler = input_handler or InputHandler()
        
        # Game state
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
        
    def start(self) -> None:
        """Start the game engine."""
        try:
            self.display.clear_screen()
            self.display.hide_cursor()
            self.run_game_loop()
        except KeyboardInterrupt:
            self.quit()
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up resources."""
        self.display.show_cursor()
        self.input_handler.cleanup()
    
    def quit(self) -> None:
        """Quit the game."""
        self.state = GameState.QUIT
        self.running = False
    
    def run_game_loop(self) -> None:
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
    
    def update(self, delta_time: float) -> None:
        """Update game logic."""
        self.handle_input()
        
        state_updates = {
            GameState.MENU: self.update_menu,
            GameState.PLAYING: self.update_game,
            GameState.PAUSED: self.update_paused,
            GameState.GAME_OVER: self.update_game_over,
            GameState.QUIT_CONFIRM: self.update_quit_confirm
        }
        
        update_func = state_updates.get(self.state)
        if update_func:
            update_func(delta_time)
        elif self.state == GameState.QUIT:
            self.running = False
    
    def handle_input(self) -> None:
        """Process input based on current state."""
        key = self.input_handler.get_key()
        if key is None:
            return
        
        if self.state == GameState.QUIT_CONFIRM:
            self._handle_quit_confirm_input(key)
            return
        
        if self.input_handler.is_quit_key(key):
            self._show_quit_confirmation()
            return
        
        input_handlers = {
            GameState.MENU: self._handle_menu_input,
            GameState.PLAYING: self._handle_game_input,
            GameState.PAUSED: self._handle_paused_input,
            GameState.GAME_OVER: self._handle_game_over_input
        }
        
        handler = input_handlers.get(self.state)
        if handler:
            handler(key)
    
    def _handle_quit_confirm_input(self, key: str) -> None:
        """Handle input in quit confirmation state."""
        if key == 'y':
            self.quit()
        elif key == 'n' or key == ' ':
            # Return to previous state
            self.state = getattr(self, '_previous_state', GameState.MENU)
    
    def _show_quit_confirmation(self) -> None:
        """Show quit confirmation dialog."""
        self._previous_state = self.state
        self.state = GameState.QUIT_CONFIRM
    
    def _handle_menu_input(self, key: str) -> None:
        """Handle input in menu state."""
        if key == ' ' or key == '\n':
            self.state = GameState.PLAYING
    
    def _handle_game_input(self, key: str) -> None:
        """Handle input during gameplay."""
        if self.input_handler.is_pause_key(key):
            self.state = GameState.PAUSED
        else:
            # Handle movement input
            direction = self.input_handler.key_to_direction(key)
            if direction != (0, 0) and self.pacman:
                self.pacman.set_direction(direction)
    
    def _handle_paused_input(self, key: str) -> None:
        """Handle input while paused."""
        if self.input_handler.is_pause_key(key):
            self.state = GameState.PLAYING
    
    def _handle_game_over_input(self, key: str) -> None:
        """Handle input on game over screen."""
        if key == ' ' or key == '\n':
            self.reset_game()
            self.state = GameState.PLAYING
    
    def update_menu(self, delta_time: float) -> None:
        """Update menu state."""
        pass
    
    def update_game(self, delta_time: float) -> None:
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
        self._check_ghost_collisions()
    
    def _check_ghost_collisions(self) -> None:
        """Check and handle ghost-Pac-Man collisions."""
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
    
    def update_paused(self, delta_time: float) -> None:
        """Update paused state."""
        pass
    
    def update_game_over(self, delta_time: float) -> None:
        """Update game over state."""
        pass
    
    def update_quit_confirm(self, delta_time: float) -> None:
        """Update quit confirmation state."""
        pass
    
    def render(self) -> None:
        """Render the current game state."""
        self.display.clear_buffer()
        
        renderers = {
            GameState.MENU: self.render_menu,
            GameState.PLAYING: self._render_playing,
            GameState.PAUSED: self._render_paused,
            GameState.GAME_OVER: self.render_game_over,
            GameState.QUIT_CONFIRM: self._render_quit_confirm
        }
        
        renderer = renderers.get(self.state)
        if renderer:
            renderer()
        
        self.display.render()
    
    def _render_playing(self) -> None:
        """Render the playing state."""
        self.render_game()
    
    def _render_paused(self) -> None:
        """Render the paused state."""
        self.render_game()
        self.render_pause_overlay()
    
    def _render_quit_confirm(self) -> None:
        """Render the quit confirmation state."""
        self.render_game()
        self.render_quit_confirm()
    
    def render_menu(self) -> None:
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
    
    def render_game(self) -> None:
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
    
    def _render_maze(self) -> None:
        """Render the maze on the display."""
        # Calculate centered position
        maze_start_y = 3
        maze_start_x = (GAME_WIDTH - self.maze.width) // 2
        
        # Ensure maze fits in the display
        max_render_height = min(self.maze.height, GAME_HEIGHT - maze_start_y - 1)
        
        for y in range(max_render_height):
            for x in range(self.maze.width):
                char = self.maze.get_cell_char(x, y)
                color = self._get_maze_cell_color(char)
                self.display.set_char(maze_start_x + x, maze_start_y + y, char, color)
    
    def _get_maze_cell_color(self, char: str) -> str:
        """Get the appropriate color for a maze cell character."""
        color_map = {
            Sprites.WALL: Colors.BLUE,
            Sprites.DOT: Colors.WHITE,
            Sprites.POWER_PELLET: Colors.YELLOW,
            Sprites.GHOST_HOUSE_FLOOR: Colors.PINK
        }
        return color_map.get(char, Colors.WHITE)
    
    def _render_pacman(self) -> None:
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
    
    def _render_ghosts(self) -> None:
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
    
    def render_pause_overlay(self) -> None:
        """Render pause overlay with centered dialog box."""
        from ..core.constants import BorderChars
        
        self._render_dialog_box(
            "PAUSED",
            "Press SPACE to continue",
            28, 4
        )
    
    def render_quit_confirm(self) -> None:
        """Render quit confirmation overlay with centered dialog box."""
        self._render_dialog_box(
            "Are you sure you want to quit?",
            "Press Y to quit, N or SPACE to continue",
            44, 5
        )
    
    def _render_dialog_box(self, title: str, subtitle: str, width: int, height: int):
        """Render a centered dialog box with the given text."""
        from ..core.constants import BorderChars
        
        # Calculate box position
        box_x = (GAME_WIDTH - width) // 2
        box_y = GAME_HEIGHT // 2 - height // 2
        
        # Fill background with spaces
        for y in range(box_y, box_y + height):
            for x in range(box_x, box_x + width):
                self.display.set_char(x, y, ' ', Colors.BLACK)
        
        # Draw box border
        self._draw_box(box_x, box_y, width, height, Colors.YELLOW)
        
        # Draw text
        text_y = box_y + height // 2 - 1
        self.display.draw_centered_text(text_y, title, Colors.YELLOW)
        self.display.draw_centered_text(text_y + 1, subtitle, Colors.WHITE)
    
    def _draw_box(self, x: int, y: int, width: int, height: int, color: str):
        """Draw a box at the specified position."""
        from ..core.constants import BorderChars
        
        # Top and bottom borders
        for i in range(x, x + width):
            self.display.set_char(i, y, BorderChars.HORIZONTAL, color)
            self.display.set_char(i, y + height - 1, BorderChars.HORIZONTAL, color)
        
        # Left and right borders
        for j in range(y, y + height):
            self.display.set_char(x, j, BorderChars.VERTICAL, color)
            self.display.set_char(x + width - 1, j, BorderChars.VERTICAL, color)
        
        # Corners
        self.display.set_char(x, y, BorderChars.TOP_LEFT, color)
        self.display.set_char(x + width - 1, y, BorderChars.TOP_RIGHT, color)
        self.display.set_char(x, y + height - 1, BorderChars.BOTTOM_LEFT, color)
        self.display.set_char(x + width - 1, y + height - 1, BorderChars.BOTTOM_RIGHT, color)
    
    def render_game_over(self) -> None:
        """Render game over screen."""
        self.display.draw_border()
        
        center_y = GAME_HEIGHT // 2
        self.display.draw_centered_text(center_y - 2, "GAME OVER", Colors.RED)
        self.display.draw_centered_text(center_y, f"Final Score: {self.score:06d}", Colors.YELLOW)
        self.display.draw_centered_text(center_y + 2, "Press SPACE to play again", Colors.WHITE)
        self.display.draw_centered_text(center_y + 3, "Press Q to quit", Colors.WHITE)
    
    def _initialize_game(self) -> None:
        """Initialize the game objects for the current level."""
        layout = get_level(self.level)
        self.maze = Maze(layout)
        
        # Find a good starting position for Pac-Man
        start_pos = self._find_pacman_start_position()
        self.pacman = PacMan(start_pos.x, start_pos.y)
        
        # Initialize ghost manager
        self.ghost_manager = GhostManager(self.maze)
    
    def _find_pacman_start_position(self) -> Position:
        """Find a suitable starting position for Pac-Man."""
        from ..entities.base import Position
        
        # Start from bottom center and look for a dot
        start_x = self.maze.width // 2
        start_y = self.maze.height - 2
        
        # Search for a position with a dot
        search_radius = 5
        for y in range(start_y, max(self.maze.height // 2, 0), -1):
            for x in range(max(0, start_x - search_radius), 
                          min(self.maze.width, start_x + search_radius + 1)):
                if self.maze.is_walkable(x, y) and self.maze.has_dot(x, y):
                    return Position(x, y)
        
        # Fallback: find any walkable position
        for y in range(start_y, 0, -1):
            if self.maze.is_walkable(start_x, y):
                return Position(start_x, y)
        
        # Last resort: any walkable position
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.is_walkable(x, y):
                    return Position(x, y)
        
        return Position(1, 1)  # Default fallback
    
    def _reset_positions(self) -> None:
        """Reset Pac-Man and ghost positions after death."""
        if self.pacman:
            self.pacman.reset()
        if self.ghost_manager:
            self.ghost_manager.reset()
    
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.score = 0
        self.lives = 3
        self.level = 1
        self._initialize_game()
