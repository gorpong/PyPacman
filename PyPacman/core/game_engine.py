"""Main game engine with improved organization."""
from __future__ import annotations

import time
from typing import Callable

from ..data.levels import get_level
from ..entities.ghost_manager import GhostManager
from ..entities.pacman import PacMan
from ..ui.display import Display
from ..ui.input_handler import InputHandler
from .colors import Colors
from .config import FRAME_TIME, GAME_HEIGHT, GAME_WIDTH
from .game_state import GameState
from .maze import Maze
from .scoring import ScoringSystem
from .sprites import BorderChars, Sprites
from .types import GameMode, Position


class GameEngine:
    """Main game engine that manages the game loop and state."""

    def __init__(
            self,
            display: Display | None = None,
            input_handler: InputHandler | None = None
    ) -> None:
        """Initialize the game engine."""
        self.display: Display = display or Display()
        self.input_handler: InputHandler = input_handler or InputHandler()

        self.mode: GameMode = GameMode.MENU
        self.running: bool = True
        self.last_frame_time: float = 0.0
        self.paused: bool = False

        self.scoring: ScoringSystem = ScoringSystem()
        self.game_state: GameState = GameState(starting_lives=3)

        self.maze: Maze | None = None
        self.pacman: PacMan | None = None
        self.ghost_manager: GhostManager | None = None

        self.previous_pacman_pos: Position | None = None

        self.player_name: str = ""

        self.score_popup: tuple[str, int, int, float] | None = None
        self.death_timer: float = 0.0

        self.menu_idle_timer: float = 0.0
        self.show_high_scores: bool = False
        self.high_score_scroll_offset: float = 0.0

        self._initialize_game()

    # Keep 'state' as property for backwards compat with tests
    @property
    def state(self) -> GameMode:
        return self.mode

    @state.setter
    def state(self, value: GameMode) -> None:
        self.mode = value

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
        self.mode = GameMode.QUIT
        self.running = False

    def run_game_loop(self) -> None:
        """Main game loop."""
        self.last_frame_time = time.time()

        while self.running:
            current_time = time.time()
            delta_time = current_time - self.last_frame_time

            if delta_time >= FRAME_TIME:
                self.update(delta_time)
                self.render()
                self.last_frame_time = current_time
            else:
                time.sleep(0.001)

    def update(self, delta_time: float) -> None:
        """Update game logic."""
        self.handle_input()

        state_updates: dict[GameMode, Callable] = {
            GameMode.MENU: self.update_menu,
            GameMode.PLAYING: self.update_game,
            GameMode.PAUSED: self.update_paused,
            GameMode.GAME_OVER: self.update_game_over,
            GameMode.HIGH_SCORE_ENTRY: self.update_high_score_entry,
            GameMode.QUIT_CONFIRM: self.update_quit_confirm
        }

        update_func = state_updates.get(self.mode)
        if update_func:
            update_func(delta_time)
        elif self.mode == GameMode.QUIT:
            self.running = False

    def handle_input(self) -> None:
        """Process input based on current state."""
        key = self.input_handler.get_key()
        if key is None:
            return

        if self.mode == GameMode.QUIT_CONFIRM:
            self._handle_quit_confirm_input(key)
            return

        if self.input_handler.is_quit_key(key):
            self._show_quit_confirmation()
            return

        input_handlers = {
            GameMode.MENU: self._handle_menu_input,
            GameMode.PLAYING: self._handle_game_input,
            GameMode.PAUSED: self._handle_paused_input,
            GameMode.GAME_OVER: self._handle_game_over_input,
            GameMode.HIGH_SCORE_ENTRY: self._handle_high_score_input
        }

        handler = input_handlers.get(self.mode)
        if handler:
            handler(key)

    def _handle_quit_confirm_input(self, key: str) -> None:
        """Handle input in quit confirmation state."""
        if key == 'y':
            self.quit()
        elif key == 'n' or key == ' ':
            self.mode = getattr(self, '_previous_mode', GameMode.MENU)

    def _show_quit_confirmation(self) -> None:
        """Show quit confirmation dialog."""
        self._previous_mode = self.mode
        self.mode = GameMode.QUIT_CONFIRM

    def _handle_menu_input(self, key: str) -> None:
        """Handle input in menu state."""
        if self.show_high_scores:
            self.show_high_scores = False
            self.menu_idle_timer = 0.0
            self.high_score_scroll_offset = 0.0
            return

        if key == ' ' or key == '\n':
            self.mode = GameMode.PLAYING
            self.menu_idle_timer = 0.0
            self.show_high_scores = False

    def _handle_game_input(self, key: str) -> None:
        """Handle input during gameplay."""
        if self.input_handler.is_pause_key(key):
            self.mode = GameMode.PAUSED
        else:
            direction = self.input_handler.key_to_direction(key)
            if direction != (0, 0) and self.pacman:
                self.pacman.set_direction(direction)

    def _handle_paused_input(self, key: str) -> None:
        """Handle input while paused."""
        if self.input_handler.is_pause_key(key):
            self.mode = GameMode.PLAYING

    def _handle_game_over_input(self, key: str) -> None:
        """Handle input on game over screen."""
        if key == ' ' or key == '\n':
            self.reset_game()
            self.mode = GameMode.PLAYING

    def _handle_high_score_input(self, key: str) -> None:
        """Handle input for high score name entry."""
        if key in ['\n', '\r', '\x0d', '\x0a']:
            if self.player_name:
                self.scoring.add_high_score(self.player_name)
            self.mode = GameMode.GAME_OVER
        elif key == '\x7f' or key == '\x08':
            if self.player_name:
                self.player_name = self.player_name[:-1]
        elif len(key) == 1 and (key.isalnum() or key == ' ') and len(self.player_name) < 20:
            self.player_name += key.upper()

    def update_menu(self, delta_time: float) -> None:
        """Update menu state."""
        self.menu_idle_timer += delta_time

        if self.menu_idle_timer >= 10.0 and not self.show_high_scores:
            self.show_high_scores = True
            self.high_score_scroll_offset = 0.0

        if self.show_high_scores:
            self.high_score_scroll_offset += delta_time * 2.0

    def update_game(self, delta_time: float) -> None:
        """Update game state."""
        if not self.pacman or not self.maze or not self.ghost_manager:
            return

        if self.score_popup:
            text, x, y, timer = self.score_popup
            timer -= delta_time
            if timer <= 0:
                self.score_popup = None
            else:
                self.score_popup = (text, x, y, timer)

        if self.death_timer > 0:
            self.death_timer -= delta_time
            return

        self.previous_pacman_pos = self.pacman.get_position()

        self.pacman.update(delta_time, self.maze)

        pac_pos = self.pacman.get_position()
        px, py = pac_pos.x, pac_pos.y
        if self.maze.collect_dot(px, py):
            self.scoring.add_dot()

        if self.maze.collect_power_pellet(px, py):
            points = self.scoring.add_power_pellet()
            self.ghost_manager.make_all_vulnerable()
            self.scoring.reset_ghost_combo()
            self.score_popup = (f"+{points}", px, py, 1.0)

        if self.maze.is_level_complete():
            self.game_state.next_level()
            self._initialize_game()
            return

        self.ghost_manager.update(delta_time, self.maze, self.pacman)

        if self.ghost_manager.vulnerability_expired:
            self.scoring.reset_ghost_combo()

        self._check_ghost_collisions()

    def _check_ghost_collisions(self) -> None:
        """Check and handle ghost-Pac-Man collisions."""
        colliding_ghost = self.ghost_manager.check_collision_with_pacman(
            self.pacman,
            self.previous_pacman_pos
        )

        if colliding_ghost:
            if colliding_ghost.is_vulnerable():
                eaten_count = self.ghost_manager.ghosts_eaten_in_sequence
                points = 200 * (2 ** (eaten_count - 1))
                points = min(points, 1600)
                pac_pos = self.pacman.get_position()
                self.score_popup = (f"+{points}", pac_pos.x, pac_pos.y, 1.0)
                self.scoring.add_ghost()
            elif colliding_ghost.is_dangerous():
                self.death_timer = 1.5
                game_over = self.game_state.lose_life()
                if game_over:
                    if self.scoring.is_high_score():
                        self.mode = GameMode.HIGH_SCORE_ENTRY
                        self.player_name = ""
                    else:
                        self.mode = GameMode.GAME_OVER
                else:
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

        renderers: dict[GameMode, Callable] = {
            GameMode.MENU: self.render_menu,
            GameMode.PLAYING: self._render_playing,
            GameMode.PAUSED: self._render_paused,
            GameMode.GAME_OVER: self.render_game_over,
            GameMode.HIGH_SCORE_ENTRY: self.render_high_score_entry,
            GameMode.QUIT_CONFIRM: self._render_quit_confirm
        }

        renderer = renderers.get(self.mode)
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
        self.display.draw_centered_text(3, "HIGH SCORES", Colors.YELLOW)

        high_scores = self.scoring.get_high_scores()

        if not high_scores:
            self.display.draw_centered_text(10, "No high scores yet!", Colors.WHITE)
            self.display.draw_centered_text(GAME_HEIGHT - 3, "Press any key to continue", Colors.CYAN)
            return

        scroll_lines = int(self.high_score_scroll_offset)

        display_start = 5
        display_end = GAME_HEIGHT - 5
        display_height = display_end - display_start

        for i in range(display_height):
            score_index = (scroll_lines + i) % len(high_scores)
            name, points = high_scores[score_index]

            rank = score_index + 1
            score_text = f"{rank:2}. {name[:15]:15} {points:06d}"

            y_pos = display_start + i
            if display_start <= y_pos < display_end:
                if i == 0 or i == display_height - 1:
                    color = Colors.WHITE
                else:
                    color = Colors.CYAN
                self.display.draw_centered_text(y_pos, score_text, color)

        self.display.draw_centered_text(GAME_HEIGHT - 3, "Press any key to continue", Colors.YELLOW)

    def render_game(self) -> None:
        """Render the main game."""
        self.display.draw_border()

        score = self.scoring.get_score()
        high_score = self.scoring.get_high_score()
        lives = self.game_state.get_lives()
        level = self.game_state.get_level()

        self.display.set_string(2, 1, f"Score: {score:06d}", Colors.YELLOW)
        self.display.set_string(22, 1, f"High: {high_score:06d}", Colors.CYAN)
        self.display.set_string(42, 1, f"Lives: {lives}", Colors.RED)
        self.display.set_string(GAME_WIDTH - 12, 1, f"Level: {level}", Colors.CYAN)

        if self.maze:
            self._render_maze()

        if self.pacman:
            self._render_pacman()

        if self.ghost_manager:
            self._render_ghosts()

        if self.score_popup:
            text, x, y, timer = self.score_popup
            maze_start_y = self._get_maze_start_y()
            maze_start_x = self._get_maze_start_x()
            screen_x = maze_start_x + x
            screen_y = maze_start_y + y - 1
            if 0 <= screen_y < GAME_HEIGHT:
                self.display.set_string(max(1, screen_x - len(text) // 2), screen_y, text, Colors.YELLOW)

    def _get_maze_start_x(self) -> int:
        """Get the X position where the maze starts (centered)."""
        if self.maze:
            return (GAME_WIDTH - self.maze.width) // 2
        return 1

    def _get_maze_start_y(self) -> int:
        """Get the Y position where the maze starts."""
        return 3

    def _get_max_maze_height(self) -> int:
        """Get the maximum height available for the maze."""
        return GAME_HEIGHT - 4

    def _render_maze(self) -> None:
        """Render the maze on the display."""
        maze_start_y = self._get_maze_start_y()
        maze_start_x = self._get_maze_start_x()

        max_render_height = min(self.maze.height, self._get_max_maze_height())

        for y in range(max_render_height):
            for x in range(self.maze.width):
                screen_x = maze_start_x + x
                screen_y = maze_start_y + y

                if 1 <= screen_x < GAME_WIDTH - 1 and 1 <= screen_y < GAME_HEIGHT - 1:
                    char = self.maze.get_cell_char(x, y)
                    color = self._get_maze_cell_color(char)
                    self.display.set_char(screen_x, screen_y, char, color)

    def _get_maze_cell_color(self, char: str) -> str:
        """Get the appropriate color for a maze cell character."""
        color_map: dict[str, str] = {
            Sprites.WALL: Colors.BLUE,
            Sprites.DOT: Colors.WHITE,
            Sprites.POWER_PELLET: Colors.YELLOW,
            Sprites.GHOST_DOOR: Colors.PINK,
        }
        return color_map.get(char, Colors.WHITE)

    def _render_pacman(self) -> None:
        """Render Pac-Man on the display."""
        if not self.pacman or not self.maze:
            return

        maze_start_y = self._get_maze_start_y()
        maze_start_x = self._get_maze_start_x()

        pac_pos = self.pacman.get_position()
        screen_x = maze_start_x + pac_pos.x
        screen_y = maze_start_y + pac_pos.y

        if 1 <= screen_x < GAME_WIDTH - 1 and 1 <= screen_y < GAME_HEIGHT - 1:
            sprite = self.pacman.get_sprite()
            self.display.set_char(screen_x, screen_y, sprite, Colors.YELLOW)

    def _render_ghosts(self) -> None:
        """Render all ghosts on the display."""
        if not self.ghost_manager or not self.maze:
            return

        maze_start_y = self._get_maze_start_y()
        maze_start_x = self._get_maze_start_x()

        for x, y, sprite, color in self.ghost_manager.get_ghost_positions():
            screen_x = maze_start_x + x
            screen_y = maze_start_y + y

            if 1 <= screen_x < GAME_WIDTH - 1 and 1 <= screen_y < GAME_HEIGHT - 1:
                self.display.set_char(screen_x, screen_y, sprite, color)

    def render_pause_overlay(self) -> None:
        """Render pause overlay with centered dialog box."""
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

    def _render_dialog_box(self, title: str, subtitle: str, width: int, height: int) -> None:
        """Render a centered dialog box with the given text."""
        box_x = (GAME_WIDTH - width) // 2
        box_y = GAME_HEIGHT // 2 - height // 2

        for y in range(box_y, box_y + height):
            for x in range(box_x, box_x + width):
                self.display.set_char(x, y, ' ', Colors.BLACK)

        self._draw_box(box_x, box_y, width, height, Colors.YELLOW)

        text_y = box_y + height // 2 - 1
        self.display.draw_centered_text(text_y, title, Colors.YELLOW)
        self.display.draw_centered_text(text_y + 1, subtitle, Colors.WHITE)

    def _draw_box(self, x: int, y: int, width: int, height: int, color: str) -> None:
        """Draw a box at the specified position."""
        for i in range(x, x + width):
            self.display.set_char(i, y, BorderChars.HORIZONTAL, color)
            self.display.set_char(i, y + height - 1, BorderChars.HORIZONTAL, color)

        for j in range(y, y + height):
            self.display.set_char(x, j, BorderChars.VERTICAL, color)
            self.display.set_char(x + width - 1, j, BorderChars.VERTICAL, color)

        self.display.set_char(x, y, BorderChars.TOP_LEFT, color)
        self.display.set_char(x + width - 1, y, BorderChars.TOP_RIGHT, color)
        self.display.set_char(x, y + height - 1, BorderChars.BOTTOM_LEFT, color)
        self.display.set_char(x + width - 1, y + height - 1, BorderChars.BOTTOM_RIGHT, color)

    def render_game_over(self) -> None:
        """Render game over screen."""
        self.display.draw_border()

        score = self.scoring.get_score()
        high_scores = self.scoring.get_high_scores()

        y = 3
        self.display.draw_centered_text(y, "HIGH SCORES", Colors.YELLOW)
        y += 2

        for i, (name, points) in enumerate(high_scores[:10]):
            rank = f"{i + 1:2}."
            score_text = f"{rank} {name[:15]:15} {points:06d}"
            color = Colors.CYAN if points == score else Colors.WHITE
            self.display.draw_centered_text(y + i, score_text, color)

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

        box_width = 24
        box_x = (GAME_WIDTH - box_width) // 2
        self.display.set_string(box_x, center_y + 2, "┌" + "─" * (box_width - 2) + "┐", Colors.WHITE)
        self.display.set_string(box_x, center_y + 3, "│" + " " * (box_width - 2) + "│", Colors.WHITE)
        self.display.set_string(box_x, center_y + 4, "└" + "─" * (box_width - 2) + "┘", Colors.WHITE)

        name_x = box_x + 2
        self.display.set_string(name_x, center_y + 3, self.player_name, Colors.YELLOW)

        cursor_x = name_x + len(self.player_name)
        if int(time.time() * 2) % 2:
            self.display.set_char(cursor_x, center_y + 3, "█", Colors.YELLOW)

        self.display.draw_centered_text(center_y + 6, "Press ENTER when done", Colors.WHITE)

    def _initialize_game(self) -> None:
        """Initialize the game objects for the current level."""
        layout = get_level(self.game_state.get_level())
        self.maze = Maze(layout)

        spawn_pos = self.maze.get_pacman_spawn()

        if not self.maze.is_walkable_for_pacman(spawn_pos.x, spawn_pos.y):
            spawn_pos = self._find_pacman_start_position()

        self.pacman = PacMan(spawn_pos.x, spawn_pos.y)
        self.previous_pacman_pos = spawn_pos

        self.ghost_manager = GhostManager(self.maze)

    def _find_pacman_start_position(self) -> Position:
        """Find a suitable starting position for Pac-Man."""
        start_x = self.maze.width // 2
        start_y = self.maze.height - 2

        search_radius = 5
        for y in range(start_y, max(self.maze.height // 2, 0), -1):
            for x in range(max(0, start_x - search_radius),
                           min(self.maze.width, start_x + search_radius + 1)):
                if self.maze.is_walkable_for_pacman(x, y):
                    return Position(x, y)

        for y in range(self.maze.height - 1, 0, -1):
            for x in range(self.maze.width):
                if self.maze.is_walkable_for_pacman(x, y):
                    return Position(x, y)

        return Position(1, 1)

    def _reset_positions(self) -> None:
        """Reset Pac-Man and ghost positions after death."""
        if self.pacman:
            self.pacman.reset()
            self.previous_pacman_pos = self.pacman.get_position()
        if self.ghost_manager:
            self.ghost_manager.reset()

    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.scoring.reset()
        self.game_state.reset()
        self._initialize_game()
