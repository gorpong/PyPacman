"""
Input handling for keyboard controls.
Supports both standard arrow keys and left-handed WASD controls.
"""

import sys
import termios
import tty
from typing import Optional
from .constants import Keys, Direction


class InputHandler:
    """Handles keyboard input for the game."""
    
    def __init__(self):
        self.old_settings = None
        self._setup_terminal()
        
    def _setup_terminal(self):
        """Setup terminal for raw input mode."""
        if sys.stdin.isatty():
            self.old_settings = termios.tcgetattr(sys.stdin.fileno())
            tty.setraw(sys.stdin.fileno())
    
    def cleanup(self):
        """Restore terminal settings."""
        if self.old_settings is not None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_settings)
    
    def get_key(self) -> Optional[str]:
        """
        Get a single key press without blocking.
        Returns None if no key is pressed.
        """
        if not sys.stdin.isatty():
            return None
            
        import select
        
        # Check if input is available
        if select.select([sys.stdin], [], [], 0) == ([], [], []):
            return None
            
        ch = sys.stdin.read(1)
        
        # Handle escape sequences (arrow keys)
        if ch == '\x1b':
            # Give a bit more time for the rest of the sequence to arrive
            # Arrow keys send ESC [ A/B/C/D, so we need to read 2 more chars
            if select.select([sys.stdin], [], [], 0.1) != ([], [], []):
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    # Now read the direction character
                    if select.select([sys.stdin], [], [], 0.1) != ([], [], []):
                        ch3 = sys.stdin.read(1)
                        # Arrow key mappings
                        arrow_keys = {
                            'A': Keys.UP,
                            'B': Keys.DOWN, 
                            'C': Keys.RIGHT,
                            'D': Keys.LEFT
                        }
                        if ch3 in arrow_keys:
                            return arrow_keys[ch3]
                    # If we got '[' but no direction, it's an incomplete sequence
                    # Return None instead of ESC to avoid false quits
                    return None
                else:
                    # ESC followed by something other than '[' - could be Alt+key
                    # Return None to ignore these sequences
                    return None
            # Pure ESC press with nothing following
            return Keys.ESCAPE
        
        return ch.lower()
    
    def key_to_direction(self, key: str) -> Direction:
        """Convert key press to direction vector."""
        key_mapping = {
            # Standard arrow keys
            Keys.UP: Direction.UP,
            Keys.DOWN: Direction.DOWN,
            Keys.LEFT: Direction.LEFT,
            Keys.RIGHT: Direction.RIGHT,
            
            # Left-handed alternatives
            Keys.W: Direction.UP,
            Keys.S: Direction.DOWN,
            Keys.A: Direction.LEFT,
            Keys.D: Direction.RIGHT,
        }
        
        return key_mapping.get(key, Direction.NONE)
    
    def is_quit_key(self, key: str) -> bool:
        """Check if the key is a quit command."""
        return key in [Keys.ESCAPE, Keys.QUIT]
    
    def is_pause_key(self, key: str) -> bool:
        """Check if the key is a pause command."""
        return key == Keys.SPACE


class MockInputHandler(InputHandler):
    """Mock input handler for testing."""
    
    def __init__(self):
        self.key_queue = []
        self.old_settings = None
    
    def _setup_terminal(self):
        """Override to avoid terminal setup in tests."""
        pass
    
    def cleanup(self):
        """Override to avoid terminal cleanup in tests."""
        pass
    
    def add_key(self, key: str):
        """Add a key to the input queue for testing."""
        self.key_queue.append(key)
    
    def get_key(self) -> Optional[str]:
        """Get the next key from the queue."""
        if self.key_queue:
            return self.key_queue.pop(0)
        return None
