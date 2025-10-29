"""
Terminal display and rendering system.
Handles screen clearing, centering, and ASCII art rendering.
"""

import os
import shutil
from typing import List, Tuple
from .constants import GAME_WIDTH, GAME_HEIGHT, MIN_TERMINAL_WIDTH, MIN_TERMINAL_HEIGHT, Colors, BorderChars


class Display:
    """Manages terminal display and rendering."""
    
    def __init__(self):
        self.terminal_width, self.terminal_height = self._get_terminal_size()
        self.offset_x, self.offset_y = self._calculate_offsets()
        self.buffer = [[' ' for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]
        
    def _get_terminal_size(self) -> Tuple[int, int]:
        """Get the current terminal size."""
        try:
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except:
            return MIN_TERMINAL_WIDTH, MIN_TERMINAL_HEIGHT
    
    def _calculate_offsets(self) -> Tuple[int, int]:
        """Calculate offsets to center the game on screen."""
        offset_x = max(0, (self.terminal_width - GAME_WIDTH) // 2)
        offset_y = max(0, (self.terminal_height - GAME_HEIGHT) // 2)
        return offset_x, offset_y
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def hide_cursor(self):
        """Hide the terminal cursor."""
        print('\033[?25l', end='', flush=True)
    
    def show_cursor(self):
        """Show the terminal cursor."""
        print('\033[?25h', end='', flush=True)
    
    def clear_buffer(self):
        """Clear the display buffer."""
        for y in range(GAME_HEIGHT):
            for x in range(GAME_WIDTH):
                self.buffer[y][x] = ' '
    
    def set_char(self, x: int, y: int, char: str, color: str = Colors.WHITE):
        """Set a character in the display buffer with color."""
        if 0 <= x < GAME_WIDTH and 0 <= y < GAME_HEIGHT:
            self.buffer[y][x] = f"{color}{char}{Colors.RESET}"
    
    def set_string(self, x: int, y: int, text: str, color: str = Colors.WHITE):
        """Set a string in the display buffer starting at position."""
        for i, char in enumerate(text):
            if x + i < GAME_WIDTH:
                self.set_char(x + i, y, char, color)
    
    def render(self):
        """Render the buffer to the terminal."""
        # Move cursor to top-left of game area
        print(f'\033[{self.offset_y + 1};{self.offset_x + 1}H', end='')
        
        for y, row in enumerate(self.buffer):
            # Move cursor to beginning of line
            print(f'\033[{self.offset_y + y + 1};{self.offset_x + 1}H', end='')
            print(''.join(row), end='')
        
        # Ensure cursor position is controlled
        print(f'\033[{self.offset_y + GAME_HEIGHT + 1};1H', end='', flush=True)
    
    def draw_border(self):
        """Draw a border around the game area."""
        # Top and bottom borders
        for x in range(GAME_WIDTH):
            self.set_char(x, 0, BorderChars.HORIZONTAL, Colors.WHITE)
            self.set_char(x, GAME_HEIGHT - 1, BorderChars.HORIZONTAL, Colors.WHITE)
        
        # Left and right borders  
        for y in range(GAME_HEIGHT):
            self.set_char(0, y, BorderChars.VERTICAL, Colors.WHITE)
            self.set_char(GAME_WIDTH - 1, y, BorderChars.VERTICAL, Colors.WHITE)
        
        # Corners
        self.set_char(0, 0, BorderChars.TOP_LEFT, Colors.WHITE)
        self.set_char(GAME_WIDTH - 1, 0, BorderChars.TOP_RIGHT, Colors.WHITE)
        self.set_char(0, GAME_HEIGHT - 1, BorderChars.BOTTOM_LEFT, Colors.WHITE)
        self.set_char(GAME_WIDTH - 1, GAME_HEIGHT - 1, BorderChars.BOTTOM_RIGHT, Colors.WHITE)
    
    def draw_centered_text(self, y: int, text: str, color: str = Colors.WHITE):
        """Draw text centered horizontally at the given y position."""
        x = max(0, (GAME_WIDTH - len(text)) // 2)
        self.set_string(x, y, text, color)
    
    def get_game_bounds(self) -> Tuple[int, int, int, int]:
        """Get the playable area bounds (excluding border)."""
        return 1, 1, GAME_WIDTH - 2, GAME_HEIGHT - 2


class MockDisplay(Display):
    """Mock display for testing."""
    
    def __init__(self):
        self.terminal_width = GAME_WIDTH
        self.terminal_height = GAME_HEIGHT
        self.offset_x = 0
        self.offset_y = 0
        self.buffer = [[' ' for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]
        self.rendered_frames = []
    
    def clear_screen(self):
        """Mock clear screen."""
        pass
    
    def hide_cursor(self):
        """Mock hide cursor."""
        pass
    
    def show_cursor(self):
        """Mock show cursor."""
        pass
    
    def render(self):
        """Mock render - store frame for testing."""
        import re
        frame = []
        for row in self.buffer:
            # Strip all ANSI color codes for testing
            clean_row = ''
            for char in row:
                # Remove all ANSI escape sequences
                clean_char = re.sub(r'\033\[[0-9;]*m', '', char)
                clean_row += clean_char
            frame.append(clean_row)
        self.rendered_frames.append(frame)
    
    def get_last_frame(self) -> List[str]:
        """Get the last rendered frame."""
        if self.rendered_frames:
            return self.rendered_frames[-1]
        return [' ' * GAME_WIDTH for _ in range(GAME_HEIGHT)]
