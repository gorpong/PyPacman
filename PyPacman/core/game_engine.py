"""Main game engine with improved organization."""

import time
from typing import Optional
from .constants import GameState, FRAME_TIME, Colors, GAME_WIDTH, GAME_HEIGHT, Score, Sprites
from .maze import Maze
from .scoring import ScoringSystem
from .game_state import GameState as GameStateManager
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
        
        # Game systems
        self.scoring = ScoringSystem()
        self.game_state = GameStateManager(starting_lives=3)
        
        # Game objects
        self.maze = None
        self.pacman = None
        self.ghost_manager = None
        
        # High score entry
        self.player_name = ""
        
        # Visual effects
        self.score_popup = None  # (text, x, y, timer)
        self.death_timer = 0.0
        
        # Menu state
        self.menu_idle_timer = 0.0
        self.show_high_scores = False
        self.high_score_scroll_offset = 0.0
        
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
            GameState.HIGH_SCORE_ENTRY: self.update_high_score_entry,
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
            GameState.GAME_OVER: self._handle_game_over_input,
            GameState.HIGH_SCORE_ENTRY: self._handle_high_score_input
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
        # If showing high scores, any key dismisses them
        if self.show_high_scores:
            self.show_high_scores = False
            self.menu_idle_timer = 0.0
            self.high_score_scroll_offset = 0.0
            return
        
        # Otherwise, space starts the game
        if key == ' ' or key == '\n':
            self.state = GameState.PLAYING
            self.menu_idle_timer = 0.0
            self.show_high_scores = False
    
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
    
    def _handle_high_score_input(self, key: str) -> None:
        """Handle input for high score name entry."""
        if key in ['\n', '\r', '\x0d', '\x0a']:  # Enter/Return - submit name
            if self.player_name:
                self.scoring.add_high_score(self.player_name)
            self.state = GameState.GAME_OVER
        elif key == '\x7f' or key == '\x08':  # Backspace
            if self.player_name:
                self.player_name = self.player_name[:-1]
        elif len(key) == 1 and (key.isalnum() or key == ' ') and len(self.player_name) < 20:
            # Add character if alphanumeric and under 20 chars
            self.player_name += key.upper()
    
    def update_menu(self, delta_time: float) -> None:
        """Update menu state."""
        # Track idle time
        self.menu_idle_timer += delta_time
        
        # Show high scores after 10 seconds of inactivity
        if self.menu_idle_timer >= 10.0 and not self.show_high_scores:
            self.show_high_scores = True
            self.high_score_scroll_offset = 0.0
        
        # Animate scroll if showing high scores
        if self.show_high_scores:
            self.high_score_scroll_offset += delta_time * 2.0  # Scroll speed
    
    def update_game(self, delta_time: float) -> None:
        """Update game state."""
        if not self.pacman or not self.maze or not self.ghost_manager:
            return
        
        # Update score popup timer
        if self.score_popup:
            text, x, y, timer = self.score_popup
            timer -= delta_time
            if timer <= 0:
                self.score_popup = None
            else:
                self.score_popup = (text, x, y, timer)
        
        # Handle death pause
        if self.death_timer > 0:
            self.death_timer -= delta_time
            return  # Don't update anything else during death
            
        # Update Pac-Man
        self.pacman.update(delta_time, self.maze)
        
        # Check dot collection
        px, py = self.pacman.get_position()
        if self.maze.collect_dot(px, py):
            self.scoring.add_dot()
            
        # Check power pellet collection
        if self.maze.collect_power_pellet(px, py):
            points = self.scoring.add_power_pellet()
            self.ghost_manager.make_all_vulnerable()
            # Reset ghost combo when eating new power pellet
            self.scoring.reset_ghost_combo()
            # Show score popup
            self.score_popup = (f"+{points}", px, py, 1.0)
            
        # Check level completion
        if self.maze.is_level_complete():
            self.game_state.next_level()
            self._initialize_game()
            
        # Update ghosts
        self.ghost_manager.update(delta_time, self.maze, self.pacman)
        
        # Reset ghost combo if vulnerability expired
        if self.ghost_manager.vulnerability_expired:
            self.scoring.reset_ghost_combo()
        
        # Check ghost collisions
        self._check_ghost_collisions()
    
    def _check_ghost_collisions(self) -> None:
        """Check and handle ghost-Pac-Man collisions."""
        colliding_ghost = self.ghost_manager.check_collision_with_pacman(self.pacman)
        if colliding_ghost:
            if colliding_ghost.is_vulnerable():
                # Eat the ghost - show score popup
                points = self.scoring.add_ghost()
                px, py = self.pacman.get_position()
                self.score_popup = (f"+{points}", px, py, 1.0)
            elif colliding_ghost.is_dangerous():
                # Pac-Man dies - pause for effect
                self.death_timer = 1.5  # 1.5 second pause
                game_over = self.game_state.lose_life()
                if game_over:
                    # Check for high score
                    if self.scoring.is_high_score():
                        self.state = GameState.HIGH_SCORE_ENTRY
                        self.player_name = ""
                    else:
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
    
    def update_high_score_entry(self, delta_time: float) -> None:
        """Update high score entry state."""
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
            GameState.HIGH_SCORE_ENTRY: self.render_high_score_entry,
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
        
        if self.show_high_scores:
            self._render_scrolling_high_scores()
        else:
            title_y = 8
            self.display.draw_centered_text(title_y, "ASCII PAC-MAN", Colors.YELLOW)
            
            controls_y = title_y + 4
            self.display.draw_centered_text(controls_y, "Controls:", Colors.WHITE)
            self.display.draw_centered_text(controls_y + 1, "Arrow Keys or WASD to move", Colors.WHITE)
            self.display.draw_centered_text(controls_y + 2, "SPACE to pause, Q to quit", Colors.WHITE)
            
            start_y = controls_y + 5
            self.display.draw_centered_text(start_y, "Press SPACE to start!", Colors.YELLOW)
    
    def _render_scrolling_high_scores(self) -> None:
        """Render scrolling high scores display."""
        # Title
        self.display.draw_centered_text(3, "HIGH SCORES", Colors.YELLOW)
        
        # Get high scores
        high_scores = self.scoring.get_high_scores()
        
        if not high_scores:
            self.display.draw_centered_text(10, "No high scores yet!", Colors.WHITE)
            self.display.draw_centered_text(GAME_HEIGHT - 3, "Press any key to continue", Colors.CYAN)
            return
        
        # Calculate scroll position (loop the list)
        scroll_lines = int(self.high_score_scroll_offset)
        
        # Display area (rows 5 to HEIGHT-5)
        display_start = 5
        display_end = GAME_HEIGHT - 5
        display_height = display_end - display_start
        
        # Render visible scores with scrolling
        for i in range(display_height):
            score_index = (scroll_lines + i) % len(high_scores)
            name, points = high_scores[score_index]
            
            # Format: rank. name  score
            rank = score_index + 1
            score_text = f"{rank:2}. {name[:15]:15} {points:06d}"
            
            y_pos = display_start + i
            if display_start <= y_pos < display_end:
                # Fade effect at edges
                if i == 0 or i == display_height - 1:
                    color = Colors.WHITE
                else:
                    color = Colors.CYAN
                self.display.draw_centered_text(y_pos, score_text, color)
        
        # Instructions
        self.display.draw_centered_text(GAME_HEIGHT - 3, "Press any key to continue", Colors.YELLOW)
    
    def render_game(self) -> None:
        """Render the main game."""
        self.display.draw_border()
        
        # Draw UI at top
        score = self.scoring.get_score()
        high_score = self.scoring.get_high_score()
        lives = self.game_state.get_lives()
        level = self.game_state.get_level()
        
        self.display.set_string(2, 1, f"Score: {score:06d}", Colors.YELLOW)
        self.display.set_string(22, 1, f"High: {high_score:06d}", Colors.CYAN)
        self.display.set_string(42, 1, f"Lives: {lives}", Colors.RED)
        self.display.set_string(GAME_WIDTH - 12, 1, f"Level: {level}", Colors.CYAN)
        
        # Draw maze starting at row 3 (below UI)
        if self.maze:
            self._render_maze()
        
        # Draw Pac-Man
        if self.pacman:
            self._render_pacman()
            
        # Draw ghosts
        if self.ghost_manager:
            self._render_ghosts()
        
        # Draw score popup if active
        if self.score_popup:
            text, x, y, timer = self.score_popup
            maze_start_y = 3
            maze_start_x = (GAME_WIDTH - self.maze.width) // 2
            screen_x = maze_start_x + x
            screen_y = maze_start_y + y - 1  # Above the position
            self.display.set_string(screen_x - len(text)//2, screen_y, text, Colors.YELLOW)
    
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
        
        score = self.scoring.get_score()
        high_scores = self.scoring.get_high_scores()
        
        # Show high scores leaderboard
        y = 3
        self.display.draw_centered_text(y, "HIGH SCORES", Colors.YELLOW)
        y += 2
        
        # Display top 10 scores
        for i, (name, points) in enumerate(high_scores[:10]):
            rank = f"{i+1:2}."
            score_text = f"{rank} {name[:15]:15} {points:06d}"
            color = Colors.CYAN if points == score else Colors.WHITE
            self.display.draw_centered_text(y + i, score_text, color)
        
        # Game over message
        self.display.draw_centered_text(GAME_HEIGHT - 5, "GAME OVER", Colors.RED)
        self.display.draw_centered_text(GAME_HEIGHT - 3, "Press SPACE to play again", Colors.WHITE)
        self.display.draw_centered_text(GAME_HEIGHT - 2, "Press Q to quit", Colors.WHITE)
    
    def render_high_score_entry(self) -> None:
        """Render high score entry screen."""
        self.display.draw_border()
        
        center_y = GAME_HEIGHT // 2
        score = self.scoring.get_score()
        
        self.display.draw_centered_text(center_y - 4, "NEW HIGH SCORE!", Colors.YELLOW)
        self.display.draw_centered_text(center_y - 2, f"Score: {score:06d}", Colors.CYAN)
        self.display.draw_centered_text(center_y, "Enter your name:", Colors.WHITE)
        
        # Draw input box
        box_width = 24
        box_x = (GAME_WIDTH - box_width) // 2
        self.display.set_string(box_x, center_y + 2, "┌" + "─" * (box_width - 2) + "┐", Colors.WHITE)
        self.display.set_string(box_x, center_y + 3, "│" + " " * (box_width - 2) + "│", Colors.WHITE)
        self.display.set_string(box_x, center_y + 4, "└" + "─" * (box_width - 2) + "┘", Colors.WHITE)
        
        # Draw entered name
        name_x = box_x + 2
        self.display.set_string(name_x, center_y + 3, self.player_name, Colors.YELLOW)
        
        # Draw cursor
        cursor_x = name_x + len(self.player_name)
        if int(time.time() * 2) % 2:  # Blinking cursor
            self.display.set_char(cursor_x, center_y + 3, "█", Colors.YELLOW)
        
        self.display.draw_centered_text(center_y + 6, "Press ENTER when done", Colors.WHITE)
    
    def _initialize_game(self) -> None:
        """Initialize the game objects for the current level."""
        layout = get_level(self.game_state.get_level())
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
        self.scoring.reset()
        self.game_state.reset()
        self._initialize_game()
