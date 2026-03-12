"""
Input handling for keyboard controls.
Supports both standard arrow keys and left-handed WASD controls.
"""
from __future__ import annotations

import select
import sys
import termios
import tty

from ..core.types import Direction, DirectionType


class Keys:
    """Key constants for input handling."""
    W: str = "w"
    A: str = "a"
    S: str = "s"
    D: str = "d"
    SPACE: str = " "
    QUIT: str = "q"


class InputHandler:
    """Handles keyboard input for the game."""

    def __init__(self) -> None:
        self.old_settings: list[int] | None = None
        self._setup_terminal()

    def _setup_terminal(self) -> None:
        """Setup terminal for raw input mode."""
        if sys.stdin.isatty():
            self.old_settings = termios.tcgetattr(sys.stdin.fileno())
            tty.setraw(sys.stdin.fileno())

    def cleanup(self) -> None:
        """Restore terminal settings."""
        if self.old_settings is not None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_settings)

    def get_key(self) -> str | None:
        """
        Get a single key press without blocking.
        Returns None if no key is pressed.
        """
        if not sys.stdin.isatty():
            return None

        if select.select([sys.stdin], [], [], 0) == ([], [], []):
            return None

        ch = sys.stdin.read(1)

        if ch == '\x1b':
            try:
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    arrow_keys = {
                        'A': 'up',
                        'B': 'down',
                        'C': 'right',
                        'D': 'left'
                    }
                    if ch3 in arrow_keys:
                        return arrow_keys[ch3]
                return 'escape'
            except Exception:
                return 'escape'

        return ch.lower()

    def key_to_direction(self, key: str) -> DirectionType:
        """Convert key press to direction vector."""
        key_mapping: dict[str, DirectionType] = {
            'up': Direction.UP,
            'down': Direction.DOWN,
            'left': Direction.LEFT,
            'right': Direction.RIGHT,
            Keys.W: Direction.UP,
            Keys.S: Direction.DOWN,
            Keys.A: Direction.LEFT,
            Keys.D: Direction.RIGHT,
        }

        return key_mapping.get(key, Direction.NONE)

    def is_quit_key(self, key: str) -> bool:
        """Check if the key is a quit command."""
        return key == Keys.QUIT or key == 'escape'

    def is_pause_key(self, key: str) -> bool:
        """Check if the key is a pause command."""
        return key == Keys.SPACE


class MockInputHandler(InputHandler):
    """Mock input handler for testing."""

    def __init__(self) -> None:
        self.key_queue: list[str] = []
        self.old_settings = None

    def _setup_terminal(self) -> None:
        """Override to avoid terminal setup in tests."""
        pass

    def cleanup(self) -> None:
        """Override to avoid terminal cleanup in tests."""
        pass

    def add_key(self, key: str) -> None:
        """Add a key to the input queue for testing."""
        self.key_queue.append(key)

    def get_key(self) -> str | None:
        """Get the next key from the queue."""
        if self.key_queue:
            return self.key_queue.pop(0)
        return None
